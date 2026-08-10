CREATE TABLE IF NOT EXISTS prime_core.brain_snapshots (
    brain_snapshot_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    source_revision TEXT NOT NULL,
    graph JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    UNIQUE(project_id, source_revision)
);
