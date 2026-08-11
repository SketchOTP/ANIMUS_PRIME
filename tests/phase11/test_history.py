from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest


pytestmark = pytest.mark.skipif(not os.getenv("PRIME_PHASE1_DB_URL"), reason="set PRIME_PHASE1_DB_URL for history integration")


def test_evidence_timelens_and_isolated_fork(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("PRIME_DATABASE_URL", os.environ["PRIME_PHASE1_DB_URL"])
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "a.txt").write_text("a", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "init", "-q"], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "test@example.invalid"], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "Test"], check=True)
    subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-qm", "state A"], check=True)
    from src.prime_core.config import Settings
    from src.prime_core.db import migrate
    from src.prime_core.history_service import HistoryService
    from src.prime_core.brain_service import BrainService
    from src.prime_core.indexer import RepositoryIndexer
    from src.prime_core.service import CoreService
    settings = Settings()
    migrate(settings)
    core = CoreService(settings)
    project = core.create_project("History Project")
    node = "node-history-" + os.urandom(3).hex()
    core.register_node(node, "Local", "linux", os.urandom(32).hex(), [str(tmp_path)], {})
    core.bind_repository(project["project_id"], node, os.urandom(32).hex(), str(repo))
    revision = RepositoryIndexer(core).build(project["project_id"])["source_revision"]
    service = HistoryService(settings)
    first = service.record_evidence(project["project_id"], "UPLOAD", "local://evidence", b"evidence", source_revision=revision)
    assert first["parser_status"] == "READY"
    citation = service.cite_evidence(project["project_id"], first["evidence_id"])
    assert service.resolve_source_reference(project["project_id"], citation["source_reference_id"], current_revision=revision)["status"] == "EXACT"
    service.record_evidence(project["project_id"], "UPLOAD", "local://later-evidence", b"later")
    checkpoint = service.add_git_checkpoint(project["project_id"], str(repo), revision, str(tmp_path / "prime-history"))
    assert checkpoint["commit_id"] == revision
    branch = subprocess.run(["git", "-C", str(repo), "branch", "--show-current"], check=True, capture_output=True, text=True).stdout.strip()
    subprocess.run(["git", "-C", str(repo), "update-ref", "-d", f"refs/heads/{branch}"], check=True)
    subprocess.run(["git", "-C", str(repo), "reflog", "expire", "--expire=now", "--all"], check=True)
    subprocess.run(["git", "-C", str(repo), "gc", "--prune=now"], check=True)
    restarted = HistoryService(settings)
    assert restarted.git_checkpoint_status(project["project_id"], revision)["coverage_status"] == "EXACT"
    lens = service.time_lens(project["project_id"], revision)
    assert lens["reconstruction_status"] == "PARTIAL"
    assert lens["source_statuses"]["repository"] == "EXACT"
    assert lens["source_statuses"]["evidence"] == "EXACT"
    assert len(lens["evidence"]) == 1
    assert lens["source_statuses"]["authority"] == "UNAVAILABLE"
    assert lens["source_statuses"]["git"] == "EXACT"
    historical_brain = BrainService(settings).build_historical(project["project_id"], revision)
    assert historical_brain["availability"] == "EXACT"
    retracted = service.retract_evidence(project["project_id"], first["evidence_id"], "superseded by State B")
    assert retracted["parser_status"] == "RETRACTED"
    assert service.resolve_source_reference(project["project_id"], citation["source_reference_id"], current_revision=revision)["later_retracted"] is True
    fork = service.fork(project["project_id"], revision, "Fork")
    assert fork["new_project_id"] != project["project_id"] and fork["memory_copy_status"] == "NONE"
