# ANIMUS PRIME — Phase 15 Qualification Continuation 059

Status: **PARTIAL — safe authenticated local product wave**
Date: 2026-08-15
Execution boundary: direct SSH/native Atlas only; no Z: path execution and no disposable environment.

## Baseline

- Frozen specification: PRIME-SPEC-V1.0.0
- Authoritative checkout: /home/sketch/Projects/ANIMUS_PRIME
- Starting local HEAD: 8829f248ab8c87f03dd94a7a29c06fef267c8855
- Starting origin/main: 8829f248ab8c87f03dd94a7a29c06fef267c8855
- Starting worktree: only preserved untracked .codebase-memory/, .prime-evidence/, and .vscode/; no unrelated tracked edits were overwritten.
- Continuation 058 closeout metadata was repaired: its qualified implementation is 8c881256b6a0164cfef9ae411eb404107ac5c3c0, and its governed/public baseline remains 8829f248ab8c87f03dd94a7a29c06fef267c8855.
- Qualified implementation commit for this continuation: 98b94732106955c246fca025f73116f56b58b5cf (feat: expose safe product qualification surfaces).

## Runtime and topology

| Component | Runtime identity | Persistence/target | Result |
|---|---|---|---|
| PostgreSQL | Existing PRIME PostgreSQL container | Existing persistent PRIME database | PASSED; reused, not recreated |
| Hindsight | Existing approved Hindsight service | Existing configured target | PASSED; preserved, no replacement bank |
| Repository Node | node-041-atlas-native, user-systemd animus-prime-node.service | /home/sketch/Projects/ANIMUS_PRIME; trust material outside Git | PASSED; active/enrolled |
| PRIME Core | animus-prime-core:continuation-059-ui, user-systemd animus-prime-core.service | Existing /home/sketch/.local/share/animus-prime-core state mount | PASSED; active and restart-recovered |
| PRIME Web UI | Core-served apps/web/index.html | Same persistent Core | PASSED; genuine UI, no second web server |

- Core listener: 127.0.0.1:18000 on Atlas.
- Node listener: 127.0.0.1:18001 on Atlas.
- Private browser interface: http://127.0.0.1:28000/ through the existing private tunnel.
- Health: /health/live and /health/ready passed; schema 0034_local_identity_authentication.sql.
- Startup policy: enabled user-systemd service.
- Restart recovery: passed against the same project, binding, Node, database, state mount, and service identity.
- The previous persistent Core containers/images were retained inactive as rollback artifacts; no unrelated service was replaced.
- Public exposure: NOT PERFORMED. Funnel/Tailscale configuration was not changed.

## Product repairs

1. Added session-protected GET /v1/projects/{project_id}/usage. It reads real usage_records and returns KNOWN records, explicit UNAVAILABLE limits, and UNAVAILABLE provider cost where no approved provider execution cost exists.
2. Extended reliability diagnostics with non-secret verified-backup status, latest record identity, encryption version, and a truthful restore boundary.
3. Added a real Project Settings metadata form for name, description, and image/avatar URL. It uses the existing CSRF/session-protected PATCH path and does not expose secrets.
4. Repaired narrow navigation CSS so the mobile navigation does not retain desktop min-width overflow.
5. Added focused regression coverage in tests/phase15/test_continuation059_safe_wave.py.

The persistent image had to be rebuilt because the existing service imported the previous image's /app tree; the repository mount is read-only and does not make image-baked Python/UI code live. The rebuild and container swap preserved the same writable state mount and user-systemd service.

## Browser/operator evidence

Browser: Chromium through the existing private Atlas tunnel, authenticated with the Continuation 058 trusted-host local identity path.

