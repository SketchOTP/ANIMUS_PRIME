ALTER TABLE prime_core.operators
    ADD COLUMN IF NOT EXISTS local_identity_hash TEXT;

CREATE TABLE IF NOT EXISTS prime_core.auth_challenges (
    challenge_id TEXT PRIMARY KEY,
    operator_id TEXT NOT NULL REFERENCES prime_core.operators(operator_id),
    purpose TEXT NOT NULL CHECK (purpose IN ('SIGN_IN', 'STEP_UP')),
    approval_code_hash TEXT NOT NULL,
    browser_nonce_hash TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL,
    approved_at TIMESTAMPTZ,
    consumed_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS auth_challenges_lookup_idx
    ON prime_core.auth_challenges(approval_code_hash, purpose, expires_at);

CREATE INDEX IF NOT EXISTS auth_challenges_browser_idx
    ON prime_core.auth_challenges(challenge_id, browser_nonce_hash, expires_at);
