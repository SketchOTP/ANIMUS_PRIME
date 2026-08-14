# ANIMUS PRIME Phase 15 — Continuation 054

## Result

**Status: PARTIAL.** The existing single-operator Atlas installation now has a persistent authenticated PRIME Core and genuine Web UI, and the original operator journey was exercised through the real private runtime. The existing repository Node was not started because the checkout does not contain an approved governed enrollment/certificate lifecycle or usable mTLS trust material. No insecure HTTP fallback, fabricated certificate, disposable replacement environment, public exposure, or unrelated service change was used.

## Baseline

- Specification: `PRIME-SPEC-V1.0.0`
- Authoritative checkout: `/home/sketch/Projects/ANIMUS_PRIME`
- Starting governed commit: `6932c0541cbd37b805c64b30b1bf77118674ff14`
- Baseline validation: 90 passed, 28 integration skips (Continuation 052)
- Existing persistent PostgreSQL: `animus-prime-phase0-postgres-1`, reused
- Existing persistent Hindsight: `mimir-hindsight-production`, reused at loopback `127.0.0.1:8888`
- Existing qualification project: `project_d9a1a5b609394282b62fc12c0d04634d`, `Qualification Project`
- Existing unrelated listeners on Atlas were inspected and left untouched
- Pre-existing untracked `.codebase-memory/`, `.prime-evidence/`, and `.vscode/` were preserved

## Recovery and operator identity

The existing approved password and existing recovery credential were not present in the governed Atlas runtime references. Direct password-hash editing was not used. A minimum local break-glass path was implemented in the repository and applied to the existing operator only:

- `migrations/prime/0031_local_recovery.sql` adds a digest-only local recovery reference.
- `packaging/core/local-recovery.sh` is loopback-only, requires a deliberate local credential, stores only mode-600 references, rotates the normal password and recovery credential, revokes active sessions, and reports no secret values.
- Core routes enforce loopback origin/address and a local recovery header; the browser UI does not expose this path.
- Recovery audit events were recorded for provisioning and reset.
- A transient local diagnostic/browser-state exposure of one-time values was detected during qualification. All affected values were immediately invalidated by rotation; no secret value was committed, written to evidence, or sent to Notion.
- The same operator identity remained in use. Re-login with the final rotated password succeeded after the recovery reset, while the pre-reset session returned HTTP 401.

## Persistent Atlas topology

| Component | Runtime mechanism | Identity / listener | Persistence and result |
|---|---|---|---|
| PostgreSQL | Existing persistent Docker container | `animus-prime-phase0-postgres-1` | Existing database reused; schema migration `0031_local_recovery.sql` applied |
| Hindsight | Existing persistent service/container | `mimir-hindsight-production`, `127.0.0.1:8888` | Existing bank reused; service/retain/recall current, Reflect unavailable and Mental Models unsupported |
| PRIME Core + Web UI | PRIME-owned `systemd --user` service starting Docker container | `animus-prime-core`, `127.0.0.1:18000` | `animus-prime-core:continuation-054`, read-only image/root with existing writable runtime state mount; `/health/ready` returned `ready` with schema `0031_local_recovery.sql` |
| Repository Node | Existing database records only | No PRIME-owned Node service or mTLS listener | Not started; TLS-required configuration correctly refused startup without approved cert/key/CA material |

The Core image was rebuilt in place and the previous PRIME-owned container was retained as a named rollback artifact. The service manager remained `systemd --user animus-prime-core.service`; no second Core instance was started. The Core served the genuine `apps/web/index.html` UI; no static or diagnostic substitute was used. Public exposure remained disabled and the existing unrelated Funnel/Tailscale configuration was not changed.

## Operator journey

Browser: Chromium controlled through the approved gstack browse skill, via the existing local SSH tunnel `127.0.0.1:28000` to Atlas loopback `127.0.0.1:18000`.

