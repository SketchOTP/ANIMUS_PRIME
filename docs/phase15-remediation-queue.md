# Phase 15 remediation queue — Continuation 005

Baseline: `PRIME-SPEC-V1.0.0`  
Governed checkpoint: `9b1b2a8f257356f2d96a7bfb169fca9b73192794`  
Observed qualification: `24 passed, 15 skipped`  
Deployment: `NOT PERFORMED`  
V1: `FAIL`

The buckets below distinguish implementation work from qualification prerequisites. A requirement may appear in both B and C: implementation must converge locally while its final status remains open until its native/live environment is exercised.

## A — can close now

None. No R-031–R-056 row currently has both complete implementation and all required qualification environments available with captured evidence.

## B — implementation incomplete

All 26 rows remain in implementation work:

- R-031–R-034 — native Node/control-plane lifecycle and packaging.
- R-035–R-036 — remote-access safety and Serve lifecycle.
- R-037–R-041 — Notion provider lifecycle and managed-history behavior.
- R-042–R-045 — backup/restore, component continuity, and capacity controls.
- R-046–R-050 — Evidence, citations, historical reconstruction, Git checkpoint preservation, and historical Ask/Brain.
- R-051–R-053 — complete browser operator experience and accessibility/degraded states.
- R-054–R-055 — approved provider/profile AI behavior, privacy, citations, injection, and isolation.
- R-056 — aggregate fresh-install end-to-end qualification.

Continuation 005 implementation started with the R-046/R-047 Evidence boundary: safe metadata validation, project-scoped storage/listing/reference/retraction routes, and persisted parser/index status. This is implementation progress, not a VERIFIED result.

## C — external qualification required

The following exact prerequisites remain unavailable or unexercised:

- R-031–R-033 — native Linux service/reboot evidence and a native Windows service host; Linux containers cannot substitute for Windows.
- R-034 — qualified private Core↔Node control-plane deployment and upgrade compatibility run.
- R-035–R-036 — signed-in Tailscale tailnet plus approved second device and real Serve/Funnel state.
- R-037–R-041 — controlled live Notion workspace/token, managed/user regions, Knowledge Source, and provider fault injection.
- R-042–R-045 — off-machine target, populated state, clean restore environment, recovery key, and capacity harness.
- R-046–R-050 — qualified PostgreSQL, parser/index execution, multi-commit history fixtures, retained authority/progress/Notion/Hindsight revisions, and Git rewrite/prune/GC fixture.
- R-051–R-053 — running qualified Core/Web instance and supported desktop/mobile browser acceptance contexts.
- R-054–R-055 — approved AI provider/model/profile, frozen configuration revision, usage/cost capture, and isolated Project A/B fixtures.
- R-056 — every prerequisite above plus a fresh-install environment.

Deterministic procedures for each C item are recorded in [`phase15-qualification-procedures.md`](phase15-qualification-procedures.md). The procedures are plans, not evidence.

## Current counts

The ledger currently reports `IMPLEMENTING=26`, `OPEN=26`, `BLOCKED=0`, `VERIFIED=0`; therefore `VERIFIED / 26 = 0/26`. `BLOCKED=0` is intentional: the rows still have independent implementation work, while exact external prerequisites are recorded as qualification blockers rather than used to halt local progress.
