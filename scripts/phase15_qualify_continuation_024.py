"""Continuation 024 native backup schedule/retry/retention qualification."""

from __future__ import annotations

import json
import secrets
import subprocess
import sys
import time
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
DB_URL = "postgresql://prime:phase1-local-only@127.0.0.1:15432/prime"
sys.path.insert(0, str(ROOT))

from src.prime_core.backup_service import BackupCoordinator
from src.prime_core.config import Settings
from src.prime_core.db import connect, migrate, transaction
from src.prime_core.reliability_service import ReliabilityService
from src.prime_core.service import CoreService
from src.prime_memory_adapter import PrimeMemoryAdapter


def _wait_core() -> None:
    for _ in range(30):
        try:
            with urlopen("http://127.0.0.1:18000/health/ready", timeout=2) as response:
                if response.status == 200:
                    return
        except Exception:
            time.sleep(1)
    raise RuntimeError("Core did not recover after restart")


def _set_schedule(settings: Settings, schedule_id: str, destination: Path) -> None:
    with transaction(settings) as db:
        db.execute(
            "UPDATE prime_core.backup_schedules SET destination=%s,next_run_at=now(),updated_at=now() WHERE schedule_id=%s",
            (str(destination), schedule_id),
        )


def _hindsight_probe() -> dict[str, object]:
    project_a = f"cont024-r044-{secrets.token_hex(4)}"
    project_b = f"cont024-r044-b-{secrets.token_hex(4)}"
    adapter_a = PrimeMemoryAdapter("http://127.0.0.1:8888", project_a)
    adapter_b = PrimeMemoryAdapter("http://127.0.0.1:8888", project_b)
    adapter_a.create_bank()
    adapter_b.create_bank()
    try:
        content = "Continuation 024 disposable Hindsight fact"
        retained = adapter_a.retain_verified(content, "doc-a")
        recalled = adapter_a.recall(content)
        isolation = adapter_b.recall(content)
        unavailable = PrimeMemoryAdapter("http://127.0.0.1:1", project_a).health()
        delete_status = adapter_a.delete_bank().status
        recreate_status = adapter_a.create_bank().status
        recovered = adapter_a.recall(content)
        return {
            "health": adapter_a.health().status,
            "retain": retained.status,
            "recall": recalled.status,
            "project_isolation": len(isolation.payload.get("results", [])) == 0,
            "unavailable": unavailable.status,
            "delete_for_restore": delete_status,
            "recreated": recreate_status,
            "recall_after_recreate": recovered.status,
        }
    finally:
        adapter_b.delete_bank()
        adapter_a.delete_bank()


