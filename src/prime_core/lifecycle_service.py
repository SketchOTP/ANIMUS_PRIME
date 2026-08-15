from __future__ import annotations

import hashlib
import json
import secrets
from typing import Any

from .db import connect, transaction
from .service import _id, now


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

ACTION_TARGETS = {
    "PAUSE": "PAUSED",
    "RESUME": "ACTIVE",
    "ENTER_COMPLETION_REVIEW": "COMPLETION_REVIEW",
    "CANCEL_COMPLETION_REVIEW": "ACTIVE",
    "REQUEST_COMPLETION": "COMPLETED",
    "REMOVE": "REMOVED",
    "ARCHIVE": "ARCHIVED",
    "DELETE": "DELETION_PENDING",
    "PURGE": "DELETED",
}

ACTION_DESCRIPTIONS = {
    "PAUSE": "Keep the project managed and inspectable while reducing ordinary watchers and automation.",
    "RESUME": "Return a paused, archived, or removed project to active management.",
    "ENTER_COMPLETION_REVIEW": "Open operator completion review without declaring the project complete.",
    "CANCEL_COMPLETION_REVIEW": "Cancel completion review and return the project to active management.",
    "REQUEST_COMPLETION": "Confirm an operator-reviewed project as completed.",
    "REMOVE": "Stop managing the project in the active PRIME dashboard while preserving the repository and external record.",
    "ARCHIVE": "Make the project read-only historical while preserving its repository, memory, and Notion record.",
    "DELETE": "Mark the project for destructive deletion after exact-target and step-up confirmation.",
    "PURGE": "Permanently purge locally controlled project data after a separate high-friction confirmation.",
}


