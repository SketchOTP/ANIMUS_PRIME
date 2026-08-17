# ANIMUS PRIME — Phase 15 Continuation 084

## Acceptance

`PARTIAL` — the bounded local closure wave repaired the supported regression seam, qualified four additional operator workflows in the authorized Atlas Qualification Lab, and repaired the persistent runtime/UI defects required to exercise them. Full regression is green, but DOD-004, DOD-031, DOD-044, DOD-047, DOD-049, DOD-055, DOD-080, DOD-081/R-056, and the external environment gates remain open.

## Baseline and scope

- Frozen specification: `PRIME-SPEC-V1.0.0`
- Starting governed PRIME commit: `a9b8cc89e10e2714006c2e5a760e96ad196264ef`
- Final implementation/evidence commit: `02d93dead9ad9479a38a3ed16171b12f3594d2b7`
- Execution authority: direct Atlas SSH, `/home/sketch/Projects/ANIMUS_PRIME`
- Existing untracked `.codebase-memory/`, `.prime-evidence/`, and `.vscode/` were preserved.
- No canonical Qualification Project was terminally mutated; all positive creation/provisioning actions used the authorized tracked lab and were marked `V1_QUALIFICATION_FIXTURE`.

## Persistent runtime

| Component | Result |
|---|---|
| PostgreSQL | Existing persistent Atlas PostgreSQL, healthy and reused |
| Hindsight | Existing `mimir-hindsight-production`, `127.0.0.1:8888`, health `healthy`, reused |
| Repository Node | Existing `node-041-atlas-native`, reused; no new Node created |
| PRIME Core/UI | `animus-prime-core:continuation-084-v5`, persistent user-systemd service `animus-prime-core.service` |
| Core listener | `127.0.0.1:8000`, private/local; health `/health/live` and `/health/ready` passed |
| Web interface | Genuine PRIME UI through the Core-served operator console, browser tunnel `http://127.0.0.1:28000` |
| Build provenance | commit `02d93dead9ad9479a38a3ed16171b12f3594d2b7`; image `animus-prime-core:continuation-084-v5`; build `2026-08-17T14:59:08-04:00` |
| Restart proof | MainPID `2972764`, service start `2026-08-17 14:59:09 EDT`; readiness returned the exact build commit/image/schema |
| Public exposure | Not performed; no Funnel/Tailscale/public listener changes |

The parent `/home/sketch/Projects` mount remains read-only for Core. The authorized lab repository `/home/sketch/Projects/ANIMUS_PRIME_V1_QUALIFICATION_GOAL_084` received a narrowly scoped nested read-write bind so the existing Core authority/creation workflow could write only inside that lab target. Unrelated Atlas repositories remained outside that write scope.

## Phase A — regression/testability repair

Observed: five AI contract tests constructed `AIExecutionService(object(), ...)` while production execution now correctly invokes PostgreSQL-backed Usage policy enforcement; one historical Continuation-059 assertion still required the obsolete `UNAVAILABLE` Usage state.

Minimal repair:

- `AIExecutionService` now accepts an optional typed Usage-policy dependency for tests while preserving the production `UsagePolicyService` default.
- Focused AI tests prove injected policy consultation, blocking, and production default construction.
- The stale Continuation-059 expectation now asserts the configured Usage snapshot.

Focused Phase A result: `16 passed`.

## Runtime/UI repairs exposed by the real operator path

1. Authority bootstrap resolved `authority-template/v1` relative to `/app`, where the persistent container did not contain the repository template. The smallest repair resolves an approved configured/Atlas-mounted template root and fails closed if `AGENTS.md` is absent.
2. The persistent Core parent repository mount is read-only. The qualification lab used a scoped nested writable bind; no broad parent write access was granted.
3. The Web UI exposed the existing backend terminal-completion operation through `REQUEST_COMPLETION`.
4. The Web UI exposed the existing authorized repository-creation endpoint for explicit `new` onboarding mode and changed the action label to `Create and bind repository`.
5. Narrow viewport CSS now prevents intrinsic grid/name overflow with `min-width: 0` and wrapping for headings.

## Browser/operator evidence

Browser: gstack `/browse`, Chromium-compatible persistent browser session, private Atlas tunnel `http://127.0.0.1:28000`.

### DOD-024 — lifecycle completion

- Existing `V1_QUALIFICATION_FIXTURE_083` was used.
- PAUSE/RESUME and COMPLETION_REVIEW were exercised through the real UI.
- A first completion attempt from `ACTIVE` was refused safely as `invalid lifecycle transition ACTIVE->COMPLETED`.
- After entering COMPLETION_REVIEW, operator-confirmed `REQUEST_COMPLETION` produced `COMPLETION_REVIEW → COMPLETED`.
- Core restart returned healthy; browser reload showed the same project `COMPLETED · ONLINE`.
- Post-completion PAUSE was refused safely as `invalid lifecycle transition COMPLETED->PAUSED`, with no mutation.
- DOD-024 is promoted to `USER_USABLE_VERIFIED`.

