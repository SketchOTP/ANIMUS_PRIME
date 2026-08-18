from __future__ import annotations

import json
import io
import logging
import time
import uuid
import hashlib
import os
import subprocess
import tarfile
import secrets
from datetime import datetime, timedelta, timezone
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import urlsplit, urlunsplit

from .config import Settings
from .db import connect, transaction
from .security import constant_time_equal, new_token, password_hash, password_verify, token_digest
from .history_primitives import record_historical_snapshot
from .authority import REQUIRED_AUTHORITY_FILES, authority_migration_plan, classify_authority_snapshot, migrate_authority, provision_authority, validate_authority
from .git_provenance import GitProvenanceError, inspect_repository_candidate, resolve_canonical_ref
from .workflow_primitives import QualificationInterruption, REPLAY_POLICIES, qualification_interrupt, resume_plan_payload, step_resume_decision
from .node_client import NodeClient, NodeClientSettings, NodeClientError
from .node_trust import NodeTrustSettings, csr_fingerprint, digest, issue_bootstrap, sign_node_certificate

UTC = timezone.utc
log = logging.getLogger("prime.core")


def now() -> datetime:
    return datetime.now(UTC)


def _id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex}"


class CoreService:
    def __init__(self, settings: Settings):
        self.settings = settings

    @staticmethod
    def _display_remote_url(remote_url: str) -> str:
        """Return an operator-useful remote locator without embedded credentials."""
        parsed = urlsplit(remote_url)
        if not parsed.scheme or not parsed.netloc or "@" not in parsed.netloc:
            return remote_url
        hostname = parsed.hostname or ""
        if parsed.port is not None:
            hostname = f"{hostname}:{parsed.port}"
        return urlunsplit((parsed.scheme, hostname, parsed.path, parsed.query, parsed.fragment))

    @staticmethod
    def _tracked_worktree_changes(repository_root: Path) -> str:
        """Report tracked changes while preserving tool-local untracked state."""
        return subprocess.run(
            ["git", "-C", str(repository_root), "status", "--porcelain", "--untracked-files=no"],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        ).stdout.strip()

    @staticmethod
    def _authority_template_root() -> Path:
        configured = os.getenv("PRIME_AUTHORITY_TEMPLATE_ROOT")
        candidates = [Path(configured)] if configured else []
        candidates.extend((Path("authority-template/v1"), Path("/home/sketch/Projects/ANIMUS_PRIME/authority-template/v1")))
        for candidate in candidates:
            resolved = candidate.expanduser().resolve()
            if (resolved / "AGENTS.md").is_file():
                return resolved
        raise FileNotFoundError("authority-template/v1/AGENTS.md")

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

    def provision_local_identity(self, local_recovery: str, identity_credential: str) -> None:
        """Provision the separate trusted-host factor through local recovery only."""
        if len(identity_credential) < 32:
            raise ValueError("local identity credential is too short")
        with transaction(self.settings) as db:
            row = db.execute(
                "SELECT operator_id, local_recovery_hash, local_identity_hash "
                "FROM prime_core.operators WHERE username='operator'"
            ).fetchone()
            if not row or not row["local_recovery_hash"] or not constant_time_equal(token_digest(local_recovery), row["local_recovery_hash"]):
                raise PermissionError("invalid local recovery credential")
            if row["local_identity_hash"]:
                raise ValueError("local identity is already provisioned")
            db.execute(
                "UPDATE prime_core.operators SET local_identity_hash=%s, updated_at=now() WHERE operator_id=%s",
                (token_digest(identity_credential), row["operator_id"]),
            )
            self._audit(
                db, "operator", row["operator_id"], "operator.local_identity_provisioned",
                metadata={"auth_method": "LOCAL_IDENTITY", "provisioning": "LOCAL_RECOVERY"},
            )

    @staticmethod
    def _approval_code() -> str:
        alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
        return "".join(secrets.choice(alphabet) for _ in range(8))

    def create_local_identity_challenge(self, purpose: str, operator_id: str | None = None) -> dict[str, Any]:
        if purpose not in {"SIGN_IN", "STEP_UP"}:
            raise ValueError("invalid local identity challenge purpose")
        browser_nonce = new_token()
        approval_code = self._approval_code()
        challenge_id = _id("authch")
        timestamp = now()
        expires_at = timestamp + timedelta(seconds=120)
        with transaction(self.settings) as db:
            if operator_id:
                row = db.execute(
                    "SELECT operator_id, local_identity_hash FROM prime_core.operators "
                    "WHERE operator_id=%s AND username='operator'",
                    (operator_id,),
                ).fetchone()
            else:
                row = db.execute(
                    "SELECT operator_id, local_identity_hash FROM prime_core.operators WHERE username='operator'"
                ).fetchone()
            if not row or not row["local_identity_hash"]:
                raise ValueError("local identity is not provisioned")
            db.execute(
                "INSERT INTO prime_core.auth_challenges "
                "(challenge_id, operator_id, purpose, approval_code_hash, browser_nonce_hash, created_at, expires_at) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (challenge_id, row["operator_id"], purpose, token_digest(approval_code),
                 token_digest(browser_nonce), timestamp, expires_at),
            )
            self._audit(
                db, "operator", row["operator_id"], "operator.local_identity_challenge_created",
                metadata={"auth_method": "LOCAL_IDENTITY", "purpose": purpose, "ttl_seconds": 120},
            )
        return {
            "challenge_id": challenge_id,
            "approval_code": approval_code,
            "purpose": purpose,
            "expires_in_seconds": 120,
            "browser_nonce": browser_nonce,
        }

    def approve_local_identity(self, approval_code: str, purpose: str, identity_credential: str) -> dict[str, Any]:
        if purpose not in {"SIGN_IN", "STEP_UP"}:
            raise ValueError("invalid local identity challenge purpose")
        with transaction(self.settings) as db:
            row = db.execute(
                "SELECT c.challenge_id, c.operator_id, c.expires_at, c.approved_at, c.consumed_at, "
                "o.local_identity_hash FROM prime_core.auth_challenges c "
                "JOIN prime_core.operators o ON o.operator_id=c.operator_id "
                "WHERE c.approval_code_hash=%s AND c.purpose=%s FOR UPDATE",
                (token_digest(approval_code), purpose),
            ).fetchone()
            if not row or not row["local_identity_hash"] or not constant_time_equal(token_digest(identity_credential), row["local_identity_hash"]):
                raise PermissionError("invalid local identity credential")
            if row["consumed_at"] or row["approved_at"] or row["expires_at"] <= now():
                raise PermissionError("local identity challenge is unavailable")
            db.execute(
                "UPDATE prime_core.auth_challenges SET approved_at=now() WHERE challenge_id=%s",
                (row["challenge_id"],),
            )
            self._audit(
                db, "operator", row["operator_id"], "operator.local_identity_approved",
                target_id=row["challenge_id"],
                metadata={"auth_method": "LOCAL_IDENTITY", "purpose": purpose},
            )
            return {"approved": True, "purpose": purpose}

    def redeem_local_identity(self, challenge_id: str, purpose: str, browser_nonce: str,
                              session_token: str | None = None) -> dict[str, Any]:
        if purpose not in {"SIGN_IN", "STEP_UP"}:
            raise ValueError("invalid local identity challenge purpose")
        timestamp = now()
        with transaction(self.settings) as db:
            row = db.execute(
                "SELECT c.challenge_id, c.operator_id, c.purpose, c.browser_nonce_hash, c.expires_at, "
                "c.approved_at, c.consumed_at FROM prime_core.auth_challenges c "
                "WHERE c.challenge_id=%s FOR UPDATE",
                (challenge_id,),
            ).fetchone()
            if (
                not row or row["purpose"] != purpose or row["consumed_at"] or not row["approved_at"]
                or row["expires_at"] <= timestamp
                or not constant_time_equal(token_digest(browser_nonce), row["browser_nonce_hash"])
            ):
                raise PermissionError("local identity challenge cannot be redeemed")
            if purpose == "STEP_UP":
                session = db.execute(
                    "SELECT session_id FROM prime_core.sessions "
                    "WHERE token_hash=%s AND operator_id=%s AND revoked_at IS NULL AND expires_at > now() FOR UPDATE",
                    (token_digest(session_token or ""), row["operator_id"]),
                ).fetchone()
                if not session:
                    raise PermissionError("authenticated operator session required for step-up")
                db.execute(
                    "UPDATE prime_core.sessions SET step_up_at=%s,last_seen_at=%s WHERE session_id=%s",
                    (timestamp, timestamp, session["session_id"]),
                )
                db.execute(
                    "UPDATE prime_core.auth_challenges SET consumed_at=%s WHERE challenge_id=%s",
                    (timestamp, challenge_id),
                )
                self._audit(
                    db, "operator", row["operator_id"], "operator.step_up",
                    target_id=challenge_id,
                    metadata={"auth_method": "LOCAL_IDENTITY", "purpose": "STEP_UP"},
                )
                return {"authenticated": True, "purpose": purpose, "auth_method": "LOCAL_IDENTITY",
                        "step_up_at": timestamp.isoformat(), "valid_for_seconds": 300}

            session = new_token()
            csrf = new_token()
            db.execute(
                "INSERT INTO prime_core.sessions(session_id, operator_id, token_hash, csrf_hash, created_at, expires_at, last_seen_at) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (_id("sess"), row["operator_id"], token_digest(session), token_digest(csrf), timestamp,
                 timestamp + timedelta(seconds=self.settings.session_ttl_seconds), timestamp),
            )
            db.execute(
                "UPDATE prime_core.auth_challenges SET consumed_at=%s WHERE challenge_id=%s",
                (timestamp, challenge_id),
            )
            self._audit(
                db, "operator", row["operator_id"], "operator.login",
                target_id=challenge_id,
                metadata={"auth_method": "LOCAL_IDENTITY", "purpose": "SIGN_IN"},
            )
            return {"authenticated": True, "actor_type": "operator", "auth_method": "LOCAL_IDENTITY",
                    "session_token": session, "csrf_token": csrf}

    def session(self, token: str) -> dict[str, Any] | None:
        with connect(self.settings) as db:
            row = db.execute(
                "SELECT s.session_id, s.operator_id, s.csrf_hash, s.expires_at, s.step_up_at, o.username "
                "FROM prime_core.sessions s JOIN prime_core.operators o ON o.operator_id=s.operator_id "
                "WHERE s.token_hash=%s AND s.revoked_at IS NULL AND s.expires_at > now()",
                (token_digest(token),),
            ).fetchone()
            if row:
                db.execute("UPDATE prime_core.sessions SET last_seen_at=now() WHERE session_id=%s", (row["session_id"],))
                db.commit()
            return dict(row) if row else None

    def step_up(self, token: str, password: str) -> dict[str, Any]:
        """Re-authenticate the current operator session for high-risk actions."""
        timestamp = now()
        with transaction(self.settings) as db:
            row = db.execute(
                "SELECT s.session_id, s.operator_id, o.password_hash "
                "FROM prime_core.sessions s JOIN prime_core.operators o ON o.operator_id=s.operator_id "
                "WHERE s.token_hash=%s AND s.revoked_at IS NULL AND s.expires_at > now()",
                (token_digest(token),),
            ).fetchone()
            if not row or not password_verify(password, row["password_hash"]):
                raise PermissionError("step-up authentication failed")
            db.execute(
                "UPDATE prime_core.sessions SET step_up_at=%s,last_seen_at=%s WHERE session_id=%s",
                (timestamp, timestamp, row["session_id"]),
            )
            self._audit(db, "operator", row["operator_id"], "operator.step_up")
            return {"authenticated": True, "step_up_at": timestamp.isoformat(), "valid_for_seconds": 300}

    def step_up_is_recent(self, session: dict[str, Any], max_age_seconds: int = 300) -> bool:
        value = session.get("step_up_at")
        if not value:
            return False
        if value.tzinfo is None:
            value = value.replace(tzinfo=UTC)
        return (now() - value).total_seconds() <= max_age_seconds

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

    def provision_local_recovery(self, credential: str) -> None:
        if len(credential) < 32:
            raise ValueError("local recovery credential is too short")
        with transaction(self.settings) as db:
            row = db.execute("SELECT operator_id, local_recovery_hash FROM prime_core.operators LIMIT 1").fetchone()
            if not row:
                raise ValueError("operator is not initialized")
            if row["local_recovery_hash"]:
                raise ValueError("local recovery is already provisioned")
            db.execute(
                "UPDATE prime_core.operators SET local_recovery_hash=%s, updated_at=now() WHERE operator_id=%s",
                (token_digest(credential), row["operator_id"]),
            )
            self._audit(db, "operator", row["operator_id"], "operator.local_recovery_provisioned", metadata={"secret_storage": "platform-secured-local-reference"})

    def recover_local(self, credential: str, new_password: str) -> tuple[str, str]:
        if len(new_password) < 12:
            raise ValueError("password must contain at least 12 characters")
        replacement = new_token()
        local_replacement = new_token()
        with transaction(self.settings) as db:
            row = db.execute("SELECT operator_id, local_recovery_hash FROM prime_core.operators LIMIT 1").fetchone()
            if not row or not row["local_recovery_hash"] or token_digest(credential) != row["local_recovery_hash"]:
                raise PermissionError("invalid local recovery credential")
            db.execute(
                "UPDATE prime_core.operators SET password_hash=%s, recovery_hash=%s, local_recovery_hash=%s, updated_at=now() WHERE operator_id=%s",
                (password_hash(new_password), token_digest(replacement), token_digest(local_replacement), row["operator_id"]),
            )
            db.execute("UPDATE prime_core.sessions SET revoked_at=now() WHERE revoked_at IS NULL")
            self._audit(db, "operator", row["operator_id"], "operator.local_recovery_reset", metadata={"recovery_issued": True, "local_recovery_rotated": True})
        return replacement, local_replacement

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

    def create_project(self, name: str, description: str = "", image_url: str | None = None) -> dict[str, Any]:
        timestamp = now()
        project_id = _id("project")
        with transaction(self.settings) as db:
            row = db.execute(
                "INSERT INTO prime_core.projects(project_id, name, description, image_url, lifecycle_state, connectivity_state, freshness_state, work_condition, onboarding_step, onboarding_state, created_at, updated_at) "
                "VALUES (%s,%s,%s,%s,'DRAFT','OFFLINE','UNKNOWN','REVIEW_REQUIRED','IDENTITY','IN_PROGRESS',%s,%s) RETURNING *",
                (project_id, name, description, image_url, timestamp, timestamp),
            ).fetchone()
            self._audit(db, "operator", "operator", "project.created", project_id=project_id, target_id=project_id)
            return dict(row)

    def update_project_metadata(self, project_id: str, name: str, description: str = "", image_url: str | None = None) -> dict[str, Any]:
        timestamp = now()
        with transaction(self.settings) as db:
            row = db.execute(
                "UPDATE prime_core.projects SET name=%s, description=%s, image_url=%s, updated_at=%s WHERE project_id=%s RETURNING *",
                (name, description, image_url, timestamp, project_id),
            ).fetchone()
            if not row:
                raise KeyError("project not found")
            self._audit(db, "operator", "operator", "project.metadata_updated", project_id=project_id, target_id=project_id)
            return dict(row)

    @staticmethod
    def _within_allowed_root(candidate: Path, allowed_roots: list[str]) -> bool:
        resolved = candidate.resolve(strict=False)
        return any(resolved == Path(raw).resolve(strict=False) or Path(raw).resolve(strict=False) in resolved.parents for raw in allowed_roots)

    def inspect_repository_for_onboarding(self, project_id: str, node_id: str, requested_path: str) -> dict[str, Any]:
        candidate = Path(requested_path).expanduser()
        if ".." in candidate.parts:
            raise ValueError("repository path traversal is not allowed")
        with connect(self.settings) as db:
            project = db.execute("SELECT project_id FROM prime_core.projects WHERE project_id=%s", (project_id,)).fetchone()
            node = db.execute("SELECT * FROM prime_core.nodes WHERE node_id=%s", (node_id,)).fetchone()
        if not project:
            raise KeyError("project not found")
        if not node:
            raise KeyError("node not found")
        if node["status"] in {"OFFLINE", "REVOKED"}:
            raise ValueError(f"Node is {node['status']}")
        roots = node["allowed_roots"] if isinstance(node["allowed_roots"], list) else json.loads(node["allowed_roots"] or "[]")
        if not self._within_allowed_root(candidate, roots):
            raise PermissionError("path is outside the enrolled Node allowed roots")
        try:
            remote = self._node_client(dict(node)).inspect_repository(str(candidate))
        except NodeClientError as exc:
            raise ValueError(str(exc)) from exc
        if remote.get("is_bare"):
            raise ValueError("bare repositories are not supported")
        top = str(remote["canonical_path"])
        common = str(remote["git_common_dir"])
        identity = str(remote["identity_fingerprint"])
        with connect(self.settings) as db:
            duplicate = db.execute("SELECT project_id FROM prime_core.repositories WHERE identity_fingerprint=%s AND project_id<>%s", (identity, project_id)).fetchone()
        authority_state = str(remote.get("authority_state") or "NONE")
        return {"project_id": project_id, "node_id": node_id, "node_name": node["name"], "canonical_path": top, "git_common_dir": common, "identity_fingerprint": identity, "is_bare": False, "branch": remote.get("branch") or "DETACHED", "authority_state": authority_state, "duplicate_project_id": duplicate["project_id"] if duplicate else None, "onboarding_decision": "REJECT_DUPLICATE" if duplicate else "REVIEW_AUTHORITY" if authority_state != "NONE" else "READY_TO_BIND"}

    def bind_verified_repository(self, inspection: dict[str, Any], confirm: bool = False) -> dict[str, Any]:
        if not confirm:
            raise ValueError("operator confirmation is required before binding a repository")
        if inspection.get("duplicate_project_id"):
            raise ValueError("repository is already bound to another active project")
        result = self.bind_repository(inspection["project_id"], inspection["node_id"], inspection["identity_fingerprint"], inspection["canonical_path"], False)
        with transaction(self.settings) as db:
            db.execute("UPDATE prime_core.projects SET onboarding_step='AUTHORITY', onboarding_state='IN_PROGRESS', updated_at=%s WHERE project_id=%s", (now(), inspection["project_id"]))
        return {**result, "authority_state": inspection.get("authority_state", "UNKNOWN")}

    @staticmethod
    def _authority_project_hash(root: Path) -> str | None:
        digest = hashlib.sha256()
        for relative in REQUIRED_AUTHORITY_FILES:
            path = root / relative
            if not path.is_file():
                return None
            digest.update(relative.encode("utf-8"))
            digest.update(b"\0")
            digest.update(path.read_bytes())
        return digest.hexdigest()

    @staticmethod
    def _rebind_refusal(project_id: str, reason: str, **details: Any) -> dict[str, Any]:
        return {
            "project_id": project_id,
            "continuity_verdict": "REFUSED",
            "refusal_reason": reason,
            "preflight_token": None,
            **details,
        }

    def inspect_repository_rebind(self, project_id: str, destination_node_id: str, destination_path: str) -> dict[str, Any]:
        """Return a non-mutating, fail-closed rebind preflight."""
        with connect(self.settings) as db:
            binding = db.execute(
                "SELECT p.project_id,b.repository_id,b.node_id,b.binding_status,b.canonical_revision,b.canonical_ref,b.canonical_ref_commit,b.binding_revision,"
                "r.canonical_path,r.identity_fingerprint,r.is_bare,n.status AS current_node_status,n.name AS current_node_name "
                "FROM prime_core.projects p JOIN prime_core.project_bindings b ON b.project_id=p.project_id "
                "JOIN prime_core.repositories r ON r.repository_id=b.repository_id "
                "JOIN prime_core.nodes n ON n.node_id=b.node_id WHERE p.project_id=%s",
                (project_id,),
            ).fetchone()
            node = db.execute("SELECT node_id,name,status,allowed_roots FROM prime_core.nodes WHERE node_id=%s", (destination_node_id,)).fetchone()
        if not binding:
            raise KeyError("project has no repository binding")
        if not node:
            return self._rebind_refusal(project_id, "DESTINATION_NODE_NOT_FOUND", current_repository_id=binding["repository_id"])
        if node["status"] in {"OFFLINE", "REVOKED"}:
            return self._rebind_refusal(project_id, "DESTINATION_NODE_UNAVAILABLE", destination_node_status=node["status"])
        canonical_ref = binding["canonical_ref"]
        canonical_commit = binding["canonical_ref_commit"]
        if not canonical_ref or not canonical_commit:
            return self._rebind_refusal(project_id, "CANONICAL_REF_CONTINUITY_UNAVAILABLE")
        roots = node["allowed_roots"] if isinstance(node["allowed_roots"], list) else json.loads(node["allowed_roots"] or "[]")
        candidate_input = Path(destination_path).expanduser()
        if not candidate_input.exists():
            return self._rebind_refusal(project_id, "DESTINATION_ABSENT", destination_path=str(candidate_input))
        if not self._within_allowed_root(candidate_input, roots):
            return self._rebind_refusal(project_id, "DESTINATION_OUTSIDE_ALLOWED_ROOT", destination_path=str(candidate_input))
        try:
            candidate = inspect_repository_candidate(candidate_input, canonical_ref, canonical_commit)
        except (OSError, GitProvenanceError) as exc:
            reason = str(exc)
            if "bare" in reason:
                reason = "BARE_REPOSITORY"
            elif "unexpected commit" in reason:
                reason = "CANONICAL_REF_MISMATCH"
            elif "worktree administrative" in reason:
                reason = "GIT_WORKTREE_REPAIR_REQUIRED"
            else:
                reason = "CANDIDATE_NOT_GIT"
            return self._rebind_refusal(project_id, reason, detail=str(exc))
        if not self._within_allowed_root(Path(candidate["candidate_top_level"]), roots):
            return self._rebind_refusal(project_id, "CANDIDATE_OUTSIDE_ALLOWED_ROOT", candidate=candidate)
        duplicate = None
        with connect(self.settings) as db:
            duplicate = db.execute(
                "SELECT project_id FROM prime_core.repositories WHERE identity_fingerprint=%s AND project_id<>%s",
                (candidate["candidate_location_fingerprint"], project_id),
            ).fetchone()
        if duplicate:
            return self._rebind_refusal(project_id, "DESTINATION_ALREADY_BOUND", duplicate_project_id=duplicate["project_id"], candidate=candidate)
        current_root = Path(binding["canonical_path"]).resolve(strict=True)
        try:
            current = inspect_repository_candidate(current_root, canonical_ref, canonical_commit)
        except (OSError, GitProvenanceError) as exc:
            return self._rebind_refusal(project_id, "CURRENT_BINDING_CONTINUITY_UNAVAILABLE", detail=str(exc))
        current_authority_hash = self._authority_project_hash(current_root)
        candidate_authority_hash = self._authority_project_hash(Path(candidate["candidate_top_level"]))
        if not current_authority_hash or not candidate_authority_hash or current_authority_hash != candidate_authority_hash:
            return self._rebind_refusal(project_id, "AUTHORITY_PROJECT_CONTINUITY_UNPROVEN", candidate=candidate)
        if candidate["dirty"] and (
            candidate["candidate_top_level"] != current["candidate_top_level"]
            or candidate["candidate_common_dir"] != current["candidate_common_dir"]
        ):
            return self._rebind_refusal(project_id, "DIRTY_REBIND_REQUIRES_VERIFIABLE_WORKTREE_CONTINUITY", candidate=candidate)
        known_objects = sorted({current["canonical_ref_commit"], current["canonical_tree"], current["candidate_head"], current["candidate_head_tree"]})
        anchor_id = _id("anchor")
        preflight_token = _id("rebind")
        snapshot = {
            "project_id": project_id,
            "repository_id": binding["repository_id"],
            "binding_revision": binding["binding_revision"],
            "destination_node_id": destination_node_id,
            "destination_path": candidate["candidate_top_level"],
            "candidate_path": candidate["candidate_path"],
            "candidate_fingerprint": candidate["candidate_location_fingerprint"],
            "candidate_location_fingerprint": candidate["candidate_location_fingerprint"],
            "candidate_head": candidate["candidate_head"],
            "canonical_ref": canonical_ref,
            "canonical_ref_commit": canonical_commit,
            "canonical_tree": candidate["canonical_tree"],
            "authority_project_hash": current_authority_hash,
            "dirty": candidate["dirty"],
            "worktree_admin_health": candidate["worktree_admin_health"],
        }
        with transaction(self.settings) as db:
            db.execute(
                "INSERT INTO prime_core.repository_continuity_anchors(anchor_id,project_id,repository_id,canonical_ref,canonical_ref_commit,canonical_revision,canonical_tree,known_objects,authority_project_hash,worktree_path,identity_fingerprint,created_at,metadata) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),%s) ON CONFLICT (project_id,repository_id,canonical_ref,canonical_ref_commit) DO UPDATE SET canonical_tree=EXCLUDED.canonical_tree,known_objects=EXCLUDED.known_objects,authority_project_hash=EXCLUDED.authority_project_hash,worktree_path=EXCLUDED.worktree_path,identity_fingerprint=EXCLUDED.identity_fingerprint,metadata=EXCLUDED.metadata",
                (anchor_id, project_id, binding["repository_id"], canonical_ref, canonical_commit, binding["canonical_revision"], current["canonical_tree"], json.dumps(known_objects), current_authority_hash, current["candidate_top_level"], current["candidate_location_fingerprint"], json.dumps({"source": "repository_rebind_preflight", "logical_continuity": True})),
            )
            db.execute(
                "INSERT INTO prime_core.repository_rebind_preflights(preflight_token,project_id,repository_id,destination_node_id,destination_path,candidate_fingerprint,candidate_head,binding_revision,snapshot,status,created_at,expires_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,'OPEN',now(),now()+interval '15 minutes')",
                (preflight_token, project_id, binding["repository_id"], destination_node_id, candidate["candidate_top_level"], candidate["candidate_location_fingerprint"], candidate["candidate_head"], binding["binding_revision"], json.dumps(snapshot)),
            )
        return {
            "project_id": project_id,
            "repository_id": binding["repository_id"],
            "current_path": binding["canonical_path"],
            "current_node_id": binding["node_id"],
            "current_location_fingerprint": binding["identity_fingerprint"],
            "candidate": candidate,
            "canonical_ref_continuity": "VERIFIED",
            "canonical_commit_continuity": "VERIFIED",
            "known_history_object_continuity": "VERIFIED",
            "authority_project_continuity": "VERIFIED",
            "duplicate_active_binding": "NONE",
            "dirty_worktree": "VERIFIED" if not candidate["dirty"] or candidate["candidate_top_level"] == current["candidate_top_level"] else "REQUIRES_REVIEW",
            "worktree_administrative_health": candidate["worktree_admin_health"],
            "continuity_verdict": "LOGICAL_REPOSITORY_CONTINUITY_VERIFIED",
            "refusal_reason": None,
            "preflight_token": preflight_token,
            "binding_revision": binding["binding_revision"],
            "real_relocation_candidate": candidate["candidate_top_level"] != current["candidate_top_level"],
        }

    def confirm_repository_rebind(self, project_id: str, preflight_token: str, confirm: bool = False) -> dict[str, Any]:
        if not confirm:
            raise ValueError("operator confirmation is required before repository rebind")
        with connect(self.settings) as db:
            preflight = db.execute("SELECT * FROM prime_core.repository_rebind_preflights WHERE preflight_token=%s", (preflight_token,)).fetchone()
        if not preflight or preflight["project_id"] != project_id:
            raise ValueError("rebind preflight not found")
        if preflight["status"] != "OPEN" or preflight["expires_at"] <= now():
            raise ValueError("STALE_REBIND_PREFLIGHT")
        with transaction(self.settings) as db:
            binding = db.execute(
                "SELECT b.*,r.canonical_path,r.identity_fingerprint,r.is_bare FROM prime_core.project_bindings b JOIN prime_core.repositories r ON r.repository_id=b.repository_id WHERE b.project_id=%s FOR UPDATE",
                (project_id,),
            ).fetchone()
            node = db.execute("SELECT node_id,status FROM prime_core.nodes WHERE node_id=%s", (preflight["destination_node_id"],)).fetchone()
            if not binding or binding["binding_revision"] != preflight["binding_revision"] or not node or node["status"] in {"OFFLINE", "REVOKED"}:
                db.execute("UPDATE prime_core.repository_rebind_preflights SET status='STALE' WHERE preflight_token=%s", (preflight_token,))
                raise ValueError("STALE_REBIND_PREFLIGHT")
            snapshot = preflight["snapshot"] if isinstance(preflight["snapshot"], dict) else json.loads(preflight["snapshot"])
            try:
                candidate = inspect_repository_candidate(Path(preflight["destination_path"]), binding["canonical_ref"], binding["canonical_ref_commit"])
            except (OSError, GitProvenanceError) as exc:
                db.execute("UPDATE prime_core.repository_rebind_preflights SET status='STALE' WHERE preflight_token=%s", (preflight_token,))
                raise ValueError("STALE_REBIND_PREFLIGHT") from exc
            if any(candidate.get(key) != snapshot.get(key) for key in ("candidate_path", "candidate_location_fingerprint", "candidate_head", "canonical_ref_commit", "canonical_tree", "dirty")):
                db.execute("UPDATE prime_core.repository_rebind_preflights SET status='STALE' WHERE preflight_token=%s", (preflight_token,))
                raise ValueError("STALE_REBIND_PREFLIGHT")
            old = {"node_id": binding["node_id"], "path": binding["canonical_path"], "fingerprint": binding["identity_fingerprint"]}
            updated = db.execute(
                "UPDATE prime_core.repositories SET node_id=%s,canonical_path=%s,identity_fingerprint=%s,last_observed_at=now() WHERE repository_id=%s RETURNING *",
                (preflight["destination_node_id"], candidate["candidate_top_level"], candidate["candidate_location_fingerprint"], binding["repository_id"]),
            ).fetchone()
            db.execute("UPDATE prime_core.project_bindings SET node_id=%s,binding_status='REBOUND',binding_revision=binding_revision+1,updated_at=now() WHERE project_id=%s", (preflight["destination_node_id"], project_id))
            db.execute(
                "INSERT INTO prime_core.repository_rebind_history(rebind_id,project_id,repository_id,previous_node_id,previous_path,previous_fingerprint,new_node_id,new_path,new_fingerprint,continuity_verdict,evidence,occurred_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now())",
                (_id("rebind"), project_id, binding["repository_id"], old["node_id"], old["path"], old["fingerprint"], preflight["destination_node_id"], candidate["candidate_top_level"], candidate["candidate_location_fingerprint"], "LOGICAL_REPOSITORY_CONTINUITY_VERIFIED", json.dumps({"preflight_token": preflight_token, "canonical_ref": binding["canonical_ref"], "canonical_commit": binding["canonical_ref_commit"], "authority_project_hash": snapshot.get("authority_project_hash")})),
            )
            db.execute("UPDATE prime_core.repository_rebind_preflights SET status='CONSUMED',consumed_at=now() WHERE preflight_token=%s", (preflight_token,))
            self._audit(db, "operator", "operator", "repository.rebound", project_id=project_id, target_id=binding["repository_id"], metadata={"previous_path": old["path"], "new_path": candidate["candidate_top_level"], "preflight_token": preflight_token})
            sequence = db.execute("SELECT COALESCE(MAX(project_sequence),0)+1 AS next_sequence FROM prime_core.events WHERE project_id=%s", (project_id,)).fetchone()["next_sequence"]
            db.execute("INSERT INTO prime_core.events(event_id,project_id,event_type,occurred_at,observed_at,project_sequence,source_revision,source_ref,payload,dedupe_key) VALUES (%s,%s,'REPOSITORY_REBOUND',now(),now(),%s,%s,%s,%s,%s)", (_id("evt"), project_id, sequence, binding["canonical_ref_commit"], candidate["candidate_top_level"], json.dumps({"repository_id": binding["repository_id"], "previous_path": old["path"], "new_path": candidate["candidate_top_level"], "continuity": "LOGICAL_REPOSITORY_CONTINUITY_VERIFIED"}), f"repository-rebound:{preflight_token}"))
            return {"project_id": project_id, "repository_id": binding["repository_id"], "binding_status": "REBOUND", "binding_revision": binding["binding_revision"] + 1, "previous": old, "current": dict(updated), "continuity_verdict": "LOGICAL_REPOSITORY_CONTINUITY_VERIFIED", "history_recorded": True, "preflight_token": preflight_token}

    def configure_canonical_ref(self, project_id: str, canonical_ref: str, confirm: bool = False) -> dict[str, Any]:
        """Persist an explicit canonical ref; active worktree state never changes it implicitly."""
        if not confirm:
            raise ValueError("operator confirmation is required before changing the canonical ref")
        with connect(self.settings) as db:
            row = db.execute(
                "SELECT r.canonical_path FROM prime_core.project_bindings b "
                "JOIN prime_core.repositories r ON r.repository_id=b.repository_id "
                "WHERE b.project_id=%s",
                (project_id,),
            ).fetchone()
        if not row:
            raise KeyError("project has no repository binding")
        root = Path(row["canonical_path"]).resolve(strict=True)
        try:
            commit = resolve_canonical_ref(root, canonical_ref)
        except GitProvenanceError as exc:
            raise ValueError(str(exc)) from exc
        timestamp = now()
        with transaction(self.settings) as db:
            updated = db.execute(
                "UPDATE prime_core.project_bindings SET canonical_ref=%s,canonical_ref_commit=%s,canonical_ref_updated_at=%s,updated_at=%s "
                "WHERE project_id=%s RETURNING project_id,canonical_ref,canonical_ref_commit,canonical_ref_updated_at",
                (canonical_ref, commit, timestamp, timestamp, project_id),
            ).fetchone()
            if not updated:
                raise KeyError("project has no repository binding")
            self._audit(db, "operator", "operator", "repository.canonical_ref_configured", project_id=project_id, target_id=canonical_ref, metadata={"canonical_commit": commit})
        return {**dict(updated), "repository_path": str(root), "change": "EXPLICIT_OPERATOR_CONFIGURATION"}

    def create_repository_for_onboarding(self, project_id: str, node_id: str, parent_path: str, repository_name: str, confirm: bool = False) -> dict[str, Any]:
        if not confirm:
            raise ValueError("operator confirmation is required before creating a repository")
        if not repository_name or repository_name in {".", ".."} or Path(repository_name).name != repository_name:
            raise ValueError("repository name must be one directory name")
        with connect(self.settings) as db:
            node = db.execute("SELECT * FROM prime_core.nodes WHERE node_id=%s", (node_id,)).fetchone()
        if not node:
            raise KeyError("node not found")
        if node["status"] in {"OFFLINE", "REVOKED"}:
            raise ValueError(f"Node is {node['status']}")
        roots = node["allowed_roots"] if isinstance(node["allowed_roots"], list) else json.loads(node["allowed_roots"] or "[]")
        parent = Path(parent_path).expanduser()
        if ".." in parent.parts or not self._within_allowed_root(parent, roots):
            raise PermissionError("repository parent is outside the enrolled Node allowed roots")
        target = parent / repository_name
        idempotency_key = f"create-repository:{project_id}:{target}"
        workflow = self.start_or_get_workflow("CREATE_REPOSITORY", idempotency_key, project_id, [
            {"step_key": "DIRECTORY_CREATED", "replay_policy": "IDEMPOTENT_EXTERNAL"},
            {"step_key": "GIT_INITIALIZED", "replay_policy": "IDEMPOTENT_EXTERNAL"},
            {"step_key": "BOUND", "replay_policy": "PURE_OR_DB_TRANSACTION"},
        ])
        self.record_workflow_resource(workflow["workflow_id"], "REPOSITORY", "onboarding-repository", str(target), {"project_id": project_id, "node_id": node_id, "node_operation_id": workflow["workflow_id"]}, "EXPECTED")
        current_step = "DIRECTORY_CREATED"
        try:
            started = self.begin_step(workflow["workflow_id"], "DIRECTORY_CREATED")
            remote = None
            if started.get("decision") == "REPAIR_REQUIRED":
                try:
                    remote = self._node_client(dict(node)).create_repository(str(parent), repository_name, workflow["workflow_id"])
                except NodeClientError as exc:
                    raise ValueError(str(exc)) from exc
                self.mark_workflow_repaired(
                    workflow["workflow_id"],
                    "DIRECTORY_CREATED",
                    {"node_operation_id": workflow["workflow_id"], "reconciliation": "NODE_IDEMPOTENCY_CONFIRMED"},
                )
                started = self.begin_step(workflow["workflow_id"], "DIRECTORY_CREATED")
            if started.get("decision") != "SKIP_COMPLETED":
                if remote is None:
                    try:
                        remote = self._node_client(dict(node)).create_repository(str(parent), repository_name, workflow["workflow_id"])
                    except NodeClientError as exc:
                        raise ValueError(str(exc)) from exc
                self.record_workflow_resource(workflow["workflow_id"], "REPOSITORY", "onboarding-repository", remote["canonical_path"], {"project_id": project_id, "node_id": node_id, "node_operation_id": workflow["workflow_id"]}, "CREATED")
                self.complete_step(workflow["workflow_id"], "DIRECTORY_CREATED", side_effect_state={"path": remote["canonical_path"], "node_operation_id": workflow["workflow_id"]})
            current_step = "GIT_INITIALIZED"
            started = self.begin_step(workflow["workflow_id"], "GIT_INITIALIZED")
            if started.get("decision") != "SKIP_COMPLETED":
                if remote is None:
                    try:
                        remote = self._node_client(dict(node)).create_repository(str(parent), repository_name, workflow["workflow_id"])
                    except NodeClientError as exc:
                        raise ValueError(str(exc)) from exc
                self.complete_step(workflow["workflow_id"], "GIT_INITIALIZED", side_effect_state={"path": str(target), "git": "verified"})
            current_step = "BOUND"
            started = self.begin_step(workflow["workflow_id"], "BOUND")
            if started.get("decision") == "SKIP_COMPLETED":
                with connect(self.settings) as db:
                    bound = dict(db.execute("SELECT * FROM prime_core.repositories WHERE project_id=%s", (project_id,)).fetchone())
                inspection = self.inspect_repository_for_onboarding(project_id, node_id, str(target))
            else:
                inspection = self.inspect_repository_for_onboarding(project_id, node_id, str(target))
                bound = self.bind_verified_repository(inspection, confirm=True)
                self.complete_step(workflow["workflow_id"], "BOUND", result_metadata={"repository_id": bound.get("repository_id")})
            self.complete_workflow(workflow["workflow_id"], "BOUND")
            return {"workflow": workflow["workflow_id"], "repository": bound, "inspection": inspection}
        except Exception as exc:
            try:
                self.fail_step(workflow["workflow_id"], current_step, str(exc), retryable=True, ambiguous_external_effect=False)
            except Exception:
                pass
            with transaction(self.settings) as db:
                db.execute("UPDATE prime_core.workflows SET status='REPAIR_REQUIRED', current_step=%s, last_error=%s, updated_at=%s WHERE workflow_id=%s", (current_step, type(exc).__name__, now(), workflow["workflow_id"]))
                db.execute("UPDATE prime_core.projects SET lifecycle_state='PROVISIONING', work_condition='REVIEW_REQUIRED', onboarding_state='REPAIR_REQUIRED', updated_at=%s WHERE project_id=%s", (now(), project_id))
            raise

    def bootstrap_project_authority(self, project_id: str, confirm: bool = False) -> dict[str, Any]:
        if not confirm:
            raise ValueError("operator confirmation is required before authority bootstrap")
        with connect(self.settings) as db:
            row = db.execute("SELECT r.canonical_path,n.* FROM prime_core.repositories r JOIN prime_core.nodes n ON n.node_id=r.node_id WHERE r.project_id=%s", (project_id,)).fetchone()
        if not row:
            raise ValueError("bind a verified repository before authority bootstrap")
        template_root = self._authority_template_root()
        files = {relative: (template_root / relative).read_text(encoding="utf-8") for relative in REQUIRED_AUTHORITY_FILES}
        operation_id = f"authority-bootstrap:{project_id}"
        source_hash = hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()
        workflow = self.start_or_get_workflow("PROVISION_PROJECT_AUTHORITY", operation_id, project_id, [
            {"step_key": "AUTHORITY_EXPECTED", "replay_policy": "PURE_OR_DB_TRANSACTION"},
            {"step_key": "AUTHORITY_WRITTEN", "replay_policy": "IDEMPOTENT_EXTERNAL"},
            {"step_key": "REVISION_RECORDED", "replay_policy": "PURE_OR_DB_TRANSACTION"},
            {"step_key": "ONBOARDING_ADVANCED", "replay_policy": "PURE_OR_DB_TRANSACTION"},
        ])
        step = self.begin_step(workflow["workflow_id"], "AUTHORITY_EXPECTED")
        if step["decision"] != "SKIP_COMPLETED":
            self.record_workflow_resource(workflow["workflow_id"], "AUTHORITY", "project-authority", str(Path(row["canonical_path"]) / ".agent"), {"template": "authority-template/v1", "source_hash": source_hash, "node_id": row["node_id"]}, "EXPECTED")
            self.complete_step(workflow["workflow_id"], "AUTHORITY_EXPECTED")
        authority: dict[str, Any] = {"files": sorted(files), "reconciled": True}
        step = self.begin_step(workflow["workflow_id"], "AUTHORITY_WRITTEN")
        if step["decision"] != "SKIP_COMPLETED":
            qualification_interrupt("PROVISION_PROJECT_AUTHORITY", "AUTHORITY_WRITTEN", "BEFORE_EXTERNAL_CALL")
            authority = self._node_client(dict(row)).bootstrap_authority(row["canonical_path"], files, operation_id)
            qualification_interrupt("PROVISION_PROJECT_AUTHORITY", "AUTHORITY_WRITTEN", "EXTERNAL_SUCCESS_BEFORE_PERSIST")
            self.record_workflow_resource(workflow["workflow_id"], "AUTHORITY", "project-authority", str(Path(row["canonical_path"]) / ".agent"), {"template": "authority-template/v1", "source_hash": source_hash, "node_id": row["node_id"], "node_operation_id": operation_id}, "CREATED")
            self.complete_step(workflow["workflow_id"], "AUTHORITY_WRITTEN", side_effect_state={"source_hash": source_hash, "node_operation_id": operation_id})
        step = self.begin_step(workflow["workflow_id"], "REVISION_RECORDED")
        if step["decision"] != "SKIP_COMPLETED":
            with connect(self.settings) as db:
                revision = db.execute("SELECT authority_revision_id FROM prime_core.authority_revisions WHERE project_id=%s AND source_path='.agent' AND source_hash=%s ORDER BY observed_at DESC LIMIT 1", (project_id, source_hash)).fetchone()
            if not revision:
                revision = self.record_authority_revision(project_id, ".agent", source_hash, "VALID", {"provenance": "operator-approved authority-template/v1", "template_manifest": str(template_root / "MANIFEST.sha256"), "node_id": row["node_id"]}, canonical_commit=None)
            self.complete_step(workflow["workflow_id"], "REVISION_RECORDED", {"authority_revision_id": revision["authority_revision_id"]})
        step = self.begin_step(workflow["workflow_id"], "ONBOARDING_ADVANCED")
        if step["decision"] != "SKIP_COMPLETED":
            with transaction(self.settings) as db:
                db.execute("UPDATE prime_core.projects SET onboarding_step='GOAL', onboarding_state='IN_PROGRESS', updated_at=%s WHERE project_id=%s", (now(), project_id))
            self.complete_step(workflow["workflow_id"], "ONBOARDING_ADVANCED")
        self.complete_workflow(workflow["workflow_id"], "ONBOARDING_ADVANCED")
        return {"project_id": project_id, "workflow_id": workflow["workflow_id"], "authority": authority, "state": "CURRENT", "template": "authority-template/v1"}

    def review_or_adopt_project_authority(self, project_id: str, decision: str, confirm: bool = False) -> dict[str, Any]:
        if decision not in {"REVIEW", "ADOPT"}:
            raise ValueError("authority decision must be REVIEW or ADOPT")
        with connect(self.settings) as db:
            row = db.execute("SELECT canonical_path FROM prime_core.repositories WHERE project_id=%s", (project_id,)).fetchone()
        if not row:
            raise ValueError("bind a verified repository before authority review")
        root = Path(row["canonical_path"]).resolve(strict=True)
        validation = validate_authority(root)
        state = "CURRENT" if validation["valid"] else "INVALID" if (root / ".agent").exists() else "NONE"
        if decision == "ADOPT" and not confirm:
            raise ValueError("operator confirmation is required before adopting existing authority")
        if decision == "ADOPT" and state != "CURRENT":
            raise ValueError("only a valid existing authority package can be adopted")
        if decision == "ADOPT":
            source_hash = hashlib.sha256(json.dumps(validation, sort_keys=True).encode()).hexdigest()
            with connect(self.settings) as db:
                existing = db.execute(
                    "SELECT authority_revision_id FROM prime_core.authority_revisions "
                    "WHERE project_id=%s AND source_path=%s AND source_hash=%s "
                    "AND metadata->>'decision'='ADOPT' ORDER BY observed_at DESC LIMIT 1",
                    (project_id, ".agent", source_hash),
                ).fetchone()
            if existing:
                return {
                    "project_id": project_id,
                    "decision": decision,
                    "state": state,
                    "valid": validation["valid"],
                    "missing": validation["missing"],
                    "files": validation["files"],
                    "rewrite": "NONE",
                    "adoption_status": "ALREADY_ADOPTED",
                    "authority_revision_id": existing["authority_revision_id"],
                }
            self.record_authority_revision(project_id, ".agent", source_hash, "VALID", {"provenance": "operator-approved existing authority adoption", "decision": "ADOPT"}, canonical_commit=None)
            with transaction(self.settings) as db:
                db.execute("UPDATE prime_core.projects SET onboarding_step='GOAL', onboarding_state='IN_PROGRESS', updated_at=%s WHERE project_id=%s", (now(), project_id))
        return {"project_id": project_id, "decision": decision, "state": state, "valid": validation["valid"], "missing": validation["missing"], "files": validation["files"], "rewrite": "NONE"}

    def inspect_project_authority_migration(self, project_id: str) -> dict[str, Any]:
        with connect(self.settings) as db:
            row = db.execute("SELECT canonical_path FROM prime_core.repositories WHERE project_id=%s", (project_id,)).fetchone()
        if not row:
            raise KeyError("project has no repository binding")
        root = Path(row["canonical_path"]).resolve(strict=True)
        files = {
            relative: (root / relative).read_text(encoding="utf-8", errors="replace")
            for relative in REQUIRED_AUTHORITY_FILES
            if (root / relative).is_file()
        }
        plan = authority_migration_plan(files)
        return {"project_id": project_id, "repository_path": str(root), "source_state": classify_authority_snapshot(files), "plan": plan, "source_hashes": {relative: hashlib.sha256(content.encode()).hexdigest() for relative, content in files.items()}}

    def migrate_project_authority(self, project_id: str, confirm: bool = False) -> dict[str, Any]:
        plan = self.inspect_project_authority_migration(project_id)
        if plan["source_state"] != "LEGACY":
            if plan["source_state"] == "CURRENT":
                return {**plan, "migration": "NOOP"}
            raise ValueError("authority is not a recognized legacy package; review is required")
        if not confirm:
            raise ValueError("explicit MIGRATE confirmation is required")
        with connect(self.settings) as db:
            row = db.execute("SELECT canonical_path FROM prime_core.repositories WHERE project_id=%s", (project_id,)).fetchone()
        root = Path(row["canonical_path"]).resolve(strict=True)
        result = migrate_authority(self._authority_template_root(), root, {
            relative: (root / relative).read_text(encoding="utf-8", errors="replace")
            for relative in REQUIRED_AUTHORITY_FILES
            if (root / relative).is_file()
        }, confirm=True)
        validation = validate_authority(root)
        if not validation["valid"]:
            raise ValueError("authority migration did not produce a valid package")
        self.record_authority_revision(project_id, ".agent", hashlib.sha256(json.dumps(validation, sort_keys=True).encode()).hexdigest(), "VALID", {"decision": "MIGRATE", "preserved_source_hashes": plan["source_hashes"], "provenance": "explicit operator migration"})
        return {**plan, "migration": "APPLIED", "authority": result}

    def list_projects(self) -> list[dict[str, Any]]:
        with connect(self.settings) as db:
            return [dict(row) for row in db.execute("SELECT * FROM prime_core.projects WHERE lifecycle_state <> 'DELETED' ORDER BY created_at").fetchall()]

    def bound_repository_lifecycle(self, project_id: str, operation_id: str, action: str) -> dict[str, Any]:
        with connect(self.settings) as db:
            row = db.execute(
                "SELECT r.repository_id,r.canonical_path,r.identity_fingerprint,n.* "
                "FROM prime_core.project_bindings b JOIN prime_core.repositories r ON r.repository_id=b.repository_id "
                "JOIN prime_core.nodes n ON n.node_id=b.node_id WHERE b.project_id=%s",
                (project_id,),
            ).fetchone()
        if not row:
            return {"status": "NOT_APPLICABLE", "reason": "PROJECT_HAS_NO_BOUND_REPOSITORY"}
        client = self._node_client(dict(row))
        if action == "QUARANTINE":
            result = client.quarantine_repository(row["canonical_path"], operation_id)
        elif action == "RESTORE":
            result = client.restore_quarantined_repository(operation_id)
        elif action == "PURGE":
            result = client.purge_quarantined_repository(operation_id)
        else:
            raise ValueError("unsupported bound repository lifecycle action")
        return {**result, "repository_id": row["repository_id"], "node_id": row["node_id"]}

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

    def _node_trust_settings(self) -> NodeTrustSettings:
        return NodeTrustSettings.from_environment()

    def issue_node_bootstrap(self, node_id: str, endpoint: str, requested_metadata: dict[str, Any]) -> dict[str, Any]:
        trust = self._node_trust_settings()
        token, payload = issue_bootstrap(trust, node_id)
        with transaction(self.settings) as db:
            node = db.execute("SELECT node_id,status,approval_state,trust_state FROM prime_core.nodes WHERE node_id=%s FOR UPDATE", (node_id,)).fetchone()
            if not node:
                raise KeyError("canonical Node record not found")
            if node["approval_state"] == "PENDING_OPERATOR_APPROVAL" or node.get("trust_state") in {"BOOTSTRAP_ISSUED", "NODE_PROOF_RECEIVED", "ACTIVE"}:
                raise ValueError("Node already has an active or pending enrollment")
            db.execute(
                "INSERT INTO prime_core.node_enrollment_challenges(challenge_id,node_id,token_digest,issued_at,expires_at,state,requested_metadata) VALUES (%s,%s,%s,%s,%s,'BOOTSTRAP_ISSUED',%s)",
                (payload["challenge_id"], node_id, digest(token), now(), datetime.fromisoformat(payload["expires_at"]), json.dumps({**requested_metadata, "endpoint": endpoint})),
            )
            db.execute("UPDATE prime_core.nodes SET approval_state='BOOTSTRAP_ISSUED', status='OFFLINE', control_endpoint=%s, trust_state='BOOTSTRAP_ISSUED' WHERE node_id=%s", (endpoint, node_id))
            self._audit(db, "operator", "operator", "node.bootstrap_issued", target_id=node_id, metadata={"challenge_id": payload["challenge_id"], "expires_at": payload["expires_at"]})
        return {**payload, "bootstrap_credential": token, "node_id": node_id, "endpoint": endpoint}

    def sync_node_proof(self, challenge_id: str, node_id: str, csr_pem: str, metadata: dict[str, Any]) -> dict[str, Any]:
        fingerprint = csr_fingerprint(csr_pem)
        with transaction(self.settings) as db:
            challenge = db.execute("SELECT * FROM prime_core.node_enrollment_challenges WHERE challenge_id=%s FOR UPDATE", (challenge_id,)).fetchone()
            if not challenge or challenge["node_id"] != node_id:
                raise KeyError("enrollment challenge not found")
            if challenge["expires_at"] <= now():
                db.execute("UPDATE prime_core.node_enrollment_challenges SET state='EXPIRED' WHERE challenge_id=%s", (challenge_id,))
                raise ValueError("enrollment challenge expired")
            if challenge["consumed_at"] or challenge["state"] != "BOOTSTRAP_ISSUED":
                raise ValueError("enrollment challenge was already consumed")
            db.execute("UPDATE prime_core.node_enrollment_challenges SET consumed_at=now(),state='PENDING_OPERATOR_APPROVAL',csr_pem=%s,csr_fingerprint=%s WHERE challenge_id=%s", (csr_pem, fingerprint, challenge_id))
            db.execute("UPDATE prime_core.nodes SET approval_state='PENDING_OPERATOR_APPROVAL', status='OFFLINE', trust_state='NODE_PROOF_RECEIVED', diagnostics=%s WHERE node_id=%s", (json.dumps({**metadata, "challenge_id": challenge_id, "csr_fingerprint": fingerprint}), node_id))
            self._audit(db, "operator", "operator", "node.proof_received", target_id=node_id, metadata={"challenge_id": challenge_id, "csr_fingerprint": fingerprint})
        return {"challenge_id": challenge_id, "node_id": node_id, "approval_state": "PENDING_OPERATOR_APPROVAL", "csr_fingerprint": fingerprint}

    def list_pending_node_enrollments(self) -> list[dict[str, Any]]:
        with connect(self.settings) as db:
            return [dict(row) for row in db.execute("SELECT challenge_id,node_id,issued_at,expires_at,state,csr_fingerprint,requested_metadata FROM prime_core.node_enrollment_challenges WHERE state='PENDING_OPERATOR_APPROVAL' ORDER BY issued_at").fetchall()]

    def _node_client(self, node: dict[str, Any], credential: str | None = None) -> NodeClient:
        trust = self._node_trust_settings()
        value = credential
        if value is None and node.get("credential_ref"):
            path = Path(node["credential_ref"])
            if path.is_file():
                value = path.read_text(encoding="utf-8").strip()
        return NodeClient(NodeClientSettings(
            base_url=node.get("control_endpoint") or os.getenv("PRIME_NODE_CONTROL_ENDPOINT", "https://127.0.0.1:18001"),
            node_id=node["node_id"],
            credential=value,
            ca_file=trust.ca_certificate,
            client_cert=trust.core_client_certificate,
            client_key=trust.core_client_private_key,
        ))

    def approve_node_enrollment(self, challenge_id: str) -> dict[str, Any]:
        with connect(self.settings) as db:
            challenge = db.execute("SELECT c.*,n.name,n.platform,n.control_endpoint FROM prime_core.node_enrollment_challenges c JOIN prime_core.nodes n ON n.node_id=c.node_id WHERE c.challenge_id=%s", (challenge_id,)).fetchone()
        if not challenge:
            raise KeyError("enrollment challenge not found")
        if challenge["state"] != "PENDING_OPERATOR_APPROVAL":
            raise ValueError("enrollment is not pending operator approval")
        trust = self._node_trust_settings()
        certificate_pem, certificate = sign_node_certificate(trust, challenge["csr_pem"], challenge["node_id"])
        bearer = new_token()
        node = dict(challenge)
        client = self._node_client(node, credential=None)
        client.approve(certificate_pem, bearer, certificate)
        credential_path = trust.credential_directory / f"{challenge['node_id']}.bearer"
        credential_path.parent.mkdir(parents=True, exist_ok=True)
        temporary = credential_path.with_suffix(".new")
        temporary.write_text(bearer, encoding="utf-8")
        os.chmod(temporary, 0o600)
        temporary.replace(credential_path)
        with transaction(self.settings) as db:
            db.execute("UPDATE prime_core.node_enrollment_challenges SET state='APPROVED',approved_at=now() WHERE challenge_id=%s", (challenge_id,))
            db.execute("UPDATE prime_core.nodes SET status='ENROLLED',approval_state='APPROVED',trust_state='ACTIVE_CREDENTIAL_PENDING_RESTART',certificate_fingerprint=%s,certificate_serial=%s,certificate_issued_at=%s,certificate_expires_at=%s,credential_ref=%s,control_endpoint=%s WHERE node_id=%s", (certificate["fingerprint"], certificate["serial"], certificate["issued_at"], certificate["expires_at"], str(credential_path), challenge["control_endpoint"], challenge["node_id"]))
            self._audit(db, "operator", "operator", "node.approved", target_id=challenge["node_id"], metadata={"challenge_id": challenge_id, "certificate_fingerprint": certificate["fingerprint"]})
        return {"node_id": challenge["node_id"], "challenge_id": challenge_id, "approval_state": "APPROVED", "certificate": certificate, "restart_required": True}

    def reject_node_enrollment(self, challenge_id: str) -> dict[str, Any]:
        with connect(self.settings) as db:
            challenge = db.execute("SELECT c.*,n.control_endpoint FROM prime_core.node_enrollment_challenges c JOIN prime_core.nodes n ON n.node_id=c.node_id WHERE c.challenge_id=%s", (challenge_id,)).fetchone()
        if not challenge:
            raise KeyError("enrollment challenge not found")
        try:
            self._node_client(dict(challenge), credential=None).reject()
        except NodeClientError:
            pass
        with transaction(self.settings) as db:
            db.execute("UPDATE prime_core.node_enrollment_challenges SET state='REJECTED',rejected_at=now(),revoked_at=now() WHERE challenge_id=%s", (challenge_id,))
            db.execute("UPDATE prime_core.nodes SET status='REVOKED',approval_state='REJECTED',trust_state='REVOKED' WHERE node_id=%s", (challenge["node_id"],))
            self._audit(db, "operator", "operator", "node.rejected", target_id=challenge["node_id"], metadata={"challenge_id": challenge_id})
        return {"node_id": challenge["node_id"], "challenge_id": challenge_id, "approval_state": "REJECTED"}

    def rotate_node_credential(self, node_id: str) -> dict[str, Any]:
        with connect(self.settings) as db:
            row = db.execute("SELECT * FROM prime_core.nodes WHERE node_id=%s", (node_id,)).fetchone()
        if not row or row["approval_state"] not in {"APPROVED", "ACTIVE"} or not row["credential_ref"]:
            raise ValueError("Node is not actively enrolled")
        result = self._node_client(dict(row)).rotate()
        replacement = result.get("node_credential")
        if not replacement:
            raise ValueError("Node did not return a replacement credential")
        path = Path(row["credential_ref"])
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(".new")
        temporary.write_text(replacement, encoding="utf-8")
        os.chmod(temporary, 0o600)
        temporary.replace(path)
        with transaction(self.settings) as db:
            self._audit(db, "operator", "operator", "node.credential_rotated", target_id=node_id, metadata={"credential_ref": str(path)})
        return {"node_id": node_id, "status": "ROTATED", "credential_ref": str(path)}

    def revoke_node(self, node_id: str) -> dict[str, Any]:
        with connect(self.settings) as db:
            row = db.execute("SELECT * FROM prime_core.nodes WHERE node_id=%s", (node_id,)).fetchone()
        if not row:
            raise KeyError("node not found")
        if row["approval_state"] in {"APPROVED", "ACTIVE"} and row["credential_ref"]:
            self._node_client(dict(row)).revoke()
        if row["credential_ref"]:
            Path(row["credential_ref"]).unlink(missing_ok=True)
        with transaction(self.settings) as db:
            db.execute("UPDATE prime_core.nodes SET status='REVOKED',approval_state='REVOKED',trust_state='REVOKED',revoked_at=now(),credential_ref=NULL WHERE node_id=%s", (node_id,))
            self._audit(db, "operator", "operator", "node.revoked", target_id=node_id, metadata={"reason": "operator_action"})
        return {"node_id": node_id, "status": "REVOKED"}

    def refresh_node_health(self) -> None:
        with connect(self.settings) as db:
            nodes = [dict(row) for row in db.execute("SELECT * FROM prime_core.nodes WHERE approval_state IN ('APPROVED','ACTIVE') AND credential_ref IS NOT NULL").fetchall()]
        for node in nodes:
            try:
                result = self._node_client(node).heartbeat()
                with transaction(self.settings) as db:
                    db.execute("UPDATE prime_core.nodes SET status='ONLINE',approval_state='ACTIVE',trust_state='ACTIVE',last_heartbeat_at=now(),last_seen_at=now(),diagnostics=%s WHERE node_id=%s", (json.dumps({"last_heartbeat": result.get("status", "ONLINE")}), node["node_id"]))
            except Exception as exc:
                with transaction(self.settings) as db:
                    db.execute("UPDATE prime_core.nodes SET status='OFFLINE',diagnostics=%s WHERE node_id=%s", (json.dumps({"last_failure": type(exc).__name__}), node["node_id"]))

    def node_client_for_project(self, project_id: str) -> tuple[dict[str, Any], NodeClient] | None:
        self.refresh_node_health()
        with connect(self.settings) as db:
            row = db.execute("SELECT n.* FROM prime_core.nodes n JOIN prime_core.project_bindings b ON b.node_id=n.node_id WHERE b.project_id=%s", (project_id,)).fetchone()
        if not row or not row["control_endpoint"] or not row["credential_ref"] or row["approval_state"] not in {"APPROVED", "ACTIVE"}:
            return None
        node = dict(row)
        return node, self._node_client(node)

    def list_nodes(self) -> list[dict[str, Any]]:
        self.refresh_node_health()
        with connect(self.settings) as db:
            return [dict(row) for row in db.execute("SELECT n.*, c.challenge_id FROM prime_core.nodes n LEFT JOIN LATERAL (SELECT challenge_id FROM prime_core.node_enrollment_challenges c WHERE c.node_id=n.node_id AND c.state='PENDING_OPERATOR_APPROVAL' ORDER BY c.issued_at DESC LIMIT 1) c ON TRUE ORDER BY n.enrolled_at").fetchall()]

    def agent_instruction_chain(self, project_id: str, relative_path: str = "") -> dict[str, Any]:
        with connect(self.settings) as db:
            row = db.execute("SELECT r.canonical_path FROM prime_core.repositories r WHERE r.project_id=%s", (project_id,)).fetchone()
        if not row:
            raise KeyError("project has no repository binding")
        live_node = self.node_client_for_project(project_id)
        if live_node:
            _, client = live_node
            root = PurePosixPath(row["canonical_path"])
            relative = PurePosixPath(relative_path or ".")
            if relative.is_absolute() or ".." in relative.parts:
                raise PermissionError("agent-chain path is outside the bound repository")
            target = root / relative
            directory = target if relative_path.endswith("/") or not relative.suffix else target.parent
            levels = [root]
            current = root
            for part in directory.relative_to(root).parts:
                current /= part
                levels.append(current)
            instructions = []
            for candidate_dir in levels:
                try:
                    listed = client.list_directory(str(candidate_dir))
                except NodeClientError:
                    continue
                candidate = next((entry for entry in listed.get("entries", []) if entry.get("name") == "AGENTS.md" and entry.get("kind") == "file"), None)
                if candidate:
                    result = client.read_file(candidate["path"])
                    instructions.append({"path": PurePosixPath(candidate["path"]).relative_to(root).as_posix(), "scope": candidate_dir.relative_to(root).as_posix() or ".", "content_hash": result.get("content_hash", "UNKNOWN")})
            return {"project_id": project_id, "target": target.relative_to(root).as_posix(), "instructions": instructions, "precedence": "EXPOSED_FOR_CODER_REVIEW; PRIME_DOES_NOT_INVENT_EXTERNAL_AGENT_SEMANTICS", "authority_relationship": ".agent is project authority; AGENTS.md is coding-agent instruction input", "mcp_relationship": "MCP/project context remains bounded by the project grant and exported provenance", "source": "LIVE_NODE"}
        root = Path(row["canonical_path"]).resolve(strict=True)
        target = (root / relative_path).resolve(strict=False)
        if target != root and root not in target.parents:
            raise PermissionError("agent-chain path is outside the bound repository")
        if target.is_dir():
            target = target / "__TARGET__"
        directories = [root, *target.parent.relative_to(root).parents]
        directories = sorted({root, *[root / part for part in target.parent.relative_to(root).parts]}, key=lambda item: len(item.parts))
        instructions = []
        for directory in directories:
            candidate = directory / "AGENTS.md"
            if candidate.is_file():
                instructions.append({"path": candidate.relative_to(root).as_posix(), "scope": directory.relative_to(root).as_posix() or ".", "content_hash": hashlib.sha256(candidate.read_bytes()).hexdigest()})
        return {"project_id": project_id, "target": target.relative_to(root).as_posix(), "instructions": instructions, "precedence": "EXPOSED_FOR_CODER_REVIEW; PRIME_DOES_NOT_INVENT_EXTERNAL_AGENT_SEMANTICS", "authority_relationship": ".agent is project authority; AGENTS.md is coding-agent instruction input", "mcp_relationship": "MCP/project context remains bounded by the project grant and exported provenance"}

    @staticmethod
    def _safe_archive_extract(archive: bytes, target: Path) -> None:
        with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as bundle:
            for member in bundle.getmembers():
                destination = (target / member.name).resolve(strict=False)
                if destination != target and target not in destination.parents:
                    raise ValueError("fork archive contains a path traversal entry")
                if member.issym() or member.islnk():
                    raise ValueError("fork archive contains an unsafe link")
                bundle.extract(member, target)

    @classmethod
    def _fork_child_goal_draft(cls, project_name: str, parent_content: str) -> str:
        """Return a child-owned Goal draft that satisfies the current review contract.

        Older approved projects can predate the structured Goal vocabulary.  A Fork
        must not fail merely because its authoritative parent Goal uses that legacy
        shape, nor may it silently approve the parent row as the child's identity.
        Preserve the approved parent content verbatim beneath an explicit child
        review envelope so the operator sees and approves the exact new revision.
        """
        try:
            cls.validate_goal_content(parent_content)
            return parent_content
        except ValueError:
            return (
                f"# {project_name} Project Goal\n\n"
                "## Child Fork Review Contract\n\n"
                "What and why: preserve the approved parent project purpose in an independently owned child fork.\n\n"
                "Target user and operator: the trusted ANIMUS PRIME operator and future authorized engineering sessions.\n\n"
                "Desired end state and outcome: an isolated child project that pursues the approved parent Goal without sharing mutable project state.\n\n"
                "Functional requirements: preserve the selected committed revision and independently bind authority, Goal, Progress, Notion, Hindsight, MCP, Brain, and activity resources.\n\n"
                "Constraints and non-functional requirements: maintain project isolation, provenance, secret safety, explicit approval, and reversible failure handling.\n\n"
                "Success and acceptance: the child remains durable, independently identifiable, and isolated from the parent after restart.\n\n"
                "Validation and evidence: verify distinct resource identities, exact Git provenance, browser usability, and restart recovery.\n\n"
                "Non-goals and out of scope: changing the approved parent Goal, copying parent memory, or granting unproven remote write capability.\n\n"
                "Failure and stop rules: stop safely on stale preflight, ambiguous external state, unavailable required integration, or incomplete isolation evidence.\n\n"
                "## Approved Parent Goal Context (verbatim)\n\n"
                f"{parent_content.rstrip()}\n"
            )

    def fork_preflight(
        self,
        source_project_id: str,
        source_revision: str,
        destination_node_id: str,
        parent_path: str,
        repository_name: str,
        project_name: str,
        remote_action: str,
        notion_parent_id: str,
        remap_remote_url: str | None = None,
        progress_items: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        if not repository_name or repository_name in {".", ".."} or Path(repository_name).name != repository_name:
            raise ValueError("repository name must be one directory name")
        if not project_name.strip():
            raise ValueError("child project name is required")
        if not notion_parent_id.strip():
            raise ValueError("approved Notion parent is required for the child Project Record")
        remote_action = remote_action.upper()
        if remote_action not in {"CLEAR", "RETAIN_READ_ONLY", "REMAP"}:
            raise ValueError("remote action must be CLEAR, RETAIN_READ_ONLY, or REMAP")
        if remote_action == "REMAP":
            if not remap_remote_url or any(character in remap_remote_url for character in "\r\n\0"):
                raise ValueError("REMAP requires one explicit safe remote URL")
        with connect(self.settings) as db:
            source = db.execute("SELECT p.*,r.canonical_path,r.node_id FROM prime_core.projects p JOIN prime_core.repositories r ON r.project_id=p.project_id WHERE p.project_id=%s", (source_project_id,)).fetchone()
            node = db.execute("SELECT node_id,name,status,allowed_roots FROM prime_core.nodes WHERE node_id=%s", (destination_node_id,)).fetchone()
            goal = db.execute("SELECT * FROM prime_core.goal_revisions WHERE project_id=%s AND status='APPROVED' ORDER BY revision_number DESC LIMIT 1", (source_project_id,)).fetchone()
            goal_items = db.execute("SELECT title,description,weight,required,acceptance_expectations FROM prime_core.goal_items WHERE project_id=%s AND goal_revision_id=%s ORDER BY title", (source_project_id, goal["goal_revision_id"] if goal else "")).fetchall()
        if not source:
            raise KeyError("source project not found")
        if not node:
            raise KeyError("destination node not found")
        if node["status"] in {"OFFLINE", "REVOKED"}:
            raise ValueError(f"Node is {node['status']}")
        if not goal:
            raise ValueError("fork requires an approved source Goal to present as a child draft")
        child_goal_content = self._fork_child_goal_draft(project_name.strip(), goal["content"])
        source_root = Path(source["canonical_path"]).resolve(strict=True)
        if self._tracked_worktree_changes(source_root):
            raise ValueError("fork requires a clean source working tree")
        resolved_revision = subprocess.run(["git", "-C", str(source_root), "rev-parse", f"{source_revision}^{{commit}}"], check=True, capture_output=True, text=True, timeout=10).stdout.strip()
        roots = node["allowed_roots"] if isinstance(node["allowed_roots"], list) else json.loads(node["allowed_roots"] or "[]")
        parent = Path(parent_path).expanduser().resolve(strict=True)
        if not parent.is_dir() or not self._within_allowed_root(parent, roots):
            raise PermissionError("fork destination is outside the enrolled Node allowed roots")
        target = parent / repository_name
        resolved_target = target.resolve(strict=False)
        if not self._within_allowed_root(resolved_target, roots):
            raise PermissionError("fork target resolves outside the enrolled Node allowed roots")
        idempotency_key = f"fork:{source_project_id}:{resolved_revision}:{target}"
        with connect(self.settings) as db:
            existing_workflow = db.execute("SELECT workflow_id FROM prime_core.workflows WHERE idempotency_key=%s", (idempotency_key,)).fetchone()
        if (target.exists() or target.is_symlink()) and not existing_workflow:
            raise FileExistsError("fork destination already exists")
        remote_names = subprocess.run(["git", "-C", str(source_root), "remote"], check=True, capture_output=True, text=True, timeout=10).stdout.split()
        remotes = []
        for name in remote_names:
            fetch_url = subprocess.run(["git", "-C", str(source_root), "remote", "get-url", name], check=True, capture_output=True, text=True, timeout=10).stdout.strip()
            push_url = subprocess.run(["git", "-C", str(source_root), "remote", "get-url", "--push", name], check=True, capture_output=True, text=True, timeout=10).stdout.strip()
            remotes.append({"name": name, "fetch_url": self._display_remote_url(fetch_url), "push_url": self._display_remote_url(push_url), "write_capability": "UNPROVEN"})
        proposed_items = list(progress_items or [])
        if not proposed_items:
            for item in goal_items:
                expectations = item["acceptance_expectations"]
                if isinstance(expectations, str):
                    expectations = json.loads(expectations)
                proposed_items.append({"title": item["title"], "description": item["description"], "weight": float(item["weight"]), "required": bool(item["required"]), "acceptance_expectations": expectations or []})
        if not proposed_items:
            raise ValueError("fork requires operator-reviewed child Progress baseline items")
        weights = sum(float(item.get("weight", 0)) for item in proposed_items)
        if any(float(item.get("weight", 0)) <= 0 for item in proposed_items) or abs(weights - 1.0) > 1e-6:
            raise ValueError("child Progress baseline items require positive weights summing to 1.0")
        fingerprint_payload = {
            "source_project_id": source_project_id,
            "source_revision": resolved_revision,
            "destination_node_id": destination_node_id,
            "target": str(target),
            "project_name": project_name.strip(),
            "remote_action": remote_action,
            "remap_remote_url": remap_remote_url if remote_action == "REMAP" else None,
            "notion_parent_id": notion_parent_id,
            "goal_revision_id": goal["goal_revision_id"],
            "goal_content_hash": goal["content_hash"],
            "child_goal_content_hash": hashlib.sha256(child_goal_content.encode()).hexdigest(),
            "progress_items": proposed_items,
            "remotes": remotes,
        }
        preflight_fingerprint = hashlib.sha256(json.dumps(fingerprint_payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        return {
            **fingerprint_payload,
            "preflight_fingerprint": preflight_fingerprint,
            "source_project_name": source["name"],
            "source_goal_content": child_goal_content,
            "source_goal_status": goal["status"],
            "destination_path": str(target),
            "destination_exists": target.exists() or target.is_symlink(),
            "existing_workflow_id": existing_workflow["workflow_id"] if existing_workflow else None,
            "memory_copy_status": "NONE",
            "notion_copy_status": "NONE_NEW_CHILD_RECORD_REQUIRED",
            "remote_policy": "WRITE_CAPABILITY_UNPROVEN_DEFAULT_CLEAR" if remote_action == "CLEAR" else remote_action,
            "confirmation_required": True,
        }

    def fork_project(
        self,
        source_project_id: str,
        source_revision: str,
        destination_node_id: str,
        parent_path: str,
        repository_name: str,
        project_name: str,
        remote_action: str,
        notion_parent_id: str,
        preflight_fingerprint: str,
        progress_items: list[dict[str, Any]],
        approve_child_goal: bool,
        approve_progress_baseline: bool,
        notion_lifecycle: Any,
        remap_remote_url: str | None = None,
        image_url: str | None = None,
        confirm: bool = False,
    ) -> dict[str, Any]:
        if not confirm:
            raise ValueError("operator confirmation is required before fork")
        if not approve_child_goal:
            raise ValueError("operator approval of the child Goal draft is required")
        if not approve_progress_baseline:
            raise ValueError("operator approval of the child Progress baseline is required")
        preflight = self.fork_preflight(source_project_id, source_revision, destination_node_id, parent_path, repository_name, project_name, remote_action, notion_parent_id, remap_remote_url, progress_items)
        if not preflight_fingerprint or not constant_time_equal(preflight_fingerprint, preflight["preflight_fingerprint"]):
            raise ValueError("fork preflight is stale or does not match the confirmed target")
        source_revision = preflight["source_revision"]
        remote_action = preflight["remote_action"]
        progress_items = preflight["progress_items"]
        with connect(self.settings) as db:
            source = db.execute("SELECT p.*,r.canonical_path,r.node_id FROM prime_core.projects p JOIN prime_core.repositories r ON r.project_id=p.project_id WHERE p.project_id=%s", (source_project_id,)).fetchone()
            node = db.execute("SELECT node_id,name,status,allowed_roots FROM prime_core.nodes WHERE node_id=%s", (destination_node_id,)).fetchone()
            goal = db.execute("SELECT * FROM prime_core.goal_revisions WHERE project_id=%s AND status='APPROVED' ORDER BY revision_number DESC LIMIT 1", (source_project_id,)).fetchone()
        if not source:
            raise KeyError("source project not found")
        if not node:
            raise KeyError("destination node not found")
        if node["status"] in {"OFFLINE", "REVOKED"}:
            raise ValueError(f"Node is {node['status']}")
        source_root = Path(source["canonical_path"]).resolve(strict=True)
        if self._tracked_worktree_changes(source_root):
            raise ValueError("fork requires a clean source working tree")
        subprocess.run(["git", "-C", str(source_root), "cat-file", "-e", f"{source_revision}^{{commit}}"], check=True, capture_output=True, text=True, timeout=10)
        roots = node["allowed_roots"] if isinstance(node["allowed_roots"], list) else json.loads(node["allowed_roots"] or "[]")
        parent = Path(parent_path).expanduser().resolve(strict=True)
        if not parent.is_dir() or not self._within_allowed_root(parent, roots):
            raise PermissionError("fork destination is outside the enrolled Node allowed roots")
        target = parent / repository_name
        resolved_target = target.resolve(strict=False)
        if not self._within_allowed_root(resolved_target, roots):
            raise PermissionError("fork target resolves outside the enrolled Node allowed roots")
        idempotency_key = f"fork:{source_project_id}:{source_revision}:{target}"
        with connect(self.settings) as db:
            existing_workflow = db.execute("SELECT * FROM prime_core.workflows WHERE idempotency_key=%s", (idempotency_key,)).fetchone()
            existing_project = db.execute("SELECT * FROM prime_core.projects WHERE project_id=%s", (existing_workflow["project_id"],)).fetchone() if existing_workflow and existing_workflow["project_id"] else None
        if (target.exists() or target.is_symlink()) and not existing_workflow:
            raise FileExistsError("fork destination already exists")
        project = dict(existing_project) if existing_project else self.create_project(project_name.strip(), source.get("description", ""), image_url)
        workflow = self.start_or_get_workflow("FORK_PROJECT", idempotency_key, project["project_id"], [
            {"step_key": "PROJECT_RESERVED", "replay_policy": "PURE_OR_DB_TRANSACTION"},
            {"step_key": "TARGET_EXPECTED", "replay_policy": "PURE_OR_DB_TRANSACTION"},
            {"step_key": "REPOSITORY_CLONED", "replay_policy": "NON_IDEMPOTENT_EXTERNAL"},
            {"step_key": "REVISION_CHECKED_OUT", "replay_policy": "IDEMPOTENT_EXTERNAL"},
            {"step_key": "REPOSITORY_SANITIZED", "replay_policy": "IDEMPOTENT_EXTERNAL"},
            {"step_key": "AUTHORITY_PROVISIONED", "replay_policy": "NON_IDEMPOTENT_EXTERNAL"},
            {"step_key": "REPOSITORY_BOUND", "replay_policy": "PURE_OR_DB_TRANSACTION"},
            {"step_key": "GOAL_DRAFTED", "replay_policy": "PURE_OR_DB_TRANSACTION"},
            {"step_key": "GOAL_APPROVED", "replay_policy": "IDEMPOTENT_EXTERNAL"},
            {"step_key": "PROGRESS_BASELINE_CREATED", "replay_policy": "PURE_OR_DB_TRANSACTION"},
            {"step_key": "INDEXED", "replay_policy": "PURE_OR_DB_TRANSACTION"},
            {"step_key": "NOTION_PROJECT_RECORD_BOUND", "replay_policy": "IDEMPOTENT_EXTERNAL"},
            {"step_key": "MCP_SCOPE_ISSUED", "replay_policy": "NON_IDEMPOTENT_EXTERNAL"},
            {"step_key": "HINDSIGHT_BOUND", "replay_policy": "IDEMPOTENT_EXTERNAL"},
            {"step_key": "PROJECT_BRAIN_INITIALIZED", "replay_policy": "PURE_OR_DB_TRANSACTION"},
            {"step_key": "EVENT_STREAM_INITIALIZED", "replay_policy": "PURE_OR_DB_TRANSACTION"},
            {"step_key": "FINALIZED", "replay_policy": "PURE_OR_DB_TRANSACTION"},
        ])
        current_step = "PROJECT_RESERVED"
        try:
            started = self.begin_step(workflow["workflow_id"], current_step)
            if started["decision"] != "SKIP_COMPLETED":
                self.complete_step(workflow["workflow_id"], current_step, {"project_id": project["project_id"]})

            current_step = "TARGET_EXPECTED"
            started = self.begin_step(workflow["workflow_id"], current_step)
            if started["decision"] != "SKIP_COMPLETED":
                self.record_workflow_resource(workflow["workflow_id"], "REPOSITORY", "child-repository", str(target), {"source_project_id": source_project_id, "source_revision": source_revision}, "EXPECTED")
                self.complete_step(workflow["workflow_id"], current_step)

            current_step = "REPOSITORY_CLONED"
            started = self.begin_step(workflow["workflow_id"], current_step)
            adopted_clone = False
            if started["decision"] == "REPAIR_REQUIRED":
                if target.is_dir():
                    inspected_commit = subprocess.run(["git", "-C", str(target), "rev-parse", "HEAD"], check=False, capture_output=True, text=True, timeout=10)
                    if inspected_commit.returncode != 0:
                        self.record_workflow_resource(workflow["workflow_id"], "REPOSITORY", "child-repository", str(target), {"reason": "TARGET_EXISTS_BUT_IS_NOT_A_RECONCILABLE_GIT_REPOSITORY"}, "RECONCILIATION_REQUIRED")
                        raise ValueError("fork target requires operator reconciliation")
                    adopted_clone = True
                    self.mark_workflow_repaired(workflow["workflow_id"], current_step, {"reconciliation": "EXISTING_CLONE_DISCOVERED", "observed_head": inspected_commit.stdout.strip()})
                elif not target.exists():
                    self.mark_workflow_repaired(workflow["workflow_id"], current_step, {"reconciliation": "TARGET_ABSENT_SAFE_TO_RETRY"})
                started = self.begin_step(workflow["workflow_id"], current_step)
            if started["decision"] != "SKIP_COMPLETED":
                qualification_interrupt("FORK_PROJECT", current_step, "BEFORE_EXTERNAL_CALL")
                if not adopted_clone:
                    subprocess.run(["git", "clone", "--no-hardlinks", str(source_root), str(target)], check=True, capture_output=True, text=True, timeout=60)
                qualification_interrupt("FORK_PROJECT", current_step, "EXTERNAL_SUCCESS_BEFORE_PERSIST")
                self.record_workflow_resource(workflow["workflow_id"], "REPOSITORY", "child-repository", str(target), {"source_project_id": source_project_id, "source_revision": source_revision}, "CREATED")
                self.complete_step(workflow["workflow_id"], current_step, side_effect_state={"path": str(target), "reconciled": adopted_clone})

            current_step = "REVISION_CHECKED_OUT"
            started = self.begin_step(workflow["workflow_id"], current_step)
            if started["decision"] != "SKIP_COMPLETED":
                subprocess.run(["git", "-C", str(target), "checkout", "--detach", source_revision], check=True, capture_output=True, text=True, timeout=30)
                self.complete_step(workflow["workflow_id"], current_step, side_effect_state={"revision": source_revision})

            current_step = "REPOSITORY_SANITIZED"
            started = self.begin_step(workflow["workflow_id"], current_step)
            if started["decision"] != "SKIP_COMPLETED":
                remotes = subprocess.run(["git", "-C", str(target), "remote"], check=True, capture_output=True, text=True, timeout=10).stdout.split()
                for remote in remotes:
                    subprocess.run(["git", "-C", str(target), "remote", "remove", remote], check=True, capture_output=True, text=True, timeout=10)
                if remote_action == "RETAIN_READ_ONLY":
                    for remote in preflight["remotes"]:
                        retained_fetch_url = subprocess.run(["git", "-C", str(source_root), "remote", "get-url", remote["name"]], check=True, capture_output=True, text=True, timeout=10).stdout.strip()
                        subprocess.run(["git", "-C", str(target), "remote", "add", remote["name"], retained_fetch_url], check=True, capture_output=True, text=True, timeout=10)
                        subprocess.run(["git", "-C", str(target), "remote", "set-url", "--push", remote["name"], "disabled-by-prime://write-capability-unproven"], check=True, capture_output=True, text=True, timeout=10)
                elif remote_action == "REMAP":
                    subprocess.run(["git", "-C", str(target), "remote", "add", "origin", str(remap_remote_url)], check=True, capture_output=True, text=True, timeout=10)
                self.complete_step(workflow["workflow_id"], current_step, {"remote_status": remote_action, "source_remotes_reviewed": len(preflight["remotes"]), "write_capability": "DISABLED" if remote_action == "RETAIN_READ_ONLY" else "OPERATOR_EXPLICIT" if remote_action == "REMAP" else "CLEARED"})

            current_step = "AUTHORITY_PROVISIONED"
            started = self.begin_step(workflow["workflow_id"], current_step)
            if started["decision"] == "REPAIR_REQUIRED":
                present = all((target / relative).is_file() for relative in REQUIRED_AUTHORITY_FILES)
                if not present:
                    self.record_workflow_resource(workflow["workflow_id"], "AUTHORITY", "child-authority", str(target), {"reason": "PARTIAL_AUTHORITY_REQUIRES_REVIEW"}, "RECONCILIATION_REQUIRED")
                    raise ValueError("child authority requires operator reconciliation")
                self.mark_workflow_repaired(workflow["workflow_id"], current_step, {"reconciliation": "AUTHORITY_FILES_DISCOVERED"})
                started = self.begin_step(workflow["workflow_id"], current_step)
            if started["decision"] != "SKIP_COMPLETED":
                for relative in REQUIRED_AUTHORITY_FILES:
                    candidate = target / relative
                    if candidate.is_file() or candidate.is_symlink():
                        candidate.unlink()
                provision_authority(self._authority_template_root(), target)
                qualification_interrupt("FORK_PROJECT", current_step, "EXTERNAL_SUCCESS_BEFORE_PERSIST")
                self.record_workflow_resource(workflow["workflow_id"], "AUTHORITY", "child-authority", str(target), {"template": "authority-template/v1", "relationship": "CHILD_SPECIFIC"}, "CREATED")
                self.complete_step(workflow["workflow_id"], current_step)

            current_step = "REPOSITORY_BOUND"
            started = self.begin_step(workflow["workflow_id"], current_step)
            with connect(self.settings) as db:
                existing_binding = db.execute("SELECT r.* FROM prime_core.repositories r WHERE r.project_id=%s", (project["project_id"],)).fetchone()
            if started["decision"] == "SKIP_COMPLETED" or existing_binding:
                binding = dict(existing_binding)
                if started["decision"] != "SKIP_COMPLETED":
                    self.complete_step(workflow["workflow_id"], current_step, {"repository_id": binding["repository_id"], "reconciled": True})
            else:
                inspection = self.inspect_repository_for_onboarding(project["project_id"], destination_node_id, str(target))
                binding = self.bind_verified_repository(inspection, confirm=True)
                self.complete_step(workflow["workflow_id"], current_step, {"repository_id": binding.get("repository_id")})

            current_step = "GOAL_DRAFTED"
            started = self.begin_step(workflow["workflow_id"], current_step)
            if started["decision"] != "SKIP_COMPLETED":
                if goal:
                    with connect(self.settings) as db:
                        draft = db.execute("SELECT * FROM prime_core.goal_revisions WHERE project_id=%s AND status IN ('DRAFT','APPROVED') ORDER BY revision_number LIMIT 1", (project["project_id"],)).fetchone()
                    if not draft:
                        draft = self.create_goal_revision(project["project_id"], preflight["source_goal_content"], approve=False)
                    self.complete_step(workflow["workflow_id"], current_step, {"goal_revision_id": draft["goal_revision_id"], "source_goal_revision_id": goal["goal_revision_id"], "relationship": "CHILD_DRAFT_FROM_PARENT_CONTENT"})
                else:
                    self.complete_step(workflow["workflow_id"], current_step, {"goal": "ABSENT"})

            with connect(self.settings) as db:
                child_goal = db.execute("SELECT * FROM prime_core.goal_revisions WHERE project_id=%s ORDER BY revision_number LIMIT 1", (project["project_id"],)).fetchone()

            current_step = "GOAL_APPROVED"
            started = self.begin_step(workflow["workflow_id"], current_step)
            if started["decision"] != "SKIP_COMPLETED":
                child_goal = self.approve_goal_revision(project["project_id"], child_goal["goal_revision_id"])
                self.complete_step(workflow["workflow_id"], current_step, {"goal_revision_id": child_goal["goal_revision_id"], "status": "APPROVED", "operator_approval": True})

            current_step = "PROGRESS_BASELINE_CREATED"
            started = self.begin_step(workflow["workflow_id"], current_step)
            with connect(self.settings) as db:
                baseline = db.execute("SELECT * FROM prime_core.progress_baseline_reviews WHERE project_id=%s AND goal_revision_id=%s AND status='APPROVED' ORDER BY created_at LIMIT 1", (project["project_id"], child_goal["goal_revision_id"])).fetchone()
            if started["decision"] != "SKIP_COMPLETED":
                if not baseline:
                    progress_service = __import__("src.prime_core.progress_service", fromlist=["ProgressService"]).ProgressService(self.settings)
                    proposed = progress_service.propose_baseline(project["project_id"], child_goal["goal_revision_id"], progress_items)
                    progress_service.approve_baseline(proposed["review_id"])
                    with connect(self.settings) as db:
                        baseline = db.execute("SELECT * FROM prime_core.progress_baseline_reviews WHERE review_id=%s", (proposed["review_id"],)).fetchone()
                self.complete_step(workflow["workflow_id"], current_step, {"review_id": baseline["review_id"], "goal_revision_id": child_goal["goal_revision_id"], "status": "APPROVED", "operator_approval": True, "source_relationship": "COPIED_AS_REVIEWED_DRAFT_NOT_SHARED"})

            current_step = "INDEXED"
            started = self.begin_step(workflow["workflow_id"], current_step)
            if started["decision"] == "SKIP_COMPLETED":
                with connect(self.settings) as db:
                    revision = db.execute("SELECT source_revision FROM prime_core.source_snapshots WHERE project_id=%s AND source_class='REPOSITORY' AND freshness_state='CURRENT' ORDER BY observed_at DESC LIMIT 1", (project["project_id"],)).fetchone()
                indexed = {"source_revision": revision["source_revision"] if revision else source_revision, "reconciled": True}
            else:
                indexed = __import__("src.prime_core.indexer", fromlist=["RepositoryIndexer"]).RepositoryIndexer(self).build(project["project_id"])
                self.complete_step(workflow["workflow_id"], current_step, {"source_revision": indexed["source_revision"]})

            current_step = "NOTION_PROJECT_RECORD_BOUND"
            started = self.begin_step(workflow["workflow_id"], current_step)
            notion_result = None
            if started["decision"] != "SKIP_COMPLETED":
                notion_lifecycle.configure(project["project_id"], "env/myassistant/notion-readonly")
                notion_result = notion_lifecycle.create_project_record(project["project_id"], notion_parent_id, project["name"], idempotency_key=f"fork-project-record:{workflow['workflow_id']}")
                if notion_result.get("status") != "BOUND":
                    raise ValueError(f"child Notion Project Record is {notion_result.get('status', 'UNAVAILABLE')}")
                self.record_workflow_resource(workflow["workflow_id"], "NOTION_PAGE", "child-project-record", notion_result["page_id"], {"project_id": project["project_id"], "parent_id": notion_parent_id, "ownership": "CHILD_MANAGED_REGION"}, "CREATED")
                self.complete_step(workflow["workflow_id"], current_step, {"page_id": notion_result["page_id"], "status": "BOUND"})
            else:
                notion_state = notion_lifecycle.projects.get(project["project_id"])
                notion_result = {"status": notion_state.status if notion_state else "UNAVAILABLE", "page_id": notion_state.page_id if notion_state else None, "idempotent": True}

            current_step = "MCP_SCOPE_ISSUED"
            started = self.begin_step(workflow["workflow_id"], current_step)
            grant = None
            if started["decision"] == "REPAIR_REQUIRED":
                with connect(self.settings) as db:
                    existing_grant = db.execute("SELECT grant_id,client_id,project_id,expires_at FROM prime_core.mcp_grants WHERE project_id=%s AND client_id='fork-initial-coder' AND revoked_at IS NULL ORDER BY created_at DESC LIMIT 1", (project["project_id"],)).fetchone()
                if existing_grant:
                    self.record_workflow_resource(workflow["workflow_id"], "MCP_GRANT", "fork-initial-coder", existing_grant["grant_id"], {"reason": "ONE_TIME_SECRET_RESPONSE_WAS_NOT_PERSISTED; ROTATION_REQUIRED"}, "RECONCILIATION_REQUIRED")
                raise ValueError("fork MCP credential requires operator rotation after interrupted issuance")
            if started["decision"] != "SKIP_COMPLETED":
                grant = __import__("src.prime_core.mcp_service", fromlist=["MCPService"]).MCPService(self.settings).issue_grant(project["project_id"], "fork-initial-coder")
                qualification_interrupt("FORK_PROJECT", current_step, "EXTERNAL_SUCCESS_BEFORE_PERSIST")
                self.record_workflow_resource(workflow["workflow_id"], "MCP_GRANT", "fork-initial-coder", grant["grant_id"], {"secret": "ONE_TIME_ISSUE_ONLY"}, "CREATED")
                self.complete_step(workflow["workflow_id"], current_step, {"grant_id": grant["grant_id"]})

            current_step = "HINDSIGHT_BOUND"
            started = self.begin_step(workflow["workflow_id"], current_step)
            if started["decision"] != "SKIP_COMPLETED":
                hindsight = __import__("src.prime_core.memory_service", fromlist=["MemoryService"]).MemoryService(self.settings).ensure_bank(project["project_id"], parent_workflow_id=workflow["workflow_id"])
                if hindsight["status"] != "CURRENT":
                    raise ValueError("child Hindsight bank is unavailable")
                self.complete_step(workflow["workflow_id"], current_step, {"bank_id": hindsight["bank_id"]})

            current_step = "PROJECT_BRAIN_INITIALIZED"
            started = self.begin_step(workflow["workflow_id"], current_step)
            if started["decision"] != "SKIP_COMPLETED":
                brain = __import__("src.prime_core.brain_service", fromlist=["BrainService"]).BrainService(self.settings).build(project["project_id"], indexed["source_revision"])
                if brain.get("availability") == "UNAVAILABLE":
                    raise ValueError("child Project Brain initialization is unavailable")
                self.complete_step(workflow["workflow_id"], current_step, {"source_revision": brain["source_revision"], "nodes": len(brain.get("nodes", [])), "classification": "DERIVED_NON_AUTHORITATIVE"})

            current_step = "EVENT_STREAM_INITIALIZED"
            started = self.begin_step(workflow["workflow_id"], current_step)
            if started["decision"] != "SKIP_COMPLETED":
                event = self.emit_event("PROJECT_FORKED", {"source_project_id": source_project_id, "source_revision": source_revision, "repository_id": binding["repository_id"], "memory_copy_status": "NONE", "notion_page_id": notion_result["page_id"], "progress_baseline_id": baseline["review_id"]}, project_id=project["project_id"], source_revision=indexed["source_revision"], dedupe_key=f"fork-finalized:{workflow['workflow_id']}")
                self.complete_step(workflow["workflow_id"], current_step, {"event_id": event["event_id"], "project_sequence": event.get("project_sequence")})

            current_step = "FINALIZED"
            started = self.begin_step(workflow["workflow_id"], current_step)
            if started["decision"] != "SKIP_COMPLETED":
                with transaction(self.settings) as db:
                    existing_fork = db.execute("SELECT * FROM prime_core.project_forks WHERE new_project_id=%s", (project["project_id"],)).fetchone()
                    if existing_fork:
                        fork = existing_fork
                    else:
                        fork = db.execute("INSERT INTO prime_core.project_forks(fork_id,source_project_id,new_project_id,source_revision,memory_copy_status,destination_node_id,destination_repository_id,destination_revision,provenance,created_at) VALUES (%s,%s,%s,%s,'NONE',%s,%s,%s,%s,%s) RETURNING *", (_id("fork"), source_project_id, project["project_id"], source_revision, destination_node_id, binding["repository_id"], indexed["source_revision"], json.dumps({"source": "git clone", "source_revision": source_revision, "memory": "NOT_COPIED", "notion": "NEW_CHILD_PROJECT_RECORD", "progress": "NEW_CHILD_APPROVED_BASELINE", "goal": "CHILD_APPROVED_REVISION_FROM_REVIEWED_PARENT_DRAFT", "hindsight": "INDEPENDENT_BANK", "brain": "DERIVED_CHILD_PROJECTION"}), now())).fetchone()
                self.complete_step(workflow["workflow_id"], current_step, {"fork_id": fork["fork_id"]})
            else:
                with connect(self.settings) as db:
                    fork = db.execute("SELECT * FROM prime_core.project_forks WHERE new_project_id=%s", (project["project_id"],)).fetchone()
            self.complete_workflow(workflow["workflow_id"], current_step)
            destination_revision = indexed["source_revision"]
            return {"workflow_id": workflow["workflow_id"], "fork": dict(fork), "project": project, "binding": binding, "indexed": indexed, "mcp_grant": grant, "memory_copy_status": "NONE", "notion_status": "NEW_CHILD_PROJECT_RECORD", "notion": notion_result, "hindsight_status": "INDEPENDENT_BANK", "goal_status": "APPROVED_CHILD_REVISION", "goal_revision_id": child_goal["goal_revision_id"], "progress_baseline_id": baseline["review_id"], "progress_status": "APPROVED_CHILD_BASELINE", "brain_status": "DERIVED_CHILD_PROJECTION", "event_status": "CHILD_SCOPED", "authority_provenance": "CURRENT_TEMPLATE_NOT_PARENT_AUTHORITY", "remote_status": remote_action, "destination_revision": destination_revision}
        except QualificationInterruption:
            with transaction(self.settings) as db:
                db.execute("UPDATE prime_core.projects SET lifecycle_state='PROVISIONING',work_condition='REVIEW_REQUIRED',onboarding_state='REPAIR_REQUIRED',updated_at=%s WHERE project_id=%s", (now(), project["project_id"]))
            raise
        except Exception as exc:
            with transaction(self.settings) as db:
                step = db.execute("SELECT status,replay_policy FROM prime_core.workflow_steps WHERE workflow_id=%s AND step_key=%s", (workflow["workflow_id"], current_step)).fetchone()
                ambiguous = bool(step and step["status"] == "RUNNING" and step["replay_policy"] == "NON_IDEMPOTENT_EXTERNAL")
                db.execute("UPDATE prime_core.workflow_steps SET status=%s,last_error=%s WHERE workflow_id=%s AND step_key=%s AND status='RUNNING'", ("REPAIR_REQUIRED" if ambiguous else "FAILED_RETRYABLE", type(exc).__name__, workflow["workflow_id"], current_step))
                db.execute("UPDATE prime_core.workflows SET status=%s,current_step=%s,last_error=%s,updated_at=%s WHERE workflow_id=%s", ("REPAIR_REQUIRED" if ambiguous else "RUNNING", current_step, type(exc).__name__, now(), workflow["workflow_id"]))
                db.execute("UPDATE prime_core.projects SET lifecycle_state='PROVISIONING',work_condition='REVIEW_REQUIRED',onboarding_state='REPAIR_REQUIRED',updated_at=%s WHERE project_id=%s", (now(), project["project_id"]))
            raise

    def bind_repository(self, project_id: str, node_id: str, identity_fingerprint: str, canonical_path: str, is_bare: bool = False) -> dict[str, Any]:
        timestamp = now()
        with transaction(self.settings) as db:
            if is_bare:
                raise ValueError("bare repositories are not supported")
            if not db.execute("SELECT 1 FROM prime_core.projects WHERE project_id=%s", (project_id,)).fetchone():
                raise KeyError("project not found")
            if not db.execute("SELECT 1 FROM prime_core.nodes WHERE node_id=%s", (node_id,)).fetchone():
                raise KeyError("node not found")
            existing_binding = db.execute(
                "SELECT repository_id FROM prime_core.project_bindings WHERE project_id=%s",
                (project_id,),
            ).fetchone()
            if existing_binding:
                raise ValueError("project already has a primary repository binding")
            duplicate = db.execute(
                "SELECT project_id FROM prime_core.repositories WHERE identity_fingerprint=%s",
                (identity_fingerprint,),
            ).fetchone()
            if duplicate:
                raise ValueError("repository is already bound to another project")
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

    @staticmethod
    def validate_goal_content(content: str) -> None:
        normalized = " ".join(content.lower().split())
        required = {
            "purpose": ("what", "why"), "operator": ("target user", "operator"),
            "end state": ("desired end state", "end state", "outcome"),
            "requirements": ("requirement", "functional"), "constraints": ("constraint", "non-functional"),
            "success": ("success", "acceptance"), "validation": ("validation", "evidence"),
            "non-goals": ("non-goal", "out of scope"), "failure rules": ("failure", "stop"),
        }
        missing = [label for label, markers in required.items() if not any(marker in normalized for marker in markers)]
        if len(content.strip()) < 80 or missing:
            raise ValueError("goal proposal is incomplete; missing: " + ", ".join(missing))

    def create_goal_revision(self, project_id: str, content: str, approve: bool = False, new_revision: bool = False) -> dict[str, Any]:
        timestamp = now()
        with connect(self.settings) as db:
            approved = db.execute("SELECT 1 FROM prime_core.goal_revisions WHERE project_id=%s AND status='APPROVED' LIMIT 1", (project_id,)).fetchone()
            binding = db.execute("SELECT canonical_path FROM prime_core.repositories WHERE project_id=%s", (project_id,)).fetchone()
        if approve and approved and not new_revision:
            raise ValueError("approved GoalRevision is protected; explicit new-revision intent is required")
        self.validate_goal_content(content)
        if approve and binding:
            canonical_path = Path(binding["canonical_path"])
            if canonical_path.exists():
                goal_path = canonical_path.resolve(strict=True) / ".agent" / "PROJECT_GOAL.md"
                if goal_path.parent.is_dir():
                    goal_path.write_text(content, encoding="utf-8")
        with transaction(self.settings) as db:
            last = db.execute("SELECT COALESCE(MAX(revision_number),0) AS number FROM prime_core.goal_revisions WHERE project_id=%s", (project_id,)).fetchone()["number"]
            status = "APPROVED" if approve else "DRAFT"
            row = db.execute(
                "INSERT INTO prime_core.goal_revisions(goal_revision_id,project_id,revision_number,content,content_hash,status,approved_by,created_at,approved_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING *",
                (_id("goal"), project_id, last + 1, content, hashlib.sha256(content.encode()).hexdigest(), status, "operator" if approve else None, timestamp, timestamp if approve else None),
            ).fetchone()
            if approve:
                db.execute("UPDATE prime_core.goal_revisions SET status='SUPERSEDED' WHERE project_id=%s AND goal_revision_id<>%s AND status='APPROVED'", (project_id, row["goal_revision_id"]))
                db.execute("UPDATE prime_core.projects SET work_condition='NORMAL', onboarding_step='INDEX', onboarding_state='IN_PROGRESS', updated_at=%s WHERE project_id=%s", (timestamp, project_id))
            record_historical_snapshot(db, project_id, "GOAL", row["goal_revision_id"], row["content_hash"], {"goal_revision_id": row["goal_revision_id"], "revision_number": row["revision_number"], "content": content, "status": status}, row["created_at"], row["content_hash"])
            self._audit(db, "operator", "operator", "goal.revision_created", project_id=project_id, target_id=row["goal_revision_id"])
            return dict(row)

    def approve_goal_revision(self, project_id: str, goal_revision_id: str) -> dict[str, Any]:
        timestamp = now()
        with connect(self.settings) as db:
            candidate = db.execute("SELECT * FROM prime_core.goal_revisions WHERE project_id=%s AND goal_revision_id=%s", (project_id, goal_revision_id)).fetchone()
            binding = db.execute("SELECT r.canonical_path,n.* FROM prime_core.repositories r JOIN prime_core.nodes n ON n.node_id=r.node_id WHERE r.project_id=%s", (project_id,)).fetchone()
        if not candidate:
            raise ValueError("GoalRevision not found")
        if candidate["status"] not in {"DRAFT", "APPROVED"}:
            raise ValueError("GoalRevision is not approvable")
        self.validate_goal_content(candidate["content"])
        workflow = self.start_or_get_workflow("APPROVE_PROJECT_GOAL", f"goal-approval:{project_id}:{goal_revision_id}", project_id, [
            {"step_key": "GOAL_FILE_EXPECTED", "replay_policy": "PURE_OR_DB_TRANSACTION"},
            {"step_key": "GOAL_FILE_WRITTEN", "replay_policy": "IDEMPOTENT_EXTERNAL"},
            {"step_key": "GOAL_APPROVED", "replay_policy": "PURE_OR_DB_TRANSACTION"},
        ])
        step = self.begin_step(workflow["workflow_id"], "GOAL_FILE_EXPECTED")
        if step["decision"] != "SKIP_COMPLETED":
            if binding:
                self.record_workflow_resource(workflow["workflow_id"], "PROJECT_GOAL_FILE", "PROJECT_GOAL.md", str(Path(binding["canonical_path"]) / "PROJECT_GOAL.md"), {"content_hash": candidate["content_hash"], "node_id": binding["node_id"]}, "EXPECTED")
            self.complete_step(workflow["workflow_id"], "GOAL_FILE_EXPECTED")
        step = self.begin_step(workflow["workflow_id"], "GOAL_FILE_WRITTEN")
        if step["decision"] != "SKIP_COMPLETED":
            if binding:
                qualification_interrupt("APPROVE_PROJECT_GOAL", "GOAL_FILE_WRITTEN", "BEFORE_EXTERNAL_CALL")
                written = self._node_client(dict(binding)).write_project_goal(binding["canonical_path"], candidate["content"], candidate["content_hash"])
                qualification_interrupt("APPROVE_PROJECT_GOAL", "GOAL_FILE_WRITTEN", "EXTERNAL_SUCCESS_BEFORE_PERSIST")
                self.record_workflow_resource(workflow["workflow_id"], "PROJECT_GOAL_FILE", "PROJECT_GOAL.md", str(Path(binding["canonical_path"]) / "PROJECT_GOAL.md"), {"content_hash": candidate["content_hash"], "node_id": binding["node_id"], "write_result": written.get("status", "CURRENT")}, "CREATED")
            self.complete_step(workflow["workflow_id"], "GOAL_FILE_WRITTEN", side_effect_state={"content_hash": candidate["content_hash"], "repository_bound": bool(binding)})
        step = self.begin_step(workflow["workflow_id"], "GOAL_APPROVED")
        if step["decision"] != "SKIP_COMPLETED":
            with transaction(self.settings) as db:
                row = db.execute("SELECT * FROM prime_core.goal_revisions WHERE project_id=%s AND goal_revision_id=%s FOR UPDATE", (project_id, goal_revision_id)).fetchone()
                if row["status"] == "DRAFT":
                    self.validate_goal_content(row["content"])
                    db.execute("UPDATE prime_core.goal_revisions SET status='SUPERSEDED' WHERE project_id=%s AND status='APPROVED'", (project_id,))
                    approved = db.execute("UPDATE prime_core.goal_revisions SET status='APPROVED',approved_by='operator',approved_at=%s WHERE goal_revision_id=%s RETURNING *", (timestamp, goal_revision_id)).fetchone()
                    db.execute("UPDATE prime_core.projects SET work_condition='NORMAL',onboarding_step='INDEX',onboarding_state='IN_PROGRESS',updated_at=%s WHERE project_id=%s", (timestamp, project_id))
                    record_historical_snapshot(db, project_id, "GOAL", goal_revision_id, row["content_hash"], {"goal_revision_id": goal_revision_id, "revision_number": row["revision_number"], "content": row["content"], "status": "APPROVED"}, row["created_at"], row["content_hash"])
                    self._audit(db, "operator", "operator", "goal.revision_approved", project_id=project_id, target_id=goal_revision_id)
                else:
                    approved = row
            self.complete_step(workflow["workflow_id"], "GOAL_APPROVED", {"goal_revision_id": goal_revision_id})
        else:
            with connect(self.settings) as db:
                approved = db.execute("SELECT * FROM prime_core.goal_revisions WHERE project_id=%s AND goal_revision_id=%s", (project_id, goal_revision_id)).fetchone()
        self.complete_workflow(workflow["workflow_id"], "GOAL_APPROVED")
        return {**dict(approved), "workflow_id": workflow["workflow_id"]}

    def record_authority_revision(self, project_id: str, source_path: str, source_hash: str, validation_status: str, metadata: dict[str, Any] | None = None, content_snapshot: str | None = None, canonical_commit: str | None = None) -> dict[str, Any]:
        with transaction(self.settings) as db:
            row = db.execute(
                "INSERT INTO prime_core.authority_revisions(authority_revision_id,project_id,source_path,source_hash,contract_version,validation_status,observed_at,metadata,content_snapshot,canonical_commit) VALUES (%s,%s,%s,%s,'authority-file-contract-v1',%s,now(),%s,%s,%s) RETURNING *",
                (_id("authority"), project_id, source_path, source_hash, validation_status, json.dumps(metadata or {}), content_snapshot, canonical_commit),
            ).fetchone()
            record_historical_snapshot(db, project_id, "AUTHORITY", row["authority_revision_id"], canonical_commit or source_hash, {"authority_revision_id": row["authority_revision_id"], "source_path": source_path, "source_hash": source_hash, "validation_status": validation_status, "content_snapshot": content_snapshot}, row["observed_at"], source_hash)
            self._audit(db, "system", "authority-observer", "authority.observed", project_id=project_id, target_id=row["authority_revision_id"])
            return dict(row)

    def create_workflow(self, workflow_type: str, idempotency_key: str, project_id: str | None = None, workflow_id: str | None = None) -> dict[str, Any]:
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
                (workflow_id or _id("workflow"), project_id, workflow_type, idempotency_key, timestamp, timestamp),
            ).fetchone()
            self._audit(db, "operator", "operator", "workflow.created", project_id=project_id, target_id=row["workflow_id"])
            return dict(row)

    def start_or_get_workflow(self, workflow_type: str, idempotency_key: str, project_id: str | None, steps: list[dict[str, Any]], workflow_id: str | None = None) -> dict[str, Any]:
        workflow = self.create_workflow(workflow_type, idempotency_key, project_id, workflow_id)
        with transaction(self.settings) as db:
            if project_id and workflow.get("project_id") is None:
                db.execute("UPDATE prime_core.workflows SET project_id=%s,updated_at=now() WHERE workflow_id=%s", (project_id, workflow["workflow_id"]))
            for index, specification in enumerate(steps):
                policy = specification.get("replay_policy", "PURE_OR_DB_TRANSACTION")
                if policy not in REPLAY_POLICIES:
                    raise ValueError("invalid workflow replay policy")
                db.execute(
                    "INSERT INTO prime_core.workflow_steps(workflow_id,step_key,step_order,status,replay_policy,input_metadata) VALUES (%s,%s,%s,'PENDING',%s,%s) ON CONFLICT (workflow_id,step_key) DO NOTHING",
                    (workflow["workflow_id"], specification["step_key"], specification.get("step_order", index), policy, json.dumps(specification.get("input_metadata", {}))),
                )
            row = db.execute("SELECT * FROM prime_core.workflows WHERE workflow_id=%s", (workflow["workflow_id"],)).fetchone()
            return dict(row)

    def begin_step(self, workflow_id: str, step_key: str) -> dict[str, Any]:
        with transaction(self.settings) as db:
            step = db.execute("SELECT * FROM prime_core.workflow_steps WHERE workflow_id=%s AND step_key=%s FOR UPDATE", (workflow_id, step_key)).fetchone()
            if not step:
                raise KeyError("workflow step not found")
            decision = step_resume_decision(step["status"], step["replay_policy"])
            if decision == "SKIP_COMPLETED":
                return {**dict(step), "decision": decision}
            if decision == "REPAIR_REQUIRED":
                db.execute("UPDATE prime_core.workflow_steps SET status='REPAIR_REQUIRED',last_error=COALESCE(last_error,'ambiguous external outcome') WHERE workflow_id=%s AND step_key=%s", (workflow_id, step_key))
                db.execute("UPDATE prime_core.workflows SET status='REPAIR_REQUIRED',current_step=%s,updated_at=now() WHERE workflow_id=%s", (step_key, workflow_id))
                return {**dict(step), "status": "REPAIR_REQUIRED", "decision": decision}
            updated = db.execute("UPDATE prime_core.workflow_steps SET status='RUNNING',attempt_count=attempt_count+1,started_at=COALESCE(started_at,now()),last_error=NULL WHERE workflow_id=%s AND step_key=%s RETURNING *", (workflow_id, step_key)).fetchone()
            db.execute("UPDATE prime_core.workflows SET status='RUNNING',current_step=%s,updated_at=now() WHERE workflow_id=%s", (step_key, workflow_id))
            return {**dict(updated), "decision": decision}

    def complete_step(self, workflow_id: str, step_key: str, result_metadata: dict[str, Any] | None = None, side_effect_state: dict[str, Any] | None = None) -> dict[str, Any]:
        with transaction(self.settings) as db:
            step = db.execute("SELECT * FROM prime_core.workflow_steps WHERE workflow_id=%s AND step_key=%s FOR UPDATE", (workflow_id, step_key)).fetchone()
            if not step:
                raise KeyError("workflow step not found")
            if step["status"] in {"SUCCEEDED", "COMPENSATED"}:
                return dict(step)
            if step["status"] != "RUNNING":
                raise ValueError("workflow step is not running")
            updated = db.execute("UPDATE prime_core.workflow_steps SET status='SUCCEEDED',completed_at=now(),result_metadata=%s,side_effect_state=%s WHERE workflow_id=%s AND step_key=%s RETURNING *", (json.dumps(result_metadata or {}), json.dumps(side_effect_state or {}), workflow_id, step_key)).fetchone()
            workflow = db.execute("SELECT completed_steps FROM prime_core.workflows WHERE workflow_id=%s FOR UPDATE", (workflow_id,)).fetchone()
            completed = workflow["completed_steps"] if isinstance(workflow["completed_steps"], list) else json.loads(workflow["completed_steps"] or "[]")
            if step_key not in completed:
                completed.append(step_key)
            db.execute("UPDATE prime_core.workflows SET completed_steps=%s,current_step=%s,status='RUNNING',updated_at=now() WHERE workflow_id=%s", (json.dumps(completed), step_key, workflow_id))
            return dict(updated)

    def fail_step(self, workflow_id: str, step_key: str, error_message: str, retryable: bool = True, ambiguous_external_effect: bool = False) -> dict[str, Any]:
        status = "REPAIR_REQUIRED" if ambiguous_external_effect else ("FAILED_RETRYABLE" if retryable else "FAILED_FINAL")
        with transaction(self.settings) as db:
            updated = db.execute("UPDATE prime_core.workflow_steps SET status=%s,last_error=%s WHERE workflow_id=%s AND step_key=%s RETURNING *", (status, error_message[:500], workflow_id, step_key)).fetchone()
            if not updated:
                raise KeyError("workflow step not found")
            db.execute("UPDATE prime_core.workflows SET status=%s,current_step=%s,retry_count=retry_count+1,last_error=%s,updated_at=now() WHERE workflow_id=%s", ("REPAIR_REQUIRED" if ambiguous_external_effect else "RUNNING", step_key, error_message[:500], workflow_id))
            return dict(updated)

    def record_workflow_resource(self, workflow_id: str, resource_type: str, resource_key: str, resource_locator: str | None, metadata: dict[str, Any] | None = None, status: str = "CREATED") -> dict[str, Any]:
        if status not in {"EXPECTED", "CREATED", "RECONCILIATION_REQUIRED", "RELEASED"}:
            raise ValueError("invalid workflow resource status")
        with transaction(self.settings) as db:
            row = db.execute(
                "INSERT INTO prime_core.workflow_resources(resource_id,workflow_id,resource_type,resource_key,resource_locator,status,metadata,created_at,updated_at) VALUES (%s,%s,%s,%s,%s,%s,%s,now(),now()) ON CONFLICT (workflow_id,resource_type,resource_key) DO UPDATE SET resource_locator=COALESCE(EXCLUDED.resource_locator,prime_core.workflow_resources.resource_locator),status=CASE WHEN prime_core.workflow_resources.status IN ('CREATED','RECONCILIATION_REQUIRED','RELEASED') AND EXCLUDED.status='EXPECTED' THEN prime_core.workflow_resources.status ELSE EXCLUDED.status END,metadata=CASE WHEN prime_core.workflow_resources.status IN ('CREATED','RECONCILIATION_REQUIRED','RELEASED') AND EXCLUDED.status='EXPECTED' THEN prime_core.workflow_resources.metadata ELSE EXCLUDED.metadata END,updated_at=now() RETURNING *",
                (_id("resource"), workflow_id, resource_type, resource_key, resource_locator, status, json.dumps(metadata or {})),
            ).fetchone()
            return dict(row)

    def complete_workflow(self, workflow_id: str, final_step: str | None = None) -> dict[str, Any]:
        with transaction(self.settings) as db:
            incomplete = db.execute(
                "SELECT step_key,status FROM prime_core.workflow_steps WHERE workflow_id=%s AND status NOT IN ('SUCCEEDED','COMPENSATED') ORDER BY step_order LIMIT 1",
                (workflow_id,),
            ).fetchone()
            if incomplete:
                raise ValueError(f"workflow step {incomplete['step_key']} is {incomplete['status']}")
            row = db.execute(
                "UPDATE prime_core.workflows SET status='SUCCEEDED',current_step=COALESCE(%s,current_step),last_error=NULL,updated_at=now() WHERE workflow_id=%s RETURNING *",
                (final_step, workflow_id),
            ).fetchone()
            if not row:
                raise KeyError("workflow not found")
            return dict(row)

    def compensate_step(self, workflow_id: str, step_key: str, result: dict[str, Any] | None = None) -> dict[str, Any]:
        with transaction(self.settings) as db:
            row = db.execute(
                "UPDATE prime_core.workflow_steps SET status='COMPENSATED',completed_at=now(),result_metadata=%s,last_error=NULL WHERE workflow_id=%s AND step_key=%s AND status IN ('RUNNING','SUCCEEDED','FAILED_RETRYABLE','REPAIR_REQUIRED') RETURNING *",
                (json.dumps(result or {}), workflow_id, step_key),
            ).fetchone()
            if not row:
                raise ValueError("workflow step cannot be compensated")
            return dict(row)

    def workflow_resume_plan(self, workflow_id: str) -> dict[str, Any]:
        with connect(self.settings) as db:
            workflow = db.execute("SELECT * FROM prime_core.workflows WHERE workflow_id=%s", (workflow_id,)).fetchone()
            if not workflow:
                raise KeyError("workflow not found")
            steps = [dict(row) for row in db.execute("SELECT * FROM prime_core.workflow_steps WHERE workflow_id=%s ORDER BY step_order", (workflow_id,)).fetchall()]
            resources = [dict(row) for row in db.execute("SELECT resource_type,resource_key,resource_locator,status,metadata FROM prime_core.workflow_resources WHERE workflow_id=%s ORDER BY created_at", (workflow_id,)).fetchall()]
        return resume_plan_payload(dict(workflow), steps, resources)

    def workflow_reconciliation_report(self, project_id: str | None = None) -> dict[str, Any]:
        where = "WHERE w.status <> 'SUCCEEDED'"
        params: list[Any] = []
        if project_id:
            where += " AND w.project_id=%s"
            params.append(project_id)
        with connect(self.settings) as db:
            workflows = [dict(row) for row in db.execute(
                f"SELECT w.* FROM prime_core.workflows w {where} ORDER BY w.updated_at,w.workflow_id",
                params,
            ).fetchall()]
            workflow_ids = [row["workflow_id"] for row in workflows]
            steps: list[dict[str, Any]] = []
            resources: list[dict[str, Any]] = []
            if workflow_ids:
                steps = [dict(row) for row in db.execute(
                    "SELECT * FROM prime_core.workflow_steps WHERE workflow_id=ANY(%s) AND status NOT IN ('SUCCEEDED','COMPENSATED') ORDER BY workflow_id,step_order",
                    (workflow_ids,),
                ).fetchall()]
                resources = [dict(row) for row in db.execute(
                    "SELECT * FROM prime_core.workflow_resources WHERE workflow_id=ANY(%s) AND status IN ('EXPECTED','CREATED','RECONCILIATION_REQUIRED') ORDER BY workflow_id,created_at",
                    (workflow_ids,),
                ).fetchall()]
        action_required = any(row["status"] == "REPAIR_REQUIRED" for row in workflows) or any(row["status"] == "RECONCILIATION_REQUIRED" for row in resources)
        return {
            "status": "ACTION_REQUIRED" if action_required else ("INCOMPLETE" if workflows else "CLEAR"),
            "incomplete_workflows": workflows,
            "incomplete_steps": steps,
            "accounted_resources": resources,
            "operator_action_required": action_required,
        }

    def mark_workflow_repaired(self, workflow_id: str, step_key: str, resolution: dict[str, Any] | None = None) -> dict[str, Any]:
        with transaction(self.settings) as db:
            updated = db.execute("UPDATE prime_core.workflow_steps SET status='PENDING',last_error=NULL,result_metadata=%s WHERE workflow_id=%s AND step_key=%s AND status='REPAIR_REQUIRED' RETURNING *", (json.dumps(resolution or {}), workflow_id, step_key)).fetchone()
            if not updated:
                raise ValueError("workflow step is not awaiting repair")
            db.execute("UPDATE prime_core.workflows SET status='RUNNING',last_error=NULL,current_step=%s,updated_at=now() WHERE workflow_id=%s", (step_key, workflow_id))
            return dict(updated)

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
                   dedupe_key: str | None = None, occurred_at: datetime | None = None,
                   source_revision: str | None = None, source_ref: str | None = None) -> dict[str, Any]:
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
                "INSERT INTO prime_core.events(event_id, project_id, event_type, occurred_at, observed_at, project_sequence, source_revision, source_ref, payload, dedupe_key) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING *",
                (_id("evt"), project_id, event_type, occurred_at or timestamp, timestamp, sequence, source_revision, source_ref, json.dumps(payload), dedupe_key),
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
