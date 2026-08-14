ALTER TABLE prime_core.sessions
    ADD COLUMN IF NOT EXISTS step_up_at TIMESTAMPTZ;

CREATE INDEX IF NOT EXISTS sessions_step_up_idx
    ON prime_core.sessions(step_up_at)
    WHERE revoked_at IS NULL AND step_up_at IS NOT NULL;
