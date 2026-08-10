CREATE TABLE IF NOT EXISTS prime_core.evidence_records (
    evidence_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    source_type TEXT NOT NULL CHECK (source_type IN ('UPLOAD','NODE_PATH','EXTERNAL_REFERENCE')),
    locator TEXT NOT NULL,
    content_hash TEXT,
    privacy_class TEXT NOT NULL DEFAULT 'PROJECT_PRIVATE',
    captured_at TIMESTAMPTZ NOT NULL,
    parser_status TEXT NOT NULL CHECK (parser_status IN ('PENDING','READY','REJECTED','UNAVAILABLE')),
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE IF NOT EXISTS prime_core.time_lens_checkpoints (
    checkpoint_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    as_of TEXT NOT NULL,
    reconstruction_status TEXT NOT NULL CHECK (reconstruction_status IN ('EXACT','PARTIAL','UNAVAILABLE')),
    source_set JSONB NOT NULL DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS prime_core.project_forks (
    fork_id TEXT PRIMARY KEY,
    source_project_id TEXT NOT NULL REFERENCES prime_core.projects(project_id) ON DELETE RESTRICT,
    new_project_id TEXT NOT NULL REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    source_revision TEXT NOT NULL,
    memory_copy_status TEXT NOT NULL DEFAULT 'NONE',
    created_at TIMESTAMPTZ NOT NULL
);
