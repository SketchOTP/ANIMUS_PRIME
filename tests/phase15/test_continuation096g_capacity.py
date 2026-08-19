from __future__ import annotations

import os
import shutil
from pathlib import Path

import pytest


pytestmark = pytest.mark.skipif(not os.getenv("PRIME_PHASE1_DB_URL"), reason="set PRIME_PHASE1_DB_URL for capacity integration")


def _settings(monkeypatch):
    monkeypatch.setenv("PRIME_DATABASE_URL", os.environ["PRIME_PHASE1_DB_URL"])
    from src.prime_core.config import Settings

    return Settings(database_url=os.environ["PRIME_PHASE1_DB_URL"])


def test_project_queue_and_running_limits_are_durable(monkeypatch):
    from src.prime_core.db import migrate
    from src.prime_core.reliability_service import ReliabilityService
    from src.prime_core.service import CoreService

    settings = _settings(monkeypatch)
    migrate(settings)
    core = CoreService(settings)
    reliability = ReliabilityService(settings)
    project_a = core.create_project("096G project A")
    project_b = core.create_project("096G project B")
    reliability.configure_capacity_policy("GLOBAL", queue_limit=20, running_limit=4, coalesce_window_ms=1000)
    reliability.configure_capacity_policy(f"PROJECT:{project_a['project_id']}", queue_limit=3, running_limit=1, coalesce_window_ms=1000)
    for number in range(3):
        core.create_job("PARSER", {"number": number}, f"096g-a-{project_a['project_id']}-{number}", project_a["project_id"])
    with pytest.raises(ValueError, match="project queue"):
        core.create_job("PARSER", {}, f"096g-a-refused-{project_a['project_id']}", project_a["project_id"])
    core.create_job("PARSER", {}, f"096g-b-0-{project_b['project_id']}", project_b["project_id"])
    first = core.claim_job()
    assert first and first["project_id"] == project_a["project_id"]
    second = core.claim_job()
    assert second and second["project_id"] == project_b["project_id"]
    status = reliability.capacity_status()
    assert status["queue"]["per_project"][project_a["project_id"]]["running"] == 1


def test_simulated_critical_disk_refuses_only_derived_work(monkeypatch, tmp_path):
    from src.prime_core.db import migrate
    from src.prime_core.service import CoreService

    settings = _settings(monkeypatch)
    migrate(settings)
    core = CoreService(settings)
    project = core.create_project("096G disk pressure")
    monkeypatch.setenv("PRIME_CAPACITY_ROOT", str(tmp_path))
    monkeypatch.setenv("PRIME_DISK_CRITICAL_BYTES", str(shutil.disk_usage(tmp_path).free + 1))
    with pytest.raises(ValueError, match="disk capacity is critical"):
        core.create_job("REINDEX", {}, f"096g-disk-derived-{project['project_id']}", project["project_id"])
    assert core.create_job("BACKUP_CONTINUITY", {}, f"096g-disk-canonical-{project['project_id']}", project["project_id"])["status"] == "QUEUED"


def test_retention_plan_protects_time_lens_and_source_history(monkeypatch):
    from src.prime_core.db import connect, migrate
    from src.prime_core.reliability_service import ReliabilityService
    from src.prime_core.service import CoreService, _id, now

    settings = _settings(monkeypatch)
    migrate(settings)
    core = CoreService(settings)
    project = core.create_project("096G retention")
    with connect(settings) as db:
        for number in range(3):
            db.execute(
                "INSERT INTO prime_core.time_lens_checkpoints(checkpoint_id,project_id,as_of,reconstruction_status,source_set,created_at) VALUES (%s,%s,%s,'EXACT','[]',%s)",
                (_id("checkpoint"), project["project_id"], f"t-{number}", now()),
            )
            db.execute(
                "INSERT INTO prime_core.brain_snapshots(brain_snapshot_id,project_id,source_revision,graph,created_at) VALUES (%s,%s,%s,'{}',%s)",
                (_id("brain"), project["project_id"], f"r-{number}", now()),
            )
        db.commit()
    reliability = ReliabilityService(settings)
    before = reliability.retention_inventory(project["project_id"])
    removed = reliability.prune_derived(project["project_id"], keep_brain=1, keep_notion=1, keep_time_lens=1)
    after = reliability.retention_inventory(project["project_id"])
    assert removed["brain_snapshots"] == 2
    assert removed["time_lens_checkpoints"] == 0
    assert before["counts"]["time_lens"] == after["counts"]["time_lens"] == 3
    plan = reliability.retention_impact_plan(project["project_id"])
    assert plan["classes"]["retained_source_ledger"]["automatic_action"] == "REFUSE_WITH_IMPACT_DISCLOSURE"
    assert plan["classes"]["repository_index_cache"]["automatic_action"] == "PRUNE_REBUILDABLE"


def test_source_identity_coalescing_is_not_time_bucketed(monkeypatch):
    from src.prime_core.db import migrate
    from src.prime_core.service import CoreService

    settings = _settings(monkeypatch)
    migrate(settings)
    core = CoreService(settings)
    project = core.create_project("096G durable coalescing")
    jobs = {
        core.create_coalesced_job("REINDEX", {"revision": "same"}, project["project_id"], "revision-same")["job_id"]
        for _ in range(50)
    }
    events = {
        core.emit_coalesced_event("REPOSITORY_CHANGED", {"revision": "same"}, project["project_id"], "revision-same")["event_id"]
        for _ in range(50)
    }
    assert len(jobs) == 1
    assert len(events) == 1


def test_saturated_project_does_not_starve_another_project(monkeypatch):
    from src.prime_core.db import migrate
    from src.prime_core.reliability_service import ReliabilityService
    from src.prime_core.service import CoreService

    settings = _settings(monkeypatch)
    migrate(settings)
    core = CoreService(settings)
    reliability = ReliabilityService(settings)
    while True:
        existing = core.claim_job()
        if not existing:
            break
        core.complete_job(existing["job_id"], True)
    project_a = core.create_project("096G fairness A")
    project_b = core.create_project("096G fairness B")
    reliability.configure_capacity_policy("GLOBAL", queue_limit=200, running_limit=4)
    reliability.configure_capacity_policy(f"PROJECT:{project_a['project_id']}", queue_limit=150, running_limit=1)
    for number in range(120):
        core.create_job("PARSER", {}, f"fair-a-{project_a['project_id']}-{number}", project_a["project_id"])
    core.create_job("PARSER", {}, f"fair-b-{project_b['project_id']}", project_b["project_id"])
    assert core.claim_job()["project_id"] == project_a["project_id"]
    assert core.claim_job()["project_id"] == project_b["project_id"]


def test_capacity_policy_has_authenticated_product_route():
    source = (Path(__file__).parents[2] / "apps" / "core" / "main.py").read_text(encoding="utf-8")
    assert '@app.put("/v1/system/capacity/policies")' in source
    assert "require_session(request, prime_session)" in source
    assert "configure_capacity_policy(" in source
