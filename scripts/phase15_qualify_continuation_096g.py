from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import time
from pathlib import Path

from src.prime_core.db import connect, migrate
from src.prime_core.indexer import RepositoryIndexer
from src.prime_core.reliability_service import ReliabilityService
from src.prime_core.service import CoreService, _id, now


def git(root: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True, text=True, timeout=120).stdout.strip()


def prepare_repository(root: Path, file_count: int = 6000) -> dict[str, object]:
    allowed_parent = Path("/mnt/storage1tb/prime-qualification/continuation-096g").resolve()
    root = root.resolve()
    if root.parent != allowed_parent:
        raise ValueError("qualification repository must use the approved external-storage parent")
    marker = root / "V1_QUALIFICATION_FIXTURE"
    if root.exists() and not marker.is_file():
        raise ValueError("existing repository is not marked as a qualification fixture")
    root.mkdir(parents=True, exist_ok=True)
    marker.write_text("ANIMUS PRIME Continuation 096G representative capacity fixture\n", encoding="utf-8")
    if not (root / ".git").is_dir():
        git(root, "init", "-b", "main")
        git(root, "config", "user.name", "ANIMUS PRIME Qualification")
        git(root, "config", "user.email", "qualification@localhost")
    existing = sum(1 for path in (root / "corpus").rglob("*.txt")) if (root / "corpus").is_dir() else 0
    if existing < file_count:
        for number in range(file_count):
            directory = root / "corpus" / f"group-{number % 120:03d}"
            directory.mkdir(parents=True, exist_ok=True)
            (directory / f"artifact-{number:05d}.txt").write_text(
                f"representative capacity artifact {number}\n"
                f"stable retrieval marker r045-large-repository-{number}\n"
                "ANIMUS PRIME preserves authority, continuity, provenance, and bounded backpressure.\n",
                encoding="utf-8",
            )
    git(root, "add", ".")
    if git(root, "status", "--porcelain"):
        git(root, "commit", "-m", "qualification: representative large repository baseline")
    return {"path": str(root), "files": file_count, "revision": git(root, "rev-parse", "HEAD")}


