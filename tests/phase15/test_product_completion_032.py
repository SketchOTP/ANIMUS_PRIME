from __future__ import annotations

import os

import pytest


pytestmark = pytest.mark.skipif(not os.getenv("PRIME_PHASE1_DB_URL"), reason="set PRIME_PHASE1_DB_URL for MCP integration")


def test_project_scoped_grant_revoke_is_type_safe(monkeypatch):
    monkeypatch.setenv("PRIME_DATABASE_URL", os.environ["PRIME_PHASE1_DB_URL"])
    from src.prime_core.config import Settings
    from src.prime_core.db import migrate
    from src.prime_core.mcp_service import MCPService
    from src.prime_core.service import CoreService

    settings = Settings()
    migrate(settings)
    core = CoreService(settings)
    source = core.create_project("MCP revoke source")
    other = core.create_project("MCP revoke other")
    mcp = MCPService(settings)
    grant = mcp.issue_grant(source["project_id"], "continuation-032-test")

    with pytest.raises(KeyError):
        mcp.revoke_grant(grant["grant_id"], other["project_id"])
    assert mcp.call(grant["token"], "prime_memory_context", {"objective": "still active"})["project_id"] == source["project_id"]

    mcp.revoke_grant(grant["grant_id"], source["project_id"])
    assert mcp.call(grant["token"], "prime_memory_context", {"objective": "revoked"})["error_code"] == "PROJECT_SCOPE_VIOLATION"
