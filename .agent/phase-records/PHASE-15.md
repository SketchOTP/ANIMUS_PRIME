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

## Continuation 023 — live PRIME Notion adapter qualification

- directive: `D-PRIME-PHASE15-REMEDIATION-023`
- baseline: `PRIME-SPEC-V1.0.0`
- qualification_evidence: `evidence/phase15/qualification-continuation-023.md`
- qualification_implementation_lineage: `4531fb0`
- database_environment: `PASS` — fresh disposable PostgreSQL/pgvector recreated on native Atlas
- native_compile: `PASS`
- full_regression: `PASS` — `86 passed`; Phases 1 through 14 `PASS`
- live_credentials: `PRESENT` for Notion read/API and Paragon; values remained process-ephemeral and were not recorded
- live_notion_target: `PASS` — inaccessible prior sandbox was replaced by a disposable child under accessible `ANIMUS PRIME` root; no canonical/user-authored content was mutated
- Paragon: `PASS` — existing `paragon`/`paragon`, `LOCAL_ONLY`, OpenAI-compatible profile exercised through the product path
- R-037: `VERIFIED` — live Project Record, binding, managed-region initialization, Documentation projection, readback, retry/idempotency and secrecy
- R-038: `VERIFIED` — live Documentation projection, user preservation, managed conflict, redaction, stale/replay/self-write and reconciliation matrix
- R-039: `VERIFIED` — live source attach, revision refresh, independent A/B bindings, detach/retraction, provenance and memory review
- R-040: `VERIFIED` — live degraded outage, canonical-state preservation, recovery/reconciliation, missing-page and restart/idempotency behavior
- R-041: `VERIFIED` — live history rollover, response-loss retry, source range, persisted identity, restart and idempotency
- preserved_verified: `R-046`, `R-047`, `R-049`, `R-054`, `R-055`
- remaining: `R-042` scheduled failure/recovery/retention; `R-043`, `R-045`, `R-048`, `R-050`–`R-053`; `R-056 OPEN`
- requirement_state: `10/26 VERIFIED`; implementation `25/26`; Phase 15/V1 `FAIL`; deployment `NOT PERFORMED`
- result: `FAIL` — aggregate V1 gate remains truthful until all 26 rows are verified

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

## Continuation 024 — scheduled recovery and Chromium operator qualification

- directive: `D-PRIME-PHASE15-REMEDIATION-024`
- baseline: `PRIME-SPEC-V1.0.0`
- qualified_implementation_commit: `95db422`
- database_environment: `PASS` — freshly recreated disposable PostgreSQL/pgvector environment; all migrations applied from zero.
- native_compile: `PASS`
- full_regression: `PASS` — `86 passed`.
- phase_gates: `PASS` — Phases 1 through 14.
- newly_verified: `R-042`, `R-052`.
- preserved_verified: `R-037`–`R-041`, `R-046`, `R-047`, `R-049`, `R-054`, and `R-055`.
- R-042: `VERIFIED` — durable schedule persisted across Core restart; scheduled backup succeeded; destination failure recorded `FAILED` with retry; known-good remained preserved; destination recovery and retry succeeded; retention preserved the latest known-good; wrong-key/tamper/truncation/credential-exclusion coverage passed.
- R-052: `VERIFIED` — real Chromium authenticated two-project journey, required project surfaces, switching/isolation, refresh/restart recovery, invalid Search/Ask project rejection, healthy/degraded states, responsive rendering, reduced-motion rule, and protected lifecycle dialog were exercised.
- R-044: `PARTIAL` — approved Hindsight health, bank isolation, delete/recreate, and unavailable behavior passed; retain remained `UNAVAILABLE`.
- remaining_partial: `R-043`, `R-044`, `R-045`, `R-048`, `R-050`, `R-051`, `R-053`; exact gaps are recorded in `evidence/phase15/qualification-continuation-024.md`.
- qualification_state: `12/26 VERIFIED`; `15 partial`; `1 blocked_by_environment` (`R-056`); `0 failed`.
- R-056: `OPEN`.
- security_tests_run: `PASS` for available native/browser/backup negative and secret-boundary checks; full keyboard/assistive-technology/untrusted-text and remaining environment-specific security gates remain unqualified.
- recovery_tests_run: `PASS` for R-042 scheduled failure/retry/recovery/retention and R-052 restart/session recovery; fresh-install/interrupted restore, sustained capacity, historical correction, and setup-resume recovery remain open.
- qualification_evidence: `evidence/phase15/qualification-continuation-024.md`
- governance_publication: `recorded by the final governance/publication commit and exact GitHub parity check at closure`
- result: `FAIL` — aggregate V1 gate remains truthful at 12/26; deployment `NOT PERFORMED`.

