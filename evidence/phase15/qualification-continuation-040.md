# ANIMUS PRIME — Continuation 040 qualification

## Baseline and boundary

- Execution host: Atlas, by direct SSH, authoritative checkout `/home/sketch/Projects/ANIMUS_PRIME`.
- Starting published tip: `0103367af7fdfcf9dc89fc009c187b914a05070d`.
- Implementation commit for this continuation: `8ef4c1eebeb35861e8c778e939dcc42fc719d5be`.
- Disposable qualification only: Phase-1 PostgreSQL and Hindsight were isolated on ports `15432` and `18888`; production `mimir-hindsight-production` on `127.0.0.1:8888` was not changed.
- Browser access used a local SSH tunnel to the Atlas Core process. The project checkout and Docker services remained on Atlas; the SSHFS `Z:` path was not used as an authority or execution path.
- Deployment, Phase 16, R-056 closure, production Hindsight changes, and new fixture design were not performed.

## Fork / Clone qualification

The direct bounded matrix used the existing Continuation 039 A2 fixture revision and produced a fresh child. Results:

- selected child revision exactly matched source A2 `a52f18dae55b6a66d7d36bde74593e2306ab2156`;
- child retained the source Git history (`2` commits) and had no remotes;
- child `.agent` passed validation and matched the current authority template for every file except the explicitly approved child `PROJECT_GOAL.md`; child goal approval was a new GoalRevision;
- the Fork-created goal was `DRAFT`, child Progress had `0` assessments before explicit approval, then a new baseline was approved and assessed;
- source and child memory ledgers were separate, source and child MCP grants were distinct and project-scoped, and Hindsight bank IDs were distinct;
- a dirty source was refused with `fork requires a clean source working tree`;
- disposable Hindsight retain/recall remained `DEGRADED_IN_DISPOSABLE_PROVIDER`; Notion was `NOT_CONFIGURED_IN_DISPOSABLE_FIXTURE`.

This closes the stale DOD-017 path-normalization audit defect and qualifies the frozen mutable-resource isolation invariant. DOD-016 remains open because its complete resource matrix still requires the separate Notion/Hindsight dependency boundary.

## Project Brain and operator surfaces

Authenticated browser qualification on the A/B fixture passed:

- Brain loaded `EXACT` at `17` nodes and `9` edges with `SOURCE_BASED_ONLY` relationship policy and derived-3D presentation;
- orbit, pan, zoom, reset, revision refresh, repository source filtering, graph-node search, accessible node selection, and selected-file Repository drill-down passed;
- selecting `src/brain-marker.txt` showed its source class, revision, content hash, and edge reason; the read-only Repository viewer returned the bounded text `ALPHA-039-BRAIN`;
- Project A → Project B reset Brain state and loaded B's distinct revision `30d0fc0b4f584fa68d097d370b54a1b8ec8cb63f` without stale A query state;
- Brain search remained graph-node/path search. The frozen contract does not require repository-content search; the stale `ALPHA-BRAIN-039` content-search audit wording is not used.

Activity filters returned source-backed `GIT_COMMIT`, `AUTHORITY_OBSERVED`, and `PROGRESS_ASSESSMENT` events. Git and authority artifacts were labeled; the Git artifact drill-down truthfully reported the unavailable repository file rather than claiming content it could not open.

Repository and Authority rendered canonical revision, bounded tree/file text, `.agent` validation, and hashes read-only. Before/after Atlas fixture Git checks remained unchanged. Search returned grouped Repository, Progress, Evidence, and Activity results for the project-scoped marker; Notion and durable Memory were absent/degraded in the disposable provider and were not promoted. Ask returned the safe `UNKNOWN` state because model execution was unavailable.

## Governed reconciliation

- DOD-017 promoted to `PRODUCT_VERIFIED`.
- DOD-051 promoted to `USER_USABLE_VERIFIED`.
- DOD-016, DOD-021, DOD-022, DOD-043, DOD-059, DOD-060, DOD-062, DOD-063, DOD-068, R-045, and R-056 remain open or blocked exactly where evidence is incomplete.
- Requirements traceability, remediation matrix, qualification ledger, alignment audit, and derived burndown were reconciled to this evidence; no prior VERIFIED remediation row was downgraded.
- §26 mechanical status after reconciliation: `8 USER_USABLE_VERIFIED / 12 PRODUCT_VERIFIED / 18 IMPLEMENTED_NOT_PRODUCT_QUALIFIED / 27 BACKEND_ONLY / 9 UI_SHELL_ONLY / 6 PARTIAL / 0 MISSING / 1 BLOCKED_BY_ENVIRONMENT`; `20 complete + 61 open = 81`.
- Remediation qualification remains `17 VERIFIED / 8 partial / R-056 blocked-open / 0 failed`; the §26 audit count and the requirement-level remediation count are separate governed views.
- The product release gate remains `FAIL`; deployment remains `NOT PERFORMED`.

## Validation states

- Focused pytest (`tests/phase15 tests/phase13`): `PASSED` — 28 passed, 13 skipped.
- Python compilation and `git diff --check`: `PASSED`.
- Governance, YAML, burndown, secret, and final parity checks: recorded in the closure result after the governance commit.
- Full suite and external/native/AT/Notion/approved-provider qualification: `NOT RUN` or `BLOCKED` where stated above; none were treated as passes.
