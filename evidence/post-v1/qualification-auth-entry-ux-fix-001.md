# ANIMUS PRIME post-V1 authentication-entry UX correction 001

## Disposition

- Directive: `D-PRIME-POSTV1-AUTH-ENTRY-UX-FIX-001`
- Result: `PARTIAL / DONE_WITH_CONCERNS`
- Main initialized-versus-uninitialized UX defect: `CORRECTED AND QUALIFIED`
- Remaining acceptance gap: `LIVE_PASSWORD_SIGN_IN_BLOCKED_BY_STALE_SECURE_REFERENCE`
- Frozen V1 posture: preserved at 81 complete / 0 open; Phase 15 remains COMPLETE; V1 remains qualified for private production use.
- Wave B, Phase 16, Continuation 097, deployment, public exposure, and Funnel: not started or changed.

## Baseline and implementation

- Starting governed/GitHub baseline: `6f86b2552d801abc9e53744b9034a6298792b586`
- Starting qualified Wave A runtime: `df5b914e194349ad67ef6c9f61229f1912512c76`
- Qualified implementation commit: `bf475690ca7b86d08721c262ba538260e3742da3`
- Runtime image: `animus-prime-core:postv1-auth-entry-bf47569`
- Build timestamp: `2026-08-20T01:34:12Z`
- Schema: `0041_capacity_controls.sql`

## Investigation answers

1. The protected UI previously used only `/v1/operator/state`; no unauthenticated initialization-state response existed.
2. Any protected-state failure, including the normal 401 for a missing or expired session, set `entryMode='auth'` and activated the combined `#setup` route.
3. Initialization was not safely knowable without authentication before this patch.
4. A UI-only correction was therefore unsafe because it would have guessed from 401 or hidden clean-install setup permanently.
5. The smallest required backend state is `GET /v1/auth/state -> {"initialized": true|false}`. It queries only whether one operator row exists and returns no identity, credentials, recovery state, projects, providers, Nodes, database details, Notion state, or diagnostics.
6. Existing authenticated refresh and Core-restart session persistence were working and passed again after the patch.
7. Before correction, initialization, setup checklist, trusted-host sign-in, password sign-in, and expanded recovery controls were mounted together on the same ordinary unauthenticated route. The new branch separates `#auth-entry` and `#setup`; setup is hidden and its controls are disabled unless Core explicitly returns `initialized:false`.

## Product correction

- Added the minimal non-sensitive `CoreService.initialized()` read and `/v1/auth/state` endpoint.
- Added explicit `initialized`, `uninitialized`, and fail-closed error entry branches.
- Initialized unauthenticated PRIME now shows only ANIMUS PRIME identity, `Sign in`, `PRIME is online and ready`, trusted-host primary action, password secondary action, and collapsed `Recovery options`.
- `Initialize new PRIME`, infrastructure setup, and setup checklist are not rendered in initialized entry; bootstrap controls are disabled unless the server confirms an uninitialized database.
- Unknown initialization state routes to a concise protected-entry error and exposes no bootstrap action or protected payload.
- The complete first-run bootstrap section remains present only for `initialized:false`; the backend bootstrap refusal remains defense in depth.
- Recovery remains unchanged behind deliberate `<details>` disclosure. Existing cookies, sessions, CSRF, origin checks, rate limiting, trusted-host challenge, password verification, recovery, session revocation, step-up, and destructive-action protections were not weakened.

## Automated validation

- Focused auth/Wave A/security suite: `21 passed`.
- Complete supported regression: `188 passed / 41 skipped / 0 failed` using `.venv`, `PYTHONPATH=.:src`, and exact basetemp `/home/sketch/.cache/animus-prime-tests/pytest-auth-entry-bf47569-20260820T0148Z`.
- The first two full-suite attempts were invalid environment evidence only: default `/tmp` hit user quota, then the attached-drive basetemp was read-only. All failures/errors were temp-file creation failures. No product assertion failed in those attempts.
- Compile/static: PASSED.
- Governance ADOPTED: PASSED.
- Product alignment/traceability/release cross-view: PASSED, 81/81.
- Burndown: PASSED, empty.
- Diff/whitespace: PASSED.
- Secret-pattern review: PASSED.

