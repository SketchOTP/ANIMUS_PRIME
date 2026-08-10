from __future__ import annotations

import json
import logging
import time
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from .config import Settings
from .db import connect, transaction
from .security import new_token, password_hash, password_verify, token_digest

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
            row = db.execute(
                "INSERT INTO prime_core.jobs(job_id, project_id, job_type, status, idempotency_key, available_at, payload, created_at, updated_at) "
                "VALUES (%s,%s,%s,'QUEUED',%s,%s,%s,%s,%s) RETURNING *",
                (_id("job"), project_id, job_type, idempotency_key, timestamp, json.dumps(payload), timestamp, timestamp),
            ).fetchone()
            self._audit(db, "operator", "operator", "job.created", project_id=project_id, target_id=row["job_id"])
            return dict(row)

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

    @staticmethod
    def _audit(db: Any, actor_type: str, actor_id: str, action: str, project_id: str | None = None,
               target_id: str | None = None, metadata: dict[str, Any] | None = None) -> None:
        db.execute(
            "INSERT INTO prime_core.audit_events(audit_id, actor_type, actor_id, action, project_id, target_id, occurred_at, metadata) "
            "VALUES (%s,%s,%s,%s,%s,%s,now(),%s)",
            (_id("audit"), actor_type, actor_id, action, project_id, target_id, json.dumps(metadata or {})),
        )
