CREATE TABLE IF NOT EXISTS prime_core.lifecycle_preflights (
    preflight_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    action TEXT NOT NULL,
    state_hash TEXT NOT NULL,
    token_hash TEXT NOT NULL UNIQUE,
    expires_at TIMESTAMPTZ NOT NULL,
    used_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS lifecycle_preflights_project_idx
    ON prime_core.lifecycle_preflights(project_id, created_at DESC);
