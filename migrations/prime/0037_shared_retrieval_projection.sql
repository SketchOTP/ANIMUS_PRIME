-- Continuation 078: derived searchable repository and Notion source projections.
ALTER TABLE prime_core.repository_files
    ADD COLUMN IF NOT EXISTS content_text TEXT;

CREATE INDEX IF NOT EXISTS repository_files_current_path_idx
    ON prime_core.repository_files(project_id, freshness_state, relative_path);

CREATE INDEX IF NOT EXISTS notion_source_observations_current_idx
    ON prime_core.notion_source_observations(project_id, source_binding_id, observed_at DESC);