### DOD-054 — positive registration and duplicate refusal

- Fresh authorized lab project `V1_QUALIFICATION_GOAL_084` used existing enrolled Node `node-041-atlas-native`.
- Browser inspection returned `READY_TO_BIND`; explicit bind created repository `repo_c3a5bb17b9d04ee2b0ad4e7a4dcd86a4` at the fixture path.
- Repeating registration against the already-bound project returned HTTP 400 `project already has a primary repository binding`; no second binding was created.
- DOD-054 is promoted to `USER_USABLE_VERIFIED`.

### DOD-057 — fresh authority provisioning

- Fresh creation target `V1_QUALIFICATION_CREATE_084B` was created in the authorized lab.
- Browser `Bootstrap authority package` completed with `authority-file-contract-v1`, validation `VALID`, and a durable source hash.
- The target contains the complete authority package including `AGENTS.md` and `.agent/` contract files.
- Restart recovery preserved the authority files and Core returned healthy.
- DOD-057 is promoted to `USER_USABLE_VERIFIED`.

### DOD-058 — guided Goal review/approval

- The real Goal workflow rejected an incomplete proposal before approval.
- A complete Goal proposal was saved as a draft, reviewed, and explicitly approved.
- An explicit new-revision intent created GoalRevision 2; approval returned `APPROVED` with content hash `ddac86e34d2609a93c7c292c360de52815432a9136e6422b884eb1db41baf047`.
- `/home/sketch/Projects/ANIMUS_PRIME_V1_QUALIFICATION_GOAL_084/.agent/PROJECT_GOAL.md` exists with the same SHA-256.
- After persistent Core restart, the file and approved Goal state remained durable.
- DOD-058 is promoted to `USER_USABLE_VERIFIED` for the bounded guided Goal contract.

### DOD-055 — creation remains partial

- The repaired UI created and bound fresh repository `V1_QUALIFICATION_CREATE_084B` under the authorized lab parent.
- Repository path: `/home/sketch/Projects/ANIMUS_PRIME_V1_QUALIFICATION_GOAL_084/creation-lab/ANIMUS_PRIME_V1_QUALIFICATION_CREATE_084B`.
- Workflow: `workflow_8b146095e3474ff6af511bb481c62aee`.
- Git working-tree identity and authority bootstrap were confirmed after restart.
- Interrupted creation/recovery and the full negative matrix were not completed in this run; DOD-055 remains `PARTIAL`.

## Browser polish and accessibility checks

- 375×812 viewport: PASSED after the CSS repair; `document.documentElement.scrollWidth == 375`, no horizontal overflow.
- Keyboard Tab traversal: PASSED; focus reached visible input/button controls and computed focus outline was `solid`.
- Destructive lifecycle confirmation/refusal: PASSED from prior bounded evidence and rechecked for terminal completion refusal.
- Browser console: NOT a clean historical log; the shared session contains earlier deliberate 401/400/403/404/503 responses from unauthenticated/degraded/refusal probes and unrelated browser activity. No new JavaScript exception was used as a pass claim.
- DOD-080 remains `PARTIAL` pending complete frozen visual/operator polish acceptance.

## Validation

- Focused 084/authority tests: `PASSED` — `3 passed`; Continuation-084 static guards: `PASSED`.
- Full supported regression: `PASSED` — `122 passed / 29 skipped / 0 failed`.
- Core readiness: `PASSED` — exact v5 build commit/image/schema returned.
- PostgreSQL/Hindsight health: `PASSED` — existing persistent services healthy.
- Governance/diff/secret checks: pending final closeout run after this evidence/governance update.
- GitHub parity: pending final publication.

## DOD/R outcome

- Newly promoted: DOD-024, DOD-054, DOD-057, DOD-058 → `USER_USABLE_VERIFIED`.
- Preserved partial: DOD-004, DOD-031, DOD-044, DOD-047, DOD-049, DOD-055, DOD-080.
- External/legitimate-target gates preserved: DOD-013, DOD-016, DOD-031, DOD-044, DOD-047, DOD-049, DOD-053, DOD-079.
- DOD-005 remains parked and previously `PRODUCT_VERIFIED`.
- DOD-081/R-056 remain open and gated; Phase 15 and V1 are not declared complete.
- Deployment/public exposure: `NOT PERFORMED`.

