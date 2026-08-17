# Current State

## Lifecycle

- Status: `ADOPTED`
- Last updated: 2026-08-17T00:00:00-04:00

## Active state after adoption

- Local directive ID: D-PRIME-PHASE15-SHARED-RETRIEVAL-GROUNDING-REPAIR-078
- External directive ID: ANIMUS PRIME - Phase 15 Continuation 078
- Objective: Repair the shared retrieval/grounding boundary used by PRIME Unified Search and Ask.
- Current status: `IN_PROGRESS`
- Acceptance: Promote DOD-021 and DOD-022 independently only if their complete frozen operator contracts pass; otherwise preserve exact defects.
- Current phase: SHARED_RETRIEVAL_GROUNDING_REPAIR_078
- Expected or actual touched areas: Repository search projection, canonical Git reads, Notion Search projection, PRIME-side Memory relevance filtering, shared retrieval hits, Ask source admission/citations, focused tests, persistent runtime, browser requalification, and governed records. No unrelated infrastructure or public exposure.
- Immediate next action: Complete the bounded repair, rebuild/restart the existing persistent Core, reindex the existing Qualification Project, and requalify Ask/Search independently.

## Temporary task-relevant facts

- Baseline PRIME-SPEC-V1.0.0; authoritative execution is direct SSH/native Atlas at /home/sketch/Projects/ANIMUS_PRIME; disposable resources: none.
- Starting PRIME state for Continuation 075 was 92e05b5199ea3901d92a1f83902cede0e0bc63e5; no PRIME source change occurred in this continuation.
- Persistent PostgreSQL, Hindsight, PRIME Core/UI, and canonical Node remain preserved. Hindsight remains healthy on 127.0.0.1:8888; the existing Hindsight image and PRIME bank were reused.
- Existing PRIME bank prime-project_d9a1a5b609394282b62fc12c0d04634d contains exactly one legitimate Mental Model, prime-operating-model, with substantive generated content and stored provenance.
- Exact 072 Reflect query remains the accepted source basis from Continuation 073: four native observation/recall calls and substantive provenance-bearing output. Continuation 074 created the model through the supported Hindsight operation.
- Runtime image identity is continuation-076-final3; persistent Core build commit c687ad619d87e5ace9d37e9ad7c202bc3760fed1; the approved runtime Notion credential remains available only through Atlas secure configuration; no synthetic target, deployment, public exposure, Funnel change, or Phase 16 occurred.
- Approved Notion sandbox parent is `3be833cb-27ff-814f-af89-ebfc3a2a8aed`; project record page is `3be833cb-27ff-8159-add6-e883c1cc54af`; controlled probe child is `3be833cb-27ff-81aa-9fe2-ffb4fcf5f980`.
- Runtime Notion capability read/write, production adapter lifecycle, and the complete persistent browser projection/conflict/detach/history operator surface passed. DOD-034/035/036/064/065/066 are USER_USABLE_VERIFIED; detached sources remain RETRACTED and history is idempotent after restart.
- Untracked .codebase-memory/, .prime-evidence/, and .vscode/ remain preserved.

## Last validation after adoption

- Command or check: Continuation 075 runtime Notion credential, approved sandbox capability, product API, adapter lifecycle, and browser status
- Result: `PASSED`

## Risks

- Current Hindsight Reflect tool-capable provider availability; PRIME operator-visible Notion lifecycle; R-045/DOD-047; legitimate targets; DOD-005; DOD-081; R-056; Phase 15/V1.

## Blockers

- ATLAS_PARAGON_SERVICE_RESTART_REQUIRES_INTERACTIVE_AUTH: RESOLVED by operator restart; new MainPID 607574 and private health verified.
- PRIME_RUNTIME_NOTION_CREDENTIAL_UNAVAILABLE: RESOLVED for the approved bounded credential path; raw token remains Atlas-only and is not governed data.
- PRIME_RUNTIME_NOTION_OPERATOR_WORKFLOW_UNQUALIFIED: RESOLVED by Continuation 076 persistent browser qualification and minimal lifecycle/idempotence repairs.

## Pending decisions

- Runtime Notion credential and backend lifecycle remain qualified; Ask/Search require an explicit repair directive and must not be treated as automatically continued.
- Keep the qualified Notion lifecycle preserved, DOD-005 parked, DOD-081/R-056 last, and Phase 16/deployment out of scope.

## Status vocabulary

ADOPTED is the repository governance lifecycle state. COMPLETE means the current directive is closed for its bounded scope and awaiting reset. PARTIAL records bounded acceptance with explicit remaining gaps.