- Authentication/protected state: PASSED; ordinary PRIME session/CSRF state loaded.
- Home / project registry: PASSED; the canonical Qualification Project was selected.
- Canonical project: project_d9a1a5b609394282b62fc12c0d04634d.
- Project binding: /home/sketch/Projects/ANIMUS_PRIME on node-041-atlas-native.
- Overview, Goal, Progress, Repository, Authority, Memory, Brain, Time Lens, Knowledge, Evidence, Activity, AI Connections, and Settings: inspected through the genuine Core-served UI; truthful incomplete/degraded states were retained where the exact clause is not complete.
- Usage: PASSED for the bounded data-backed surface. The UI showed project-scoped historical ASK_PRIME records from the unconfigured provider, limits UNAVAILABLE, and estimated cost UNAVAILABLE; no fabricated cost was shown.
- Backup: PASSED for the bounded diagnostic surface. The UI showed an existing verified continuity record, 108 records, AES-256-GCM/PBKDF2-HMAC-SHA256 encryption, and a protected restore boundary. Destructive restore was not run.
- Metadata continuity: PASSED. Through the real Project Settings form, the operator changed name to "Qualification Project 059 Probe", description to "Continuation 059 reversible metadata probe", and image URL to https://example.invalid/continuation-059-avatar.png. The same project ID, Node, and repository path remained bound. After Core restart and browser reload all values persisted. The exact original state was then restored through the form: name "Qualification Project", blank description, null image URL.
- Progress/Alignment: PARTIAL. Current progress/history and challenge controls were data-backed and visible; no false correction/challenge mutation was submitted. Goal Alignment, milestones, and complete correction acceptance remain open.
- Integrity: PARTIAL. A healthy data-backed structural snapshot was visible; no authority rewrite or synthetic failure was introduced. Negative structural-failure qualification remains open.
- Registration: PARTIAL/preserved. Current-path repository inspection returned REVIEW_AUTHORITY; outside-root and nonexistent paths were rejected; registration with confirm=false was rejected. No binding mutation was performed.
- Notifications: UI_SHELL_ONLY. The Settings surface remains descriptive and has no qualified notification lifecycle.
- Responsive/polish: PARTIAL with bounded advancement. At 375x812, document scrollWidth was 375 with no horizontal overflow. Keyboard Tab reached a control with :focus-visible, a 3px focus outline, and a 2px offset. Full frozen polish acceptance remains open.
- Core restart/reload: PASSED; the same project and metadata continuity returned after restart.
- Provider-degraded state: PASSED; unconfigured provider/limits/cost are explicit, not generic success.
- Node-offline DOD-074 boundary: preserved from prior qualification; persisted project/history/Progress remain usable, Node-required operations fail closed, and the original enrolled state was restored.

## Governed requirement outcomes

- DOD-005: BACKEND_ONLY, unchanged and PARKED. No safe existing non-authority source with a supported restoration-bounded retraction path was available; no mutation was attempted.
- DOD-026: PARTIAL.
- DOD-027: PARTIAL.
- DOD-047: PARTIAL.
- DOD-048: UI_SHELL_ONLY.
- DOD-049: PARTIAL.
- DOD-054: IMPLEMENTED_NOT_PRODUCT_QUALIFIED.
- DOD-056: USER_USABLE_VERIFIED for the exercised single-project metadata continuity path.
- DOD-080: PARTIAL; responsive overflow and keyboard focus were advanced, but the complete frozen polish clause is not closed.
- DOD-074: preserved qualified operator boundary; no new Node or substitute environment used.
- R-056: OPEN and gated. This continuation did not attempt aggregate release closure.
- Local actionable queue after reconciliation: 5 LOCAL_CODE, 14 LOCAL_BROWSER_QUALIFICATION, 0 LOCAL_NATIVE_QUALIFICATION, 0 EVIDENCE_RECONCILIATION, and 15 EXTERNAL_ENVIRONMENT items.
- Parked work remains parked: DOD-005 direct mutation, DOD-004 generic expansion, DOD-039 relocation, DOD-050 upgrade expansion, and DOD-053 second-machine work.

## Validation

- Focused safe-wave/authentication/recovery checks: PASSED — 6 passed.
- Full repository regression: PASSED — 98 passed, 28 skipped in 6.94s using the repository .venv. The increase from 96 to 98 is the two-test Continuation 059 focused regression file; skip count is unchanged.
- Compile/static checks: PASSED — Python compile, prime-local-auth shell syntax, and git diff --check.
- Governance: PASSED — scripts/validate_governance.py --mode ADOPTED.
- Burndown: PASSED — totals, IDs, status counts, fields, and work-class totals reconcile; 14 local browser items remain.
- Product alignment structural audit: PASSED; V1_PRODUCT_GOAL_ALIGNMENT remains FAIL because the frozen release gate is not complete.
- Phase 15 aggregate qualifier: BLOCKED/FAIL by the established environment boundary. Running through the repository .venv reported missing PRIME_PHASE1_DB_URL/PRIME_DATABASE_URL for the phase migration qualification; no substitute database was created.
- Persistent runtime: PASSED — Core/Node active, private listeners healthy, same persistent state and project after restart.
- Browser: PASSED for the bounded authenticated safe wave; exact remaining clauses are recorded above.
- Secret check: PASSED — no raw credentials or private key material were added to Git, evidence, .agent, Notion, or browser-visible diagnostics.
- Deployment/public exposure: NOT PERFORMED.

## Publication identity

The final governed SHA and origin/main parity were verified after publication and recorded in the Continuation 059 Notion checkpoint and final handoff. The qualified implementation SHA is 98b94732106955c246fca025f73116f56b58b5cf; no intermediate implementation SHA is treated as the final governed publication.

Phase 15 remains PARTIAL. V1 is not declared. Phase 16 was not created. Deployment was not performed.
