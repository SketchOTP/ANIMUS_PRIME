CREATE TABLE IF NOT EXISTS prime_core.usage_limits (
    limit_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    capability TEXT NOT NULL,
    period TEXT NOT NULL CHECK (period IN ('DAILY', 'MONTHLY')),
    max_units NUMERIC NOT NULL CHECK (max_units > 0),
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (project_id, capability, period)
);

CREATE INDEX IF NOT EXISTS usage_limits_project_idx
    ON prime_core.usage_limits(project_id, enabled);

CREATE TABLE IF NOT EXISTS prime_core.upgrade_preflights (
    preflight_id TEXT PRIMARY KEY,
    target_version TEXT NOT NULL,
    target_schema TEXT,
    compatibility TEXT NOT NULL,
    migration_required BOOLEAN NOT NULL,
    backup_required BOOLEAN NOT NULL,
    backup_available BOOLEAN NOT NULL,
    status TEXT NOT NULL,
    recovery_guidance TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS upgrade_preflights_created_idx
    ON prime_core.upgrade_preflights(created_at DESC);
