# ANIMUS PRIME Project Profile

## Lifecycle

- Status: `ADOPTED`
- Last verified: `2026-08-10T23:12:00Z`

## Identity

- Project name or identifier: `ANIMUS PRIME`
- Purpose: `Local-first project continuity and intelligence layer for repository-backed AI-assisted engineering projects.`
- Repository root: `/home/sketch/Projects/ANIMUS_PRIME`
- Verified remote: `git@github.com:SketchOTP/ANIMUS_PRIME.git — canonical GitHub publication; local checkout remains the implementation authority`
- Maturity or current phase: `Phase 15 remediation — requirement-level qualification in progress`

## Languages and runtimes

- Python 3.13.7 backend baseline; Node 20.19.0 frontend tooling baseline; PostgreSQL 17.10 and Hindsight 0.6.1 services.

## Tools

- Build: `docker compose -f docker-compose.phase1.yml build core node`
- Test: `python3 -m pytest tests -q`
- Lint: `NOT CONFIGURED — qualification uses compileall and governance checks`
- Type-check: `NOT CONFIGURED — qualification uses compileall and runtime tests`
- Packaging: `Docker Compose pinned Core/Node qualification; native Linux/Windows packaging remains open in R-031/R-032`
- Preferred navigation/indexing: `codebase-memory-mcp, then targeted rg for non-code assets`
- Project-specific commands: `python3 -m pytest tests/phase0 -q; python3 scripts/phase0_qualify.py`

## Verified commands

Reference authority package validator: `python3 authority-template/v1/scripts/validate_governance.py` with its clean-package mode.
- `python3 scripts/validate_governance.py --mode ADOPTED`
- `python3 scripts/phase0_qualify.py`
- `python3 scripts/phase15_qualify.py`

## Constraints

- Platform/compatibility: `Linux amd64 qualification host; containerized Core/Node qualification is available; native Windows Node qualification remains an external requirement.`
- Security: `One trusted operator; project isolation; private Tailscale-only remote access; no public Funnel.`
- Data handling: `Local-first, deny-by-default egress, redacted logs, no secrets/raw logs in governance memory.`
- Deployment: `PostgreSQL canonical persistence and separately owned Hindsight service in a supported PostgreSQL cluster.`
