# ANIMUS PRIME — Continuation 082

## Acceptance

`PARTIAL` — local release-closure and normalization wave completed. One frozen DOD row (DOD-050) was promoted to `USER_USABLE_VERIFIED`; the remaining queue is reduced from 20 to 19 open rows. Phase 15, DOD-081, and R-056 remain open. DOD-005 remained parked as directed.

No public exposure, deployment, Funnel change, destructive restore, synthetic project, synthetic Node, synthetic repository, or Phase 16 activity occurred.

## Baseline and authority

- Frozen specification: `PRIME-SPEC-V1.0.0`.
- Starting governed/public baseline: `5ba226c9c4c680dfcbe037df1713618e2739ff6b`.
- Qualified implementation commit: `c850aa947882cf78138bb245f9cd42d11323decb` (`fix: restore operator surface script loading`).
- Local worktree contained the pre-existing untracked `.codebase-memory/`, `.prime-evidence/`, and `.vscode/` directories; they were preserved and not staged.
- Direct execution authority: Atlas SSH checkout `/home/sketch/Projects/ANIMUS_PRIME`; no `Z:` path was used for runtime execution.
- The final governed publication SHA is recorded by the closeout commit and final parity check.

## Persistent Atlas runtime

| Component | Observed state |
|---|---|
| PostgreSQL | Existing persistent `animus-prime-phase0-postgres-1`, healthy; PRIME Core remains attached to the existing database/schema. |
| Hindsight | Existing persistent service; `127.0.0.1:8888/health` returned `{"status":"healthy","database":"connected"}`. Reflect/Mental Models remain truthfully unavailable in the current setup and were not changed here. |
| Repository Node | Existing enrolled Atlas Node; `animus-prime-node.service` active. No replacement Node created. |
| PRIME Core | Systemd user service `animus-prime-core.service` active; container `animus-prime-core`, image `animus-prime-core:continuation-082`, container user `1000:1000`. |
| Core process identity | Container ID `92585deb731d63ba999474c99cfdf98b0b878e4dd05d7c1e8b7204c714c53df5`; observed MainPID `2464902`; observed start `2026-08-17T13:52:10.251834717Z`. |
| Core health | `/health/ready` returned `ready`, spec `PRIME-SPEC-V1.0.0`, build `c850aa9`, schema `0039_usage_limits_and_upgrade_preflights.sql`. |
| Web UI | Genuine `apps/web/index.html` through the persistent Core private listener; browser URL was `http://127.0.0.1:28000/` over an SSH local forward to Atlas `127.0.0.1:8000`. |
| Public exposure | None. No Funnel, public ingress, firewall broadening, or unrelated service change. |
| Persistence | PostgreSQL state, Hindsight state, repository binding, Node identity, and runtime state remained on the existing Atlas installation. |

The prior Core container was retained stopped as `animus-prime-core-081-preserved-082` for rollback, and the intermediate pre-rebuild container was retained stopped. Only one PRIME Core instance was active.

## Product changes

The qualified implementation adds the smallest V1-linked runtime surface for:

- project-scoped daily/monthly usage limits with durable PostgreSQL policy state;
- operator-visible limit configuration and truthful `EXCEEDED` refusal;
- upgrade status and append-only compatibility preflight records;
- no-op `READY`, backup-required `REFUSED`, downgrade `REFUSED`, and interrupted-migration `RECOVERY_REQUIRED` states;
- persistent UI controls for Usage and Upgrades;
- migration `0039_usage_limits_and_upgrade_preflights.sql` and focused tests.

No provider, Hindsight, Notion, Tailscale, Windows, second-device, or external architecture was changed.

## Direct workflow qualification — DOD-004 boundary

Using the existing Qualification Project `project_d9a1a5b609394282b62fc12c0d04634d` only:

- durable workflow identity was created with idempotency key `continuation-082-qualification-workflow`;
- replay with the same idempotency key returned the same workflow identity;
- `inspect_persistent_state` began and completed with `PURE_OR_DB_TRANSACTION`;
- `record_operator_result` began and completed with `IDEMPOTENT_EXTERNAL`;
- a real repository binding resource reference was recorded for `/home/sketch/Projects/ANIMUS_PRIME`;
- resume planning returned both completed steps, no ambiguity, no reconciliation requirement, and `next_safe_action: COMPLETE`.

This directly qualifies the durable local primitives. DOD-004 remains `BACKEND_ONLY` because Fork, Notion, Hindsight, restore, archive, and the complete interruption/orphan/compensation matrix were not run.

## Usage and cost — DOD-047 / R-045 boundary

The real browser displayed historical project-scoped usage records, provider identity, units, and truthful `estimated cost: UNAVAILABLE` state. Through the Usage form, a daily `ASK_PRIME` limit was saved on the real Qualification Project. The direct enforcement check refused a projected request above the consumed budget with `allowed=false`, `status=EXCEEDED`; the policy was then disabled and verified as `DISABLED` so the qualification did not leave an arbitrary active limit on the governed project.

