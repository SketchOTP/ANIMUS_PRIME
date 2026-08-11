-- Continuation 011: project-scoped Notion lifecycle, source provenance and managed history.
ALTER TABLE prime_core.notion_projects
    ADD COLUMN IF NOT EXISTS credential_reference TEXT,
    ADD COLUMN IF NOT EXISTS workspace_id TEXT,
    ADD COLUMN IF NOT EXISTS provider_health JSONB NOT NULL DEFAULT '{}'::jsonb,
    ADD COLUMN IF NOT EXISTS binding_state TEXT NOT NULL DEFAULT 'UNCONFIGURED',
    ADD COLUMN IF NOT EXISTS desired_sync_state TEXT NOT NULL DEFAULT 'ENABLED';

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'notion_projects_binding_state_check') THEN
        ALTER TABLE prime_core.notion_projects ADD CONSTRAINT notion_projects_binding_state_check
            CHECK (binding_state IN ('UNCONFIGURED','CONNECTED','BINDING','BOUND','DEGRADED','ACCESS_LOST','PAGE_MISSING','CONFLICT','REAUTH_REQUIRED'));
    END IF;
END $$;

CREATE TABLE IF NOT EXISTS prime_core.notion_managed_regions (
    region_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    page_id TEXT NOT NULL,
    region_key TEXT NOT NULL,
    block_identity TEXT,
    expected_hash TEXT,
    rendered_hash TEXT,
    updated_provider_revision TEXT,
    updated_at TIMESTAMPTZ NOT NULL,
    UNIQUE(project_id, page_id, region_key)
);

CREATE TABLE IF NOT EXISTS prime_core.notion_documentation_jobs (
    documentation_run_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    source_commit TEXT,
    authority_revision TEXT,
    progress_assessment_id TEXT,
    evidence_refs JSONB NOT NULL DEFAULT '[]'::jsonb,
    managed_sections JSONB NOT NULL DEFAULT '[]'::jsonb,
    rendered_hash TEXT,
    provider_revision TEXT,
    status TEXT NOT NULL,
    attempts INTEGER NOT NULL DEFAULT 0,
    last_error TEXT,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL,
    UNIQUE(project_id, source_commit, managed_sections)
);

CREATE TABLE IF NOT EXISTS prime_core.notion_knowledge_sources (
    source_binding_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    page_id TEXT NOT NULL,
    page_url TEXT,
    access_mode TEXT NOT NULL DEFAULT 'READ_ONLY',
    status TEXT NOT NULL,
    observed_revision TEXT,
    observed_hash TEXT,
    observed_at TIMESTAMPTZ,
    detached_at TIMESTAMPTZ,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    UNIQUE(project_id, page_id)
);

CREATE TABLE IF NOT EXISTS prime_core.notion_source_observations (
    observation_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    source_binding_id TEXT NOT NULL REFERENCES prime_core.notion_knowledge_sources(source_binding_id) ON DELETE CASCADE,
    page_id TEXT NOT NULL,
    block_identity TEXT,
    observed_revision TEXT,
    content_hash TEXT,
    observed_at TIMESTAMPTZ NOT NULL,
    availability_status TEXT NOT NULL,
    content JSONB,
    UNIQUE(project_id, source_binding_id, page_id, observed_revision, content_hash)
);

CREATE TABLE IF NOT EXISTS prime_core.notion_history_pages (
    history_page_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES prime_core.projects(project_id) ON DELETE CASCADE,
    parent_page_id TEXT NOT NULL,
    period TEXT NOT NULL,
    source_revision_start TEXT,
    source_revision_end TEXT,
    managed_content_hash TEXT NOT NULL,
    provider_revision TEXT,
    created_at TIMESTAMPTZ NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    UNIQUE(project_id, period)
);

CREATE INDEX IF NOT EXISTS notion_sources_project_status_idx
    ON prime_core.notion_knowledge_sources(project_id, status);
CREATE INDEX IF NOT EXISTS notion_jobs_project_status_idx
    ON prime_core.notion_documentation_jobs(project_id, status, updated_at);
