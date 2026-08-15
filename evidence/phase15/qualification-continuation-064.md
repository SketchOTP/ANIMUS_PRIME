# ANIMUS PRIME Phase 15 Continuation 064

## Result

`PARTIAL` / `DONE_WITH_CONCERNS` for the bounded explicit operator-workflow scope.

The genuine persistent Atlas product now exposes durable, auditable lifecycle preflight/action workflows, distinct Remove/Archive/Delete controls, protected destructive-action checks, repository onboarding inspection before binding, authority review/adoption controls, and guided Goal draft/approval controls. The existing canonical Qualification Project was used for reversible and refusal qualification only. No canonical delete, purge, remove, archive, completion request, positive Class-B creation, secondary target, deployment, Phase 16 work, or R-056 closure was performed.

## Baseline

- Specification: `PRIME-SPEC-V1.0.0`
- Authoritative checkout: `/home/sketch/Projects/ANIMUS_PRIME`
- Starting governed implementation: `ed7f7ce8b0a0a57da804047becb858d5ce76d873`
- Qualified implementation candidate: `c32586abdf981bf2df1aec3d29bbb85b73512d2b`
- Worktree before implementation: only preserved untracked `.codebase-memory/`, `.prime-evidence/`, and `.vscode/`
- Persistent PostgreSQL: existing `animus-prime-phase0-postgres-1`, reused and not reset
- Persistent Hindsight: existing `mimir-hindsight-production`, reused and not reset
- Repository Node: existing canonical Atlas Node, user unit active before and after qualification
- Existing project: `project_d9a1a5b609394282b62fc12c0d04634d` (`Qualification Project`)

## Persistent runtime topology

| Component | Runtime mechanism | Listener / identity | Persistence | Result |
|---|---|---|---|---|
| PostgreSQL | existing Docker container | existing phase0 PostgreSQL container, healthy | existing persistent database | `PASSED`, reused |
| Hindsight | existing Docker container | `127.0.0.1:8888`, existing Hindsight process | existing persistent Hindsight state | `PASSED`, reused |
| Repository Node | `systemd --user` unit `animus-prime-node.service` | `127.0.0.1:18001`, existing Node identity | existing repository/trust state | `PASSED`, active |
| PRIME Core | `systemd --user` unit `animus-prime-core.service` controlling Docker | `127.0.0.1:18000`, `animus-prime-core:continuation-064` | `/home/sketch/.local/share/animus-prime-core` bind, unchanged | `PASSED`, active |
| PRIME Web UI | Core-served genuine UI from `apps/web/index.html` | `127.0.0.1:18000/` | served by persistent Core | `PASSED`, authenticated browser reached it |

Readiness after the swap and after restart:

```json
{"status":"ready","spec_revision":"PRIME-SPEC-V1.0.0","build_commit":"c32586abdf981bf2df1aec3d29bbb85b73512d2b","image_identity":"animus-prime-core:continuation-064","schema_version":"0036_operator_workflows.sql","service_version":"1.0.0"}
```

The swap preserved host networking, the read-only repository bind, the persistent state bind, and the existing user-service mechanism. The former container remains stopped as the recoverable `animus-prime-core-rollback-064`; no persistent data was deleted. Public exposure was not changed. Tailscale Funnel was not enabled.

## Implementation

- Added migration `0036_operator_workflows.sql` for durable lifecycle preflights with expiry, stale-state protection, and single-use tokens.
- Added explicit lifecycle actions and consequences for PAUSE, RESUME, ENTER_COMPLETION_REVIEW, CANCEL_COMPLETION_REVIEW, REQUEST_COMPLETION, REMOVE, ARCHIVE, DELETE, and PURGE.
- Added exact-target, confirmation, recent-step-up, stale/replay, and audit enforcement for high-risk actions.
- Added repository inspection before binding and explicit bind controls in the onboarding UI.
- Added guided Goal completeness validation, draft review, explicit approval, and `GoalRevision` protection against silent overwrite.
- Added authority review/adoption controls without automatic rewrite.
- Added focused tests for distinct action targets and descriptions plus incomplete/complete Goal handling.

## Browser operator evidence

