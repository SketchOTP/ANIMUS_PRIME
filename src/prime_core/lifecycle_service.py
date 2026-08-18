from __future__ import annotations

import hashlib
import json
import secrets
from typing import Any, Callable

from .db import connect, transaction
from .service import _id, now
from .workflow_primitives import qualification_interrupt

ALLOWED = {
    "DRAFT": {"PROVISIONING", "DELETION_PENDING"},
    "PROVISIONING": {"READY", "PAUSED", "DELETION_PENDING", "ARCHIVED", "REMOVED"},
    "READY": {"ACTIVE", "PAUSED", "DELETION_PENDING", "ARCHIVED", "REMOVED"},
    "ACTIVE": {"PAUSED", "COMPLETION_REVIEW", "DELETION_PENDING", "ARCHIVED", "REMOVED"},
    "PAUSED": {"ACTIVE", "COMPLETION_REVIEW", "DELETION_PENDING", "ARCHIVED", "REMOVED"},
    "COMPLETION_REVIEW": {"COMPLETED", "ACTIVE", "DELETION_PENDING", "ARCHIVED", "REMOVED"},
    "COMPLETED": {"ARCHIVED", "ACTIVE", "REMOVED", "DELETION_PENDING"},
    "ARCHIVED": {"ACTIVE", "REMOVED", "DELETION_PENDING"},
    "REMOVED": {"ACTIVE", "DELETION_PENDING"},
    "DELETION_PENDING": {"DELETED"},
    "DELETED": set(),
}

ACTION_TARGETS = {"PAUSE": "PAUSED", "RESUME": "ACTIVE", "ENTER_COMPLETION_REVIEW": "COMPLETION_REVIEW", "CANCEL_COMPLETION_REVIEW": "ACTIVE", "REQUEST_COMPLETION": "COMPLETED", "REMOVE": "REMOVED", "ARCHIVE": "ARCHIVED", "DELETE": "DELETION_PENDING", "PURGE": "DELETED"}
ACTION_DESCRIPTIONS = {
    "PAUSE": "Keep the project managed and inspectable while reducing ordinary watchers and automation.",
    "RESUME": "Return a paused, archived, or removed project to active management.",
    "ENTER_COMPLETION_REVIEW": "Open operator completion review without declaring the project complete.",
    "CANCEL_COMPLETION_REVIEW": "Cancel completion review and return the project to active management.",
    "REQUEST_COMPLETION": "Confirm an operator-reviewed project as completed.",
    "REMOVE": "Stop managing the project in the active PRIME dashboard while preserving the repository and external record.",
    "ARCHIVE": "Make the project read-only historical while preserving its repository, memory, and Notion record.",
    "DELETE": "Archive managed external state, quarantine the repository, revoke project access, stop work, and enter deletion pending.",
    "PURGE": "Erase selected locally controlled resources while retaining only the minimum audit tombstone.",
}


