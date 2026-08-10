from __future__ import annotations

import json
from typing import Any

from .db import connect, transaction
from .service import _id, now


class ReliabilityService:
    def __init__(self, settings: Any):
        self.settings = settings

    def record_backup(self, backup_type: str, locator: str, content_hash: str | None, verified: bool) -> dict[str, Any]:
        status = "VERIFIED" if verified else "STARTED"
        with transaction(self.settings) as db:
            row = db.execute("INSERT INTO prime_core.backup_records(backup_id,backup_type,locator,content_hash,status,captured_at,verified_at) VALUES (%s,%s,%s,%s,%s,%s,CASE WHEN %s THEN now() ELSE NULL END) RETURNING *", (_id("backup"), backup_type, locator, content_hash, status, now(), verified)).fetchone()
            return dict(row)

    def diagnostics(self) -> dict[str, Any]:
        with connect(self.settings) as db:
            counts = {}
            for table in ("jobs", "workflows", "events", "backup_records"):
                counts[table] = db.execute(f"SELECT count(*) AS count FROM prime_core.{table}").fetchone()["count"]
            jobs = db.execute("SELECT status,count(*) AS count FROM prime_core.jobs GROUP BY status").fetchall()
            health = {"database": "CONNECTED", "queue": "NORMAL" if sum(row["count"] for row in jobs if row["status"] in ('QUEUED','RUNNING')) < 1000 else "BACKPRESSURE"}
            return {"health": health, "counts": counts, "jobs": [dict(row) for row in jobs]}

    def sample(self, component: str, status: str, metrics: dict[str, Any]) -> None:
        with transaction(self.settings) as db:
            db.execute("INSERT INTO prime_core.diagnostic_samples(sample_id,component,status,metrics,observed_at) VALUES (%s,%s,%s,%s,%s)", (_id("diag"), component, status, json.dumps(metrics), now()))

