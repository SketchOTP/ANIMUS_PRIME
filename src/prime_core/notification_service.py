from __future__ import annotations

import json
from typing import Any

from .db import connect, transaction
from .service import _id, now


MATERIAL_CATEGORIES = {
    "COMPLETION_REVIEW_READY",
    "SIGNIFICANT_PROGRESS_REGRESSION",
    "PROLONGED_NODE_OUTAGE",
    "INVALID_AUTHORITY",
    "NOTION_MANAGED_CONFLICT",
    "REPOSITORY_UNBOUND",
    "GOAL_NOT_APPROVED",
    "PROJECT_STALE",
    "WORK_CONDITION",
    "NODE_DEGRADED",
    "EVIDENCE_DEGRADED",
}


class NotificationService:
    """Persist high-signal operator conditions without routine event noise."""

    def __init__(self, settings: Any):
        self.settings = settings

    def sync(self, project_id: str, conditions: list[dict[str, Any]]) -> list[dict[str, Any]]:
        material = [item for item in conditions if str(item.get("category", "")).upper() in MATERIAL_CATEGORIES]
        current_keys = {f"{str(item.get('category')).upper()}:{str(item.get('dedupe_key') or item.get('category'))}" for item in material}
        with transaction(self.settings) as db:
            rows: list[dict[str, Any]] = []
            for item in material:
                category = str(item["category"]).upper()
                dedupe_key = str(item.get("dedupe_key") or category)
                timestamp = now()
                existing = db.execute(
                    "SELECT * FROM prime_core.notifications WHERE project_id=%s AND category=%s AND dedupe_key=%s AND status='OPEN' FOR UPDATE",
                    (project_id, category, dedupe_key),
                ).fetchone()
                if existing:
                    db.execute(
                        "UPDATE prime_core.notifications SET message=%s,severity=%s,source_type=%s,source_ref=%s,last_seen_at=%s,metadata=%s WHERE notification_id=%s",
                        (str(item.get("message", "Material project condition requires review.")), str(item.get("severity", "MEDIUM")), item.get("source_type"), item.get("source_ref"), timestamp, json.dumps(item.get("metadata") or {}), existing["notification_id"]),
                    )
                    row = dict(existing)
                    row.update({"last_seen_at": timestamp, "message": item.get("message"), "severity": item.get("severity")})
                else:
                    notification_id = _id("notification")
                    db.execute(
                        "INSERT INTO prime_core.notifications(notification_id,project_id,severity,status,message,created_at,resolved_at,category,dedupe_key,source_type,source_ref,first_seen_at,last_seen_at,dismissed_at,metadata) VALUES (%s,%s,%s,'OPEN',%s,%s,NULL,%s,%s,%s,%s,%s,%s,NULL,%s)",
                        (notification_id, project_id, str(item.get("severity", "MEDIUM")), str(item.get("message", "Material project condition requires review.")), timestamp, category, dedupe_key, item.get("source_type"), item.get("source_ref"), timestamp, timestamp, json.dumps(item.get("metadata") or {})),
                    )
                    row = {"notification_id": notification_id, "project_id": project_id, "severity": item.get("severity", "MEDIUM"), "status": "OPEN", "message": item.get("message"), "created_at": timestamp, "category": category, "dedupe_key": dedupe_key, "source_type": item.get("source_type"), "source_ref": item.get("source_ref"), "first_seen_at": timestamp, "last_seen_at": timestamp, "metadata": item.get("metadata") or {}}
                rows.append(row)
            db.execute(
                "UPDATE prime_core.notifications SET status='RESOLVED',resolved_at=%s WHERE project_id=%s AND status='OPEN' AND (category || ':' || dedupe_key) <> ALL(%s)",
                (now(), project_id, list(current_keys) or ["__none__"]),
            )
            return rows

    def list_open(self, project_id: str | None = None) -> list[dict[str, Any]]:
        with connect(self.settings) as db:
            if project_id:
                rows = db.execute("SELECT * FROM prime_core.notifications WHERE project_id=%s AND status='OPEN' ORDER BY last_seen_at DESC", (project_id,))
            else:
                rows = db.execute("SELECT * FROM prime_core.notifications WHERE status='OPEN' ORDER BY last_seen_at DESC")
            return [dict(row) for row in rows.fetchall()]

    def dismiss(self, notification_id: str) -> dict[str, Any]:
        with transaction(self.settings) as db:
            row = db.execute("SELECT * FROM prime_core.notifications WHERE notification_id=%s FOR UPDATE", (notification_id,)).fetchone()
            if not row:
                raise KeyError("notification not found")
            if row["status"] == "OPEN":
                timestamp = now()
                db.execute("UPDATE prime_core.notifications SET status='DISMISSED',dismissed_at=%s,resolved_at=%s WHERE notification_id=%s", (timestamp, timestamp, notification_id))
                row = dict(row)
                row.update({"status": "DISMISSED", "dismissed_at": timestamp, "resolved_at": timestamp})
            return dict(row)
