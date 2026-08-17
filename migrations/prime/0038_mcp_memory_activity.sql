CREATE TABLE IF NOT EXISTS prime_core.mcp_memory_activity (
    activity_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    grant_id TEXT NOT NULL,
    client_id TEXT NOT NULL,
    tool TEXT NOT NULL,
    request_kind TEXT NOT NULL,
    objective_or_query TEXT,
    returned_memory_ids JSONB NOT NULL DEFAULT '[]'::jsonb,
    source_types JSONB NOT NULL DEFAULT '[]'::jsonb,
    requested_max_results INTEGER,
    requested_max_tokens INTEGER,
    actual_result_count INTEGER NOT NULL DEFAULT 0,
    stored_memory_id TEXT,
    reported_memory_id TEXT,
    status TEXT NOT NULL,
    response_status TEXT,
    error_code TEXT,
    created_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX IF NOT EXISTS mcp_memory_activity_project_created_idx
    ON prime_core.mcp_memory_activity(project_id, created_at DESC);

CREATE INDEX IF NOT EXISTS mcp_memory_activity_grant_created_idx
    ON prime_core.mcp_memory_activity(grant_id, created_at DESC);
