from __future__ import annotations

import json
import logging
import time
import uuid
import hashlib
import os
from datetime import datetime, timedelta, timezone
from typing import Any

from .config import Settings
from .db import connect, transaction
from .security import new_token, password_hash, password_verify, token_digest
from .history_primitives import record_historical_snapshot

UTC = timezone.utc
log = logging.getLogger("prime.core")


def now() -> datetime:
    return datetime.now(UTC)


def _id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex}"


class CoreService:
    def __init__(self, settings: Settings):
        self.settings = settings

    def bootstrap(self, password: str) -> str:
        if len(password) < 12:
            raise ValueError("password must contain at least 12 characters")
        timestamp = now()
        recovery = new_token()
        with transaction(self.settings) as db:
            existing = db.execute("SELECT 1 FROM prime_core.operators LIMIT 1").fetchone()
            if existing:
                raise ValueError("operator is already initialized")
            db.execute(
                "INSERT INTO prime_core.operators(operator_id, username, password_hash, recovery_hash, created_at, updated_at) "
                "VALUES (%s, 'operator', %s, %s, %s, %s)",
                (_id("op"), password_hash(password), token_digest(recovery), timestamp, timestamp),
            )
            self._audit(db, "system", "bootstrap", "operator.bootstrap", metadata={"recovery_issued": True})
        return recovery

    def login(self, password: str) -> tuple[str, str]:
        with transaction(self.settings) as db:
            row = db.execute(
                "SELECT operator_id, password_hash FROM prime_core.operators WHERE username='operator'"
            ).fetchone()
            if not row or not password_verify(password, row["password_hash"]):
                raise PermissionError("invalid credentials")
            session = new_token()
            csrf = new_token()
            timestamp = now()
            db.execute(
                "INSERT INTO prime_core.sessions(session_id, operator_id, token_hash, csrf_hash, created_at, expires_at, last_seen_at) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (_id("sess"), row["operator_id"], token_digest(session), token_digest(csrf), timestamp,
                 timestamp + timedelta(seconds=self.settings.session_ttl_seconds), timestamp),
            )
            self._audit(db, "operator", row["operator_id"], "operator.login")
            return session, csrf

    def session(self, token: str) -> dict[str, Any] | None:
        with connect(self.settings) as db:
            row = db.execute(
                "SELECT s.session_id, s.operator_id, s.csrf_hash, s.expires_at, o.username "
                "FROM prime_core.sessions s JOIN prime_core.operators o ON o.operator_id=s.operator_id "
                "WHERE s.token_hash=%s AND s.revoked_at IS NULL AND s.expires_at > now()",
                (token_digest(token),),
            ).fetchone()
            if row:
                db.execute("UPDATE prime_core.sessions SET last_seen_at=now() WHERE session_id=%s", (row["session_id"],))
                db.commit()
            return dict(row) if row else None

    def logout(self, token: str) -> None:
        with transaction(self.settings) as db:
            db.execute("UPDATE prime_core.sessions SET revoked_at=now() WHERE token_hash=%s", (token_digest(token),))

    def recover(self, recovery: str, new_password: str) -> str:
        if len(new_password) < 12:
            raise ValueError("password must contain at least 12 characters")
        replacement = new_token()
        with transaction(self.settings) as db:
            row = db.execute("SELECT operator_id, recovery_hash FROM prime_core.operators LIMIT 1").fetchone()
            if not row or token_digest(recovery) != row["recovery_hash"]:
                raise PermissionError("invalid recovery credential")
            db.execute(
                "UPDATE prime_core.operators SET password_hash=%s, recovery_hash=%s, updated_at=now() WHERE operator_id=%s",
                (password_hash(new_password), token_digest(replacement), row["operator_id"]),
            )
            db.execute("UPDATE prime_core.sessions SET revoked_at=now() WHERE revoked_at IS NULL")
            self._audit(db, "operator", row["operator_id"], "operator.recovery_reset")
        return replacement

    def create_job(self, job_type: str, payload: dict[str, Any], idempotency_key: str, project_id: str | None = None) -> dict[str, Any]:
        timestamp = now()
        with transaction(self.settings) as db:
            existing = db.execute("SELECT * FROM prime_core.jobs WHERE idempotency_key=%s", (idempotency_key,)).fetchone()
            if existing:
                return dict(existing)
            queue_limit = int(os.getenv("PRIME_QUEUE_LIMIT", "1000"))
            queue_count = db.execute("SELECT count(*) AS count FROM prime_core.jobs WHERE status IN ('QUEUED','RUNNING')").fetchone()["count"]
            derived_job = job_type.upper() in {"INDEX", "REINDEX", "BRAIN", "PARSER", "NOTION_PROJECTION", "MODEL_CACHE", "REPOSITORY_SCAN"}
            if int(queue_count) >= queue_limit and derived_job:
                raise ValueError("derived work backpressure: queue capacity exceeded")
            row = db.execute(
                "INSERT INTO prime_core.jobs(job_id, project_id, job_type, status, idempotency_key, available_at, payload, created_at, updated_at) "
                "VALUES (%s,%s,%s,'QUEUED',%s,%s,%s,%s,%s) RETURNING *",
                (_id("job"), project_id, job_type, idempotency_key, timestamp, json.dumps(payload), timestamp, timestamp),
            ).fetchone()
            self._audit(db, "operator", "operator", "job.created", project_id=project_id, target_id=row["job_id"])
            return dict(row)

    def create_coalesced_job(self, job_type: str, payload: dict[str, Any], project_id: str, source_key: str) -> dict[str, Any]:
        """Coalesce bursty derived work into one durable, idempotent job."""
        window_ms = int(os.getenv("PRIME_EVENT_COALESCE_WINDOW_MS", "1000"))
        bucket = int(time.time() * 1000 // max(window_ms, 1))
        return self.create_job(job_type, payload, f"coalesced:{project_id}:{job_type}:{source_key}:{bucket}", project_id)

    def create_project(self, name: str) -> dict[str, Any]:
        timestamp = now()
        project_id = _id("project")
        with transaction(self.settings) as db:
            row = db.execute(
                "INSERT INTO prime_core.projects(project_id, name, lifecycle_state, connectivity_state, freshness_state, work_condition, created_at, updated_at) "
                "VALUES (%s,%s,'DRAFT','OFFLINE','UNKNOWN','REVIEW_REQUIRED',%s,%s) RETURNING *",
                (project_id, name, timestamp, timestamp),
            ).fetchone()
            self._audit(db, "operator", "operator", "project.created", project_id=project_id, target_id=project_id)
            return dict(row)

    def list_projects(self) -> list[dict[str, Any]]:
        with connect(self.settings) as db:
            return [dict(row) for row in db.execute("SELECT * FROM prime_core.projects ORDER BY created_at").fetchall()]

    def register_node(self, node_id: str, name: str, platform: str, identity_fingerprint: str, allowed_roots: list[str], capabilities: dict[str, Any]) -> dict[str, Any]:
        timestamp = now()
        with transaction(self.settings) as db:
            row = db.execute(
                "INSERT INTO prime_core.nodes(node_id,name,platform,status,identity_fingerprint,allowed_roots,capabilities,enrolled_at,last_seen_at) "
                "VALUES (%s,%s,%s,'ENROLLED',%s,%s,%s,%s,%s) "
                "ON CONFLICT (node_id) DO UPDATE SET name=EXCLUDED.name, platform=EXCLUDED.platform, status='ONLINE', allowed_roots=EXCLUDED.allowed_roots, capabilities=EXCLUDED.capabilities, last_seen_at=EXCLUDED.last_seen_at RETURNING *",
                (node_id, name, platform, identity_fingerprint, json.dumps(allowed_roots), json.dumps(capabilities), timestamp, timestamp),
            ).fetchone()
            self._audit(db, "operator", "operator", "node.registered", target_id=node_id)
            return dict(row)

    def list_nodes(self) -> list[dict[str, Any]]:
        with connect(self.settings) as db:
            return [dict(row) for row in db.execute("SELECT * FROM prime_core.nodes ORDER BY enrolled_at").fetchall()]

    def bind_repository(self, project_id: str, node_id: str, identity_fingerprint: str, canonical_path: str, is_bare: bool = False) -> dict[str, Any]:
        timestamp = now()
        with transaction(self.settings) as db:
            if is_bare:
                raise ValueError("bare repositories are not supported")
            if not db.execute("SELECT 1 FROM prime_core.projects WHERE project_id=%s", (project_id,)).fetchone():
                raise KeyError("project not found")
            if not db.execute("SELECT 1 FROM prime_core.nodes WHERE node_id=%s", (node_id,)).fetchone():
                raise KeyError("node not found")
            row = db.execute(
                "INSERT INTO prime_core.repositories(repository_id,node_id,project_id,identity_fingerprint,canonical_path,is_bare,created_at,last_observed_at) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING *",
                (_id("repo"), node_id, project_id, identity_fingerprint, canonical_path, is_bare, timestamp, timestamp),
            ).fetchone()
            db.execute(
                "INSERT INTO prime_core.project_bindings(project_id,node_id,repository_id,binding_status,bound_at,updated_at) VALUES (%s,%s,%s,'BOUND',%s,%s)",
                (project_id, node_id, row["repository_id"], timestamp, timestamp),
            )
            db.execute("UPDATE prime_core.projects SET lifecycle_state='PROVISIONING', connectivity_state='ONLINE', freshness_state='CURRENT', work_condition='NORMAL', updated_at=%s WHERE project_id=%s", (timestamp, project_id))
            self._audit(db, "operator", "operator", "repository.bound", project_id=project_id, target_id=row["repository_id"])
            return dict(row)

    def create_goal_revision(self, project_id: str, content: str, approve: bool = False) -> dict[str, Any]:
        timestamp = now()
        with transaction(self.settings) as db:
            last = db.execute("SELECT COALESCE(MAX(revision_number),0) AS number FROM prime_core.goal_revisions WHERE project_id=%s", (project_id,)).fetchone()["number"]
            status = "APPROVED" if approve else "DRAFT"
            row = db.execute(
                "INSERT INTO prime_core.goal_revisions(goal_revision_id,project_id,revision_number,content,content_hash,status,approved_by,created_at,approved_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING *",
                (_id("goal"), project_id, last + 1, content, hashlib.sha256(content.encode()).hexdigest(), status, "operator" if approve else None, timestamp, timestamp if approve else None),
            ).fetchone()
            if approve:
                db.execute("UPDATE prime_core.goal_revisions SET status='SUPERSEDED' WHERE project_id=%s AND goal_revision_id<>%s AND status='APPROVED'", (project_id, row["goal_revision_id"]))
                db.execute("UPDATE prime_core.projects SET work_condition='NORMAL', updated_at=%s WHERE project_id=%s", (timestamp, project_id))
            record_historical_snapshot(db, project_id, "GOAL", row["goal_revision_id"], row["content_hash"], {"goal_revision_id": row["goal_revision_id"], "revision_number": row["revision_number"], "content": content, "status": status}, row["created_at"], row["content_hash"])
            self._audit(db, "operator", "operator", "goal.revision_created", project_id=project_id, target_id=row["goal_revision_id"])
            return dict(row)

    def record_authority_revision(self, project_id: str, source_path: str, source_hash: str, validation_status: str, metadata: dict[str, Any] | None = None, content_snapshot: str | None = None, canonical_commit: str | None = None) -> dict[str, Any]:
        with transaction(self.settings) as db:
            row = db.execute(
                "INSERT INTO prime_core.authority_revisions(authority_revision_id,project_id,source_path,source_hash,contract_version,validation_status,observed_at,metadata,content_snapshot,canonical_commit) VALUES (%s,%s,%s,%s,'authority-file-contract-v1',%s,now(),%s,%s,%s) RETURNING *",
                (_id("authority"), project_id, source_path, source_hash, validation_status, json.dumps(metadata or {}), content_snapshot, canonical_commit),
            ).fetchone()
            record_historical_snapshot(db, project_id, "AUTHORITY", row["authority_revision_id"], canonical_commit or source_hash, {"authority_revision_id": row["authority_revision_id"], "source_path": source_path, "source_hash": source_hash, "validation_status": validation_status, "content_snapshot": content_snapshot}, row["observed_at"], source_hash)
            self._audit(db, "system", "authority-observer", "authority.observed", project_id=project_id, target_id=row["authority_revision_id"])
            return dict(row)

    def create_workflow(self, workflow_type: str, idempotency_key: str, project_id: str | None = None) -> dict[str, Any]:
        timestamp = now()
        with transaction(self.settings) as db:
            existing = db.execute("SELECT * FROM prime_core.workflows WHERE idempotency_key=%s", (idempotency_key,)).fetchone()
            if existing:
                return dict(existing)
            if project_id and not db.execute("SELECT 1 FROM prime_core.projects WHERE project_id=%s", (project_id,)).fetchone():
                raise KeyError("project not found")
            row = db.execute(
                "INSERT INTO prime_core.workflows(workflow_id, project_id, workflow_type, status, idempotency_key, created_at, updated_at) "
                "VALUES (%s,%s,%s,'RUNNING',%s,%s,%s) RETURNING *",
                (_id("workflow"), project_id, workflow_type, idempotency_key, timestamp, timestamp),
            ).fetchone()
            self._audit(db, "operator", "operator", "workflow.created", project_id=project_id, target_id=row["workflow_id"])
            return dict(row)

    def claim_job(self) -> dict[str, Any] | None:
        with transaction(self.settings) as db:
            row = db.execute(
                "SELECT * FROM prime_core.jobs WHERE status='QUEUED' AND available_at <= now() "
                "ORDER BY created_at FOR UPDATE SKIP LOCKED LIMIT 1"
            ).fetchone()
            if not row:
                return None
            updated = db.execute(
                "UPDATE prime_core.jobs SET status='RUNNING', attempts=attempts+1, started_at=now(), updated_at=now() "
                "WHERE job_id=%s RETURNING *", (row["job_id"],)
            ).fetchone()
            return dict(updated)

    def complete_job(self, job_id: str, success: bool, error: str | None = None) -> None:
        with transaction(self.settings) as db:
            row = db.execute("SELECT attempts, max_attempts FROM prime_core.jobs WHERE job_id=%s FOR UPDATE", (job_id,)).fetchone()
            if not row:
                raise KeyError("job not found")
            status = "SUCCEEDED" if success else ("DEAD_LETTER" if row["attempts"] >= row["max_attempts"] else "QUEUED")
            db.execute(
                "UPDATE prime_core.jobs SET status=%s, last_error=%s, available_at=now()+make_interval(secs => %s), "
                "completed_at=CASE WHEN %s THEN now() ELSE NULL END, updated_at=now() WHERE job_id=%s",
                (status, error, min(2 ** max(row["attempts"] - 1, 0), 300), success, job_id),
            )

    def emit_event(self, event_type: str, payload: dict[str, Any], project_id: str | None = None,
                   dedupe_key: str | None = None, occurred_at: datetime | None = None) -> dict[str, Any]:
        timestamp = now()
        with transaction(self.settings) as db:
            if dedupe_key:
                existing = db.execute("SELECT * FROM prime_core.events WHERE dedupe_key=%s", (dedupe_key,)).fetchone()
                if existing:
                    return dict(existing)
            sequence = None
            if project_id:
                db.execute("SELECT pg_advisory_xact_lock(hashtext(%s))", (project_id,))
                sequence = db.execute(
                    "SELECT COALESCE(MAX(project_sequence),0)+1 AS next_sequence FROM prime_core.events WHERE project_id=%s",
                    (project_id,),
                ).fetchone()["next_sequence"]
            row = db.execute(
                "INSERT INTO prime_core.events(event_id, project_id, event_type, occurred_at, observed_at, project_sequence, payload, dedupe_key) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING *",
                (_id("evt"), project_id, event_type, occurred_at or timestamp, timestamp, sequence, json.dumps(payload), dedupe_key),
            ).fetchone()
            return dict(row)

    def emit_coalesced_event(self, event_type: str, payload: dict[str, Any], project_id: str, source_key: str) -> dict[str, Any]:
        window_ms = int(os.getenv("PRIME_EVENT_COALESCE_WINDOW_MS", "1000"))
        bucket = int(time.time() * 1000 // max(window_ms, 1))
        return self.emit_event(event_type, payload, project_id=project_id, dedupe_key=f"coalesced:{project_id}:{event_type}:{source_key}:{bucket}")

    @staticmethod
    def _audit(db: Any, actor_type: str, actor_id: str, action: str, project_id: str | None = None,
               target_id: str | None = None, metadata: dict[str, Any] | None = None) -> None:
        db.execute(
            "INSERT INTO prime_core.audit_events(audit_id, actor_type, actor_id, action, project_id, target_id, occurred_at, metadata) "
            "VALUES (%s,%s,%s,%s,%s,%s,now(),%s)",
            (_id("audit"), actor_type, actor_id, action, project_id, target_id, json.dumps(metadata or {})),
        )
