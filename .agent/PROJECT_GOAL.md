# ANIMUS PRIME Project Goal

## Lifecycle

- Status: `ADOPTED`
- Last verified: `2026-08-10T15:41:00Z`

## Goal

Build ANIMUS PRIME V1 as local-first, project-isolated continuity infrastructure for repository-backed AI-assisted engineering projects. PRIME preserves project identity, authority, repository/Git evidence, durable Hindsight-backed memory, documentation, progress, and resumable context while Codex remains responsible for engineering work.

## Observable success measures

- A single trusted operator can install, configure, use, recover, and qualify PRIME through the complete approved V1 workflow.
- Every managed project has one primary Git repository, isolated authority, memory, indexing, events, Notion state, credentials, progress, and MCP scope.
- All derived answers and progress are source-grounded, cited, freshness-aware, and honest about degraded states.
- Phase 0 through Phase 15 qualify against `PRIME-SPEC-V1.0.0` with zero unassigned or unverified V1 requirements.

## Scope

- PRIME Core, Nodes, onboarding, authority bootstrap, repository/Git read model, events/jobs, Hindsight adapter, PRIME Memory MCP, Notion Documentation Agent, progress, Ask/Search, Project Brain, Evidence, Time Lens, Fork/Clone, lifecycle, Tailscale-only access, reliability, backups, recovery, and operator UX as defined by the approved specification.

## Non-goals

- PRIME is not a coding agent, autonomous coding loop, generic knowledge connector, cross-project reasoning system, or public MCP service.
- Dreaming Loop execution and Oracle execution are future-only by the approved specification.

## Constraints

- One trusted operator; local access plus private Tailscale tailnet access.
- PostgreSQL is canonical PRIME persistence; Hindsight is the V1 memory engine behind an adapter.
- Repository, Git, `.agent`, and `PROJECT_GOAL.md` remain authoritative for their defined domains.
- Normal observation is read-only; lifecycle and bootstrap writes are explicit, auditable, and recoverable.
- Privacy/egress is deny-by-default and project isolation is release-blocking.

## Governing external specifications

- `baseline/PRIME-SPEC-V1.0.0.notion.md` — `PRIME-SPEC-V1.0.0`.
- `baseline/Implementation-Handoff-Record-PRIME-SPEC-V1.0.0.notion.md`.

## Owner or approval authority

- The single trusted project operator; normative changes require the approved SpecChangeRecord/new-baseline process.
