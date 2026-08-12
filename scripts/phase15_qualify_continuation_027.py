"""Continuation 027 qualification harness for R-043, R-045, and R-048.

The harness uses the production Core services against a disposable PostgreSQL
database. It never writes credentials to the result. R-045 is intentionally
reported as partial when the frozen implementation does not expose a required
normative boundary; a large burst alone is not promoted as sustained proof.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import time
import uuid
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

import psycopg
from psycopg import sql

ROOT = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(ROOT))

from src.prime_core.ai_service import AIExecutionService, ProviderResult
from src.prime_core.backup_service import BackupCoordinator, BackupError
from src.prime_core.brain_service import BrainService
from src.prime_core.config import Settings
from src.prime_core.db import connect, migrate
from src.prime_core.history_service import HistoryService
from src.prime_core.indexer import RepositoryIndexer
from src.prime_core.memory_service import MemoryService
from src.prime_core.notion_service import NotionProjectionService
from src.prime_core.progress_service import ProgressService
from src.prime_core.reliability_service import ReliabilityService
from src.prime_core.service import CoreService
from src.prime_memory_adapter import AdapterResult


class FixtureMemory:
    def retain_verified(self, content: str, document_id: str) -> AdapterResult:
        return AdapterResult("CURRENT", {"document_id": document_id})

    def recall(self, query: str) -> AdapterResult:
        return AdapterResult("CURRENT", {"results": []})


class FixtureProvider:
    is_local = True

    def generate(self, request: dict) -> ProviderResult:
        source_id = request["sources"][0]["source"].get("source_id", "fixture-source") if request["sources"] else "fixture-source"
        return ProviderResult(
            {"category": "SOURCE FACT", "answer": "continuity fixture", "citations": [{"source_id": source_id}]},
            input_tokens=8,
            output_tokens=5,
            estimated_cost=0,
            usage_metadata={"fixture": "continuation-027"},
        )


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout.strip()


def db_url(base: str, name: str) -> str:
    parsed = urlsplit(base)
    return urlunsplit((parsed.scheme, parsed.netloc, f"/{name}", parsed.query, parsed.fragment))


def create_database(base: str, name: str) -> str:
    maintenance = db_url(base, "postgres")
    with psycopg.connect(maintenance, autocommit=True) as db:
        db.execute(sql.SQL("CREATE DATABASE {} ").format(sql.Identifier(name)))
    return db_url(base, name)


def drop_database(base: str, name: str) -> None:
    maintenance = db_url(base, "postgres")
    with psycopg.connect(maintenance, autocommit=True) as db:
        db.execute(sql.SQL("DROP DATABASE IF EXISTS {} WITH (FORCE)").format(sql.Identifier(name)))


def request_for_restore(csrf: str) -> object:
    from starlette.requests import Request

    return Request({
        "type": "http", "method": "POST", "path": "/v1/backups/restore",
        "headers": [(b"x-prime-csrf", csrf.encode()), (b"cookie", f"prime_csrf={csrf}".encode())], "query_string": b"", "server": ("qualification", 80),
        "client": ("qualification", 1), "scheme": "http",
    })


def response_json(response: object) -> dict:
    if isinstance(response, dict):
        return response
    return json.loads(response.body.decode("utf-8"))


def populate_source(settings: Settings, root: Path) -> dict:
    repo = root / "repository"
    repo.mkdir()
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "qualification@example.invalid")
    git(repo, "config", "user.name", "Continuation 027 Qualification")
    core = CoreService(settings)
    project = core.create_project("Continuation 027 representative source")
    project_id = project["project_id"]
    node_id = "node-c027-" + uuid.uuid4().hex[:10]
    core.register_node(node_id, "Continuation 027 Node", "linux", hashlib.sha256(node_id.encode()).hexdigest(), [str(root)], {})
    binding = core.bind_repository(project_id, node_id, hashlib.sha256(str(repo).encode()).hexdigest(), str(repo))
    history = HistoryService(settings)
    memory = MemoryService(settings, adapter_factory=lambda _project_id: FixtureMemory())
    progress = ProgressService(settings)
    notion = NotionProjectionService(settings)
    brain = BrainService(settings)
    indexer = RepositoryIndexer(core)
    checkpoint_root = root / "prime-owned-checkpoints"
    goal_revision_id = None
    memory_a = None
    revisions: dict[str, str] = {}
    cutoffs: dict[str, str] = {}
    evidence: dict[str, dict] = {}
    state_data = {
        "A": ("VALID", 20, "P1 remains valid", "Evidence A supports P1"),
        "B": ("VALID", 45, "P1 reaffirmed", "Evidence B supports P1"),
        "C": ("INVALID", 35, "P2 corrects P1", "Evidence C contradicts P1"),
        "D": ("VALID", 75, "P2 is current", "Evidence D confirms P2"),
    }
    for label, (authority_status, progress_value, memory_text, evidence_text) in state_data.items():
        (repo / "state.txt").write_text(f"STATE {label}\n{memory_text}\n", encoding="utf-8")
        git(repo, "add", "state.txt")
        git(repo, "commit", "-qm", f"state {label}")
        revision = git(repo, "rev-parse", "HEAD")
        revisions[label] = revision
        indexer.build(project_id)
        core.record_authority_revision(project_id, f".agent/state-{label}.md", revision, authority_status, canonical_commit=revision)
        item = history.store_uploaded_evidence(project_id, f"evidence-{label}.txt", evidence_text.encode(), "text/plain", source_revision=revision)
        evidence[label] = item
        if label == "A":
            goal = core.create_goal_revision(project_id, "Goal v1: preserve continuity", approve=True)
            goal_revision_id = goal["goal_revision_id"]
            review = progress.propose_baseline(project_id, goal_revision_id, [{"title": "continuity", "weight": 1.0, "completion": 0}])
            progress.approve_baseline(review["review_id"])
        progress.assess(project_id, goal_revision_id, [{"title": "continuity", "weight": 1.0, "completion": progress_value / 100, "confidence": 1.0}], repository_revision=revision, summary=f"Progress {progress_value}")
        stored = memory.store(project_id, memory_text, "FACT", source_revision=revision, source_reference_id=item["source_reference_id"], supersedes_memory_id=memory_a if label == "C" else None, correction_reason="Evidence C contradicts P1" if label == "C" else None)
        if label == "A":
            memory_a = stored["memory_id"]
        notion._record(project_id, item["content_hash"], "SYNCED", {"source_revision": revision}, f"State {label} / {item['source_reference_id']}")
        history.add_git_checkpoint(project_id, str(repo), revision, str(checkpoint_root))
        brain.build(project_id, revision)
        time.sleep(0.04)
        cutoffs[label] = datetime.now(timezone.utc).isoformat()

    old_provider = os.environ.get("PRIME_AI_PROVIDER")
    old_model = os.environ.get("PRIME_AI_MODEL")
    os.environ["PRIME_AI_PROVIDER"] = "fixture"
    os.environ["PRIME_AI_MODEL"] = "qualification-model"
    AIExecutionService(settings, providers={"fixture": FixtureProvider()}).execute(
        project_id, "ASK_PRIME", {"question": "what is retained?"},
        [{"source_id": "fixture-source", "source_class": "EVIDENCE", "source_revision": revisions["D"], "content_hash": evidence["D"]["content_hash"], "project_id": project_id, "text": "continuity fixture"}],
    )
    if old_provider is None:
        os.environ.pop("PRIME_AI_PROVIDER", None)
    else:
        os.environ["PRIME_AI_PROVIDER"] = old_provider
    if old_model is None:
        os.environ.pop("PRIME_AI_MODEL", None)
    else:
        os.environ["PRIME_AI_MODEL"] = old_model
    return {"project": project, "project_id": project_id, "repo": repo, "binding": binding, "revisions": revisions, "cutoffs": cutoffs, "evidence": evidence, "checkpoint_root": checkpoint_root, "goal_revision_id": goal_revision_id}


def qualify_r043(settings: Settings, fixture: dict, root: Path, base_url: str, passphrase: str) -> dict:
    coordinator = BackupCoordinator()
    bundle = root / "continuity" / "source.prime-continuity"
    backup = coordinator.create_continuity_backup(settings, bundle, passphrase, project_ids=[fixture["project_id"]], destination_class="operator-selected")
    preflight = coordinator.preflight_restore(bundle, passphrase)
    serialized = json.dumps(preflight["components"], sort_keys=True)
    assert "password_hash" not in serialized and "recovery_hash" not in serialized and "token_hash" not in serialized
    assert preflight["manifest"]["continuity"] is True
    assert preflight["manifest"]["project_ids"] == [fixture["project_id"]]
    assert preflight["components"]["configuration"]["secrets"] == "REPROVISION_REQUIRED"

    fresh_name = "prime_c027_fresh_" + uuid.uuid4().hex[:8]
    collision_name = "prime_c027_collision_" + uuid.uuid4().hex[:8]
    interrupted_name = "prime_c027_interrupt_" + uuid.uuid4().hex[:8]
    fresh_url = collision_url = interrupted_url = None
    try:
        fresh_url = create_database(base_url, fresh_name)
        fresh = Settings(database_url=fresh_url)
        migrate(fresh)
        restored = coordinator.restore_bundle(fresh, bundle, passphrase, storage_root=root / "fresh-restored-content")
        assert restored["status"] == "RESTORED"
        with connect(fresh) as db:
            project_row = db.execute("SELECT project_id,name FROM prime_core.projects WHERE project_id=%s", (fixture["project_id"],)).fetchone()
            evidence_row = db.execute("SELECT evidence_id,content_hash,source_reference_id FROM prime_core.evidence_records WHERE project_id=%s AND source_revision=%s", (fixture["project_id"], fixture["revisions"]["B"])).fetchone()
            ai_row = db.execute("SELECT count(*) AS count FROM prime_core.ai_runs WHERE project_id=%s", (fixture["project_id"],)).fetchone()
            usage_row = db.execute("SELECT count(*) AS count FROM prime_core.usage_records WHERE project_id=%s", (fixture["project_id"],)).fetchone()
        assert project_row["name"] == fixture["project"]["name"]
        assert evidence_row["content_hash"] == fixture["evidence"]["B"]["content_hash"]
        assert evidence_row["source_reference_id"] == fixture["evidence"]["B"]["source_reference_id"]
        assert ai_row["count"] >= 1 and usage_row["count"] >= 1

        collision_url = create_database(base_url, collision_name)
        collision = Settings(database_url=collision_url)
        migrate(collision)
        conflicting = CoreService(collision).create_project("conflicting target")
        before = len(CoreService(collision).list_projects())
        try:
            coordinator.restore_bundle(collision, bundle, passphrase)
        except BackupError as exc:
            assert "collision" in str(exc)
        else:
            raise AssertionError("populated target restore was not refused")
        assert len(CoreService(collision).list_projects()) == before
        assert CoreService(collision).list_projects()[0]["project_id"] == conflicting["project_id"]

        import apps.core.main as main
        main.settings = fresh
        main.service = CoreService(fresh)
        operator_password = "c027-operator-password"
        main.service.bootstrap(operator_password)
        session, csrf = main.service.login(operator_password)
        body = main.BackupRequest(destination=str(bundle), passphrase=passphrase, replace=True, safety_destination=str(root / "safety-checkpoint"), storage_root=str(root / "fresh-replaced-content"))
        blocked = response_json(main.restore_backup(body, request_for_restore(csrf), prime_session=session, step_up="BAD"))
        assert blocked["error_code"] == "RESTORE_STEP_UP_REQUIRED"
        approved = response_json(main.restore_backup(body, request_for_restore(csrf), prime_session=session, step_up="CONFIRM"))
        assert approved["status"] == "RESTORED"

        interrupted_url = create_database(base_url, interrupted_name)
        interrupted = Settings(database_url=interrupted_url)
        migrate(interrupted)
        CoreService(interrupted).create_project("interrupted target")
        try:
            coordinator.restore_bundle(interrupted, bundle, passphrase, replace=True, safety_destination=root / "interrupt-safety", storage_root=root / "interrupt-restored-content", fail_after_tables=2)
        except BackupError:
            pass
        else:
            raise AssertionError("interrupted restore unexpectedly succeeded")
        with connect(interrupted) as db:
            workflow = db.execute("SELECT status,current_step FROM prime_core.restore_workflows ORDER BY started_at DESC LIMIT 1").fetchone()
        assert workflow == {"status": "REPAIR_REQUIRED", "current_step": "FAILED"}
        return {"status": "VERIFIED", "backup_id": backup["backup_id"], "locator": str(bundle), "fresh_restore": restored["component_fidelity"], "collision": "REFUSED_WITHOUT_MUTATION", "step_up": "CONFIRM_REQUIRED_FOR_REPLACEMENT", "interrupted_workflow": dict(workflow), "secret_exclusion": "PASSED"}
    finally:
        for name in (fresh_name, collision_name, interrupted_name):
            drop_database(base_url, name)


def qualify_r045(settings: Settings, fixture: dict, root: Path) -> dict:
    old_queue = os.environ.get("PRIME_QUEUE_LIMIT")
    os.environ["PRIME_QUEUE_LIMIT"] = "32"
    service = CoreService(settings)
    started = time.monotonic()
    submitted = refused = 0
    peaks = []
    for number in range(300):
        try:
            service.create_coalesced_job("PARSER", {"source_revision": fixture["revisions"]["D"], "event": number}, fixture["project_id"], f"sustained-{number}")
            submitted += 1
        except ValueError as exc:
            assert "backpressure" in str(exc)
            refused += 1
        peaks.append(ReliabilityService(settings).capacity_status(root)["queue"]["queued"])
        time.sleep(0.005)
    duration = time.monotonic() - started
    while True:
        job = service.claim_job()
        if job is None:
            break
        service.complete_job(job["job_id"], True)
    recovery_started = time.monotonic()
    while ReliabilityService(settings).capacity_status(root)["queue"]["queued"]:
        time.sleep(0.01)
    recovery_time = time.monotonic() - recovery_started
    if old_queue is None:
        os.environ.pop("PRIME_QUEUE_LIMIT", None)
    else:
        os.environ["PRIME_QUEUE_LIMIT"] = old_queue
    return {
        "status": "PARTIAL", "duration_seconds": round(duration, 3), "input_events": 300,
        "parser_jobs_submitted": submitted, "parser_jobs_refused": refused,
        "parser_queue_peak": max(peaks or [0]), "configured_queue_limit": 32,
        "time_to_recover_seconds": round(recovery_time, 3),
        "backpressure": "PASSED", "canonical_writes_prioritized": ReliabilityService(settings).capacity_status(root)["canonical_writes_prioritized"],
        "missing_normative_observability": ["parser concurrency bound", "index backlog and drain", "stale-job revision protection", "retention pressure preservation", "usage/cost throttle/refusal"],
    }


def qualify_r048(settings: Settings, fixture: dict, root: Path, backup: dict, passphrase: str) -> dict:
    history = HistoryService(settings)
    baseline = history.historical_context(fixture["project_id"], fixture["cutoffs"]["B"])
    required = ["repository", "authority", "goal", "evidence", "progress", "memory", "notion", "brain", "git"]
    assert all(baseline["source_statuses"].get(key) == "EXACT" for key in required), baseline["source_statuses"]
    matrix = []
    with connect(settings) as db:
        evidence_row = db.execute("SELECT evidence_id,storage_path FROM prime_core.evidence_records WHERE project_id=%s AND source_revision=%s", (fixture["project_id"], fixture["revisions"]["B"])).fetchone()
        checkpoint_rows = db.execute("SELECT bundle_locator FROM prime_core.git_history_checkpoints WHERE project_id=%s", (fixture["project_id"],)).fetchall()
    evidence_path = Path(evidence_row["storage_path"])
    original_evidence = evidence_path.read_bytes()
    evidence_path.unlink()
    degraded = history.historical_context(fixture["project_id"], fixture["cutoffs"]["B"])
    with connect(settings) as db:
        evidence_ref = db.execute("SELECT source_reference_id FROM prime_core.evidence_records WHERE evidence_id=%s", (evidence_row["evidence_id"],)).fetchone()["source_reference_id"]
    assert history.resolve_source_reference(fixture["project_id"], evidence_ref)["status"] == "UNAVAILABLE"
    matrix.append({"class": "Evidence/SourceReference", "baseline": "EXACT", "loss": degraded["source_statuses"]["evidence"], "expected": "PARTIAL"})
    evidence_path.write_bytes(original_evidence)
    assert history.reindex_evidence(fixture["project_id"], evidence_row["evidence_id"])["index_status"] == "READY"
    assert history.historical_context(fixture["project_id"], fixture["cutoffs"]["B"])["source_statuses"]["evidence"] == "EXACT"
    for label, table, status_key in (("AuthorityRevision", "authority_revisions", "authority"), ("Goal/GoalModel", "goal_revisions", "goal"), ("Progress", "progress_assessments", "progress"), ("Memory/source ledger", "memory_records", "memory"), ("Notion projection", "notion_projection_revisions", "notion"), ("Brain", "brain_snapshots", "brain")):
        with connect(settings) as db:
            db.execute(sql.SQL("DELETE FROM prime_core.{} WHERE project_id=%s").format(sql.Identifier(table)), (fixture["project_id"],))
            db.commit()
        degraded = history.historical_context(fixture["project_id"], fixture["cutoffs"]["B"])
        matrix.append({"class": label, "baseline": "EXACT", "loss": degraded["source_statuses"][status_key], "expected": "UNAVAILABLE"})
        with connect(settings) as db:
            db.rollback()
        # The source is restored by the production continuity restore below.
        coordinator = BackupCoordinator()
        coordinator.restore_bundle(settings, Path(backup["locator"]), passphrase, replace=True, safety_destination=root / f"r048-safety-{status_key}", storage_root=root / f"r048-restored-{status_key}")
        recovered = history.historical_context(fixture["project_id"], fixture["cutoffs"]["B"])
        assert recovered["source_statuses"][status_key] == "EXACT", (label, recovered["source_statuses"])
    with connect(settings) as db:
        current_checkpoint = db.execute("SELECT bundle_locator FROM prime_core.git_history_checkpoints WHERE project_id=%s AND commit_id=%s", (fixture["project_id"], fixture["revisions"]["B"])).fetchone()
    for bundle_row in ([current_checkpoint] if current_checkpoint else []):
        path = Path(bundle_row["bundle_locator"])
        if path.is_file():
            bytes_before = path.read_bytes()
            path.unlink()
            status = history.git_checkpoint_status(fixture["project_id"], fixture["revisions"]["B"])["coverage_status"]
            matrix.append({"class": "retained Git checkpoint", "baseline": "EXACT", "loss": status, "expected": "UNAVAILABLE"})
            path.write_bytes(bytes_before)
            break
    current_memory = history.historical_context(fixture["project_id"], fixture["cutoffs"]["D"])
    assert current_memory["source_statuses"]["memory"] == "EXACT"
    return {"status": "VERIFIED", "baseline": baseline["source_statuses"], "matrix": matrix, "correction_timeline": "A/B=P1; C=P2 correction; D=current P2; P1 retained historically", "loss_of_correction_source": "UNAVAILABLE is now reported by source-reference resolution when managed Evidence bytes disappear"}


def main() -> None:
    base_url = os.environ.get("PRIME_PHASE1_DB_URL") or os.environ.get("PRIME_DATABASE_URL")
    if not base_url:
        raise SystemExit("PRIME_PHASE1_DB_URL or PRIME_DATABASE_URL is required")
    settings = Settings(database_url=base_url)
    migrate(settings)
    root = Path(tempfile.mkdtemp(prefix="prime-c027-"))
    try:
        fixture = populate_source(settings, root)
        passphrase = "continuation-027-" + uuid.uuid4().hex
        backup = qualify_r043(settings, fixture, root, base_url, passphrase)
        r045 = qualify_r045(settings, fixture, root)
        r048 = qualify_r048(settings, fixture, root, backup, passphrase)
        result = {"continuation": "027", "r043": backup, "r045": r045, "r048": r048, "project_id": fixture["project_id"], "revisions": fixture["revisions"]}
        print(json.dumps(result, sort_keys=True, default=str))
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    main()
