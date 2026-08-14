ALTER TABLE prime_core.operators
    ADD COLUMN IF NOT EXISTS local_recovery_hash TEXT;
