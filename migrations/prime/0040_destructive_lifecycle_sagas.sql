CREATE TABLE IF NOT EXISTS prime_core.project_deletion_tombstones (
    project_id TEXT PRIMARY KEY,
    project_name_hash TEXT NOT NULL,
    deleted_at TIMESTAMPTZ NOT NULL,
    actor_id TEXT NOT NULL,
    disposition JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE IF NOT EXISTS prime_core.lifecycle_resource_dispositions (
    disposition_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    workflow_id TEXT REFERENCES prime_core.workflows(workflow_id) ON DELETE SET NULL,
    resource_type TEXT NOT NULL,
    resource_key TEXT NOT NULL,
    locator TEXT,
    status TEXT NOT NULL,
    details JSONB NOT NULL DEFAULT '{}'::jsonb,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE(project_id, resource_type, resource_key)
);

CREATE INDEX IF NOT EXISTS lifecycle_resource_dispositions_project_idx
    ON prime_core.lifecycle_resource_dispositions(project_id, resource_type);
