# Phase 15 remediation queue — Continuation 008

Baseline: `PRIME-SPEC-V1.0.0`  
Governed implementation/evidence checkpoint: `7b5ef0a` / `342fc58`
Observed qualification: `47 passed` on clean disposable PostgreSQL; external recovery obligations remain partial
Deployment: `NOT PERFORMED`  
V1: `FAIL`

The buckets below distinguish implementation work from qualification prerequisites. A requirement may appear in both B and C: implementation must converge locally while its final status remains open until its native/live environment is exercised.

## A — can close now

R-042–R-050 local implementation boundaries are now complete. Their qualification remains `partial` until the external/full-system evidence obligations run.

## B — implementation incomplete

Seventeen rows remain in implementation work; R-042–R-050 are implementation-complete but still await qualification:

- R-031–R-034 — native Node/control-plane lifecycle and packaging.
- R-035–R-036 — remote-access safety and Serve lifecycle.
- R-037–R-041 — Notion provider lifecycle and managed-history behavior.
- R-051–R-053 — complete browser operator experience and accessibility/degraded states.
- R-054–R-055 — approved provider/profile AI behavior, privacy, citations, injection, and isolation.
- R-056 — aggregate fresh-install end-to-end qualification.

Continuation 007 closed the R-046–R-050 local implementation cluster with explicit Evidence storage/lifecycle/parser states, durable citation mutation semantics, append-only historical snapshots, actual PostgreSQL checkpoint registration, retained bundle reconstruction, historical Ask/Brain, and Return to Now. These rows are implementation-complete but only partially qualified; this is not a VERIFIED result.

Continuation 008 closed the R-042–R-045 local recovery/capacity cluster with authenticated continuity backups, clean restore workflow state, component fidelity labels, managed Evidence/Git payload restoration, persisted schedules, reference-aware retention, queue backpressure, coalescing helpers, and disk health. These rows are implementation-complete but only partially qualified; this is not a VERIFIED result.

## C — external qualification required

The following exact prerequisites remain unavailable or unexercised:

- R-031–R-033 — native Linux service/reboot evidence and a native Windows service host; Linux containers cannot substitute for Windows.
- R-034 — qualified private Core↔Node control-plane deployment and upgrade compatibility run.
- R-035–R-036 — signed-in Tailscale tailnet plus approved second device and real Serve/Funnel state.
- R-037–R-041 — controlled live Notion workspace/token, managed/user regions, Knowledge Source, and provider fault injection.
- R-042–R-045 — genuinely separate off-machine target, populated clean-install/destructive safety drill, live Hindsight loss/rebuild, interrupted restore, sustained capacity/disk-pressure harness, and complete schedule failure/recovery evidence.
- R-046–R-050 — live/long-running Evidence and parser/index, product-surface citation, complete State A/B/C/D historical walkthrough, backup/restore, and browser/live isolation evidence.
- R-051–R-053 — running qualified Core/Web instance and supported desktop/mobile browser acceptance contexts.
- R-054–R-055 — approved AI provider/model/profile, frozen configuration revision, usage/cost capture, and isolated Project A/B fixtures.
- R-056 — every prerequisite above plus a fresh-install environment.

Deterministic procedures for each C item are recorded in [`phase15-qualification-procedures.md`](phase15-qualification-procedures.md). The procedures are plans, not evidence.

## Current counts

The ledger currently reports `implementation_complete=9/26`, `IMPLEMENTING=17`, `OPEN=26`, `BLOCKED=0`, `VERIFIED=0`; therefore `VERIFIED / 26 = 0/26`. `BLOCKED=0` is intentional: exact external prerequisites are recorded as qualification blockers rather than used to halt local progress.
