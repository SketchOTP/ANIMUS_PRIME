# Current State

## Lifecycle

- Status: `ADOPTED`
- Last updated: `2026-08-11T01:24:00Z`

## Active state after adoption

- Local directive ID: `D-PRIME-PHASE15-REMEDIATION-007`
- External directive ID: `NONE`
- Objective: `Build and qualify ANIMUS PRIME through Phase 15 against PRIME-SPEC-V1.0.0.`
- Current status: `IN_PROGRESS`
- Acceptance: `Phase 0 through Phase 14 PASS; Phase 15 mechanical regression PASS but V1 Definition-of-Done gate FAIL.`
- Current phase: `15`
- Expected or actual touched areas: `R-046/R-050 Evidence/history cluster, apps/core, src/prime_core/history_service.py, src/prime_core/brain_service.py, src/prime_core/intelligence_service.py, src/prime_core/history_primitives.py, migrations/prime/0017-0019, tests/phase11, docs/phase15 ledger/matrix, evidence/phase15`
- Immediate next action: `Advance to R-042–R-045 backup/restore/capacity implementation while preserving the R-046–R-050 partial qualification state; then continue remaining local implementation rows and native/live qualification.`

## Temporary task-relevant facts

Approved baseline: `PRIME-SPEC-V1.0.0`; handoff manifest: `48306047cbd84df583bca6530f25d3dd3c1674d490d11a6e621add0238f36ec9`.

## Last validation after adoption

- Command or check: `python3 scripts/validate_governance.py --mode ADOPTED`
- Result: `PASSED`

## Risks

- Phase 15 V1 release gate failed on seven explicit normative gap categories in evidence/phase15/qualification-report.md.
- Release-gap reconciliation reopened R-005, R-008, R-011, R-014, R-015, R-017, R-018, R-020, R-023 and R-024; granular rows R-031 through R-045 and R-051 through R-056 remain IMPLEMENTING, while R-046 through R-050 are IMPLEMENTED.
- Historical phase PASS records remain unchanged audit evidence and are superseded for final release verification only where the remediation matrix says so.
- Requirement-level ledger added at `docs/phase15-remediation-qualification-ledger.yaml` and linked from the release matrix.
- R-031 implementation tightened: packaged Node service now refuses service-mode startup without complete TLS/mTLS files; disposable Compose qualification explicitly opts into insecure HTTP.
- Local real-process HTTPS/mTLS evidence recorded at `evidence/phase15/R-031-local-tls-mtls-process.md`.
- R-031 remains `IMPLEMENTING` / `OPEN`; native Linux service, Windows service, restart/reboot, offline recovery, and upgrade evidence are not present.
- Full disposable Phase-15 run recorded at `evidence/phase15/remediation-qualification-003.md`: 38 tests and Phases 1–14 passed; V1 gate correctly failed on open remediation rows.
- Continuation 004 requires the ledger fields `original_owning_phase`, `native_or_live_execution_required`, `evidence_paths`, `implementation_commit`, `evidence_commit`, and `remaining_gap`; the ledger now conforms.
- Codebase-memory MCP indexing was attempted before local discovery but returned `Transport closed`; repository mapping used targeted tracked-file inspection as the documented fallback.
- Continuation 005 skip inventory records all 15 skipped tests, their PostgreSQL prerequisite, affected requirements, and release-blocking status.
- Continuation 005 deterministic qualification procedures cover native Node, Tailscale, live Notion, backup/restore/capacity, Evidence/Time Lens, browser UX, approved AI, and full V1 walkthroughs.
- R-046/R-047 implementation preflight added project-scoped Evidence upload/reference/list/retraction routes and explicit parser/index status; no requirement was promoted to VERIFIED.
- Continuation 006 added durable Evidence source references, safe HTTPS/Node locators, bounded inert-text extraction, Evidence quota/annotation/link boundaries, historical cutoff context, historical Ask context, and PRIME-owned Git checkpoint bundle preservation.
- Continuation 007 closes local implementation for R-046–R-050: explicit Evidence storage/lifecycle/parser states, durable citation mutation semantics, append-only historical snapshots, actual PostgreSQL Git checkpoint registration, retained bundle reconstruction, historical Ask/Brain, and Return to Now. Latest governed implementation commit is `723809e`; Continuation 007 evidence/governance commit is `a617ae5`; final outcome correction is recorded in `OUTCOMES.md`.
- Clean disposable Phase-15 mechanical run passed 43 tests and Phases 1–14; the V1 requirement gate correctly remained `FAIL`.
- R-046–R-050 remain `qualification_status=partial`; R-049 is still `IMPLEMENTED`, not `VERIFIED`, until the complete release qualification succeeds.
- Separate remediation qualification states now exist for all R-031–R-056 rows; skipped/unavailable environments do not imply implementation completion.
- Remediation counts — `implementation_complete=5/26`, `IMPLEMENTING=21`, `OPEN=26`, `BLOCKED=0`, `VERIFIED=0`; qualification `partial=5`, `blocked_by_environment=21`; `VERIFIED / 26 = 0/26`.

## Blockers

- System Python lacks `psycopg`, and the default host `PRIME_PHASE1_DB_URL` is unset; the qualified `.venv` plus disposable PostgreSQL path was exercised for local evidence. Native Windows/Linux service, live Notion/Tailscale, backup/restore target, approved AI, browser, and full end-to-end environments remain unqualified.

## Pending decisions

- None.

## Status vocabulary

Allowed adopted-project statuses: `IDLE`, `PLANNING`, `IN_PROGRESS`, `VALIDATING`, `BLOCKED`, `COMPLETE`. `CURRENT.md` is mutable and never replaces historical ledgers. Reset it to `IDLE` when an adopted task closes.
