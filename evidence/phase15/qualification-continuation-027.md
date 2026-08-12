# ANIMUS PRIME — Phase 15 Qualification Continuation 027

Baseline: `PRIME-SPEC-V1.0.0`

Qualification implementation commit: `23cd1fd` (`qualify continuation 027 recovery boundaries`)

Native authoritative checkout: `/home/sketch/Projects/ANIMUS_PRIME` (accessed through the Atlas SSHFS mapping; Git operations used the native checkout identity, never a `Z:\home...` double-prefix).

## R-043 — VERIFIED

The new disposable production-path harness `scripts/phase15_qualify_continuation_027.py` populated a representative PRIME source with Project, Node/repository binding and identity, Goal/GoalModel, Progress history, Authority history, managed Evidence and SourceReference, memory ledger and correction state, retained Git bundles, historical inputs, Notion projection revisions, AI run/usage/provenance metadata, backup metadata, and durable restore workflow state. It then:

- created and preflight-verified an encrypted continuity backup;
- mechanically confirmed manifest/project identity and managed-content hashes;
- confirmed credential-bearing fields were excluded and configuration is `REPROVISION_REQUIRED`;
- restored into a newly created PostgreSQL database migrated from zero;
- verified project identity, Evidence identity/hash/source reference, AI metadata, usage records, managed Evidence bytes, retained Git bundle fidelity, historical-state fidelity, and Hindsight `SOURCE_LEDGER_REBUILD` labeling;
- refused a populated conflicting target without mutation;
- required `X-PRIME-STEP-UP: CONFIRM` for replacement through the production restore route, including `replace=true`, and created the safety checkpoint;
- interrupted replacement after target mutation began and observed durable `REPAIR_REQUIRED / FAILED` workflow state.

The run exposed and fixed two production defects before the final pass: destructive replacement did not previously require the step-up header, and backup secret filtering missed fields such as `password_hash`, `recovery_hash`, and `token_hash`. The final harness result was `R-043 = VERIFIED`, with `remaining_gap = NONE`.

## R-045 — PARTIAL

The production Core queue boundary was exercised with 300 legitimate parser jobs over `20.078s`. The configured queue bound was `32`; `32` jobs were accepted, `268` were refused by derived-work backpressure, the durable parser queue peaked at `32`, canonical writes remained prioritized, and recovery completed in `0.031s` after the queue was drained.

This is not a promotion. The frozen implementation does not expose or enforce the remaining normative boundaries required for closure: parser running-count/concurrency telemetry, index backlog and drain telemetry, stale-job revision rejection, retention-pressure preservation across all protected classes, and usage/cost limit throttle/refusal records. A 300-event load is retained as partial evidence only. `remaining_gap` remains those five observability/enforcement categories.

## R-048 — VERIFIED

The same real A/B/C/D project established a State-B baseline with all required source classes `EXACT`: repository/Git, AuthorityRevision, Goal/GoalModel, Progress, Evidence/SourceReference, memory/source ledger, Notion projection revision, Brain, and retained Git checkpoint.

The independent loss/recovery matrix removed one source class at a time and restored the exact original continuity source through the production restore path. Results:

| Source class | Loss result | Recovery |
| --- | --- | --- |
| Evidence/SourceReference | `PARTIAL`; direct source-reference resolution became `UNAVAILABLE` when managed bytes disappeared | exact bytes restored and reindexed; `EXACT` |
| AuthorityRevision | `UNAVAILABLE` | `EXACT` |
| Goal/GoalModel | `UNAVAILABLE` | `EXACT` |
| Progress | `UNAVAILABLE` | `EXACT` |
| Memory/source ledger | `UNAVAILABLE` | `EXACT` |
| Notion projection revision | `UNAVAILABLE` | `EXACT` |
| Brain | `UNAVAILABLE` | `EXACT` |
| retained Git checkpoint | `UNAVAILABLE` | exact bundle restored; `EXACT` |

The correction timeline remained truthful: A/B recorded P1, C introduced P2 as a correction/supersession, D preferred P2 while retaining P1 historically. Missing Evidence bytes no longer appear fully supported. The final harness result was `R-048 = VERIFIED`, with `remaining_gap = NONE`.

## R-044 — PARTIAL / ENVIRONMENT DIAGNOSIS

The approved Hindsight retain path remains `UNAVAILABLE`. No Hindsight process or listener was present on the qualification host; `127.0.0.1:18888` actively refused all health probes, and the local Docker engine was unavailable. The pinned compose contract expects Hindsight `0.6.1` on container port `8888` mapped to `18888`, with its configured database and model-provider environment. This is an environment-availability/configuration blocker, not evidence of a PRIME adapter schema defect. No raw credentials or provider payloads were recorded, and Hindsight was not connected to Paragon.

## R-053 — PARTIAL

The frozen acceptance is the §16.4/§16A/§25.7 accessible responsive operator experience: keyboard-accessible controls, visible focus/semantic state, reduced-motion behavior, responsive desktop/mobile operation, and accessible Project Brain tree/list fallback without information existing only in color, animation, spatial position, or hover state. Existing Chromium evidence covers the available browser checks. No valid external assistive-technology environment (for example Orca, Narrator, or NVDA with a supported browser) was available, so no external AT claim or promotion is made.

## Governed result

- Implementation: `25/26`
- Qualification: `16/26 VERIFIED`, `9 partial`, `1 blocked/open — R-056`, `0 failed`
- Newly verified: `R-043`, `R-048`
- Preserved verified: `R-037`, `R-038`, `R-039`, `R-040`, `R-041`, `R-042`, `R-046`, `R-047`, `R-049`, `R-050`, `R-051`, `R-052`, `R-054`, `R-055`
- R-045 remains partial; R-044 and R-053 remain partial; R-056 remains `blocked_by_environment / OPEN`.
- Phase 15: `FAIL`; V1: `FAIL`.
- Deployment: `NOT PERFORMED`.

## Validation evidence

- Focused Continuation 027 harness: `PASSED` — R-043 verified, R-045 partial with explicit metrics, R-048 verified.
- Focused existing qualification tests: `PASSED` — `3 passed, 83 deselected`.
- Native Python AST parse of changed Python files: `PASSED`.
- Full regression: `PASSED` — `85 passed, 1 skipped` under `--import-mode=importlib`; the only skipped test requires a separate mount unavailable in this environment.
- Phases 1–14 qualification scripts: `PASSED` — all fourteen scripts completed successfully against a fresh disposable PostgreSQL database.
- Governance validator: `PASSED` — adopted governance validation checked 17 required files and 6 Cursor rules.
- YAML/count reconciliation: `PASSED` — 26 rows; `16 verified`, `9 partial`, `1 blocked_by_environment` (`R-056`), `0 failed`.
- AST parse: `PASSED` for changed Python files.
- Diff check: `PASSED` — `git diff --check` returned clean for the pending publication diff.
- Tracked-secret scan: `PASSED` — no bearer/token/private-key candidates were found in tracked files outside the frozen baseline.
- GitHub publication/parity: `PASSED` — evidence/governance commit `46ae788` was pushed to `origin/main`; local and origin resolved to the same SHA.
- Notion publication: `PASSED` — Continuation 027 execution record appended and refetched on the connected disposable qualification page.
