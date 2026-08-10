ALTER TABLE prime_core.evidence_records
    ADD COLUMN IF NOT EXISTS retracted_at TIMESTAMPTZ,
    ADD COLUMN IF NOT EXISTS retraction_reason TEXT,
    ADD COLUMN IF NOT EXISTS index_status TEXT NOT NULL DEFAULT 'UNAVAILABLE';

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'evidence_records_index_status_check'
          AND conrelid = 'prime_core.evidence_records'::regclass
    ) THEN
        ALTER TABLE prime_core.evidence_records
            ADD CONSTRAINT evidence_records_index_status_check
            CHECK (index_status IN ('PENDING', 'READY', 'UNAVAILABLE', 'FAILED'));
    END IF;
END $$;
