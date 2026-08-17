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


pytestmark = pytest.mark.skipif(not os.getenv("PRIME_PHASE1_DB_URL"), reason="set PRIME_PHASE1_DB_URL for approved MCP integration")


def test_mcp_has_exact_six_tools_and_grant_scope(monkeypatch):
    monkeypatch.setenv("PRIME_DATABASE_URL", os.environ["PRIME_PHASE1_DB_URL"])
    from src.prime_core.config import Settings
    from src.prime_core.db import migrate
    from src.prime_core.memory_service import MemoryService
    from src.prime_core.mcp_service import CANONICAL_TOOLS, MCPService
    from src.prime_core.service import CoreService
    from src.prime_core.history_service import HistoryService
    settings = Settings()
    migrate(settings)
    core = CoreService(settings)
    project = core.create_project("MCP Project")
    source = HistoryService(settings).create_source_reference(project["project_id"], "AUTHORITY", ".agent/LEARNINGS.md", revision="commit-A")
    fake = FakeAdapter(project["project_id"])
    mcp = MCPService(settings, MemoryService(settings, lambda _: fake))
    grant = mcp.issue_grant(project["project_id"], "codex-test")
    assert len(CANONICAL_TOOLS) == 6
    stored = mcp.call(grant["token"], "prime_memory_store", {"kind": "learning", "summary": "bounded context", "content": "bounded context", "source_refs": [source["source_reference_id"]], "salience": "high", "confidence": 0.9, "working_context": {"git_commit": "commit-A", "git_ref": "main", "worktree_path_or_id": "/repo"}, "project_id": "forged"})
    assert stored["status"] == "stored"
    assert source["source_reference_id"] in stored["provenance_refs"]
    memory = mcp.call(grant["token"], "prime_memory_get", {"memory_id": stored["memory_id"]})
    assert memory["result"]["source_reference_id"] == source["source_reference_id"]
    assert memory["result"]["source_revision"] == "commit-A"
    assert memory["result"]["metadata"]["salience"] == "high"
    recalled = mcp.call(grant["token"], "prime_memory_recall", {"query": "context", "project_id": "forged"})
    assert recalled["project_id"] == project["project_id"]
    assert recalled["results"]
    assert recalled["results"][0]["source_reference_id"] == source["source_reference_id"]
    assert mcp.call(grant["token"], "raw_hindsight", {})["error_code"] == "INVALID_INPUT"
    mcp.revoke_grant(grant["grant_id"])
    assert mcp.call(grant["token"], "prime_memory_context", {"objective": "x"})["error_code"] == "PROJECT_SCOPE_VIOLATION"


@pytest.mark.skipif(not os.getenv("PRIME_MCP_TEST_PROJECT_ID"), reason="set PRIME_MCP_TEST_PROJECT_ID for approved MCP activity integration")
def test_mcp_memory_activity_persists_bounded_request_result_and_scope(monkeypatch):
    monkeypatch.setenv("PRIME_DATABASE_URL", os.environ["PRIME_PHASE1_DB_URL"])
    from src.prime_core.config import Settings
    from src.prime_core.db import connect, migrate
    from src.prime_core.memory_service import MemoryService
    from src.prime_core.mcp_service import MCPService

    settings = Settings()
    migrate(settings)
    project_id = os.environ["PRIME_MCP_TEST_PROJECT_ID"]
    fake = FakeAdapter(project_id)
    mcp = MCPService(settings, MemoryService(settings, lambda _: fake))
    grant = mcp.issue_grant(project_id, "codex-activity-test")
    stored = mcp.call(grant["token"], "prime_memory_store", {
        "kind": "learning", "summary": "bounded", "content": "bounded existing context",
        "source_refs": [], "working_context": {"git_commit": "commit-activity"},
    })
    recall = mcp.call(grant["token"], "prime_memory_recall", {
        "query": "api_key=do-not-store existing context", "max_results": 3,
    })
    context = mcp.call(grant["token"], "prime_memory_context", {
        "objective": "Resume the existing project safely", "max_tokens": 1200,
    })
    assert stored["status"] == "stored"
    assert recall["results"]
    assert context["project_id"] == project_id
    with connect(settings) as db:
        rows = db.execute(
            "SELECT tool,grant_id,client_id,request_kind,objective_or_query,returned_memory_ids,"
            "requested_max_results,requested_max_tokens,actual_result_count,status "
            "FROM prime_core.mcp_memory_activity WHERE project_id=%s AND client_id=%s ORDER BY created_at DESC LIMIT 3",
            (project_id, "codex-activity-test"),
        ).fetchall()
    assert [row["tool"] for row in reversed(rows)] == ["prime_memory_store", "prime_memory_recall", "prime_memory_context"]
    assert all(row["grant_id"] == grant["grant_id"] and row["client_id"] == "codex-activity-test" for row in rows)
    query_row = next(row for row in rows if row["tool"] == "prime_memory_recall")
    context_row = next(row for row in rows if row["tool"] == "prime_memory_context")
    store_row = next(row for row in rows if row["tool"] == "prime_memory_store")
    assert query_row["request_kind"] == "QUERY"
    assert "[REDACTED]" in query_row["objective_or_query"]
    assert "do-not-store" not in query_row["objective_or_query"]
    assert query_row["requested_max_results"] == 3
    assert context_row["request_kind"] == "OBJECTIVE"
    assert context_row["requested_max_tokens"] == 1200
    assert stored["memory_id"] in store_row["returned_memory_ids"]
    assert stored["memory_id"] in query_row["returned_memory_ids"]
    assert query_row["actual_result_count"] >= 1
    assert all(row["status"] == "SUCCEEDED" for row in rows)
