from __future__ import annotations

"""Bounded Notion lifecycle and projection services.

The provider boundary deliberately models Notion as an external projection and
read-only knowledge source.  It does not make provider content authoritative,
and it never exposes the credential used by the Core-side adapter.
"""

import hashlib
import json
import os
import re
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _local_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex}"

START = "<!-- PRIME_MANAGED_START -->"
END = "<!-- PRIME_MANAGED_END -->"
REGION_START = "<!-- PRIME_MANAGED_REGION:{region}:START -->"
REGION_END = "<!-- PRIME_MANAGED_REGION:{region}:END -->"
SELF_WRITE_PREFIX = "PRIME-WRITE/"


class NotionProviderError(RuntimeError):
    def __init__(self, code: str, message: str, retryable: bool = False):
        super().__init__(message)
        self.code = code
        self.retryable = retryable


@dataclass
class NotionPage:
    page_id: str
    title: str
    content: str
    parent_id: str | None = None
    revision: int = 1
    archived: bool = False
    last_write_id: str | None = None


class NotionProvider(Protocol):
    def health(self) -> dict[str, Any]: ...
    def create_page(self, parent_id: str, title: str, content: str, idempotency_key: str) -> NotionPage: ...
    def get_page(self, page_id: str) -> NotionPage: ...
    def update_region(self, page_id: str, region: str, expected_hash: str | None, content: str, write_id: str) -> NotionPage: ...
    def create_history_page(self, parent_id: str, title: str, content: str, idempotency_key: str) -> NotionPage: ...


class InMemoryNotionProvider:
    """Deterministic local provider double for lifecycle and failure tests."""

    def __init__(self) -> None:
        self.pages: dict[str, NotionPage] = {}
        self.idempotent_creates: dict[str, str] = {}
        self.fail_mode: str | None = None
        self.lost_response_once = False
        self._counter = 0

    def _fail(self) -> None:
        if self.fail_mode == "timeout":
            raise NotionProviderError("TIMEOUT", "provider timed out", retryable=True)
        if self.fail_mode == "rate_limit":
            raise NotionProviderError("RATE_LIMIT", "provider rate limited request", retryable=True)
        if self.fail_mode == "access_denied":
            raise NotionProviderError("ACCESS_DENIED", "provider denied access", retryable=False)
        if self.fail_mode == "unavailable":
            raise NotionProviderError("UNAVAILABLE", "provider is unavailable", retryable=True)

    def health(self) -> dict[str, Any]:
        if self.fail_mode in {"timeout", "unavailable", "rate_limit"}:
            return {"status": "DEGRADED", "code": self.fail_mode.upper()}
        if self.fail_mode == "access_denied":
            return {"status": "REAUTH_REQUIRED", "code": "ACCESS_DENIED"}
        return {"status": "CONNECTED", "workspace_id": "local-test-workspace", "capabilities": ["read", "write"]}

    def _new_page(self, parent_id: str, title: str, content: str) -> NotionPage:
        self._counter += 1
        page = NotionPage(f"notion-local-{self._counter}", title, content, parent_id)
        self.pages[page.page_id] = page
        return page

    def create_page(self, parent_id: str, title: str, content: str, idempotency_key: str) -> NotionPage:
        self._fail()
        if idempotency_key in self.idempotent_creates:
            return self.pages[self.idempotent_creates[idempotency_key]]
        page = self._new_page(parent_id, title, content)
        self.idempotent_creates[idempotency_key] = page.page_id
        if self.lost_response_once:
            self.lost_response_once = False
            raise NotionProviderError("LOST_RESPONSE", "response lost after successful create", retryable=True)
        return page

    def get_page(self, page_id: str) -> NotionPage:
        self._fail()
        page = self.pages.get(page_id)
        if not page or page.archived:
            raise NotionProviderError("PAGE_MISSING", "Notion page is missing", retryable=False)
        return page

    def update_region(self, page_id: str, region: str, expected_hash: str | None, content: str, write_id: str) -> NotionPage:
        self._fail()
        page = self.get_page(page_id)
        if page.last_write_id == write_id:
            return page
        start_marker = REGION_START.format(region=region)
        end_marker = REGION_END.format(region=region)
        start = page.content.find(start_marker)
        end = page.content.find(end_marker)
        if start < 0 or end < start:
            raise NotionProviderError("CONFLICT", "managed region is missing or ambiguous")
        current = page.content[start + len(start_marker):end].strip()
        if expected_hash and hashlib.sha256(current.encode()).hexdigest() != expected_hash:
            raise NotionProviderError("CONFLICT", "managed region was manually edited")
        replacement = f"{start_marker}\n{content.strip()}\n{end_marker}"
        page.content = page.content[:start] + replacement + page.content[end + len(end_marker):]
        page.revision += 1
        page.last_write_id = write_id
        return page

    def create_history_page(self, parent_id: str, title: str, content: str, idempotency_key: str) -> NotionPage:
        return self.create_page(parent_id, title, content, idempotency_key)

    def append_text(self, page_id: str, content: str) -> None:
        self._fail()
        page = self.get_page(page_id)
        page.content += "\n" + content
        page.revision += 1

    def archive_page(self, page_id: str) -> None:
        self._fail()
        page = self.pages.get(page_id)
        if not page:
            raise NotionProviderError("PAGE_MISSING", "Notion page is missing")
        page.archived = True


