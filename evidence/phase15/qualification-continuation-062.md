# ANIMUS PRIME Phase 15 Qualification Continuation 062

**Result: PARTIAL**

This continuation restored the approved existing gstack browser harness and qualified the existing Continuation 061 persistent Atlas product through the genuine authenticated browser. No PRIME product dependency, Docker image, database, project, repository, Node, browser profile, or public network boundary was replaced or created.

## Baseline

- Frozen specification: `PRIME-SPEC-V1.0.0`
- Starting governed HEAD: `93b4cbb799415659d9a6235e0ac7e77f29ba8027`
- Product implementation at start: `6dd5d805852ab7573ec95d3f4a4f6dfe3a3b3708`
- Starting worktree: only preserved untracked `.codebase-memory/`, `.prime-evidence/`, and `.vscode/`
- Runtime image: `animus-prime-core:continuation-061-local-product3`
- Runtime schema: `0035_notifications_lifecycle.sql`
- Existing persistent PostgreSQL: `animus-prime-phase0-postgres-1`
- Existing persistent Hindsight: `mimir-hindsight-production`, private Atlas loopback `127.0.0.1:8888`
- Existing canonical Node: `node-041-atlas-native`, user service `animus-prime-node.service`
- Existing PRIME Core: user service `animus-prime-core.service`
- Browser route: existing SSH forwarding `127.0.0.1:28000 -> Atlas 127.0.0.1:18000`; the unrelated Windows listener on `127.0.0.1:18000` was not stopped or changed

## Runtime provenance

`GET /health/ready` through the verified Atlas forwarding route returned:

```text
status: ready
spec_revision: PRIME-SPEC-V1.0.0
build_commit: 6dd5d805852ab7573ec95d3f4a4f6dfe3a3b3708
image_identity: animus-prime-core:continuation-061-local-product3
schema_version: 0035_notifications_lifecycle.sql
service_version: 1.0.0
```

Core and Node user services were active. Core and Node listeners remained private on Atlas loopback `127.0.0.1:18000` and `127.0.0.1:18001`. Public exposure, Funnel changes, deployment, and Phase 16 were not performed.

## Browser harness

- gstack root: `C:\Users\sketc\.agents\skills\gstack`
- installation type: existing local gstack checkout
- gstack version: `0.12.9.0`
- gstack checkout HEAD: `5319b8a13bce04a60328323397d51360e0538b7b`
- Node: `v24.13.1`
- Bun: `1.3.10`
- package manager: Bun
- Playwright declaration: `^1.58.2`
- lockfile Playwright: `1.58.2`
- `node_modules/playwright`: present at the gstack root
- Node resolution: resolved from the gstack root `node_modules/playwright/index.mjs`
- bundled `server-node.mjs`: present
- browse command: present as the existing Windows wrapper and compiled executable
- browser cache: existing cache present
- state/profile: existing gstack `.gstack/browse.json` state preserved; no profile deletion or second profile created
- repair performed: no dependency installation or version change was needed; the supported local gstack wrapper was launched from its own writable checkout/state rather than the PRIME SSHFS path
- prior SSHFS route: rejected because it attempted to write `.gstack` on the read-only UNC representation and returned `EPERM`
- harness smoke: **PASSED** — server start/resume, persistent Chromium, snapshot, goto, viewport, keyboard, screenshot, reload, same PID/state, and no dependency error
- unauthenticated smoke `401`: expected protected-entry response, not a harness failure

## Operator journey

Browser: persistent Chromium through gstack, authenticated against the Atlas Core at `http://127.0.0.1:28000/`, using the existing trusted-host local identity flow. The only selected project was the existing `Qualification Project`, ID `project_d9a1a5b609394282b62fc12c0d04634d`.

- Authentication: **PASSED** — short-lived SIGN_IN challenge approved by the existing Atlas helper; no password rotation and no credential value recorded
- Home: **PASSED** — authenticated registry loaded; 722 existing project records were returned
- Needs Attention: **PASSED** — no unresolved conditions for the selected project
- Project selection: **PASSED** — existing Qualification Project remained `ACTIVE · ONLINE · CURRENT`
- Overview: **PASSED** — same project identity and repository binding remained visible
- Goal: **PASSED** — approved GoalRevision 1 and content hash rendered
- Progress: **PASSED** — data-backed `32.2987654320988%`, confidence `0.88`, freshness `STALE`, history and GoalItems rendered
- Goal Alignment/Milestones: **PARTIAL** — per-item Alignment `UNKNOWN` was rendered with stable milestone IDs and no fabricated evidence; truthful correction remained unsubmitted
- Ask: **PASSED / truthful degraded** — safe `UNKNOWN` because model execution/evidence did not support a safe answer
- Search: **PASSED** — 8 project-scoped results for `Qualification Project`
- Memory: **PASSED / DEGRADED** — project-scoped memory record and provenance rendered
- Knowledge: **PASSED / DISCONNECTED** — no live Notion page was claimed
- Evidence: **PASSED** — current evidence count rendered as zero without stale success
- Activity: **PASSED** — source-backed Authority/Memory events rendered with source references
- Repository: **PASSED** when Node online — canonical path and revision rendered; tree load worked
- Authority: **PASSED** — `.agent` validation `VALID`, authority hash and precedence rendered
- Project Brain: **PASSED** — `EXACT`, derived-only, source revision and accessible graph metadata rendered
- Time Lens: **PASSED** — `CURRENT` state rendered; no unsupported historical claim made
- Backup: **PARTIAL** — verified continuity metadata, 108 records, encryption metadata, and protected restore warning rendered; preflight without approved inputs refused with HTTP 422 and no mutation; no export or destructive restore was run
- Notifications: **PASSED** — healthy zero-open state rendered after recovery; routine events did not create notifications
- Settings: **PASSED** — authentication, Notion, provider, Hindsight, remote access, backup, notifications, upgrade, and diagnostics sections rendered
- logout/re-login: **PASSED** — logout returned to protected entry; a fresh trusted-host challenge restored authenticated state and the same Qualification Project was selected again
- browser console: **PASSED** after clearing stale unauthenticated/challenge polling messages and reloading the authenticated Atlas route; no console errors remained
- responsive widths: **PASSED** at `375x812`, `768x1024`, and `1440x900`; `scrollWidth == innerWidth` at all three widths
- keyboard: **PASSED** — Tab moved focus to a visible interactive control at the narrow viewport

