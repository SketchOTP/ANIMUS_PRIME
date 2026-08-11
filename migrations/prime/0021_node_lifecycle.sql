ALTER TABLE prime_core.nodes
    ADD COLUMN IF NOT EXISTS protocol_version TEXT NOT NULL DEFAULT 'node-control-v1',
    ADD COLUMN IF NOT EXISTS node_version TEXT NOT NULL DEFAULT '1.0.0',
    ADD COLUMN IF NOT EXISTS approval_state TEXT NOT NULL DEFAULT 'APPROVED',
    ADD COLUMN IF NOT EXISTS last_heartbeat_at TIMESTAMPTZ,
    ADD COLUMN IF NOT EXISTS compatibility_state TEXT NOT NULL DEFAULT 'COMPATIBLE',
    ADD COLUMN IF NOT EXISTS diagnostics JSONB NOT NULL DEFAULT '{}'::jsonb;

CREATE INDEX IF NOT EXISTS nodes_health_idx ON prime_core.nodes(status, last_seen_at);
