CREATE TABLE IF NOT EXISTS prime_core.memory_records (
    memory_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    source_reference_id TEXT REFERENCES prime_core.source_references(source_reference_id) ON DELETE SET NULL,
    document_id TEXT NOT NULL UNIQUE,
    content_hash TEXT NOT NULL,
    content_class TEXT NOT NULL CHECK (content_class IN ('FACT','EXPERIENCE','OBSERVATION','DECISION','RATIONALE','FAILURE','PROCEDURE','ENVIRONMENT','CONSTRAINT','LEARNING','HYPOTHESIS')),
    content TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('STORED','QUEUED','DUPLICATE','REJECTED','DEGRADED','SUPERSEDED','TOMBSTONED')),
    bank_id TEXT NOT NULL,
    branch_context TEXT,
    source_revision TEXT,
    created_at TIMESTAMPTZ NOT NULL,
    supersedes_memory_id TEXT REFERENCES prime_core.memory_records(memory_id) ON DELETE SET NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);
CREATE UNIQUE INDEX IF NOT EXISTS memory_project_hash_idx ON prime_core.memory_records(project_id, content_hash) WHERE status NOT IN ('TOMBSTONED','SUPERSEDED');

CREATE TABLE IF NOT EXISTS prime_core.memory_corrections (
    correction_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    memory_id TEXT NOT NULL REFERENCES prime_core.memory_records(memory_id) ON DELETE CASCADE,
    correction_type TEXT NOT NULL CHECK (correction_type IN ('SUPERSEDE','TOMBSTONE','RETRACT')),
    reason TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    actor_type TEXT NOT NULL,
    actor_id TEXT NOT NULL
);
