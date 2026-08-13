from __future__ import annotations

import os

import pytest

from src.prime_memory_adapter import AdapterResult


class FakeAdapter:
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.documents: list[dict] = []

    def retain_verified(self, content: str, document_id: str):
        self.documents.append({"content": content, "document_id": document_id})
        return AdapterResult("CURRENT", {"results": self.documents})

    def recall(self, query: str):
        return AdapterResult("CURRENT", {"results": self.documents})

    def create_bank(self):
        return AdapterResult("CURRENT", {})

    def delete_bank(self):
        self.documents.clear()
        return AdapterResult("CURRENT", {})


pytestmark = pytest.mark.skipif(not os.getenv("PRIME_PHASE1_DB_URL"), reason="set PRIME_PHASE1_DB_URL for memory integration")


def test_memory_project_isolation_secret_filter_and_tombstone(monkeypatch):
    monkeypatch.setenv("PRIME_DATABASE_URL", os.environ["PRIME_PHASE1_DB_URL"])
    from src.prime_core.config import Settings
    from src.prime_core.db import migrate
    from src.prime_core.memory_service import MemoryService
    from src.prime_core.service import CoreService
    settings = Settings()
    migrate(settings)
    core = CoreService(settings)
    project = core.create_project("Memory Project")
    fake = FakeAdapter(project["project_id"])
    service = MemoryService(settings, lambda _: fake)
    rejected = service.store(project["project_id"], "api_key=do-not-store", "SECRET")
    assert rejected["status"] == "REJECTED"
    stored = service.store(project["project_id"], "Decision: use PostgreSQL", "DECISION", source_revision="r1")
    assert stored["status"] == "STORED"
    duplicate = service.store(project["project_id"], "Decision: use PostgreSQL", "DECISION", source_revision="r1")
    assert duplicate["status"] == "DUPLICATE"
    assert service.recall(project["project_id"], "Decision")["results"]
    service.tombstone(project["project_id"], stored["memory_id"], "operator correction")
    assert service.recall(project["project_id"], "Decision")["results"] == []


def test_source_ledger_rebuild_excludes_superseded_and_tombstoned(monkeypatch):
    monkeypatch.setenv("PRIME_DATABASE_URL", os.environ["PRIME_PHASE1_DB_URL"])
    from src.prime_core.config import Settings
    from src.prime_core.db import migrate
    from src.prime_core.memory_service import MemoryService
    from src.prime_core.service import CoreService
    settings = Settings()
    migrate(settings)
    project = CoreService(settings).create_project("Memory rebuild")
    fake = FakeAdapter(project["project_id"])
    service = MemoryService(settings, lambda _: fake)
    current = service.store(project["project_id"], "retain this current fact", "FACT", source_revision="r1")
    superseded = service.store(project["project_id"], "old correction", "FACT", source_revision="r1")
    replacement = service.store(project["project_id"], "new correction", "FACT", source_revision="r2", supersedes_memory_id=superseded["memory_id"], correction_reason="verified")
    service.tombstone(project["project_id"], replacement["memory_id"], "removed")
    rebuilt = service.rebuild_from_source_ledger(project["project_id"])
    assert rebuilt["status"] == "CURRENT"
    assert rebuilt["mode"] == "SOURCE_LEDGER_REBUILD"
    assert rebuilt["restored"] == 1
    assert rebuilt["eligible"] == 1
    assert rebuilt["superseded_and_tombstoned_excluded"] is True
    assert fake.documents[0]["document_id"] == current["memory_id"]
