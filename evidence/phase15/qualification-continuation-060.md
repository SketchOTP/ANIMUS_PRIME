# ANIMUS PRIME — Phase 15 Qualification Continuation 060

Status: PARTIAL
Date: 2026-08-15

## Baseline

- Frozen specification: PRIME-SPEC-V1.0.0
- Authoritative checkout: /home/sketch/Projects/ANIMUS_PRIME
- Starting governed HEAD and origin/main: ae1acc574e4060c98437b26a916ba539a1c4e444
- Starting worktree: only pre-existing untracked .codebase-memory/, .prime-evidence/, and .vscode/; preserved
- Qualified implementation commit: 0324b380fc5fac54fa037695cfe09146ba850baa
- Final publication and parity are recorded by the closing Git checks.
- Deployment, public exposure, Funnel change, Phase 16 creation, and R-056 closure: NOT PERFORMED.

## Persistent Atlas topology

- PostgreSQL: EXISTING persistent PRIME database, reused; no substitute database.
- Hindsight: EXISTING persistent service, reused.
- Repository Node: canonical node-041-atlas-native, existing identity preserved.
- PRIME Core: PRIME-owned Docker container under animus-prime-core.service, image animus-prime-core:continuation-060-provenance2.
- PRIME Web UI: genuine Core-served operator UI.
- Runtime: user systemd supervising PRIME-owned Core and Node; Core uses host networking.
- Core listener: 127.0.0.1:18000.
- State: existing writable /home/sketch/.local/share/animus-prime-core plus existing PostgreSQL/Hindsight targets.
- Startup/restart recovery: PASSED; no duplicate Core or ephemeral database.
- Public exposure: NOT PERFORMED; unrelated Funnel/Tailscale state untouched.

## Runtime provenance

The existing PRIME Core image was rebuilt from 0324b380fc5fac54fa037695cfe09146ba850baa and swapped through the existing PRIME-owned service path while preserving network, user, command, workdir, mounts, database reference, Hindsight reference, and Node topology.

The final /health/ready response reported:
status ready; spec_revision PRIME-SPEC-V1.0.0; build_commit 0324b380fc5fac54fa037695cfe09146ba850baa; build_timestamp 2026-08-15T00:00:00Z; image_identity animus-prime-core:continuation-060-provenance2; schema_version 0034_local_identity_authentication.sql; service_version 1.0.0.

Protected system/build and operator-state metadata rendered in the genuine UI. An intentional wrong-commit probe produced a truthful mismatch. Focused tests prove missing build configuration reports UNKNOWN rather than reading checkout Git state.

## Operator/browser evidence

- Real persistent Chromium through the approved browser QA path.
- Protected login, existing Qualification Project selection, Overview, Home/System Health: PASSED.
- System Health showed Core, schema, qualified commit, and image identity.
- Progress, Ask, Search, Memory, Knowledge, Evidence, Activity, Backup, and Integrity surfaces rendered existing data and truthful provider/source states.
- Goal showed approved items; Alignment and milestone projection remained UNKNOWN/unavailable.
- Notifications remained a settings shell only; no backend/lifecycle was invented.
- Backup showed existing verified continuity, encryption metadata, and restore-preflight; no export or destructive restore executed.
- Responsive widths 375x812, 768x1024, and 1440x900: PASSED with no horizontal overflow after containing long diagnostics.
- Keyboard focus: PASSED. Browser console after reload: PASSED with no errors.
- Complete ARIA, contrast, touch, and full polish qualification remains open.

## Requirement results

- DOD-005: BACKEND_ONLY / PARKED. No safe existing non-authority source with reversible retraction/restoration was available; no persistent mutation or synthetic source used.
- DOD-026: PARTIAL. Goal, approved items, Progress and correction visible; Alignment/milestone projection UNKNOWN.
- DOD-027: PARTIAL. Healthy data-backed Integrity and truthful Notion-disconnected state visible; structural-failure mutation not performed.
- DOD-047: PARTIAL. Usage records and truthful unavailable limits/cost visible; no approved provider/profile for provider-backed qualification.
- DOD-048: UI_SHELL_ONLY. Notification lifecycle not implemented or qualified.
- DOD-049: PARTIAL. Continuity, encryption metadata, and restore preflight visible; export/restore controls not added/executed.
- DOD-054: IMPLEMENTED_NOT_PRODUCT_QUALIFIED. Registration code exists; full real-browser negative matrix not executed.
- DOD-080: PARTIAL advanced. Runtime identity, overflow containment, responsive widths, visible focus, and no-console-error behavior passed; full polish remains open.
- DOD-056: PRESERVED USER_USABLE_VERIFIED for the prior metadata continuity path.
- No new USER_USABLE_VERIFIED or PRODUCT_VERIFIED promotion is claimed.

## Aggregate qualifier boundary

Native Atlas and the user-systemd unit do not expose PRIME_PHASE1_DB_URL or PRIME_DATABASE_URL. The running Core container has a secure database reference, but the established aggregate qualifier requires one of those variables natively and performs migrations/fixtures that could mutate persistent PRIME state. It was not run. No substitute database, project, repository, Node, worktree, or browser profile was created.

## Validation

- Focused provenance/web-shell tests: PASSED (3 passed).
- Full regression: PASSED (100 passed, 28 skipped). The 059 floor was 98 passed/28 skipped; two new provenance tests explain the increase.
- Compile/static, runtime health/restart, browser bounded checks, governance, burndown, and secret checks: PASSED.
- Burndown: audit_total 81, complete 47, burndown 34, LOCAL_CODE 5, LOCAL_BROWSER_QUALIFICATION 14, EXTERNAL_ENVIRONMENT 15.
- Product alignment audit: PASSED structurally; V1_PRODUCT_GOAL_ALIGNMENT remains FAIL because the frozen completion gate is not satisfied.
- Aggregate qualifier: BLOCKED / NOT RUN at the persistent database credential/environment boundary.
- Git local/origin/GitHub parity: verified after publication.

## Conclusion

- R-056: OPEN / GATED.
- Phase 15: PARTIAL.
- V1: NOT DECLARED.
- Deployment: NOT PERFORMED.
- Next action: remaining safe local queue only; DOD-005 parked, high-risk state-changing qualification outside scope, external blockers truthful, and R-056 gated.
