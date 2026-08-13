from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path
from typing import Any

from .history_service import HistoryService
from .memory_service import MemoryService


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
            record = self._latest_record(content)
            if not record:
                continue
            identifier, body = record
            content_hash = hashlib.sha256(body.encode("utf-8")).hexdigest()
            if self._already_admitted(project_id, identifier, content_hash):
                records.append({"source_path": relative_path, "record_id": identifier, "status": "DUPLICATE"})
                continue
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
            }
            try:
                source = self.history.create_source_reference(project_id, "AUTHORITY", relative_path, source_revision, content_hash, metadata)
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
                    metadata=metadata,
                )
                records.append({"source_path": relative_path, "record_id": identifier, **stored, "event_id": event["event_id"], "source_reference_id": source["source_reference_id"]})
            except Exception as exc:
                records.append({"source_path": relative_path, "record_id": identifier, "status": "DEGRADED", "reason": type(exc).__name__})
        status = "CURRENT" if all(item.get("status") not in {"DEGRADED", "UNAVAILABLE"} for item in records) else "DEGRADED"
        return {"status": status, "records": records}

    def _already_admitted(self, project_id: str, identifier: str, content_hash: str) -> bool:
        from .db import connect
        with connect(self.settings) as db:
            return bool(db.execute("SELECT 1 FROM prime_core.memory_records WHERE project_id=%s AND metadata->>'authority_record_id'=%s AND metadata->>'authority_source_hash'=%s AND status NOT IN ('TOMBSTONED','SUPERSEDED') LIMIT 1", (project_id, identifier, content_hash)).fetchone())

    @classmethod
    def _latest_record(cls, content: str) -> tuple[str, str] | None:
        matches = list(cls.HEADING.finditer(content))
        if not matches:
            return None
        match = matches[-1]
        identifier = match.group(1).split(" - ", 1)[0].strip()
        body = content[match.start():].strip()
        return (identifier, body) if identifier and len(body) >= 40 else None

    @staticmethod
    def _branch(root: Path) -> str:
        try:
            return subprocess.run(["git", "-C", str(root), "branch", "--show-current"], check=False, capture_output=True, text=True, timeout=5).stdout.strip() or "DETACHED"
        except (OSError, subprocess.SubprocessError):
            return "UNKNOWN"
