# ANIMUS PRIME - Phase 15 Continuation 075

Result: PARTIAL. The approved PRIME runtime Notion credential was made available through the existing secure runtime path. Real PRIME capability, product-API projection, and adapter lifecycle qualification passed against the approved sandbox. The complete operator-visible Notion lifecycle remains unqualified because the persistent UI exposes connection/health state but not the qualified projection, conflict, detach, and history actions. Phase 15/V1 remains INCOMPLETE. Deployment/public exposure NOT PERFORMED. Phase 16 NOT CREATED.

## Baseline and execution boundary

- Baseline: `92e05b5199ea3901d92a1f83902cede0e0bc63e5`
- Starting local HEAD: `92e05b5199ea3901d92a1f83902cede0e0bc63e5`
- Starting `origin/main`: `92e05b5199ea3901d92a1f83902cede0e0bc63e5`
- Execution: direct SSH/native Atlas at `/home/sketch/Projects/ANIMUS_PRIME`; no `Z:` runtime execution.
- Preserved unrelated untracked state: `.codebase-memory/`, `.prime-evidence/`, `.vscode/`.
- Existing PostgreSQL, Hindsight, PRIME project, enrolled Node, Core/UI topology, and PARAGON were preserved. No replacement database, bank, project, repository, Node, or Core stack was created.
- Approved Notion target only: `ANIMUS PRIME - Runtime Notion Qualification Sandbox - 2026-08-16`, parent page `3be833cb-27ff-814f-af89-ebfc3a2a8aed`.
- The canonical PRIME SOT, frozen specification, and unrelated MyAssistant pages were not mutated.

## Secure runtime credential

- Credential source: Atlas-only `/home/sketch/.config/animus-prime/notion-runtime.env`, mode `0600`, owner `sketch`.
- Runtime variable: `NOTION_READONLY_KEY`; raw value intentionally omitted from this evidence, Git, `.agent`, Notion, PostgreSQL, browser-visible state, and logs.
- PRIME credential reference: `env/myassistant/notion-readonly`.
- PRIME metadata reference file: `/home/sketch/.local/share/animus-prime-core/notion-credential-reference.json`, mode `0600`; reference metadata only.
- PRIME lifecycle state: `/home/sketch/.local/share/animus-prime-core/notion-lifecycle-state.json`, mode `0600`; no raw credential.
- The credential was resolved by the existing `NotionCredentialResolver`; no broad secret discovery or new authentication architecture was used.

## Persistent runtime

- Service: `animus-prime-core.service`, active/running through the existing user systemd path.
- New persistent container: `animus-prime-core`; image `animus-prime-core:continuation-074-final2`.
- Previous container preserved as rollback: `animus-prime-core-pre-notion-075`.
- New MainPID after credential-enabled restart: `947310`.
- Active-enter timestamp after restart: `2026-08-16 16:18:57 EDT`.
- Listener: private `127.0.0.1:18000`; no public exposure, Funnel, firewall, or Tailscale change.
- `/health/ready`: PASSED.
- Health build provenance: commit `376dfce3ce8e46941b7fa276fd751872a7fcd462`, image `animus-prime-core:continuation-074-final2`, schema `0036_operator_workflows.sql`.
- Existing PostgreSQL and Hindsight health/database connectivity remained healthy; no reset or substitute service was used.

## Runtime Notion capability

The existing PRIME runtime path successfully resolved the approved credential and exercised the approved sandbox:

- Capability read probe: PASSED; page read and block read available.
- Managed write probe: PASSED; page write available and `managed_write=CAPABILITY_PRESENT`.
- Controlled probe child created under the approved sandbox: `3be833cb-27ff-81aa-9fe2-ffb4fcf5f980`.
- No raw credential appeared in the response, UI, logs, or evidence.

The probe child is approved qualification data within the named sandbox; it is not a substitute project, bank, or repository.

## PRIME product/API path

