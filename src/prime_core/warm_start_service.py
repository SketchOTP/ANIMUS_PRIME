from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

from .db import connect
from .history_service import HistoryService
from .memory_service import MemoryService, SECRET_PATTERN


class WarmStartService:
    """Explicit, bounded admission of operator-selected continuity context."""

    AUTHORITY_PATHS = (
        ".agent/PROJECT_GOAL.md",
        ".agent/CURRENT.md",
        ".agent/OUTCOMES.md",
        ".agent/LEARNINGS.md",
        ".agent/RECORD.md",
        ".agent/DIRECTIVES.md",
    )
    AUTHORITY_CONTENT_CLASSES = {
        ".agent/PROJECT_GOAL.md": "CONSTRAINT",
        ".agent/CURRENT.md": "OBSERVATION",
        ".agent/OUTCOMES.md": "OBSERVATION",
        ".agent/LEARNINGS.md": "LEARNING",
        ".agent/RECORD.md": "DECISION",
        ".agent/DIRECTIVES.md": "DECISION",
    }
    MAX_AUTHORITY_BYTES = 40_000
    MAX_NOTION_BYTES = 40_000

    def __init__(self, settings: Any, service: Any):
        self.settings = settings
        self.service = service
        self.history = HistoryService(settings)
        self.memory = MemoryService(settings)

    def _binding(self, project_id: str) -> dict[str, Any]:
        with connect(self.settings) as db:
            row = db.execute(
                "SELECT r.canonical_path,b.canonical_revision,b.node_id "
                "FROM prime_core.project_bindings b "
                "JOIN prime_core.repositories r ON r.repository_id=b.repository_id "
                "WHERE b.project_id=%s",
                (project_id,),
            ).fetchone()
        if not row:
            raise KeyError("project has no repository binding")
        return dict(row)

    def _root(self, project_id: str) -> tuple[Path, dict[str, Any]]:
        binding = self._binding(project_id)
        root = Path(binding["canonical_path"]).expanduser().resolve(strict=True)
        if not root.is_dir():
            raise ValueError("project repository root is not a directory")
        return root, binding

    @staticmethod
    def _revision(root: Path, configured: str | None) -> str:
        try:
            result = subprocess.run(
                ["git", "-C", str(root), "rev-parse", "HEAD"],
                check=False,
                capture_output=True,
                text=True,
                timeout=8,
            )
            return result.stdout.strip() or configured or "UNKNOWN"
        except (OSError, subprocess.SubprocessError):
            return configured or "UNKNOWN"

    @classmethod
    def _authority_candidate(cls, root: Path, relative_path: str, revision: str) -> dict[str, Any]:
        if relative_path not in cls.AUTHORITY_PATHS:
            raise ValueError(f"authority path is not selectable: {relative_path}")
        path = (root / relative_path).resolve()
        try:
            path.relative_to(root)
        except ValueError as exc:
            raise ValueError("authority path escapes repository root") from exc
        if not path.is_file():
            return {"source_class": "AUTHORITY", "locator": relative_path, "status": "UNAVAILABLE"}
        if path.stat().st_size > cls.MAX_AUTHORITY_BYTES:
            return {"source_class": "AUTHORITY", "locator": relative_path, "status": "SKIPPED", "reason": "bounded file size exceeded"}
        content = path.read_text(encoding="utf-8", errors="replace")
        return {
            "source_class": "AUTHORITY",
            "locator": relative_path,
            "status": "CURRENT",
            "revision": revision,
            "content_hash": hashlib.sha256(content.encode("utf-8")).hexdigest(),
            "size_bytes": len(content.encode("utf-8")),
            "preview": content[:320],
        }

    def _notion_candidates(self, project_id: str) -> list[dict[str, Any]]:
        with connect(self.settings) as db:
            rows = db.execute(
                "SELECT s.source_binding_id,s.page_id,s.page_url,s.status,s.observed_revision,s.observed_hash,s.observed_at,s.metadata,"
                "COALESCE(o.content->>'text','') AS content_text "
                "FROM prime_core.notion_knowledge_sources s "
                "LEFT JOIN LATERAL (SELECT content FROM prime_core.notion_source_observations o "
                "WHERE o.project_id=s.project_id AND o.source_binding_id=s.source_binding_id "
                "AND o.availability_status='CURRENT' ORDER BY o.observed_at DESC LIMIT 1) o ON TRUE "
                "WHERE s.project_id=%s ORDER BY s.observed_at DESC NULLS LAST",
                (project_id,),
            ).fetchall()
        candidates: list[dict[str, Any]] = []
        for row in rows:
            item = dict(row)
            content = item.pop("content_text", "") or ""
            item["source_class"] = "NOTION_KNOWLEDGE"
            item["classification"] = "NON_AUTHORITATIVE_KNOWLEDGE"
            item["content_available"] = bool(content) and item.get("status") == "ATTACHED"
            item["content_preview"] = content[:320] if item["content_available"] else ""
            item["status"] = "CURRENT" if item["content_available"] else (item.get("status") or "UNAVAILABLE")
            candidates.append(item)
        return candidates

    def preview(self, project_id: str, authority_paths: list[str] | None = None, notion_source_binding_ids: list[str] | None = None) -> dict[str, Any]:
        root, binding = self._root(project_id)
        revision = self._revision(root, binding.get("canonical_revision"))
        requested_authority = authority_paths if authority_paths is not None else list(self.AUTHORITY_PATHS)
        requested_notion = set(notion_source_binding_ids or [])
        authority = [self._authority_candidate(root, path, revision) for path in requested_authority]
        notion = [item for item in self._notion_candidates(project_id) if not requested_notion or item.get("source_binding_id") in requested_notion]
        return {
            "status": "READY",
            "project_id": project_id,
            "repository_revision": revision,
            "selection_required": True,
            "authority_candidates": authority,
            "notion_candidates": notion,
            "policy": {
                "selected_only": True,
                "repository_bulk_ingestion": False,
                "git_history_ingestion": False,
                "notion_bulk_ingestion": False,
                "notion_classification": "NON_AUTHORITATIVE_KNOWLEDGE",
                "deduplication": "CONTENT_HASH_AND_PROJECT",
            },
        }

    def _source_reference(self, project_id: str, source_class: str, locator: str, revision: str, content_hash: str, metadata: dict[str, Any]) -> dict[str, Any]:
        with connect(self.settings) as db:
            existing = db.execute(
                "SELECT * FROM prime_core.source_references WHERE project_id=%s AND source_class=%s AND locator=%s AND revision=%s AND content_hash=%s ORDER BY captured_at DESC LIMIT 1",
                (project_id, source_class, locator, revision, content_hash),
            ).fetchone()
        if existing:
            return dict(existing)
        return self.history.create_source_reference(project_id, source_class, locator, revision, content_hash, metadata)

    def _admit(self, project_id: str, content: str, content_class: str, source_class: str, locator: str, revision: str, content_hash: str, metadata: dict[str, Any]) -> dict[str, Any]:
        source = self._source_reference(project_id, source_class, locator, revision, content_hash, metadata)
        result = self.memory.store(
            project_id,
            content,
            content_class,
            source_revision=revision,
            source_reference_id=source["source_reference_id"],
            metadata={
                **metadata,
                "warm_start": True,
                "selected_by": "operator",
                "source_class": source_class,
                "source_locator": locator,
                "source_revision": revision,
                "source_hash": content_hash,
            },
        )
        result.update({"source_reference_id": source["source_reference_id"], "source_class": source_class, "locator": locator, "revision": revision, "content_hash": content_hash})
        self.service.emit_event(
            "WARM_START_MEMORY_ADMISSION",
            {"source_class": source_class, "locator": locator, "content_hash": content_hash, "status": result.get("status")},
            project_id=project_id,
            dedupe_key=f"warm-start:{project_id}:{source_class}:{locator}:{content_hash}",
            source_revision=revision,
            source_ref=source["source_reference_id"],
        )
        return result

    @classmethod
    def _content_class(cls, source_class: str, locator: str) -> str:
        if source_class == "AUTHORITY":
            return cls.AUTHORITY_CONTENT_CLASSES.get(locator, "OBSERVATION")
        return "OBSERVATION"

    def run(self, project_id: str, authority_paths: list[str], notion_source_binding_ids: list[str], confirm: bool = False) -> dict[str, Any]:
        if not confirm:
            raise ValueError("Warm Start requires explicit confirmation")
        if not authority_paths and not notion_source_binding_ids:
            raise ValueError("Warm Start requires at least one selected source")
        root, binding = self._root(project_id)
        revision = self._revision(root, binding.get("canonical_revision"))
        admitted: list[dict[str, Any]] = []
        skipped: list[dict[str, Any]] = []
        rejected: list[dict[str, Any]] = []
        for relative_path in list(dict.fromkeys(authority_paths)):
            candidate = self._authority_candidate(root, relative_path, revision)
            if candidate["status"] != "CURRENT":
                skipped.append(candidate)
                continue
            path = root / relative_path
            content = path.read_text(encoding="utf-8", errors="replace")
            if SECRET_PATTERN.search(content):
                rejected.append({**candidate, "status": "REJECTED", "reason": "secret-sensitive content rejected"})
                continue
            admitted.append(self._admit(project_id, content, self._content_class("AUTHORITY", relative_path), "AUTHORITY", relative_path, revision, candidate["content_hash"], {"authority_path": relative_path, "authority_classification": "AUTHORITATIVE"}))
        selected = set(notion_source_binding_ids)
        for candidate in self._notion_candidates(project_id):
            if candidate.get("source_binding_id") not in selected:
                continue
            if candidate.get("status") != "CURRENT" or not candidate.get("content_available"):
                skipped.append({"source_class": "NOTION_KNOWLEDGE", "source_binding_id": candidate.get("source_binding_id"), "status": candidate.get("status", "UNAVAILABLE"), "reason": "source is not current with readable content"})
                continue
            with connect(self.settings) as db:
                row = db.execute(
                    "SELECT content->>'text' AS text FROM prime_core.notion_source_observations WHERE project_id=%s AND source_binding_id=%s AND availability_status='CURRENT' ORDER BY observed_at DESC LIMIT 1",
                    (project_id, candidate["source_binding_id"]),
                ).fetchone()
            content = (row or {}).get("text", "") if row else ""
            if not content:
                skipped.append({"source_class": "NOTION_KNOWLEDGE", "source_binding_id": candidate.get("source_binding_id"), "status": "UNAVAILABLE", "reason": "current observation has no text"})
                continue
            if len(content.encode("utf-8")) > self.MAX_NOTION_BYTES:
                skipped.append({"source_class": "NOTION_KNOWLEDGE", "source_binding_id": candidate.get("source_binding_id"), "status": "SKIPPED", "reason": "bounded source size exceeded"})
                continue
            if SECRET_PATTERN.search(content):
                rejected.append({"source_class": "NOTION_KNOWLEDGE", "source_binding_id": candidate.get("source_binding_id"), "status": "REJECTED", "reason": "secret-sensitive content rejected"})
                continue
            admitted.append(self._admit(project_id, content, self._content_class("NOTION_KNOWLEDGE", candidate.get("page_url") or candidate.get("page_id") or candidate["source_binding_id"]), "NOTION_KNOWLEDGE", candidate.get("page_url") or candidate.get("page_id") or candidate["source_binding_id"], str(candidate.get("observed_revision") or "UNKNOWN"), str(candidate.get("observed_hash") or hashlib.sha256(content.encode()).hexdigest()), {"notion_source_binding_id": candidate["source_binding_id"], "notion_page_id": candidate.get("page_id"), "authority_classification": "NON_AUTHORITATIVE_KNOWLEDGE"}))
        status = "CURRENT" if not rejected and not any(item.get("status") in {"DEGRADED", "UNAVAILABLE"} for item in skipped) else "PARTIAL"
        return {"status": status, "project_id": project_id, "repository_revision": revision, "admitted": admitted, "skipped": skipped, "rejected": rejected, "selected_count": len(authority_paths) + len(notion_source_binding_ids), "admitted_count": len(admitted), "deduplicated_count": sum(1 for item in admitted if item.get("status") == "DUPLICATE"), "policy": {"selected_only": True, "repository_bulk_ingestion": False, "git_history_ingestion": False, "notion_bulk_ingestion": False}}
