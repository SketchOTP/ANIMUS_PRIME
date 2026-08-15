# ANIMUS PRIME Phase 15  Continuation 061

## Result

**Status: PARTIAL.** Safe local product implementation advanced and the persistent Atlas Core now runs the final qualified implementation. A real authenticated API probe found and repaired a snapshot crash before operator qualification. Persistent restart recovery and the authenticated Qualification Project API path now pass. The required browser qualification remains blocked by the approved gstack browser tool's missing Playwright dependency; no browser-based promotion is claimed.

## Baseline and boundaries

- Specification: `PRIME-SPEC-V1.0.0`
- Authoritative checkout: `/home/sketch/Projects/ANIMUS_PRIME`
- Starting governed baseline: `4aa8ac051d12bca2f12f0de7471e83c82e3702b8`
- Starting runtime qualified implementation: `0324b380fc5fac54fa037695cfe09146ba850baa`
- Final qualified implementation: `6dd5d805852ab7573ec95d3f4a4f6dfe3a3b3708`
- Product implementation ancestors: `18df5bb`, `202ed00`, then `6dd5d80`
- Existing untracked `.codebase-memory/`, `.prime-evidence/`, and `.vscode/` were preserved.
- No disposable database, project, repository, worktree, Node, browser profile, duplicate Core, public ingress, Funnel change, deployment, Phase 16, or R-056 closure was performed.

## Persistent Atlas topology

| Component | Runtime mechanism | Identity / listener | Result |
|---|---|---|---|
| PostgreSQL | Existing persistent Docker service | `animus-prime-phase0-postgres-1` | Existing database reused; no reset or substitute state |
| Hindsight | Existing persistent service/container | `mimir-hindsight-production`, loopback `127.0.0.1:8888` | Existing service/bank preserved; Reflect/Mental Models remain unavailable |
| PRIME Core + genuine Web UI | PRIME-owned user-systemd service starting Docker | `animus-prime-core`, private `127.0.0.1:18000` | Running image `animus-prime-core:continuation-061-local-product3`; same writable state mount |
| Repository Node | Existing enrolled user-systemd service | canonical Atlas Node, private `127.0.0.1:18001` | Service active; existing identity/state preserved |
| Service manager | `systemd --user` | `animus-prime-core.service`, `animus-prime-node.service` | Both active after rebuild and Core restart |
| Public exposure | None authorized | no Funnel or firewall change | NOT PERFORMED |

Readiness after the persistent swap and subsequent Core restart returned:

- spec revision: `PRIME-SPEC-V1.0.0`
- build commit: `6dd5d805852ab7573ec95d3f4a4f6dfe3a3b3708`
- image identity: `animus-prime-core:continuation-061-local-product3`
- schema: `0035_notifications_lifecycle.sql`
- service version: `1.0.0`

The container was swapped under the existing PRIME-owned service identity with the previous container retained as `animus-prime-core-rollback-061-product3`. The existing environment references, read-only checkout mount, writable runtime state mount, host networking, user, workdir, and command were preserved. No raw environment values were recorded.

## Product implementation and repair

Implemented in the earlier Continuation 061 product commits:

- additive notification lifecycle fields/migration, dedupe and resolve behavior, open-list and dismiss routes;
- GoalItem-derived advisory alignment and stable milestones;
- data-backed snapshot/context alignment output;
- genuine UI Notifications rendering and dismiss control;
- guarded Backup create/preflight controls using the existing step-up/confirmation boundary;
- related UI polish.

Observed defect during the first real authenticated API probe:

- `GET /v1/projects/project_d9a1a5b609394282b62fc12c0d04634d/snapshot` returned HTTP 500;
- root cause: `_project_snapshot` reused the `progress` service variable for the database assessment row, then attempted `progress.alignment(...)`;
- minimal repair: rename the row to `progress_row`, preserve the `ProgressService` instance, and add a focused regression assertion;
- repair commit: `6dd5d805852ab7573ec95d3f4a4f6dfe3a3b3708`.

## Authenticated persistent API qualification

Using the existing trusted-host local identity flow and the existing Qualification Project only:

