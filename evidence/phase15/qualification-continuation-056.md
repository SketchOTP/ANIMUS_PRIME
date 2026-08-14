# ANIMUS PRIME — Phase 15 Qualification Continuation 056

Status: **PARTIAL — Local V1 convergence**
Date: 2026-08-14
Execution boundary: direct SSH/native Atlas only; no `Z:` path execution and no disposable environment.

## Baseline and publication identity

- Frozen specification: `PRIME-SPEC-V1.0.0`
- Authoritative checkout: `/home/sketch/Projects/ANIMUS_PRIME`
- Starting governed commit: `94e01e48d3b878b792b724476a07d4139a7a453a`
- Starting `origin/main`: `94e01e48d3b878b792b724476a07d4139a7a453a`
- Starting worktree: only preserved untracked `.codebase-memory/`, `.prime-evidence/`, and `.vscode/`; no unrelated tracked changes were overwritten.
- The Continuation 055 ledger contained a non-resolvable transcription `0a3c82f53d0c5c70a37db7f8c3a2dbdb6d76d42f`. GitHub history confirms the actual qualified implementation commit is `0a3c82f0c606fb80f914eb59116dd5f46b9d5ec5` (`feat-persistent-node-trust-lifecycle`). Git history was not rewritten; the ledger and 055 evidence now contain the resolvable SHA and an explicit correction note.

## Scope and implementation

This continuation addressed the next local convergence queue without reopening parked work:

- Added persistent step-up authentication storage and API behavior through migration `0033_step_up_authentication.sql`, including five-minute recent-authentication state and audit logging.
- Added the genuine Core-served Web UI recovery and step-up controls. Recovery responses do not render or persist returned recovery credentials in the browser page.
- Protected backup restore with an authenticated session, explicit `X-PRIME-STEP-UP: CONFIRM`, and recent step-up state.
- Extended source retraction to append a current `DEGRADED` documentation projection while preserving the prior `SYNCED` projection for historical provenance.
- Added focused regression coverage for secret-safe recovery/step-up UI and source-lifecycle documentation projection staleness.

Files changed for the implementation are `apps/core/main.py`, `apps/web/index.html`, `migrations/prime/0033_step_up_authentication.sql`, `src/prime_core/history_service.py`, `src/prime_core/service.py`, `tests/phase15/test_recovery_secret_regression.py`, and `tests/phase15/test_requirement_qualification.py`.

## Persistent Atlas topology

| Component | Runtime and identity | Persistence / target | Result |
|---|---|---|---|
| PostgreSQL | Existing persistent PostgreSQL instance; reused, not recreated | Existing PRIME database | PASSED — schema migration applied and readiness returned `0033_step_up_authentication.sql` |
| Hindsight | Existing approved Hindsight integration | Existing configured target | PASSED — preserved; no replacement bank created |
| Repository Node | `animus-prime-node.service`, canonical `node-041-atlas-native` | `/home/sketch/Projects/ANIMUS_PRIME`, trust references outside Git | PASSED — user service active/enabled; prior mTLS identity preserved |
| PRIME Core | `animus-prime-core.service` managing container `animus-prime-core`; image `animus-prime-core:continuation-056` | Existing persistent Core state mount and same container identity | PASSED — service active/enabled; no duplicate Core |
| PRIME Web UI | Core-served `apps/web/index.html` | Same persistent Core process | PASSED — real UI reached over the private SSH tunnel |

Core listener is `127.0.0.1:18000` on Atlas. The Windows browser used `http://127.0.0.1:28000/` through an SSH local forward to Atlas `127.0.0.1:18000`; direct Windows access to `127.0.0.1:18000` was not used. The Node listener remains private at `127.0.0.1:18001`. Existing PostgreSQL/Hindsight listeners and unrelated Atlas services were not replaced or modified. Public exposure and Funnel changes were not performed.

The Core service was re-established after the image rebuild by stopping the PRIME-owned container and starting the same container through the enabled user systemd unit. Readiness then returned:

```json
{"status":"ready","schema_version":"0033_step_up_authentication.sql"}
```

This was a persistent service restart, not a disposable replacement environment. Startup policy remains user-systemd enabled; clean stop/start and restart recovery were exercised against the same persistent container/state path.

## DOD-005 exact frozen-criterion re-evaluation

