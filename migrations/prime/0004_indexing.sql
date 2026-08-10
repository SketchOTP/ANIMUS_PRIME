CREATE TABLE IF NOT EXISTS prime_core.repository_files (
    repository_file_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    repository_id TEXT NOT NULL REFERENCES prime_core.repositories(repository_id) ON DELETE CASCADE,
    relative_path TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    size_bytes BIGINT NOT NULL,
    file_kind TEXT NOT NULL,
    source_revision TEXT NOT NULL,
    freshness_state TEXT NOT NULL CHECK (freshness_state IN ('CURRENT','STALE','UNKNOWN')),
    observed_at TIMESTAMPTZ NOT NULL,
    UNIQUE(repository_id, relative_path, source_revision)
);

CREATE TABLE IF NOT EXISTS prime_core.source_snapshots (
    source_snapshot_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    source_class TEXT NOT NULL,
    source_revision TEXT NOT NULL,
    source_hash TEXT,
    freshness_state TEXT NOT NULL CHECK (freshness_state IN ('CURRENT','STALE','UNKNOWN')),
    observed_at TIMESTAMPTZ NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    UNIQUE(project_id, source_class, source_revision)
);
