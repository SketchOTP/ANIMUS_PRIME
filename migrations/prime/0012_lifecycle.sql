CREATE TABLE IF NOT EXISTS prime_core.lifecycle_operations (
    operation_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    from_state TEXT NOT NULL,
    to_state TEXT NOT NULL,
    actor_type TEXT NOT NULL,
    actor_id TEXT NOT NULL,
    confirmation_hash TEXT,
    step_up_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS prime_core.remote_access_status (
    status_id TEXT PRIMARY KEY,
    provider TEXT NOT NULL,
    mode TEXT NOT NULL CHECK (mode IN ('DISABLED','SERVE','FUNNEL','UNKNOWN')),
    endpoint TEXT,
    observed_at TIMESTAMPTZ NOT NULL,
    details JSONB NOT NULL DEFAULT '{}'::jsonb
);
