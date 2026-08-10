from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Any

from .db import connect, transaction
from .evidence_validation import validate_evidence, validate_filename, validate_mime_type, validate_privacy_class
from .service import _id, now


class HistoryService:
    def __init__(self, settings: Any):
        self.settings = settings

    def record_evidence(
        self,
        project_id: str,
        source_type: str,
        locator: str,
        content: bytes | None = None,
        privacy_class: str = "PROJECT_PRIVATE",
    ) -> dict[str, Any]:
        if not validate_privacy_class(privacy_class):
            raise ValueError("unsupported Evidence privacy class")
        digest = hashlib.sha256(content).hexdigest() if content is not None else None
        size = len(content) if content is not None else None
        parser_status = "READY" if validate_evidence(content or b"", source_type) else "REJECTED"
        with transaction(self.settings) as db:
            row = db.execute("INSERT INTO prime_core.evidence_records(evidence_id,project_id,source_type,locator,content_hash,captured_at,parser_status,privacy_class,size_bytes) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING *", (_id("evidence"), project_id, source_type, locator, digest, now(), parser_status, privacy_class, size)).fetchone()
            return dict(row)

    def store_uploaded_evidence(
        self,
        project_id: str,
        filename: str,
        content: bytes,
        mime_type: str,
        privacy_class: str = "PROJECT_PRIVATE",
    ) -> dict[str, Any]:
        if not validate_filename(filename):
            raise ValueError("Evidence filename must be a simple leaf name")
        if not validate_mime_type(mime_type):
            raise ValueError("unsupported Evidence MIME type")
        if not validate_privacy_class(privacy_class):
            raise ValueError("unsupported Evidence privacy class")
        if not validate_evidence(content, "UPLOAD"):
            raise ValueError("Evidence content failed safe validation")
        root = Path(os.getenv("PRIME_EVIDENCE_ROOT", ".prime-evidence")).resolve()
        target_dir = (root / project_id).resolve()
        if root not in target_dir.parents:
            raise ValueError("invalid Evidence storage root")
        target_dir.mkdir(parents=True, exist_ok=True)
        digest = hashlib.sha256(content).hexdigest()
        target = target_dir / f"{digest}-{filename}"
        target.write_bytes(content)
        with transaction(self.settings) as db:
            row = db.execute("INSERT INTO prime_core.evidence_records(evidence_id,project_id,source_type,locator,content_hash,captured_at,parser_status,index_status,privacy_class,storage_path,mime_type,size_bytes) VALUES (%s,%s,'UPLOAD',%s,%s,%s,'READY','UNAVAILABLE',%s,%s,%s,%s) RETURNING *", (_id("evidence"), project_id, filename, digest, now(), privacy_class, str(target), mime_type.strip().lower(), len(content))).fetchone()
            return dict(row)

    def list_evidence(self, project_id: str, include_retracted: bool = False) -> list[dict[str, Any]]:
        predicate = "" if include_retracted else " AND retracted_at IS NULL"
        with transaction(self.settings) as db:
            rows = db.execute(
                "SELECT * FROM prime_core.evidence_records WHERE project_id=%s" + predicate + " ORDER BY captured_at DESC",
                (project_id,),
            ).fetchall()
            return [dict(row) for row in rows]

    def retract_evidence(self, project_id: str, evidence_id: str, reason: str) -> dict[str, Any]:
        if not reason.strip():
            raise ValueError("Evidence retraction reason is required")
        with transaction(self.settings) as db:
            row = db.execute(
                "UPDATE prime_core.evidence_records SET retracted_at=%s,retraction_reason=%s WHERE project_id=%s AND evidence_id=%s AND retracted_at IS NULL RETURNING *",
                (now(), reason.strip()[:500], project_id, evidence_id),
            ).fetchone()
            if not row:
                raise KeyError("Evidence record not found or already retracted")
            return dict(row)

    def time_lens(self, project_id: str, as_of: str) -> dict[str, Any]:
        with transaction(self.settings) as db:
            row = db.execute("SELECT source_revision FROM prime_core.repository_files WHERE project_id=%s AND source_revision=%s LIMIT 1", (project_id, as_of)).fetchone()
            status = "EXACT" if row else "UNAVAILABLE"
            db.execute("INSERT INTO prime_core.time_lens_checkpoints(checkpoint_id,project_id,as_of,reconstruction_status,source_set,created_at) VALUES (%s,%s,%s,%s,'[]',%s)", (_id("checkpoint"), project_id, as_of, status, now()))
            return {"project_id": project_id, "as_of": as_of, "reconstruction_status": status}

    def fork(self, source_project_id: str, source_revision: str, name: str) -> dict[str, Any]:
        timestamp = now()
        with transaction(self.settings) as db:
            if not db.execute("SELECT 1 FROM prime_core.repository_files WHERE project_id=%s AND source_revision=%s LIMIT 1", (source_project_id, source_revision)).fetchone():
                raise ValueError("fork requires an observed canonical revision")
            new_project_id = _id("project")
            db.execute("INSERT INTO prime_core.projects(project_id,name,lifecycle_state,connectivity_state,freshness_state,work_condition,created_at,updated_at) VALUES (%s,%s,'DRAFT','OFFLINE','UNKNOWN','REVIEW_REQUIRED',%s,%s)", (new_project_id, name, timestamp, timestamp))
            fork_id = _id("fork")
            db.execute("INSERT INTO prime_core.project_forks(fork_id,source_project_id,new_project_id,source_revision,created_at) VALUES (%s,%s,%s,%s,%s)", (fork_id, source_project_id, new_project_id, source_revision, timestamp))
            return {"fork_id": fork_id, "new_project_id": new_project_id, "source_project_id": source_project_id, "source_revision": source_revision, "memory_copy_status": "NONE"}
