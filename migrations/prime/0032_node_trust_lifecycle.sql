ALTER TABLE prime_core.nodes
    ADD COLUMN IF NOT EXISTS control_endpoint TEXT,
    ADD COLUMN IF NOT EXISTS certificate_fingerprint TEXT,
    ADD COLUMN IF NOT EXISTS certificate_serial TEXT,
    ADD COLUMN IF NOT EXISTS certificate_issued_at TIMESTAMPTZ,
    ADD COLUMN IF NOT EXISTS certificate_expires_at TIMESTAMPTZ,
    ADD COLUMN IF NOT EXISTS credential_ref TEXT,
    ADD COLUMN IF NOT EXISTS trust_state TEXT NOT NULL DEFAULT 'UNTRUSTED';

CREATE TABLE IF NOT EXISTS prime_core.node_enrollment_challenges (
    challenge_id TEXT PRIMARY KEY,
    node_id TEXT NOT NULL REFERENCES prime_core.nodes(node_id) ON DELETE RESTRICT,
    token_digest TEXT NOT NULL UNIQUE,
    issued_at TIMESTAMPTZ NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL,
    consumed_at TIMESTAMPTZ,
    revoked_at TIMESTAMPTZ,
    state TEXT NOT NULL CHECK (state IN ('BOOTSTRAP_ISSUED','NODE_PROOF_RECEIVED','PENDING_OPERATOR_APPROVAL','APPROVED','REJECTED','EXPIRED')),
    csr_pem TEXT,
    csr_fingerprint TEXT,
    requested_metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    approved_at TIMESTAMPTZ,
    rejected_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS node_enrollment_state_idx
    ON prime_core.node_enrollment_challenges(node_id, state, expires_at);