Browser: approved persistent gstack Chromium state, reaching the private Atlas Core through a narrow SSH forward to the existing loopback listener. No disposable browser profile or project-local browser dependency was used.

- Authentication: `PASSED`; trusted PRIME host challenge was approved on Atlas, then the existing operator session loaded.
- Home / Projects: `PASSED`; authenticated Core state loaded and the existing Qualification Project was selected by its real project identity.
- Overview: `PASSED`; project snapshot loaded with `ACTIVE`, `ONLINE`, and `CURRENT` state before mutation.
- PAUSE: `PASSED`; preflight displayed the exact project, Node, repository path, consequence, and `ACTIVE → PAUSED`; typed `CONFIRM` executed the action and recorded the lifecycle result.
- Restart persistence: `PASSED`; Core was restarted through `systemctl --user`, readiness returned with the candidate commit and schema, and the browser still showed the project `PAUSED`.
- RESUME: `PASSED`; preflight and typed confirmation restored `PAUSED → ACTIVE`.
- Completion review: `PASSED` bounded reversible path; entered `ACTIVE → COMPLETION_REVIEW` and canceled back to `ACTIVE` with an audit result.
- Remove / Archive / Delete distinction: `PASSED` at the UI/preflight boundary; each control displayed a distinct consequence and target. No canonical Remove or Archive execution was performed.
- Delete refusal: `PASSED`; preflight required the exact project identity and reported recent step-up absent. A wrong-target submission returned a refusal requiring exact identity, with no lifecycle mutation.
- Authority: `PASSED`; review returned `VALID`, contract `authority-file-contract-v1`, and “no rewrite requested.” Adopt was not used because no adoption was required.
- Goal: UI exposes draft-save and explicit approval controls; existing approved Goal state was not overwritten. Full positive Goal creation was not manufactured because no legitimate secondary target was available.
- Repository onboarding: UI exposes inspect-without-binding followed by explicit binding; no new project or repository was created for evidence.
- Ask, Search, Memory, Knowledge, Evidence, Activity, and remaining project surfaces: existing authenticated UI remained available; no unrelated workflow was promoted from this bounded cycle.

## Safety and degraded boundaries

- PostgreSQL, Hindsight, Node identity, repository binding, Goal identity, and authority hash were preserved.
- No public listener, Funnel, firewall, security weakening, or unrelated service was changed.
- No raw secret, password, recovery code, database credential, or private key was placed in repository evidence or `.agent` records.
- Notion live write capability remains conditional/unverified except for the project journal/checkpoint update.
- Optional AI/provider capabilities remain truthfully degraded where unavailable.
- Hindsight Reflect/Mental Models, Windows/native, second-device, and external qualification remain outside this cycle.
- DOD-005 remains parked/backend-only; this cycle does not reopen or close it.
- DOD-074 remains preserved from prior qualification; no new claim is made here.

## Validation

- Focused Continuation 064 tests: `PASSED` — 3 passed.
- Full regression: `PASSED` — 107 passed, 28 skipped. The pass count increased by three from the 104/28 baseline due to the new focused workflow tests; skip count did not change.
- Compile/static: `PASSED` — `compileall`.
- Diff whitespace: `PASSED` — `git diff --check`.
- Runtime readiness, schema migration, service identity, listener ownership, persistent bind, and rollback target: `PASSED`.
- Browser authentication, lifecycle preflight/action, restart persistence, reversible completion review, authority review, and delete refusal: `PASSED` for the bounded paths listed above.
- Governance, burndown, alignment, and tracked-secret checks: run at closeout; results are recorded in the final governed publication state.

## Remaining gaps

- Positive Class-B registration/creation/authority/Goal workflows still need a legitimate non-canonical target or approved real operator action; no synthetic target will be created.
- Canonical Remove, Archive, Delete, Purge, and completion-request outcomes remain unqualified by design.
- Full stale/replay/CSRF/step-up negative matrix and backup/privacy reconciliation remain open.
- Provider/external environment gaps, DOD-005, R-056, Phase 15 completion, and V1 declaration remain open.

R-056: `OPEN`.

Phase 15: `PARTIAL`.

V1: not declared.

Deployment: `NOT PERFORMED`.
