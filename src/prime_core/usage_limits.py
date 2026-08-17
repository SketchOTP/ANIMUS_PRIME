from __future__ import annotations

from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Any, Callable
import uuid

from .db import connect, transaction

UTC = timezone.utc


def _period_start(period: str, now: datetime) -> datetime:
    if period == "MONTHLY":
        return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    return now.replace(hour=0, minute=0, second=0, microsecond=0)


def _number(value: Any) -> float:
    return float(value or 0)


class UsagePolicyService:
    """Project-scoped usage policy and enforcement boundary."""

    def __init__(self, settings: Any, clock: Callable[[], datetime] | None = None):
        self.settings = settings
        self.clock = clock or (lambda: datetime.now(UTC))

    def upsert(self, project_id: str, capability: str, period: str, max_units: float, enabled: bool = True) -> dict[str, Any]:
        with transaction(self.settings) as db:
            row = db.execute(
                "INSERT INTO prime_core.usage_limits(limit_id, project_id, capability, period, max_units, enabled) "
                "VALUES (%s,%s,%s,%s,%s,%s) "
                "ON CONFLICT (project_id, capability, period) DO UPDATE SET max_units=EXCLUDED.max_units, enabled=EXCLUDED.enabled, updated_at=now() "
                "RETURNING limit_id, project_id, capability, period, max_units, enabled, created_at, updated_at",
                ("limit_" + uuid.uuid4().hex, project_id, capability, period, max_units, enabled),
            ).fetchone()
        return dict(row)

    def disable(self, project_id: str, limit_id: str) -> bool:
        with transaction(self.settings) as db:
            result = db.execute(
                "UPDATE prime_core.usage_limits SET enabled=FALSE, updated_at=now() WHERE project_id=%s AND limit_id=%s",
                (project_id, limit_id),
            )
        return result.rowcount == 1

    def snapshot(self, project_id: str) -> list[dict[str, Any]]:
        current = self.clock()
        with connect(self.settings) as db:
            rows = db.execute(
                "SELECT limit_id, project_id, capability, period, max_units, enabled, created_at, updated_at "
                "FROM prime_core.usage_limits WHERE project_id=%s ORDER BY capability, period",
                (project_id,),
            ).fetchall()
            result: list[dict[str, Any]] = []
            for row in rows:
                item = dict(row)
                start = _period_start(item["period"], current)
                consumed = db.execute(
                    "SELECT COALESCE(SUM(units), 0) AS units FROM prime_core.usage_records "
                    "WHERE project_id=%s AND capability=%s AND occurred_at >= %s",
                    (project_id, item["capability"], start),
                ).fetchone()["units"]
                maximum = _number(item["max_units"])
                used = _number(consumed)
                item.update(
                    period_started_at=start,
                    consumed_units=used,
                    remaining_units=max(0.0, maximum - used),
                    status=("DISABLED" if not item["enabled"] else "EXCEEDED" if used >= maximum else "KNOWN"),
                )
                result.append(item)
        return result

    def check(self, project_id: str, capability: str, projected_units: float) -> dict[str, Any]:
        policies = [item for item in self.snapshot(project_id) if item["enabled"] and item["capability"] in {capability, "*"}]
        if not policies:
            return {"allowed": True, "status": "UNLIMITED", "capability": capability, "projected_units": projected_units}
        blocked = next((item for item in policies if projected_units > item["remaining_units"]), None)
        if blocked:
            return {
                "allowed": False,
                "status": "EXCEEDED",
                "reason": "project usage limit would be exceeded",
                "limit_id": blocked["limit_id"],
                "capability": blocked["capability"],
                "max_units": blocked["max_units"],
                "consumed_units": blocked["consumed_units"],
                "remaining_units": blocked["remaining_units"],
                "projected_units": projected_units,
            }
        return {"allowed": True, "status": "WITHIN_LIMIT", "capability": capability, "projected_units": projected_units, "limits": policies}