## Continuation 020 — integrated product AI lifecycle

- directive: `D-PRIME-PHASE15-REMEDIATION-020`
- baseline: `PRIME-SPEC-V1.0.0`
- qualified_implementation_commit: `4531fb05523f4036382be1d1eda7d9a4c19d989d`
- qualification_evidence: `evidence/phase15/qualification-continuation-020.md`
- database_environment: `PASS` — fresh disposable PostgreSQL/pgvector container and all migrations from zero.
- full_regression: `PASS` — `86 passed`.
- phase_gates: `PASS` — Phases 1 through 14.
- implementation_changes: `IntelligenceService` now owns product-level Documentation projection and memory admission/correction side effects; memory correction persists supersession and history; Notion API/provider translation now has exact marker idempotency and bounded page lifecycle support; Continuation 020 adds product-path qualification and focused provider/lifecycle tests.
- R-055: `VERIFIED` — real Paragon through IntelligenceService; durable ai_runs; product Project A/B source rejection before provider dispatch; Goal, Progress, Ask, Alignment, Documentation, memory; managed projection/conflict; invalid citation rejection; correction supersession/history; provider degradation/recovery; history rollover/restart; secret-safe metadata.
- R-037–R-041: `PARTIAL` — offline PRIME provider/lifecycle path passed, but live Notion create-page requests return archived-parent validation because the approved disposable target is in trash; no canonical or user-authored page was mutated.
- preserved_verified: `R-046`, `R-047`, `R-049`, `R-054`.
- qualification_state: `5/26 VERIFIED`; `20 partial`; `1 blocked_by_environment` (`R-056`); `0 failed`.
- R-056: `OPEN`.
- result: `FAIL` — Phase 15/V1 remains below 26/26; deployment `NOT PERFORMED`.

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

## Continuation 019 — real Paragon cross-surface and disposable Notion writes

- directive: `D-PRIME-PHASE15-REMEDIATION-019`
- baseline: `PRIME-SPEC-V1.0.0`
- qualified_implementation_commit: `877b92ed3cb903022206d874f01e144f1c1e33b3`
- database_environment: `PASS` — fresh disposable PostgreSQL `17.10`, pgvector `0.8.2`, all migrations from zero.
- full_regression: `PASS` — `80 passed`; Phases 1 through 14 `PASS`.
- newly_verified: none; preserved `R-046`, `R-047`, `R-049`, `R-054` `VERIFIED`.
- Paragon: `PASS` — real Project A/B-scoped Goal, Progress, Ask, Documentation, Alignment, and memory execution; grounded fact, UNKNOWN, source isolation, prompt-injection resistance, supported/unsupported memory, outage degradation, explicit recovery, and durable provenance exercised.
- Notion: `PASS` — standalone disposable connected-workspace create/read/update, managed-region preservation, child source revision refresh; no canonical or user-authored page touched.
- R-055: `PARTIAL` — integrated product projection, live invalid-citation, contradiction/correction, and complete lifecycle closure remain.
- R-037–R-041: `PARTIAL` — local PRIME adapter project binding, managed-region conflict/replay, source detach/retraction, outage reconciliation, and history rollover remain.
- requirement_state: `4/26 VERIFIED`; `21 partial`; `1 blocked_by_environment` (`R-056`); `0 failed`; R-056 remains `OPEN`.
- qualification_evidence: `evidence/phase15/qualification-continuation-019.md`
- security_tests_run: `PASS` for local-only provider, source isolation, untrusted injection, citation bounds, outage/no-fallback, secret-safe durable metadata, and disposable Notion write boundary.
- recovery_tests_run: `PASS` for Paragon outage/recovery and new run identity; Notion local-adapter reconciliation/history remains unverified.
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

## Continuation 025 — ledger reconciliation, setup resume, and Time Lens control