The frozen criterion requires current source-derived Search, Documentation, Progress, and Memory views to retract when a source is removed while historical provenance remains until purge. The implementation now:

- invalidates current source references and derived Memory/Search/Progress views;
- appends a current `DEGRADED` documentation projection with source lifecycle `RETRACTED`;
- preserves the prior `SYNCED` projection as historical provenance;
- exposes the derived count `documentation_projections_staled`.

This is a local architectural invariant and is not blocked automatically by live Notion. A safe direct persistent mutation qualification against the governed project was not run in this continuation because creating substitute project/database state is forbidden and the existing qualification project must not be destructively mutated merely to manufacture evidence. Therefore DOD-005 remains truthfully `BACKEND_ONLY`, with `blocked_by: NONE`; the next action is bounded direct qualification on the existing governed path with restoration guaranteed.

## DOD-008 operator recovery and step-up

The real persistent Core behavior was exercised with the existing single operator and secret-safe remote handling:

- recovery rotation: `PASSED`;
- previous sessions revoked and replacement references stored outside Git with owner-only permissions: `PASSED`;
- fresh authenticated session followed by recent step-up re-authentication: `PASSED`;
- restore without recent step-up: refused with HTTP `403`, `RESTORE_STEP_UP_REQUIRED`: `PASSED`;
- recovery and step-up controls visible on the actual Core-served UI through the private browser tunnel: `PASSED`.

No raw credential was recorded in evidence, Git, `.agent`, Notion, browser-visible diagnostics, or logs. Qualification material was rotated again after the check. DOD-008 is promoted to `USER_USABLE_VERIFIED` for the bounded single-operator path.

## DOD-009 backup/privacy reconciliation

The frozen backup/privacy criterion is supported by the existing AES-256-GCM/PBKDF2 backup implementation, coherent manifest/recovery tests, and the web/core no-store boundary. The actual web shell has no service-worker payload cache; browser fetches use `cache: 'no-store'`, and Core responses include `Cache-Control: no-store` plus the established security headers. Existing R-042/R-043 evidence and Phase 13 backup/reliability tests remain the implementation basis. DOD-009 is promoted to `PRODUCT_VERIFIED`; no new database or backup target was created.

## Browser/operator checks

The actual Core-served UI was reached through Chromium using the private SSH tunnel. The recovery and step-up controls were present in the real page, and no returned recovery credential was rendered by the page. The previously qualified authenticated project journey and Node healthy/offline/recovery journey remain preserved from Continuation 055. Optional Notion/model/Hindsight Reflect capabilities continue to show bounded unavailable/degraded states rather than blocking the local product.

## Validation

- Focused recovery/source-lifecycle and backup/privacy checks: **PASSED** — `7 passed, 11 skipped`; integration skips require the established `PRIME_PHASE1_DB_URL` boundary.
- Full regression: **PASSED** — `94 passed, 28 skipped in 8.03s`; the pass increase reflects this continuation's focused regression coverage; skip count is unchanged.
- Compile/static and `git diff --check`: **PASSED**.
- Governance, burndown, and product-alignment structural checks: **PASSED** where applicable; the broader V1 release gate remains intentionally open.
- Persistent runtime: **PASSED** — Core service active/enabled, Node service active/enabled, readiness healthy, same persistent container/state identity.
- Browser/UI: **PASSED** for the bounded recovery/step-up visibility and preserved previously qualified operator journey; no claim is made for unavailable external integrations.
- Secret checks: **PASSED** — no raw credential material recorded.
- Deployment/public exposure: **NOT PERFORMED**.

## Governed state after Continuation 056

- DOD-008: `USER_USABLE_VERIFIED` for the bounded recovery/step-up path.
- DOD-009: `PRODUCT_VERIFIED` for encrypted coherent backup and browser/service-worker privacy invariants.
- DOD-005: `BACKEND_ONLY`; direct persistent mutation qualification remains required and is not a live Notion blocker.
- Local queue: 5 `LOCAL_CODE`, 15 `LOCAL_BROWSER_QUALIFICATION`, 0 `LOCAL_NATIVE_QUALIFICATION`, 0 `EVIDENCE_RECONCILIATION`, and 15 `EXTERNAL_ENVIRONMENT` items.
- R-056 remains open and gated. Phase 15 and V1 remain incomplete. Phase 16 was not created. Deployment was not performed.
