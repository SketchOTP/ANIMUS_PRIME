from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path
from typing import Any

from .history_service import HistoryService
from .memory_service import MemoryService, SECRET_PATTERN


class AuthorityMemoryAdmission:
    """Project-bound admission of consequential .agent records after indexing."""

    RECORD_SPECS = {
        ".agent/DIRECTIVES.md": "DECISION",
        ".agent/OUTCOMES.md": "OBSERVATION",
        ".agent/LEARNINGS.md": "LEARNING",
        ".agent/RECORD.md": "DECISION",
    }
    HEADING = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)

    def __init__(self, settings: Any, service: Any):
        self.settings = settings
        self.service = service
        self.history = HistoryService(settings)
        self.memory = MemoryService(settings)

    def admit(self, project_id: str, root: Path, source_revision: str) -> dict[str, Any]:
        branch = self._branch(root)
        records: list[dict[str, Any]] = []
        for relative_path, content_class in self.RECORD_SPECS.items():
            path = root / relative_path
            if not path.is_file():
                continue
            try:
                content = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError):
                continue
            parsed = self._records(content)
            existing = self._existing_admissions(project_id, relative_path)
            if not existing:
                # Automatic admission is an observation delta, not warm start.
                # Historical seeding is a separate, explicit lifecycle policy.
                continue
            last_known_index = max(
                (index for index, (identifier, _body) in enumerate(parsed) if identifier in existing),
                default=-1,
            )
            for index, (identifier, body) in enumerate(parsed):
                if index < last_known_index:
                    continue
                content_hash = hashlib.sha256(body.encode("utf-8")).hexdigest()
                prior = existing.get(identifier)
                if prior and prior["content_hash"] == content_hash and index == last_known_index:
                    records.append({"source_path": relative_path, "record_id": identifier, "status": "DUPLICATE"})
                    continue
                if SECRET_PATTERN.search(body):
                    records.append({"source_path": relative_path, "record_id": identifier, "status": "REJECTED", "reason": "secret-sensitive content rejected"})
                    continue
                supersedes_memory_id = prior["memory_id"] if prior else None
                revision_kind = "AUTHORITY_RECORD_REVISION" if supersedes_memory_id else "AUTHORITY_RECORD_INITIAL"
                metadata = {
                    "automatic": True,
                    "admission_policy": {
                        "durability": "HIGH",
                        "novelty": "CONTENT_HASH_AND_RECORD_ID",
                        "future_usefulness": "CONSEQUENTIAL_AUTHORITY_RECORD",
                        "evidence_quality": "CANONICAL_AGENT_FILE",
                        "project_relevance": "PROJECT_BOUND",
                        "sensitivity": "SECRET_FILTERED",
                    },
                    "authority_record_id": identifier,
                    "authority_source_path": relative_path,
                    "authority_source_hash": content_hash,
                    "canonical_commit": source_revision,
                    "branch": branch,
                    "worktree": "MAIN_WORKTREE",
                    "record_kind": revision_kind,
                }
                try:
                    source = self._source_reference(project_id, relative_path, source_revision, content_hash, metadata)
                    event = self.service.emit_event(
                        "AUTHORITY_MEMORY_ADMISSION",
                        {"record_id": identifier, "source_path": relative_path, "source_hash": content_hash},
                        project_id=project_id,
                        dedupe_key=f"authority-memory:{project_id}:{identifier}:{content_hash}",
                        source_revision=source_revision,
                        source_ref=source["source_reference_id"],
                    )
                    metadata["event_id"] = event["event_id"]
                    stored = self.memory.store(
                        project_id,
                        body,
                        content_class,
                        source_revision=source_revision,
                        source_reference_id=source["source_reference_id"],
                        branch_context=branch,
                        supersedes_memory_id=supersedes_memory_id,
                        correction_reason=revision_kind if supersedes_memory_id else None,
                        metadata=metadata,
                    )
                    records.append({"source_path": relative_path, "record_id": identifier, **stored, "event_id": event["event_id"], "source_reference_id": source["source_reference_id"], "supersedes_memory_id": supersedes_memory_id})
                except Exception as exc:
                    records.append({"source_path": relative_path, "record_id": identifier, "status": "DEGRADED", "reason": type(exc).__name__})
        status = "CURRENT" if all(item.get("status") not in {"DEGRADED", "UNAVAILABLE"} for item in records) else "DEGRADED"
        return {"status": status, "records": records}

    def _source_reference(self, project_id: str, relative_path: str, source_revision: str, content_hash: str, metadata: dict[str, Any]) -> dict[str, Any]:
        from .db import connect
        with connect(self.settings) as db:
            existing = db.execute(
                "SELECT * FROM prime_core.source_references WHERE project_id=%s AND source_class='AUTHORITY' AND locator=%s AND revision=%s AND content_hash=%s ORDER BY captured_at DESC LIMIT 1",
                (project_id, relative_path, source_revision, content_hash),
            ).fetchone()
        if existing:
            return dict(existing)
        try:
            return self.history.create_source_reference(project_id, "AUTHORITY", relative_path, source_revision, content_hash, metadata)
        except Exception:
            with connect(self.settings) as db:
                existing = db.execute(
                    "SELECT * FROM prime_core.source_references WHERE project_id=%s AND source_class='AUTHORITY' AND locator=%s AND revision=%s AND content_hash=%s ORDER BY captured_at DESC LIMIT 1",
                    (project_id, relative_path, source_revision, content_hash),
                ).fetchone()
            if not existing:
                raise
            return dict(existing)

    def _existing_admissions(self, project_id: str, source_path: str) -> dict[str, dict[str, Any]]:
        from .db import connect
        with connect(self.settings) as db:
            rows = db.execute(
                "SELECT memory_id, metadata->>'authority_record_id' AS record_id, "
                "metadata->>'authority_source_hash' AS content_hash, status "
                "FROM prime_core.memory_records WHERE project_id=%s "
                "AND metadata->>'authority_source_path'=%s "
                "AND status NOT IN ('TOMBSTONED') ORDER BY created_at",
                (project_id, source_path),
            ).fetchall()
        result: dict[str, dict[str, Any]] = {}
        for row in rows:
            identifier = row.get("record_id")
            if identifier:
                result[identifier] = dict(row)
        return result

    @classmethod
    def _records(cls, content: str) -> list[tuple[str, str]]:
        matches = list(cls.HEADING.finditer(content))
        records: list[tuple[str, str]] = []
        for index, match in enumerate(matches):
            end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
            identifier = match.group(1).split(" - ", 1)[0].strip()
            body = content[match.start():end].strip()
            if identifier and len(body) >= 40:
                records.append((identifier, body))
        return records

    @staticmethod
    def _branch(root: Path) -> str:
        try:
            return subprocess.run(["git", "-C", str(root), "branch", "--show-current"], check=False, capture_output=True, text=True, timeout=5).stdout.strip() or "DETACHED"
        except (OSError, subprocess.SubprocessError):
            return "UNKNOWN"
