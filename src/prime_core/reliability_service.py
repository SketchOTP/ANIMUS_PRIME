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
        root = root or Path.cwd()
        warning_bytes = int(os.getenv("PRIME_DISK_WARNING_BYTES", str(2 * 1024 * 1024 * 1024)))
        critical_bytes = int(os.getenv("PRIME_DISK_CRITICAL_BYTES", str(512 * 1024 * 1024)))
        free = shutil.disk_usage(root).free
        with connect(self.settings) as db:
            queue_rows = db.execute("SELECT status,count(*) AS count FROM prime_core.jobs GROUP BY status").fetchall()
            queued = sum(int(row["count"]) for row in queue_rows if row["status"] in ("QUEUED", "RUNNING"))
        queue_limit = int(os.getenv("PRIME_QUEUE_LIMIT", "1000"))
        disk = "CRITICAL" if free < critical_bytes else ("WARNING" if free < warning_bytes else "HEALTHY")
        return {
            "queue": {"queued": queued, "limit": queue_limit, "status": "BACKPRESSURE" if queued >= queue_limit else "NORMAL"},
            "disk": {"free_bytes": free, "status": disk, "derived_work_allowed": disk == "HEALTHY"},
            "canonical_writes_prioritized": True,
            "protected_data_auto_purge": False,
        }

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
        """Prune disposable projections only; canonical history is never auto-purged."""
        with transaction(self.settings) as db:
            removed = {}
            for table, timestamp_column, keep in (("brain_snapshots", "created_at", keep_brain), ("notion_projection_revisions", "observed_at", keep_notion), ("time_lens_checkpoints", "created_at", keep_time_lens)):
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
            return {"health": health, "counts": counts, "jobs": [dict(row) for row in jobs], "capacity": pressure}

    def sample(self, component: str, status: str, metrics: dict[str, Any]) -> None:
        with transaction(self.settings) as db:
            db.execute("INSERT INTO prime_core.diagnostic_samples(sample_id,component,status,metrics,observed_at) VALUES (%s,%s,%s,%s,%s)", (_id("diag"), component, status, json.dumps(metrics), now()))