class LifecycleService:
    def __init__(self, settings: Any, core: Any | None = None, memory: Any | None = None, notion_resolver: Callable[[], Any] | None = None):
        self.settings, self.core, self.memory, self.notion_resolver = settings, core, memory, notion_resolver

    @staticmethod
    def _state_hash(project: dict[str, Any], binding: dict[str, Any] | None) -> str:
        values = {"project_id": project.get("project_id"), "lifecycle_state": project.get("lifecycle_state"), "updated_at": project.get("updated_at").isoformat() if hasattr(project.get("updated_at"), "isoformat") else project.get("updated_at"), "repository_id": binding.get("repository_id") if binding else None, "canonical_path": binding.get("canonical_path") if binding else None, "identity_fingerprint": binding.get("identity_fingerprint") if binding else None}
        return hashlib.sha256(json.dumps(values, sort_keys=True, default=str).encode()).hexdigest()

    @staticmethod
    def _action(action: str) -> str:
        action = action.upper().strip()
        if action not in ACTION_TARGETS:
            raise ValueError(f"unsupported lifecycle action: {action}")
        return action

    def _binding(self, db: Any, project_id: str) -> Any:
        return db.execute("SELECT r.repository_id,r.canonical_path,r.identity_fingerprint,r.is_bare,b.node_id,n.name AS node_name,n.status AS node_status FROM prime_core.project_bindings b JOIN prime_core.repositories r ON r.repository_id=b.repository_id LEFT JOIN prime_core.nodes n ON n.node_id=b.node_id WHERE b.project_id=%s", (project_id,)).fetchone()

    def _backup_disclosure(self, db: Any, project_id: str) -> dict[str, Any]:
        rows = db.execute("SELECT backup_id,status,destination_class,verified_at FROM prime_core.backup_records WHERE project_ids @> %s::jsonb ORDER BY captured_at DESC LIMIT 20", (json.dumps([project_id]),)).fetchall()
        return {"matching_backups": [dict(row) for row in rows], "policy": "ENCRYPTED_BACKUPS_SURVIVE_UNTIL_EXISTING_RETENTION_EXPIRY"}

    def preflight(self, project_id: str, action: str, step_up_recent: bool = False) -> dict[str, Any]:
        action = self._action(action)
        with connect(self.settings) as db:
            project = db.execute("SELECT * FROM prime_core.projects WHERE project_id=%s", (project_id,)).fetchone()
            if not project:
                raise KeyError("project not found")
            binding = self._binding(db, project_id)
            backup = self._backup_disclosure(db, project_id) if action in {"DELETE", "PURGE"} else None
            grants = db.execute("SELECT count(*) AS count FROM prime_core.mcp_grants WHERE project_id=%s AND revoked_at IS NULL", (project_id,)).fetchone()["count"]
            jobs = db.execute("SELECT count(*) AS count FROM prime_core.jobs WHERE project_id=%s AND status IN ('QUEUED','RUNNING','ACTION_REQUIRED')", (project_id,)).fetchone()["count"]
        token, preflight_id = secrets.token_urlsafe(32), _id("lifecycle-preflight")
        with transaction(self.settings) as db:
            db.execute("INSERT INTO prime_core.lifecycle_preflights(preflight_id,project_id,action,state_hash,token_hash,expires_at) VALUES (%s,%s,%s,%s,%s,now()+interval '5 minutes')", (preflight_id, project_id, action, self._state_hash(dict(project), dict(binding) if binding else None), hashlib.sha256(token.encode()).hexdigest()))
        repository_confirmation = f"{project['name']}::{binding['canonical_path']}" if action == "PURGE" and binding else None
        return {
            "preflight_id": preflight_id, "preflight_token": token, "project_id": project_id, "action": action, "current_state": project["lifecycle_state"], "target_state": ACTION_TARGETS[action], "description": ACTION_DESCRIPTIONS[action],
            "requires_step_up": action in {"DELETE", "PURGE", "REQUEST_COMPLETION"}, "step_up_recent": bool(step_up_recent), "expires_in_seconds": 300,
            "target": {"project_name": project["name"], "node_id": binding["node_id"] if binding else None, "node_name": binding["node_name"] if binding else None, "canonical_path": binding["canonical_path"] if binding else None, "repository_id": binding["repository_id"] if binding else None},
            "disposition": {"repository": "preserved untouched" if action in {"REMOVE", "ARCHIVE"} else ("move to Node-owned quarantine" if action == "DELETE" else "erase only from recorded quarantine when separately selected"), "prime_metadata": "retained" if action != "PURGE" else "purged except minimum audit tombstone", "hindsight": "preserved" if action != "PURGE" else "project bank deleted through supported Hindsight API", "notion": "managed page archived but never erased by PRIME" if action == "DELETE" else "external page survives", "credentials": {"active_project_grants": grants}, "active_work": {"jobs": jobs, "watchers": "no separate watcher runtime"}, "backups": backup, "external_survival": ["Notion pages", "remote Git providers", "external Evidence URLs", "provider logs", "retained encrypted backups"]},
            "repository_erasure_confirmation": repository_confirmation,
        }

    def _validate(self, project_id: str, action: str, token: str, confirmation: str | None, step_up_recent: bool) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any] | None]:
        with connect(self.settings) as db:
            preflight = db.execute("SELECT * FROM prime_core.lifecycle_preflights WHERE project_id=%s AND action=%s AND token_hash=%s", (project_id, action, hashlib.sha256(token.encode()).hexdigest())).fetchone()
            project = db.execute("SELECT * FROM prime_core.projects WHERE project_id=%s", (project_id,)).fetchone()
            binding = self._binding(db, project_id)
        if not preflight:
            raise ValueError("lifecycle preflight is invalid")
        if preflight["used_at"] is not None:
            raise ValueError("lifecycle preflight has already been used")
        if preflight["expires_at"] <= now():
            raise ValueError("lifecycle preflight is stale")
        if not project:
            raise KeyError("project not found")
        if preflight["state_hash"] != self._state_hash(dict(project), dict(binding) if binding else None):
            raise ValueError("lifecycle preflight is stale because project state changed")
        target = ACTION_TARGETS[action]
        if target not in ALLOWED.get(project["lifecycle_state"], set()):
            raise ValueError(f"invalid lifecycle transition {project['lifecycle_state']}->{target}")
        if action in {"DELETE", "PURGE", "REQUEST_COMPLETION"}:
            if confirmation != project_id:
                raise PermissionError("exact project identity confirmation is required")
            if not step_up_recent:
                raise PermissionError("recent step-up authentication is required")
        elif confirmation != "CONFIRM":
            raise ValueError("explicit confirmation is required")
        return dict(preflight), dict(project), dict(binding) if binding else None

    def _record_disposition(self, project_id: str, workflow_id: str, resource_type: str, resource_key: str, locator: str | None, status: str, details: dict[str, Any]) -> None:
        with transaction(self.settings) as db:
            db.execute("INSERT INTO prime_core.lifecycle_resource_dispositions(disposition_id,project_id,workflow_id,resource_type,resource_key,locator,status,details) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT(project_id,resource_type,resource_key) DO UPDATE SET workflow_id=EXCLUDED.workflow_id,locator=EXCLUDED.locator,status=EXCLUDED.status,details=EXCLUDED.details,updated_at=now()", (_id("disp"), project_id, workflow_id, resource_type, resource_key, locator, status, json.dumps(details)))

    def _step(self, workflow: dict[str, Any], key: str, action: Callable[[], dict[str, Any]], resource: tuple[str, str] | None = None) -> dict[str, Any]:
        step = self.core.begin_step(workflow["workflow_id"], key)
        if step.get("decision") == "SKIP_COMPLETED":
            value = step.get("result_metadata") or step.get("side_effect_state") or {}
            return value if isinstance(value, dict) else json.loads(value)
        try:
            result = action()
            qualification_interrupt(workflow["workflow_type"], key, "AFTER_EFFECT_BEFORE_CHECKPOINT")
            if resource:
                self.core.record_workflow_resource(workflow["workflow_id"], resource[0], resource[1], result.get("quarantine_path") or result.get("page_id") or result.get("bank_id"), result, "CREATED")
            self.core.complete_step(workflow["workflow_id"], key, result, result)
            return result
        except Exception as exc:
            self.core.fail_step(workflow["workflow_id"], key, str(exc), retryable=True, ambiguous_external_effect=False)
            raise

    def _atomic_transition(self, project_id: str, action: str, preflight_id: str, confirmation: str, current: str, target: str, workflow_id: str | None = None) -> dict[str, Any]:
        operation_id = _id("lifecycle")
        with transaction(self.settings) as db:
            db.execute("UPDATE prime_core.projects SET lifecycle_state=%s,updated_at=now() WHERE project_id=%s", (target, project_id))
            db.execute("UPDATE prime_core.lifecycle_preflights SET used_at=now() WHERE preflight_id=%s", (preflight_id,))
            if action == "PURGE":
                return {"operation_id": operation_id, "project_id": project_id, "action": action, "from_state": current, "to_state": target, "workflow_id": workflow_id}
            db.execute("INSERT INTO prime_core.lifecycle_operations(operation_id,project_id,from_state,to_state,actor_type,actor_id,confirmation_hash,step_up_at,created_at) VALUES (%s,%s,%s,%s,'operator','operator',%s,now(),now())", (operation_id, project_id, current, target, hashlib.sha256(confirmation.encode()).hexdigest()))
            db.execute("INSERT INTO prime_core.audit_events(audit_id,actor_type,actor_id,action,project_id,target_id,occurred_at,metadata) VALUES (%s,'operator','operator',%s,%s,%s,now(),%s)", (_id("audit"), f"project.lifecycle.{action.lower()}", project_id, operation_id, json.dumps({"from_state": current, "to_state": target, "workflow_id": workflow_id})))
            sequence = db.execute("SELECT COALESCE(MAX(project_sequence),0)+1 AS n FROM prime_core.events WHERE project_id=%s", (project_id,)).fetchone()["n"]
            db.execute("INSERT INTO prime_core.events(event_id,project_id,event_type,occurred_at,observed_at,project_sequence,payload) VALUES (%s,%s,%s,now(),now(),%s,%s)", (_id("evt"), project_id, f"PROJECT_{action}", sequence, json.dumps({"from_state": current, "to_state": target, "operation_id": operation_id, "workflow_id": workflow_id})))
        return {"operation_id": operation_id, "project_id": project_id, "action": action, "from_state": current, "to_state": target, "workflow_id": workflow_id}

    def _delete(self, project_id: str, preflight: dict[str, Any], project: dict[str, Any], binding: dict[str, Any] | None, confirmation: str, preserve_snapshot: bool) -> dict[str, Any]:
        steps = [{"step_key": "PREFLIGHT_VERIFIED"}, {"step_key": "SNAPSHOT_DISPOSITION"}, {"step_key": "NOTION_DISPOSITION", "replay_policy": "IDEMPOTENT_EXTERNAL"}, {"step_key": "REPOSITORY_QUARANTINED", "replay_policy": "IDEMPOTENT_EXTERNAL"}, {"step_key": "ACTIVE_WORK_STOPPED"}, {"step_key": "CREDENTIALS_REVOKED"}, {"step_key": "RESOURCE_DISPOSITION_RECORDED"}, {"step_key": "STATE_TRANSITIONED"}]
        workflow = self.core.start_or_get_workflow("PROJECT_DELETE", f"lifecycle:{preflight['preflight_id']}", project_id, steps)
        self._step(workflow, "PREFLIGHT_VERIFIED", lambda: {"project_id": project_id, "state": project["lifecycle_state"], "step_up": "VERIFIED"})
        payload = {"project_id": project_id, "project_name": project["name"], "repository": binding, "captured_at": now().isoformat()}
        snap = self._step(workflow, "SNAPSHOT_DISPOSITION", lambda: {"preserved": preserve_snapshot, "snapshot_hash": hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest() if preserve_snapshot else None, "mode": "METADATA_RECOVERY_SNAPSHOT" if preserve_snapshot else "OPERATOR_DECLINED"})
        self._record_disposition(project_id, workflow["workflow_id"], "RECOVERY_SNAPSHOT", "final", None, snap["mode"], snap)
        def notion_action() -> dict[str, Any]:
            if not self.notion_resolver:
                return {"status": "NOT_APPLICABLE", "reason": "NOTION_RESOLVER_UNAVAILABLE"}
            notion = self.notion_resolver()
            state = notion.projects.get(project_id)
            if not state or not state.page_id:
                return {"status": "NOT_APPLICABLE", "reason": "NO_MANAGED_PROJECT_RECORD"}
            try:
                notion.provider.get_page(state.page_id)
                notion.provider.archive_page(state.page_id)
                status = "ARCHIVED"
            except Exception as exc:
                if getattr(exc, "code", None) != "PAGE_MISSING":
                    raise
                status = "ARCHIVED_RECONCILED"
            return {"status": status, "page_id": state.page_id, "external_page_survives": True}
        notion = self._step(workflow, "NOTION_DISPOSITION", notion_action, ("NOTION_PAGE", "project-record"))
        self._record_disposition(project_id, workflow["workflow_id"], "NOTION_PAGE", "project-record", notion.get("page_id"), notion["status"], notion)
        repo = self._step(workflow, "REPOSITORY_QUARANTINED", lambda: self.core.bound_repository_lifecycle(project_id, workflow["workflow_id"], "QUARANTINE"), ("REPOSITORY_QUARANTINE", "bound-repository"))
        self._record_disposition(project_id, workflow["workflow_id"], "REPOSITORY_QUARANTINE", "bound-repository", repo.get("quarantine_path"), repo.get("status", "QUARANTINED"), repo)
        def stop() -> dict[str, Any]:
            with transaction(self.settings) as db:
                rows = db.execute("UPDATE prime_core.jobs SET status='CANCELLED',completed_at=now(),updated_at=now(),last_error='PROJECT_DELETION' WHERE project_id=%s AND status IN ('QUEUED','RUNNING','ACTION_REQUIRED') RETURNING job_id", (project_id,)).fetchall()
            return {"jobs_cancelled": len(rows), "watchers": "NO_SEPARATE_RUNTIME"}
        self._step(workflow, "ACTIVE_WORK_STOPPED", stop)
        def revoke() -> dict[str, Any]:
            with transaction(self.settings) as db:
                rows = db.execute("UPDATE prime_core.mcp_grants SET revoked_at=COALESCE(revoked_at,now()) WHERE project_id=%s RETURNING grant_id", (project_id,)).fetchall()
            return {"project_grants_revoked": len(rows), "fail_closed": True}
        self._step(workflow, "CREDENTIALS_REVOKED", revoke, ("PROJECT_CREDENTIALS", "mcp-grants"))
        self._step(workflow, "RESOURCE_DISPOSITION_RECORDED", lambda: {"repository": repo, "notion": notion, "snapshot": snap})
        result = self._step(workflow, "STATE_TRANSITIONED", lambda: self._atomic_transition(project_id, "DELETE", preflight["preflight_id"], confirmation, project["lifecycle_state"], "DELETION_PENDING", workflow["workflow_id"]))
        self.core.complete_workflow(workflow["workflow_id"], "STATE_TRANSITIONED")
        return result

    def _purge_rows(self, project_id: str, workflow_id: str) -> dict[str, Any]:
        preserve = {"projects", "audit_events", "workflows", "lifecycle_preflights", "lifecycle_operations", "lifecycle_resource_dispositions", "project_deletion_tombstones"}
        with connect(self.settings) as db:
            tables = [r["table_name"] for r in db.execute("SELECT table_name FROM information_schema.columns WHERE table_schema='prime_core' AND column_name='project_id' ORDER BY table_name").fetchall() if r["table_name"] not in preserve]
        deleted, pending = {}, tables
        for _ in range(3):
            retry = []
            for table in pending:
                if not table.replace("_", "").isalnum():
                    raise RuntimeError("unsafe purge table identifier")
                try:
                    with transaction(self.settings) as db:
                        deleted[table] = deleted.get(table, 0) + db.execute(f'DELETE FROM prime_core."{table}" WHERE project_id=%s', (project_id,)).rowcount
                except Exception:
                    retry.append(table)
            pending = retry
            if not pending:
                break
        if pending:
            raise RuntimeError("project-local purge blocked by foreign-key ordering: " + ",".join(sorted(pending)))
        with transaction(self.settings) as db:
            db.execute("DELETE FROM prime_core.workflows WHERE project_id=%s AND workflow_id<>%s", (project_id, workflow_id))
            db.execute("DELETE FROM prime_core.audit_events WHERE project_id=%s", (project_id,))
        return {"deleted_rows_by_table": deleted, "preserved": ["current purge workflow", "minimum audit tombstone", "resource disposition ledger"]}

    def _purge(self, project_id: str, preflight: dict[str, Any], project: dict[str, Any], binding: dict[str, Any] | None, confirmation: str, repository_confirmation: str | None, erase_repository: bool) -> dict[str, Any]:
        expected = f"{project['name']}::{binding['canonical_path']}" if binding else None
        if erase_repository and repository_confirmation != expected:
            raise PermissionError("exact project name and repository path confirmation is required for repository erasure")
        steps = [{"step_key": "PURGE_PLAN_VERIFIED"}, {"step_key": "HINDSIGHT_PURGED", "replay_policy": "IDEMPOTENT_EXTERNAL"}, {"step_key": "REPOSITORY_PURGED", "replay_policy": "IDEMPOTENT_EXTERNAL"}, {"step_key": "LOCAL_RESOURCES_PURGED"}, {"step_key": "MINIMAL_TOMBSTONE_WRITTEN"}, {"step_key": "PURGE_COMPLETED"}]
        workflow = self.core.start_or_get_workflow("PROJECT_PURGE", f"lifecycle:{preflight['preflight_id']}", project_id, steps)
        with connect(self.settings) as db:
            backup = self._backup_disclosure(db, project_id)
        plan = {"repository_erasure": erase_repository, "external_survival": ["Notion page", "remote Git", "external Evidence URLs", "provider logs"], "backup": backup}
        self._step(workflow, "PURGE_PLAN_VERIFIED", lambda: plan)
        def memory_action() -> dict[str, Any]:
            if not self.memory:
                raise RuntimeError("memory adapter is unavailable")
            value = self.memory.adapter_factory(project_id).delete_bank()
            if value.status == "UNAVAILABLE":
                raise RuntimeError(f"Hindsight bank deletion unavailable: {value.reason}")
            return {"status": value.status, "bank_id": f"prime-{project_id}", "payload": value.payload}
        hindsight = self._step(workflow, "HINDSIGHT_PURGED", memory_action, ("HINDSIGHT_BANK", f"prime-{project_id}"))
        self._record_disposition(project_id, workflow["workflow_id"], "HINDSIGHT_BANK", f"prime-{project_id}", None, "PURGED", hindsight)
        def repo_action() -> dict[str, Any]:
            if not erase_repository:
                return {"status": "PRESERVED_BY_OPERATOR"}
            with connect(self.settings) as db:
                row = db.execute("SELECT details FROM prime_core.lifecycle_resource_dispositions WHERE project_id=%s AND resource_type='REPOSITORY_QUARANTINE' AND resource_key='bound-repository'", (project_id,)).fetchone()
            if not row:
                raise RuntimeError("recorded repository quarantine disposition is missing")
            return self.core.bound_repository_lifecycle(project_id, row["details"]["operation_id"], "PURGE")
        repo = self._step(workflow, "REPOSITORY_PURGED", repo_action, ("REPOSITORY_PURGE", "bound-repository"))
        self._record_disposition(project_id, workflow["workflow_id"], "REPOSITORY_PURGE", "bound-repository", repo.get("quarantine_path"), repo.get("status", "PURGED"), repo)
        local = self._step(workflow, "LOCAL_RESOURCES_PURGED", lambda: self._purge_rows(project_id, workflow["workflow_id"]))
        def tombstone() -> dict[str, Any]:
            disposition = {"repository": repo, "hindsight": hindsight, "local": local, "external_survival": plan["external_survival"], "backup": backup}
            with transaction(self.settings) as db:
                db.execute("INSERT INTO prime_core.project_deletion_tombstones(project_id,project_name_hash,deleted_at,actor_id,disposition) VALUES (%s,%s,now(),'operator',%s) ON CONFLICT(project_id) DO UPDATE SET disposition=EXCLUDED.disposition,deleted_at=EXCLUDED.deleted_at", (project_id, hashlib.sha256(project["name"].encode()).hexdigest(), json.dumps(disposition)))
                db.execute("INSERT INTO prime_core.audit_events(audit_id,actor_type,actor_id,action,project_id,target_id,occurred_at,metadata) VALUES (%s,'operator','operator','project.lifecycle.purge_tombstone',NULL,%s,now(),%s)", (_id("audit"), project_id, json.dumps({"project_id": project_id, "workflow_id": workflow["workflow_id"], "disposition": "PURGED"})))
            return {"project_id": project_id, "content_retained": False, "audit_tombstone": True}
        self._step(workflow, "MINIMAL_TOMBSTONE_WRITTEN", tombstone)
        result = self._step(workflow, "PURGE_COMPLETED", lambda: self._atomic_transition(project_id, "PURGE", preflight["preflight_id"], confirmation, project["lifecycle_state"], "DELETED", workflow["workflow_id"]))
        with transaction(self.settings) as db:
            columns = {r["column_name"] for r in db.execute("SELECT column_name FROM information_schema.columns WHERE table_schema='prime_core' AND table_name='projects'").fetchall()}
            values = ["name='[PURGED]'", "connectivity_state='OFFLINE'", "freshness_state='UNKNOWN'", "work_condition='NORMAL'"]
            if "description" in columns:
                values.append("description='' ")
            if "image_url" in columns:
                values.append("image_url=NULL")
            db.execute(f"UPDATE prime_core.projects SET {','.join(values)},updated_at=now() WHERE project_id=%s", (project_id,))
        self.core.complete_workflow(workflow["workflow_id"], "PURGE_COMPLETED")
        return {**result, "disposition": plan, "orphan_resources": []}

    def execute(self, project_id: str, action: str, preflight_token: str, confirmation: str | None = None, step_up_recent: bool = False, repository_confirmation: str | None = None, include_repository_erasure: bool = False, preserve_recovery_snapshot: bool = False) -> dict[str, Any]:
        action = self._action(action)
        if not preflight_token:
            raise ValueError("valid lifecycle preflight is required")
        preflight, project, binding = self._validate(project_id, action, preflight_token, confirmation, step_up_recent)
        if action == "DELETE":
            if not self.core:
                raise RuntimeError("durable lifecycle workflow service is unavailable")
            return self._delete(project_id, preflight, project, binding, confirmation or "", preserve_recovery_snapshot)
        if action == "PURGE":
            if not self.core:
                raise RuntimeError("durable lifecycle workflow service is unavailable")
            return self._purge(project_id, preflight, project, binding, confirmation or "", repository_confirmation, include_repository_erasure)
        return self._atomic_transition(project_id, action, preflight["preflight_id"], confirmation or "", project["lifecycle_state"], ACTION_TARGETS[action])

    def transition(self, project_id: str, target: str, confirmation: str | None = None, step_up_recent: bool = False) -> dict[str, Any]:
        action = next((key for key, value in ACTION_TARGETS.items() if value == target.upper().strip()), None)
        if action is None:
            raise ValueError(f"unsupported lifecycle target: {target}")
        preflight = self.preflight(project_id, action, step_up_recent)
        return self.execute(project_id, action, preflight["preflight_token"], confirmation, step_up_recent)