DOD-047 remains `PARTIAL`. Authoritative provider-backed cost attribution and the remaining capacity/retention telemetry clauses of R-045 still require the approved provider/profile or other legitimate external condition.

## Backup — bounded DOD-049 result

An encrypted continuity export was created from the real Qualification Project and moved to existing durable Atlas storage:

`/mnt/storage1tb/project-archives/ANIMUS_PRIME/continuation-082/prime-continuity-082.bundle`

- size: `10576307` bytes;
- mode: `600`;
- SHA-256: `67b28f2d74d53e3cae6c89a285bd63416e83af8ab9cd482f11c67a863af620f6`;
- backup service result: verified, schema `0039`, real project count `1`;
- browser showed verified backup state and guarded restore preflight.

No destructive restore or recovery was attempted against the governed Atlas installation. DOD-049 remains `PARTIAL` pending an approved independent restore target.

## Upgrade qualification — DOD-050

Through the genuine browser Settings surface on the persistent Core:

1. Current build/schema inspection showed `c850aa9`, image `animus-prime-core:continuation-082`, and schema `0039_usage_limits_and_upgrade_preflights.sql`.
2. A no-op preflight for service `1.0.0` and the current schema returned `compatibility=NO_OP`, `status=READY`, and no installation change.
3. A schema-changing preflight without an available verified backup returned `compatibility=BACKUP_REQUIRED`, `status=REFUSED`.
4. With the backup-available qualification flag set, the same guarded interrupted-migration path returned `compatibility=RECOVERY_REQUIRED`, `status=RECOVERY_REQUIRED`, with guidance to recover from the verified continuity backup and confirmation that no partial migration was applied by preflight.

DOD-050 is promoted to `USER_USABLE_VERIFIED`. No migration was applied and no release was deployed.

## Remaining local/external normalization

- DOD-053 remains backend-only with the exact blocker `LEGITIMATE_SECOND_ENROLLED_LAN_MACHINE_AND_PROJECT_TARGET_REQUIRED`.
- DOD-058 remains partial; no fresh Goal target or governed Goal rewrite was manufactured.
- DOD-077 remains partial; protected negative deletion paths remain qualified, but positive destructive deletion was not performed.
- DOD-080 remains partial; the existing no-overflow/focus/console/refusal evidence is preserved, but the full frozen polish acceptance is not newly claimed.
- DOD-005 remained parked.
- Notion runtime credential/resource prerequisite from 067 remains unresolved.
- Hindsight Reflect/Mental Models current-setup limitation remains unresolved outside this bounded wave.
- DOD-081 and aggregate R-056 remain last/gated.

Mechanical reconciliation after the sweep:

- audit: 81 total; `32 PRODUCT_VERIFIED`, `30 USER_USABLE_VERIFIED`, `6 BACKEND_ONLY`, `5 IMPLEMENTED_NOT_PRODUCT_QUALIFIED`, `7 PARTIAL`, `1 BLOCKED_BY_ENVIRONMENT`;
- release queue: `62 complete / 19 open`;
- open work classes: `4 LOCAL_CODE`, `9 LOCAL_BROWSER_QUALIFICATION`, `6 EXTERNAL_ENVIRONMENT`;
- no failed rows were introduced.

## Operator journey

The real browser reloaded the persistent UI and showed `Qualification Project · ACTIVE · ONLINE · freshness CURRENT`. Existing 081 operator evidence remains preserved for Authentication, Home, Needs Attention, project selection, Overview, Progress, Ask, Search, Memory, Knowledge, Evidence, and Activity. Continuation 082 newly exercised the Usage and Upgrade surfaces on the same real project. The browser console contained historical unauthorized/degraded requests during the preserved session, but no new script-loading error remained after the c850 rebuild; the bounded UI controls rendered and operated successfully.

## Validation

- Focused tests: `PASSED` — `11 passed in 0.32s` for `tests/phase15/test_continuation_082_local_closure.py`, `tests/phase15/test_continuation050.py`, and `tests/phase15/test_runtime_provenance.py`.
- Compile/import checks: `PASSED` — `py_compile` for changed Python modules and `import apps.core.main`.
- Browser: `PASSED` for persistent reload, current-project state, Usage limit configuration/refusal/disable, Upgrade status, no-op preflight, backup-required refusal, and recovery-required preflight using gstack `/browse`.
- Persistent runtime health: `PASSED` — Core ready, systemd active, Hindsight healthy, PostgreSQL healthy, Node active.
- Governance/burndown/traceability YAML parse: `PASSED` after reconciliation; final repository governance suite is recorded at closeout.
- Full regression: `NOT RUN` in this bounded closeout because the established full suite includes persistent-environment mutation paths; focused regression and static checks were run without resetting Atlas state.

## Publication boundary

The implementation image was rebuilt from `c850aa947882cf78138bb245f9cd42d11323decb` and the persistent Core was recreated/restarted through its existing user systemd service. No deployment or public exposure was performed. The final governed commit, GitHub parity, and Notion checkpoint are recorded after closeout publication.
