from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

import pytest


pytestmark = pytest.mark.skipif(
    not os.getenv("PRIME_PHASE1_DB_URL"),
    reason="set PRIME_PHASE1_DB_URL for requirement qualification integration",
)


def _git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _settings(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("PRIME_DATABASE_URL", os.environ["PRIME_PHASE1_DB_URL"])
    from src.prime_core.config import Settings

    return Settings()


def test_r049_retained_checkpoint_survives_rewrite_gc_and_time_lens(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    from src.prime_core.brain_service import BrainService
    from src.prime_core.db import connect, migrate
    from src.prime_core.history_service import HistoryService
    from src.prime_core.indexer import RepositoryIndexer
    from src.prime_core.service import CoreService

    settings = _settings(monkeypatch)
    migrate(settings)
    repo = tmp_path / "managed-repository"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "qualification@example.invalid")
    _git(repo, "config", "user.name", "Qualification")
    (repo / "state.txt").write_text("state A\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-qm", "state A")
    state_a = _git(repo, "rev-parse", "HEAD")
    branch = _git(repo, "branch", "--show-current")

    core = CoreService(settings)
    project = core.create_project("R-049 retained checkpoint")
    project_id = project["project_id"]
    node_id = "node-qualification-r049"
    core.register_node(node_id, "Qualification Node", "linux", hashlib.sha256(node_id.encode()).hexdigest(), [str(tmp_path)], {})
    core.bind_repository(project_id, node_id, hashlib.sha256(str(repo).encode()).hexdigest(), str(repo))
    indexed = RepositoryIndexer(core).build(project_id)
    assert indexed["source_revision"] == state_a

    history_root = tmp_path / "prime-owned-history"
    service = HistoryService(settings)
    checkpoint = service.add_git_checkpoint(project_id, str(repo), state_a, str(history_root))
    with connect(settings) as db:
        source = db.execute(
            "SELECT source_reference_id FROM prime_core.git_history_checkpoints WHERE project_id=%s AND commit_id=%s",
            (project_id, state_a),
        ).fetchone()
    assert source and source["source_reference_id"] == checkpoint["source_reference_id"]

    # Create later history, then remove every ordinary repository ref to A.
    for label in ("state B", "state C", "state D"):
        (repo / "state.txt").write_text(f"{label}\n", encoding="utf-8")
        _git(repo, "add", "state.txt")
        _git(repo, "commit", "-qm", label)
    _git(repo, "update-ref", "-d", f"refs/heads/{branch}")
    _git(repo, "reflog", "expire", "--expire=now", "--all")
    _git(repo, "gc", "--prune=now")

    ordinary_history = subprocess.run(
        ["git", "-C", str(repo), "cat-file", "-e", f"{state_a}^{{commit}}"],
        capture_output=True,
        text=True,
    )
    assert ordinary_history.returncode != 0

    restarted = HistoryService(settings)
    retained = restarted.git_checkpoint_status(project_id, state_a)
    assert retained["coverage_status"] == "EXACT"
    citation = restarted.resolve_source_reference(
        project_id, checkpoint["source_reference_id"], current_revision=state_a
    )
    assert citation["status"] == "EXACT"
    assert Path(retained["bundle_locator"]).resolve().parent != repo.resolve()
    bundle_path = Path(retained["bundle_locator"])
    bundle_bytes = bundle_path.read_bytes()
    bundle_path.unlink()
    unavailable_citation = restarted.resolve_source_reference(
        project_id, checkpoint["source_reference_id"], current_revision=state_a
    )
    assert unavailable_citation["status"] == "UNAVAILABLE"
    bundle_path.write_bytes(bundle_bytes)
    assert restarted.resolve_source_reference(
        project_id, checkpoint["source_reference_id"], current_revision=state_a
    )["status"] == "EXACT"

    lens = restarted.time_lens(project_id, state_a)
    assert lens["source_statuses"]["repository"] == "EXACT"
    assert lens["source_statuses"]["git"] == "EXACT"
    assert lens["repository_reconstruction"]["source"] == "PRIME_GIT_CHECKPOINT"
    assert BrainService(settings).build_historical(project_id, state_a)["availability"] == "EXACT"

    missing = restarted.git_checkpoint_status(project_id, "not-retained-checkpoint")
    assert missing["coverage_status"] == "UNAVAILABLE"
    degraded = restarted.time_lens(project_id, "not-retained-checkpoint")
    assert degraded["reconstruction_status"] in {"PARTIAL", "UNAVAILABLE"}
    assert degraded["source_statuses"]["git"] == "UNAVAILABLE"


def test_r046_r047_real_evidence_files_retract_prune_reindex_and_isolate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    from src.prime_core.db import connect, migrate
    from src.prime_core.history_service import HistoryService
    from src.prime_core.service import CoreService

    settings = _settings(monkeypatch)
    migrate(settings)
    core = CoreService(settings)
    project_a = core.create_project("R-046 Evidence A")
    project_b = core.create_project("R-046 Evidence B")
    service = HistoryService(settings)

    evidence = service.store_uploaded_evidence(
        project_a["project_id"],
        "report.txt",
        b"State A managed evidence\n",
        "text/plain",
        source_revision="commit-A",
    )
    retrieved = service.retrieve_evidence(project_a["project_id"], evidence["evidence_id"])
    assert retrieved["availability"] == "EXACT"
    assert retrieved["content"] == b"State A managed evidence\n"
    citation = service.cite_evidence(project_a["project_id"], evidence["evidence_id"])
    assert service.resolve_source_reference(
        project_a["project_id"], citation["source_reference_id"], current_revision="commit-A"
    )["status"] == "EXACT"
    with pytest.raises(KeyError):
        service.retrieve_evidence(project_b["project_id"], evidence["evidence_id"])

    changed = service.resolve_source_reference(
        project_a["project_id"], citation["source_reference_id"], current_revision="commit-B", current_content_hash="different"
    )
    assert changed["status"] == "HISTORICAL"
    retracted = service.retract_evidence(project_a["project_id"], evidence["evidence_id"], "State A retracted")
    assert retracted["parser_status"] == "RETRACTED"
    retracted_citation = service.resolve_source_reference(
        project_a["project_id"], citation["source_reference_id"], current_revision="commit-A"
    )
    assert retracted_citation["status"] == "HISTORICAL"
    assert retracted_citation["later_retracted"] is True

    purged = service.store_uploaded_evidence(
        project_a["project_id"], "pruned.txt", b"pruned historical source\n", "text/plain", source_revision="commit-A"
    )
    purged_citation = service.cite_evidence(project_a["project_id"], purged["evidence_id"])
    service.purge_evidence(project_a["project_id"], purged["evidence_id"], force=True)
    unavailable = service.resolve_source_reference(
        project_a["project_id"], purged_citation["source_reference_id"], current_revision="commit-A"
    )
    assert unavailable["status"] == "UNAVAILABLE"

    monkeypatch.setenv("PRIME_EVIDENCE_PARSER_AVAILABLE", "0")
    degraded = service.store_uploaded_evidence(
        project_a["project_id"], "degraded.txt", b"parser recovery fixture\n", "text/plain", source_revision="commit-C"
    )
    assert degraded["parser_status"] == "UNSUPPORTED"
    monkeypatch.setenv("PRIME_EVIDENCE_PARSER_AVAILABLE", "1")
    recovered = service.reindex_evidence(project_a["project_id"], degraded["evidence_id"])
    assert recovered["parser_status"] == "INDEXED"
    assert recovered["content_hash"] == hashlib.sha256(b"parser recovery fixture\n").hexdigest()


def test_r046_complete_file_matrix_and_node_reference_boundaries(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    from src.prime_core.db import connect, migrate
    from src.prime_core.history_service import HistoryService
    from src.prime_core.service import CoreService

    monkeypatch.setenv("PRIME_EVIDENCE_ROOT", str(tmp_path / "managed-evidence"))
    settings = _settings(monkeypatch)
    migrate(settings)
    project = CoreService(settings).create_project("R-046 complete matrix")
    other = CoreService(settings).create_project("R-046 isolation target")
    service = HistoryService(settings)

    with pytest.raises(ValueError):
        service.store_uploaded_evidence(project["project_id"], "active.html", b"<html><script>alert(1)</script></html>", "application/octet-stream")
    with pytest.raises(ValueError):
        service.store_uploaded_evidence(project["project_id"], "active.svg", b"<svg onload=alert(1) />", "image/svg+xml")
    with pytest.raises(ValueError):
        service.store_uploaded_evidence(project["project_id"], "wrong.txt", b"plain text", "application/json")
    with pytest.raises(ValueError):
        service.store_uploaded_evidence(project["project_id"], "archive.zip", b"PK\x03\x04", "application/zip")
    with pytest.raises(ValueError):
        service.store_uploaded_evidence(project["project_id"], "oversize.bin", b"x" * (50 * 1024 * 1024 + 1), "application/octet-stream")

    bounded = service.store_uploaded_evidence(
        project["project_id"], "bounded.txt", b"x" * 210_000, "text/plain", source_revision="commit-A"
    )
    assert bounded["parser_status"] == "INDEXED"
    assert len(bounded["extracted_text"]) == 200_000
    with pytest.raises(KeyError):
        service.retrieve_evidence(other["project_id"], bounded["evidence_id"])

    allowed = tmp_path / "node-root"
    allowed.mkdir()
    node_file = allowed / "node.txt"
    node_file.write_text("node Evidence", encoding="utf-8")
    monkeypatch.setenv("PRIME_NODE_ALLOWED_ROOTS", str(allowed))
    with pytest.raises(ValueError):
        service.record_evidence(project["project_id"], "NODE_PATH", str(tmp_path / "outside.txt"))
    node_evidence = service.record_evidence(project["project_id"], "NODE_PATH", str(node_file), source_revision="commit-A")
    assert service.retrieve_evidence(project["project_id"], node_evidence["evidence_id"])["availability"] == "EXACT"
    node_file.unlink()
    assert service.retrieve_evidence(project["project_id"], node_evidence["evidence_id"])["availability"] == "UNAVAILABLE"
    compressed = service.store_uploaded_evidence(project["project_id"], "compressed.bin", b"PK\x03\x04compressed", "application/octet-stream")
    assert compressed["parser_status"] == "UNSUPPORTED"


def test_r047_product_search_ask_and_documentation_preserve_evidence_citation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    from src.prime_core.db import migrate
    from src.prime_core.history_service import HistoryService
    from src.prime_core.intelligence_service import IntelligenceService
    from src.prime_core.notion_service import NotionProjectionService
    from src.prime_core.service import CoreService

    monkeypatch.setenv("PRIME_EVIDENCE_ROOT", str(tmp_path / "managed-evidence"))
    settings = _settings(monkeypatch)
    migrate(settings)
    project = CoreService(settings).create_project("R-047 product citations")
    service = HistoryService(settings)
    evidence = service.store_uploaded_evidence(
        project["project_id"], "source.txt", b"E1 durable source content", "text/plain", source_revision="commit-A"
    )
    citation = service.cite_evidence(project["project_id"], evidence["evidence_id"])
    intelligence = IntelligenceService(settings)
    search = intelligence.search(project["project_id"], "durable source")
    assert search["groups"]["Evidence"][0]["evidence_id"] == evidence["evidence_id"]
    assert search["groups"]["Evidence"][0]["source_reference_id"] == citation["source_reference_id"]

    class QualifiedAsk:
        def execute(self, project_id, function, payload, sources):
            evidence_source = next(source for source in sources if source["source_class"] == "Evidence")
            return {
                "status": "SUCCEEDED",
                "result": {
                    "category": "SOURCE FACT",
                    "answer": "E1 supports the answer.",
                    "citations": [{"source_id": evidence_source["source_id"], "source_reference_id": citation["source_reference_id"]}],
                },
                "run_id": "run-r047",
                "provider": "qualification",
                "model": "qualification-model",
                "profile_revision": "profile",
                "prompt_revision": "prompt",
                "schema_revision": "schema",
                "privacy_mode": "LOCAL_ONLY",
                "source_revision_set": [],
                "status": "SUCCEEDED",
            }

    intelligence.ai = QualifiedAsk()
    answer = intelligence.ask(project["project_id"], "durable source")
    assert answer["answer"] == "E1 supports the answer."
    assert answer["citations"][0]["source_id"] == evidence["evidence_id"]
    assert answer["citations"][0]["source_reference_id"] == citation["source_reference_id"]

    from src.prime_core.progress_service import ProgressService
    goal = CoreService(settings).create_goal_revision(project["project_id"], "Cited progress", approve=True)
    progress = ProgressService(settings)
    review = progress.propose_baseline(project["project_id"], goal["goal_revision_id"], [{"title": "source", "weight": 1.0, "completion": 0.0}])
    progress.approve_baseline(review["review_id"])
    assessment = progress.assess(project["project_id"], goal["goal_revision_id"], [{"title": "source", "weight": 1.0, "completion": 1.0, "confidence": 1.0}], repository_revision="commit-A", evidence_refs=[citation["source_reference_id"]])
    assert assessment["evidence_refs"] == [citation["source_reference_id"]]

    projection = NotionProjectionService(settings)
    rendered = projection.project(
        project["project_id"],
        "before\n<!-- PRIME_MANAGED_START -->old<!-- PRIME_MANAGED_END -->\nafter",
        f"Evidence E1 / SourceReference {citation['source_reference_id']}",
    )
    assert citation["source_reference_id"] in rendered["content"]
    service.retract_evidence(project["project_id"], evidence["evidence_id"], "source superseded")
    assert intelligence.search(project["project_id"], "Cited progress")["groups"]["Progress"] == []
    assert progress.snapshot(project["project_id"])["assessment"] is None
    assert intelligence.search(project["project_id"], "durable source")["groups"]["Evidence"] == []
    restored = service.store_uploaded_evidence(
        project["project_id"], "restored.txt", b"E1 durable source content", "text/plain", source_revision="commit-A"
    )
    assert restored["content_hash"] == evidence["content_hash"]


def test_r043_continuity_backup_clean_restore_identity_and_interruption(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    import psycopg
    from dataclasses import replace
    from psycopg import sql
    from urllib.parse import urlsplit, urlunsplit

    from src.prime_core.backup_service import BackupCoordinator, BackupError
    from src.prime_core.db import connect, migrate
    from src.prime_core.history_service import HistoryService
    from src.prime_core.service import CoreService

    monkeypatch.setenv("PRIME_EVIDENCE_ROOT", str(tmp_path / "source-evidence"))
    source = _settings(monkeypatch)
    migrate(source)
    core = CoreService(source)
    project = core.create_project("R-043 restore identity")
    node = "node-r043-" + os.urandom(4).hex()
    core.register_node(node, "Qualification Node", "linux", hashlib.sha256(node.encode()).hexdigest(), [str(tmp_path)], {})
    core.bind_repository(project["project_id"], node, os.urandom(32).hex(), str(tmp_path))
    goal = core.create_goal_revision(project["project_id"], "Restore this project", approve=True)
    core.record_authority_revision(project["project_id"], ".agent/CURRENT.md", "authority-r043", "VALID", canonical_commit="commit-A")
    evidence = HistoryService(source).store_uploaded_evidence(project["project_id"], "restore.txt", b"restore identity", "text/plain", source_revision="commit-A")
    backup_path = tmp_path / "backup" / "prime.continuity"
    backup = BackupCoordinator().create_continuity_backup(source, backup_path, "r043 qualification recovery key", project_ids=[project["project_id"]], destination_class="operator-selected")
    assert backup["status"] == "VERIFIED"

    parsed = urlsplit(source.database_url)
    database_name = "prime_r043_" + os.urandom(6).hex()
    maintenance_url = urlunsplit((parsed.scheme, parsed.netloc, "/postgres", parsed.query, parsed.fragment))
    target_url = urlunsplit((parsed.scheme, parsed.netloc, "/" + database_name, parsed.query, parsed.fragment))
    with psycopg.connect(maintenance_url, autocommit=True) as maintenance:
        maintenance.execute(sql.SQL("CREATE DATABASE {} ").format(sql.Identifier(database_name)))
    target = replace(source, database_url=target_url)
    try:
        migrate(target)
        restored = BackupCoordinator().restore_bundle(target, backup_path, "r043 qualification recovery key", storage_root=tmp_path / "restored-evidence")
        assert restored["status"] == "RESTORED"
        with connect(target) as db:
            restored_row = db.execute("SELECT project_id,name FROM prime_core.projects WHERE project_id=%s", (project["project_id"],)).fetchone()
            restored_evidence = db.execute("SELECT evidence_id,content_hash,source_reference_id FROM prime_core.evidence_records WHERE evidence_id=%s", (evidence["evidence_id"],)).fetchone()
            workflow = db.execute("SELECT status,current_step FROM prime_core.restore_workflows WHERE restore_id=%s", (restored["restore_id"],)).fetchone()
        assert restored_row["name"] == project["name"]
        assert restored_evidence["content_hash"] == evidence["content_hash"]
        assert restored_evidence["source_reference_id"] == evidence["source_reference_id"]
        assert workflow == {"status": "SUCCEEDED", "current_step": "COMPLETE"}
        reindexed = HistoryService(target).reindex_evidence(project["project_id"], evidence["evidence_id"])
        assert reindexed["content_hash"] == evidence["content_hash"]

        with pytest.raises(BackupError):
            BackupCoordinator().restore_bundle(
                target,
                backup_path,
                "r043 qualification recovery key",
                replace=True,
                safety_destination=tmp_path / "safety-checkpoint",
                fail_after_tables=1,
            )
        with connect(target) as db:
            interrupted = db.execute("SELECT status,current_step,error_code FROM prime_core.restore_workflows ORDER BY started_at DESC LIMIT 1").fetchone()
        assert interrupted["status"] == "REPAIR_REQUIRED"
        assert interrupted["current_step"] == "FAILED"
        assert interrupted["error_code"] == "RuntimeError"
    finally:
        with psycopg.connect(maintenance_url, autocommit=True) as maintenance:
            maintenance.execute(sql.SQL("DROP DATABASE {} ").format(sql.Identifier(database_name)))


def test_r045_sustained_queue_quota_disk_pressure_and_recovery(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    import shutil
    import time

    from src.prime_core.db import migrate
    from src.prime_core.history_service import HistoryService
    from src.prime_core.reliability_service import ReliabilityService
    from src.prime_core.service import CoreService

    monkeypatch.setenv("PRIME_EVIDENCE_ROOT", str(tmp_path / "capacity-evidence"))
    monkeypatch.setenv("PRIME_QUEUE_LIMIT", "32")
    monkeypatch.setenv("PRIME_EVIDENCE_PROJECT_QUOTA_BYTES", "64")
    settings = _settings(monkeypatch)
    migrate(settings)
    core = CoreService(settings)
    project = core.create_project("R-045 sustained capacity")
    started = time.monotonic()
    accepted = 0
    refused = 0
    for number in range(256):
        try:
            core.create_coalesced_job("REINDEX", {"event": number}, project["project_id"], f"burst-{number}")
            accepted += 1
        except ValueError as exc:
            assert "backpressure" in str(exc)
            refused += 1
    duration = time.monotonic() - started
    reliability = ReliabilityService(settings)
    pressure = reliability.capacity_status(tmp_path)
    assert accepted <= 32
    assert refused > 0
    assert pressure["queue"]["queued"] <= pressure["queue"]["limit"]
    assert pressure["canonical_writes_prioritized"] is True
    with pytest.raises(ValueError, match="quota"):
        HistoryService(settings).store_uploaded_evidence(project["project_id"], "quota.txt", b"q" * 65, "text/plain")

    free = shutil.disk_usage(tmp_path).free
    monkeypatch.setenv("PRIME_DISK_WARNING_BYTES", str(free + 1))
    monkeypatch.setenv("PRIME_DISK_CRITICAL_BYTES", "1")
    warning = reliability.capacity_status(tmp_path)
    assert warning["disk"]["status"] == "WARNING"
    monkeypatch.setenv("PRIME_DISK_WARNING_BYTES", "0")
    healthy = reliability.capacity_status(tmp_path)
    assert healthy["disk"]["status"] == "HEALTHY"
    assert duration >= 0


def test_r042_real_separate_mount_backup_target_and_manifest(
    monkeypatch: pytest.MonkeyPatch,
):
    from src.prime_core.backup_service import BackupCoordinator
    from src.prime_core.db import migrate
    from src.prime_core.service import CoreService

    target_root = Path("/mnt/storage1tb")
    if not target_root.is_dir() or target_root.stat().st_dev == Path.cwd().stat().st_dev:
        pytest.skip("no independent writable backup mount is available")
    settings = _settings(monkeypatch)
    migrate(settings)
    project = CoreService(settings).create_project("R-042 external target")
    destination_dir = target_root / ".animus-prime-qualification-017"
    destination = destination_dir / "prime.continuity"
    try:
        result = BackupCoordinator().create_continuity_backup(
            settings,
            destination,
            "r042 qualification recovery key",
            project_ids=[project["project_id"]],
        )
        assert result["status"] == "VERIFIED"
        assert result["manifest"]["destination_class"] == "off-machine"
        assert result["manifest"]["continuity"] is True
    finally:
        destination.unlink(missing_ok=True)
        try:
            destination_dir.rmdir()
        except OSError:
            pass


def test_r048_r050_historical_abcd_ask_brain_and_return_to_now(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    import time
    from datetime import datetime, timezone

    from src.prime_memory_adapter import AdapterResult
    from src.prime_core.brain_service import BrainService
    from src.prime_core.db import connect, migrate
    from src.prime_core.history_service import HistoryService
    from src.prime_core.indexer import RepositoryIndexer
    from src.prime_core.intelligence_service import IntelligenceService
    from src.prime_core.memory_service import MemoryService
    from src.prime_core.notion_service import NotionProjectionService
    from src.prime_core.progress_service import ProgressService
    from src.prime_core.service import CoreService

    class QualificationMemory:
        def retain_verified(self, content, document_id):
            return AdapterResult("CURRENT", {"document_id": document_id})

        def recall(self, query):
            return AdapterResult("CURRENT", {"results": []})

    settings = _settings(monkeypatch)
    migrate(settings)
    repo = tmp_path / "historical-repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "qualification@example.invalid")
    _git(repo, "config", "user.name", "Qualification")
    core = CoreService(settings)
    project = core.create_project("R-048/R-050 A B C D")
    node = "node-historical-" + os.urandom(4).hex()
    core.register_node(node, "Historical Node", "linux", os.urandom(32).hex(), [str(tmp_path)], {})
    core.bind_repository(project["project_id"], node, os.urandom(32).hex(), str(repo))
    history = HistoryService(settings)
    memory = MemoryService(settings, adapter_factory=lambda _project_id: QualificationMemory())
    notion = NotionProjectionService(settings)
    progress = ProgressService(settings)
    checkpoints = tmp_path / "historical-checkpoints"
    cutoffs = {}

    def state(label: str, authority_status: str, progress_value: int, memory_text: str):
        (repo / "state.txt").write_text(f"STATE {label}\n", encoding="utf-8")
        _git(repo, "add", "state.txt")
        _git(repo, "commit", "-qm", f"state {label}")
        revision = _git(repo, "rev-parse", "HEAD")
        RepositoryIndexer(core).build(project["project_id"])
        core.record_authority_revision(project["project_id"], f".agent/{label}.md", revision, authority_status, canonical_commit=revision)
        evidence = history.store_uploaded_evidence(project["project_id"], f"evidence-{label}.txt", f"Evidence {label}".encode(), "text/plain", source_revision=revision)
        if label == "A":
            goal = core.create_goal_revision(project["project_id"], "Goal v1", approve=True)
            review = progress.propose_baseline(project["project_id"], goal["goal_revision_id"], [{"title": "continuity", "weight": 1.0, "completion": 0.0}])
            progress.approve_baseline(review["review_id"])
            state.goal_revision_id = goal["goal_revision_id"]
        progress.assess(project["project_id"], state.goal_revision_id, [{"title": "continuity", "weight": 1.0, "completion": progress_value / 100, "confidence": 1.0}], repository_revision=revision, summary=f"Progress {progress_value}")
        memory.store(project["project_id"], memory_text, "FACT", source_revision=revision, source_reference_id=evidence["source_reference_id"])
        notion._record(project["project_id"], evidence["content_hash"], "SYNCED", {"source_revision": revision}, f"Evidence {label} / {evidence['source_reference_id']}")
        history.add_git_checkpoint(project["project_id"], str(repo), revision, str(checkpoints))
        BrainService(settings).build(project["project_id"], revision)
        time.sleep(0.03)
        cutoffs[label] = datetime.now(timezone.utc).isoformat()
        return revision

    state.goal_revision_id = None
    revisions = {}
    revisions["A"] = state("A", "VALID", 20, "Memory A")
    revisions["B"] = state("B", "VALID", 45, "Memory B")
    revisions["C"] = state("C", "INVALID", 35, "Memory C correction")
    revisions["D"] = state("D", "VALID", 75, "Memory D")

    intelligence = IntelligenceService(settings, memory=memory)
    with connect(settings) as db:
        state_b_evidence = db.execute("SELECT evidence_id,storage_path FROM prime_core.evidence_records WHERE project_id=%s AND source_revision=%s", (project["project_id"], revisions["B"])).fetchone()
    removed_bytes = Path(state_b_evidence["storage_path"]).read_bytes()
    Path(state_b_evidence["storage_path"]).unlink()
    unavailable_b = history.historical_context(project["project_id"], cutoffs["B"])
    assert unavailable_b["source_statuses"]["evidence"] == "PARTIAL"
    Path(state_b_evidence["storage_path"]).write_bytes(removed_bytes)
    assert history.reindex_evidence(project["project_id"], state_b_evidence["evidence_id"])["index_status"] == "READY"
    assert history.historical_context(project["project_id"], cutoffs["B"])["source_statuses"]["evidence"] == "EXACT"
    direct_revision_context = history.historical_context(project["project_id"], revisions["B"])
    assert direct_revision_context["source_statuses"]["repository"] == "EXACT"
    assert direct_revision_context["source_statuses"]["goal"] == "EXACT"
    assert direct_revision_context["goal"][0]["content"] == "Goal v1"
    assert BrainService(settings).build_historical(project["project_id"], revisions["B"])["source_revision"] == revisions["B"]
    for label, revision in revisions.items():
        context = history.historical_context(project["project_id"], cutoffs[label])
        assert context["selected_revision"] == revision
        assert context["source_statuses"]["repository"] == "EXACT"
        assert context["source_statuses"]["evidence"] == "EXACT"
        assert context["source_statuses"]["progress"] == "EXACT"
        assert context["source_statuses"]["authority"] == "EXACT"
        assert context["source_statuses"]["notion"] == "EXACT"
        assert all(row["source_revision"] in revisions.values() for row in context["evidence"])
        observed_labels = {row["source_revision"] for row in context["evidence"]}
        assert revision in observed_labels
        assert all(revisions[later] not in observed_labels for later in revisions if later > label)
        assert BrainService(settings).build_historical(project["project_id"], cutoffs[label])["availability"] == "EXACT"
        answer = intelligence.ask_at(project["project_id"], "what was known?", cutoffs[label])
        assert answer["historical"] is True
        assert answer["later_current_state_used"] is False
        assert all(citation.get("source_revision") in observed_labels for citation in answer["citations"] if citation.get("source_revision"))
    now_state = history.return_to_now(project["project_id"])
    assert now_state["mode"] == "CURRENT"
    assert now_state["selected_revision"] == revisions["D"]