class NotionApiProvider:
    """Production NotionApiClient-backed provider for PRIME lifecycle services.

    The lifecycle service owns ordering, projection state, and recovery. This
    adapter owns only translation between Notion blocks and the narrow provider
    protocol, with bounded idempotency markers for retry/restart recovery.
    """

    is_external = True

    def __init__(self, client: Any):
        self.client = client
        self._idempotent_pages: dict[str, str] = {}

    @staticmethod
    def _error(exc: Exception) -> NotionProviderError:
        status = getattr(exc, "status", 503)
        retryable = bool(getattr(exc, "retryable", False))
        code = {401: "ACCESS_DENIED", 403: "ACCESS_DENIED", 404: "PAGE_MISSING", 409: "CONFLICT", 429: "RATE_LIMIT"}.get(status, "UNAVAILABLE" if retryable else "PROVIDER_ERROR")
        return NotionProviderError(code, "Notion provider request failed", retryable=retryable)

    @staticmethod
    def _rich_text(block: dict[str, Any]) -> str:
        payload = block.get(block.get("type", ""), {}) if isinstance(block, dict) else {}
        parts = payload.get("rich_text", []) if isinstance(payload, dict) else []
        return "".join(item.get("plain_text") or item.get("text", {}).get("content", "") for item in parts if isinstance(item, dict))

    @classmethod
    def _blocks(cls, content: str) -> list[dict[str, Any]]:
        lines = [line for line in content.splitlines() if line.strip()]
        return [{"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": line[:2000]}}]}} for line in (lines or ["PRIME content"])]

    @classmethod
    def _title(cls, page: dict[str, Any]) -> str:
        properties = page.get("properties", {}) if isinstance(page, dict) else {}
        for prop in properties.values():
            if isinstance(prop, dict) and prop.get("type") == "title":
                return "".join(item.get("plain_text", "") for item in prop.get("title", []))
        return "PRIME Project Record"

    def _page(self, page_id: str) -> NotionPage:
        try:
            page = self.client.retrieve_page(page_id)
            blocks = self.client.retrieve_children(page_id).get("results", [])
        except Exception as exc:
            raise self._error(exc) from exc
        content = "\n".join(self._rich_text(block) for block in blocks if isinstance(block, dict) and block.get("type"))
        digits = re.sub(r"\D", "", str(page.get("last_edited_time", "")))
        archived = bool(page.get("archived", False) or page.get("in_trash", False))
        if archived:
            raise NotionProviderError("PAGE_MISSING", "Notion page is archived", retryable=False)
        return NotionPage(page_id, self._title(page), content, (page.get("parent") or {}).get("page_id"), revision=int(digits[-9:] or "1"), archived=False)

    def health(self) -> dict[str, Any]:
        try:
            return {**self.client.provider_health(), "capabilities": ["read", "write", "search"]}
        except Exception as exc:
            return {"status": "DEGRADED", "error_code": type(exc).__name__}

    def create_page(self, parent_id: str, title: str, content: str, idempotency_key: str) -> NotionPage:
        marker = f"<!-- PRIME_IDEMPOTENCY:{hashlib.sha256(idempotency_key.encode()).hexdigest()[:24]} -->"
        try:
            known_id = self._idempotent_pages.get(idempotency_key)
            if known_id:
                return self._page(known_id)
            # Search makes retry safe even after Core/provider adapter restart.
            matches = self.client.search_pages(marker).get("results", [])
            for match in matches[:20]:
                if not isinstance(match, dict) or not match.get("id"):
                    continue
                candidate = self._page(match["id"])
                # Notion search is relevance-ranked, not an exact-key lookup.
                # Require the marker in fetched page content before treating a
                # result as the prior idempotent creation.
                if marker in candidate.content:
                    self._idempotent_pages[idempotency_key] = candidate.page_id
                    return candidate
            properties = {"title": {"title": [{"type": "text", "text": {"content": title[:2000]}}]}}
            parent = {"type": "workspace", "workspace": True} if parent_id == "workspace" else {"type": "page_id", "page_id": parent_id}
            payload = self.client.create_page(parent, properties, self._blocks(marker + "\n" + content))
            page = self._page(payload["id"])
            self._idempotent_pages[idempotency_key] = page.page_id
            return page
        except NotionProviderError:
            raise
        except Exception as exc:
            raise self._error(exc) from exc

    def get_page(self, page_id: str) -> NotionPage:
        return self._page(page_id)

    def update_region(self, page_id: str, region: str, expected_hash: str | None, content: str, write_id: str) -> NotionPage:
        try:
            self._page(page_id)
            blocks = self.client.retrieve_children(page_id).get("results", [])
            texts = [self._rich_text(block) for block in blocks]
            start_marker = REGION_START.format(region=region)
            end_marker = REGION_END.format(region=region)
            starts = [i for i, text in enumerate(texts) if text.strip() == start_marker]
            ends = [i for i, text in enumerate(texts) if text.strip() == end_marker]
            if len(starts) != 1 or len(ends) != 1 or ends[0] != starts[0] + 2:
                raise NotionProviderError("CONFLICT", "managed region is missing or ambiguous")
            current = texts[starts[0] + 1].strip()
            if expected_hash and hashlib.sha256(current.encode()).hexdigest() != expected_hash:
                raise NotionProviderError("CONFLICT", "managed region was manually edited")
            self.client.update_block(blocks[starts[0] + 1]["id"], {"paragraph": {"rich_text": [{"type": "text", "text": {"content": content.strip()[:2000]}}]}})
            return self._page(page_id)
        except NotionProviderError:
            raise
        except Exception as exc:
            raise self._error(exc) from exc

    def create_history_page(self, parent_id: str, title: str, content: str, idempotency_key: str) -> NotionPage:
        return self.create_page(parent_id, title, content, idempotency_key)

    def append_text(self, page_id: str, content: str) -> None:
        try:
            self.client.append_children(page_id, self._blocks(content))
        except Exception as exc:
            raise self._error(exc) from exc

    def archive_page(self, page_id: str) -> None:
        try:
            self.client.archive_page(page_id)
        except Exception as exc:
            raise self._error(exc) from exc


