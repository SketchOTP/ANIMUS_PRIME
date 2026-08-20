# ANIMUS PRIME Post-V1 UX Wave A Qualification

## Disposition

- Directive: `D-PRIME-POSTV1-UX-WAVE-A-001`
- Acceptance: `MET`
- Frozen V1 posture: preserved at 81/81 with Phase 15 complete
- Deployment: not performed
- Public exposure or Funnel change: not performed
- Phase 16 or Continuation 097: not created

## Baseline and provenance

- Starting governed PRIME commit: `a3b941b88226085334f6bb908dba17439bcdb91b`
- Qualified frozen V1 runtime before Wave A: `d067a247dbeea47eb8b061111db04e7cd95bebe2`
- Wave A implementation commit: `df5b914e194349ad67ef6c9f61229f1912512c76`
- Approved external design-reference baseline: `/home/sketch/Projects/animus_directive` at committed lineage `550b303...`
- Canonical design brief: `docs/post-v1/ANIMUS-PRIME-UX-DESIGN-REMEDIATION-BRIEF.md`
- Authoritative execution path: direct Atlas checkout `/home/sketch/Projects/ANIMUS_PRIME`; no mapped `Z:` path was used.

## Bounded implementation

Wave A changed the existing genuine web application in `apps/web/index.html`; it did not create a second UI or a replacement runtime.

- Added the approved dark-neon token foundation, compact global navigation, selected-project identity, contextual project navigation, and one-active-surface routing.
- Reduced global navigation to Home, Projects, Attention, Activity, and System while preserving every qualified V1 project/system surface through contextual routes.
- Added state-driven protected entry and setup behavior without changing authentication, trusted-host, CSRF, or API contracts.
- Rebuilt Home around health, key counts, needs attention, resume work, recent projects, and recent activity.
- Rebuilt Projects around concise identity/status/action cards, a content filter, a 24-card initial window, progressive show-more behavior, and collapsed project creation.
- Preserved old deep links through the route map, safely sent invalid routes to Home, and held project routes on the Projects surface when no project is selected.
- Added responsive navigation/drawer behavior, 44-pixel controls, visible keyboard focus, reduced-motion handling, and a 320-pixel no-overflow layout.
- Added `tests/phase15/test_post_v1_wave_a.py` for tokens, shell/navigation, one-surface routing, deep-link safety, project scale controls, accessibility, product boundaries, unique IDs, and JavaScript syntax.

No backend/API, migration, PostgreSQL, Node, Hindsight, Notion integration, or network contract changed.

## Validation

### Focused and static

- `python3 -m pytest -q tests/phase15/test_post_v1_wave_a.py tests/phase14/test_web_shell.py tests/phase15/test_continuation059_safe_wave.py tests/phase15/test_recovery_secret_regression.py`: `PASSED` — 9 passed.
- `PYTHONPATH=.:src .venv/bin/python -m compileall -q apps src scripts tests`: `PASSED`.
- `git diff --check`: `PASSED`.
- Governed YAML/governance validation in adopted mode: `PASSED`.
- Product-alignment validation: `PASSED` — preserved 81/81.
- V1 burndown validation: `PASSED` — empty.

### Full supported regression

Executed with the repository virtual environment, `PYTHONPATH=.:src`, and a bounded temporary root on attached storage:

`TMPDIR=<storage1tb temp> PYTHONPATH=.:src .venv/bin/python -m pytest -q --basetemp=<storage1tb temp>/run`

Result: `PASSED` — 175 passed / 41 skipped / 0 failed.

Unsupported attempts using system Python, an omitted `PYTHONPATH`, or the quota-constrained default `/tmp` were environment/command-selection failures and were not counted as product regressions. The Phase-15 qualification driver was not used as a post-V1 release gate because its database-backed Phase-15 fixture contract was not configured for this Wave A UI run.

## Persistent Atlas runtime