def main() -> None:
    database_url = os.environ["PRIME_PHASE1_DB_URL"]
    root = Path(os.environ.get("PRIME_096G_FIXTURE_ROOT", "/mnt/storage1tb/prime-qualification/continuation-096g/representative-repo"))
    from src.prime_core.config import Settings

    settings = Settings(database_url=database_url)
    migrate(settings)
    core = CoreService(settings)
    reliability = ReliabilityService(settings)
    repository = prepare_repository(root)
    project = core.create_project("V1_QUALIFICATION_FIXTURE_096G_LARGE_REPOSITORY")
    node = core.register_node(
        "node-096g-atlas-external",
        "Atlas external-storage qualification Node",
        "linux",
        hashlib.sha256(str(root.parent).encode()).hexdigest(),
        [str(root.parent)],
        {"qualification_fixture": True, "transport": "ATLAS_NATIVE"},
    )
    binding = core.bind_repository(project["project_id"], node["node_id"], hashlib.sha256(str(root).encode()).hexdigest(), str(root))
    reliability.configure_capacity_policy("GLOBAL", queue_limit=64, running_limit=4, coalesce_window_ms=5000)
    reliability.configure_capacity_policy(f"PROJECT:{project['project_id']}", queue_limit=24, running_limit=2, coalesce_window_ms=5000)
    for retention_class in (
        "normalized_events", "audit_security_logs", "repository_index_cache", "brain_layout_cache",
        "model_run_traces", "notification_history", "terminal_job_payloads", "retained_source_ledger",
    ):
        reliability.configure_capacity_policy(f"RETENTION:{retention_class}", max_items=1000, retention_days=90)

    indexer = RepositoryIndexer(core)
    index_started = time.monotonic()
    indexed = indexer.build(project["project_id"])
    index_seconds = time.monotonic() - index_started
    search_started = time.monotonic()
    search = indexer.search(project["project_id"], "r045 large repository 4321")
    search_seconds = time.monotonic() - search_started
    assert indexed["files_indexed"] >= 6001
    assert any("artifact-04321.txt" in item["relative_path"] for item in search)

    changed = [f"corpus/group-{number % 120:03d}/artifact-{number:05d}.txt" for number in range(100)]
    old_revision = repository["revision"]
    for number, relative in enumerate(changed):
        path = root / relative
        path.write_text(path.read_text(encoding="utf-8") + f"current revision update {number}\n", encoding="utf-8")
    git(root, "add", *changed)
    git(root, "commit", "-m", "qualification: current revision update")
    current_revision = git(root, "rev-parse", "HEAD")
    stale_before_current = None
    try:
        indexer.observe_incremental(project["project_id"], changed, str(old_revision))
    except ValueError as exc:
        stale_before_current = str(exc)
    assert stale_before_current == "OBSERVATION_REVISION_MISMATCH"
    current_observation = indexer.observe_incremental(project["project_id"], changed, current_revision)
    stale_after_current = None
    try:
        indexer.observe_incremental(project["project_id"], changed, str(old_revision))
    except ValueError as exc:
        stale_after_current = str(exc)
    assert stale_after_current == "OBSERVATION_REVISION_MISMATCH"
    with connect(settings) as db:
        canonical_revision = db.execute("SELECT canonical_revision FROM prime_core.project_bindings WHERE project_id=%s", (project["project_id"],)).fetchone()["canonical_revision"]
    assert canonical_revision == current_revision

    coalesced_ids = {
        core.create_coalesced_job("REINDEX", {"revision": current_revision}, project["project_id"], current_revision)["job_id"]
        for _ in range(1000)
    }
    assert len(coalesced_ids) == 1
    accepted = 0
    refused = 0
    for number in range(100):
        try:
            core.create_job("PARSER", {"number": number}, f"096g-distinct-{project['project_id']}-{number}", project["project_id"])
            accepted += 1
        except ValueError as exc:
            assert "backpressure" in str(exc)
            refused += 1
    assert accepted <= 23 and refused > 0
    first = core.claim_job()
    second = core.claim_job()
    third = core.claim_job()
    assert first and second and first["project_id"] == second["project_id"] == project["project_id"]
    assert third is None
    core.complete_job(first["job_id"], True)
    recovered = core.claim_job()
    assert recovered and recovered["project_id"] == project["project_id"]
    for job in (second, recovered):
        core.complete_job(job["job_id"], True)
    while True:
        job = core.claim_job()
        if not job:
            break
        core.complete_job(job["job_id"], True)
    drained = reliability.capacity_status(root)
    assert drained["queue"]["queued"] == 0

    with connect(settings) as db:
        for number in range(4):
            db.execute(
                "INSERT INTO prime_core.brain_snapshots(brain_snapshot_id,project_id,source_revision,graph,created_at) VALUES (%s,%s,%s,'{}',%s)",
                (_id("brain"), project["project_id"], f"brain-{number}", now()),
            )
            db.execute(
                "INSERT INTO prime_core.time_lens_checkpoints(checkpoint_id,project_id,as_of,reconstruction_status,source_set,created_at) VALUES (%s,%s,%s,'EXACT','[]',%s)",
                (_id("checkpoint"), project["project_id"], f"as-of-{number}", now()),
            )
        db.commit()
    before_retention = reliability.retention_inventory(project["project_id"])
    retention_plan = reliability.retention_impact_plan(project["project_id"])
    assert all(item["policy"] for item in retention_plan["classes"].values())
    retention_removed = reliability.prune_derived(project["project_id"], keep_brain=1, keep_notion=1, keep_time_lens=1)
    after_retention = reliability.retention_inventory(project["project_id"])
    assert retention_removed["brain_snapshots"] == 3
    assert retention_removed["time_lens_checkpoints"] == 0
    assert before_retention["counts"]["time_lens"] == after_retention["counts"]["time_lens"]

    free = shutil.disk_usage(root).free
    os.environ["PRIME_CAPACITY_ROOT"] = str(root)
    os.environ["PRIME_DISK_CRITICAL_BYTES"] = str(free + 1)
    critical = reliability.capacity_status(root)
    disk_refusal = None
    try:
        core.create_job("REINDEX", {}, f"096g-critical-{project['project_id']}", project["project_id"])
    except ValueError as exc:
        disk_refusal = str(exc)
    assert critical["disk"]["status"] == "CRITICAL" and disk_refusal and "disk capacity" in disk_refusal
    canonical = core.create_job("BACKUP_CONTINUITY", {}, f"096g-critical-canonical-{project['project_id']}", project["project_id"])
    os.environ["PRIME_DISK_CRITICAL_BYTES"] = "1"
    recovered_disk = reliability.capacity_status(root)
    assert recovered_disk["disk"]["status"] != "CRITICAL"

    result = {
        "status": "VERIFIED",
        "project_id": project["project_id"],
        "node_id": node["node_id"],
        "repository_id": binding["repository_id"],
        "repository": repository,
        "index": {**indexed, "seconds": round(index_seconds, 3)},
        "search": {"seconds": round(search_seconds, 3), "result_count": len(search), "target_found": True},
        "revision": {"old": old_revision, "current": current_revision, "stale_before": stale_before_current, "stale_after": stale_after_current, "canonical_after": canonical_revision, "files_incremental": current_observation["files_indexed"]},
        "queue": {"coalesced_inputs": 1000, "coalesced_jobs": len(coalesced_ids), "distinct_accepted": accepted, "distinct_refused": refused, "project_running_limit": 2, "drained": drained["queue"]},
        "retention": {"before": before_retention, "plan": retention_plan, "removed": retention_removed, "after": after_retention},
        "disk": {"simulated": True, "critical": critical["disk"], "derived_refusal": disk_refusal, "canonical_job_status": canonical["status"], "recovered": recovered_disk["disk"]},
        "hindsight": {"health": recovered_disk["storage_growth"]["hindsight_health"], "automatic_memory_deletion": False},
        "external_storage": {"device": root.stat().st_dev, "root": str(root)},
    }
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
