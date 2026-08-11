-- Keep the historical READY/REJECTED compatibility states while adding the
-- explicit lifecycle states required by the Evidence parser boundary.
ALTER TABLE prime_core.evidence_records
    DROP CONSTRAINT IF EXISTS evidence_records_parser_status_check;

ALTER TABLE prime_core.evidence_records
    ADD CONSTRAINT evidence_records_parser_status_check
    CHECK (parser_status IN ('PENDING','INDEXED','READY','UNSUPPORTED','FAILED','REJECTED','UNAVAILABLE','RETRACTED'));
