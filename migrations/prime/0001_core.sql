CREATE SCHEMA IF NOT EXISTS prime_core;

CREATE TABLE IF NOT EXISTS prime_core.schema_migrations (
    version TEXT PRIMARY KEY,
    applied_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS prime_core.operators (
    operator_id TEXT PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    recovery_hash TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS prime_core.sessions (
    session_id TEXT PRIMARY KEY,
    operator_id TEXT NOT NULL REFERENCES prime_core.operators(operator_id) ON DELETE CASCADE,
    token_hash TEXT NOT NULL UNIQUE,
    csrf_hash TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL,
    last_seen_at TIMESTAMPTZ NOT NULL,
    revoked_at TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS sessions_active_idx ON prime_core.sessions(token_hash, expires_at)
    WHERE revoked_at IS NULL;

CREATE TABLE IF NOT EXISTS prime_core.projects (
    project_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    lifecycle_state TEXT NOT NULL CHECK (lifecycle_state IN
      ('DRAFT','PROVISIONING','READY','ACTIVE','PAUSED','COMPLETION_REVIEW','COMPLETED','ARCHIVED','REMOVED','DELETION_PENDING','DELETED')),
    connectivity_state TEXT NOT NULL CHECK (connectivity_state IN ('ONLINE','DEGRADED','OFFLINE')),
    freshness_state TEXT NOT NULL CHECK (freshness_state IN ('CURRENT','STALE','UNKNOWN')),
    work_condition TEXT NOT NULL CHECK (work_condition IN ('NORMAL','BLOCKED','CONFLICT','INVALID_AUTHORITY','REVIEW_REQUIRED')),
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS prime_core.source_references (
    source_reference_id TEXT PRIMARY KEY,
    project_id TEXT REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    source_class TEXT NOT NULL,
    locator TEXT NOT NULL,
    revision TEXT,
    content_hash TEXT,
    freshness_state TEXT NOT NULL CHECK (freshness_state IN ('CURRENT','STALE','UNKNOWN')),
    captured_at TIMESTAMPTZ NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE IF NOT EXISTS prime_core.events (
    event_id TEXT PRIMARY KEY,
    project_id TEXT REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    node_id TEXT,
    event_type TEXT NOT NULL,
    occurred_at TIMESTAMPTZ NOT NULL,
    observed_at TIMESTAMPTZ NOT NULL,
    project_sequence BIGINT,
    source_revision TEXT,
    source_ref TEXT,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    dedupe_key TEXT UNIQUE
);
CREATE UNIQUE INDEX IF NOT EXISTS events_project_sequence_idx
    ON prime_core.events(project_id, project_sequence) WHERE project_id IS NOT NULL;

CREATE TABLE IF NOT EXISTS prime_core.jobs (
    job_id TEXT PRIMARY KEY,
    project_id TEXT REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    job_type TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('QUEUED','RUNNING','SUCCEEDED','FAILED','CANCELLED','DEAD_LETTER','ACTION_REQUIRED')),
    idempotency_key TEXT UNIQUE,
    source_revision TEXT,
    attempts INTEGER NOT NULL DEFAULT 0,
    max_attempts INTEGER NOT NULL DEFAULT 3,
    available_at TIMESTAMPTZ NOT NULL,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    last_error TEXT,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);
CREATE INDEX IF NOT EXISTS jobs_claim_idx ON prime_core.jobs(status, available_at);

CREATE TABLE IF NOT EXISTS prime_core.workflows (
    workflow_id TEXT PRIMARY KEY,
    project_id TEXT REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    workflow_type TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('RUNNING','PAUSED','SUCCEEDED','FAILED','CANCELLED','REPAIR_REQUIRED')),
    current_step TEXT,
    completed_steps JSONB NOT NULL DEFAULT '[]'::jsonb,
    retry_count INTEGER NOT NULL DEFAULT 0,
    idempotency_key TEXT UNIQUE,
    last_error TEXT,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS prime_core.audit_events (
    audit_id TEXT PRIMARY KEY,
    actor_type TEXT NOT NULL,
    actor_id TEXT NOT NULL,
    action TEXT NOT NULL,
    project_id TEXT REFERENCES prime_core.projects(project_id) ON DELETE SET NULL,
    target_type TEXT,
    target_id TEXT,
    occurred_at TIMESTAMPTZ NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE IF NOT EXISTS prime_core.notifications (
    notification_id TEXT PRIMARY KEY,
    project_id TEXT REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    severity TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'OPEN',
    message TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    resolved_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS prime_core.usage_records (
    usage_id TEXT PRIMARY KEY,
    project_id TEXT REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    capability TEXT NOT NULL,
    provider TEXT,
    units NUMERIC NOT NULL DEFAULT 0,
    estimated_cost NUMERIC,
    occurred_at TIMESTAMPTZ NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE IF NOT EXISTS prime_core.settings (
    setting_key TEXT PRIMARY KEY,
    setting_value JSONB NOT NULL,
    secret_reference BOOLEAN NOT NULL DEFAULT FALSE,
    updated_at TIMESTAMPTZ NOT NULL
);