@dataclass
class _ProjectState:
    project_id: str
    credential_ref: str | None = None
    status: str = "UNCONFIGURED"
    page_id: str | None = None
    parent_id: str | None = None
    latest_source_rank: int = 0
    latest_source_revision: str | None = None
    managed_hashes: dict[str, str] = field(default_factory=dict)
    projection_revisions: list[dict[str, Any]] = field(default_factory=list)
    jobs: dict[str, dict[str, Any]] = field(default_factory=dict)
    sources: dict[str, dict[str, Any]] = field(default_factory=dict)
    history_pages: dict[str, dict[str, Any]] = field(default_factory=dict)
    admitted_memory: dict[str, dict[str, Any]] = field(default_factory=dict)


class NotionLifecycleService:
    """Project-scoped lifecycle, Documentation Agent and Knowledge Source boundary."""

    def __init__(self, provider: NotionProvider | None = None, history_limit: int = 20, state_path: Path | None = None, settings: Any | None = None, event_sink: Any | None = None):
        self.provider = provider or InMemoryNotionProvider()
        self.history_limit = max(1, history_limit)
        self.state_path = state_path
        self.settings = settings
        self.event_sink = event_sink
        self.projects: dict[str, _ProjectState] = {}
        self._load()

    def _event(self, event_type: str, project_id: str, payload: dict[str, Any]) -> None:
        if self.event_sink:
            self.event_sink(event_type, payload, project_id=project_id, dedupe_key=f"notion:{event_type}:{project_id}:{payload.get('page_id') or payload.get('binding_id') or payload.get('documentation_run_id') or payload.get('period')}")

    def _record_binding(self, state: _ProjectState, status: str, page_id: str | None = None, content_hash: str | None = None, metadata: dict[str, Any] | None = None) -> None:
        if not self.settings:
            return
        from .db import transaction
        with transaction(self.settings) as db:
            db.execute("INSERT INTO prime_core.notion_projects(project_id,page_id,connection_status,managed_content_hash,last_synced_at,updated_at) VALUES (%s,%s,%s,%s,CASE WHEN %s='CONNECTED' THEN now() ELSE NULL END,now()) ON CONFLICT (project_id) DO UPDATE SET page_id=COALESCE(EXCLUDED.page_id,prime_core.notion_projects.page_id),connection_status=EXCLUDED.connection_status,managed_content_hash=COALESCE(EXCLUDED.managed_content_hash,prime_core.notion_projects.managed_content_hash),last_synced_at=EXCLUDED.last_synced_at,updated_at=now()", (state.project_id, page_id, "CONNECTED" if status in {"BOUND", "SYNCED"} else ("CONFLICT" if status == "CONFLICT" else "DEGRADED"), content_hash, status))
            revision_id = _local_id("notionrev")
            db.execute("INSERT INTO prime_core.notion_projection_revisions(projection_revision_id,project_id,content_hash,source_set,sync_status,observed_at,metadata) VALUES (%s,%s,%s,%s,%s,now(),%s)", (revision_id, state.project_id, content_hash or "", json.dumps([]), "SYNCED" if status == "SYNCED" else ("CONFLICT" if status == "CONFLICT" else "DEGRADED"), json.dumps(metadata or {})))

    def _persist(self) -> None:
        if not self.state_path:
            return
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {project_id: vars(state) for project_id, state in self.projects.items()}
        temporary = self.state_path.with_name(self.state_path.name + ".tmp")
        temporary.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")
        os.replace(temporary, self.state_path)

    def _load(self) -> None:
        if not self.state_path or not self.state_path.is_file():
            return
        try:
            payload = json.loads(self.state_path.read_text(encoding="utf-8"))
            for project_id, values in payload.items():
                self.projects[project_id] = _ProjectState(project_id=project_id, **{key: value for key, value in values.items() if key != "project_id"})
        except (OSError, ValueError, TypeError):
            # A corrupt projection snapshot must degrade the Notion projection,
            # not prevent the repository and .agent authority from starting.
            self.projects = {}

    def _state(self, project_id: str) -> _ProjectState:
        return self.projects.setdefault(project_id, _ProjectState(project_id))

    @staticmethod
    def _markers(regions: dict[str, str] | None = None) -> str:
        regions = regions or {
            "PROJECT_OVERVIEW": "Notion Project Record",
            "CURRENT_STATUS": "Status: INITIALIZING",
            "PROGRESS": "Progress: pending first assessment",
            "RECENT_HISTORY": "Recent history: none",
        }
        parts: list[str] = []
        for key, content in regions.items():
            parts.append(REGION_START.format(region=key) + "\n" + content + "\n" + REGION_END.format(region=key))
        return "\n\n".join(parts)

    @staticmethod
    def _redact(content: str) -> str:
        patterns = [
            (r"(?i)(api[_-]?key|token|password|secret|private[_-]?key)\s*[:=]\s*[^\s]+", r"\1: [REDACTED]"),
            (r"-----BEGIN [A-Z ]+PRIVATE KEY-----.*?-----END [A-Z ]+PRIVATE KEY-----", "[REDACTED PRIVATE KEY]"),
        ]
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        return content

    def configure(self, project_id: str, credential_ref: str) -> dict[str, Any]:
        if not credential_ref or credential_ref.startswith(("sk-", "ntn_", "secret_")):
            raise ValueError("Notion requires a Core-owned credential reference, not a raw secret")
        state = self._state(project_id)
        state.credential_ref = credential_ref
        health = self.provider.health()
        state.status = health.get("status", "DEGRADED")
        self._persist()
        return self.health(project_id)

    def health(self, project_id: str) -> dict[str, Any]:
        state = self._state(project_id)
        health = self.provider.health() if state.credential_ref else {"status": "UNCONFIGURED"}
        if state.page_id and health.get("status") == "CONNECTED":
            state.status = "BOUND"
        elif health.get("status") != "CONNECTED":
            state.status = health.get("status", "DEGRADED")
        return {"project_id": project_id, "status": state.status, "provider": {k: v for k, v in health.items() if k != "credential"}, "page_id": state.page_id}

    def create_project_record(self, project_id: str, parent_id: str, title: str, idempotency_key: str | None = None) -> dict[str, Any]:
        state = self._state(project_id)
        if not state.credential_ref:
            raise NotionProviderError("UNCONFIGURED", "Notion provider is not configured")
        if state.page_id:
            return {"status": "BOUND", "page_id": state.page_id, "idempotent": True}
        key = idempotency_key or f"project-record/{project_id}"
        state.status = "BINDING"
        try:
            page = self.provider.create_page(parent_id, title, self._markers(), key)
        except NotionProviderError as exc:
            if exc.code == "LOST_RESPONSE":
                try:
                    page = self.provider.create_page(parent_id, title, self._markers(), key)
                except NotionProviderError as retry:
                    state.status = "DEGRADED" if retry.retryable else "CONFLICT"
                    return {"status": state.status, "retryable": retry.retryable, "error_code": retry.code}
            else:
                state.status = "DEGRADED" if exc.retryable else ("REAUTH_REQUIRED" if exc.code == "ACCESS_DENIED" else "CONFLICT")
                return {"status": state.status, "retryable": exc.retryable, "error_code": exc.code}
        state.page_id, state.parent_id, state.status = page.page_id, parent_id, "BOUND"
        state.projection_revisions.append({"source_revision": "initial", "provider_revision": page.revision, "content_hash": hashlib.sha256(page.content.encode()).hexdigest(), "self_write": True})
        self._persist()
        self._record_binding(state, "BOUND", page.page_id, state.projection_revisions[-1]["content_hash"], {"source_revision": "initial", "page_revision": page.revision})
        self._event("notion.project_record.bound", project_id, {"page_id": page.page_id, "status": "BOUND"})
        return {"status": "BOUND", "page_id": page.page_id, "page_revision": page.revision, "idempotent": False}

    def bind_existing(self, project_id: str, page_id: str, expected_parent_id: str | None = None) -> dict[str, Any]:
        state = self._state(project_id)
        if not state.credential_ref:
            raise NotionProviderError("UNCONFIGURED", "Notion provider is not configured")
        try:
            page = self.provider.get_page(page_id)
        except NotionProviderError as exc:
            state.status = "PAGE_MISSING" if exc.code == "PAGE_MISSING" else "ACCESS_LOST"
            return {"status": state.status, "error_code": exc.code}
        if expected_parent_id and page.parent_id != expected_parent_id:
            state.status = "CONFLICT"
            return {"status": "CONFLICT", "reason": "page parent/location does not match approved target"}
        if not self._has_unambiguous_regions(page.content):
            state.status = "CONFLICT"
            return {"status": "CONFLICT", "reason": "existing content has no safe PRIME-managed regions"}
        state.page_id, state.parent_id, state.status = page.page_id, page.parent_id, "BOUND"
        self._persist()
        return {"status": "BOUND", "page_id": page.page_id, "page_revision": page.revision}

    @staticmethod
    def _has_unambiguous_regions(content: str) -> bool:
        starts = re.findall(r"<!-- PRIME_MANAGED_REGION:([A-Z0-9_]{1,50}):START -->", content)
        ends = re.findall(r"<!-- PRIME_MANAGED_REGION:([A-Z0-9_]{1,50}):END -->", content)
        return len(starts) == 4 and len(ends) == 4 and len(set(starts)) == 4 and set(starts) == set(ends)

    def document(self, project_id: str, sections: dict[str, str], source_revision: str, source_rank: int = 0, documentation_run_id: str | None = None) -> dict[str, Any]:
        state = self._state(project_id)
        if not state.page_id:
            return {"status": "DEGRADED", "retryable": False, "error_code": "PROJECT_RECORD_MISSING"}
        run_id = documentation_run_id or uuid.uuid4().hex
        if source_rank < state.latest_source_rank:
            return {"status": "STALE_JOB_REJECTED", "documentation_run_id": run_id, "source_revision": source_revision}
        # Reserve the source ordering before the provider call.  If the call
        # fails, a retry of this same rank remains valid; an older job cannot
        # overtake the failed/newer projection.
        state.latest_source_rank = max(state.latest_source_rank, source_rank)
        write_id = SELF_WRITE_PREFIX + run_id
        try:
            page = self.provider.get_page(state.page_id)
            for region, raw in sections.items():
                if not re.fullmatch(r"[A-Z0-9_]{1,50}", region):
                    raise ValueError("invalid managed region")
                rendered = self._redact(raw)
                expected = state.managed_hashes.get(region)
                page = self.provider.update_region(page.page_id, region, expected, rendered, write_id)
                state.managed_hashes[region] = hashlib.sha256(rendered.strip().encode()).hexdigest()
        except NotionProviderError as exc:
            state.status = "CONFLICT" if exc.code == "CONFLICT" else ("ACCESS_LOST" if exc.code == "ACCESS_DENIED" else "DEGRADED")
            state.jobs[run_id] = {"status": "RETRYABLE" if exc.retryable else "ACTION_REQUIRED", "source_revision": source_revision, "error_code": exc.code}
            self._persist()
            return {"status": state.status, "retryable": exc.retryable, "documentation_run_id": run_id, "error_code": exc.code}
        state.latest_source_rank = source_rank
        state.latest_source_revision = source_revision
        projection = {"documentation_run_id": run_id, "project_id": project_id, "source_commit": source_revision, "authority_revision": source_revision, "managed_sections": sorted(sections), "rendered_hash": hashlib.sha256(page.content.encode()).hexdigest(), "provider_revision": page.revision, "self_write_id": write_id, "status": "SYNCED"}
        state.projection_revisions.append(projection)
        state.status = "BOUND"
        state.jobs[run_id] = {"status": "SUCCEEDED", "source_revision": source_revision}
        self._persist()
        self._record_binding(state, "SYNCED", page.page_id, projection["rendered_hash"], projection)
        self._event("notion.documentation.projected", project_id, projection)
        return {"status": "SYNCED", "page_id": page.page_id, "page_revision": page.revision, "projection": projection}

    def attach_source(self, project_id: str, source_binding_id: str, page_id: str) -> dict[str, Any]:
        state = self._state(project_id)
        if source_binding_id in state.sources:
            return {**state.sources[source_binding_id], "idempotent": True}
        try:
            page = self.provider.get_page(page_id)
        except NotionProviderError as exc:
            state.sources[source_binding_id] = {"binding_id": source_binding_id, "page_id": page_id, "status": "ACCESS_LOST" if exc.code == "ACCESS_DENIED" else "UNAVAILABLE"}
            return state.sources[source_binding_id]
        binding = {"binding_id": source_binding_id, "project_id": project_id, "page_id": page_id, "status": "ATTACHED", "revision": str(page.revision), "content_hash": hashlib.sha256(page.content.encode()).hexdigest(), "observed_at": _utcnow().isoformat()}
        state.sources[source_binding_id] = binding
        self._persist()
        self._event("notion.source.attached", project_id, binding)
        return binding

    def refresh_source(self, project_id: str, source_binding_id: str) -> dict[str, Any]:
        state = self._state(project_id)
        binding = state.sources.get(source_binding_id)
        if not binding:
            raise KeyError(source_binding_id)
        try:
            page = self.provider.get_page(binding["page_id"])
        except NotionProviderError as exc:
            binding["status"] = "ACCESS_LOST" if exc.code == "ACCESS_DENIED" else ("DELETED" if exc.code == "PAGE_MISSING" else "UNAVAILABLE")
            return {**binding, "retrieval": "RETRACTED"}
        content = page.content
        binding.update({"status": "ATTACHED", "revision": str(page.revision), "content_hash": hashlib.sha256(content.encode()).hexdigest(), "observed_at": _utcnow().isoformat()})
        self._persist()
        return {**binding, "retrieval": "CURRENT", "content": content, "provenance": {"project_id": project_id, "source_binding_id": source_binding_id, "page_id": page.page_id, "block_identity": page.page_id, "observed_revision": str(page.revision), "content_hash": binding["content_hash"], "observed_at": binding["observed_at"]}}

    def detach_source(self, project_id: str, source_binding_id: str, purge_history: bool = False) -> dict[str, Any]:
        state = self._state(project_id)
        binding = state.sources.get(source_binding_id)
        if not binding:
            raise KeyError(source_binding_id)
        binding.update({"status": "DETACHED", "retrieval": "RETRACTED", "detached_at": _utcnow().isoformat(), "purged": purge_history})
        for memory in state.admitted_memory.values():
            if memory.get("source_binding_id") == source_binding_id:
                memory["reconciliation_status"] = "REVIEW_REQUIRED"
        self._persist()
        self._event("notion.source.detached", project_id, binding)
        return dict(binding)

    def admit_memory_reference(self, project_id: str, memory_id: str, source_binding_id: str) -> dict[str, Any]:
        if source_binding_id not in self._state(project_id).sources:
            raise KeyError(source_binding_id)
        item = {"memory_id": memory_id, "source_binding_id": source_binding_id, "reconciliation_status": "CURRENT"}
        self._state(project_id).admitted_memory[memory_id] = item
        self._persist()
        return item

    def reconcile(self, project_id: str) -> dict[str, Any]:
        state = self._state(project_id)
        results: list[dict[str, Any]] = []
        if state.page_id:
            try:
                page = self.provider.get_page(state.page_id)
                state.status = "BOUND"
                results.append({"kind": "project_record", "status": "CURRENT", "page_revision": page.revision})
            except NotionProviderError as exc:
                state.status = "PAGE_MISSING" if exc.code == "PAGE_MISSING" else ("ACCESS_LOST" if exc.code == "ACCESS_DENIED" else "DEGRADED")
                results.append({"kind": "project_record", "status": state.status, "error_code": exc.code})
        for binding_id in list(state.sources):
            refreshed = self.refresh_source(project_id, binding_id)
            results.append({"kind": "knowledge_source", "binding_id": binding_id, "status": refreshed["status"], "retrieval": refreshed.get("retrieval")})
        self._persist()
        return {"project_id": project_id, "status": state.status, "results": results, "queued_jobs": [dict(job, job_id=job_id) for job_id, job in state.jobs.items() if job.get("status") != "SUCCEEDED"]}

    def rollover_history(self, project_id: str, period: str, managed_content: str, source_revision_start: str, source_revision_end: str) -> dict[str, Any]:
        state = self._state(project_id)
        if not state.page_id:
            raise NotionProviderError("PROJECT_RECORD_MISSING", "Project Record is not bound")
        if period in state.history_pages:
            return {**state.history_pages[period], "idempotent": True}
        key = f"history/{project_id}/{period}"
        try:
            page = self.provider.create_history_page(state.page_id, f"PRIME History — {period}", self._redact(managed_content), key)
        except NotionProviderError as exc:
            if exc.code != "LOST_RESPONSE":
                raise
            page = self.provider.create_history_page(state.page_id, f"PRIME History — {period}", self._redact(managed_content), key)
        result = {"project_id": project_id, "history_page_id": page.page_id, "period": period, "source_revision_start": source_revision_start, "source_revision_end": source_revision_end, "managed_content_hash": hashlib.sha256(managed_content.encode()).hexdigest(), "created_at": _utcnow().isoformat(), "notion_target_id": page.page_id}
        state.history_pages[period] = result
        self._persist()
        self._event("notion.history.rolled_over", project_id, result)
        return result

    def backup_metadata(self, project_id: str) -> dict[str, Any]:
        state = self._state(project_id)
        return {"project_id": project_id, "credential_state": "REPROVISION_REQUIRED", "credential_ref": state.credential_ref, "status": state.status, "page_id": state.page_id, "parent_id": state.parent_id, "managed_hashes": dict(state.managed_hashes), "projection_revisions": list(state.projection_revisions), "sources": [dict(item) for item in state.sources.values()], "history_pages": list(state.history_pages.values()), "admitted_memory": list(state.admitted_memory.values())}


