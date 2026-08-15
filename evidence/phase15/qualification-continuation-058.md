# ANIMUS PRIME — Phase 15 Qualification Continuation 058

## Result

**PARTIAL — trusted-host local identity authentication and persistent operator continuity qualified; Phase 15 and R-056 remain open.**

This continuation was executed directly on Atlas over SSH at `/home/sketch/Projects/ANIMUS_PRIME`. No `Z:`/SSHFS execution, disposable environment, replacement database, replacement Hindsight bank, duplicate Node, synthetic project, public ingress, credential rotation, deployment, or Phase 16 activity was used.

## Baseline and provenance

- Frozen specification: `PRIME-SPEC-V1.0.0`.
- Starting governed/public baseline: `9a2b54f3dab98eae49b3dd55b86a42674c49fac3`.
- Starting local HEAD: `9a2b54f3dab98eae49b3dd55b86a42674c49fac3`.
- Starting `origin/main`: `9a2b54f3dab98eae49b3dd55b86a42674c49fac3`.
- Qualified implementation commit: `8c881256b6a0164cfef9ae411eb404107ac5c3c0` (`feat: add trusted-host local identity authentication`).
- Final governed HEAD and `origin/main`: recorded after publication below.
- Initial worktree state contained only the preserved untracked `.codebase-memory/`, `.prime-evidence/`, and `.vscode/` artifacts; they were not staged.

## Bounded prior-art review

