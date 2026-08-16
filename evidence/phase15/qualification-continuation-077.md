# ANIMUS PRIME — Phase 15 Qualification Continuation 077

Status: `PARTIAL` — DOD-021 Ask and DOD-022 Unified Search remain unqualified.

Date: 2026-08-16

## Scope and acceptance

This continuation was limited to requalifying the real authenticated persistent PRIME Ask and Unified Search surfaces against the existing Qualification Project and the existing persistent Atlas services. No product source, runtime image, Hindsight data, Notion credential, PARAGON configuration, external page, synthetic target, or public exposure was changed.

The bounded runtime preconditions passed, but the live product did not satisfy the complete frozen Ask or Search contracts. No DOD/R promotion is justified.

## Baseline and repository state

- Frozen specification: `PRIME-SPEC-V1.0.0`
- Starting governed HEAD: `5737cbbe260d39c0896e22c3ef93150363272ea0`
- Starting `origin/main`: `5737cbbe260d39c0896e22c3ef93150363272ea0`
- Starting worktree: tracked tree clean; existing untracked `.codebase-memory/`, `.prime-evidence/`, and `.vscode/` preserved.
- Qualified PRIME implementation: unchanged, Core build commit `c687ad619d87e5ace9d37e9ad7c202bc3760fed1`.
- Final governed HEAD: recorded by the publication closeout and Git parity checks for this evidence-only continuation.

## Persistent Atlas runtime

- Canonical checkout: `/home/sketch/Projects/ANIMUS_PRIME`; all runtime actions used direct Atlas SSH/native execution.
- PostgreSQL: existing persistent `animus-prime-phase0-postgres-1`, preserved and healthy.
- Hindsight: existing persistent `mimir-hindsight-production`, preserved; existing PRIME bank reused.
- Repository Node: existing enrolled Node and project binding preserved; no new Node created.
- PRIME Core: existing persistent Docker service `animus-prime-core`, image `animus-prime-core:continuation-076-final3`; private listener `127.0.0.1:18000`; live and ready health passed.
- Core readiness reported spec `PRIME-SPEC-V1.0.0`, schema `0036_operator_workflows.sql`, and build commit `c687ad619d87e5ace9d37e9ad7c202bc3760fed1`.
- PARAGON: existing `paragon.service` remained active with its established private health check passing; no PARAGON change was made.
- Public exposure: not performed; private/local boundary preserved.

## Browser and authentication

- Browser: Chromium through the required gstack `/browse` workflow.
- Interface: `http://127.0.0.1:28000/`.
- Trusted-host sign-in: passed through the existing approval flow; no raw credential was printed or recorded.
- Existing Qualification Project: `project_d9a1a5b609394282b62fc12c0d04634d`.
- Project selection: passed.
- Reload/session persistence: passed; the authenticated UI returned to the selected project with `NORMAL / Qualification Project`, `ACTIVE`, `ONLINE`, and freshness `CURRENT`.
- Browser console after reload: clean; no console errors observed.

## Notion source lifecycle used for the qualification

