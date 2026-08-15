ALTER TABLE prime_core.notifications
    ADD COLUMN IF NOT EXISTS category TEXT NOT NULL DEFAULT 'GENERAL',
    ADD COLUMN IF NOT EXISTS dedupe_key TEXT NOT NULL DEFAULT '',
    ADD COLUMN IF NOT EXISTS source_type TEXT,
    ADD COLUMN IF NOT EXISTS source_ref TEXT,
    ADD COLUMN IF NOT EXISTS first_seen_at TIMESTAMPTZ,
    ADD COLUMN IF NOT EXISTS last_seen_at TIMESTAMPTZ,
    ADD COLUMN IF NOT EXISTS dismissed_at TIMESTAMPTZ,
    ADD COLUMN IF NOT EXISTS metadata JSONB NOT NULL DEFAULT '{}'::jsonb;

UPDATE prime_core.notifications
SET first_seen_at = COALESCE(first_seen_at, created_at),
    last_seen_at = COALESCE(last_seen_at, created_at),
    dedupe_key = COALESCE(NULLIF(dedupe_key, ''), notification_id)
WHERE first_seen_at IS NULL OR last_seen_at IS NULL OR dedupe_key = '';

CREATE INDEX IF NOT EXISTS notifications_project_status_idx
    ON prime_core.notifications(project_id, status, last_seen_at DESC);

CREATE UNIQUE INDEX IF NOT EXISTS notifications_open_dedupe_idx
    ON prime_core.notifications(project_id, category, dedupe_key)
    WHERE status = 'OPEN';