- Protected entry and wrong-password rejection: PASSED. Invalid credentials were rejected without revealing authentication details.
- Authentication and re-login: PASSED. Authenticated `/v1/operator/state` and `/v1/system/setup` returned 200.
- Home: PASSED. Core/database state was healthy and the real project registry loaded.
- Needs Attention: PASSED. The real project surface rendered its current conditions; no synthetic project was created.
- Project selection: PASSED. Existing `Qualification Project` opened with ACTIVE / ONLINE / CURRENT state.
- Overview: PASSED. Goal, binding, integrity, progress, and activity surfaces loaded.
- Progress: PASSED. Existing current assessment and history rendered with source revision and confidence.
- Ask: PASSED as truthful degraded behavior. The unavailable model returned `UNKNOWN` rather than an unsupported answer.
- Search: PASSED. A project-scoped query returned repository and memory source groups with freshness labels.
- Memory: PASSED. Existing PRIME memory records and Hindsight capability state rendered.
- Knowledge: PASSED as truthful degraded behavior. Notion was shown disconnected/unavailable rather than fabricated as connected.
- Evidence: PASSED as truthful empty/current state. No current Evidence rows were manufactured.
- Activity: PASSED. Existing project events rendered.
- Brain: PASSED. Existing project loaded an `EXACT` derived graph with 2 nodes and 1 edge.
- Time Lens: PASSED. A historical commit loaded as `PARTIAL` with explicit availability boundaries.
- Repository: PASSED. The existing canonical path, branch, revision, and read-only repository tree loaded.
- Authority: PASSED. The `.agent` authority chain and validation state loaded.
- Refresh/restart continuity: PASSED. Selected project state now persists as a non-secret project ID in browser local storage, was restored after page refresh, and the same project remained available after Core restart/reload. This repaired the observed `Select a project first` failure on Time Lens and Brain after refresh.

## Node boundary and DOD follow-through

The existing database contained Node records, but inspection found no approved Atlas Node service definition, governed bootstrap/enrollment flow, certificate/key/CA references, or long-lived mTLS credential that could be safely activated. The packaged Node correctly refuses to run without TLS material; the insecure HTTP override was not used. Therefore:

- Repository Node: **NOT STARTED — BLOCKED by missing governed mTLS enrollment/trust lifecycle**.
- DOD-074 operator-visible offline-Node journey: **NOT REQUALIFIED in this continuation** because the legitimate Node cannot be brought to a healthy enrolled state without inventing trust material. Existing backend continuity evidence remains preserved and truthful.
- DOD-005 operator-visible source lifecycle: **PARTIAL**. Current Progress, Search, and Memory surfaces were inspected; no current Evidence rows or approved Notion projection were available to exercise the full retraction path.

## Repairs

### Local recovery

- User-visible problem: existing operator could not be recovered through an approved available credential path.
- Root cause: no usable password/recovery reference and no repository implementation of the spec-required local break-glass path.
- Minimal repair: digest-only loopback recovery provision/reset endpoints, secure external references, session revocation, rotation, and audit.
- Tests: `tests/phase1/test_local_recovery.py` covers loopback enforcement and non-secret one-time response shape.
- Result: same operator recovered and re-authenticated; old session rejected.

### Project selection continuity

- User-visible problem: after refresh/restart, Time Lens and Brain reported `Select a project first` despite an authenticated project session.
- Root cause: `activeProjectId` existed only in page memory; refresh rebuilt the project list without restoring selection.
- Minimal repair: persist only the selected project ID in browser local storage, validate it against the authenticated project list, restore it through the existing load path, and clear it on logout or invalid selection.
- Result: Qualification Project restored after refresh and Core restart; Brain and Time Lens loaded successfully through the persistent UI.

## Validation record

Secret scans exclude the mode-600 Atlas runtime reference directory and never print its contents.

- Focused local recovery and Node safety tests: **PASSED** — 6 passed
- Full regression: **PASSED** — 92 passed, 28 skipped. The two-test increase from the 052 baseline is the new local-recovery coverage; the integration skip count is unchanged.
- Compile/static checks: **PASSED** — Python compileall and shell syntax
- Governance: **PASSED** — adopted validator
- Burndown: **PASSED** — counts, IDs, statuses, acceptance kinds, work classes, and fields reconciled
- Product alignment: **PASSED** for the audit; broader V1 product-goal alignment remains **FAIL** by design
- YAML and diff checks: **PASSED**
- Runtime health and service persistence: **PASSED** — systemd active/enabled and `/health/ready` ready on schema `0031_local_recovery.sql`
- Browser operator qualification: **PASSED** for the listed surfaces; Node-dependent steps remain blocked

## Governed closeout

- Qualified implementation commit: `f36234e` (`phase15-continuation-054-operator-recovery`)
- Local HEAD / `origin/main` / GitHub `main`: required to be equal before publication is reported
- Notion: a new child checkpoint for Continuation 054 is required; prior checkpoint pages are not reused
- Deployment: **NOT PERFORMED**
- Phase 16: **NOT CREATED**
- R-056: **OPEN / GATED**
- Phase 15: **PARTIAL**
- V1: **NOT DECLARED**
