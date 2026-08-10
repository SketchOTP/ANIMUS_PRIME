CREATE TABLE IF NOT EXISTS prime_core.progress_baseline_reviews (
    review_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    goal_revision_id TEXT NOT NULL REFERENCES prime_core.goal_revisions(goal_revision_id) ON DELETE CASCADE,
    items JSONB NOT NULL,
    weights_sum NUMERIC NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('PENDING','APPROVED','REJECTED')),
    created_at TIMESTAMPTZ NOT NULL,
    approved_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS prime_core.goal_items (
    goal_item_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    goal_revision_id TEXT NOT NULL REFERENCES prime_core.goal_revisions(goal_revision_id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    weight NUMERIC NOT NULL,
    required BOOLEAN NOT NULL,
    acceptance_expectations JSONB NOT NULL DEFAULT '[]'::jsonb,
    UNIQUE(goal_revision_id, goal_item_id)
);

CREATE TABLE IF NOT EXISTS prime_core.progress_assessments (
    assessment_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    goal_revision_id TEXT NOT NULL REFERENCES prime_core.goal_revisions(goal_revision_id) ON DELETE CASCADE,
    repository_revision TEXT,
    progress_percent NUMERIC NOT NULL,
    confidence NUMERIC NOT NULL,
    freshness_state TEXT NOT NULL CHECK (freshness_state IN ('CURRENT','STALE','UNKNOWN')),
    summary TEXT NOT NULL,
    item_results JSONB NOT NULL,
    evidence_refs JSONB NOT NULL DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ NOT NULL
);
