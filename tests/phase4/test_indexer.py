from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest


pytestmark = pytest.mark.skipif(not os.getenv("PRIME_PHASE1_DB_URL"), reason="set PRIME_PHASE1_DB_URL for indexing integration")


def test_index_is_deterministic_and_searchable(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("PRIME_DATABASE_URL", os.environ["PRIME_PHASE1_DB_URL"])
    if os.getenv("PRIME_QUALIFICATION_STATE", "clean").lower() == "persistent":
        pytest.skip(
            "FRESH_STATE_REQUIRED — deterministic index fixture requires isolated repository/project state; "
            "preserved clean-state evidence remains authoritative"
        )
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "README.md").write_text("phase four", encoding="utf-8")
    (repo / ".agent").mkdir()
    (repo / ".agent" / "CURRENT.md").write_text("current", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "init", "-q"], check=True)
    from src.prime_core.config import Settings
    from src.prime_core.db import migrate
    from src.prime_core.service import CoreService
    from src.prime_core.indexer import RepositoryIndexer
    settings = Settings(database_url=os.environ["PRIME_PHASE1_DB_URL"])
    migrate(settings)
    service = CoreService(settings)
    project = service.create_project("Index Project")
    service.register_node("node-index", "Local", "linux", "c" * 64, [str(tmp_path)], {})
    service.bind_repository(project["project_id"], "node-index", "d" * 64, str(repo))
    indexer = RepositoryIndexer(service)
    first = indexer.build(project["project_id"])
    second = indexer.build(project["project_id"])
    assert first["files_indexed"] == 2
    assert second["source_revision"] == first["source_revision"]
    assert indexer.search(project["project_id"], "README")[0]["relative_path"] == "README.md"
    natural = indexer.search(project["project_id"], "What does the repository say about phase four?")
    assert natural and natural[0]["relative_path"] == "README.md"