class LifecycleService:
    def __init__(self, settings: Any):
        self.settings = settings

    @staticmethod
    def _state_hash(project: dict[str, Any], binding: dict[str, Any] | None) -> str:
        values = {
            "project_id": project.get("project_id"),
            "lifecycle_state": project.get("lifecycle_state"),
            "updated_at": project.get("updated_at").isoformat() if hasattr(project.get("updated_at"), "isoformat") else project.get("updated_at"),
            "repository_id": binding.get("repository_id") if binding else None,
            "canonical_path": binding.get("canonical_path") if binding else None,
            "identity_fingerprint": binding.get("identity_fingerprint") if binding else None,
        }
        return hashlib.sha256(json.dumps(values, sort_keys=True, default=str).encode()).hexdigest()

    @staticmethod
    def _action(action: str) -> str:
        normalized = action.upper().strip()
        if normalized not in ACTION_TARGETS:
            raise ValueError(f"unsupported lifecycle action: {normalized}")
        return normalized

    def _binding(self, db: Any, project_id: str) -> Any:
        return db.execute(
            "SELECT r.repository_id,r.canonical_path,r.identity_fingerprint,"
            "r.is_bare,b.node_id,n.name AS node_name,n.status AS node_status "
            "FROM prime_core.project_bindings b JOIN prime_core.repositories r ON r.repository_id=b.repository_id "
            "LEFT JOIN prime_core.nodes n ON n.node_id=b.node_id WHERE b.project_id=%s", (project_id,),
        ).fetchone()

    def preflight(self, project_id: str, action: str, step_up_recent: bool = False) -> dict[str, Any]:
        action = self._action(action)
        with connect(self.settings) as db:
            project = db.execute("SELECT * FROM prime_core.projects WHERE project_id=%s", (project_id,)).fetchone()
            binding = self._binding(db, project_id)
        if not project:
            raise KeyError("project not found")
        binding_dict = dict(binding) if binding else None
        state_hash = self._state_hash(dict(project), binding_dict)
        token = secrets.token_urlsafe(32)
        preflight_id = _id("lifecycle-preflight")
        with transaction(self.settings) as db:
            db.execute(
                "INSERT INTO prime_core.lifecycle_preflights(preflight_id,project_id,action,state_hash,token_hash,expires_at) "
                "VALUES (%s,%s,%s,%s,%s,now()+interval '5 minutes')",
                (preflight_id, project_id, action, state_hash, hashlib.sha256(token.encode()).hexdigest()),
            )
        return {
            "preflight_id": preflight_id, "preflight_token": token, "project_id": project_id,
            "action": action, "current_state": project["lifecycle_state"], "target_state": ACTION_TARGETS[action],
            "description": ACTION_DESCRIPTIONS[action], "requires_step_up": action in {"DELETE", "PURGE", "REQUEST_COMPLETION"},
            "step_up_recent": bool(step_up_recent), "expires_in_seconds": 300,
            "target": {
                "project_name": project["name"], "node_id": binding["node_id"] if binding else None,
                "node_name": binding["node_name"] if binding else None,
                "canonical_path": binding["canonical_path"] if binding else None,
                "repository_id": binding["repository_id"] if binding else None,
                "dirty_state": binding.get("dirty_state") if binding else None,
            },
            "disposition": {
                "repository": "preserved untouched" if action in {"REMOVE", "ARCHIVE"} else "quarantine/archive-first; no filesystem mutation in this request",
                "prime_metadata": "retained with auditable lifecycle state", "external_notion": "not deleted by PRIME",
            },
        }

    def execute(self, project_id: str, action: str, preflight_token: str, confirmation: str | None = None, step_up_recent: bool = False) -> dict[str, Any]:
        action = self._action(action)
        if not preflight_token:
            raise ValueError("valid lifecycle preflight is required")
        token_hash = hashlib.sha256(preflight_token.encode()).hexdigest()
        with transaction(self.settings) as db:
            preflight = db.execute(
                "SELECT * FROM prime_core.lifecycle_preflights WHERE project_id=%s AND action=%s AND token_hash=%s FOR UPDATE",
                (project_id, action, token_hash),
            ).fetchone()
            if not preflight:
                raise ValueError("lifecycle preflight is invalid")
            if preflight["used_at"] is not None:
                raise ValueError("lifecycle preflight has already been used")
            if preflight["expires_at"] <= now():
                raise ValueError("lifecycle preflight is stale")
            row = db.execute("SELECT * FROM prime_core.projects WHERE project_id=%s FOR UPDATE", (project_id,)).fetchone()
            binding = self._binding(db, project_id)
            if not row:
                raise KeyError("project not found")
            if preflight["state_hash"] != self._state_hash(dict(row), dict(binding) if binding else None):
                raise ValueError("lifecycle preflight is stale because project state changed")
            current, target = row["lifecycle_state"], ACTION_TARGETS[action]
            if target not in ALLOWED.get(current, set()):
                raise ValueError(f"invalid lifecycle transition {current}->{target}")
            if action in {"DELETE", "PURGE", "REQUEST_COMPLETION"}:
                if confirmation != project_id:
                    raise PermissionError("exact project identity confirmation is required")
                if not step_up_recent:
                    raise PermissionError("recent step-up authentication is required")
            elif confirmation != "CONFIRM":
                raise ValueError("explicit confirmation is required")
            db.execute("UPDATE prime_core.projects SET lifecycle_state=%s,updated_at=now() WHERE project_id=%s", (target, project_id))
            db.execute("UPDATE prime_core.lifecycle_preflights SET used_at=now() WHERE preflight_id=%s", (preflight["preflight_id"],))
            operation_id = _id("lifecycle")
            db.execute(
                "INSERT INTO prime_core.lifecycle_operations(operation_id,project_id,from_state,to_state,actor_type,actor_id,confirmation_hash,step_up_at,created_at) "
                "VALUES (%s,%s,%s,%s,'operator','operator',%s,%s,now())",
                (operation_id, project_id, current, target, hashlib.sha256((confirmation or "").encode()).hexdigest() if confirmation else None, now() if step_up_recent else None),
            )
            db.execute(
                "INSERT INTO prime_core.audit_events(audit_id,actor_type,actor_id,action,project_id,target_id,occurred_at,metadata) "
                "VALUES (%s,'operator','operator',%s,%s,%s,now(),%s)",
                (_id("audit"), f"project.lifecycle.{action.lower()}", project_id, operation_id, json.dumps({"from_state": current, "to_state": target})),
            )
            sequence = db.execute("SELECT COALESCE(MAX(project_sequence),0)+1 AS next_sequence FROM prime_core.events WHERE project_id=%s", (project_id,)).fetchone()["next_sequence"]
            db.execute(
                "INSERT INTO prime_core.events(event_id,project_id,event_type,occurred_at,observed_at,project_sequence,payload) VALUES (%s,%s,%s,now(),now(),%s,%s)",
                (_id("evt"), project_id, f"PROJECT_{action}", sequence, json.dumps({"from_state": current, "to_state": target, "operation_id": operation_id})),
            )
            return {"operation_id": operation_id, "project_id": project_id, "action": action, "from_state": current, "to_state": target}

    def transition(self, project_id: str, target: str, confirmation: str | None = None, step_up_recent: bool = False) -> dict[str, Any]:
        target = target.upper().strip()
        action = next((key for key, value in ACTION_TARGETS.items() if value == target), None)
        if action is None:
            raise ValueError(f"unsupported lifecycle target: {target}")
        preflight = self.preflight(project_id, action, step_up_recent)
        return self.execute(project_id, action, preflight["preflight_token"], confirmation, step_up_recent)
