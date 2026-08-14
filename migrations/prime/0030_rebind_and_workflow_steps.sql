ALTER TABLE prime_core.project_bindings
    ADD COLUMN IF NOT EXISTS binding_revision BIGINT NOT NULL DEFAULT 0;

CREATE TABLE IF NOT EXISTS prime_core.repository_continuity_anchors (
    anchor_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    repository_id TEXT NOT NULL REFERENCES prime_core.repositories(repository_id) ON DELETE RESTRICT,
    canonical_ref TEXT NOT NULL,
    canonical_ref_commit TEXT NOT NULL,
    canonical_revision TEXT,
    canonical_tree TEXT,
    known_objects JSONB NOT NULL DEFAULT '[]'::jsonb,
    authority_project_hash TEXT,
    worktree_path TEXT NOT NULL,
    identity_fingerprint TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);
CREATE UNIQUE INDEX IF NOT EXISTS repository_continuity_anchor_current_idx
    ON prime_core.repository_continuity_anchors(project_id, repository_id, canonical_ref, canonical_ref_commit);

CREATE TABLE IF NOT EXISTS prime_core.repository_rebind_preflights (
    preflight_token TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    repository_id TEXT NOT NULL REFERENCES prime_core.repositories(repository_id) ON DELETE RESTRICT,
    destination_node_id TEXT NOT NULL REFERENCES prime_core.nodes(node_id) ON DELETE RESTRICT,
    destination_path TEXT NOT NULL,
    candidate_fingerprint TEXT NOT NULL,
    candidate_head TEXT NOT NULL,
    binding_revision BIGINT NOT NULL,
    snapshot JSONB NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('OPEN','CONSUMED','STALE','REJECTED')),
    created_at TIMESTAMPTZ NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL,
    consumed_at TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS repository_rebind_preflight_project_idx
    ON prime_core.repository_rebind_preflights(project_id, created_at DESC);

CREATE TABLE IF NOT EXISTS prime_core.repository_rebind_history (
    rebind_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    repository_id TEXT NOT NULL REFERENCES prime_core.repositories(repository_id) ON DELETE RESTRICT,
    previous_node_id TEXT NOT NULL,
    previous_path TEXT NOT NULL,
    previous_fingerprint TEXT NOT NULL,
    new_node_id TEXT NOT NULL,
    new_path TEXT NOT NULL,
    new_fingerprint TEXT NOT NULL,
    continuity_verdict TEXT NOT NULL,
    evidence JSONB NOT NULL DEFAULT '{}'::jsonb,
    occurred_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS prime_core.workflow_steps (
    workflow_id TEXT NOT NULL REFERENCES prime_core.workflows(workflow_id) ON DELETE CASCADE,
    step_key TEXT NOT NULL,
    step_order INTEGER NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('PENDING','RUNNING','SUCCEEDED','FAILED_RETRYABLE','FAILED_FINAL','REPAIR_REQUIRED','COMPENSATED')),
    attempt_count INTEGER NOT NULL DEFAULT 0,
    replay_policy TEXT NOT NULL CHECK (replay_policy IN ('PURE_OR_DB_TRANSACTION','IDEMPOTENT_EXTERNAL','NON_IDEMPOTENT_EXTERNAL')),
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    last_error TEXT,
    input_metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    result_metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    side_effect_state JSONB NOT NULL DEFAULT '{}'::jsonb,
    PRIMARY KEY (workflow_id, step_key),
    UNIQUE (workflow_id, step_order)
);
CREATE INDEX IF NOT EXISTS workflow_steps_resume_idx
    ON prime_core.workflow_steps(workflow_id, step_order, status);

CREATE TABLE IF NOT EXISTS prime_core.workflow_resources (
    resource_id TEXT PRIMARY KEY,
    workflow_id TEXT NOT NULL REFERENCES prime_core.workflows(workflow_id) ON DELETE CASCADE,
    resource_type TEXT NOT NULL,
    resource_key TEXT NOT NULL,
    resource_locator TEXT,
    status TEXT NOT NULL CHECK (status IN ('EXPECTED','CREATED','RECONCILIATION_REQUIRED','RELEASED')),
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL,
    UNIQUE (workflow_id, resource_type, resource_key)
);