def main() -> None:
    settings = Settings(database_url=DB_URL)
    migrate(settings)
    core = CoreService(settings)
    project = core.create_project("Continuation 024 backup qualification")
    run_root = Path("/tmp") / f"prime-qualification-024-{secrets.token_hex(8)}"
    run_root.mkdir(parents=True)
    off_machine = Path("/mnt/storage1tb")
    if not off_machine.is_dir() or off_machine.stat().st_dev == Path.cwd().stat().st_dev:
        raise RuntimeError("independent off-machine target is unavailable")
    destination_root = off_machine / f".animus-prime-qualification-024-{secrets.token_hex(8)}"
    destination_root.mkdir(parents=True)
    known_good = destination_root / "known-good-1.continuity"
    scheduled = destination_root / "scheduled.continuity"
    passphrase = "qualification-" + secrets.token_urlsafe(24)
    coordinator = BackupCoordinator()
    reliability = ReliabilityService(settings)

    first = coordinator.create_continuity_backup(
        settings, known_good, passphrase, project_ids=[project["project_id"]], destination_class="off-machine"
    )
    schedule = reliability.configure_backup_schedule(str(scheduled), "qualification", "operator-recovery-reference")
    subprocess.run(
        ["docker", "compose", "-f", "docker-compose.phase1.yml", "restart", "core"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    _wait_core()
    persisted = ReliabilityService(settings).due_backup_schedules()
    persisted_schedule = next(row for row in persisted if row["schedule_id"] == schedule["schedule_id"])

    queued_success = ReliabilityService(settings).enqueue_due_backup_jobs()
    scheduled_result = coordinator.create_continuity_backup(
        settings, scheduled, passphrase, project_ids=[project["project_id"]], destination_class="off-machine"
    )
    reliability.record_schedule_result(schedule["schedule_id"], True)

    blocked_parent = run_root / "unavailable-destination"
    blocked_parent.write_text("qualification destination intentionally unavailable", encoding="utf-8")
    blocked_destination = blocked_parent / "scheduled.continuity"
    _set_schedule(settings, schedule["schedule_id"], blocked_destination)
    failed_jobs = ReliabilityService(settings).enqueue_due_backup_jobs()
    failure_error = None
    try:
        coordinator.create_continuity_backup(
            settings, blocked_destination, passphrase, project_ids=[project["project_id"]], destination_class="off-machine"
        )
    except Exception as exc:
        failure_error = type(exc).__name__
        reliability.record_schedule_result(schedule["schedule_id"], False, "disposable destination unavailable")
    if failure_error is None:
        raise AssertionError("disposable destination failure did not fail closed")
    with connect(settings) as db:
        failed_schedule = db.execute("SELECT * FROM prime_core.backup_schedules WHERE schedule_id=%s", (schedule["schedule_id"],)).fetchone()
        known_good_row = db.execute("SELECT status,locator FROM prime_core.backup_records WHERE backup_id=%s", (first["backup_id"],)).fetchone()
    if failed_schedule["last_status"] != "FAILED" or failed_schedule["retry_count"] < 1:
        raise AssertionError("failed schedule did not persist retry state")
    if known_good_row["status"] != "VERIFIED" or not Path(known_good_row["locator"]).is_file():
        raise AssertionError("previous known-good backup was not preserved")

    blocked_parent.unlink()
    _set_schedule(settings, schedule["schedule_id"], scheduled)
    recovered_jobs = ReliabilityService(settings).enqueue_due_backup_jobs()
    recovered = coordinator.create_continuity_backup(
        settings, scheduled, passphrase, project_ids=[project["project_id"]], destination_class="off-machine"
    )
    reliability.record_schedule_result(schedule["schedule_id"], True)
    with connect(settings) as db:
        recovered_schedule = db.execute("SELECT last_status,retry_count FROM prime_core.backup_schedules WHERE schedule_id=%s", (schedule["schedule_id"],)).fetchone()
    if recovered_schedule["last_status"] != "VERIFIED" or recovered_schedule["retry_count"] != 0:
        raise AssertionError("schedule did not recover to VERIFIED")

    generations = [recovered]
    for number in range(2, 5):
        generations.append(
            coordinator.create_continuity_backup(
                settings,
                destination_root / f"generation-{number}.continuity",
                passphrase,
                project_ids=[project["project_id"]],
                destination_class="off-machine",
            )
        )
    retention = ReliabilityService(settings).retention_plan("continuation-024", max_items=3)
    removed = ReliabilityService(settings).prune_backup_files(retention)
    latest = generations[-1]
    if not Path(latest["locator"]).is_file() or latest["backup_id"] not in retention["keep"]:
        raise AssertionError("retention did not preserve latest known-good backup")
    hindsight = _hindsight_probe()

    print(json.dumps({
        "status": "PASSED",
        "project": "disposable",
        "schedule_persisted_across_core_restart": persisted_schedule["schedule_id"] == schedule["schedule_id"],
        "initial_scheduled_backup": scheduled_result["status"],
        "queued_success_jobs": len(queued_success),
        "failure_state": failed_schedule["last_status"],
        "failure_retry_count": failed_schedule["retry_count"],
        "failed_jobs": len(failed_jobs),
        "known_good_preserved_after_failure": True,
        "retry_jobs": len(recovered_jobs),
        "recovered_backup": recovered["status"],
        "health_after_recovery": recovered_schedule["last_status"],
        "retention_generations": len(generations) + 2,
        "retention_removed_disposable_generations": len(removed),
        "latest_known_good_retained": True,
        "negative_coverage": "wrong-key/tamper/truncation/credential-exclusion covered by focused tests",
        "hindsight": hindsight,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
