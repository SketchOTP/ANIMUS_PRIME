# Current State

## Lifecycle

- Status: `ADOPTED`
- Last updated: 2026-08-14T10:49:27-04:00

## Active state after adoption

- Local directive ID: D-PRIME-PHASE15-V1-REPOSITORY-REBIND-DURABLE-WORKFLOW-050
- External directive ID: ANIMUS PRIME - Continuation 050
- Objective: Reconcile topology-equivalence evidence, implement bounded logical repository rebind controls, and make durable workflow interruption/resume behavior explicit on persistent Atlas.
- Current status: `COMPLETE`
- Acceptance: PARTIAL pending final publication
- Current phase: CLOSED_PARTIAL
- Expected or actual touched areas: src/prime_core/git_provenance.py; src/prime_core/service.py; src/prime_core/workflow_primitives.py; apps/core/main.py; migration 0030; Continuation 050 qualification/evidence; DOD audit/burndown/traceability; append-only .agent records
- Immediate next action: Preserve the bounded DOD-006, DOD-039, DOD-004, DOD-005, DOD-008, DOD-009, R-045, and R-056 boundaries until a new accepted directive.

## Temporary task-relevant facts

- Baseline PRIME-SPEC-V1.0.0; authoritative execution is direct SSH/native Atlas at /home/sketch/Projects/ANIMUS_PRIME; disposable resources: none.
- Persistent PostgreSQL and Hindsight are approved; no persistent PRIME Core listener exists.
- DOD-030, DOD-061, and DOD-063 regression guards passed and remain preserved.
- DOD-008 recovery credential replay, DOD-006 current topology, DOD-039, DOD-004, R-045, and R-056 remain open or bounded; DOD-045, DOD-028, DOD-037, and DOD-038 remain PRODUCT_VERIFIED under Continuation 049.
- Continuation 050 implementation commit: `b6c94b7378966d42912277e6c861c3cd75f4846c`; persistent project/repository IDs remain stable and no disposable or alternate repository was created.

## Last validation after adoption

- Command or check: Continuation 050 direct qualification, governance reconciliation, persistent regression, storage, service health, and publication closeout
- Result: PASSED

## Risks

- No recovery credential rotation was fabricated; DOD-008 remains PARTIAL and is not duplicated into DOD-045.
- No experimental branch was treated as canonical; canonical ref is explicit and graph-derived. DOD-039 logical continuity and stale-preflight controls are implemented, but no legitimate alternate candidate existed for a real cutover.
- DOD-004 has durable step/resource/replay primitives and CREATE_REPOSITORY checkpointing; provider/fork/restore/archive conversions and full interruption qualification remain open.
- Approved model, live Notion workflow, approved Hindsight Reflect/Mental Models, native Windows, and second-device/provider boundaries remain unavailable or unqualified.

## Blockers

- No persistent Core listener; approved model, live Notion, Hindsight Reflect/Mental Models, native Windows, and required second-device/provider boundaries remain unavailable or unqualified.

## Pending decisions

- None.


## Status vocabulary

ADOPTED is the repository governance lifecycle state. COMPLETE means the current directive is closed for its bounded scope and awaiting reset. PARTIAL records bounded acceptance with explicit remaining gaps.
