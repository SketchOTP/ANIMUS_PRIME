# Phase 15 Qualification Record

phase: 15
implementation_baseline_spec_revision: PRIME-SPEC-V1.0.0
start_commit: 3e99516
qualified_commit: NOT_QUALIFIED
requirements_owned: R-024, R-026, R-027
requirements_implemented: PARTIAL; remediation R-031 through R-056 IMPLEMENTING
requirements_verified: mechanical regression only; V1 release requirements reopened
requirements_blocked: live-provider/cross-platform/recovery/UX/AI evidence gaps
schema_versions_changed: NONE
protocol_versions_changed: full-v1-qualification
tests_run: python3 -m pytest tests -q; scripts/phase15_qualify.py
tests_passed: local suite 20 passed; 15 PostgreSQL integration tests skipped; V1 DoD gate failed
security_tests_run: PENDING_GATE
recovery_tests_run: PENDING_GATE
known_limitations: Full V1 Definition of Done must be reconciled against all normative deliverables; a passing scaffold/regression suite is not sufficient. See docs/phase15-remediation-matrix.yaml.
remediation_progress: R1-R6 implementation foundations added, including Core-side Node client; R1-R6 live/cross-platform/recovery/provider/UX evidence still open
result: FAIL

## Continuation 015 — database qualification recovery

- directive: `D-PRIME-PHASE15-REMEDIATION-015`
- baseline: `PRIME-SPEC-V1.0.0`
- implementation_defect_commit: `344efd6`
- database_environment: `PASS` — fresh disposable `pgvector/pgvector` container; PostgreSQL `17.10`; pgvector `0.8.2`; no host volume; application role connected; credentials omitted.
- migrations: `PASS` — all 24 migrations from zero through `0024_ai_execution.sql`; idempotence and schema/table checks passed.
- phase_gates: `PASS` — Phases 1 through 14.
- full_regression: `PASS` — `71 passed` with database variables configured; no database-dependent skips remained.
- state_reuse_check: `FAILED` — a later invocation against the populated database hit three expected state-collision failures; the database was recreated and the authoritative fresh rerun passed.
- defect_found: `FAIL then repaired` — `ai_runs` INSERT had 22 placeholders for 21 columns; fixed minimally in `src/prime_core/ai_service.py`.
- requirement_state: `0/26 VERIFIED`; R-042–R-050 remain `partial`; native/live/off-machine/browser/provider paths remain `blocked_by_environment`; R-056 remains `OPEN`.
- qualification_evidence: `evidence/phase15/qualification-continuation-015.md`
- security_tests_run: `PASS` for available local suite; live/native security environments not available.
- recovery_tests_run: `PASS` for available local database-backed tests; off-machine/interrupted/fresh-install recovery evidence remains unverified.
- result: `FAIL` — V1 gate remains truthful; deployment `NOT PERFORMED`.