## DOD-048 Notifications

**PRODUCT_VERIFIED for the frozen high-signal/no-routine-noise clause.** The healthy selected project initially showed zero open material notifications. During the legitimate reversible canonical Node outage, exactly one deduplicated notification appeared:

- category: `NODE_DEGRADED`
- severity: `HIGH`
- message: bound repository Node is offline
- source: the existing Qualification Project

The notification did not multiply during the outage. After the same Node was restored, the notification resolved and the healthy zero-open state returned. No synthetic notification row was inserted.

## DOD-027 Integrity

**PRODUCT_VERIFIED for the directly exercised canonical-Node outage boundary.** Before the outage, the project ID, Node identity, repository path, and hashes of `AGENTS.md`, `.agent/CURRENT.md`, `.agent/DIRECTIVES.md`, `.agent/OUTCOMES.md`, `.agent/LEARNINGS.md`, and `.agent/RECORD.md` were captured. During the outage:

- Integrity rendered `node: OFFLINE` while retaining `authority: VALID`
- Node-required repository tree loading failed closed with `ConnectionRefusedError`
- no `.agent` rewrite occurred
- all captured authority hashes were unchanged after recovery
- the same Node service was restored and the project returned to `ONLINE` / Integrity `NORMAL`

The broader aggregate R-056 gate remains open.

## DOD-049 Backup

**PARTIAL.** The browser exposed verified backup freshness, record count, AES-256-GCM/PBKDF2-HMAC-SHA256 metadata, an approved-destination field, and a clear destructive-restore step-up warning. The preflight control refused incomplete input with HTTP 422 and did not mutate state. No approved destination/passphrase was available for a non-destructive export, and destructive restore was not run.

## DOD-026 Goal Alignment / Milestones

**PARTIAL.** GoalItems rendered, each had a stable projected milestone identity, and Alignment rendered truthfully as `UNKNOWN` without fabricated evidence. The existing append-only correction history was visible. No knowingly false correction was submitted, so the complete correction/challenge clause remains open.

## DOD-054 Registration negatives

**IMPLEMENTED_NOT_PRODUCT_QUALIFIED.** The existing project and canonical Node remained unchanged. The full negative matrix was not forced through the browser because the current UI registration form is only activated by creating/onboarding a project; using that path would require creating a project or mutating the canonical binding, both outside this safe continuation. Duplicate binding, outside-root, traversal, nonexistent path, natural non-Git, `confirm=false`, and Node-offline registration clauses remain open.

## DOD-080 Polish

**PARTIAL.** No-overflow, keyboard focus, and clean-console checks passed at the required widths. The full visual/operator polish acceptance remains open.

## Runtime recovery

- Core restart recovery: **PRESERVED PASSED** from Continuation 061; build/image/schema provenance remained exact in 062
- Node outage restoration: **PASSED** — the existing Node service was restored in the guaranteed cleanup path
- authentication continuity: **PASSED** — logout and trusted-host re-login succeeded
- persistent project continuity: **PASSED** — no project, repository binding, authority, or Node identity changed

## Validation

- focused product/authentication tests: **PASSED** — 6 passed
- full regression: **PASSED** — 104 passed, 28 skipped; the initial post-promotion run exposed and then corrected a burndown/count mismatch, not a product regression
- compile/static: **PASSED** — `compileall -q apps src tests`
- governance: **PASSED** — adopted governance validator
- burndown: **PASSED** — audit total 81, burndown 32, complete plus burndown 81; status counts and IDs match
- alignment audit: **PASSED** — structural audit PASS; V1 product gate remains FAIL as expected
- diff/secret: **PASSED** — `git diff --check` and tracked-secret validation

## Governed result

- Newly PRODUCT_VERIFIED: DOD-027 canonical-Node Integrity/no-authority-rewrite boundary; DOD-048 high-signal notification lifecycle
- Preserved PRODUCT_VERIFIED: all prior governed product rows
- Still PARTIAL: DOD-026, DOD-049, DOD-080, provider-backed DOD-047, and other previously open rows
- Still IMPLEMENTED_NOT_PRODUCT_QUALIFIED: DOD-054
- DOD-005: `BACKEND_ONLY / PARKED`
- R-056: `OPEN / GATED`
- Phase 15: `PARTIAL`
- V1: `NOT DECLARED`
- Deployment: `NOT PERFORMED`
