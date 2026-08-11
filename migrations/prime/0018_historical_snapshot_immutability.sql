-- Historical rows are append-only lifecycle observations, not mutable projections.
ALTER TABLE prime_core.historical_revisions
    DROP CONSTRAINT IF EXISTS historical_revisions_project_id_artifact_type_artifact_id_source_revision_key;

CREATE UNIQUE INDEX IF NOT EXISTS historical_revisions_event_identity_idx
    ON prime_core.historical_revisions(project_id, artifact_type, artifact_id, source_revision, observed_at);