class NotionProjectionService:
    """Compatibility projection used by the Phase 7 database tests."""

    def __init__(self, settings: Any):
        self.settings = settings

    def project(self, project_id: str, existing_content: str, managed_content: str, available: bool = True) -> dict[str, Any]:
        if not available:
            self._record(project_id, "", "DEGRADED", {"reason": "notion unavailable"}, None)
            return {"status": "DEGRADED", "retryable": True}
        if START not in existing_content or END not in existing_content or existing_content.index(START) > existing_content.index(END):
            self._record(project_id, "", "CONFLICT", {"reason": "managed markers missing or ambiguous"}, existing_content)
            return {"status": "CONFLICT", "retryable": False}
        replacement = f"{START}\n{managed_content.strip()}\n{END}"
        content = existing_content[: existing_content.index(START)] + replacement + existing_content[existing_content.index(END) + len(END):]
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        self._record(project_id, content_hash, "SYNCED", {"managed_hash": hashlib.sha256(managed_content.encode()).hexdigest()}, content)
        return {"status": "SYNCED", "content": content, "content_hash": content_hash, "idempotent": content == existing_content}

    def _record(self, project_id: str, content_hash: str, status: str, metadata: dict[str, Any], rendered_content: str | None) -> None:
        from .db import transaction
        from .history_primitives import record_historical_snapshot
        connection_status = {"SYNCED": "CONNECTED", "DEGRADED": "DEGRADED", "CONFLICT": "CONFLICT"}[status]
        with transaction(self.settings) as db:
            db.execute("INSERT INTO prime_core.notion_projects(project_id,connection_status,managed_content_hash,last_synced_at,updated_at) VALUES (%s,%s,%s,CASE WHEN %s='SYNCED' THEN now() ELSE NULL END,now()) ON CONFLICT (project_id) DO UPDATE SET connection_status=EXCLUDED.connection_status,managed_content_hash=EXCLUDED.managed_content_hash,last_synced_at=EXCLUDED.last_synced_at,updated_at=now()", (project_id, connection_status, content_hash or None, status))
            observed = _utcnow()
            revision_id = _local_id("notionrev")
            db.execute("INSERT INTO prime_core.notion_projection_revisions(projection_revision_id,project_id,content_hash,source_set,sync_status,observed_at,metadata,rendered_content,managed_section_key,notion_target_refs) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (revision_id, project_id, content_hash, json.dumps([]), status, observed, json.dumps(metadata), rendered_content, "PRIME_MANAGED", json.dumps({})))
            record_historical_snapshot(db, project_id, "NOTION_PROJECTION", revision_id, metadata.get("source_revision"), {"projection_revision_id": revision_id, "content_hash": content_hash, "sync_status": status, "rendered_content": rendered_content, "metadata": metadata}, observed, content_hash or None)
