ALTER TABLE prime_core.projects
    ADD COLUMN IF NOT EXISTS description TEXT NOT NULL DEFAULT '',
    ADD COLUMN IF NOT EXISTS image_url TEXT,
    ADD COLUMN IF NOT EXISTS onboarding_step TEXT NOT NULL DEFAULT 'IDENTITY',
    ADD COLUMN IF NOT EXISTS onboarding_state TEXT NOT NULL DEFAULT 'IN_PROGRESS';

CREATE INDEX IF NOT EXISTS projects_onboarding_idx
    ON prime_core.projects(onboarding_state, onboarding_step);
