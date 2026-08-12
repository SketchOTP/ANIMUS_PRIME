# ANIMUS PRIME Phase 15 Qualification — Continuation 024

Date: 2026-08-12
Baseline: `PRIME-SPEC-V1.0.0`
Authoritative environment: native Atlas `/home/sketch/Projects/ANIMUS_PRIME`
Execution mode: disposable PostgreSQL/pgvector, native Docker/Compose, native Python, Chromium through a bounded local proxy to Atlas Core

## Fresh baseline and regression

- Native compile: `PASSED` (`.venv/bin/python -m compileall -q apps src scripts tests`).
- Fresh PostgreSQL/pgvector reset: `PASSED`; the exact anonymous qualification volume was removed and recreated.
- Full regression: `PASSED` — `86 passed`.
- Phases 1–14: `PASSED`.
- Governance before qualification publication: `PASSED`.
- Phase 15/V1 aggregate: `FAILED` truthfully at `10/26 VERIFIED`; R-056 remains `OPEN`.
- The recurring Windows-side `distutils-precedence.pth` warning is host Python noise from the SSH wrapper; native Atlas qualification completed successfully.

## Minimal defects repaired

1. `src/prime_core/reliability_service.py` cast the exponential retry value to integer before PostgreSQL `make_interval`, fixing scheduled retry result recording on the approved PostgreSQL version.
2. `apps/core/main.py` now returns bounded `404 PROJECT_NOT_FOUND` for invalid project Search and Ask routes instead of empty Search success and an unhandled Ask `500`.

No architecture, baseline, deployment, canonical Notion content, or protected worktree entries were changed.

## R-042 — VERIFIED

Native `scripts/phase15_qualify_continuation_024.py` passed the complete remaining scheduled matrix against `/mnt/storage1tb` on the independent `/dev/sdb1` target:

- durable schedule configured and observed after an actual Core restart;
- scheduled off-machine backup succeeded and was recorded `VERIFIED`;
- only the disposable qualification destination was made unavailable;
- the scheduled attempt recorded `FAILED`, with retry count `1` and one durable retry job;
- the previous known-good backup remained present and `VERIFIED`;
- the destination was restored, retry/subsequent backup succeeded, and schedule health returned `VERIFIED` with retry count reset to `0`;
- six backup generations were exercised; retention removed only disposable candidates and retained the latest known-good generation;
- wrong-key, tamper, truncation, and credential-exclusion negative coverage passed in the focused backup tests;
- no credential value was written to the schedule, manifest, evidence, or database state.

Decision: `R-042 = VERIFIED`, `remaining_gap = NONE`.

## R-043 — PARTIAL

The existing focused qualification passed clean-install restore identity, managed Evidence hash/source-reference preservation, restore workflow completion, populated-target destructive safety checkpoint, and deterministic interrupted restore (`REPAIR_REQUIRED`). The focused backup matrix also passed wrong-key, tamper, truncation, and secret-exclusion checks.

Remaining exact gap: one complete representative state has not yet been assembled and restored across every required class in the directive, including retained Git checkpoint, historical revisions, Notion binding/projection metadata, AI run/usage metadata, memory corrections/tombstones, ordinary populated-target collision refusal, approved step-up impact presentation, and the full interrupted resume/repair/rollback story.

Decision: `PARTIAL`.

## R-044 — PARTIAL

The existing approved Hindsight backend was reached through PRIME's existing `PrimeMemoryAdapter` boundary. Health, disposable bank creation, project-bank isolation, bank deletion/recreation, and transport-unavailable degradation all passed. The backend's memory retain operation returned `UNAVAILABLE` in this environment, so durable retained/recalled memory could not be promoted. PRIME's source-ledger rebuild label remains distinct from exact backend restore.

Remaining exact gap: successful durable Hindsight retain/recall plus full outage/recreation/source-ledger rebuild evidence preserving corrections and tombstones.

Decision: `PARTIAL`.

## R-045 — PARTIAL

The focused capacity qualification passed 256-event burst handling, queue cap/refusal, Evidence quota refusal, disk warning, canonical-write prioritization, and health recovery. The fresh run also passed the existing reliability and qualification tests.

