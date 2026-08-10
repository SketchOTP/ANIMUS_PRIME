# Current State

## Lifecycle

- Status: `ADOPTED`
- Last updated: `2026-08-10T22:42:18Z`

## Active state after adoption

- Local directive ID: `D-PRIME-PHASE0-001`
- External directive ID: `NONE`
- Objective: `Build and qualify ANIMUS PRIME through Phase 15 against PRIME-SPEC-V1.0.0.`
- Current status: `IN_PROGRESS`
- Acceptance: `Phase 0 through Phase 14 PASS; Phase 15 mechanical regression PASS but V1 Definition-of-Done gate FAIL.`
- Current phase: `15`
- Expected or actual touched areas: `R1-R6 remediation foundations, Core↔Node client, apps/core, apps/web, docs/phase15-remediation-matrix.yaml, evidence/phase15`
- Immediate next action: `Qualify each open remediation requirement from the detailed ledger; R-031 has local TLS/mTLS process evidence but remains open pending native Linux/Windows service evidence.`

## Temporary task-relevant facts

Approved baseline: `PRIME-SPEC-V1.0.0`; handoff manifest: `48306047cbd84df583bca6530f25d3dd3c1674d490d11a6e621add0238f36ec9`.

## Last validation after adoption

- Command or check: `python3 -m pytest tests -q; python3 scripts/phase15_qualify.py`
- Result: `FAILED`

## Risks

- Phase 15 V1 release gate failed on seven explicit normative gap categories in evidence/phase15/qualification-report.md.
- Release-gap reconciliation reopened R-005, R-008, R-011, R-014, R-015, R-017, R-018, R-020, R-023 and R-024; granular rows R-031 through R-056 are IMPLEMENTING.
- Historical phase PASS records remain unchanged audit evidence and are superseded for final release verification only where the remediation matrix says so.
- Requirement-level ledger added at `docs/phase15-remediation-qualification-ledger.yaml` and linked from the release matrix.
- R-031 implementation tightened: packaged Node service now refuses service-mode startup without complete TLS/mTLS files; disposable Compose qualification explicitly opts into insecure HTTP.
- Local real-process HTTPS/mTLS evidence recorded at `evidence/phase15/R-031-local-tls-mtls-process.md`.
- R-031 remains `IMPLEMENTING` / `OPEN`; native Linux service, Windows service, restart/reboot, offline recovery, and upgrade evidence are not present.

## Blockers

- None.

## Pending decisions

- None.

## Status vocabulary

Allowed adopted-project statuses: `IDLE`, `PLANNING`, `IN_PROGRESS`, `VALIDATING`, `BLOCKED`, `COMPLETE`. `CURRENT.md` is mutable and never replaces historical ledgers. Reset it to `IDLE` when an adopted task closes.
