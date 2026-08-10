CREATE TABLE IF NOT EXISTS prime_core.backup_schedules (
    schedule_id TEXT PRIMARY KEY,
    destination TEXT NOT NULL,
    cadence TEXT NOT NULL,
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    last_started_at TIMESTAMPTZ,
    last_completed_at TIMESTAMPTZ,
    last_error TEXT,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

ALTER TABLE prime_core.evidence_records ADD COLUMN IF NOT EXISTS storage_path TEXT;
ALTER TABLE prime_core.evidence_records ADD COLUMN IF NOT EXISTS mime_type TEXT;
ALTER TABLE prime_core.evidence_records ADD COLUMN IF NOT EXISTS size_bytes BIGINT;

CREATE TABLE IF NOT EXISTS prime_core.git_history_checkpoints (
    checkpoint_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    commit_id TEXT NOT NULL,
    bundle_locator TEXT,
    coverage_status TEXT NOT NULL CHECK (coverage_status IN ('EXACT','PARTIAL','UNAVAILABLE')),
    content_hash TEXT,
    captured_at TIMESTAMPTZ NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);
