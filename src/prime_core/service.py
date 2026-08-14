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
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from .config import Settings
from .db import connect, transaction
from .security import new_token, password_hash, password_verify, token_digest
from .history_primitives import record_historical_snapshot
from .authority import REQUIRED_AUTHORITY_FILES, authority_migration_plan, classify_authority_snapshot, migrate_authority, provision_authority, validate_authority
from .git_provenance import GitProvenanceError, resolve_canonical_ref

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
            node = db.execute("SELECT node_id,name,status,allowed_roots FROM prime_core.nodes WHERE node_id=%s", (node_id,)).fetchone()
        if not project:
            raise KeyError("project not found")
        if not node:
            raise KeyError("node not found")
        if node["status"] in {"OFFLINE", "REVOKED"}:
            raise ValueError(f"Node is {node['status']}")
        roots = node["allowed_roots"] if isinstance(node["allowed_roots"], list) else json.loads(node["allowed_roots"] or "[]")
        if not self._within_allowed_root(candidate, roots):
            raise PermissionError("path is outside the enrolled Node allowed roots")
        if not candidate.exists() or not candidate.is_dir():
            raise FileNotFoundError("repository path does not exist or is not a directory")
        try:
            values = subprocess.run(["git", "-C", str(candidate), "rev-parse", "--show-toplevel", "--git-common-dir", "--is-bare-repository"], check=True, capture_output=True, text=True, timeout=5).stdout.splitlines()
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
            raise ValueError("path is not a readable Git working repository") from exc
        if len(values) < 3 or values[2].strip().lower() == "true":
            raise ValueError("bare repositories are not supported")
        top = Path(values[0]).resolve()
        common = Path(values[1])
        if not common.is_absolute():
            common = (candidate / common).resolve()
        identity = hashlib.sha256(str(common).encode("utf-8")).hexdigest()
        with connect(self.settings) as db:
            duplicate = db.execute("SELECT project_id FROM prime_core.repositories WHERE identity_fingerprint=%s AND project_id<>%s", (identity, project_id)).fetchone()
        authority_root = top / ".agent"
        if not authority_root.exists():
            authority_state = "NONE"
        else:
            authority_state = "CURRENT" if validate_authority(top)["valid"] else "INVALID"
        return {"project_id": project_id, "node_id": node_id, "node_name": node["name"], "canonical_path": str(top), "git_common_dir": str(common), "identity_fingerprint": identity, "is_bare": False, "branch": subprocess.run(["git", "-C", str(top), "branch", "--show-current"], check=False, capture_output=True, text=True, timeout=5).stdout.strip() or "DETACHED", "authority_state": authority_state, "duplicate_project_id": duplicate["project_id"] if duplicate else None, "onboarding_decision": "REJECT_DUPLICATE" if duplicate else "REVIEW_AUTHORITY" if authority_state != "NONE" else "READY_TO_BIND"}

    def bind_verified_repository(self, inspection: dict[str, Any], confirm: bool = False) -> dict[str, Any]:
        if not confirm:
            raise ValueError("operator confirmation is required before binding a repository")
        if inspection.get("duplicate_project_id"):
            raise ValueError("repository is already bound to another active project")
        result = self.bind_repository(inspection["project_id"], inspection["node_id"], inspection["identity_fingerprint"], inspection["canonical_path"], False)
        with transaction(self.settings) as db:
            db.execute("UPDATE prime_core.projects SET onboarding_step='AUTHORITY', onboarding_state='IN_PROGRESS', updated_at=%s WHERE project_id=%s", (now(), inspection["project_id"]))
        return {**result, "authority_state": inspection.get("authority_state", "UNKNOWN")}

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
            node = db.execute("SELECT allowed_roots,status FROM prime_core.nodes WHERE node_id=%s", (node_id,)).fetchone()
        if not node:
            raise KeyError("node not found")
        if node["status"] in {"OFFLINE", "REVOKED"}:
            raise ValueError(f"Node is {node['status']}")
        roots = node["allowed_roots"] if isinstance(node["allowed_roots"], list) else json.loads(node["allowed_roots"] or "[]")
        parent = Path(parent_path).expanduser().resolve(strict=True)
        if not parent.is_dir() or not self._within_allowed_root(parent, roots):
            raise PermissionError("repository parent is outside the enrolled Node allowed roots")
        target = parent / repository_name
        if target.exists() or target.is_symlink():
            raise FileExistsError("repository target already exists")
        workflow = self.create_workflow("CREATE_REPOSITORY", f"create-repository:{project_id}:{target}", project_id)
        try:
            target.mkdir()
            subprocess.run(["git", "-C", str(target), "init", "--initial-branch=main"], check=True, capture_output=True, text=True, timeout=10)
            inspection = self.inspect_repository_for_onboarding(project_id, node_id, str(target))
            bound = self.bind_verified_repository(inspection, confirm=True)
            with transaction(self.settings) as db:
                db.execute("UPDATE prime_core.workflows SET status='SUCCEEDED', current_step='BOUND', completed_steps='[\"DIRECTORY_CREATED\",\"GIT_INITIALIZED\",\"BOUND\"]'::jsonb, updated_at=%s WHERE workflow_id=%s", (now(), workflow["workflow_id"]))
            return {"workflow": workflow["workflow_id"], "repository": bound, "inspection": inspection}
        except Exception as exc:
            with transaction(self.settings) as db:
                db.execute("UPDATE prime_core.workflows SET status='REPAIR_REQUIRED', current_step='RECONCILIATION_REQUIRED', last_error=%s, updated_at=%s WHERE workflow_id=%s", (type(exc).__name__, now(), workflow["workflow_id"]))
                db.execute("UPDATE prime_core.projects SET lifecycle_state='PROVISIONING', work_condition='REVIEW_REQUIRED', onboarding_state='REPAIR_REQUIRED', updated_at=%s WHERE project_id=%s", (now(), project_id))
            raise

    def bootstrap_project_authority(self, project_id: str, confirm: bool = False) -> dict[str, Any]:
        if not confirm:
            raise ValueError("operator confirmation is required before authority bootstrap")
        with connect(self.settings) as db:
            row = db.execute("SELECT canonical_path FROM prime_core.repositories WHERE project_id=%s", (project_id,)).fetchone()
        if not row:
            raise ValueError("bind a verified repository before authority bootstrap")
        root = Path(row["canonical_path"]).resolve(strict=True)
        if (root / ".agent").exists():
            raise FileExistsError("authority already exists; use explicit adopt or review flow")
        result = provision_authority(Path("authority-template/v1").resolve(), root)
        authority = validate_authority(root)
        with transaction(self.settings) as db:
            db.execute("UPDATE prime_core.projects SET onboarding_step='GOAL', onboarding_state='IN_PROGRESS', updated_at=%s WHERE project_id=%s", (now(), project_id))
        self.record_authority_revision(project_id, ".agent", hashlib.sha256(json.dumps(authority, sort_keys=True).encode()).hexdigest(), "VALID", {"provenance": "operator-approved authority-template/v1", "template_manifest": str(Path("authority-template/v1/MANIFEST.sha256").resolve())}, canonical_commit=None)
        return {"project_id": project_id, "authority": result, "state": "CURRENT", "template": "authority-template/v1"}

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
        result = migrate_authority(Path("authority-template/v1").resolve(), root, {
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

    def agent_instruction_chain(self, project_id: str, relative_path: str = "") -> dict[str, Any]:
        with connect(self.settings) as db:
            row = db.execute("SELECT r.canonical_path FROM prime_core.repositories r WHERE r.project_id=%s", (project_id,)).fetchone()
        if not row:
            raise KeyError("project has no repository binding")
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

    def fork_project(self, source_project_id: str, source_revision: str, destination_node_id: str, parent_path: str, repository_name: str, confirm: bool = False) -> dict[str, Any]:
        if not confirm:
            raise ValueError("operator confirmation is required before fork")
        if not repository_name or repository_name in {".", ".."} or Path(repository_name).name != repository_name:
            raise ValueError("repository name must be one directory name")
        with connect(self.settings) as db:
            source = db.execute("SELECT p.*,r.canonical_path,r.node_id FROM prime_core.projects p JOIN prime_core.repositories r ON r.project_id=p.project_id WHERE p.project_id=%s", (source_project_id,)).fetchone()
            node = db.execute("SELECT node_id,name,status,allowed_roots FROM prime_core.nodes WHERE node_id=%s", (destination_node_id,)).fetchone()
            goal = db.execute("SELECT content FROM prime_core.goal_revisions WHERE project_id=%s AND status='APPROVED' ORDER BY revision_number DESC LIMIT 1", (source_project_id,)).fetchone()
        if not source:
            raise KeyError("source project not found")
        if not node:
            raise KeyError("destination node not found")
        if node["status"] in {"OFFLINE", "REVOKED"}:
            raise ValueError(f"Node is {node['status']}")
        source_root = Path(source["canonical_path"]).resolve(strict=True)
        clean = subprocess.run(["git", "-C", str(source_root), "status", "--porcelain"], check=True, capture_output=True, text=True, timeout=10).stdout.strip()
        if clean:
            raise ValueError("fork requires a clean source working tree")
        subprocess.run(["git", "-C", str(source_root), "cat-file", "-e", f"{source_revision}^{{commit}}"], check=True, capture_output=True, text=True, timeout=10)
        roots = node["allowed_roots"] if isinstance(node["allowed_roots"], list) else json.loads(node["allowed_roots"] or "[]")
        parent = Path(parent_path).expanduser().resolve(strict=True)
        if not parent.is_dir() or not self._within_allowed_root(parent, roots):
            raise PermissionError("fork destination is outside the enrolled Node allowed roots")
        target = parent / repository_name
        if target.exists() or target.is_symlink():
            raise FileExistsError("fork destination already exists")
        project = self.create_project(repository_name, source.get("description", ""), source.get("image_url"))
        workflow = self.create_workflow("FORK_PROJECT", f"fork:{source_project_id}:{source_revision}:{target}", project["project_id"])
        try:
            subprocess.run(["git", "clone", "--no-hardlinks", str(source_root), str(target)], check=True, capture_output=True, text=True, timeout=60)
            subprocess.run(["git", "-C", str(target), "checkout", "--detach", source_revision], check=True, capture_output=True, text=True, timeout=30)
            remotes = subprocess.run(["git", "-C", str(target), "remote"], check=True, capture_output=True, text=True, timeout=10).stdout.split()
            for remote in remotes:
                subprocess.run(["git", "-C", str(target), "remote", "remove", remote], check=True, capture_output=True, text=True, timeout=10)
            for relative in REQUIRED_AUTHORITY_FILES:
                candidate = target / relative
                if candidate.is_file() or candidate.is_symlink():
                    candidate.unlink()
            provision_authority(Path("authority-template/v1").resolve(), target)
            inspection = self.inspect_repository_for_onboarding(project["project_id"], destination_node_id, str(target))
            binding = self.bind_verified_repository(inspection, confirm=True)
            if goal:
                self.create_goal_revision(project["project_id"], goal["content"], approve=False)
            indexed = __import__("src.prime_core.indexer", fromlist=["RepositoryIndexer"]).RepositoryIndexer(self).build(project["project_id"])
            grant = __import__("src.prime_core.mcp_service", fromlist=["MCPService"]).MCPService(self.settings).issue_grant(project["project_id"], "fork-initial-coder")
            destination_revision = indexed["source_revision"]
            with transaction(self.settings) as db:
                fork = db.execute("INSERT INTO prime_core.project_forks(fork_id,source_project_id,new_project_id,source_revision,memory_copy_status,destination_node_id,destination_repository_id,destination_revision,provenance,created_at) VALUES (%s,%s,%s,%s,'NONE',%s,%s,%s,%s,%s) RETURNING *", (_id("fork"), source_project_id, project["project_id"], source_revision, destination_node_id, binding["repository_id"], destination_revision, json.dumps({"source": "git archive", "source_revision": source_revision, "memory": "NOT_COPIED", "notion": "NOT_COPIED", "hindsight": "DEGRADED_OR_UNAVAILABLE"}), now())).fetchone()
                db.execute("UPDATE prime_core.workflows SET status='SUCCEEDED',current_step='INDEXED',completed_steps='[\"CLONED\",\"REMOTES_CLEARED\",\"AUTHORITY_TEMPLATE\",\"BOUND\",\"GOAL_DRAFT\",\"INDEXED\"]'::jsonb,updated_at=%s WHERE workflow_id=%s", (now(), workflow["workflow_id"]))
            return {"fork": dict(fork), "project": project, "binding": binding, "indexed": indexed, "mcp_grant": grant, "memory_copy_status": "NONE", "notion_status": "NOT_COPIED", "hindsight_status": "DEGRADED_OR_UNAVAILABLE", "goal_status": "DRAFT", "authority_provenance": "CURRENT_TEMPLATE_NOT_PARENT_AUTHORITY", "remote_status": "CLEARED"}
        except Exception as exc:
            with transaction(self.settings) as db:
                db.execute("UPDATE prime_core.workflows SET status='REPAIR_REQUIRED',current_step='RECONCILIATION_REQUIRED',last_error=%s,updated_at=%s WHERE workflow_id=%s", (type(exc).__name__, now(), workflow["workflow_id"]))
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

    def create_goal_revision(self, project_id: str, content: str, approve: bool = False) -> dict[str, Any]:
        timestamp = now()
        if approve:
            with connect(self.settings) as db:
                binding = db.execute("SELECT canonical_path FROM prime_core.repositories WHERE project_id=%s", (project_id,)).fetchone()
            if binding:
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
