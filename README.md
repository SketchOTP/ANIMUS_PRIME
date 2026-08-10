# ANIMUS PRIME

ANIMUS PRIME is local-first project continuity infrastructure for repository-backed AI-assisted engineering projects. PRIME preserves project identity, authority, evidence, memory, documentation, and resumability; Codex remains the engineering worker.

## Baseline

Implementation is authorized against `PRIME-SPEC-V1.0.0`. The immutable source exports and handoff identity are in `baseline/`. Phase 1+ implementation is gated on a recorded Phase 0 `PASS`.

## Phase 0 status

Phase 0 establishes the source lock, authority contract, domain contracts, threat model, dependency pins, test harness, and qualification evidence. It must pass before feature implementation begins.

## Repository conventions

- `contracts/` — versioned shared contracts and invariant definitions.
- `baseline/` — frozen specification and implementation-baseline identity.
- `authority-template/v1/` — materialized approved authority package.
- `dependencies/` — exact pins, compatibility evidence, notices, and SBOM inputs.
- `docs/` — implementation governance and traceability.
- `tests/phase0/` — Phase 0 contract and source-lock tests.
- `.agent/phase-records/` — append-only phase qualification records.

No normal monitoring or intelligence path may edit application source files. Lifecycle writes require explicit, auditable operations.
