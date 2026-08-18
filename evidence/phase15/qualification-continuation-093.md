# Phase 15 Qualification — Continuation 093

Date: 2026-08-18
Frozen specification: `PRIME-SPEC-V1.0.0`
Starting governed HEAD: `71cf76a44846ec9d24080e28f92c0f7bca09ff4a`
Qualified implementation: `65e553f084f5c5fba970ad7bf25c581ab15066ff`
Disposition: **COMPLETE for the bounded Continuation 093 scope**

## Objective and result

Continuation 093 completed the genuine Fork workflow and the remaining frozen V1 polish boundary using the persistent Atlas product. DOD-016 and DOD-080 are promoted to `USER_USABLE_VERIFIED`. The governed queue moves from 74 complete / 7 open to 76 complete / 5 open. The five open rows are DOD-013, DOD-047, DOD-053, DOD-079, and aggregate DOD-081/R-056.

No deployment, public exposure, Phase 16 work, specification change, synthetic project, synthetic bank, or synthetic machine was performed.

## Persistent browser tooling gate

The approved non-privileged Playwright installation is outside the repository and outside canonical PRIME runtime state:

- install root: `/mnt/storage1tb/prime-tooling/gstack-playwright`
- Playwright: `1.62.1`
- Chrome for Testing: `151.0.7922.34`, Playwright revision `1234`
- browser: `/mnt/storage1tb/prime-tooling/gstack-playwright/chromium-1234/chrome-linux64/chrome`
- headless shell: `/mnt/storage1tb/prime-tooling/gstack-playwright/chromium_headless_shell-1234/chrome-headless-shell-linux64/chrome-headless-shell`
- ffmpeg: `/mnt/storage1tb/prime-tooling/gstack-playwright/ffmpeg-1011/ffmpeg-linux`
- gstack environment: `/home/sketch/.gstack/browser.env` (external, mode `0600`)
- Chrome SHA-256: `0b20b130e7edd9dd51873be867761295fe0cfad490c2b9a64f95bd3cfc08fa71`
- headless-shell SHA-256: `e11fc9ce65c96313476f7ee9844b6fb6a9220fb048693cfe9eee00acf4170a9f`
- ffmpeg SHA-256: `460d44f3416005662f528d4b92e7b94ace924e8a0288106d3803b73c56eaadc8`

The first supported installation attempt failed because temporary extraction under `/tmp` reached the account quota. Repeating the supported install with `TMPDIR` on `/mnt/storage1tb` succeeded. Atlas blocks the unprivileged Chromium sandbox, so gstack's supported `GSTACK_CHROMIUM_NO_SANDBOX=1` path was required. No privileged package or Xvfb installation was used. gstack launched the installed browser successfully before qualification began.

## Runtime provenance

- image: `animus-prime-core:continuation-093-65e553f`
- image ID: `sha256:82791590061475955dfbc1962264ee357acfb84066e7ba4bb15f965fdb861cdc`
- build commit: `65e553f084f5c5fba970ad7bf25c581ab15066ff`
- build timestamp: `2026-08-18T23:25:00Z`
- container start: `2026-08-18T23:25:08.82302022Z`
- listener: `127.0.0.1:8000`
- service: persistent user-managed PRIME Core, active
- readiness: `ready`
- schema: through `0040_destructive_lifecycle_sagas.sql`

The existing persistent PostgreSQL, Hindsight, Notion credential reference, repository Node, and PRIME state were reused. No secret value was printed or committed. Rollback containers were preserved.

## Product repairs

1. Implemented the complete durable Fork workflow: child identity, selected revision, independent repository, mutable child authority, independent Goal/baseline, new MCP grant, separate Hindsight bank, separate Notion Project Record, Brain state, durable workflow steps, and `PROJECT_FORKED` activity.
2. Restricted source cleanliness checks to tracked changes so unrelated untracked operator files are preserved without making a valid source revision unusable.
3. Adapted approved legacy parent Goals into an independent child Goal review state without rewriting parent authority.
4. Rejected invalid memory content classes at the API boundary with HTTP 422 instead of allowing a database exception to surface as HTTP 500.
5. Updated one stale Continuation-031 Fork request fixture to the current confirmed workflow contract.

## Qualification summary

- Fork/isolation: PASSED; see `qualification-continuation-093-fork-isolation-matrix.md`.
- Polish/browser: PASSED; see `qualification-continuation-093-polish-matrix.md`.
- External gates: reconciled; see `qualification-continuation-093-external-gates.md`.
- focused Continuation 093 tests: `8 passed`.
- affected focused suite: `16 passed`.
- full supported regression: `149 passed / 35 skipped / 0 failed`.
- persistent restart and re-read: PASSED.
- duplicate/replay protection: PASSED.
- browser console after final reload/matrix: no errors.
- public exposure: NOT PERFORMED.
- deployment: NOT PERFORMED.

## Acceptance reconciliation

`DOD-016`: `USER_USABLE_VERIFIED`.

`DOD-080`: `USER_USABLE_VERIFIED`.

`DOD-081` / `R-056`: OPEN. All local-code and local-browser rows are exhausted, but release remains blocked by the four explicit external requirements listed in the external-gates record. Phase 15 and V1 remain incomplete.
