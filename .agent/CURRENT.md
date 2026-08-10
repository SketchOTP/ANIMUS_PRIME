# Current State

## Lifecycle

- Status: `ADOPTED`
- Last updated: `2026-08-10T15:41:00Z`

## Active state after adoption

- Local directive ID: `D-PRIME-PHASE0-001`
- External directive ID: `NONE`
- Objective: `Qualify Phase 0 source lock, contracts, dependencies, threat model, and harness against PRIME-SPEC-V1.0.0.`
- Current status: `IN_PROGRESS`
- Acceptance: `Phase 0 PASS with exact qualified Git commit; then advance sequentially.`
- Current phase: `0`
- Expected or actual touched areas: `baseline, authority-template/v1, contracts, dependencies, threat-model, docs, tests/phase0, .agent`
- Immediate next action: `Complete runtime smoke and Phase 0 qualification.`

## Temporary task-relevant facts

- Approved baseline: `PRIME-SPEC-V1.0.0`; handoff manifest: `48306047cbd84df583bca6530f25d3dd3c1674d490d11a6e621add0238f36ec9`.

## Last validation after adoption

- Command or check: `authority-template/v1/scripts/validate_governance.py --mode TEMPLATE`
- Result: `PASSED`

## Risks

- Runtime dependency smoke and Phase 0 qualification remain open.

## Blockers

- None.

## Pending decisions

- None.

## Status vocabulary

Allowed adopted-project statuses: `IDLE`, `PLANNING`, `IN_PROGRESS`, `VALIDATING`, `BLOCKED`, `COMPLETE`. `CURRENT.md` is mutable and never replaces historical ledgers. Reset it to `IDLE` when an adopted task closes.
