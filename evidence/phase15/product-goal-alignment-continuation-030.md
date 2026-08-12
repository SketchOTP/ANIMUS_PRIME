# ANIMUS PRIME — Continuation 030 Evidence

Date: 2026-08-12
Baseline: `PRIME-SPEC-V1.0.0`
Authoritative checkout: `/home/sketch/Projects/ANIMUS_PRIME`
Parent implementation/evidence tip: `0273f07682461e9795bbd469fbd7cbd13f5364de`
Status: `PARTIAL`

## Scope

Continuation 030 is the V1 Product Completion Wave 2 for zero-to-managed-project onboarding and a replacement AI-coder handoff. It must preserve truthful external/environment boundaries and must not change the frozen baseline, create Phase 16, deploy, or close R-056.

## Wave-1 audit reconciliation

- DOD-042 was stale at `MISSING`. The existing Continuation 029 export was rechecked against the frozen clauses and now includes a documented schema/version, generated freshness timestamp, canonical repository revision, source revisions, explicit claim provenance, degraded/unknown markers, no-store operator download responses, Markdown and JSON formats, redaction, and Project A/B isolation evidence. It is now `USER_USABLE_VERIFIED` in `docs/v1-product-goal-alignment-audit.yaml`.
- DOD-022, DOD-040, DOD-041, DOD-043, DOD-044, and DOD-054 through DOD-060 plus DOD-062 and DOD-063 were updated from stale shell/backend wording to precise `IMPLEMENTED_NOT_PRODUCT_QUALIFIED` gaps where Continuation 029 or this implementation now supplies real behavior. No row was promoted without complete product qualification.

## Implementation completed in this run

- `apps/core/main.py` now exposes setup status with truthful `READY`, `DEGRADED`, and `REQUIRES_ACTION` states, durable resume guidance, project metadata update, Node-constrained repository inspection/registration, approved-root new repository creation, explicit authority bootstrap/adopt/review boundaries, and onboarding state.
- `src/prime_core/service.py` adds persistent metadata, path/root/Git/duplicate validation, non-bare repository creation through a durable workflow with `REPAIR_REQUIRED` on post-directory failure, explicit authority bootstrap protection, existing-authority adoption, and explicit approved goal write-through to `.agent/PROJECT_GOAL.md`.
- `src/prime_core/indexer.py` marks the project `ACTIVE` with truthful `AWAITING_BASELINE` state after the initial repository observation. It does not fabricate progress percentages or GoalModel completion.
- `migrations/prime/0025_product_onboarding.sql` adds project description/image and resumable onboarding state.
- `apps/web/index.html` now exposes setup status, Node/project onboarding mode selection, explicit existing/new repository flow, authority bootstrap boundary, and reviewed goal approval form.
- `_git_state` now reports an initialized repository without a first commit as `UNBORN`, distinct from an unavailable repository, so the replacement-coder handoff does not overstate Git history.

## Validation so far

- In-process Python compile: `PASSED` (avoids SSHFS `__pycache__` permission failure).
- Focused product/export regression: `PASSED` — 62 passed, 25 skipped.
- Product plus Node regression: `PASSED` — 186 passed, 75 skipped.
- §26 structural audit: `PASSED` — 81 items; status counts are `BACKEND_ONLY=33`, `BLOCKED_BY_ENVIRONMENT=1`, `IMPLEMENTED_NOT_PRODUCT_QUALIFIED=19`, `MISSING=0`, `PARTIAL=8`, `PRODUCT_VERIFIED=7`, `UI_SHELL_ONLY=9`, `USER_USABLE_VERIFIED=4`; V1 gate remains `FAIL`.
- Browser qualification of the new Wave-2 onboarding flow: `PASSED` — authenticated fresh-DB browser session showed setup readiness/degradation states, rejected a parent outside enrolled Node roots, created a non-bare repository under the approved root, bootstrapped `authority-template/v1`, approved the reviewed goal, requested initial indexing, and displayed truthful `UNKNOWN` progress / `AWAITING_BASELINE` state.
- Fresh-database end-to-end onboarding and negative matrix: `PASSED` — disposable `prime_product_030`; direct persistence confirmed `CREATE_REPOSITORY` `SUCCEEDED`, repository `UNBORN`/branch `main`, authority `VALID`, approved GoalRevision 1, and onboarding `BASELINE` / `AWAITING_BASELINE`.
- Context export and isolation: `PASSED` — JSON and Markdown returned 200 with download dispositions, provenance, `UNBORN`, redaction, and no Project B marker; final browser console had no errors after the expected negative-path 400 was cleared.
- Governed-view reconciliation: `PASSED` — requirements traceability records R-042/R-052 as `VERIFIED` and R-056 as `IMPLEMENTING`; the remediation matrix and qualification ledger agree at 16 `VERIFIED`, 9 implementation-open, and R-056 `OPEN`.
- Governance/publication/Notion reconciliation: `PASSED` at run close; the governed commit was published with local/origin parity and the Continuation 030 result was appended to the authoritative Notion qualification page without credential material.

## Known remaining gaps

- DOD-044/054/055/056/057/058 are implemented but not yet promoted pending fresh browser, restart/resume, negative-path, and authority/GoalModel qualification.
- The fresh browser run qualifies the primary onboarding path and allowed-root rejection, but does not yet establish interrupted restart/resume recovery or the complete GoalModel-bound progress workflow; these rows remain `IMPLEMENTED_NOT_PRODUCT_QUALIFIED`.
- GoalModel baseline and initial evidence-backed progress remain intentionally `AWAITING_BASELINE`; no random percentage is generated.
- DOD-041 still lacks root/nested `AGENTS.md` chain inventory and visible precedence/conflict handling.
- DOD-043 still lacks activity filters and source drill-down.
- DOD-040 still lacks complete operator rotation/revocation qualification.
- Hindsight retain, native Node lifecycle, private second-device Tailscale, external assistive technology, R-044, R-053, and R-056 remain unresolved.
- Deployment remains `NOT PERFORMED`.
