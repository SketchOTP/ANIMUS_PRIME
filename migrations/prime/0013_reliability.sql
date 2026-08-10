CREATE TABLE IF NOT EXISTS prime_core.backup_records (
    backup_id TEXT PRIMARY KEY,
    backup_type TEXT NOT NULL CHECK (backup_type IN ('CORE_DB','MEMORY_LEDGER','HINDSIGHT_EXPORT','CONFIG_REFERENCE')),
    locator TEXT NOT NULL,
    content_hash TEXT,
    status TEXT NOT NULL CHECK (status IN ('STARTED','VERIFIED','FAILED','STALE')),
    captured_at TIMESTAMPTZ NOT NULL,
    verified_at TIMESTAMPTZ,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE IF NOT EXISTS prime_core.diagnostic_samples (
    sample_id TEXT PRIMARY KEY,
    component TEXT NOT NULL,
    status TEXT NOT NULL,
    metrics JSONB NOT NULL DEFAULT '{}'::jsonb,
    observed_at TIMESTAMPTZ NOT NULL
);
