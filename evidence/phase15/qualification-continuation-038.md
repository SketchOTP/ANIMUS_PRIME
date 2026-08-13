# ANIMUS PRIME — Continuation 038 Qualification Evidence

Date: 2026-08-13  
Execution: DIRECT SSH / NATIVE ATLAS  
Checkout: `/home/sketch/Projects/ANIMUS_PRIME`  
Baseline tip: `6a262697fbba12542b7709ece7534a46295d1ded`  
Baseline: `PRIME-SPEC-V1.0.0`

## Governance reconciliation

The authoritative audit contains 81 DOD rows: 18 complete and 63 open. The derived burndown now contains exactly the 63 non-complete rows. Mechanically validated work-class totals are:

- `LOCAL_CODE`: 11
- `LOCAL_BROWSER_QUALIFICATION`: 24
- `LOCAL_NATIVE_QUALIFICATION`: 0
- `EVIDENCE_RECONCILIATION`: 3
- `EXTERNAL_ENVIRONMENT`: 25
- `AGGREGATE_RELEASE_GATE`: 0

The validator now hard-fails stale header totals, duplicate audit or burndown IDs, complete rows present in the open burndown, missing open rows, status or acceptance-kind drift, invalid work classes, incomplete required fields, non-concrete actions, architectural UI-gap prose, and work-class sum mismatch. All checks passed. The authoritative remediation count remains `17 VERIFIED / 8 partial / R-056 blocked-open / 0 failed`; no ledger, matrix, or traceability promotion was made in this continuation.

## Native Atlas path-contract trace

The disposable Core/Node stack ran on Atlas over direct SSH with a Windows localhost tunnel only for browser access. The application path field, JavaScript value, JSON request, Core validation, Node/service boundary, and actual filesystem target were traced.

With ordinary Git Bash invocation, the test argument `/tmp/prime038-source` was mutated by MSYS before the browser process received it. The browser field and JavaScript both showed `C:/Users/sketc/AppData/Local/Temp/prime038-source`; the outgoing JSON carried the same value; Core rejected it as outside the enrolled `/tmp` root. The first mutation was therefore the Git Bash/MSYS process boundary, before application code.

With `MSYS_NO_PATHCONV=1`, the browser displayed and retained `/tmp/prime038-source`; JavaScript, outgoing JSON, Core response, service boundary, and the real Atlas target all carried `/tmp/prime038-source`. PRIME's path handling is opaque and correct for the native contract. No product normalization patch was made. Cross-platform request serialization and allowed-root/symlink-escape regression tests were added and passed.

## Browser Fork / Clone

An authenticated disposable Project B was bound to `/tmp/prime038-source` on Atlas. Browser Fork A1 submitted source revision `e5d88145189b2ba859a12c2e310ee685cb4f89cb` to `/tmp/prime038-forks/c038-fork-a1`; the browser request returned 200 and the destination had a real Git checkout at `53d9dc9d4c07cd830a5f4f79959e0659067c7bf0` with the expected fork commit. A2 submitted source revision `943e0f4a1fc19c51b412bd3730a81b5c36edf7ea` to `/tmp/prime038-forks/c038-fork-a2`; the destination had a real Git checkout at `c5e44a5082f9b3889b4cb15c86e597d2906cec40` with the expected fork commit.

These results establish native path fidelity, selected-revision submission, real destination creation, and independent repository identities for the bounded A1/A2 path. The complete DOD-016/DOD-017 matrix, including all resource-isolation and dirty-source cases in the required governed resource record, was not completed in this run. DOD-016 and DOD-017 remain open and are not promoted.

## Brain browser

Authenticated Brain browser focus was attempted on the disposable source project. The Brain response was `availability=UNAVAILABLE`, `source_revision=UNKNOWN`, with zero nodes and zero edges because this disposable registration did not produce a qualified Brain snapshot/index. No focus-state or isolation promotion was made. DOD-051 remains `IMPLEMENTED_NOT_PRODUCT_QUALIFIED`/open.

## Hindsight reflect / Mental Models

A disposable Hindsight bank was created, retained two facts, queried for reflect, and deleted. Health, bank creation, retain, and deletion were `CURRENT`; reflect returned `UNAVAILABLE` with an empty payload and reason `hindsight unavailable`. Atlas logs showed the approved configured provider identity `openai/routerbot-local`, slow extraction calls, and `Starting agentic reflect` without a successful bounded reflect response. This is a real provider/reflect completion boundary, not evidence for a product promotion. DOD-068 remains `BACKEND_ONLY`/open.

No Search, Activity, Repository, Progress, Ask, or architecture rows were promoted in this continuation. R-045 remains partial. R-056 remains blocked/open. Phase 16 and deployment were not performed.

## Validation

- Burndown validator: PASSED.
- Ordinary `.venv` tests and scripts: PASSED (`75 passed, 28 skipped`).
- Test collection: PASSED (`103 collected`).
- Python compileall: PASSED.
- Fresh disposable PostgreSQL/pgvector and all 26 migrations: PASSED. Two pre-existing mode-660 migration files required a temporary disposable container readability adjustment; tracked files were not changed by that adjustment.
- Cross-platform path and allowed-root tests: PASSED (`8 passed`).
- Browser path contract and Fork A1/A2 bounded evidence: PASSED; complete isolation qualification: PARTIAL.
- Brain browser focus/state: BLOCKED/UNAVAILABLE in the disposable fixture.
- Hindsight reflect/Mental Models: BLOCKED/UNAVAILABLE.
- Notion publication: PENDING at evidence creation; verified after the final governed commit.
- Deployment: NOT PERFORMED.

