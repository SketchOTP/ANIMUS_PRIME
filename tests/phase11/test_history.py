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
    from src.prime_core.config import Settings
    from src.prime_core.db import migrate
    from src.prime_core.history_service import HistoryService
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
    assert service.record_evidence(project["project_id"], "UPLOAD", "local://evidence", b"evidence")["parser_status"] == "READY"
    assert service.time_lens(project["project_id"], revision)["reconstruction_status"] == "EXACT"
    fork = service.fork(project["project_id"], revision, "Fork")
    assert fork["new_project_id"] != project["project_id"] and fork["memory_copy_status"] == "NONE"
