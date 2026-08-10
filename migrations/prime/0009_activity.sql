CREATE TABLE IF NOT EXISTS prime_core.activity_checkpoints (
    project_id TEXT PRIMARY KEY REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    last_seen_event_sequence BIGINT NOT NULL DEFAULT 0,
    updated_at TIMESTAMPTZ NOT NULL
);