## Persistent runtime

- Service manager: `systemd --user`, `animus-prime-core.service`.
- Runtime replacement preserved user `1000:1000`, host network, all established mounts, credential references, and `unless-stopped` restart policy.
- Retained rollback container: `animus-prime-core-pre-auth-entry-df5b914`.
- Post-qualification restart changed MainPID `64425 -> 77376` at `Wed 2026-08-19 21:42:44 EDT`.
- Readiness after restart reports exact commit `bf475690ca7b86d08721c262ba538260e3742da3` and image `animus-prime-core:postv1-auth-entry-bf47569`.
- `GET /v1/auth/state` returns exactly `{"initialized":true}` on the real persistent installation.
- The first replacement helper attempt stopped before service mutation because `/mnt/storage1tb/prime-tooling/runtime` was read-only. The successful attempt used a mode-0600 `/dev/shm` environment file that was removed automatically after container creation; no credential was printed or persisted.

## Real private-browser qualification

- Browser: gstack `/browse`, HeadlessChrome `145.0.7632.6` on genuine Windows host SKETCH.
- URL: `https://atlas-2.tail1a5964.ts.net/`.
- Initialized fresh session: PASSED. Active route was only `auth-entry`; `setup` and `bootstrap-form` were not visible; recovery was closed.
- Desktop visual: PASSED.
- Mobile 320 by 800: PASSED with document width exactly 320 and no horizontal overflow.
- Keyboard: PASSED; initial Tab focused trusted-host primary, followed by password and sign-in.
- Recovery disclosure: PASSED closed by default, visible only after deliberate summary activation, and re-collapsed successfully.
- Trusted-host sign-in: PASSED through the existing Atlas local-identity helper; Home loaded authenticated.
- Authenticated refresh: PASSED with no console errors.
- Core restart/session recovery: PASSED on the same browser session and exact new build/image.
- Logout: PASSED; returned to compact initialized sign-in with setup/bootstrap absent and recovery collapsed.
- Protected-data boundary: PASSED; `/v1/operator/state` returned 401 before authentication, then `/v1/auth/state` returned only the boolean bootstrap state.
- Performance smoke: 39 ms total browser load measurement.

## Password acceptance concern

- Live password sign-in was attempted once using the existing mode-0600 `/home/sketch/.config/animus-prime/operator.password` reference without displaying its contents.
- Result: `INVALID_CREDENTIALS` / HTTP 401.
- A bounded in-process comparison confirmed the stored password reference does not match the current operator password hash. No broad secret discovery was performed.
- No password, recovery credential, session, or operator state was rotated. Recovery was not invoked because this directive did not authorize authentication-state mutation merely to manufacture a browser PASS.
- Automated password-route coverage remains green, and trusted-host authentication is fully usable, but the directive's explicit live password-success item remains unqualified.
- Operator/Architect action required: provide the current operator password through an approved ephemeral path, or explicitly authorize recovery-based password/reference rotation and its session-revocation consequence.

## Visual evidence

- `/home/sketch/auth-entry-desktop-final.png` — SHA-256 `ff8e8a53dc644e3e2f80c4ca4207718e4a051f590b328266ef3186746648f704`
- `/home/sketch/auth-entry-mobile-final.png` — SHA-256 `a66730f77bf1ed762efca45dbb0f0fe2ba0fe02788e391b5caa182c6a764f4f5`

## Boundary

The initialized-entry defect is fixed and running privately. The overall directive remains PARTIAL solely because live password login cannot be truthfully marked successful against the stale approved reference. Frozen V1 remains complete; this post-V1 acceptance gap does not reopen any V1 DOD or requirement.
