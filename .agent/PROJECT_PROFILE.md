# ANIMUS PRIME Project Profile

## Lifecycle

- Status: `ADOPTED`
- Last verified: `2026-08-10T15:41:00Z`

## Identity

- Project name or identifier: `ANIMUS PRIME`
- Purpose: `Local-first project continuity and intelligence layer for repository-backed AI-assisted engineering projects.`
- Repository root: `/home/sketch/Projects/ANIMUS_PRIME`
- Verified remote: `NONE — local canonical implementation repository`
- Maturity or current phase: `Phase 0 — source lock and contracts`

## Languages and runtimes

- Python 3.13.7 backend baseline; Node 20.19.0 frontend tooling baseline; PostgreSQL 17.10 and Hindsight 0.6.1 services.

## Tools

- Build: `NOT RUN — feature skeleton is Phase 1+`
- Test: `python3 -m pytest tests/phase0`
- Lint: `NOT CONFIGURED — Phase 0 contract-only repository`
- Type-check: `NOT CONFIGURED — Phase 0 contract-only repository`
- Packaging: `Docker Compose pinned baseline; qualification in Phase 0`
- Preferred navigation/indexing: `codebase-memory-mcp, then targeted rg for non-code assets`

## Verified commands

- Governance template validation: `python3 authority-template/v1/scripts/validate_governance.py --mode TEMPLATE`
- Adopted-project validation: `python3 scripts/validate_governance.py --mode ADOPTED`
- Phase 0 qualification: `python3 scripts/phase0_qualify.py`

## Constraints

- Platform/compatibility: `Linux amd64 qualification host; containerized production posture; Windows Node compatibility is later-phase qualification.`
- Security: `One trusted operator; project isolation; private Tailscale-only remote access; no public Funnel.`
- Data handling: `Local-first, deny-by-default egress, redacted logs, no secrets/raw logs in governance memory.`
- Deployment: `PostgreSQL canonical persistence and separately owned Hindsight service in a supported PostgreSQL cluster.`

## Adoption guidance

The active implementation baseline is recorded in `baseline/implementation-baseline.yaml`. Normative changes require a `SpecChangeRecord` and new baseline.
