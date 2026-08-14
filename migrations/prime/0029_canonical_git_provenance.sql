ALTER TABLE prime_core.project_bindings
    ADD COLUMN IF NOT EXISTS canonical_ref TEXT,
    ADD COLUMN IF NOT EXISTS canonical_ref_commit TEXT,
    ADD COLUMN IF NOT EXISTS canonical_ref_updated_at TIMESTAMPTZ;
