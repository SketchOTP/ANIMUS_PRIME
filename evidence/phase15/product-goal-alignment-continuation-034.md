# ANIMUS PRIME — Continuation 034 Evidence

- Directive: `D-PRIME-PHASE15-PRODUCT-COMPLETION-034`
- Baseline: `PRIME-SPEC-V1.0.0`
- Execution host: Atlas, direct native SSH
- Published baseline: `b325390f72d4ec0bd7f23f39ba75293fcc9b13f5`
- Deployment: NOT PERFORMED

## Clean published artifact

A disposable native Atlas worktree was created at the exact published tip. The
checkout had no untracked files and `git status --porcelain` was empty.

- `git rev-parse HEAD`: `b325390f72d4ec0bd7f23f39ba75293fcc9b13f5`
- Migration `0025_product_onboarding.sql`: mode `664`, `sketch:sketch`
- Migration `0026_product_completion_wave3.sql`: mode `664`, `sketch:sketch`
- Core image: built from the clean checkout with `Dockerfile.core`
- Image runtime user: `nobody` (`uid=65534`, `gid=65534`)
- Migration modes inside image: both `664`, readable by `nobody`
- Fresh PostgreSQL/pgvector: healthy
- Applied migrations: `26`, latest `0026_product_completion_wave3.sql`
- `/health/live` before restart: PASSED
- Core restart: PASSED
- `/health/live` after restart: PASSED
- Compose health after restart: healthy

Classification: `DEVELOPMENT_WORKTREE_PERMISSION_CONTAMINATION`.

The published checkout and normal unprivileged image work. The long-lived
development checkout still contains unrelated local migration mode `660`
changes, which were not chmodded, rewritten, staged, or included in this
qualification. Packaging repair: NONE.

## Actionable burndown

`docs/v1-product-gap-burndown.yaml` was rebuilt from the authoritative audit,
traceability, remediation matrix, and qualification ledger. The validator
reported:

- audit total: `81`
- complete rows: `11`
- burndown rows: `70`
- complete plus burndown: `81`
- ID parity: PASSED
- status parity with audit: PASSED
- required fields: PASSED
- valid work classes: PASSED
- concrete exact behavior and next action fields: PASSED

Work classes:

- `LOCAL_CODE`: `12`
- `LOCAL_BROWSER_QUALIFICATION`: `28`
- `LOCAL_NATIVE_QUALIFICATION`: `0`
- `EVIDENCE_RECONCILIATION`: `1`
- `EXTERNAL_ENVIRONMENT`: `29`
- `AGGREGATE_RELEASE_GATE`: `0`

DOD-079 now distinguishes the available Linux host/systemd inspection from the
separate Windows-host dependency. It remains blocked because the repository
does not expose a deterministic native service installer/unit for Linux
qualification and no supported Windows host is in scope.

## High-yield current product regression

An authenticated disposable fixture was loaded through the current product
against a read-only fixture mount. The fixture contained two isolated project
records, two enrolled node records, nine repository files, GoalItems, weighted
progress history, authority files, memory, evidence, activity, and degraded
Notion/AI states.

Observed current behavior:

- Brain graph loaded with `10` nodes and `6` edges, source-labelled accessible
  fallback, and `derived-3d` interaction metadata. Representative-scale,
  live-update, and Project A/B isolation acceptance was not demonstrated.
- Repository tree and bounded text files loaded after mounting the disposable
  fixture read-only. Canonical Git revision was `UNAVAILABLE` in that read-only
  browser container, so mutation-proof Git qualification was not promoted.
- Search returned three project-scoped results, but only Repository and Activity
  source groups. Required full Repository/.agent/Git/Notion/Memory/Activity
  grouping and A/B isolation were not demonstrated.
- Ask returned truthful `UNKNOWN` because model execution was unavailable.
- Time Lens returned `HISTORICAL now · UNAVAILABLE`; the required historical
  selector/reconstruction/Brain/Return-to-Now acceptance was not promoted.
- AI Connections rendered safe metadata and `NEVER_RETURNED_AFTER_ISSUANCE`
  policy with an empty grant state. The full issue/list/rotate/old-reject/new-
  accept/revoke/reject/reissue lifecycle was not run.
- Activity rendered source-free events with `source revision: NONE`; the
  source-backed Git/Authority/Goal/Progress/Evidence/AI drill-down matrix was
  not promoted.
- Ask, Time Lens, Search, AI Connections, Activity, Brain, Repository, and Git
  remained at their existing audit statuses. No DOD was promoted from shell
  presence or degraded-state rendering.

The fixture exposed a qualification setup boundary: the default disposable
Core service does not mount host-side fixture paths. A second disposable Core
container was used only for browser qualification, retained `USER nobody`, and
mounted the exact fixture read-only. No long-lived project data or containers
were changed.

## Environment boundaries

- Linux: Atlas is a live systemd host; current operator is `uid=1000(sketch)`.
  Noninteractive sudo is limited to an unrelated hardware service restart. No
  PRIME native service installer or unit surface was found in `src/prime_node`,
  `apps/node`, or `scripts`.
- Windows: no supported Windows host qualification was performed.
- Tailscale: installed and running with one visible self peer; existing Funnel
  and tailnet Serve configuration was inspected only. No Funnel or Serve state
  was modified. An approved second device was not available.
- Hindsight: the Atlas Hindsight container health endpoint returned healthy and
  database connected, but the approved PRIME retain/bank path remained
  unavailable in Core. No Hindsight redesign or fabricated qualification was
  performed.
- External assistive technology: not available; browser accessibility output
  was not treated as equivalent.
- Live Notion: current process reported `REAUTH_REQUIRED`; no new live write or
  separate fork Project Record was fabricated.

## Validation

- Clean published checkout and normal unprivileged Core startup: PASSED
- 26 migrations and Core restart: PASSED
- Full pytest with importlib collection: PASSED (`64 passed, 27 skipped`)
- Phases 1–14: PASSED
- Native Python compileall: PASSED
- Adopted governance validation: PASSED
- Product alignment audit: PASSED structurally; V1 gate remains FAIL
- Actionable burndown validation: PASSED
- `git diff --check`: PASSED
- Precise tracked secret scan: PASSED
- Browser qualification: PASSED for authenticated fixture loading and truthful
  degraded states; complete DOD promotion: NOT RUN / NOT JUSTIFIED
- Fork browser/isolation: NOT RUN
- Deployment: NOT PERFORMED

Continuation 034 remains a truthful `PARTIAL` closure. The clean published
artifact is not a packaging defect. The burndown is now an execution queue, but
Brain completion, Fork isolation, current Time Lens/Search/Ask/AI/Activity
qualification, native Node lifecycle, Windows, Tailscale second-device,
Hindsight, external AT, and R-056 remain open.
