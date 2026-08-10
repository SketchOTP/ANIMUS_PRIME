CREATE TABLE IF NOT EXISTS prime_core.notion_projects (
    project_id TEXT PRIMARY KEY REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    page_id TEXT,
    page_url TEXT,
    connection_status TEXT NOT NULL CHECK (connection_status IN ('CONNECTED','DEGRADED','DISCONNECTED','CONFLICT')),
    managed_content_hash TEXT,
    last_synced_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS prime_core.notion_projection_revisions (
    projection_revision_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    content_hash TEXT NOT NULL,
    source_set JSONB NOT NULL DEFAULT '[]'::jsonb,
    sync_status TEXT NOT NULL CHECK (sync_status IN ('SYNCED','DEGRADED','CONFLICT','RETRYABLE')),
    observed_at TIMESTAMPTZ NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);
