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
    safe_parser_result,
    sniff_mime_type,
    validate_evidence,
    validate_external_locator,
    validate_filename,
    validate_mime_consistency,
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

    @staticmethod
    def _record_historical(db: Any, project_id: str, artifact_type: str, artifact_id: str,
                           source_revision: str | None, snapshot: dict[str, Any],
                           observed_at: datetime, content_hash: str | None = None,
                           availability_status: str = "EXACT") -> None:
        """Persist an immutable reconstruction input alongside the live projection."""
        db.execute(
            "INSERT INTO prime_core.historical_revisions(historical_revision_id,project_id,artifact_type,artifact_id,source_revision,content_hash,snapshot,availability_status,observed_at) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING",
            (_id("hist"), project_id, artifact_type, artifact_id, source_revision, content_hash,
             json.dumps(snapshot), availability_status, observed_at),
        )

    @staticmethod
    def _quota(db: Any, project_id: str, incoming: int) -> None:
        per_project = int(os.getenv("PRIME_EVIDENCE_PROJECT_QUOTA_BYTES", str(500 * 1024 * 1024)))
        global_quota = int(os.getenv("PRIME_EVIDENCE_GLOBAL_QUOTA_BYTES", str(2 * 1024 * 1024 * 1024)))
        project_used = db.execute("SELECT COALESCE(SUM(size_bytes),0) AS total FROM prime_core.evidence_records WHERE project_id=%s AND retracted_at IS NULL AND purged_at IS NULL", (project_id,)).fetchone()["total"]
        global_used = db.execute("SELECT COALESCE(SUM(size_bytes),0) AS total FROM prime_core.evidence_records WHERE retracted_at IS NULL AND purged_at IS NULL").fetchone()["total"]
        if int(incoming) > 50 * 1024 * 1024:
            raise ValueError("Evidence artifact exceeds the configured per-artifact limit")
        if int(project_used or 0) + incoming > per_project:
            raise ValueError("Evidence project quota exceeded")
        if int(global_used or 0) + incoming > global_quota:
            raise ValueError("Evidence global quota exceeded")

    def record_evidence(
        self,
        project_id: str,
        source_type: str,
        locator: str,
        content: bytes | None = None,
        privacy_class: str = "PROJECT_PRIVATE",
        source_revision: str | None = None,
    ) -> dict[str, Any]:
        if source_type not in {"UPLOAD", "NODE_PATH", "EXTERNAL_REFERENCE"}:
            raise ValueError("unsupported Evidence source type")
        if source_type == "EXTERNAL_REFERENCE" and not validate_external_locator(locator):
            raise ValueError("external Evidence references must be safe HTTPS URLs")
        if source_type == "NODE_PATH":
            roots = [item for item in os.getenv("PRIME_NODE_ALLOWED_ROOTS", "").split(os.pathsep) if item]
            if not validate_node_locator(locator, roots):
                raise ValueError("Node Evidence reference is outside approved roots")
            node_path = Path(locator)
            if content is None and node_path.is_file():
                if node_path.stat().st_size <= 50 * 1024 * 1024:
                    content = node_path.read_bytes()
        if not validate_privacy_class(privacy_class):
            raise ValueError("unsupported Evidence privacy class")
        digest = hashlib.sha256(content).hexdigest() if content is not None else None
        size = len(content) if content is not None else None
        if content is not None and not validate_evidence(content, source_type):
            raise ValueError("Evidence content failed safe validation")
        parser_status = "READY" if content is not None else "PENDING"
        index_status = "READY" if content is not None else "UNAVAILABLE"
        storage_mode = {"UPLOAD": "MANAGED_COPY", "NODE_PATH": "NODE_REFERENCE", "EXTERNAL_REFERENCE": "EXTERNAL_REFERENCE"}[source_type]
        with transaction(self.settings) as db:
            if digest:
                duplicate = db.execute("SELECT * FROM prime_core.evidence_records WHERE project_id=%s AND content_hash=%s AND retracted_at IS NULL AND purged_at IS NULL", (project_id, digest)).fetchone()
                if duplicate:
                    return dict(duplicate)
                self._quota(db, project_id, size or 0)
            evidence_id = _id("evidence")
            captured = now()
            source_ref_id = _id("source")
            storage_path = None
            if content is not None and source_type == "UPLOAD":
                root = Path(os.getenv("PRIME_EVIDENCE_ROOT", ".prime-evidence")).resolve()
                target_dir = (root / project_id).resolve()
                if root not in target_dir.parents:
                    raise ValueError("invalid Evidence storage root")
                target_dir.mkdir(parents=True, exist_ok=True)
                storage_path = target_dir / f"{digest}-{evidence_id}.bin"
                storage_path.write_bytes(content)
            db.execute(
                "INSERT INTO prime_core.source_references(source_reference_id,project_id,source_class,locator,revision,content_hash,freshness_state,captured_at,metadata) VALUES (%s,%s,'EVIDENCE',%s,%s,%s,'CURRENT',%s,%s)",
                (source_ref_id, project_id, locator, source_revision, digest, captured, json.dumps({"source_type": source_type, "privacy_class": privacy_class})),
            )
            row = db.execute("INSERT INTO prime_core.evidence_records(evidence_id,project_id,source_type,locator,content_hash,captured_at,observed_at,parser_status,index_status,privacy_class,size_bytes,source_reference_id,immutable_identity,creator_type,creator_id,source_revision,storage_mode,source_uri,storage_path,mime_type) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'operator','operator',%s,%s,%s,%s,%s) RETURNING *", (evidence_id, project_id, source_type, locator, digest, captured, captured, parser_status, index_status, privacy_class, size, source_ref_id, digest or locator, source_revision, storage_mode, locator, str(storage_path) if storage_path else None, sniff_mime_type(content, locator) if content is not None else None)).fetchone()
            self._record_historical(db, project_id, "EVIDENCE", evidence_id, source_revision, {"evidence_id": evidence_id, "source_reference_id": source_ref_id, "content_hash": digest, "locator": locator, "storage_mode": storage_mode, "privacy_class": privacy_class, "parser_status": parser_status}, captured, digest)
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
        if not validate_mime_consistency(content, filename, mime_type):
            raise ValueError("Evidence MIME type does not match content")
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
        with transaction(self.settings) as db:
            duplicate = db.execute("SELECT * FROM prime_core.evidence_records WHERE project_id=%s AND content_hash=%s AND retracted_at IS NULL AND purged_at IS NULL", (project_id, digest)).fetchone()
            if duplicate:
                return dict(duplicate)
            self._quota(db, project_id, len(content))
            evidence_id = _id("evidence")
            captured = now()
            source_ref_id = _id("source")
            target = target_dir / f"{digest}-{filename}"
            target.write_bytes(content)
            parser_status, extracted_text, parser_error = safe_parser_result(content, mime_type, filename)
            index_status = "READY" if parser_status == "INDEXED" else ("UNAVAILABLE" if parser_status == "UNSUPPORTED" else parser_status)
            db.execute(
                "INSERT INTO prime_core.source_references(source_reference_id,project_id,source_class,locator,revision,content_hash,freshness_state,captured_at,metadata) VALUES (%s,%s,'EVIDENCE',%s,%s,%s,'CURRENT',%s,%s)",
                (source_ref_id, project_id, str(target), source_revision, digest, captured, json.dumps({"source_type": "UPLOAD", "filename": filename, "mime_type": mime_type.strip().lower()})),
            )
            row = db.execute("INSERT INTO prime_core.evidence_records(evidence_id,project_id,source_type,locator,content_hash,captured_at,observed_at,parser_status,index_status,privacy_class,storage_path,mime_type,size_bytes,source_reference_id,immutable_identity,creator_type,creator_id,extracted_text,source_revision,storage_mode,source_uri,parser_error) VALUES (%s,%s,'UPLOAD',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'operator','operator',%s,%s,'MANAGED_COPY',%s,%s) RETURNING *", (evidence_id, project_id, filename, digest, captured, captured, parser_status, index_status, privacy_class, str(target), mime_type.strip().lower(), len(content), source_ref_id, digest, extracted_text, source_revision, str(target), parser_error)).fetchone()
            self._record_historical(db, project_id, "EVIDENCE", evidence_id, source_revision, {"evidence_id": evidence_id, "source_reference_id": source_ref_id, "content_hash": digest, "locator": filename, "storage_mode": "MANAGED_COPY", "mime_type": mime_type.strip().lower(), "parser_status": parser_status, "index_status": index_status, "extracted_text": extracted_text}, captured, digest)
            return dict(row)

    def annotate_evidence(self, project_id: str, evidence_id: str, annotation: str) -> dict[str, Any]:
        if not annotation.strip():
            raise ValueError("Evidence annotation is required")
        with transaction(self.settings) as db:
            if not db.execute("SELECT 1 FROM prime_core.evidence_records WHERE project_id=%s AND evidence_id=%s", (project_id, evidence_id)).fetchone():
                raise KeyError("Evidence record not found")
            row = db.execute("INSERT INTO prime_core.evidence_annotations(annotation_id,project_id,evidence_id,annotation,created_at) VALUES (%s,%s,%s,%s,%s) RETURNING *", (_id("annotation"), project_id, evidence_id, annotation.strip()[:4000], now())).fetchone()
            return dict(row)

    def retrieve_evidence(self, project_id: str, evidence_id: str) -> dict[str, Any]:
        with connect(self.settings) as db:
            row = db.execute("SELECT * FROM prime_core.evidence_records WHERE project_id=%s AND evidence_id=%s", (project_id, evidence_id)).fetchone()
        if not row:
            raise KeyError("Evidence record not found")
        result = dict(row)
        if result.get("storage_mode") == "MANAGED_COPY" and result.get("storage_path"):
            path = Path(result["storage_path"])
            if not path.is_file():
                return {**result, "availability": "UNAVAILABLE", "reason": "managed-copy-missing"}
            data = path.read_bytes()
            if result.get("content_hash") and hashlib.sha256(data).hexdigest() != result["content_hash"]:
                return {**result, "availability": "PARTIAL", "reason": "content-hash-mismatch"}
            result["availability"] = "EXACT"
            result["content"] = data
        elif result.get("storage_mode") == "NODE_REFERENCE":
            path = Path(result["source_uri"] or result["locator"])
            result["availability"] = "EXACT" if path.is_file() else "UNAVAILABLE"
        else:
            result["availability"] = "EXACT" if result.get("source_uri") else "UNAVAILABLE"
        return result

    def reindex_evidence(self, project_id: str, evidence_id: str) -> dict[str, Any]:
        result = self.retrieve_evidence(project_id, evidence_id)
        if result.get("availability") != "EXACT" or not result.get("content"):
            with transaction(self.settings) as db:
                row = db.execute("UPDATE prime_core.evidence_records SET index_status='UNAVAILABLE',parser_status='UNSUPPORTED' WHERE project_id=%s AND evidence_id=%s RETURNING *", (project_id, evidence_id)).fetchone()
                return dict(row) if row else result
        parser_status, extracted_text, parser_error = safe_parser_result(result["content"], result.get("mime_type") or "application/octet-stream", result.get("locator") or "")
        index_status = "READY" if parser_status == "INDEXED" else ("UNAVAILABLE" if parser_status == "UNSUPPORTED" else parser_status)
        with transaction(self.settings) as db:
            row = db.execute("UPDATE prime_core.evidence_records SET parser_status=%s,index_status=%s,extracted_text=%s,parser_error=%s WHERE project_id=%s AND evidence_id=%s RETURNING *", (parser_status, index_status, extracted_text, parser_error, project_id, evidence_id)).fetchone()
            if not row:
                raise KeyError("Evidence record not found")
            return dict(row)

    def archive_evidence(self, project_id: str, evidence_id: str) -> dict[str, Any]:
        with transaction(self.settings) as db:
            row = db.execute("UPDATE prime_core.evidence_records SET archived_at=COALESCE(archived_at,now()) WHERE project_id=%s AND evidence_id=%s RETURNING *", (project_id, evidence_id)).fetchone()
            if not row:
                raise KeyError("Evidence record not found")
            self._record_historical(db, project_id, "EVIDENCE", evidence_id, row.get("source_revision"), {"evidence_id": evidence_id, "archived_at": row["archived_at"].isoformat()}, row["archived_at"], row.get("content_hash"))
            return dict(row)

    def purge_evidence(self, project_id: str, evidence_id: str, force: bool = False) -> dict[str, Any]:
        with transaction(self.settings) as db:
            row = db.execute("SELECT * FROM prime_core.evidence_records WHERE project_id=%s AND evidence_id=%s", (project_id, evidence_id)).fetchone()
            if not row:
                raise KeyError("Evidence record not found")
            referenced = db.execute("SELECT 1 FROM prime_core.evidence_links WHERE project_id=%s AND evidence_id=%s LIMIT 1", (project_id, evidence_id)).fetchone()
            if referenced and not force:
                raise ValueError("referenced Evidence cannot be purged without explicit force")
            if row.get("storage_path"):
                Path(row["storage_path"]).unlink(missing_ok=True)
            updated = db.execute("UPDATE prime_core.evidence_records SET purged_at=now(),archived_at=COALESCE(archived_at,now()),storage_path=NULL,extracted_text=NULL,index_status='UNAVAILABLE',parser_status='RETRACTED' WHERE project_id=%s AND evidence_id=%s RETURNING *", (project_id, evidence_id)).fetchone()
            return dict(updated)

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
            return {"source_reference_id": ref_id, "evidence_id": evidence_id, "source_revision": row.get("source_revision"), "content_hash": row["content_hash"], "immutable_identity": row.get("immutable_identity"), "storage_mode": row.get("storage_mode"), "retracted": row.get("retracted_at") is not None}

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
        evidence = None
        if row["source_class"] == "EVIDENCE":
            with connect(self.settings) as db:
                evidence = db.execute("SELECT evidence_id,retracted_at,purged_at,content_hash,storage_mode,storage_path,source_uri FROM prime_core.evidence_records WHERE project_id=%s AND source_reference_id=%s", (project_id, source_reference_id)).fetchone()
        if row["source_class"] == "GIT_COMMIT":
            with connect(self.settings) as db:
                checkpoint = db.execute("SELECT bundle_locator,content_hash,retained FROM prime_core.git_history_checkpoints WHERE project_id=%s AND source_reference_id=%s", (project_id, source_reference_id)).fetchone()
            if not checkpoint or not checkpoint.get("retained"):
                return {"source_reference_id": source_reference_id, "status": "UNAVAILABLE", "locator": row["locator"], "revision": row["revision"], "content_hash": row["content_hash"], "historical_available": False, "reason": "CHECKPOINT_NOT_RETAINED"}
            checkpoint_status = checkpoint_bundle_status(checkpoint.get("bundle_locator"), checkpoint.get("content_hash"))
            if checkpoint_status != "EXACT":
                return {"source_reference_id": source_reference_id, "status": checkpoint_status, "locator": row["locator"], "revision": row["revision"], "content_hash": row["content_hash"], "historical_available": False, "reason": "CHECKPOINT_BUNDLE_UNAVAILABLE"}
        if not source_available:
            return {"source_reference_id": source_reference_id, "status": "CHANGED_HISTORICAL_CONTENT_UNAVAILABLE", "locator": row["locator"], "revision": row["revision"], "content_hash": row["content_hash"], "historical_available": False}
        if evidence and evidence.get("purged_at"):
            return {"source_reference_id": source_reference_id, "status": "UNAVAILABLE", "locator": row["locator"], "revision": row["revision"], "content_hash": row["content_hash"], "historical_available": False, "reason": "EVIDENCE_PURGED"}
        if evidence:
            evidence_available = True
            if evidence.get("storage_mode") == "MANAGED_COPY":
                path = Path(evidence.get("storage_path") or "")
                evidence_available = path.is_file()
                if evidence_available and evidence.get("content_hash"):
                    try:
                        evidence_available = hashlib.sha256(path.read_bytes()).hexdigest() == evidence["content_hash"]
                    except OSError:
                        evidence_available = False
            elif evidence.get("storage_mode") == "NODE_REFERENCE":
                evidence_available = Path(evidence.get("source_uri") or "").is_file()
            if not evidence_available:
                return {"source_reference_id": source_reference_id, "status": "UNAVAILABLE", "locator": row["locator"], "revision": row["revision"], "content_hash": row["content_hash"], "historical_available": False, "reason": "EVIDENCE_CONTENT_UNAVAILABLE"}
        revision_match = current_revision is None or current_revision == row["revision"]
        hash_match = current_content_hash is None or current_content_hash == row["content_hash"]
        if revision_match and hash_match:
            if evidence and evidence.get("retracted_at"):
                return {"source_reference_id": source_reference_id, "status": "HISTORICAL", "locator": row["locator"], "revision": row["revision"], "content_hash": row["content_hash"], "warning": "SOURCE_RETRACTED", "historical_available": True, "later_retracted": True, "purged": False}
            return {"source_reference_id": source_reference_id, "status": "EXACT", "locator": row["locator"], "revision": row["revision"], "content_hash": row["content_hash"], "historical_available": True, "later_retracted": bool(evidence and evidence.get("retracted_at")), "purged": bool(evidence and evidence.get("purged_at"))}
        return {"source_reference_id": source_reference_id, "status": "HISTORICAL", "locator": row["locator"], "revision": row["revision"], "content_hash": row["content_hash"], "warning": "SOURCE_CHANGED", "historical_available": True, "later_retracted": bool(evidence and evidence.get("retracted_at")), "purged": False}

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
            captured = now()
            source_ref_id = _id("source")
            db.execute("INSERT INTO prime_core.source_references(source_reference_id,project_id,source_class,locator,revision,content_hash,freshness_state,captured_at,metadata) VALUES (%s,%s,'GIT_COMMIT',%s,%s,%s,'CURRENT',%s,%s)", (source_ref_id, project_id, str(repo), verified_commit, bundle_hash, captured, json.dumps({"preservation": "git-bundle", "canonical_commit": verified_commit})))
            row = db.execute("INSERT INTO prime_core.git_history_checkpoints(checkpoint_id,project_id,commit_id,bundle_locator,coverage_status,content_hash,captured_at,metadata,repository_path,verified_at,retained,source_reference_id) VALUES (%s,%s,%s,%s,'EXACT',%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (project_id,commit_id) DO UPDATE SET bundle_locator=EXCLUDED.bundle_locator,coverage_status='EXACT',content_hash=EXCLUDED.content_hash,verified_at=EXCLUDED.verified_at,retained=TRUE,source_reference_id=EXCLUDED.source_reference_id RETURNING *", (_id("gitcheckpoint"), project_id, verified_commit, str(bundle), bundle_hash, captured, json.dumps({"preservation": "git-bundle", "source": "canonical-commit"}), str(repo), captured, True, source_ref_id)).fetchone()
            self._record_historical(db, project_id, "GIT_CHECKPOINT", row["checkpoint_id"], verified_commit, {"checkpoint_id": row["checkpoint_id"], "commit_id": verified_commit, "bundle_locator": str(bundle), "content_hash": bundle_hash, "source_reference_id": source_ref_id}, captured, bundle_hash)
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
        """Return a frozen, source-by-source historical boundary; never current state."""
        cutoff: datetime | None = None
        try:
            cutoff = datetime.fromisoformat(as_of.replace("Z", "+00:00"))
        except ValueError:
            pass
        with connect(self.settings) as db:
            selected_revision = as_of
            if cutoff:
                selected = db.execute("SELECT source_revision FROM prime_core.repository_files WHERE project_id=%s AND observed_at<=%s ORDER BY observed_at DESC LIMIT 1", (project_id, cutoff)).fetchone()
                selected_revision = selected["source_revision"] if selected else None
                evidence = db.execute("SELECT evidence_id,source_reference_id,content_hash,captured_at,retracted_at,source_revision,parser_status,index_status,storage_mode,storage_path,source_uri FROM prime_core.evidence_records WHERE project_id=%s AND captured_at<=%s ORDER BY captured_at", (project_id, cutoff)).fetchall()
                progress = db.execute("SELECT assessment_id,repository_revision,progress_percent,created_at FROM prime_core.progress_assessments WHERE project_id=%s AND created_at<=%s ORDER BY created_at", (project_id, cutoff)).fetchall()
                memories = db.execute("SELECT memory_id,source_revision,status,created_at FROM prime_core.memory_records WHERE project_id=%s AND created_at<=%s ORDER BY created_at", (project_id, cutoff)).fetchall()
                notion = db.execute("SELECT projection_revision_id,content_hash,sync_status,observed_at FROM prime_core.notion_projection_revisions WHERE project_id=%s AND observed_at<=%s ORDER BY observed_at", (project_id, cutoff)).fetchall()
                authority = db.execute("SELECT authority_revision_id,source_path,source_hash,validation_status,observed_at FROM prime_core.authority_revisions WHERE project_id=%s AND observed_at<=%s ORDER BY observed_at", (project_id, cutoff)).fetchall()
                goal = db.execute("SELECT goal_revision_id,revision_number,content_hash,status,created_at FROM prime_core.goal_revisions WHERE project_id=%s AND created_at<=%s ORDER BY created_at", (project_id, cutoff)).fetchall()
                git = db.execute("SELECT checkpoint_id,commit_id,bundle_locator,content_hash,captured_at,retained FROM prime_core.git_history_checkpoints WHERE project_id=%s AND captured_at<=%s AND retained=TRUE ORDER BY captured_at", (project_id, cutoff)).fetchall()
                historical = db.execute("SELECT artifact_type,artifact_id,source_revision,content_hash,snapshot,availability_status,observed_at FROM prime_core.historical_revisions WHERE project_id=%s AND observed_at<=%s ORDER BY observed_at", (project_id, cutoff)).fetchall()
            else:
                evidence = db.execute("SELECT evidence_id,source_reference_id,content_hash,captured_at,retracted_at,source_revision,parser_status,index_status,storage_mode,storage_path,source_uri FROM prime_core.evidence_records WHERE project_id=%s AND source_revision=%s", (project_id, as_of)).fetchall()
                progress = db.execute("SELECT assessment_id,repository_revision,progress_percent,created_at FROM prime_core.progress_assessments WHERE project_id=%s AND repository_revision=%s", (project_id, as_of)).fetchall()
                memories = db.execute("SELECT memory_id,source_revision,status,created_at FROM prime_core.memory_records WHERE project_id=%s AND source_revision=%s", (project_id, as_of)).fetchall()
                notion = db.execute("SELECT projection_revision_id,content_hash,sync_status,observed_at FROM prime_core.notion_projection_revisions WHERE project_id=%s AND metadata->>'source_revision'=%s", (project_id, as_of)).fetchall()
                authority = db.execute("SELECT authority_revision_id,source_path,source_hash,validation_status,observed_at FROM prime_core.authority_revisions WHERE project_id=%s AND source_hash=%s", (project_id, as_of)).fetchall()
                goal = db.execute("SELECT goal_revision_id,revision_number,content_hash,status,created_at FROM prime_core.goal_revisions WHERE project_id=%s AND content_hash=%s", (project_id, as_of)).fetchall()
                git = db.execute("SELECT checkpoint_id,commit_id,bundle_locator,content_hash,captured_at,retained FROM prime_core.git_history_checkpoints WHERE project_id=%s AND commit_id=%s AND retained=TRUE", (project_id, as_of)).fetchall()
                historical = db.execute("SELECT artifact_type,artifact_id,source_revision,content_hash,snapshot,availability_status,observed_at FROM prime_core.historical_revisions WHERE project_id=%s AND source_revision=%s ORDER BY observed_at", (project_id, as_of)).fetchall()
            repository = db.execute("SELECT relative_path,content_hash,size_bytes,file_kind,source_revision,observed_at FROM prime_core.repository_files WHERE project_id=%s AND source_revision=%s ORDER BY relative_path", (project_id, selected_revision)).fetchall() if selected_revision else []
            retained_git = [dict(item) for item in git if item.get("bundle_locator") and checkpoint_bundle_status(item["bundle_locator"], item.get("content_hash")) == "EXACT"]
            brain = db.execute("SELECT 1 FROM prime_core.brain_snapshots WHERE project_id=%s AND source_revision=%s LIMIT 1", (project_id, selected_revision)).fetchone() if selected_revision else None
            repository_source = "INDEX" if repository else None
            repository_status = "EXACT" if repository else "UNAVAILABLE"
            if selected_revision and repository:
                binding = db.execute("SELECT r.canonical_path FROM prime_core.project_bindings b JOIN prime_core.repositories r ON r.repository_id=b.repository_id WHERE b.project_id=%s", (project_id,)).fetchone()
                if binding:
                    try:
                        subprocess.run(["git", "-C", str(Path(binding["canonical_path"]).resolve()), "cat-file", "-e", f"{selected_revision}^{{commit}}"], check=True, capture_output=True, text=True, timeout=10)
                    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
                        repository_status = "UNAVAILABLE"
                        repository_source = None
            if retained_git:
                repository_status = "EXACT"
                repository_source = "PRIME_GIT_CHECKPOINT"
            evidence_states = []
            for item in evidence:
                if item.get("storage_mode") == "MANAGED_COPY":
                    path = Path(item.get("storage_path") or "")
                    available = path.is_file()
                    if available and item.get("content_hash"):
                        try:
                            available = hashlib.sha256(path.read_bytes()).hexdigest() == item["content_hash"]
                        except OSError:
                            available = False
                    evidence_states.append("EXACT" if available else "UNAVAILABLE")
                elif item.get("storage_mode") == "NODE_REFERENCE":
                    evidence_states.append("EXACT" if Path(item.get("source_uri") or "").is_file() else "UNAVAILABLE")
                else:
                    evidence_states.append("EXACT" if item.get("source_uri") else "UNAVAILABLE")
            evidence_status = "UNAVAILABLE" if not evidence_states else ("EXACT" if all(value == "EXACT" for value in evidence_states) else ("UNAVAILABLE" if not any(value == "EXACT" for value in evidence_states) else "PARTIAL"))
            statuses = {"repository": repository_status, "authority": "EXACT" if authority else "UNAVAILABLE", "goal": "EXACT" if goal else "UNAVAILABLE", "evidence": evidence_status, "progress": "EXACT" if progress else "UNAVAILABLE", "memory": "EXACT" if memories else "UNAVAILABLE", "notion": "EXACT" if notion else "UNAVAILABLE", "brain": "EXACT" if brain else "UNAVAILABLE", "git": "EXACT" if retained_git else ("PARTIAL" if git else "UNAVAILABLE")}
            return {"project_id": project_id, "as_of": as_of, "selected_revision": selected_revision, "reconstruction_status": reconstruction_status(statuses), "source_statuses": statuses, "evidence": [dict(item) for item in evidence], "progress": [dict(item) for item in progress], "memory": [dict(item) for item in memories], "notion": [dict(item) for item in notion], "authority": [dict(item) for item in authority], "goal": [dict(item) for item in goal], "git": [dict(item) for item in git], "repository": [dict(item) for item in repository], "historical_artifacts": [dict(item) for item in historical], "repository_reconstruction": {"status": statuses["repository"], "source": repository_source, "commit_id": retained_git[0]["commit_id"] if retained_git else selected_revision}}

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
                "UPDATE prime_core.evidence_records SET retracted_at=%s,retraction_reason=%s,parser_status='RETRACTED',index_status='UNAVAILABLE' WHERE project_id=%s AND evidence_id=%s AND retracted_at IS NULL RETURNING *",
                (now(), reason.strip()[:500], project_id, evidence_id),
            ).fetchone()
            if not row:
                raise KeyError("Evidence record not found or already retracted")
            self._record_historical(db, project_id, "EVIDENCE", evidence_id, row.get("source_revision"), {"evidence_id": evidence_id, "retracted_at": row["retracted_at"].isoformat(), "retraction_reason": row["retraction_reason"]}, row["retracted_at"], row.get("content_hash"))
            return dict(row)

    def time_lens(self, project_id: str, as_of: str) -> dict[str, Any]:
        context = self.historical_context(project_id, as_of)
        with transaction(self.settings) as db:
            db.execute("INSERT INTO prime_core.time_lens_checkpoints(checkpoint_id,project_id,as_of,reconstruction_status,source_set,created_at) VALUES (%s,%s,%s,%s,%s,%s)", (_id("checkpoint"), project_id, as_of, context["reconstruction_status"], json.dumps(context["source_statuses"]), now()))
            return {**context, "mode": "HISTORICAL", "return_to_now": {"method": "GET", "path": f"/v1/projects/{project_id}/time-lens/state?as_of=now"}}

    def return_to_now(self, project_id: str) -> dict[str, Any]:
        with connect(self.settings) as db:
            latest = db.execute("SELECT observed_at FROM prime_core.repository_files WHERE project_id=%s ORDER BY observed_at DESC LIMIT 1", (project_id,)).fetchone()
        if not latest:
            return {"project_id": project_id, "mode": "CURRENT", "source_statuses": {}, "reconstruction_status": "UNAVAILABLE"}
        # Current state is a time boundary. Revision-only lookup cannot select
        # durable Goal/Authority/Memory rows whose identity is not the Git SHA.
        current = self.historical_context(project_id, latest["observed_at"].isoformat())
        return {**current, "mode": "CURRENT", "return_to_now": None}

    def backup_manifest(self, project_id: str) -> dict[str, Any]:
        """Expose the durable Evidence/history component set to the backup coordinator."""
        with connect(self.settings) as db:
            evidence = db.execute("SELECT evidence_id,content_hash,size_bytes,storage_mode,storage_path,source_reference_id,source_revision,retracted_at,purged_at FROM prime_core.evidence_records WHERE project_id=%s ORDER BY evidence_id", (project_id,)).fetchall()
            revisions = db.execute("SELECT historical_revision_id,artifact_type,artifact_id,source_revision,content_hash,availability_status,observed_at FROM prime_core.historical_revisions WHERE project_id=%s ORDER BY observed_at", (project_id,)).fetchall()
            checkpoints = db.execute("SELECT checkpoint_id,commit_id,bundle_locator,content_hash,coverage_status,retained FROM prime_core.git_history_checkpoints WHERE project_id=%s ORDER BY captured_at", (project_id,)).fetchall()
        return {"project_id": project_id, "revision": now().isoformat(), "evidence": [dict(row) for row in evidence], "historical_revisions": [dict(row) for row in revisions], "git_checkpoints": [dict(row) for row in checkpoints]}

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
