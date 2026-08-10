CREATE TABLE IF NOT EXISTS prime_core.mcp_grants (
    grant_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    client_id TEXT NOT NULL,
    token_hash TEXT NOT NULL UNIQUE,
    capabilities JSONB NOT NULL DEFAULT '["prime_memory_store","prime_memory_recall","prime_memory_timeline","prime_memory_get","prime_memory_report_problem","prime_memory_context"]'::jsonb,
    created_at TIMESTAMPTZ NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL,
    revoked_at TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS mcp_grants_active_idx ON prime_core.mcp_grants(token_hash, expires_at) WHERE revoked_at IS NULL;

CREATE TABLE IF NOT EXISTS prime_core.mcp_problem_reports (
    report_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    memory_id TEXT NOT NULL REFERENCES prime_core.memory_records(memory_id) ON DELETE CASCADE,
    problem TEXT NOT NULL,
    note TEXT NOT NULL,
    client_id TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL
);
