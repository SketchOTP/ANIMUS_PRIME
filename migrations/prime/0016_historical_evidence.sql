ALTER TABLE prime_core.evidence_records
    ADD COLUMN IF NOT EXISTS source_reference_id TEXT REFERENCES prime_core.source_references(source_reference_id) ON DELETE SET NULL,
    ADD COLUMN IF NOT EXISTS observed_at TIMESTAMPTZ,
    ADD COLUMN IF NOT EXISTS creator_type TEXT,
    ADD COLUMN IF NOT EXISTS creator_id TEXT,
    ADD COLUMN IF NOT EXISTS extracted_text TEXT,
    ADD COLUMN IF NOT EXISTS immutable_identity TEXT,
    ADD COLUMN IF NOT EXISTS archived_at TIMESTAMPTZ,
    ADD COLUMN IF NOT EXISTS source_revision TEXT;

UPDATE prime_core.evidence_records SET observed_at = captured_at WHERE observed_at IS NULL;

CREATE TABLE IF NOT EXISTS prime_core.evidence_links (
    evidence_link_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    evidence_id TEXT NOT NULL REFERENCES prime_core.evidence_records(evidence_id) ON DELETE CASCADE,
    relation_type TEXT NOT NULL CHECK (relation_type IN ('GOAL_ITEM','VALIDATION','DIRECTIVE','COMMIT','OUTCOME','ANNOTATION')),
    target_id TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    UNIQUE(project_id, evidence_id, relation_type, target_id)
);

CREATE INDEX IF NOT EXISTS evidence_links_project_idx
    ON prime_core.evidence_links(project_id, relation_type, target_id);

CREATE TABLE IF NOT EXISTS prime_core.evidence_annotations (
    annotation_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    evidence_id TEXT NOT NULL REFERENCES prime_core.evidence_records(evidence_id) ON DELETE CASCADE,
    annotation TEXT NOT NULL,
    source_reference_id TEXT REFERENCES prime_core.source_references(source_reference_id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL,
    retracted_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS source_references_project_revision_idx
    ON prime_core.source_references(project_id, source_class, revision, captured_at);

CREATE UNIQUE INDEX IF NOT EXISTS git_history_project_commit_idx
    ON prime_core.git_history_checkpoints(project_id, commit_id);

ALTER TABLE prime_core.git_history_checkpoints
    ADD COLUMN IF NOT EXISTS repository_path TEXT,
    ADD COLUMN IF NOT EXISTS verified_at TIMESTAMPTZ,
    ADD COLUMN IF NOT EXISTS retained BOOLEAN NOT NULL DEFAULT TRUE;