- Runtime image: `animus-prime-core:postv1-wave-a-df5b914`
- Image revision: `df5b914e194349ad67ef6c9f61229f1912512c76`
- Image creation timestamp: `2026-08-20T00:26:07Z`
- Service: `animus-prime-core.service`
- Post-qualification restart MainPID: `4139059`
- Post-qualification active timestamp: `Wed 2026-08-19 20:34:27 EDT`
- Readiness: `PASSED`
- Readiness identity: build `df5b914e194349ad67ef6c9f61229f1912512c76`, image `animus-prime-core:postv1-wave-a-df5b914`, schema `0041_capacity_controls.sql`, service `1.0.0`.

The first container recreation omitted the established `1000:1000` runtime user and failed closed on the persistent credential-reference file; automatic rollback restored the qualified prior runtime. A second recreation exposed inherited old build-identity environment values. The final recreation preserved the established user/mount/network/restart contract and removed only those inherited provenance overrides. No persistent data was reset and the prior qualified container remains available as rollback evidence.

## Real private-browser qualification

- Browser: persistent gstack Playwright Chromium under `/mnt/storage1tb/prime-tooling/gstack-playwright`
- URL: `https://atlas-2.tail1a5964.ts.net/`
- Protected entry: `PASSED`; unauthenticated state exposed only authentication/setup controls.
- Trusted-host sign-in: `PASSED` through the existing Atlas approval helper.
- Home: `PASSED`; twelve interactive controls in the active surface versus the previous all-surfaces document, with concise health/attention/resume/recent information.
- Projects: `PASSED`; 24 of 746 cards initially rendered, project filter present, and progressive show-more available.
- Project selection: `PASSED` using the qualified Linux project `project_db3ef8c4bc834e68a2e9a9deabbb5a80`.
- Contextual project shell: `PASSED`; persistent identity, status, group tabs, and only the selected workspace surface visually active.
- Deep links: `PASSED` for Progress, Search, Warm Start, diagnostics/system aliasing, refresh, and invalid-route Home fallback.
- No-project project route: `PASSED`; the Projects surface is active and selected-project identity is hidden while the requested project route remains pending.
- Core restart/session recovery: `PASSED`; same authenticated session and selected Linux project returned after service-manager restart on the exact Wave A image.
- Logout/re-login: `PASSED`; protected state cleared, trusted-host sign-in succeeded again, and the no-project state opened the Projects surface safely.
- Responsive: `PASSED` at 320 by 800; no horizontal document overflow, mobile navigation opened with its scrim and closed on Escape.
- Keyboard/focus: `PASSED` for sequential focus and route-heading focus behavior; reduced-motion and visible-focus contracts are also covered by the focused test.
- Performance smoke: `PASSED`; authenticated overview reload completed in approximately 30 ms in the private browser measurement.

Historical 401 console entries were produced by expected pre-authentication trusted-host polling. Current authenticated reload and interactions produced no new product failure.

## Visual evidence

- `/home/sketch/wave-a-home-final-desktop.png` — SHA-256 `419a7a07b86dafd36938e3e7e975eb6f0783e7a98a8f1d2df61117d155061681`
- `/home/sketch/wave-a-projects-final-desktop.png` — SHA-256 `a16f8b338bdbf898b4c1639025af991b15d148ef3d74fa9cef47a4d34dafeb9d`
- `/home/sketch/wave-a-overview-mobile-final.png` — SHA-256 `0da9eeb75bde24b2b6edd16e219e2ba384faca21b4eed2f8fb04e3b2953f64f9`
- `/home/sketch/wave-a-overview-final-desktop.png` — SHA-256 `d47b8852561eda28ea69ffcc66af897f92a217527d67368adb3b765b64147f07`

## Final boundary

Wave A is complete for design foundation, shell/navigation, Home, and Projects. Later project-surface redesign waves remain unstarted. The frozen V1 qualification is preserved; private production use remains the only authorized operating posture.