The existing approved source page `3be833cb-27ff-81aa-9fe2-ffb4fcf5f980` was attached through the real PRIME UI under binding `continuation-077-search-source`, refreshed, and then explicitly detached again. The refresh returned `CURRENT` with project/source/page/block identity, observed revision `201100000`, and content hash `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. The source content response was honestly `NO CONTENT RETURNED`; no external deletion was claimed. After detach the UI showed `DETACHED / RETRACTED / purged NO`, and a search for the page identity returned no Notion result. This retraction/exclusion behavior passed, but it does not qualify positive Notion search indexing.

## DOD-022 — Unified Search

### Passed bounded behavior

- Authenticated Search was exercised through the persistent UI.
- Repository results were returned for `notion_service.py` and `AGENTS.md`.
- Memory results were returned and remained project-scoped by the API path.
- Direct authenticated API inspection for `AGENTS.md` returned grouped counts: Repository `2`, Authority `0`, Git `0`, Notion Knowledge `0`, Activity `0`, Progress `0`, Memory `8`, Evidence `0`.
- The explicitly detached/retracted Notion source was excluded from Search results. This is a real lifecycle safety result.

### Failed frozen acceptance behavior

- No positive Git result was available for the existing Qualification Project. The persistent Git checkpoint table contained rows globally, but none for this project; no checkpoint was created solely for qualification.
- No positive Notion Knowledge result was returned for the attached/refreshed approved source. The existing Notion lifecycle state is not indexed into the Search database path used by this surface.
- A unique no-result query `prime-no-result-077-9f2c` returned eight unrelated Memory hits, including scores down to `0.1216`, instead of an empty/no-result state. This is unsound no-result behavior.
- Complete grouped-source freshness, revision display, drill-down, and Project A/B isolation were therefore not established.

Result: `DOD-022` remains `IMPLEMENTED_NOT_PRODUCT_QUALIFIED`; mapped `R-047` remains open.

## DOD-021 — Project-scoped Ask

### Passed bounded behavior

- Authenticated Ask was exercised through the real UI/API path with the UI-supplied CSRF header.
- The approved PARAGON provider executed the requests; the AI run reported `SUCCEEDED`, provider/model `paragon`, and privacy mode `LOCAL_ONLY`.
- An unsupported question, `What is the private operator's favorite color?`, returned `UNKNOWN` without citations. The negative refusal boundary passed.

### Failed frozen acceptance behavior

- `What is the goal of ANIMUS PRIME?` returned `UNKNOWN` without citations.
- `What did Continuation 076 qualify?` returned `UNKNOWN` without citations.
- `What is the current ANIMUS PRIME Notion operator workflow status` returned stale unsupported prose referring to older Continuation 054/052 state, with citations to old memory material rather than the current qualified state.
- `What does AGENTS.md say about code exploration?` returned `UNKNOWN` without citations, showing that natural-language questions do not retrieve relevant repository content through the current source path.
- The implementation currently feeds Ask only Repository, Memory, and Evidence results; it does not include Authority, Git, Notion, Activity, or Progress groups in model sources. Repository matching is path-oriented rather than content-aware for these natural-language questions. Citation-bearing current-state answers were not produced.

Result: `DOD-021` remains `PARTIAL`; mapped `R-054` remains not promotable for this operator contract.

## Changes and repairs

- PRIME product source: no change.
- Runtime configuration/image: no change.
- PARAGON/Hindsight/Notion external state: no unrelated change; the approved Notion source was attached, refreshed, and explicitly detached as part of the bounded lifecycle test.
- Governance/audit/burndown/evidence/.agent records: updated to preserve the exact live result and current blockers.
- No implementation repair was made because closing both defects requires a distinct source-indexing/current-grounding behavior change that was outside a truthful qualification-only closeout.

## Validation

- Persistent Core health/readiness: `PASSED`
- Existing PARAGON private health: `PASSED`
- Existing PostgreSQL/Hindsight runtime preservation: `PASSED`
- Authenticated browser sign-in/project selection/reload: `PASSED`
- Browser console cleanliness: `PASSED`
- Notion refresh provenance: `PASSED`
- Notion detach/retraction and Search exclusion: `PASSED`
- Unified Search complete frozen contract: `FAILED`
- Ask complete frozen contract: `FAILED`
- Unique no-result behavior: `FAILED`
- Focused product tests: `NOT RUN` (no product code changed)
- Full product regression: `NOT RUN` (no product code changed)
- Compile/static checks: `NOT RUN` (no product code changed)
- Governance/burndown/diff/secret checks: run at publication closeout
- Deployment/public exposure: `NOT PERFORMED`

## Remaining governed state

- DOD-021: `PARTIAL`; repair current-state grounding, source selection, citation, and revision-aware Ask behavior, then requalify.
- DOD-022: `IMPLEMENTED_NOT_PRODUCT_QUALIFIED`; repair Search indexing/grouping/no-result filtering, then requalify grouped source freshness, drill-down, and isolation.
- DOD-005 remains parked as directed.
- DOD-081 and R-056 remain last/gated.
- Notion remains available for its already-qualified lifecycle, but its positive Search projection/index path is not qualified here.
- Phase 15 remains incomplete; V1 is not declared.
- No automatic Continuation 078 is authorized by this record.
