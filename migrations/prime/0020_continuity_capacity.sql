-- Continuation 008: durable continuity backup metadata and active capacity controls.
ALTER TABLE prime_core.backup_records
    DROP CONSTRAINT IF EXISTS backup_records_backup_type_check;
ALTER TABLE prime_core.backup_records
    ADD CONSTRAINT backup_records_backup_type_check
    CHECK (backup_type IN ('CORE_DB','MEMORY_LEDGER','HINDSIGHT_EXPORT','CONFIG_REFERENCE','CONTINUITY'));
ALTER TABLE prime_core.backup_records
    ADD COLUMN IF NOT EXISTS prime_version TEXT,
    ADD COLUMN IF NOT EXISTS spec_revision TEXT,
    ADD COLUMN IF NOT EXISTS schema_revision TEXT,
    ADD COLUMN IF NOT EXISTS source_high_water_mark TEXT,
    ADD COLUMN IF NOT EXISTS project_ids JSONB NOT NULL DEFAULT '[]'::jsonb,
    ADD COLUMN IF NOT EXISTS component_inventory JSONB NOT NULL DEFAULT '{}'::jsonb,
    ADD COLUMN IF NOT EXISTS component_versions JSONB NOT NULL DEFAULT '{}'::jsonb,
    ADD COLUMN IF NOT EXISTS encryption_version TEXT,
    ADD COLUMN IF NOT EXISTS destination_class TEXT NOT NULL DEFAULT 'same-host',
    ADD COLUMN IF NOT EXISTS manifest JSONB NOT NULL DEFAULT '{}'::jsonb,
    ADD COLUMN IF NOT EXISTS failure_reason TEXT;

ALTER TABLE prime_core.backup_schedules
    ADD COLUMN IF NOT EXISTS key_reference TEXT,
    ADD COLUMN IF NOT EXISTS next_run_at TIMESTAMPTZ,
    ADD COLUMN IF NOT EXISTS retry_count INTEGER NOT NULL DEFAULT 0,
    ADD COLUMN IF NOT EXISTS last_status TEXT NOT NULL DEFAULT 'NOT_RUN',
    ADD COLUMN IF NOT EXISTS idempotency_prefix TEXT;

CREATE TABLE IF NOT EXISTS prime_core.restore_workflows (
    restore_id TEXT PRIMARY KEY,
    backup_id TEXT,
    bundle_locator TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('PREFLIGHT','RUNNING','SUCCEEDED','FAILED','REPAIR_REQUIRED')),
    current_step TEXT NOT NULL,
    safety_backup_locator TEXT,
    error_code TEXT,
    error_message TEXT,
    started_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL,
    completed_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS prime_core.capacity_policies (
    policy_id TEXT PRIMARY KEY,
    scope TEXT NOT NULL UNIQUE,
    max_bytes BIGINT,
    max_items INTEGER,
    retention_days INTEGER,
    queue_limit INTEGER,
    coalesce_window_ms INTEGER NOT NULL DEFAULT 1000,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS backup_records_verified_idx
    ON prime_core.backup_records(status, verified_at DESC);
CREATE INDEX IF NOT EXISTS backup_schedules_due_idx
    ON prime_core.backup_schedules(enabled, next_run_at);
