# Current State

## Lifecycle

- Status: `ADOPTED`
- Last updated: `2026-08-11T13:28:00Z`

## Active state after adoption

- Local directive ID: `D-PRIME-PHASE15-REMEDIATION-013`
- External directive ID: `NONE`
- Objective: `Build and qualify ANIMUS PRIME through Phase 15 against PRIME-SPEC-V1.0.0.`
- Current status: `IN_PROGRESS`
- Acceptance: `Phase 0 through Phase 14 PASS; Phase 15 mechanical regression PASS but V1 Definition-of-Done gate FAIL.`
- Current phase: `15`
- Expected or actual touched areas: `Core AI profile/execution/provenance boundary, migrations/prime/0024_ai_execution.sql, project-scoped Ask integration, authenticated AI profile/execute routes, golden fixtures, R-054/R-055 ledgers/evidence, MyAssistant runtime-source trace, and .agent governance records`
- Immediate next action: `Run final Phase-15 mechanical qualification, reconcile the exact evidence commit, and retain live provider/local-model, browser, native/live integration, and R-056 qualification blocks.`

## Temporary task-relevant facts

Approved baseline: `PRIME-SPEC-V1.0.0`; handoff manifest: `48306047cbd84df583bca6530f25d3dd3c1674d490d11a6e621add0238f36ec9`.

## Last validation after adoption

- Command or check: `./.venv/bin/python scripts/validate_governance.py --mode ADOPTED`; `./.venv/bin/python -m pytest tests -q`; `./.venv/bin/python -m compileall -q src apps tests`; `git diff --check`; `./.venv/bin/python scripts/phase15_qualify.py`
- Result: `FAILED`

## Risks

- Phase 15 V1 release gate failed on seven explicit normative gap categories in evidence/phase15/qualification-report.md.
- Release-gap reconciliation reopened R-005, R-008, R-011, R-014, R-015, R-017, R-018, R-020, R-023 and R-024; granular rows R-031 through R-045 and R-051 through R-056 remain IMPLEMENTING, while R-046 through R-050 are IMPLEMENTED.
- Historical phase PASS records remain unchanged audit evidence and are superseded for final release verification only where the remediation matrix says so.
- Requirement-level ledger added at `docs/phase15-remediation-qualification-ledger.yaml` and linked from the release matrix.
- R-031 implementation tightened: packaged Node service now refuses service-mode startup without complete TLS/mTLS files; disposable Compose qualification explicitly opts into insecure HTTP.
- Continuation 009 closes local R-031–R-034 implementation with persistent Node lifecycle/health/protocol state, bounded diagnostics/snapshots, persistent allowed roots, private-bind validation, idempotent Linux/Windows service registration paths, and focused path/identity tests. Native Linux/Windows and qualified private deployment remain unqualified.
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
- Continuation 008 closes local R-042–R-045 implementation: authenticated continuity v2 backup/manifest, clean restore workflow, component fidelity/rebuild semantics, schedule persistence, quotas, retention, queue/disk backpressure, coalescing helpers, and recovery regression protection. R-042–R-045 remain `qualification_status=partial` because separate off-machine, fresh-install/destructive, live Hindsight, interrupted-restore, and sustained capacity evidence is not complete. Governed implementation commit: `7b5ef0a`; evidence/governance commit: `342fc58`.
- Separate remediation qualification states now exist for all R-031–R-056 rows; skipped/unavailable environments do not imply implementation completion.
- Remediation counts — `implementation_complete=15/26`, `IMPLEMENTING=11`, `OPEN=26`, `BLOCKED=0`, `VERIFIED=0`; qualification `partial=9`, `blocked_by_environment=17`; `VERIFIED / 26 = 0/26`.
- Continuation 010 closes the local R-035–R-036 Tailscale adapter boundary with actual-state vocabulary, fixed command allowlist, Serve-only ownership/refusal, loopback validation, persisted desired state, reconciliation, and focused local tests. Live tailnet/second-device qualification remains blocked_by_environment; implementation convergence is now 15/26.
- Continuation 011 closes the local R-037–R-041 Notion lifecycle boundary with Core-owned credential references, Project Record idempotency, stable managed regions, source provenance/retraction, reconciliation, provider-double fault tests, and idempotent managed-history rollover. Live Notion qualification remains blocked_by_environment; implementation convergence is now 20/26.
- Continuation 011 persistence correction adds atomic non-secret lifecycle state snapshot/load and restart coverage at `659fc3ce9659611e34dedf3d6e2b4b892088d355`; live Notion qualification remains blocked_by_environment.
- Continuation 012 adds secret-safe MyAssistant credential-reference import/capability-test boundaries, migration 0023, operator-state/Ask routes, and the complete local R-051–R-053 shell; implementation convergence is now 23/26 while live Notion and supported-browser qualification remain unverified.
- Continuation 013 adds the Core-owned AI execution/profile boundary, durable run/source/profile/usage provenance, privacy and no-fallback enforcement, grounded Ask integration, structured-output/citation checks, prompt-injection and project-isolation defenses, and versioned golden fixtures; implementation convergence is now 25/26. R-056 remains open.

## Blockers

- System Python lacks `psycopg`, and the default host `PRIME_PHASE1_DB_URL` is unset; the qualified `.venv` plus disposable PostgreSQL path was exercised for local evidence. The separate off-machine target, fresh-install/destructive restore drill, native Windows/Linux service, live Notion/Tailscale, live Hindsight, approved AI, browser, sustained capacity, and full end-to-end environments remain unqualified.
- Codebase-memory MCP indexing was attempted for Continuation 011 and returned `Transport closed`; targeted local inspection was used and recorded as a blocker.
- Codebase-memory MCP indexing was retried for Continuation 012 and again returned `Transport closed`; targeted local inspection was used and recorded as a blocker.
- `NOTION_READONLY_KEY` was absent from the current runtime and no local MyAssistant config reference was found; no token material was printed or persisted. Live PRIME Notion capability qualification remains blocked_by_environment.
- Continuation 013 re-inspected candidate config paths, service names, process command lines, and matching runtime environment variable names without printing values; no usable existing MyAssistant Notion secret source was found. Live PRIME Notion capability qualification remains blocked_by_environment.
- Continuation 013 final validation: focused AI fixture tests PASSED (6 passed); full suite PASSED (54 passed, 17 skipped); compileall PASSED; adopted governance PASSED; diff check PASSED; Phase-15 qualification FAILED truthfully at 25/26 implementation-complete and 0/26 VERIFIED; implementation commit `10e0650a6fd14df3837baa7b45ff60d9ec33693b`; evidence/governance commit `e81010f27ef74b34e6bdc7d2618a219ac61ba2bb`; final governance state is recorded in the current HEAD; deployment NOT PERFORMED.

## Pending decisions

- None.

## Status vocabulary

Allowed adopted-project statuses: `IDLE`, `PLANNING`, `IN_PROGRESS`, `VALIDATING`, `BLOCKED`, `COMPLETE`. `CURRENT.md` is mutable and never replaces historical ledgers. Reset it to `IDLE` when an adopted task closes.