- directive: `D-PRIME-PHASE15-REMEDIATION-025`
- baseline: `PRIME-SPEC-V1.0.0`
- qualification_implementation_commit: `44608f1`
- prior evidence basis: `evidence/phase15/qualification-continuation-024.md`; R-042 and R-052 were not rerun.
- governance correction: `qualification_status` map, ledger records, matrix, and traceability now agree on `R-042` and `R-052` as VERIFIED; mechanical count is `12/26 VERIFIED`, `13 partial`, `1 blocked_by_environment` (`R-056`), `0 failed` before new promotion.
- R-051: `VERIFIED` — fresh browser bootstrap interrupted by Core stop returned `502`; same form resumed after Core recovery and returned `200`; login, operator state, project creation, and global navigation passed; prior negative/CSRF/restart/reconnect evidence preserved.
- R-053: `PARTIAL` — keyboard focus traversal, Enter form submission, untrusted project-name rendering, responsive/no-overflow, reduced-motion, textual-state, Brain alternative, and dialog checks passed; external assistive-technology run remains unavailable.
- R-050: `PARTIAL` — interactive Time Lens boundary selector, custom revision/timestamp field, historical-state action, safe status rendering, and Return to Now were added and exercised; populated State-B browser fixture, source removal/recovery, historical citations/Brain, and complete browser return-to-current remain open.
- focused_regression: `PASS` — R-043, R-045, and R-048/R-050 tests, `3 passed`; no promotion claimed for those rows.
- qualification_state: `13/26 VERIFIED`; `12 partial`; `1 blocked_by_environment` (`R-056`); `0 failed`.
- R-056: `OPEN`.
- governance_publication: `governance/evidence commit d261c2b; final-tip e44a904; local/origin parity confirmed; Notion append BLOCKED by unavailable authenticated edit surface`
- result: `FAIL` — aggregate V1 gate remains truthful at 13/26; deployment `NOT PERFORMED`.

## Continuation 026 — populated historical browser qualification

- directive: `D-PRIME-PHASE15-REMEDIATION-026`
- baseline: `PRIME-SPEC-V1.0.0`
- qualification_implementation_commit: `5c2ec8e`
- qualification_evidence: `evidence/phase15/qualification-continuation-026.md`
- native_focused_regression: `PASS` — `4 passed`; web shell `1 passed`; compileall `PASS`.
- fresh_full_regression: `PASS` — `86 passed` with `--import-mode=importlib`.
- phase_gates: `PASS` — Phases 1 through 14 qualification scripts.
- historical_fixture: `PASS` — real disposable Git A/B/C/D repository and durable PRIME records for repository, authority, Goal, Progress, Evidence, Memory, Notion projection, Brain, and retained Git bundles.
- browser_historical_state: `PASS` — State B displayed `HISTORICAL · EXACT`; all source classes were `EXACT`.
- browser_ask_brain: `PASS` — Ask and Brain returned HTTP `200`; Ask used only State-A/State-B material and `later_current_state_used=false`.
- browser_loss_recovery: `PASS` — deliberate State-B Evidence loss displayed source-level `PARTIAL`; exact restore returned all sources `EXACT`.
- browser_return_to_now: `PASS` — current boundary displayed `CURRENT · EXACT` after the history-service correction.
- newly_verified: `R-050`.
- preserved_verified: `R-037`, `R-038`, `R-039`, `R-040`, `R-041`, `R-042`, `R-046`, `R-047`, `R-049`, `R-051`, `R-052`, `R-054`, `R-055`.
- qualification_state: `14/26 VERIFIED`; `11 partial`; `1 blocked_by_environment` (`R-056`); `0 failed`.
- partial_rows: `R-031`–`R-036`, `R-043`, `R-044`, `R-045`, `R-048`, `R-053`.
- R-056: `OPEN`.
- governance_publication: `PASS` — evidence/governance commit `d11bf98d`; final local/origin parity confirmed at `a4a3916f6fc5dc54298f6b2621f7e8e03071fbf0`.
- notion_publication: `PASS` — Continuation 026 execution record appended and refetched on the connected disposable qualification page.
- result: `FAIL` — Phase 15/V1 remains below 26/26; deployment `NOT PERFORMED`.
