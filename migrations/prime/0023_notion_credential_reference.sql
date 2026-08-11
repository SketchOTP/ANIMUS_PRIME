-- Continuation 012: secret-free MyAssistant authorization reference metadata.
CREATE TABLE IF NOT EXISTS prime_core.notion_credential_references (
    credential_reference_id TEXT PRIMARY KEY,
    credential_reference TEXT NOT NULL UNIQUE,
    source_kind TEXT NOT NULL,
    source_environment TEXT NOT NULL,
    migration_status TEXT NOT NULL CHECK (migration_status IN ('IMPORTED','NOOP','CONFLICT','SOURCE_ABSENT','REAUTH_REQUIRED','DEGRADED')),
    workspace_id TEXT,
    integration_actor_id TEXT,
    granted_page_id TEXT,
    read_access TEXT NOT NULL DEFAULT 'UNKNOWN',
    write_access TEXT NOT NULL DEFAULT 'UNKNOWN',
    capabilities JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
