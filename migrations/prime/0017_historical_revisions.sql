-- Continuation 007: durable historical snapshots and explicit Evidence storage mode.
ALTER TABLE prime_core.evidence_records
    ADD COLUMN IF NOT EXISTS storage_mode TEXT NOT NULL DEFAULT 'MANAGED_COPY',
    ADD COLUMN IF NOT EXISTS purged_at TIMESTAMPTZ,
    ADD COLUMN IF NOT EXISTS parser_error TEXT,
    ADD COLUMN IF NOT EXISTS source_uri TEXT;

ALTER TABLE prime_core.authority_revisions
    ADD COLUMN IF NOT EXISTS content_snapshot TEXT,
    ADD COLUMN IF NOT EXISTS canonical_commit TEXT;

ALTER TABLE prime_core.notion_projection_revisions
    ADD COLUMN IF NOT EXISTS rendered_content TEXT,
    ADD COLUMN IF NOT EXISTS managed_section_key TEXT,
    ADD COLUMN IF NOT EXISTS notion_target_refs JSONB NOT NULL DEFAULT '{}'::jsonb;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'evidence_records_storage_mode_check'
          AND conrelid = 'prime_core.evidence_records'::regclass
    ) THEN
        ALTER TABLE prime_core.evidence_records
            ADD CONSTRAINT evidence_records_storage_mode_check
            CHECK (storage_mode IN ('MANAGED_COPY', 'NODE_REFERENCE', 'EXTERNAL_REFERENCE'));
    END IF;
END $$;

CREATE UNIQUE INDEX IF NOT EXISTS evidence_project_content_hash_idx
    ON prime_core.evidence_records(project_id, content_hash)
    WHERE content_hash IS NOT NULL AND retracted_at IS NULL AND purged_at IS NULL;

CREATE TABLE IF NOT EXISTS prime_core.historical_revisions (
    historical_revision_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    artifact_type TEXT NOT NULL,
    artifact_id TEXT NOT NULL,
    source_revision TEXT,
    content_hash TEXT,
    snapshot JSONB NOT NULL,
    availability_status TEXT NOT NULL CHECK (availability_status IN ('EXACT','PARTIAL','UNAVAILABLE')),
    observed_at TIMESTAMPTZ NOT NULL,
    UNIQUE(project_id, artifact_type, artifact_id, source_revision)
);

CREATE INDEX IF NOT EXISTS historical_revisions_cutoff_idx
    ON prime_core.historical_revisions(project_id, artifact_type, observed_at);

ALTER TABLE prime_core.git_history_checkpoints
    ADD COLUMN IF NOT EXISTS source_reference_id TEXT REFERENCES prime_core.source_references(source_reference_id) ON DELETE SET NULL;
