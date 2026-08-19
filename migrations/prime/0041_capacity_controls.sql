-- Continuation 096G: activate durable global/project capacity controls.
ALTER TABLE prime_core.capacity_policies
    ADD COLUMN IF NOT EXISTS running_limit INTEGER;

CREATE INDEX IF NOT EXISTS jobs_project_status_created_idx
    ON prime_core.jobs(project_id, status, created_at);

