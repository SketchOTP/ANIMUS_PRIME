# ANIMUS PRIME - Continuation 039 Qualification Evidence

Date: 2026-08-13  
Execution: DIRECT SSH / NATIVE ATLAS  
Checkout: `/home/sketch/Projects/ANIMUS_PRIME`  
Baseline tip: `27ce9619fe1c5c733843d4fddea252270c39c231`  
Baseline: `PRIME-SPEC-V1.0.0`

## Scope and fixture

This cycle used the native Atlas checkout and a disposable Core/Node/PostgreSQL/Hindsight stack. The existing production Hindsight service `mimir-hindsight-production` was not changed. A single reusable fixture builder created exactly two independent projects before browser qualification:

| fixture | project | repository | canonical revision | Brain | PRIME memory | Hindsight bank |
|---|---|---|---|---:|---:|---|
| A | `project_31f2062c839e43e6995bfc16352afc3f` | `/qualification/continuation-039-project-a` | `f9cbb02a36b1a2ff693f7288f9775f1d7de84e0b` | 17 nodes / 9 edges | 4 records | `prime-project_31f2062c839e43e6995bfc16352afc3f` |
| B | `project_72d462bcceb64916898cca472e3301d9` | `/qualification/continuation-039-project-b` | `55895b2818f93f4f524af5db3492e7f5f8f0a54b` | 17 nodes / 9 edges | 4 records | `prime-project_72d462bcceb64916898cca472e3301d9` |

Both fixture repositories were real Git repositories with clean working trees, distinct A/B markers, authority packages, approved goals, progress assessments, evidence, activity, MCP grants, retained Git checkpoints, and project-bound Hindsight retain/recall evidence. Notion remained `DISCONNECTED`/`UNCONFIGURED`; no external Notion qualification was claimed.

The builder initially exposed two disposable setup defects: the Core container could not reach the host-mapped Hindsight port, and a correction test superseded its only current fact. The disposable compose override was corrected to route Hindsight through `host.docker.internal:18888`, and the fixture now retains a current durable anchor while keeping correction-seed and tombstoned rows separate. The final builder run asserted authority validity, nonzero Brain topology, recallable Hindsight results, and clean Git state.

## Brain and browser state

Authenticated browser qualification passed for both A and B:

- Brain returned `availability=EXACT`, the selected fixture revision, `17` nodes, `9` edges, `layout=derived-3d`, and `relationship_policy=SOURCE_BASED_ONLY`.
- Orbit-left, orbit-right, pan, zoom, reset-camera, accessible list, source-class filtering, and node selection controls were exercised.
- Filtering out the selected node now clears stale selection details and reports `No node selected.`.
- Switching A to B clears project-scoped Brain query/filter, Ask/Search inputs, Activity filter, Time Lens custom boundary, source selection, and selected Brain details. B loaded its own revision and topology without A query residue.
- The exact DOD-051 literal `ALPHA-BRAIN-039` was not promoted: the current Brain filter searches node label/kind, while the fixture marker is content in `src/brain-marker.txt`; the exact literal therefore returned zero nodes. This is an honest product qualification gap, not a fixture substitution.

## Fork / Clone and isolation

Browser Fork from A passed with real destination repositories:

- A1 source `d8eb28c14ca710067d63165b2b8ed9221792267f` created `project_1094466bb6aa49d2b2f66a7f2bc0e88f` at `/qualification/c039-fork-a1`, indexed destination revision `14db768cd4932bafc71821d83f3b6d58e9579336`, and produced the real fork commit `14db768 Fork from d8eb28c...`.
- A2 source `f9cbb02a36b1a2ff693f7288f9775f1d7de84e0b` created `project_ce0dfffef3004f03862a4860da1023ff` at `/qualification/c039-fork-a2`, indexed destination revision `9248d301fad4be81a3277cb7dfb716c20b0c9ba1`, and produced the real fork commit `9248d30 Fork from f9cbb02...`.
- A dirty-source attempt was made after adding one exact disposable untracked file. The API stopped safely with `fork requires a clean source working tree`; the file was removed and the source returned clean.
- Fork results explicitly reported `Memory: NONE; Notion: NOT_COPIED.` The complete DOD-016 resource-status matrix and every DOD-017 isolation negative case were not fully re-run, so DOD-016 and DOD-017 remain open and unpromoted.

## Activity, Repository, Search, Progress, Ask

- Activity loaded all six project events with sequence, source revision, source artifact, and payload. Filtering `GIT_COMMIT` returned exactly the Git event.
- Repository tree loaded the A repository at canonical revision `f9cbb02...` and returned the authority, source, marker, and project files through the read-only viewer.
- Search returned A-scoped `ALPHA-039` results across Activity, Progress, Memory, and Evidence. Exact Repository/Authority source-class coverage and the complete A/B negative-isolation search matrix were not established; DOD-022 remains open.
- Progress showed `100`, confidence `0.9`, and `CURRENT`; no new governed promotion was made.
- Ask returned the safe result `UNKNOWN: model execution is unavailable or the evidence does not support a safe answer`, with a project-scoped Memory citation. Approved model execution remains unavailable; DOD-021 remains open.

## Hindsight and remaining boundaries

Fixture Hindsight retain/recall was independently recallable for both A and B. A direct `PrimeMemoryAdapter.reflect()` probe against the disposable A bank returned `UNAVAILABLE` after the adapter's bounded 30-second timeout. No reflect or Mental Models promotion was made; DOD-068 remains open. R-045 remains partial/open. R-056 remains blocked/open. No native Node/Windows lifecycle, Tailscale/second-device, assistive-technology, external Notion, or production deployment evidence was fabricated. Phase 16 was not started.

## Governed state and validation

The authoritative counts remain unchanged: §26 `7 USER_USABLE_VERIFIED / 11 PRODUCT_VERIFIED / 20 IMPLEMENTED_NOT_PRODUCT_QUALIFIED / 27 BACKEND_ONLY / 9 UI_SHELL_ONLY / 6 PARTIAL / 0 MISSING / 1 BLOCKED_BY_ENVIRONMENT`; `18 complete / 63 open`; burndown `11 LOCAL_CODE / 24 LOCAL_BROWSER_QUALIFICATION / 0 LOCAL_NATIVE_QUALIFICATION / 3 EVIDENCE_RECONCILIATION / 25 EXTERNAL_ENVIRONMENT / 0 AGGREGATE_RELEASE_GATE`; remediation `17 VERIFIED / 8 partial / R-056 blocked-open / 0 failed`.

- `.venv/bin/python -m pytest tests scripts -q`: PASSED (`75 passed, 28 skipped`).
- Adopted governance validator: PASSED.
- Product-gap burndown validator: PASSED; `81` rows, `18` complete, `63` open.
- Product-alignment audit: PASSED; frozen V1 product goal: FAIL, as expected.
- Diff check: PASSED.
- Changed-file secret scan: PASSED.
- Notion publication: PENDING at evidence creation; verified after the final governed commit.
- Deployment: NOT PERFORMED.
