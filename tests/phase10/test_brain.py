from __future__ import annotations

import os
import subprocess
import uuid
from pathlib import Path

import pytest


pytestmark = pytest.mark.skipif(not os.getenv("PRIME_PHASE1_DB_URL"), reason="set PRIME_PHASE1_DB_URL for Brain integration")


def test_brain_is_derived_and_rebuildable(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("PRIME_DATABASE_URL", os.environ["PRIME_PHASE1_DB_URL"])
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "main.py").write_text("print('ok')", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "init", "-q"], check=True)
    from src.prime_core.config import Settings
    from src.prime_core.db import migrate
    from src.prime_core.brain_service import BrainService
    from src.prime_core.indexer import RepositoryIndexer
    from src.prime_core.service import CoreService
    settings = Settings()
    migrate(settings)
    core = CoreService(settings)
    project = core.create_project("Brain Project")
    node_id = "node-brain-" + uuid.uuid4().hex
    core.register_node(node_id, "Local", "linux", uuid.uuid4().hex + uuid.uuid4().hex, [str(tmp_path)], {})
    core.bind_repository(project["project_id"], node_id, uuid.uuid4().hex + uuid.uuid4().hex, str(repo))
    RepositoryIndexer(core).build(project["project_id"])
    service = BrainService(settings)
    graph = service.build(project["project_id"])
    assert any(node["label"] == "main.py" for node in graph["nodes"])
    assert service.get(project["project_id"])["project_id"] == project["project_id"]
