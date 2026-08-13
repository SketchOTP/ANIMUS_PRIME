# ANIMUS PRIME — Continuation 037 Qualification Evidence

Date: 2026-08-13
Execution: DIRECT SSH / NATIVE ATLAS
Checkout: `/home/sketch/Projects/ANIMUS_PRIME`
Baseline: `PRIME-SPEC-V1.0.0`

## R-044 and Hindsight

A fresh disposable PostgreSQL/pgvector database was used for the qualification fixture. A separate Project A contained a live Hindsight bank, current PRIME memory/source-ledger rows, managed Evidence bytes, and a PRIME-owned retained Git bundle. The production `BackupCoordinator.create_continuity_backup` path created the encrypted continuity artifact and its manifest. No Hindsight database dump, volume copy, direct Postgres write, or production/private memory was used.

The manifest identified `prime_postgresql=EXACT`, `historical_state=EXACT`, `evidence=EXACT_FOR_MANAGED_BYTES`, `git_checkpoints=EXACT_FOR_RETAINED_BUNDLES`, `configuration=EXACT_NON_SECRET_ONLY`, and `hindsight=SOURCE_LEDGER_REBUILD / REBUILDABLE_NOT_BIT_IDENTICAL`. Evidence hash restored exactly as `77eb6e6989e60bc9907af9abd31fe52013bcdeac0a5328e2ddd3276dbd3cccda`; retained Git bundle hash restored exactly as `b7112888d66e1cdbf3e3017e6a1bd868d294c69c46492eacd6b485a520d40d4d`.

With Hindsight intentionally unavailable, PRIME remained queryable and the rebuild operation returned `UNAVAILABLE` with `mode=SOURCE_LEDGER_REBUILD`; no fake restore success was emitted. After service recovery, the supported `MemoryService.rebuild_from_source_ledger` lifecycle recreated the bank and restored one eligible current ledger row. Superseded and tombstoned rows were excluded. The result was `CURRENT`, explicitly `SOURCE_LEDGER_REBUILD`, and `REBUILDABLE_NOT_BIT_IDENTICAL`.

Negative cases passed: missing required continuity component refused; corrupt/truncated archive refused. Existing wrong-key, tamper, collision, step-up, and interrupted-restore negatives remain covered by Continuation 027 evidence. R-044 is promoted to VERIFIED.

## Hindsight product semantics

Disposable Project A and Project B banks were created as `prime-<project_id>`. A-only and B-only facts remained project-bound at PRIME recall, with no cross-project memory/document identity. Correction recorded reason, source revision, and immutable prior row. Supersession made the old row historical; tombstone excluded the new row from current recall while preserving its history.

DOD-067, DOD-069, and DOD-070 are promoted to PRODUCT_VERIFIED. DOD-068 remains BACKEND_ONLY/open because the approved native Mental Models/reflect path was not available as a complete qualified product behavior.

## Authenticated historical UX

The native Core listener was exercised through the gstack browser tunnel with an authenticated operator session. A disposable Project B was populated with a committed historical source, Goal, Evidence, memory, retained Git checkpoint, and Brain snapshot, then advanced to a current D revision. Time Lens visibly rendered `HISTORICAL`, the selected timestamp, reconstruction status, source statuses, historical Goal content, and historical Brain availability/revision/node count. Historical Ask returned `HISTORICAL`, an evidence-backed answer, and a citation carrying the historical source revision/hash. No later current-only source appeared. Return to Now cleared historical Ask state and reloaded the current boundary. DOD-014 and DOD-015 are promoted to USER_USABLE_VERIFIED.

Source-loss behavior was also exercised: deleting the disposable historical source caused PARTIAL/UNAVAILABLE classification and no current Goal/Brain substitution. Restoration returned the exact source path where reconstructable.

## Fork, Brain, and AI Connections

Clean source Fork/Clone qualification passed A1/A2 selected-revision fidelity, independent destination project/repository identity, dirty-source refusal, independent Goal/Progress/MCP rows, no copied memory, and distinct destination bank identities. A browser fork attempt on the Windows-to-Atlas path exposed a path normalization defect (`C:` was prepended to the native `/tmp` path), so the complete browser Fork workflow remains open. DOD-017 is not promoted solely on API evidence. DOD-016 remains externally blocked by live Notion/Hindsight resource configuration.

Brain scale used a clean clone of the authoritative source: 277 repository files, 324 nodes, 264 edges, 0.338 seconds graph build. Controlled repository observation advanced Brain revision A to B and surfaced `LIVE-BRAIN-037.txt`. A/B Brain and Search markers remained project-isolated. DOD-051 remains open for the full browser interaction/focus-state acceptance.

Authenticated AI Connections rendered safe metadata and completed rotation, revocation, and reissue without secret persistence. DOD-040 is promoted to USER_USABLE_VERIFIED.

## Validation

- Ordinary suite: 66 passed, 28 skipped.
- Fresh zero-state DB-backed suite: 94 passed.
- Fresh PostgreSQL/pgvector: PASS.
- Phases 1–14 on fresh database: PASS.
- Web JavaScript parse: PASS.
- Browser authenticated historical and AI Connections flows: PASS for the stated evidence; full Fork browser flow: PARTIAL.
- Deployment: NOT PERFORMED.
