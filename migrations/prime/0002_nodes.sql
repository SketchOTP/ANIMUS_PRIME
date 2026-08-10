CREATE TABLE IF NOT EXISTS prime_core.nodes (
    node_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    platform TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('ENROLLED','ONLINE','DEGRADED','OFFLINE','REVOKED')),
    identity_fingerprint TEXT NOT NULL UNIQUE,
    allowed_roots JSONB NOT NULL DEFAULT '[]'::jsonb,
    capabilities JSONB NOT NULL DEFAULT '{}'::jsonb,
    enrolled_at TIMESTAMPTZ NOT NULL,
    last_seen_at TIMESTAMPTZ,
    revoked_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS prime_core.repositories (
    repository_id TEXT PRIMARY KEY,
    node_id TEXT NOT NULL REFERENCES prime_core.nodes(node_id) ON DELETE RESTRICT,
    project_id TEXT REFERENCES prime_core.projects(project_id) ON DELETE SET NULL,
    identity_fingerprint TEXT NOT NULL UNIQUE,
    canonical_path TEXT NOT NULL,
    is_bare BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL,
    last_observed_at TIMESTAMPTZ NOT NULL
);