- [RFC 8628](https://www.rfc-editor.org/info/rfc8628/) informed the use of a short-lived user approval code and separate verification interaction. PRIME does not put a bearer approval token in the browser URL.
- [RFC 8252](https://www.rfc-editor.org/info/rfc8252/) informed the narrow loopback transport boundary. Loopback is not treated as identity proof; PRIME additionally requires a separate host-held secret.
- [WebAuthn Level 3](https://www.w3.org/TR/webauthn-3/) was reviewed as the stronger platform-authenticator option and rejected for this bounded Atlas-only path because it would expand scope beyond the existing approved secret architecture. It remains a possible future option, not a requirement of this continuation.

Repository code navigation followed the project contract as far as the available tool surface allowed. The required jCodemunch MCP tools were not available in this session, so targeted Atlas text inspection was used for configuration/non-code review and only specific implementation files were edited.

## Persistent Atlas topology

| Component | Runtime mechanism | Identity/listener | Persistence/startup | Result |
|---|---|---|---|---|
| PostgreSQL | Existing persistent service/container | Existing PRIME database target; identity preserved and secrets omitted | Existing persistent storage | PASS — reused, not replaced |
| Hindsight | Existing persistent service/container | Existing approved Hindsight target; credentials omitted | Existing persistent storage | PASS — reused, not replaced |
| Repository Node | User systemd service | `node-041-atlas-native`, `127.0.0.1:18001` | Enabled, active, trust material outside Git | PASS — active/enrolled |
| PRIME Core | PRIME-owned Docker container under user systemd | `animus-prime-core`, image `animus-prime-core:continuation-058`, host network, `127.0.0.1:18000`, user `1000:1000`, workdir `/app` | Existing `/home/sketch/.local/share/animus-prime-core`; enabled and active | PASS — live/ready |
| PRIME Web UI | Core-served genuine web application | Reached through the private local browser tunnel to the real Core UI | Served by the persistent Core runtime | PASS — real UI, not a diagnostic substitute |

Core health returned `{"status":"live","service":"prime-core"}` and readiness returned schema `0034_local_identity_authentication.sql`. Systemd reported Core and Node both `enabled` and `active`. Listeners remained private on `127.0.0.1`; public exposure and unrelated Funnel configuration were untouched.

## Trusted-host local identity implementation

Migration `0034_local_identity_authentication.sql` adds a nullable digest field for the separate local identity and a durable challenge table with purpose, browser nonce digest, approval-code digest, expiry, approval, and consumption state. No raw secret is stored in PostgreSQL, Git, evidence, browser-visible diagnostics, or Notion.

Provisioning used the already-approved existing local recovery path. The host-held local identity reference is outside the repository, parent directory mode `0700`, file mode `0600`; the secret was not read into evidence or printed. The existing operator password was not read, rotated, or replaced.

The browser creates a 120-second `SIGN_IN` or `STEP_UP` challenge and receives only a short-lived approval code plus an HttpOnly browser nonce. The browser displays the exact Atlas command but never handles the host secret. `packaging/core/prime-local-auth` reads the separate secret only on Atlas and calls the loopback approval endpoint. Redemption is bound to challenge ID, purpose, browser nonce, expiry, and operator session for step-up; successful sign-in creates ordinary `prime_session` and CSRF cookies.

## Operator/browser evidence

Browser: real Chromium controlled through the project-required gstack browse skill, reaching the genuine private Core-served UI.

- Authentication: **PASS** — trusted-host SIGN_IN challenge was approved on Atlas and redeemed into protected PRIME state.
- Protected entry/project selection: **PASS** — the existing Qualification Project was selected; repository path `/home/sketch/Projects/ANIMUS_PRIME`, canonical revision beginning `9a2b54f`, project ACTIVE/ONLINE, Node ONLINE.
- Home / Needs Attention: **PASS** — protected shell loaded; no fabricated warning state was added.
- Overview: **PASS** — after Core restart, `Qualification Project · ACTIVE · ONLINE · freshness CURRENT` returned.
- Progress / Alignment: **PASS** — project-scoped progress loaded with current freshness and confidence data.
- Ask: **PASS as truthful degraded behavior** — the real UI returned `UNKNOWN` because model execution was unavailable or evidence did not support a safe answer; no unsupported answer was presented.
- Search: **PASS** — the real project-scoped search returned 16 results with source/revision/freshness information.
- Memory: **PASS** — stored project memories loaded.
- Knowledge: **PASS as truthful degraded state** — external knowledge was disconnected with no page URL.
- Evidence: **PASS** — evidence state loaded and reported its actual zero-current-evidence state.
- Activity: **PASS** — activity/history events loaded.
- Repository: **PASS** — real path, branch `main`, canonical revision, and dirty state were displayed truthfully.
- Authority: **PASS** — authority contract and `.agent` state loaded.
- Time Lens: **PASS** — current view and historical selector loaded.
- Usage: **PASS** — project-scoped state displayed.
- Backup: **PASS as truthful degraded state** — current state reported `UNKNOWN`; no unsupported backup claim was promoted.
- AI Connections / provider state: **PASS as truthful degraded state** — unavailable provider state remained bounded.
- Trusted-host STEP_UP: **PASS** — Atlas approval completed and the UI reported step-up accepted for 300 seconds.
- Logout/re-login: **PASS** — the same protected browser path was re-established through the host-approved sign-in flow after runtime restart; no password mutation was used.
- Responsive narrow viewport, keyboard-only critical flow, destructive confirmation, lifecycle mutation, registration, creation, deletion, release, and external provider workflows: **NOT RUN** in this bounded authentication continuation; they remain in the local qualification queue or parked/external scope.

## Security negatives and persistence

- Approval without `X-PRIME-Local-Identity`: **PASS — HTTP 401**.
- Approval with an incorrect host secret: **PASS — HTTP 401**.
- Replay of a consumed challenge: **PASS — HTTP 401**.
- Sign-in and step-up purpose confusion: **PASS** through purpose-specific API/static contract checks; the service rejects mismatched purpose and requires an existing session/CSRF for STEP_UP.
- Pre-approval polling: **PASS** — browser polling remains pending on the expected 401 until Atlas approval, then succeeds.
- Core restart: **PASS** — user-systemd restart returned Core and UI; the same project, repository binding, Node state, Progress, history, and operator-visible identity remained available.
- Clean shutdown/startup and duplicate Core prevention: **PASS** — systemd-owned `animus-prime-core` remained the single active PRIME Core; no unrelated listener was replaced.

## DOD and governed state

- DOD-005: **UNCHANGED BACKEND_ONLY**. The real Qualification Project still lacks a safe existing non-authority source with a supported reversible retraction/restoration path. No mutation was attempted and no synthetic source was created.
- DOD-008: **PRESERVED USER_USABLE_VERIFIED**, with the new trusted-host local identity path adding a bounded sign-in/step-up route alongside the existing recovery controls.
- DOD-009: **PRESERVED PRODUCT_VERIFIED**.
- DOD-074: **PRESERVED** from Continuation 055; not reopened here.
- R-056: **OPEN/GATED**. This continuation improves prerequisites but does not satisfy the complete integrated acceptance contract.
- Phase 15: **PARTIAL / not complete**.
- V1: **NOT DECLARED**.
- Deployment/public release: **NOT PERFORMED**.

## Validation

- Focused: `PYTHONPATH=. .venv/bin/pytest -q tests/phase15/test_local_identity_authentication.py tests/phase15/test_recovery_secret_regression.py` — **PASSED, 4 passed**.
- Full regression: `PYTHONPATH=. .venv/bin/pytest -q` — **PASSED, 96 passed, 28 skipped**. The prior floor was 94 passed / 28 skipped; the two additional passes are the new local-identity static/security contract tests, and the skip count did not change.
- Compile: `python -m py_compile apps/core/main.py src/prime_core/service.py tests/phase15/test_local_identity_authentication.py` — **PASSED**.
- Shell syntax: `bash -n packaging/core/prime-local-auth` — **PASSED**.
- Governance, burndown, alignment, traceability, diff, and secret scans — final post-record results recorded at closeout below.
- Browser/security/restart: **PASSED** for the bounded scope described above.

## Closeout publication

- Qualified implementation: `8c881256b6a0164cfef9ae411eb404107ac5c3c0`.
- Final governed HEAD: `8829f248ab8c87f03dd94a7a29c06fef267c8855`.
- `origin/main`: `8829f248ab8c87f03dd94a7a29c06fef267c8855`.
- GitHub main: `8829f248ab8c87f03dd94a7a29c06fef267c8855`.
- Parity: **PASSED**.
- Notion checkpoint: [Phase 15 Product Completion Checkpoint 058 — 8829f24](https://app.notion.com/p/3bc833cb27ff811693ffcc763d4de350).
