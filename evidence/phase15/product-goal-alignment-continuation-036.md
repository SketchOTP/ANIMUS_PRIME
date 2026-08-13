# ANIMUS PRIME — Continuation 036 Evidence

Date: 2026-08-13
Execution: DIRECT SSH / NATIVE ATLAS
Checkout: `/home/sketch/Projects/ANIMUS_PRIME`
Baseline: `PRIME-SPEC-V1.0.0`

## Semantic audit reconciliation

Continuation 035 left architectural rows with generic operator-UI gap prose. Continuation 036 reviewed the exact frozen clauses and replaced that prose in the audit and derived burndown for DOD-002, DOD-005, DOD-006, DOD-007, DOD-009, DOD-018, DOD-028, DOD-033, DOD-037, DOD-038, DOD-039, DOD-045, and DOD-061. No row was promoted solely from this reconciliation. The validator now rejects architectural rows whose missing behavior or next action requires an operator screen/workflow without an explicit frozen user-facing clause.

Mechanical result: 81 audit items, 12 complete, 69 open, IDs/statuses/acceptance kinds/work classes aligned, architectural semantics PASS. Work-class totals are LOCAL_CODE 12, LOCAL_BROWSER_QUALIFICATION 25, LOCAL_NATIVE_QUALIFICATION 0, EVIDENCE_RECONCILIATION 3, EXTERNAL_ENVIRONMENT 29, AGGREGATE_RELEASE_GATE 0.

## Hindsight endpoint and extraction

The prior defect was confirmed in code: `MemoryService` constructed `PrimeMemoryAdapter` against `127.0.0.1:18888`, while the Atlas Hindsight service was healthy on `127.0.0.1:8888`. The approved source of truth is now `Settings.hindsight_base_url`, configured by `PRIME_HINDSIGHT_BASE_URL` and defaulting to `http://127.0.0.1:8888`. The adapter timeout is configured by `PRIME_HINDSIGHT_TIMEOUT_SECONDS`, default 30 seconds. Compose host mapping now matches the service topology at `8888:8888`. URLs contain no secrets.

Endpoint matrix:

- configured 8888 health: CURRENT
- wrong/unreachable port 1: UNAVAILABLE
- recovery to configured 8888: CURRENT
- project bank create/delete/recreate: CURRENT
- project isolation: bank remains `prime-<project_id>` and no cross-bank data was used

Controlled extraction used the disposable fact: `The qualification project database engine is PostgreSQL 17.` The earlier 10-second adapter timeout expired before Hindsight completed its provider call. Hindsight logs then showed the provider extracting and storing 1 fact in about 13.7 seconds. With the configured 30-second timeout, PRIME returned `retain=CURRENT`, and recall returned 1 durable result. The adapter’s recall-backed verification was preserved. No direct database writes, fabricated facts, or production schema changes were made. Full R-044 correction/supersession/tombstone and source-ledger rebuild matrix remains incomplete, so R-044 stays partial.

## Historical Goal / Brain / Ask

The historical service now reconstructs the latest Goal revision valid at a selected timestamp and includes Goal content in the returned historical context. Direct committed-revision selection also falls back to the Goal revision observed before that repository revision when the Goal hash is not the revision identifier. Time Lens browser submission now loads the selected historical Brain endpoint, renders historical Goal content or truthful UNAVAILABLE, and Return to Now reloads current Brain.

The historical A/B/C/D integration test passed direct revision Goal selection, historical Goal content, historical Brain source revision, historical Ask citations, no later-state leakage, and Return to Now. Browser smoke on the native Core endpoint passed page load, truthful unauthenticated state, Time Lens controls, Brain controls, and no stale authenticated payload. Full authenticated browser promotion was not claimed because the disposable Core instance had no browser session.

## Validation

- `PYTHONPATH=. .venv/bin/pytest tests scripts -q`: PASSED, 66 passed, 27 skipped.
- `PYTHONPATH=. .venv/bin/pytest -q`: PASSED, 66 passed, 27 skipped.
- Fresh zero-state PostgreSQL 17.10 / pgvector 0.8.2: PASSED.
- All 26 migrations from zero: PASSED.
- Fresh database-backed `pytest -q -rs`: PASSED, 93 passed.
- Phases 1–14: PASSED.
- `compileall`: PASSED.
- Web JavaScript `node --check`: PASSED.
- Hindsight endpoint matrix: PASSED.
- Hindsight durable retain/recall: PASSED.
- Historical Goal/Brain/Ask integration: PASSED.
- Semantic audit/burndown validator: PASSED.
- `git diff --check`: PASSED.
- Browser smoke: PASSED with truthful unauthenticated state; full authenticated product qualification NOT RUN.
- Deployment: NOT PERFORMED.

## Governed result

§26 remains 12 complete / 69 open. Remediation remains 16 VERIFIED / 9 partial / R-056 blocked-open / 0 failed. V1_PRODUCT_GOAL_ALIGNMENT, Phase 15, and V1 remain FAIL. Newly promoted rows: none. Remaining local work includes authenticated Brain scale/live/A-B qualification, clean-source Fork fidelity/isolation, Search/Activity/Repository/Progress browser closure, and full R-044 matrix. External Notion, native Node, Windows, Tailscale second-device, assistive technology, and R-056 remain explicit boundaries.