from __future__ import annotations

import hashlib
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

from .db import connect, transaction
from .evidence_validation import (
    extract_safe_text,
    validate_evidence,
    validate_external_locator,
    validate_filename,
    validate_mime_type,
    validate_node_locator,
    validate_privacy_class,
)
from .service import _id, now
from .git_history import checkpoint_bundle_status, create_checkpoint_bundle
from .history_primitives import reconstruction_status


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
        source_revision: str | None = None,
    ) -> dict[str, Any]:
        if source_type == "EXTERNAL_REFERENCE" and not validate_external_locator(locator):
            raise ValueError("external Evidence references must be safe HTTPS URLs")
        if source_type == "NODE_PATH":
            roots = [item for item in os.getenv("PRIME_NODE_ALLOWED_ROOTS", "").split(os.pathsep) if item]
            if not validate_node_locator(locator, roots):
                raise ValueError("Node Evidence reference is outside approved roots")
        if not validate_privacy_class(privacy_class):
            raise ValueError("unsupported Evidence privacy class")
        digest = hashlib.sha256(content).hexdigest() if content is not None else None
        size = len(content) if content is not None else None
        parser_status = "READY" if validate_evidence(content or b"", source_type) else "REJECTED"
        with transaction(self.settings) as db:
            evidence_id = _id("evidence")
            captured = now()
            source_ref_id = _id("source")
            db.execute(
                "INSERT INTO prime_core.source_references(source_reference_id,project_id,source_class,locator,revision,content_hash,freshness_state,captured_at,metadata) VALUES (%s,%s,'EVIDENCE',%s,%s,%s,'CURRENT',%s,%s)",
                (source_ref_id, project_id, locator, source_revision, digest, captured, json.dumps({"source_type": source_type, "privacy_class": privacy_class})),
            )
            row = db.execute("INSERT INTO prime_core.evidence_records(evidence_id,project_id,source_type,locator,content_hash,captured_at,observed_at,parser_status,index_status,privacy_class,size_bytes,source_reference_id,immutable_identity,creator_type,creator_id,source_revision) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,'UNAVAILABLE',%s,%s,%s,%s,'operator','operator',%s) RETURNING *", (evidence_id, project_id, source_type, locator, digest, captured, captured, parser_status, privacy_class, size, source_ref_id, digest or locator, source_revision)).fetchone()
            return dict(row)

    def store_uploaded_evidence(
        self,
        project_id: str,
        filename: str,
        content: bytes,
        mime_type: str,
        privacy_class: str = "PROJECT_PRIVATE",
        source_revision: str | None = None,
    ) -> dict[str, Any]:
        if not validate_filename(filename):
            raise ValueError("Evidence filename must be a simple leaf name")
        if not validate_mime_type(mime_type):
            raise ValueError("unsupported Evidence MIME type")
        if not validate_privacy_class(privacy_class):
            raise ValueError("unsupported Evidence privacy class")
        if not validate_evidence(content, "UPLOAD"):
            raise ValueError("Evidence content failed safe validation")
        quota = int(os.getenv("PRIME_EVIDENCE_PROJECT_QUOTA_BYTES", str(500 * 1024 * 1024)))
        root = Path(os.getenv("PRIME_EVIDENCE_ROOT", ".prime-evidence")).resolve()
        target_dir = (root / project_id).resolve()
        if root not in target_dir.parents:
            raise ValueError("invalid Evidence storage root")
        target_dir.mkdir(parents=True, exist_ok=True)
        digest = hashlib.sha256(content).hexdigest()
        target = target_dir / f"{digest}-{filename}"
        target.write_bytes(content)
        extracted_text = extract_safe_text(content, mime_type)
        index_status = "READY" if extracted_text is not None else "UNAVAILABLE"
        with transaction(self.settings) as db:
            used = db.execute("SELECT COALESCE(SUM(size_bytes),0) AS total FROM prime_core.evidence_records WHERE project_id=%s AND retracted_at IS NULL", (project_id,)).fetchone()["total"]
            if int(used or 0) + len(content) > quota:
                target.unlink(missing_ok=True)
                raise ValueError("Evidence project quota exceeded")
            evidence_id = _id("evidence")
            captured = now()
            source_ref_id = _id("source")
            db.execute(
                "INSERT INTO prime_core.source_references(source_reference_id,project_id,source_class,locator,revision,content_hash,freshness_state,captured_at,metadata) VALUES (%s,%s,'EVIDENCE',%s,%s,%s,'CURRENT',%s,%s)",
                (source_ref_id, project_id, str(target), source_revision, digest, captured, json.dumps({"source_type": "UPLOAD", "filename": filename, "mime_type": mime_type.strip().lower()})),
            )
            row = db.execute("INSERT INTO prime_core.evidence_records(evidence_id,project_id,source_type,locator,content_hash,captured_at,observed_at,parser_status,index_status,privacy_class,storage_path,mime_type,size_bytes,source_reference_id,immutable_identity,creator_type,creator_id,extracted_text,source_revision) VALUES (%s,%s,'UPLOAD',%s,%s,%s,%s,'READY',%s,%s,%s,%s,%s,%s,%s,%s,'operator','operator',%s,%s) RETURNING *", (evidence_id, project_id, filename, digest, captured, captured, index_status, privacy_class, str(target), mime_type.strip().lower(), len(content), source_ref_id, digest, extracted_text, source_revision)).fetchone()
            return dict(row)

    def annotate_evidence(self, project_id: str, evidence_id: str, annotation: str) -> dict[str, Any]:
        if not annotation.strip():
            raise ValueError("Evidence annotation is required")
        with transaction(self.settings) as db:
            if not db.execute("SELECT 1 FROM prime_core.evidence_records WHERE project_id=%s AND evidence_id=%s", (project_id, evidence_id)).fetchone():
                raise KeyError("Evidence record not found")
            row = db.execute("INSERT INTO prime_core.evidence_annotations(annotation_id,project_id,evidence_id,annotation,created_at) VALUES (%s,%s,%s,%s,%s) RETURNING *", (_id("annotation"), project_id, evidence_id, annotation.strip()[:4000], now())).fetchone()
            return dict(row)

    def create_source_reference(
        self,
        project_id: str,
        source_class: str,
        locator: str,
        revision: str | None = None,
        content_hash: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if not source_class.strip() or not locator.strip():
            raise ValueError("SourceReference requires source class and locator")
        with transaction(self.settings) as db:
            row = db.execute(
                "INSERT INTO prime_core.source_references(source_reference_id,project_id,source_class,locator,revision,content_hash,freshness_state,captured_at,metadata) VALUES (%s,%s,%s,%s,%s,%s,'CURRENT',%s,%s) RETURNING *",
                (_id("source"), project_id, source_class.strip(), locator.strip(), revision, content_hash, now(), json.dumps(metadata or {})),
            ).fetchone()
            return dict(row)

    def cite_evidence(self, project_id: str, evidence_id: str, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
        with transaction(self.settings) as db:
            row = db.execute("SELECT * FROM prime_core.evidence_records WHERE project_id=%s AND evidence_id=%s", (project_id, evidence_id)).fetchone()
            if not row:
                raise KeyError("Evidence record not found")
            ref_id = row.get("source_reference_id")
            if not ref_id:
                ref_id = _id("source")
                db.execute("INSERT INTO prime_core.source_references(source_reference_id,project_id,source_class,locator,revision,content_hash,freshness_state,captured_at,metadata) VALUES (%s,%s,'EVIDENCE',%s,%s,%s,'CURRENT',%s,%s)", (ref_id, project_id, row["locator"], None, row["content_hash"], row["captured_at"], json.dumps(metadata or {})))
                db.execute("UPDATE prime_core.evidence_records SET source_reference_id=%s WHERE project_id=%s AND evidence_id=%s", (ref_id, project_id, evidence_id))
            return {"source_reference_id": ref_id, "evidence_id": evidence_id, "source_revision": row["content_hash"], "content_hash": row["content_hash"], "retracted": row.get("retracted_at") is not None}

    def link_evidence(self, project_id: str, evidence_id: str, relation_type: str, target_id: str) -> dict[str, Any]:
        if relation_type not in {"GOAL_ITEM", "VALIDATION", "DIRECTIVE", "COMMIT", "OUTCOME", "ANNOTATION"}:
            raise ValueError("unsupported Evidence relationship")
        with transaction(self.settings) as db:
            if not db.execute("SELECT 1 FROM prime_core.evidence_records WHERE project_id=%s AND evidence_id=%s", (project_id, evidence_id)).fetchone():
                raise KeyError("Evidence record not found")
            row = db.execute("INSERT INTO prime_core.evidence_links(evidence_link_id,project_id,evidence_id,relation_type,target_id,created_at) VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT (project_id,evidence_id,relation_type,target_id) DO UPDATE SET created_at=EXCLUDED.created_at RETURNING *", (_id("evidencelink"), project_id, evidence_id, relation_type, target_id, now())).fetchone()
            return dict(row)

    def resolve_source_reference(
        self,
        project_id: str,
        source_reference_id: str,
        current_revision: str | None = None,
        current_content_hash: str | None = None,
        source_available: bool = True,
    ) -> dict[str, Any]:
        with connect(self.settings) as db:
            row = db.execute("SELECT * FROM prime_core.source_references WHERE project_id=%s AND source_reference_id=%s", (project_id, source_reference_id)).fetchone()
        if not row:
            return {"source_reference_id": source_reference_id, "status": "UNAVAILABLE", "reason": "SOURCE_NOT_FOUND"}
        if not source_available:
            return {"source_reference_id": source_reference_id, "status": "CHANGED_HISTORICAL_CONTENT_UNAVAILABLE", "locator": row["locator"], "revision": row["revision"], "content_hash": row["content_hash"]}
        revision_match = current_revision is None or current_revision == row["revision"]
        hash_match = current_content_hash is None or current_content_hash == row["content_hash"]
        if revision_match and hash_match:
            return {"source_reference_id": source_reference_id, "status": "EXACT", "locator": row["locator"], "revision": row["revision"], "content_hash": row["content_hash"]}
        return {"source_reference_id": source_reference_id, "status": "HISTORICAL", "locator": row["locator"], "revision": row["revision"], "content_hash": row["content_hash"], "warning": "SOURCE_CHANGED"}

    def add_git_checkpoint(self, project_id: str, repository_path: str, commit_id: str, cache_root: str | None = None) -> dict[str, Any]:
        repo = Path(repository_path).resolve()
        if not repo.is_dir() or not (repo / ".git").exists():
            raise ValueError("Git checkpoint requires a working repository")
        root = Path(cache_root or os.getenv("PRIME_HISTORY_ROOT", ".prime-history")).resolve()
        target_dir = (root / project_id).resolve()
        if root not in target_dir.parents:
            raise ValueError("invalid Git checkpoint cache root")
        target_dir.mkdir(parents=True, exist_ok=True)
        bundle = target_dir / f"{commit_id}.bundle"
        bundle_result = create_checkpoint_bundle(str(repo), commit_id, str(bundle))
        verified_commit = bundle_result["commit_id"]
        bundle_hash = bundle_result["content_hash"]
        with transaction(self.settings) as db:
            row = db.execute("INSERT INTO prime_core.git_history_checkpoints(checkpoint_id,project_id,commit_id,bundle_locator,coverage_status,content_hash,captured_at,metadata,repository_path,verified_at,retained) VALUES (%s,%s,%s,%s,'EXACT',%s,%s,%s,%s,%s,%s) ON CONFLICT (project_id,commit_id) DO UPDATE SET bundle_locator=EXCLUDED.bundle_locator,coverage_status='EXACT',content_hash=EXCLUDED.content_hash,verified_at=EXCLUDED.verified_at,retained=TRUE RETURNING *", (_id("gitcheckpoint"), project_id, verified_commit, str(bundle), bundle_hash, now(), json.dumps({"preservation": "git-bundle", "source": "canonical-commit"}), str(repo), now(), True)).fetchone()
            db.execute("INSERT INTO prime_core.source_references(source_reference_id,project_id,source_class,locator,revision,content_hash,freshness_state,captured_at,metadata) VALUES (%s,%s,'GIT_COMMIT',%s,%s,%s,'CURRENT',%s,%s) ON CONFLICT (source_reference_id) DO NOTHING", (_id("source"), project_id, str(repo), verified_commit, bundle_hash, now(), json.dumps({"checkpoint_id": row["checkpoint_id"]})))
            return dict(row)

    def git_checkpoint_status(self, project_id: str, commit_id: str) -> dict[str, Any]:
        with connect(self.settings) as db:
            row = db.execute("SELECT * FROM prime_core.git_history_checkpoints WHERE project_id=%s AND commit_id=%s AND retained=TRUE", (project_id, commit_id)).fetchone()
        if not row:
            return {"commit_id": commit_id, "coverage_status": "UNAVAILABLE"}
        bundle = Path(row["bundle_locator"])
        if not bundle.is_file():
            return {"commit_id": commit_id, "coverage_status": "UNAVAILABLE", "reason": "bundle_missing"}
        digest = hashlib.sha256(bundle.read_bytes()).hexdigest()
        return {"commit_id": commit_id, "coverage_status": checkpoint_bundle_status(str(bundle), row["content_hash"]), "bundle_locator": str(bundle), "content_hash": digest}

    def historical_context(self, project_id: str, as_of: str) -> dict[str, Any]:
        """Return only records observed at the selected boundary; never current state."""
        cutoff: datetime | None = None
        try:
            cutoff = datetime.fromisoformat(as_of.replace("Z", "+00:00"))
        except ValueError:
            pass
        with connect(self.settings) as db:
            if cutoff:
                evidence = db.execute("SELECT evidence_id,source_reference_id,content_hash,captured_at,retracted_at FROM prime_core.evidence_records WHERE project_id=%s AND captured_at<=%s ORDER BY captured_at", (project_id, cutoff)).fetchall()
                progress = db.execute("SELECT assessment_id,repository_revision,progress_percent,created_at FROM prime_core.progress_assessments WHERE project_id=%s AND created_at<=%s ORDER BY created_at", (project_id, cutoff)).fetchall()
                memories = db.execute("SELECT memory_id,source_revision,status,created_at FROM prime_core.memory_records WHERE project_id=%s AND created_at<=%s ORDER BY created_at", (project_id, cutoff)).fetchall()
                notion = db.execute("SELECT projection_revision_id,content_hash,sync_status,observed_at FROM prime_core.notion_projection_revisions WHERE project_id=%s AND observed_at<=%s ORDER BY observed_at", (project_id, cutoff)).fetchall()
            else:
                evidence = db.execute("SELECT evidence_id,source_reference_id,content_hash,captured_at,retracted_at FROM prime_core.evidence_records WHERE project_id=%s AND source_revision=%s", (project_id, as_of)).fetchall()
                progress = db.execute("SELECT assessment_id,repository_revision,progress_percent,created_at FROM prime_core.progress_assessments WHERE project_id=%s AND repository_revision=%s", (project_id, as_of)).fetchall()
                memories = db.execute("SELECT memory_id,source_revision,status,created_at FROM prime_core.memory_records WHERE project_id=%s AND source_revision=%s", (project_id, as_of)).fetchall()
                notion = []
            statuses = {
                "authority": "EXACT" if (db.execute("SELECT 1 FROM prime_core.authority_revisions WHERE project_id=%s AND observed_at<=%s LIMIT 1", (project_id, cutoff)).fetchone() if cutoff else db.execute("SELECT 1 FROM prime_core.authority_revisions WHERE project_id=%s AND source_hash=%s LIMIT 1", (project_id, as_of)).fetchone()) else "UNAVAILABLE",
                "goal": "EXACT" if (db.execute("SELECT 1 FROM prime_core.goal_revisions WHERE project_id=%s AND created_at<=%s LIMIT 1", (project_id, cutoff)).fetchone() if cutoff else db.execute("SELECT 1 FROM prime_core.goal_revisions WHERE project_id=%s AND content_hash=%s LIMIT 1", (project_id, as_of)).fetchone()) else "UNAVAILABLE",
                "evidence": "EXACT" if evidence else "UNAVAILABLE",
                "progress": "EXACT" if progress else "UNAVAILABLE",
                "memory": "EXACT" if memories else "UNAVAILABLE",
                "notion": "EXACT" if notion else "UNAVAILABLE",
                "brain": "EXACT" if (db.execute("SELECT 1 FROM prime_core.brain_snapshots WHERE project_id=%s AND created_at<=%s LIMIT 1", (project_id, cutoff)).fetchone() if cutoff else db.execute("SELECT 1 FROM prime_core.brain_snapshots WHERE project_id=%s AND source_revision=%s LIMIT 1", (project_id, as_of)).fetchone()) else "UNAVAILABLE",
                "git": "EXACT" if (db.execute("SELECT 1 FROM prime_core.git_history_checkpoints WHERE project_id=%s AND captured_at<=%s AND retained=TRUE LIMIT 1", (project_id, cutoff)).fetchone() if cutoff else db.execute("SELECT 1 FROM prime_core.git_history_checkpoints WHERE project_id=%s AND commit_id=%s AND retained=TRUE LIMIT 1", (project_id, as_of)).fetchone()) else "UNAVAILABLE",
            }
            return {"project_id": project_id, "as_of": as_of, "reconstruction_status": reconstruction_status(statuses), "source_statuses": statuses, "evidence": [dict(item) for item in evidence], "progress": [dict(item) for item in progress], "memory": [dict(item) for item in memories], "notion": [dict(item) for item in notion]}

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
        context = self.historical_context(project_id, as_of)
        with transaction(self.settings) as db:
            row = db.execute("SELECT source_revision FROM prime_core.repository_files WHERE project_id=%s AND source_revision=%s LIMIT 1", (project_id, as_of)).fetchone()
            context["source_statuses"]["repository"] = "EXACT" if row else "UNAVAILABLE"
            context["reconstruction_status"] = reconstruction_status(context["source_statuses"])
            db.execute("INSERT INTO prime_core.time_lens_checkpoints(checkpoint_id,project_id,as_of,reconstruction_status,source_set,created_at) VALUES (%s,%s,%s,%s,%s,%s)", (_id("checkpoint"), project_id, as_of, context["reconstruction_status"], json.dumps(context["source_statuses"]), now()))
            return context

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
