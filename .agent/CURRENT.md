# Current State

## Lifecycle

- Status: `ADOPTED`
- Last updated: 2026-08-15T00:00:00-04:00

## Active state after adoption

- Local directive ID: D-PRIME-PHASE15-SAFE-PRODUCT-WAVE-059
- External directive ID: ANIMUS PRIME - Phase 15 Continuation 059
- Objective: Establish spec-compliant trusted-host local identity sign-in and step-up authentication on the existing persistent Atlas PRIME installation, then resume the real browser operator journey.
- Current status: `COMPLETE`
- Acceptance: PARTIAL; trusted-host sign-in, step-up, negative security cases, persistent service restart, and the real protected browser journey passed, while DOD-005, the remaining local queue, external boundaries, and R-056 remain open.
- Current phase: AUTHENTICATED_LOCAL_BROWSER_QUALIFICATION_059
- Expected or actual touched areas: Core Usage/Backup/Metadata surfaces; responsive UI polish; browser qualification; persistent image/service; evidence and governed records
- Immediate next action: close the remaining locally actionable safe wave, keep DOD-005 parked and R-056 gated, then reassess only the still-open exact clauses.

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
- Continuation 058 implementation commit: `8c881256b6a0164cfef9ae411eb404107ac5c3c0`; the existing single operator now has a separate host-held local identity secret, stored only as a digest in Core state, with short-lived SIGN_IN and STEP_UP challenge/approval/redeem flows.
- Continuation 058 qualified the real persistent Core/UI path: trusted-host sign-in and 300-second step-up succeeded; missing/wrong host-secret approval returned 401; consumed challenge replay returned 401; Core restart preserved authenticated project identity, Progress, repository binding, and Node state.

- Continuation 059 active image: animus-prime-core:continuation-059-ui under animus-prime-core.service; prior persistent images/containers are inactive rollback artifacts. Existing PostgreSQL, Hindsight, canonical Node, state mount, and private listeners were preserved.
- Continuation 059 browser evidence: Usage renders project-scoped records with truthful unavailable limits/cost states; Backup renders the existing verified continuity record and encryption version; Project Settings provides a real metadata form.
- Continuation 059 metadata evidence: name, description, image URL, canonical project ID, Node, and repository path persisted through Core restart and were restored exactly to the original governed values.
- Continuation 059 status: DOD-026, DOD-027, DOD-047, and DOD-049 are PARTIAL; DOD-056 is USER_USABLE_VERIFIED; DOD-048 remains shell-only; DOD-005 remains BACKEND_ONLY. The 375px browser check passes without horizontal overflow and keyboard Tab shows visible focus.

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

- Continuation 057: the real Qualification Project is bound to `/home/sketch/Projects/ANIMUS_PRIME` and `node-041-atlas-native`; its current sources are authority records only. No safe existing non-authority source with a supported reversible retraction/restoration path was found, so DOD-005 remains BACKEND_ONLY without mutation.

- Continuation 058: the approved recovery path provisioned a separate local identity without reading or changing the operator password. The browser never receives the host secret; Atlas-only approval redeems into ordinary PRIME session/CSRF state. External Notion, model, Hindsight Reflect/Mental Models, Windows, second-device, and provider boundaries remain truthful degraded/unavailable states.

- DOD-005 now propagates evidence retraction to current source references, linked memory, evidence-backed Progress views, and current Documentation projection state while preserving historical projection provenance; direct qualification remains open.
- DOD-074 persisted project/history/Progress reads remain available with the canonical Node offline, while Node-required repository inspection fails closed and returns after service recovery; the exercised operator boundary is now qualified.


## Status vocabulary

ADOPTED is the repository governance lifecycle state. COMPLETE means the current directive is closed for its bounded scope and awaiting reset. PARTIAL records bounded acceptance with explicit remaining gaps.
