# Current State

## Lifecycle

- Status: `ADOPTED`
- Last updated: 2026-08-14T07:54:00-04:00

## Active state after adoption

- Local directive ID: D-PRIME-PHASE15-V1-FROZEN-AUTH-PROVENANCE-049
- External directive ID: ANIMUS PRIME - Continuation 049
- Objective: Reconcile the authentication boundary, establish canonical Git truth, preserve memory provenance, and close explicit authority migration paths.
- Current status: `COMPLETE`
- Acceptance: PARTIAL
- Current phase: CLOSED_PARTIAL
- Expected or actual touched areas: src/prime_core/git_provenance.py; src/prime_core/authority.py; src/prime_core/service.py; src/prime_core/memory_service.py; src/prime_core/mcp_service.py; apps/core/main.py; migration 0029; DOD audit/burndown/traceability; Continuation 049 evidence
- Immediate next action: Await the next accepted directive; preserve DOD-008/DOD-006/R-045/R-056 boundaries.

## Temporary task-relevant facts

- Baseline PRIME-SPEC-V1.0.0; authoritative execution is direct SSH/native Atlas at /home/sketch/Projects/ANIMUS_PRIME; disposable resources: none.
- Persistent PostgreSQL and Hindsight are approved; no persistent PRIME Core listener exists.
- DOD-030, DOD-061, and DOD-063 regression guards passed and remain preserved.
- DOD-008 recovery credential replay, DOD-006 current topology, DOD-039, DOD-004, R-045, and R-056 remain open or bounded; DOD-045, DOD-028, DOD-037, and DOD-038 are PRODUCT_VERIFIED under Continuation 049.

## Last validation after adoption

- Command or check: Continuation 049 direct qualification, governance reconciliation, persistent regression, storage, service health, full validation, and publication checks
- Result: PASSED

## Risks

- No recovery credential rotation was fabricated; DOD-008 remains PARTIAL and is not duplicated into DOD-045.
- No experimental branch was treated as canonical; canonical ref is explicit and graph-derived.
- Approved model, live Notion workflow, approved Hindsight Reflect/Mental Models, native Windows, and second-device/provider boundaries remain unavailable or unqualified.

## Blockers

- No persistent Core listener; approved model, live Notion, Hindsight Reflect/Mental Models, native Windows, and required second-device/provider boundaries remain unavailable or unqualified.

## Pending decisions

- None.


## Status vocabulary

ADOPTED is the repository governance lifecycle state. COMPLETE means the current directive is closed for its bounded scope and awaiting reset. PARTIAL records bounded acceptance with explicit remaining gaps.
