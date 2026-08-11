CREATE TABLE IF NOT EXISTS prime_core.ai_runs (
    run_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    function TEXT NOT NULL,
    provider TEXT NOT NULL,
    model TEXT NOT NULL,
    profile_revision TEXT NOT NULL,
    prompt_revision TEXT NOT NULL,
    schema_revision TEXT NOT NULL,
    retrieval_policy_revision TEXT NOT NULL,
    fixture_revision TEXT NOT NULL,
    privacy_mode TEXT NOT NULL CHECK (privacy_mode IN ('CLOUD_MODELS_ALLOWED','LOCAL_ONLY')),
    source_revision_set JSONB NOT NULL DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ NOT NULL,
    status TEXT NOT NULL,
    latency_ms NUMERIC,
    input_tokens INTEGER,
    output_tokens INTEGER,
    estimated_cost NUMERIC,
    provider_usage JSONB NOT NULL DEFAULT '{}'::jsonb,
    error_class TEXT,
    result JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS ai_runs_project_created_idx
    ON prime_core.ai_runs(project_id, created_at DESC);

CREATE INDEX IF NOT EXISTS ai_runs_function_status_idx
    ON prime_core.ai_runs(function, status, created_at DESC);
