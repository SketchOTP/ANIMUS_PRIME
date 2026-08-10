from __future__ import annotations

import os

import pytest

from src.prime_memory_adapter import AdapterResult


class FakeAdapter:
    def __init__(self, project_id: str):
        self.documents: list[dict] = []

    def retain_verified(self, content: str, document_id: str):
        self.documents.append({"content": content, "document_id": document_id})
        return AdapterResult("CURRENT", {})

    def recall(self, query: str):
        return AdapterResult("CURRENT", {"results": self.documents})


pytestmark = pytest.mark.skipif(not os.getenv("PRIME_PHASE1_DB_URL"), reason="set PRIME_PHASE1_DB_URL for MCP integration")


def test_mcp_has_exact_six_tools_and_grant_scope(monkeypatch):
    monkeypatch.setenv("PRIME_DATABASE_URL", os.environ["PRIME_PHASE1_DB_URL"])
    from src.prime_core.config import Settings
    from src.prime_core.db import migrate
    from src.prime_core.memory_service import MemoryService
    from src.prime_core.mcp_service import CANONICAL_TOOLS, MCPService
    from src.prime_core.service import CoreService
    settings = Settings()
    migrate(settings)
    core = CoreService(settings)
    project = core.create_project("MCP Project")
    fake = FakeAdapter(project["project_id"])
    mcp = MCPService(settings, MemoryService(settings, lambda _: fake))
    grant = mcp.issue_grant(project["project_id"], "codex-test")
    assert len(CANONICAL_TOOLS) == 6
    stored = mcp.call(grant["token"], "prime_memory_store", {"kind": "learning", "summary": "test", "content": "bounded context", "project_id": "forged"})
    assert stored["status"] == "stored"
    recalled = mcp.call(grant["token"], "prime_memory_recall", {"query": "context", "project_id": "forged"})
    assert recalled["project_id"] == project["project_id"]
    assert recalled["results"]
    assert mcp.call(grant["token"], "raw_hindsight", {})["error_code"] == "INVALID_INPUT"
    mcp.revoke_grant(grant["grant_id"])
    assert mcp.call(grant["token"], "prime_memory_context", {"objective": "x"})["error_code"] == "PROJECT_SCOPE_VIOLATION"
