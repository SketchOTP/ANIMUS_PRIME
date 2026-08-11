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

## Continuation 016 — first requirement-level verification

- directive: `D-PRIME-PHASE15-REMEDIATION-016`
- baseline: `PRIME-SPEC-V1.0.0`
- qualified_commit: `8893b2b5a6612eaa85b5767a80fe4b462069d4f1`
- database_environment: `PASS` — fresh PostgreSQL `17.10`, pgvector `0.8.2`, all 24 migrations from zero.
- phase_gates: `PASS` — Phases 1 through 14.
- full_regression: `PASS` — `73 passed`.
- newly_verified: `R-049` — retained PRIME-owned checkpoint survives repository rewrite/reflog expiry/GC, restart, bundle loss/recovery, citation resolution, Time Lens reconstruction, non-retained degradation, and ownership-boundary checks.
- implementation_defect: `PASS` — purged Evidence now resolves `UNAVAILABLE`; retracted Evidence resolves historical with explicit retraction; Git citation checks retained bundle integrity; Time Lens distinguishes live repository reachability from retained PRIME checkpoint.
- requirement_state: `1/26 VERIFIED`; `17 partial`; `8 blocked_by_environment`; `0 failed`; R-056 remains `OPEN`.
- environment_reconciliation: Linux/systemd, Chromium, Tailscale, and Hindsight are present but incomplete for exact normative qualification; Notion secret source is `NOT FOUND`; approved AI/local inference is unavailable.
- qualification_evidence: `evidence/phase15/qualification-continuation-016.md`
- security_tests_run: `PASS` for R-049 and exercised Evidence/citation cases; remaining live/native security environments remain incomplete.
- recovery_tests_run: `PASS` for R-049 retained bundle loss/recovery; destructive/interrupted/off-machine recovery remains unverified.
- result: `FAIL` — aggregate V1 gate remains truthful; deployment `NOT PERFORMED`.

## Continuation 018 — approved local AI and PRIME Notion capability

- directive: `D-PRIME-PHASE15-REMEDIATION-018`
- baseline: `PRIME-SPEC-V1.0.0`
- qualified_implementation_commit: `e7705dc0a1ece7e12dbfc3d35e914a0a2833d7da`
- database_environment: `PASS` — fresh PostgreSQL `17.10`, pgvector `0.8.2`, all 24 migrations from zero.
- full_regression: `PASS` — `80 passed`; Phases 1 through 14 `PASS`.
- newly_verified: `R-054`; preserved `R-046`, `R-047`, `R-049` `VERIFIED`.
- R-054: real Paragon OpenAI-compatible `/chat/completions` execution for Ask, Progress, Documentation, and memory admission under `LOCAL_ONLY`; structured output, usage/provenance, injection, isolation, outage, recovery, and secret-redaction evidence passed.
- R-037–R-041: supplied PRIME Notion authorization, health, frozen source/handoff page, and child-block reads passed; live write/lifecycle criteria remain partial and no write probe was run.
- R-055: Paragon cross-function execution and safety paths passed, but full Goal/Alignment/correction and isolated Project A/B evaluation remains partial.
- requirement_state: `4/26 VERIFIED`; `21 partial`; `1 blocked_by_environment` (`R-056`); `0 failed`; R-056 remains `OPEN`.
- environment_reconciliation: Paragon endpoint reachable and approved for this qualification; Notion connected for read capability; no credentials persisted; Chromium remains the supported browser harness; native Windows/root, private second-device Tailscale, live Notion writes, full Hindsight/provider-dependent paths, and R-056 remain open.
- qualification_evidence: `evidence/phase15/qualification-continuation-018.md`
- security_tests_run: `PASS` for provider local-only, prompt-injection-as-data, cross-project rejection, structured-output, and secret-redaction paths; Notion write probe intentionally `NOT RUN`.
- recovery_tests_run: `PASS` for provider outage/recovery; Notion read re-import/capability passed; live write/reconciliation recovery remains open.
- result: `FAIL` — aggregate V1 gate remains truthful; deployment `NOT PERFORMED`.

## Continuation 017 — Evidence and product citation verification

- directive: `D-PRIME-PHASE15-REMEDIATION-017`
- baseline: `PRIME-SPEC-V1.0.0`
- qualified_implementation_commit: `dbf94f7eab521c4a0973681654a83fddec8470db`
- database_environment: `PASS` — fresh PostgreSQL `17.10`, pgvector `0.8.2`, all 24 migrations from zero.
- full_regression: `PASS` — `79 passed`; Phases 1 through 14 `PASS`.
- newly_verified: `R-046`, `R-047`; preserved `R-049` `VERIFIED`.
- R-046: real active-content/MIME/size/parser/Node-root/isolation matrix plus managed Evidence backup/clean-restore/reindex identity passed.
- R-047: real product Search/Ask/Progress/Documentation E1/S1 citation, retraction, restore/reindex, and project-isolation matrix passed.
- exercised_partial: `R-042`, `R-043`, `R-045`, `R-048`, `R-050`; exact remaining gaps are recorded in the evidence package.
- requirement_state: `3/26 VERIFIED`; `15 partial`; `8 blocked_by_environment`; `0 failed`; R-056 remains `OPEN`.
- environment_reconciliation: Chromium CDP shell/setup/auth/navigation/degraded/responsive/security paths exercised; agent-browser absent and full assistive-technology/historical browser path remains partial. Native root, Windows, private second-device Tailscale, approved Hindsight model/provider, live Notion, approved AI remain incomplete. Independent `/dev/sdb1` target passed backup classification.
- qualification_evidence: `evidence/phase15/qualification-continuation-017.md`
- security_tests_run: `PASS` for R-046/R-047 exercised boundaries; remaining live/native/provider security environments incomplete.
- recovery_tests_run: `PASS` for Evidence parser/reindex, managed restore identity, off-mount encrypted backup, and durable interrupted restore state; complete R-042/R-043 recovery matrix remains open.
- result: `FAIL` — aggregate V1 gate remains truthful; deployment `NOT PERFORMED`.
