CREATE TABLE IF NOT EXISTS prime_core.progress_corrections (
    correction_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    assessment_id TEXT NOT NULL REFERENCES prime_core.progress_assessments(assessment_id) ON DELETE RESTRICT,
    goal_revision_id TEXT NOT NULL REFERENCES prime_core.goal_revisions(goal_revision_id) ON DELETE RESTRICT,
    category TEXT NOT NULL CHECK (category IN ('MISSED_EVIDENCE','INCORRECT_INTERPRETATION','STALE_SOURCE','WRONG_STATUS','BAD_GOAL_MODEL')),
    reason TEXT NOT NULL,
    operator_id TEXT NOT NULL,
    source_refs JSONB NOT NULL DEFAULT '[]'::jsonb,
    status TEXT NOT NULL CHECK (status IN ('OPEN','REASSESSED','RESOLVED','REJECTED')) DEFAULT 'OPEN',
    created_at TIMESTAMPTZ NOT NULL,
    reassessment_id TEXT REFERENCES prime_core.progress_assessments(assessment_id) ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS progress_corrections_project_idx
    ON prime_core.progress_corrections(project_id, created_at DESC);
