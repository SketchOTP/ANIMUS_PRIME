from __future__ import annotations

import json
import os
import shutil
from pathlib import Path
from typing import Any

from .db import connect, transaction
from .service import _id, now


class ReliabilityService:
    def __init__(self, settings: Any):
        self.settings = settings

    def configure_capacity_policy(
        self,
        scope: str,
        *,
        queue_limit: int | None = None,
        running_limit: int | None = None,
        coalesce_window_ms: int = 1000,
        max_items: int | None = None,
        max_bytes: int | None = None,
        retention_days: int | None = None,
    ) -> dict[str, Any]:
        if scope != "GLOBAL" and not (scope.startswith("PROJECT:") or scope.startswith("RETENTION:")):
            raise ValueError("unsupported capacity policy scope")
        for value in (queue_limit, running_limit, coalesce_window_ms, max_items, max_bytes, retention_days):
            if value is not None and value < 1:
                raise ValueError("capacity policy values must be positive")
        with transaction(self.settings) as db:
            row = db.execute(
                "INSERT INTO prime_core.capacity_policies(policy_id,scope,max_bytes,max_items,retention_days,queue_limit,running_limit,coalesce_window_ms,updated_at) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,now()) ON CONFLICT (scope) DO UPDATE SET "
                "max_bytes=EXCLUDED.max_bytes,max_items=EXCLUDED.max_items,retention_days=EXCLUDED.retention_days,"
                "queue_limit=EXCLUDED.queue_limit,running_limit=EXCLUDED.running_limit,coalesce_window_ms=EXCLUDED.coalesce_window_ms,updated_at=now() RETURNING *",
                (_id("capacity"), scope, max_bytes, max_items, retention_days, queue_limit, running_limit, coalesce_window_ms),
            ).fetchone()
        return dict(row)

    def record_backup(self, backup_type: str, locator: str, content_hash: str | None, verified: bool) -> dict[str, Any]:
        status = "VERIFIED" if verified else "STARTED"
        with transaction(self.settings) as db:
            row = db.execute("INSERT INTO prime_core.backup_records(backup_id,backup_type,locator,content_hash,status,captured_at,verified_at) VALUES (%s,%s,%s,%s,%s,%s,CASE WHEN %s THEN now() ELSE NULL END) RETURNING *", (_id("backup"), backup_type, locator, content_hash, status, now(), verified)).fetchone()
            return dict(row)

    def record_continuity_backup(self, result: dict[str, Any], project_ids: list[str]) -> dict[str, Any]:
        manifest = result["manifest"]
        with transaction(self.settings) as db:
            row = db.execute(
                "INSERT INTO prime_core.backup_records(backup_id,backup_type,locator,content_hash,status,captured_at,verified_at,"
                "prime_version,spec_revision,schema_revision,source_high_water_mark,project_ids,component_inventory,component_versions,"
                "encryption_version,destination_class,manifest,metadata) VALUES (%s,'CONTINUITY',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
                "ON CONFLICT (backup_id) DO UPDATE SET status=EXCLUDED.status,verified_at=EXCLUDED.verified_at RETURNING *",
                (
                    manifest["backup_id"], result["locator"], result["content_hash"], "VERIFIED", manifest["created_at"],
                    manifest["created_at"], manifest.get("prime_version"), manifest.get("spec_revision"), manifest.get("schema_revision"),
                    manifest.get("source_high_water_mark"), json.dumps(project_ids), json.dumps(manifest.get("component_inventory", [])),
                    json.dumps(manifest.get("component_versions", {})), manifest.get("encryption_version"), manifest.get("destination_class"),
                    json.dumps(manifest), json.dumps({"recovery": "clean-install restore supported", "secrets": "reprovision required"}),
                ),
            ).fetchone()
            return dict(row)

    def configure_backup_schedule(self, destination: str, cadence: str, key_reference: str) -> dict[str, Any]:
        if not key_reference or any(token in key_reference.lower() for token in ("pass", "secret", "token")):
            raise ValueError("backup schedule must reference external recovery material, not contain a secret")
        with transaction(self.settings) as db:
            row = db.execute(
                "INSERT INTO prime_core.backup_schedules(schedule_id,destination,cadence,key_reference,next_run_at,idempotency_prefix,updated_at) "
                "VALUES (%s,%s,%s,%s,now(),%s,now()) RETURNING *",
                (_id("schedule"), destination, cadence, key_reference, _id("backup-schedule")),
            ).fetchone()
            return dict(row)

    def due_backup_schedules(self) -> list[dict[str, Any]]:
        with connect(self.settings) as db:
            return [dict(row) for row in db.execute("SELECT * FROM prime_core.backup_schedules WHERE enabled AND (next_run_at IS NULL OR next_run_at<=now()) ORDER BY next_run_at").fetchall()]

    def enqueue_due_backup_jobs(self) -> list[dict[str, Any]]:
        """Turn missed/due schedules into durable idempotent jobs without storing keys."""
        from .service import CoreService

        jobs: list[dict[str, Any]] = []
        for schedule in self.due_backup_schedules():
            key = f"{schedule['idempotency_prefix']}:{schedule['next_run_at']}"
            job = CoreService(self.settings).create_job(
                "BACKUP_CONTINUITY",
                {"destination": schedule["destination"], "key_reference": schedule["key_reference"], "schedule_id": schedule["schedule_id"]},
                key,
            )
            jobs.append(job)
            with transaction(self.settings) as db:
                db.execute("UPDATE prime_core.backup_schedules SET last_started_at=now(),last_status='QUEUED',updated_at=now() WHERE schedule_id=%s", (schedule["schedule_id"],))
        return jobs

    def record_schedule_result(self, schedule_id: str, success: bool, error: str | None = None) -> None:
        with transaction(self.settings) as db:
            db.execute(
                "UPDATE prime_core.backup_schedules SET last_completed_at=CASE WHEN %s THEN now() ELSE last_completed_at END,"
                "last_error=%s,last_status=%s,retry_count=CASE WHEN %s THEN 0 ELSE retry_count+1 END,"
                "next_run_at=now()+CASE WHEN %s THEN interval '1 hour' ELSE make_interval(mins => LEAST(60, (2 ^ retry_count)::integer)) END,updated_at=now() WHERE schedule_id=%s",
                (success, error, "VERIFIED" if success else "FAILED", success, success, schedule_id),
            )

    def capacity_status(self, root: Path | None = None) -> dict[str, Any]:
        root = root or Path(os.getenv("PRIME_CAPACITY_ROOT", "."))
        warning_bytes = int(os.getenv("PRIME_DISK_WARNING_BYTES", str(2 * 1024 * 1024 * 1024)))
        critical_bytes = int(os.getenv("PRIME_DISK_CRITICAL_BYTES", str(512 * 1024 * 1024)))
        free = shutil.disk_usage(root).free
        with connect(self.settings) as db:
            queue_rows = db.execute("SELECT status,count(*) AS count FROM prime_core.jobs GROUP BY status").fetchall()
            queued = sum(int(row["count"]) for row in queue_rows if row["status"] in ("QUEUED", "RUNNING"))
            global_row = db.execute("SELECT queue_limit,running_limit,coalesce_window_ms FROM prime_core.capacity_policies WHERE scope='GLOBAL'").fetchone()
            project_rows = db.execute(
                "SELECT project_id,status,count(*) AS count FROM prime_core.jobs WHERE project_id IS NOT NULL AND status IN ('QUEUED','RUNNING') GROUP BY project_id,status ORDER BY project_id,status"
            ).fetchall()
            memory_records = int(db.execute("SELECT count(*) AS count FROM prime_core.memory_records WHERE status NOT IN ('TOMBSTONED','SUPERSEDED')").fetchone()["count"])
            database_bytes = int(db.execute("SELECT pg_database_size(current_database()) AS bytes").fetchone()["bytes"])
        queue_limit = int(global_row["queue_limit"] if global_row and global_row["queue_limit"] is not None else os.getenv("PRIME_QUEUE_LIMIT", "1000"))
        disk = "CRITICAL" if free < critical_bytes else ("WARNING" if free < warning_bytes else "HEALTHY")
        per_project: dict[str, dict[str, int]] = {}
        for row in project_rows:
            per_project.setdefault(row["project_id"], {"queued": 0, "running": 0})[row["status"].lower()] = int(row["count"])
        try:
            from src.prime_memory_adapter import PrimeMemoryAdapter
            hindsight = PrimeMemoryAdapter(self.settings.hindsight_base_url, "system-capacity", min(self.settings.hindsight_timeout_seconds, 2.0)).health().status
        except Exception:
            hindsight = "UNAVAILABLE"
        return {
            "queue": {"queued": queued, "limit": queue_limit, "status": "BACKPRESSURE" if queued >= queue_limit else "NORMAL", "per_project": per_project},
            "policy": {"global": dict(global_row) if global_row else {"queue_limit": queue_limit, "running_limit": int(os.getenv("PRIME_PROJECT_RUNNING_LIMIT", "2")), "coalesce_window_ms": int(os.getenv("PRIME_EVENT_COALESCE_WINDOW_MS", "1000"))}},
            "disk": {"root": str(root.resolve()), "free_bytes": free, "status": disk, "derived_work_allowed": disk != "CRITICAL"},
            "storage_growth": {"database_bytes": database_bytes, "durable_memory_records": memory_records, "hindsight_health": hindsight},
            "canonical_writes_prioritized": True,
            "protected_data_auto_purge": False,
        }

    def retention_impact_plan(self, project_id: str) -> dict[str, Any]:
        """Report policy and reference consequences without deleting protected history."""
        inventory = self.retention_inventory(project_id)
        classes = {
            "normalized_events": {"table": "events", "protected": True, "reason": "Time Lens and durable workflow history"},
            "audit_security_logs": {"table": "audit_events", "protected": True, "reason": "audit requirement"},
            "repository_index_cache": {"table": "repository_files", "protected": False, "reason": "rebuildable from current repository"},
            "brain_layout_cache": {"table": "brain_snapshots", "protected": False, "reason": "rebuildable derived layout"},
            "model_run_traces": {"table": "ai_runs", "protected": True, "reason": "provider/source provenance"},
            "notification_history": {"table": "notifications", "protected": True, "reason": "operator/audit history"},
            "terminal_job_payloads": {"table": "jobs", "protected": True, "reason": "workflow/dead-letter recovery"},
            "retained_source_ledger": {"table": "source_references", "protected": True, "reason": "citation and reconstruction coverage"},
        }
        with connect(self.settings) as db:
            policies = {row["scope"]: dict(row) for row in db.execute("SELECT * FROM prime_core.capacity_policies WHERE scope LIKE 'RETENTION:%'").fetchall()}
            for name, item in classes.items():
                predicate = "project_id=%s"
                if name == "terminal_job_payloads":
                    predicate += " AND status IN ('SUCCEEDED','CANCELLED','DEAD_LETTER')"
                item["count"] = int(db.execute(f"SELECT count(*) AS count FROM prime_core.{item['table']} WHERE {predicate}", (project_id,)).fetchone()["count"])
                item["policy"] = policies.get(f"RETENTION:{name}")
                item["automatic_action"] = "PRUNE_REBUILDABLE" if not item["protected"] else "REFUSE_WITH_IMPACT_DISCLOSURE"
        return {"project_id": project_id, "inventory": inventory, "classes": classes, "protected_pruning_requires_explicit_loss_acceptance": True}

    def retention_plan(self, scope: str, *, retention_days: int = 30, max_items: int = 10) -> dict[str, Any]:
        if retention_days < 1 or max_items < 1:
            raise ValueError("retention policy must preserve at least one item")
        with connect(self.settings) as db:
            backups = [dict(row) for row in db.execute(
                "SELECT backup_id,locator,status,captured_at,verified_at FROM prime_core.backup_records "
                "WHERE backup_type='CONTINUITY' ORDER BY captured_at DESC"
            ).fetchall()]
        keep = set()
        latest_verified = next((row for row in backups if row["status"] == "VERIFIED"), None)
        if latest_verified:
            keep.add(latest_verified["backup_id"])
        keep.update(row["backup_id"] for row in backups[:max_items])
        candidates = [row for row in backups if row["backup_id"] not in keep]
        return {"scope": scope, "retention_days": retention_days, "max_items": max_items, "keep": sorted(keep), "candidates": candidates, "protected": "latest verified backup and referenced canonical data"}

    def prune_backup_files(self, plan: dict[str, Any]) -> list[str]:
        removed: list[str] = []
        for row in plan.get("candidates", []):
            path = Path(row["locator"])
            if path.is_file():
                path.unlink()
                removed.append(str(path))
        return removed

    def retention_inventory(self, project_id: str | None = None) -> dict[str, Any]:
        predicate = "WHERE project_id=%s" if project_id else ""
        params = (project_id,) if project_id else ()
        with connect(self.settings) as db:
            counts = {}
            for name, table in (
                ("evidence", "evidence_records"), ("historical", "historical_revisions"),
                ("git_checkpoints", "git_history_checkpoints"), ("time_lens", "time_lens_checkpoints"),
                ("brain_cache", "brain_snapshots"), ("notion_projection", "notion_projection_revisions"),
            ):
                counts[name] = db.execute(f"SELECT count(*) AS count FROM prime_core.{table} {predicate}", params).fetchone()["count"]
        return {
            "protected": ["projects", "goal_models", "progress_assessments", "corrections", "source_references", "historical_revisions"],
            "retention_pinned": ["git_checkpoints", "time_lens", "notion_projection"],
            "derived_rebuildable": ["brain_cache", "repository_index", "evidence_parser_index"],
            "counts": counts,
        }

    def prune_derived(self, project_id: str, *, keep_brain: int = 1, keep_notion: int = 10, keep_time_lens: int = 10) -> dict[str, int]:
        """Prune only rebuildable projections; retained Notion and Time Lens history is pinned."""
        with transaction(self.settings) as db:
            removed = {"notion_projection_revisions": 0, "time_lens_checkpoints": 0}
            for table, timestamp_column, keep in (("brain_snapshots", "created_at", keep_brain),):
                rows = db.execute(f"SELECT ctid FROM prime_core.{table} WHERE project_id=%s ORDER BY {timestamp_column} DESC OFFSET %s", (project_id, keep)).fetchall()
                count = 0
                for row in rows:
                    db.execute(f"DELETE FROM prime_core.{table} WHERE ctid=%s", (row["ctid"],))
                    count += 1
                removed[table] = count
            return removed

    def release_git_checkpoint(self, project_id: str, checkpoint_id: str, *, force: bool = False) -> dict[str, Any]:
        """Reference-aware Git cleanup downgrades coverage before releasing bytes."""
        with transaction(self.settings) as db:
            row = db.execute("SELECT * FROM prime_core.git_history_checkpoints WHERE project_id=%s AND checkpoint_id=%s FOR UPDATE", (project_id, checkpoint_id)).fetchone()
            if not row:
                raise KeyError("Git checkpoint not found")
            dependency = db.execute("SELECT 1 FROM prime_core.historical_revisions WHERE project_id=%s AND artifact_type='GIT_CHECKPOINT' AND artifact_id=%s LIMIT 1", (project_id, checkpoint_id)).fetchone()
            if dependency and not force:
                raise ValueError("Git checkpoint is provenance-pinned and cannot be released")
            updated = db.execute("UPDATE prime_core.git_history_checkpoints SET retained=FALSE,coverage_status='PARTIAL' WHERE project_id=%s AND checkpoint_id=%s RETURNING *", (project_id, checkpoint_id)).fetchone()
            return dict(updated)

    def diagnostics(self) -> dict[str, Any]:
        with connect(self.settings) as db:
            counts = {}
            for table in ("jobs", "workflows", "events", "backup_records"):
                counts[table] = db.execute(f"SELECT count(*) AS count FROM prime_core.{table}").fetchone()["count"]
            jobs = db.execute("SELECT status,count(*) AS count FROM prime_core.jobs GROUP BY status").fetchall()
            pressure = self.capacity_status()
            health = {"database": "CONNECTED", "queue": pressure["queue"]["status"], "disk": pressure["disk"]["status"]}
            latest = db.execute(
                "SELECT backup_id,status,captured_at,verified_at,encryption_version,destination_class FROM prime_core.backup_records WHERE backup_type='CONTINUITY' ORDER BY captured_at DESC LIMIT 20"
            ).fetchall()
            latest_verified = next((row for row in latest if row["status"] == "VERIFIED"), None)
            return {
                "health": health,
                "counts": counts,
                "jobs": [dict(row) for row in jobs],
                "capacity": pressure,
                "backup_status": "HEALTHY" if latest_verified else "REQUIRES_ACTION",
                "backup_detail": "Latest verified continuity backup is recorded." if latest_verified else "No verified continuity backup is currently recorded.",
                "latest_verified_backup": latest_verified["backup_id"] if latest_verified else "NONE",
                "backup_encryption": latest_verified["encryption_version"] if latest_verified else "UNKNOWN",
            }

    def sample(self, component: str, status: str, metrics: dict[str, Any]) -> None:
        with transaction(self.settings) as db:
            db.execute("INSERT INTO prime_core.diagnostic_samples(sample_id,component,status,metrics,observed_at) VALUES (%s,%s,%s,%s,%s)", (_id("diag"), component, status, json.dumps(metrics), now()))