- SIGN_IN challenge/Atlas approval/redeem: **PASSED**; no credential value was recorded.
- `/v1/operator/state`: **PASSED**; existing project registry returned.
- Qualification Project selection: **PASSED**; project ID `project_d9a1a5b609394282b62fc12c0d04634d`.
- Project snapshot: **PASSED** after repair; returned the same ACTIVE/ONLINE project.
- Alignment: **PASSED as truthful degraded state**; `UNKNOWN` because no current evidence-backed assessment exists, with stable GoalItem/milestone identities and no authority mutation.
- Notifications endpoint: **PASSED**; zero open notifications because the real project had no active attention conditions.
- Context export: **PASSED**; authenticated response returned provenance-bearing output.
- Core restart recovery: **PASSED**; after `systemctl --user restart animus-prime-core.service`, readiness returned and the same Qualification Project remained ACTIVE/ONLINE with alignment UNKNOWN and zero open notifications.
- Genuine UI shell: **PASSED over private HTTP GET**; the served page contained the Notifications and Backup controls and retained no-store, frame-deny, and restrictive content-security headers. This is not a substitute for browser qualification.

## Requested product surfaces

- Notifications: **IMPLEMENTED; API/structural qualification PASSED; browser lifecycle BLOCKED**. No active notification existed in the real project to safely dismiss or resolve.
- Goal Alignment/Milestones: **IMPLEMENTED; API qualification PASSED with truthful UNKNOWN state; browser BLOCKED**.
- Backup: **Controls implemented and guarded; structural qualification PASSED; no destructive restore or export mutation performed**.
- Integrity: **Existing persistent snapshot/provenance path remained healthy; negative browser qualification NOT RUN**.
- Registration: **No mutation or synthetic repository was created; duplicate/outside-root/traversal/non-Git negative browser matrix NOT RUN**.
- Polish: **UI shell markers/security headers PASSED; responsive, keyboard, console, reduced-motion, and touch checks BLOCKED pending approved browser tool**.

## Operator journey

The real browser journey remains **BLOCKED** for this continuation because the required gstack `/browse` executable could not start:

- direct execution from the SSHFS checkout attempted to create `.gstack` on the read-only UNC-backed path and failed with EPERM;
- local execution reached the bundled `server-node.mjs`, which failed with `ERR_MODULE_NOT_FOUND: Cannot find package 'playwright'`;
- existing unrelated Chrome/Node processes were not altered;
- no package installation or disposable browser profile was used.

Therefore Authentication, Home, Needs Attention, project selection, Overview, Progress, Ask, Search, Memory, Knowledge, Evidence, Activity, responsive behavior, keyboard flow, and browser restart/logout/re-login are **NOT promoted by 061**. Prior truthful browser evidence remains preserved.

## DOD and gate status

- DOD-005: **BACKEND_ONLY / PARKED**; no source mutation was attempted.
- DOD-026, DOD-027, DOD-049, DOD-080: **PARTIAL**; no browser promotion.
- DOD-047: **PARTIAL**; provider boundary remains truthful.
- DOD-048: **UI_SHELL_ONLY**.
- DOD-054: **IMPLEMENTED_NOT_PRODUCT_QUALIFIED**.
- DOD-009: **PRODUCT_VERIFIED** remains preserved from prior governed evidence.
- DOD-056: **USER_USABLE_VERIFIED** remains preserved from prior governed evidence.
- Aggregate qualifier: **BLOCKED** by the established secure database/environment boundary; no substitute database was created.
- R-056: **OPEN / GATED**.
- Phase 15: **PARTIAL**.
- V1: **NOT DECLARED**.
- Deployment: **NOT PERFORMED**.

## Validation

- Focused Continuation 061 product + web-shell tests: **PASSED  5 passed**.
- Full repository regression: **PASSED  104 passed, 28 skipped**. The increase from 100 passed is the four Continuation 061 product tests; skip count unchanged.
- Compile/static: **PASSED**  `.venv/bin/python -m compileall -q apps src tests`.
- Governance: **PASSED**  adopted validator.
- Burndown: **PASSED**  81 total, 47 complete, 34 open; declared counts and work classes reconcile.
- Product alignment audit: **PASSED** structurally; overall V1 alignment remains FAIL by design.
- Diff check: **PASSED**.
- Tracked secret scan: **PASSED**  no tracked private-key or common-token matches.
- Persistent runtime health/listeners/restart: **PASSED**.
- Browser qualification: **BLOCKED**  missing bundled Playwright dependency in gstack browse.
- Production-image full pytest: **NOT RUN / BLOCKED**  the image lacks PyYAML and the repository mount is read-only for pytest cache; the enrolled Atlas `.venv` regression is the authoritative repository test run.

## Remaining gaps

The 061 implementation is additive but not a Phase 15 completion claim. Browser qualification of the new surfaces, registration negatives, integrity negatives, full backup lifecycle, and remaining local/external requirements are still open. Notifications had no live condition in the existing project, so no fabricated test row was created. DOD-005, the aggregate qualifier, high-risk rows, external integrations, R-056, Phase 15 completion, V1, and deployment remain gated.
