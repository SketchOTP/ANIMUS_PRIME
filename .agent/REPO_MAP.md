# Repository Map

## Entry points

- `README.md` — project boundary and phase gate.
- `scripts/phase0_qualify.py` — Phase 0 source-lock qualification entry point.

## Core modules

- `src/` — implementation modules added by owning phases.
- `authority-template/v1/` — approved authority bootstrap package.

## Interfaces and contracts

- `contracts/` — versioned shared domain, authority, isolation, storage, and privacy contracts.
- `baseline/implementation-baseline.yaml` — active immutable-baseline identity.

## Tests and validation

- `tests/phase0/` — source-lock, contract, and adapter qualification tests.
- `.github/workflows/phase0.yml` — CI qualification entry point.

## Configuration

- `docker-compose.phase0.yml` — pinned PostgreSQL/pgvector/Hindsight qualification stack.
- `dependencies/pins.yaml` — exact dependency and image pins.

## Generated areas

- `evidence/phase0/` — redacted qualification evidence.
- `authority-template/v1/MANIFEST.sha256` — generated content manifest for the approved template.

## External integration points

- `baseline/*.notion.md` — frozen Notion source and handoff exports.
- `dependencies/` — upstream release and license evidence.

## Areas that must not be edited manually

- `baseline/` — immutable after source lock; changes require a new baseline.
- `authority-template/v1/` — changes require a new template version and manifest.
