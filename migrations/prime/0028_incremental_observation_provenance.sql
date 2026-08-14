ALTER TABLE prime_core.repository_files
    ADD COLUMN IF NOT EXISTS observation_basis TEXT NOT NULL DEFAULT 'COMMITTED_CANONICAL',
    ADD COLUMN IF NOT EXISTS canonical_revision TEXT,
    ADD COLUMN IF NOT EXISTS worktree_branch TEXT,
    ADD COLUMN IF NOT EXISTS worktree_path TEXT;