- Authenticated PRIME product call `POST /v1/projects/project_d9a1a5b609394282b62fc12c0d04634d/ai/product` with `function=DOCUMENTATION` returned HTTP 200.
- The call used the existing PRIME project and approved sandbox parent, with no synthetic project or source set.
- Resulting project record page: `3be833cb-27ff-8159-add6-e883c1cc54af`.
- Project snapshot reported Notion `CONNECTED`, with managed content hash present and no raw credential.
- Browser re-authentication through the normal trusted PRIME local-auth flow succeeded after the Core restart.
- Persistent UI displayed Notion `HEALTHY`, imported existing local authorization, and read access `Available`.
- The UI did not expose a complete operator action path for projection, conflict, detach, or managed history. Its Knowledge surface showed `CONNECTED`, but page URL and last-synced fields remained `NONE`.

## Existing adapter lifecycle qualification

The direct probe used the production `NotionApiProvider` and `NotionLifecycleService` inside the persistent Core container, against the existing qualification project and approved sandbox. No fake provider or test-only integration was used.

- Existing project record binding: `BOUND`; repeat bind was idempotent.
- First managed projection: `SYNCED` to the existing project record page; managed section `CURRENT_STATUS`.
- Operator-authored text: preserved across projection and recovery.
- User-content conflict: returned `CONFLICT`/`CONFLICT`; no overwrite occurred.
- Recovery after conflict: `SYNCED`.
- Stale job: rejected as `STALE_JOB_REJECTED` for source revision `continuation-075-stale`.
- Managed history: created one history page for period `2026-08-16-075`; repeat operation was idempotent.
- Source lifecycle attach/refresh: `ATTACHED`; retrieval `CURRENT`; provenance present.
- Source lifecycle detach: `DETACHED`; retrieval `RETRACTED`; `purged=false`.
- Project record operator text remained present after the complete lifecycle sequence.
- Durable state and page identity remained tied to the approved sandbox/project; no canonical SOT page was touched.

## Qualification boundary and governance

The real runtime capability and backend lifecycle are now evidenced, but the frozen Notion-backed requirements that require a user-facing workflow are not promoted by backend calls alone. No DOD or R status was promoted in this continuation.

- DOD-034, DOD-035, DOD-036, DOD-064, DOD-065, and DOD-066 remain `BACKEND_ONLY` / not user-usable verified because the persistent PRIME UI does not expose the complete lifecycle workflow.
- R-037 through R-041 remain `VERIFIED` on their prior governed evidence; this continuation adds supporting runtime facts and does not replace their historical basis.
- DOD-005 remains parked.
- DOD-081 and R-056 remain gated/last.
- Notion-runtime capability is no longer absent; the remaining gap is the operator-visible product path, not credential resolution.
- No PARAGON, Hindsight architecture, Windows, second-device, Tailscale, Phase 16, deployment, or public-exposure work was performed.

## Validation

- Persistent Core restart and private health: PASSED.
- Runtime Notion credential resolution and capability read: PASSED.
- Managed write probe in approved sandbox: PASSED.
- PRIME authenticated Documentation product API path: PASSED (HTTP 200).
- Production adapter lifecycle: PASSED for bind, projection, preservation, conflict refusal, recovery, stale rejection, history idempotence, attach/refresh provenance, and detach/retraction.
- Browser authenticated UI/read-status qualification: PASSED for connection/health/read state; NOT COMPLETE for full operator lifecycle because the action surface is absent.
- `python -m compileall -q apps src tests`: PASSED.
- Full regression: PASSED, `110 passed, 28 skipped`.
- Governance validation: PASSED, `validate_governance.py --mode ADOPTED`.
- Burndown validation: PASSED; `audit_total=81`, `complete=50`, `burndown=31`, complete plus burndown `81`.
- `git diff --check`: PASSED.
- Secret scan: PASSED; no raw token pattern in governed files.
- Deployment/public exposure: NOT PERFORMED.

## Final conclusion

Continuation 075 is `PARTIAL`: the approved runtime Notion credential and real PRIME backend lifecycle are available and qualified in the named sandbox, but the frozen operator-visible Notion workflow is not yet qualified. The next bounded product decision is to expose and qualify that existing lifecycle through the genuine PRIME UI/API contract, or formally record the remaining UI boundary. No automatic Continuation 076 is started.
