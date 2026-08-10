from __future__ import annotations

import hashlib
from typing import Any

from .db import transaction
from .service import _id, now

ALLOWED = {
    "DRAFT": {"PROVISIONING", "DELETION_PENDING"}, "PROVISIONING": {"READY", "PAUSED", "DELETION_PENDING"},
    "READY": {"ACTIVE", "PAUSED", "DELETION_PENDING"}, "ACTIVE": {"PAUSED", "COMPLETION_REVIEW", "DELETION_PENDING"},
    "PAUSED": {"ACTIVE", "DELETION_PENDING"}, "COMPLETION_REVIEW": {"COMPLETED", "ACTIVE", "DELETION_PENDING"},
    "COMPLETED": {"ARCHIVED", "ACTIVE"}, "ARCHIVED": {"ACTIVE", "DELETION_PENDING"},
    "DELETION_PENDING": {"DELETED"}, "DELETED": set(),
}


class LifecycleService:
    def __init__(self, settings: Any):
        self.settings = settings

    def transition(self, project_id: str, target: str, confirmation: str | None = None, step_up_recent: bool = False) -> dict[str, Any]:
        with transaction(self.settings) as db:
            row = db.execute("SELECT lifecycle_state FROM prime_core.projects WHERE project_id=%s FOR UPDATE", (project_id,)).fetchone()
            if not row:
                raise KeyError("project not found")
            current = row["lifecycle_state"]
            if target not in ALLOWED.get(current, set()):
                raise ValueError(f"invalid lifecycle transition {current}->{target}")
            destructive = target in {"DELETION_PENDING", "DELETED"}
            if destructive and (confirmation != project_id or not step_up_recent):
                raise PermissionError("destructive lifecycle transition requires exact confirmation and recent step-up authentication")
            db.execute("UPDATE prime_core.projects SET lifecycle_state=%s,updated_at=now() WHERE project_id=%s", (target, project_id))
            db.execute("INSERT INTO prime_core.lifecycle_operations(operation_id,project_id,from_state,to_state,actor_type,actor_id,confirmation_hash,step_up_at,created_at) VALUES (%s,%s,%s,%s,'operator','operator',%s,%s,%s)", (_id("lifecycle"), project_id, current, target, hashlib.sha256((confirmation or "").encode()).hexdigest() if confirmation else None, now() if step_up_recent else None, now()))
            return {"project_id": project_id, "from_state": current, "to_state": target}

