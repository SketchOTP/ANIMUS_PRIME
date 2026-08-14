# ANIMUS PRIME Phase 15 Qualification - Continuation 053

Date: 2026-08-14
Directive: `D-PRIME-PHASE15-V1-PERSISTENT-ATLAS-CORE-UI-053`
Authority: `PRIME-SPEC-V1.0.0`

## Scope and result

This continuation was authorized to establish the genuine persistent private
PRIME Core/Web topology on Atlas. The Core-served Web UI is now running under a
PRIME-owned user-level systemd service and survives a clean stop/start cycle.
The authenticated operator journey could not be completed because the existing
operator password was not present in an approved credential reference. No
password reset, bootstrap, credential discovery, or synthetic session was used.

The repository Node remains an enrolled database record, but Atlas has no
PRIME-owned Node service or approved mTLS credential set. The packaged Node
correctly refuses service mode without mTLS, and the disposable-only insecure
HTTP override was not used. The Node is therefore recorded as a truthful
unavailable dependency for this continuation.

## Baseline

- Published baseline: `2ed5ba3267554a393ca19c4d78eb476c0d89fdc5`.
- Atlas checkout: `/home/sketch/Projects/ANIMUS_PRIME`.
- Local HEAD before changes: `2ed5ba3267554a393ca19c4d78eb476c0d89fdc5`.
- `origin/main` before changes: `2ed5ba3267554a393ca19c4d78eb476c0d89fdc5`.
- Worktree before changes: only pre-existing untracked `.codebase-memory/`,
  `.prime-evidence/`, and `.vscode/`.
- Existing PostgreSQL: container `animus-prime-phase0-postgres-1`, pinned
  pgvector image `e04af45eb526`, healthy, existing persistent database/schema;
  no new database or host port was created.
- Existing Hindsight: container `mimir-hindsight-production`, process
  `hindsight-api`, loopback `127.0.0.1:8888`; `/health` returned HTTP 200 and
  `{"status":"healthy","database":"connected"}`.
- Existing qualification project: `project_d9a1a5b609394282b62fc12c0d04634d`,
  `Qualification Project`, `ACTIVE`, `ONLINE`, `CURRENT`.
- Existing repository binding: node `node-041-atlas-native`, repository
  `repo_1eb92bbce8d44309861368d8690247c6`, `BOUND`, canonical ref
  `refs/heads/main`, canonical ref commit `dc425cc7582a46f86fe7b35b0889343785bf5c25`.
- Existing repository Node record: `node-041-atlas-native`, approved, Linux,
  allowed root `/home/sketch/Projects`, database status `ENROLLED`.

## Persistent runtime topology

| Component | Runtime mechanism | Identity / listener | Persistence | Result |
|---|---|---|---|---|
| PostgreSQL | Existing Docker container | `animus-prime-phase0-postgres-1`, existing private Docker network | Existing PostgreSQL volume/database | `PASSED`, preserved and reused |
| Hindsight | Existing Docker container, host network | `mimir-hindsight-production`, `hindsight-api`, `127.0.0.1:8888` | Existing Hindsight-owned storage | `PASSED`, preserved and reused |
| PRIME Core | PRIME-owned Docker container managed by user systemd | `animus-prime-core`, image `animus-prime-core:continuation-053`, UID `1000:1000`, host network, `127.0.0.1:18000` | Existing Atlas runtime directory `/home/sketch/.local/share/animus-prime-core`; repository mounted read-only at its canonical path | `PASSED`, running and ready |
| PRIME Web UI | Core-served `apps/web/index.html` | No second Web service; served by Core at `http://127.0.0.1:18000/` | Same Core runtime | `PASSED`, real UI returned HTTP 200 |
| Repository Node | Intended native service path inspected; not started | No PRIME-owned process/listener on `18001`; record `node-041-atlas-native` remains `ENROLLED` | No service state directory or approved mTLS reference was present | `BLOCKED`, secure startup material absent |

Service manager: user systemd, `animus-prime-core.service`, enabled and active
with `Linger=yes` for user `sketch`. The Docker container has restart policy
`no`; systemd owns the service lifecycle. No unrelated service or listener was
replaced. Existing unrelated listeners on `5173` and `8080` were untouched.

Startup policy: automatic user-service startup is enabled. Public exposure:
none. Core and Hindsight bind loopback only, no host port is published from the
Core container, no Funnel or public ingress was enabled or changed, and
PostgreSQL was not exposed.

Health: Core `/health/live` returned `{"status":"live","service":"prime-core"}`;
Core `/health/ready` returned `{"status":"ready","schema_version":"0030_rebind_and_workflow_steps.sql"}`.
The Core startup log showed database connection/migration startup completion.

## Runtime repair

Observed user-visible/runtime failure: the first persistent Core start failed
before application import with `PermissionError` for
`src/prime_core/git_provenance.py`. The repository file was mode `0770`, while
the pinned Docker image correctly runs as non-root.

Minimal repair: `Dockerfile.core` now normalizes copied application permissions
with `RUN chmod -R a+rX /app` before the existing `USER nobody` declaration.
The image was rebuilt from the governed checkout and started successfully as
UID `1000:1000` through the PRIME-owned service.

