ALTER TABLE prime_core.project_forks
    ADD COLUMN IF NOT EXISTS destination_node_id TEXT REFERENCES prime_core.nodes(node_id) ON DELETE RESTRICT,
    ADD COLUMN IF NOT EXISTS destination_repository_id TEXT REFERENCES prime_core.repositories(repository_id) ON DELETE RESTRICT,
    ADD COLUMN IF NOT EXISTS destination_revision TEXT,
    ADD COLUMN IF NOT EXISTS provenance JSONB NOT NULL DEFAULT '{}'::jsonb;

CREATE INDEX IF NOT EXISTS project_forks_source_idx
    ON prime_core.project_forks(source_project_id, source_revision);
