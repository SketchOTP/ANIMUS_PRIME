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
    from src.prime_core.db import migrate
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
