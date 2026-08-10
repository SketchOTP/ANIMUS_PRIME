# Current State

## Lifecycle

- Status: `ADOPTED`
- Last updated: `2026-08-10T17:05:00Z`

## Active state after adoption

- Local directive ID: `D-PRIME-PHASE0-001`
- External directive ID: `NONE`
- Objective: `Build and qualify ANIMUS PRIME through Phase 15 against PRIME-SPEC-V1.0.0.`
- Current status: `IN_PROGRESS`
- Acceptance: `Phase 0 through Phase 2 PASS; proceed sequentially with exact qualified Git commits.`
- Current phase: `2`
- Expected or actual touched areas: `apps/node, src/prime_node, migrations/prime/0002_nodes.sql, tests/phase2, Dockerfile.node, docs, .agent`
- Immediate next action: `Begin Phase 3 project onboarding, .agent authority, and goal approval.`

## Temporary task-relevant facts

Approved baseline: `PRIME-SPEC-V1.0.0`; handoff manifest: `48306047cbd84df583bca6530f25d3dd3c1674d490d11a6e621add0238f36ec9`.

## Last validation after adoption

- Command or check: `pytest tests/phase0 tests/phase1 tests/phase2 -q; scripts/phase1_qualify.py; scripts/phase2_qualify.py; Core/Node health`
- Result: `PASSED`

## Risks

- Phases 2–15 remain unimplemented and unqualified.

## Blockers

- None.

## Pending decisions

- None.

## Status vocabulary

Allowed adopted-project statuses: `IDLE`, `PLANNING`, `IN_PROGRESS`, `VALIDATING`, `BLOCKED`, `COMPLETE`. `CURRENT.md` is mutable and never replaces historical ledgers. Reset it to `IDLE` when an adopted task closes.