Remaining exact gap: sustained parser concurrency saturation, indexing backlog, retention pressure, stale-job protection, provider-independent usage/cost bounds, and recorded sustained-duration recovery metrics.

Decision: `PARTIAL`.

## R-048 — PARTIAL

The governed A/B/C/D fixture passed exact repository, authority, Goal/Progress, Evidence, Notion projection, Git checkpoint, historical Ask, historical Brain, missing-Evidence `PARTIAL`, restored-Evidence `EXACT`, and Return-to-Now behavior. Later revisions were excluded from earlier historical contexts.

Remaining exact gap: independent removal/recovery of every required source class and the complete P1-believed → P2-corrected lifecycle proving correction timing/provenance without backward leakage into State B.

Decision: `PARTIAL`.

## R-050 — PARTIAL

The backend historical Ask/Brain and citation cutoff behavior passed in the governed A/B/C/D fixture. Real Chromium rendered the Time Lens surface and the accessible project shell, but the current web surface contains descriptive Time Lens text rather than an interactive historical revision selector.

Remaining exact gap: real browser selection of State B, visible historical mode/time/completeness, historical citations and Brain, source removal/recovery in browser, and Return to Now from that selected revision.

Decision: `PARTIAL`.

## R-051 — PARTIAL

Fresh Chromium state passed first-run bootstrap, login, two-project onboarding, global/project navigation, invalid login, unauthenticated protected-state rejection (`401`), CSRF rejection (`403`), logout invalidation, relogin, Core restart, refresh/reconnect, and durable project recovery.

Remaining exact gap: interrupted initial setup and explicit setup-resume qualification.

Decision: `PARTIAL`.

## R-052 — VERIFIED

Real Chromium passed with two disposable projects and a fresh browser state. The required Overview, Ask, Search, Goal, Progress, Repository, Authority, Memory, Brain, Time Lens, Knowledge, Evidence, Activity, AI Connections, and Settings surfaces were present in the accessibility tree and rendered at desktop, tablet, and narrow/mobile viewports. Project A/B switching remained isolated; refresh and Core restart recovered the project registry; invalid Search and Ask project routes returned `404 PROJECT_NOT_FOUND` after the minimal route fix; healthy Core state rendered `HEALTHY`; provider absence rendered `DEGRADED-SAFE` and Ask returned safe `UNKNOWN`.

Decision: `R-052 = VERIFIED`, `remaining_gap = NONE`.

## R-053 — PARTIAL

Chromium accessibility-tree inspection, desktop/tablet/mobile responsive screenshots, textual non-color-only status semantics, accessible names, Brain list/tree fallback, empty/degraded/error content, reduced-motion CSS rule, and destructive dialog Escape cancellation passed. The rendered mobile layout had no horizontal overflow (`scrollWidth == innerWidth`).

Remaining exact gap: full keyboard-only focus-order/form-submission evidence, safe untrusted-text fixture, and any separately required external assistive-technology run. The external assistive-technology criterion is tracked separately and is not treated as a blanket blocker.

Decision: `PARTIAL`.

## Preserved and deferred state

Preserved `VERIFIED`: `R-037`, `R-038`, `R-039`, `R-040`, `R-041`, `R-046`, `R-047`, `R-049`, `R-054`, `R-055`.

Still open or partial by exact evidence: `R-043`, `R-044`, `R-045`, `R-048`, `R-050`, `R-051`, `R-053`; native `R-031–R-034`; private Tailscale `R-035–R-036`; and integrated `R-056 = OPEN`.

No credentials or raw provider/Hindsight payloads are included in this evidence. Deployment: `NOT PERFORMED`.

## Post-publication governance correction

The initial summary line above was published before the qualification ledger's top-level status map was reconciled. The evidence decisions in this record already promote `R-042` and `R-052` to `VERIFIED`; the authoritative governed count after the Continuation 025 correction is `12/26 VERIFIED`, `13 partial`, `1 blocked_by_environment` (`R-056`), and `0 failed`. No R-042 or R-052 qualification was rerun.
