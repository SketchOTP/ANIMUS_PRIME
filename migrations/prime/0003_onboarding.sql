CREATE TABLE IF NOT EXISTS prime_core.project_bindings (
    project_id TEXT PRIMARY KEY REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    node_id TEXT NOT NULL REFERENCES prime_core.nodes(node_id) ON DELETE RESTRICT,
    repository_id TEXT NOT NULL REFERENCES prime_core.repositories(repository_id) ON DELETE RESTRICT,
    binding_status TEXT NOT NULL CHECK (binding_status IN ('PROVISIONING','BOUND','REVIEW_REQUIRED','REBOUND')),
    canonical_revision TEXT,
    bound_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS prime_core.goal_revisions (
    goal_revision_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    revision_number INTEGER NOT NULL,
    content TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('DRAFT','APPROVED','REJECTED','SUPERSEDED')),
    approved_by TEXT,
    created_at TIMESTAMPTZ NOT NULL,
    approved_at TIMESTAMPTZ,
    UNIQUE(project_id, revision_number)
);

CREATE TABLE IF NOT EXISTS prime_core.authority_revisions (
    authority_revision_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    source_path TEXT NOT NULL,
    source_hash TEXT NOT NULL,
    contract_version TEXT NOT NULL,
    validation_status TEXT NOT NULL CHECK (validation_status IN ('VALID','INVALID','MISSING','CONFLICT')),
    observed_at TIMESTAMPTZ NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);
