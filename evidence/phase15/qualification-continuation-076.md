# ANIMUS PRIME Phase 15 Qualification Continuation 076

## Scope and acceptance

- Directive: `ANIMUS PRIME - Phase 15 Continuation 076`
- Objective: qualify the approved persistent runtime Notion lifecycle through PRIME's real authenticated web UI.
- Scope boundary: existing persistent Atlas Core/UI, existing Qualification Project, approved Notion sandbox, and the existing secure runtime authorization. No new project, repository, bank, Node, provider, public ingress, deployment, DOD-005, DOD-081, R-056, Phase 16, or synthetic target was created.

## Baseline

- Starting governed PRIME commit: `23189b2de427a5f06ae85fb839b0edafa5c3a072`
- Starting local/origin parity: local `23189b2`, `origin/main` `23189b2`; worktree preserved untracked `.codebase-memory/`, `.prime-evidence/`, and `.vscode/`.
- Existing persistent services: PostgreSQL, Hindsight, PRIME Core/UI, and the enrolled Atlas repository Node were preserved.
- Approved Notion parent: `3be833cb-27ff-814f-af89-ebfc3a2a8aed`
- Existing PRIME project record: `3be833cb-27ff-8159-add6-e883c1cc54af`
- Existing controlled read-only source page: `3be833cb-27ff-81aa-9fe2-ffb4fcf5f980`
- Project qualified through the UI: `project_d9a1a5b609394282b62fc12c0d04634d` (`Qualification Project`)
- Raw credentials were not written to this evidence, Git, Notion, browser DOM, or application state.

## Implementation and runtime

- Initial UI implementation: `bbe4c80618d6bf83e157d55633e2a15f278f80f2`, exposing the authenticated Notion state and operator actions.
- Lifecycle repair: `606de3927ad723059ad4843db5a7d441b719bd40`, preserving `DETACHED / RETRACTED` sources during refresh and reconciliation.
- Final operator-route repair: `c687ad619d87e5ace9d37e9ad7c202bc3760fed1`, honoring an already-persisted same-period history page as idempotent instead of retrying external creation.
- Final persistent image: `animus-prime-core:continuation-076-final3`
- Final runtime build commit: `c687ad619d87e5ace9d37e9ad7c202bc3760fed1`
- Final runtime build timestamp: `2026-08-16T17:35:00Z`
- Runtime mechanism: PRIME-owned Docker container animus-prime-core, with restart/replacement performed through the existing persistent container path.
- Final container health: ready, schema 0036_operator_workflows.sql, service version 1.0.0.
- Final container process identity: uvicorn PID 1060360; container StartedAt 2026-08-16T21:11:29Z (2026-08-16 17:11:29 EDT).
- Previous Core image was retained as named rollback container `animus-prime-core-pre-076-final2`.
- Listener remained the existing private local Core/UI topology; no public exposure or Funnel change occurred.

## Browser operator qualification

Browser: gstack Chromium session through the persistent local UI at `http://127.0.0.1:28000/`.

- Authentication: trusted PRIME host challenge approved on Atlas; protected state loaded without browser-visible host secret.
- Project selection: existing `Qualification Project` selected; project identity and repository binding remained unchanged.
- Notion state: `BOUND`, health `BOUND`, existing record page and approved parent displayed, classification `PRIME_MANAGED_RECORD_AND_READ_ONLY_SOURCES`, authoritative `NO`.
- Managed record: UI displayed page identity, URL, revision, managed sections, latest source revision, and history count.
- Synchronize managed record: `SYNCED` through the real PRIME Documentation path; managed content and operator-owned content remained separate.
- History: first UI action returned `BOUND`; repeated same-period action returned `BOUND` without a duplicate page. Persistent state re-read after Core restart showed three history pages and preserved history identity.
- Attach source: existing approved child page attached through the UI under binding `continuation-076-ui-source`.
- Refresh source: returned `CURRENT` with project/source/page identity, observed revision, content hash, and provenance. Raw source content was not exposed as current authoritative state.
- Detach/retract: explicit UI confirmation returned `DETACHED`, `RETRACTED`, and `purged: NO`; the UI stated PRIME does not delete the external Notion page.
- Reconcile after detach: returned `BOUND` and preserved the source as `DETACHED / RETRACTED / purged NO`; it did not reactivate the source.
- Conflict boundary: existing Continuation 075 live conflict refusal/recovery evidence remains the source basis; the operator sync/reconcile controls are now exposed in the real UI and do not overwrite operator-owned content.
- Browser console after a clean buffer: no console errors.
- Core restart/recovery: service restart produced a new MainPID/start time; browser re-authenticated and the same project/record/history/source state remained available.

## Defects repaired during qualification

### Detached source reactivation

- Observed failure: the first real UI reconcile action refreshed a previously detached source and changed its persisted status to `ATTACHED` while public retrieval still said `RETRACTED`.
- Root cause: reconcile did not skip detached source bindings, and refresh did not enforce the retraction boundary.
- Minimal repair: `606de3927ad723059ad4843db5a7d441b719bd40` makes detached refresh return `RETRACTED` and makes reconcile preserve detached bindings.
- Requalification: UI detach followed by UI reconcile preserved `DETACHED / RETRACTED / purged NO`.

### Persisted history idempotence

- Observed failure: after a same-period history page already existed durably, the long-lived operator route retried external page creation and returned a generic action failure instead of returning the existing history.
- Root cause: the operator route did not short-circuit a persisted same-period history record before the external create path.
- Minimal repair: `c687ad619d87e5ace9d37e9ad7c202bc3760fed1` returns the existing persisted history with `idempotent: true`.
- Requalification: after rebuilding/restarting final3, the real UI history action succeeded and a repeated action remained idempotent.

## Governed result

The complete applicable operator surface is now qualified against the approved persistent Notion resource. The following frozen rows are promoted to `USER_USABLE_VERIFIED` in the product audit and removed from the open burndown: DOD-034, DOD-035, DOD-036, DOD-064, DOD-065, and DOD-066. R-037 through R-041 remain `VERIFIED`; the three governed views now agree on the Notion lifecycle boundary. No unrelated row was promoted.

## Validation

- Focused Notion/UI suite: `14 passed, 1 skipped`.
- Full regression: `110 passed, 28 skipped`.
- Compileall: `PASSED`.
- Git diff check: `PASSED`.
- Governance validation `--mode ADOPTED`: `PASSED`.
- Product burndown validation: `PASSED`; 81 audit rows, 56 complete, 25 open, work-class totals `LOCAL_CODE=5`, `LOCAL_BROWSER_QUALIFICATION=12`, `EXTERNAL_ENVIRONMENT=8`.
- Persistent Core readiness and image provenance: `PASSED`.
- Browser operator workflow and restart recovery: `PASSED`.
- Bare host Python full-suite attempt: `NOT APPLICABLE` as a product result; it lacked the repository's `.venv` dependencies and failed collection on missing `psycopg`. The supported Atlas `.venv` regression above passed.
- Deployment/public exposure: `NOT PERFORMED`.

## Remaining boundaries

- PRIME runtime Notion qualification is no longer blocked for the approved sandbox path; no raw credential is governed.
- DOD-005 remains parked.
- Remaining external/provider/legitimate-target gaps, DOD-081, and R-056 remain open or gated.
- Phase 15 and V1 remain incomplete; Phase 16 and external deployment were not created or performed.

## Publication

- Final governed commit: recorded in the publication closeout report and verified against origin/main.
