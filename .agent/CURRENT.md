# Current State

## Lifecycle

- Status: `ADOPTED`
- Last updated: 2026-08-14T22:10:00-04:00

## Active state after adoption

- Local directive ID: D-PRIME-PHASE15-V1-RESTORATION-BOUNDED-LOCAL-QUALIFICATION-057
- External directive ID: ANIMUS PRIME - Phase 15 Continuation 057
- Objective: Correct qualification provenance, preflight DOD-005 against the real Qualification Project without unsafe mutation, and harvest safe local product qualification evidence.
- Current status: `PARTIAL`
- Acceptance: PARTIAL; DOD-005 preflight hard-stopped truthfully with no safe reversible candidate, browser wave is limited by unavailable current operator credentials, and R-056 remains gated.
- Current phase: RESTORATION_BOUNDED_LOCAL_QUALIFICATION_057
- Expected or actual touched areas: Core/Node trust lifecycle; persistent Atlas Node service; private Core/UI runtime; browser operator journey; recovery-secret guard; evidence and governed records
- Immediate next action: use the approved secure operator credential path to resume authenticated local browser qualification, or keep those clauses open; keep DOD-004/DOD-039/DOD-050/DOD-053 parked and do not start R-056 prematurely.

## Temporary task-relevant facts

- Baseline PRIME-SPEC-V1.0.0; authoritative execution is direct SSH/native Atlas at /home/sketch/Projects/ANIMUS_PRIME; disposable resources: none.
- Persistent PostgreSQL and Hindsight are approved and reused; PRIME Core/UI now runs privately at `127.0.0.1:18000` under user systemd.
- DOD-030, DOD-061, and DOD-063 regression guards passed and remain preserved.
- DOD-008 bounded recovery/step-up is USER_USABLE_VERIFIED; DOD-009 backup/privacy is PRODUCT_VERIFIED; DOD-005 remains BACKEND_ONLY; DOD-006 current topology, DOD-039, DOD-004, DOD-050, DOD-053, DOD-074, R-045, and R-056 remain open or bounded; DOD-045, DOD-028, DOD-037, and DOD-038 remain PRODUCT_VERIFIED under Continuation 049.
- Continuation 050 implementation commit: `b6c94b7378966d42912277e6c861c3cd75f4846c`; persistent project/repository IDs remain stable and no disposable or alternate repository was created.
- Continuation 053 runtime image/service is private and restart-recovered; Continuation 055 now runs the canonical Node through a user-systemd mTLS service at `127.0.0.1:18001`.
- Continuation 054 added and exercised a loopback-only platform-local recovery secret path; the same operator identity was retained, credentials rotated, prior sessions revoked, and replacement references stored mode `0600` outside Git.
- Continuation 054 authenticated the Qualification Project through the real Core-served UI; Search, Ask, Goal, Progress, Repository, Authority, Memory, Knowledge, Evidence, Activity, Brain, Time Lens, AI Connections, and Settings states were inspected without promoting incomplete requirements.
- Continuation 051 parks DOD-039 pending a naturally available alternate location; no further DOD-039 implementation is authorized by this directive.
- Continuation 055 preserves the canonical Node identity `node-041-atlas-native`, uses persistent trust material outside Git, and keeps public ingress, deployment, Phase 16, and parked qualification work out of scope.

## Last validation after adoption

- Command or check: Continuation 055 mTLS lifecycle, browser healthy/offline/recovery journey, trust-chain checks, focused regression, governance, and persistent runtime checks
- Result: PASSED

## Risks

- DOD-008 local recovery is now USER_USABLE_VERIFIED for the bounded loopback/platform-local recovery and recent step-up path; raw credential material remains outside Git and project records.
- No experimental branch was treated as canonical; canonical ref is explicit and graph-derived. DOD-039 logical continuity and stale-preflight controls are implemented, but no legitimate alternate candidate existed for a real cutover.
- DOD-004 has durable step/resource/replay primitives and CREATE_REPOSITORY checkpointing; provider/fork/restore/archive conversions and full interruption qualification remain open.
- Approved model, live Notion workflow, approved Hindsight Reflect/Mental Models, native Windows, and second-device/provider boundaries remain unavailable or unqualified.

## Blockers

- DOD-005 direct persistent mutation qualification, approved model, live Notion projection, Hindsight Reflect/Mental Models, native Windows, and required second-device/provider boundaries remain unavailable or unqualified; R-056 remains gated.

## Pending decisions

- Continuation 057: the real Qualification Project is bound to `/home/sketch/Projects/ANIMUS_PRIME` and `node-041-atlas-native`; its current sources are authority records only. No safe existing non-authority source with a supported reversible retraction/restoration path was found, so DOD-005 remains BACKEND_ONLY without mutation. The live UI exposes protected entry, but the prior operator credential is not available in this run and no credential rotation was performed.

- DOD-005 now propagates evidence retraction to current source references, linked memory, evidence-backed Progress views, and current Documentation projection state while preserving historical projection provenance; direct qualification remains open.
- DOD-074 persisted project/history/Progress reads remain available with the canonical Node offline, while Node-required repository inspection fails closed and returns after service recovery; the exercised operator boundary is now qualified.


## Status vocabulary

ADOPTED is the repository governance lifecycle state. COMPLETE means the current directive is closed for its bounded scope and awaiting reset. PARTIAL records bounded acceptance with explicit remaining gaps.