Packaging added: `packaging/core/prime-core.service` and its README describe
the persistent Core-served UI service without embedding credentials. Machine
local environment and runtime directories remain outside Git with restricted
permissions.

## Operator/browser evidence

Browser: real Chromium through the installed `/browse` skill. The browser tool
session used local Windows metadata only because running it from the SSHFS
workspace reproduced the malformed-path failure. A private SSH tunnel forwarded
local `127.0.0.1:28000` to Atlas `127.0.0.1:18000`; the product itself remained
on Atlas.

- Protected entry: `PASSED`; `/v1/core/status` returned HTTP 401 with
  `AUTHENTICATION_REQUIRED`.
- Login: `BLOCKED`; the existing operator record exists, but its password was
  not provided in an approved reference. No bootstrap, recovery reset, guessed
  password, or fabricated session was used.
- Home: `PARTIAL`; the genuine shell loaded and displayed the truthful
  authentication-required state. Protected project data was not presented.
- Needs Attention: `NOT RUN`, authenticated project state unavailable.
- Project selection: `NOT RUN`, authenticated project list unavailable.
- Overview, Progress, Ask, Search, Memory, Knowledge, Evidence, Activity:
  `NOT RUN` as authenticated project surfaces; the real controls are present in
  the served UI shell.
- Invalid route: `PASSED`; `/not-a-real-prime-route` returned HTTP 404.
- Refresh/recovery: `PASSED`; the real UI returned HTTP 200 after Core restart
  and its heading remained `Keep every project understandable.`
- Responsive: `PASSED` for rendered 375x812 shell inspection. Navigation and
  critical controls remained visible and textual.
- Keyboard: `PASSED` for Tab focus; focus reached the branded navigation link.
- Console/network: no unexpected JavaScript errors; the only recorded error
  was the expected unauthenticated 401 request.
- Logout, re-login, destructive confirmation, provider-degraded authenticated
  state, and Node-offline authenticated operation: `NOT RUN` because login was
  blocked.

## Restart qualification

1. `systemctl --user stop animus-prime-core.service`: `PASSED`; service became
   inactive, container became `exited`, and `127.0.0.1:18000` disappeared.
2. `systemctl --user start animus-prime-core.service`: `PASSED`; the same
   `animus-prime-core` container and image returned.
3. Recovery: `PASSED`; `/health/ready` returned ready with schema
   `0030_rebind_and_workflow_steps.sql`, systemd was active/enabled, and the
   Core listener returned on `127.0.0.1:18000`.
4. Duplicate check: `PASSED`; only one PRIME Core container and one Core
   listener were present.
5. Persistence reset check: `PASSED`; no database, project, repository, Node,
   Hindsight bank, or qualification-only state was created or reset.

## DOD-005 and DOD-074

DOD-005: `PARTIAL`. Continuation 052 backend source-retraction propagation is
preserved. The authenticated operator-visible source lifecycle was not run in
this continuation because login was blocked. Documentation/Notion projection
was not fabricated.

DOD-074: `PARTIAL`. Continuation 052's reversible persisted-state/offline-Node
qualification and restoration evidence is preserved. The operator-visible
offline-Node journey was not run because the existing Node service lacks
approved mTLS material and browser authentication was unavailable. The current
database Node record was not changed.

## Degraded or unavailable integrations

- Notion: `UNCONFIGURED` in the served shell; no live Core write capability was
  claimed and the missing MyAssistant credential was not rediscovered.
- AI provider: `DEGRADED-SAFE`; no approved live provider was enabled.
- LOCAL_ONLY: not enabled or fabricated.
- Hindsight Reflect/Mental Models: unavailable/unqualified; base Hindsight
  health is healthy.
- Windows/native Node: not qualified; no Windows Node was created.
- Second device: not run.
- Tailscale: inspected only; no Funnel or public exposure was enabled.

## Validation

- Focused: `PASSED` through the authenticated-free runtime checks; no
  authenticated project qualification was claimed.
- Regression: `PASSED`, `90 passed, 28 skipped in 6.38s`, matching the Continuation
  052 comparison baseline.
- Integration: `NOT RUN` for authenticated persistent-project and live Node
  operations; no destructive reset was used.
- Compile/static: `PASSED`, `compileall`; `git diff --check` passed.
- Governance: `PASSED`, `scripts/validate_governance.py --mode ADOPTED`.
- Product alignment: `PASSED` for audit structure; the expected broader
  `V1_PRODUCT_GOAL_ALIGNMENT` remains `FAIL` by design.
- Burndown: `PASSED`; 81 total, 42 complete, 39 open/burndown, status sums and
  work-class totals consistent.
- Persistent runtime: `PASSED`, Core/Hindsight health, listener ownership,
  clean stop/start, readiness, and no duplicate checks.
- Browser: `PARTIAL`, real shell/protected-route/404/responsive/keyboard/restart
  checks passed; authenticated operator journey is blocked by the existing
  operator credential.
- Deployment: `NOT PERFORMED`.

## Governed status

No requirement or DOD row was promoted by shell visibility or service health.
R-056 remains `IMPLEMENTING`; Phase 15 remains open; V1 was not declared. The
next authorized action is to provide the existing operator credential through a
safe private handoff, then resume authenticated browser qualification without
resetting persistent state.
