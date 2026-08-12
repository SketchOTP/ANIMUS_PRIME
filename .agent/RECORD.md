# Project Decision and Milestone Record Template

After adoption, use this append-only record for major durable project events and decisions, not routine task outcomes.

## Entry guidance after adoption

Use it for architectural decisions, governance changes, releases, qualification or certification events, major reversals, important milestones, and decision supersessions.

Each live entry should include:

- Date.
- Record or decision ID.
- Status.
- Decision or event.
- Rationale.
- Affected areas.
- Supersession relationship when applicable.

Allowed status values are `PROPOSED`, `ACTIVE`, `SUPERSEDED`, `REVERSED`, and `CLOSED`.

Do not add live decisions or milestones to this template. Examples must remain outside the shipped template state.

## DEC-PRIME-PHASE0-001

- Date: 2026-08-10
- Record or decision ID: DEC-PRIME-PHASE0-001
- Status: ACTIVE
- Decision or event: Phase 0 source lock and dependency qualification established.
- Rationale: PRIME-SPEC-V1.0.0 requires immutable inputs, explicit contracts, pinned dependencies, Hindsight adapter boundaries, and a governed Git baseline before feature implementation.
- Affected areas: baseline, authority-template/v1, contracts, dependencies, threat-model, qualification harness.
- Supersedes record: none

## DEC-PRIME-PHASE15-007

- Date: 2026-08-11
- Record or decision ID: DEC-PRIME-PHASE15-007
- Status: CLOSED
- Decision or event: Continuation 007 closed the local implementation milestone for R-046 through R-050 while retaining partial qualification and the V1 release block.
- Rationale: Evidence, citation, historical reconstruction, Git checkpoint, Time Lens, Historical Ask, and historical Brain boundaries must stabilize before backup/restore and capacity work consumes them.
- Affected areas: Evidence lifecycle/parser boundary, SourceReference/citation, historical revisions, Git checkpoint preservation, Time Lens, Historical Ask/Brain, qualification ledger, and Phase-15 governance records.
- Supersedes record: none

## DEC-PRIME-PHASE15-008

- Date: 2026-08-11
- Record or decision ID: DEC-PRIME-PHASE15-008
- Status: CLOSED
- Decision or event: Continuation 008 closed the local implementation milestone for R-042 through R-045 while retaining partial qualification and the V1 release block.
- Rationale: PRIME continuity recovery must preserve the finalized Evidence/history objects, distinguish exact PostgreSQL state from Hindsight source-ledger rebuild, restore managed payload locators into the clean target, and apply active retention/backpressure controls before later control-plane work.
- Affected areas: Continuity v2 backup/manifest/encryption, clean restore workflow, Hindsight/Evidence/historical/Git component fidelity, persisted backup scheduling, quotas, retention, queue/disk capacity controls, R-046–R-050 regression protection, qualification ledger, and Phase-15 governance records.
- Supersedes record: none
## DEC-PRIME-PHASE15-009

- Date: 2026-08-11
- Record or decision ID: DEC-PRIME-PHASE15-009
- Status: CLOSED
- Decision or event: Continuation 009 closed the local implementation milestone for R-031 through R-034 while retaining blocked native qualification and the V1 release block.
- Rationale: The existing Node architecture now has the complete local lifecycle and private-boundary implementation; native host and qualified private deployment evidence must remain separate.
- Affected areas: Node lifecycle, Core↔Node client, systemd/Windows packaging, node migration, qualification ledger, and Phase-15 governance records.
- Supersedes record: none

## DEC-PRIME-PHASE15-010

- Date: 2026-08-11
- Record or decision ID: DEC-PRIME-PHASE15-010
- Status: CLOSED
- Decision or event: Continuation 010 closed the local implementation milestone for R-035 and R-036 while retaining blocked live Tailscale qualification and the V1 release block.
- Rationale: Private remote access must remain a Serve-only operator Web plane with fixed argv, loopback validation, explicit ownership, truthful actual-state reporting, and unchanged PRIME authentication.
- Affected areas: Tailscale adapter, Core remote-access routes, remote-access tests, qualification ledger/matrix, and Phase-15 governance records.
- Supersedes record: none

## DEC-PRIME-PHASE15-011

- Date: 2026-08-11
- Record or decision ID: DEC-PRIME-PHASE15-011
- Status: CLOSED
- Decision or event: Continuation 011 closed the local implementation milestone for R-037 through R-041 while retaining blocked live Notion qualification and the V1 release block.
- Rationale: Notion remains a human-readable projection and optional read-only knowledge surface, never project authority. Managed regions, user content, source provenance, failure states, and history identity require separate bounded lifecycle records before live qualification.
- Affected areas: Notion lifecycle/provider boundary, Documentation Agent ordering, Knowledge Sources, reconciliation, managed history, migration 0022, tests, qualification ledger/matrix, and Phase-15 governance records.
- Supersedes record: none

## DEC-PRIME-PHASE15-012

- Date: 2026-08-11
- Record or decision ID: DEC-PRIME-PHASE15-012
- Status: CLOSED
- Decision or event: Continuation 012 closed the local implementation milestone for R-051 through R-053 and established the MyAssistant Notion authorization reuse boundary while retaining live/browser qualification blocks.
- Rationale: PRIME must reuse the existing authorization without exposing its secret, capability-test actual Notion permissions, and expose the complete operator product shell with truthful state handling before live qualification can be attempted.
- Affected areas: Notion credential registry and capability API, migration 0023, operator state/Ask routes, responsive web shell, setup/auth/project workflow, accessibility and status semantics, R-051–R-053 ledger/matrix/evidence, and governance records.
- Supersedes record: none
## DEC-PRIME-PHASE15-013

- Date: 2026-08-11
- Record or decision ID: DEC-PRIME-PHASE15-013
- Status: CLOSED
- Decision or event: Close the local R-054/R-055 implementation boundary with a Core-owned, profile-specific AI execution service. The service treats all source text as untrusted data, enforces privacy before provider dispatch, validates structured outputs/citations, records durable non-secret provenance/usage, and refuses hidden fallback. R-056 remains the aggregate clean-install E2E requirement.
- Rationale: AI provider qualification is not reproducible or safe when profile identity, source revisions, privacy mode, usage, and output validation are implicit. The Core boundary makes those conditions durable while keeping live qualification separate.
- Affected areas: `src/prime_core/ai_service.py`; `src/prime_core/intelligence_service.py`; `apps/core/main.py`; `migrations/prime/0024_ai_execution.sql`; AI golden fixtures; R-054/R-055 qualification ledger and evidence.
- Supersedes record: none

## DEC-PRIME-PHASE15-014

- Date: 2026-08-11
- Record or decision ID: DEC-PRIME-PHASE15-014
- Status: CLOSED
- Decision or event: Publish the complete governed PRIME repository to `SketchOTP/ANIMUS_PRIME` and make exact `main` parity a checkpoint requirement.
- Rationale: GitHub was a stale placeholder while the governed implementation existed only locally. Explicit force-with-lease publication against the verified placeholder preserves continuity without allowing an unrestricted overwrite, and future governed checkpoints must be externally inspectable before completion.
- Affected areas: canonical Git remote, `main` publication, secret-safety inspection, representative source/governance/test/migration/evidence paths, Phase-15 publication evidence.
- Supersedes record: none

## DEC-PRIME-PHASE15-015

- Date: 2026-08-11
- Record or decision ID: DEC-PRIME-PHASE15-015
- Status: CLOSED
- Decision or event: Remove the local PostgreSQL qualification blocker using the existing disposable Phase-1 stack and repair the actual AI persistence defect exposed by clean database-backed execution.
- Rationale: Phase 1–13 gates must reflect a real clean migration environment rather than an unavailable host variable. The first real Ask execution exposed a 21-column/22-placeholder `ai_runs` insert mismatch; qualification required the minimum repair and a fresh rerun.
- Affected areas: disposable PostgreSQL/pgvector qualification environment, migrations through `0024_ai_execution.sql`, `src/prime_core/ai_service.py`, Phase 1–14 gates, full regression, Phase-15 evidence, and qualification governance.
- Supersedes record: none

## DEC-PRIME-PHASE15-016

- Date: 2026-08-11
- Record or decision ID: DEC-PRIME-PHASE15-016
- Status: CLOSED
- Decision or event: Promote R-049 independently to VERIFIED after exact PostgreSQL/Git/Time Lens qualification; repair citation resolution so Evidence retraction/purge and missing Git checkpoint bundles cannot report `EXACT`.
- Rationale: Qualification is per requirement. A retained PRIME-owned Git checkpoint is independently releasable evidence when ordinary refs/history are pruned and the retained artifact survives restart, degraded loss, and recovery. Citation status must follow retained source identity and lifecycle state rather than current hash equality alone.
- Affected areas: `src/prime_core/history_service.py`, `tests/phase15/test_requirement_qualification.py`, R-049 ledger/matrix/traceability, Phase-15 evidence, and continuation governance.
- Supersedes record: DEC-PRIME-PHASE15-015

## DEC-PRIME-PHASE15-017

- Date: 2026-08-11
- Record or decision ID: DEC-PRIME-PHASE15-017
- Status: CLOSED
- Decision or event: Promote R-046 and R-047 independently to VERIFIED after real PostgreSQL-backed Evidence file, parser, root/isolation, backup/restore, Search, Ask, Progress, Documentation, retraction, and recovery qualification; preserve R-049 VERIFIED and keep R-042/R-043/R-045/R-048/R-050 partial where exact remaining normative branches are incomplete.
- Rationale: Requirement release status follows complete evidence per row, not aggregate test count. The minimum production repair was to admit Evidence into Intelligence Search/Ask, retain Progress evidence references, make separate-mount classification device-aware, persist interrupted restore state after rollback, and report historical Evidence availability truthfully.
- Affected areas: `src/prime_core/backup_service.py`, `src/prime_core/history_service.py`, `src/prime_core/intelligence_service.py`, `src/prime_core/progress_service.py`, `apps/core/main.py`, `tests/phase15/test_requirement_qualification.py`, R-046/R-047 ledger/matrix/traceability, Phase-15 evidence, and continuation governance.
- Supersedes record: DEC-PRIME-PHASE15-016

## DEC-PRIME-PHASE15-018

- Date: 2026-08-11
- Record or decision ID: DEC-PRIME-PHASE15-018
- Status: CLOSED
- Decision or event: Use the operator-approved Paragon endpoint as an environment-backed LOCAL_ONLY provider through the existing AI execution boundary; promote R-054 to VERIFIED after real provider execution and preserve R-055 partial. Treat the supplied Notion authorization as ephemeral and qualify only read capability without an explicitly controlled write target; move R-037–R-041 to partial rather than environment-blocked.
- Rationale: The endpoint and credential were intentionally supplied for qualification. The minimum adapter preserves the frozen provider/privacy/provenance contract without introducing a second architecture or persisting secrets. Notion reads are independently proven, while uncontrolled live writes would not establish safe lifecycle evidence.
- Affected areas: `src/prime_core/ai_service.py`, `tests/phase15/test_ai_execution.py`, Notion credential/API boundary, R-037–R-041/R-054/R-055 ledger/matrix/traceability, Phase-15 evidence, and continuation governance.
- Supersedes record: DEC-PRIME-PHASE15-017

## DEC-PRIME-PHASE15-019

- Date: 2026-08-12
- Record or decision ID: DEC-PRIME-PHASE15-019
- Status: CLOSED
- Decision or event: Use the approved Paragon profile through the existing AI execution boundary for the real Continuation 019 Project A/B and six-function matrix, and use only a standalone connected Notion qualification sandbox for live write capability and managed/source revision probes. Preserve R-055 and R-037–R-041 as partial until integrated product and local-adapter lifecycle criteria are complete.
- Rationale: The new environments support meaningful qualification, but direct provider-boundary success and connector-level disposable writes must not be overstated as complete integrated product lifecycle evidence. The frozen baseline, authority boundary, secret policy, R-046/R-047/R-049/R-054 VERIFIED set, R-056 OPEN state, and no-deployment rule remain unchanged.
- Affected areas: `src/prime_core/ai_service.py`, `scripts/phase15_qualify_continuation_019.py`, Notion disposable sandbox, R-037–R-041/R-055 ledgers and evidence, Phase-15 governance records, and GitHub publication.
- Supersedes record: DEC-PRIME-PHASE15-018

## DEC-PRIME-PHASE15-020

- Date: 2026-08-12
- Record or decision ID: DEC-PRIME-PHASE15-020
- Status: CLOSED
- Decision or event: Promote R-055 to VERIFIED after Continuation 020 completed the real Paragon AI lifecycle through IntelligenceService, durable ai_runs/provenance, product Project A/B source rejection, managed Documentation projection, invalid-citation rejection, correction/supersession history, provider degradation/recovery, and bounded history rollover. Keep R-037–R-041 partial because their approved live disposable parent is in trash and the Notion API rejected create-page requests against archived targets.
- Rationale: R-055's exact product AI lifecycle is independently complete; live Notion adapter qualification is a separate requirement family. The qualification target failure is concrete and must not be worked around by mutating canonical pages. R-056 remains OPEN and V1 remains FAIL until all 26 rows are verified.
- Affected areas: `src/prime_core/intelligence_service.py`, `src/prime_core/memory_service.py`, `src/prime_core/notion_api.py`, `src/prime_core/notion_service.py`, `scripts/phase15_qualify_continuation_020.py`, R-055 ledgers/matrix/traceability, and `evidence/phase15/qualification-continuation-020.md`.
- Supersedes record: DEC-PRIME-PHASE15-019

## DEC-PRIME-PHASE15-021

- Date: 2026-08-12
- Record or decision ID: DEC-PRIME-PHASE15-021
- Status: CLOSED
- Decision or event: Treat Atlas `/home/sketch/Projects/ANIMUS_PRIME` at final status-synchronized HEAD `e7b70d26f1016bde2d5479cd3adeadda9ee4d725` as the authoritative current state, with inherited Continuation 020 qualification commit `e7f6099679a982d9708c3a4c96d87fa900a0e89d`. Accept Continuation 020's fresh disposable `86 passed` result as the recorded qualification evidence, while classifying the current populated-database `83 passed/3 state-collision failures` rerun as non-authoritative reuse evidence rather than a code regression.
- Rationale: the current failures are deterministic collisions from prior durable test state, while governance and compileall pass and the current ledgers, evidence, implementation diff, and Architect record agree on the same 5/26 qualification state. A fresh reset is required for a new authoritative regression and was intentionally not performed during this read/verify takeover pass.
- Affected areas: `.agent/CURRENT.md`, `.agent/DIRECTIVES.md`, `.agent/OUTCOMES.md`, `.agent/LEARNINGS.md`, qualification execution records, and future fresh-database rerun procedure.
- Supersedes record: none
## DEC-PRIME-PHASE15-022

- Date: 2026-08-12
- Record or decision ID: DEC-PRIME-PHASE15-022
- Status: ACTIVE
- Decision or event: Treat the existing `PRIME Qualification Sandbox — Continuation 019` as a current disposable-parent candidate only; do not mutate it until PRIME's own production adapter can execute with the existing runtime authorization. Correct R-042 to remove the already-satisfied off-machine-target criterion and retain only scheduled failure/recovery, retry, known-good preservation, subsequent success, and retention gaps.
- Rationale: Notion workspace access is not equivalent to PRIME `NotionApiClient` authorization. Continuation 017 already proved `/mnt/storage1tb` on `/dev/sdb1`; repeating that criterion would misstate qualification progress.
- Affected areas: `evidence/phase15/qualification-continuation-022.md`, `evidence/phase15/qualification-continuation-017.md`, `docs/phase15-remediation-qualification-ledger.yaml`, and `docs/phase15-remediation-matrix.yaml`.
- Supersedes record: none

## DEC-PRIME-PHASE15-023

- Date: 2026-08-13
- Record or decision ID: DEC-PRIME-PHASE15-023
- Status: CLOSED
- Decision or event: Promote R-037 through R-041 to VERIFIED after native Atlas qualification completed the actual PRIME NotionApiClient/NotionApiProvider/NotionLifecycleService path against a disposable live Notion sandbox with the approved Paragon profile. Preserve R-046, R-047, R-049, R-054, and R-055 VERIFIED; keep R-042's scheduled failure/recovery/retention gap and R-056 OPEN; keep Phase 15/V1 FAIL at 10/26.
- Rationale: Fresh native Docker/PostgreSQL qualification and the 86-test regression passed. The previous sandbox was unavailable to the supplied integration, so a disposable child under accessible ANIMUS PRIME was provisioned under the explicit Continuation 023 exception. Live Project Record binding, managed projection, source lifecycle, degradation/recovery, and history rollover evidence passed without canonical/user-authored mutation or credential persistence.
- Affected areas: `evidence/phase15/qualification-continuation-023.md`, `docs/requirements-traceability.yaml`, `docs/phase15-remediation-matrix.yaml`, `docs/phase15-remediation-qualification-ledger.yaml`, `.agent/phase-records/PHASE-15.md`, `.agent/CURRENT.md`, and publication records.
- Supersedes record: DEC-PRIME-PHASE15-022

## DEC-PRIME-PHASE15-024

- Date: 2026-08-12
- Record or decision ID: DEC-PRIME-PHASE15-024
- Status: CLOSED
- Decision or event: Promote R-042 and R-052 to VERIFIED from Continuation 024 evidence. Preserve the prior ten VERIFIED rows, keep R-043, R-044, R-045, R-048, R-050, R-051, and R-053 partial, keep R-056 OPEN, and keep Phase 15/V1 FAIL at 12/26.
- Rationale: The native Atlas backup harness exercised durable schedule persistence, failure/retry, known-good preservation, recovery, retention, and negative security cases against the independent off-machine target. The real Chromium run exercised the complete supported operator journey across two projects, project isolation/switching, restart recovery, invalid project rejection, required surfaces, responsive rendering, degraded truthfulness, and protected lifecycle entry. Hindsight retain returned UNAVAILABLE and was not overstated. The two product fixes were minimal and directly evidenced by the fresh regression and browser run.
- Affected areas: `apps/core/main.py`, `src/prime_core/reliability_service.py`, `scripts/phase15_qualify_continuation_024.py`, `evidence/phase15/qualification-continuation-024.md`, `docs/requirements-traceability.yaml`, `docs/phase15-remediation-matrix.yaml`, `docs/phase15-remediation-qualification-ledger.yaml`, and append-only `.agent` records.
- Supersedes record: DEC-PRIME-PHASE15-023

## DEC-PRIME-PHASE15-025

- Date: 2026-08-12
- Record or decision ID: DEC-PRIME-PHASE15-025
- Status: ACTIVE
- Decision or event: Treat the Continuation 025 reconciliation as the authoritative current qualification state: R-042 and R-052 remain VERIFIED from Continuation 024, R-051 is newly VERIFIED from fresh browser setup-resume evidence, R-050 remains partial after the minimum interactive Time Lens implementation, and R-053 remains partial pending external assistive technology.
- Rationale: The stale top-level ledger map, not the row records, caused the 12/26 versus 10/26 inconsistency. Mechanical parsing of all three governed views now yields 12/26 before Continuation 025 promotion. The fresh R-051 browser interruption/resume path returned `502` during Core outage and `200` after recovery. Time Lens controls now call the existing bounded backend routes and render returned status with text-only DOM updates.
- Affected areas: `docs/phase15-remediation-qualification-ledger.yaml`, `docs/phase15-remediation-matrix.yaml`, `docs/requirements-traceability.yaml`, `apps/web/index.html`, `tests/phase14/test_web_shell.py`, and Continuation 025 evidence.
- Supersedes record: DEC-PRIME-PHASE15-024

## DEC-PRIME-PHASE15-026

- Date: 2026-08-12
- Record or decision ID: DEC-PRIME-PHASE15-026
- Status: ACTIVE
- Decision or event: Promote R-050 to VERIFIED from Continuation 026's real State-A/B/C/D browser qualification. Preserve R-042, R-052, and the prior thirteen verified rows; keep R-043, R-044, R-045, R-048, and R-053 partial; keep R-056 OPEN; and set the governed count to 14/26.
- Rationale: The populated historical fixture reconstructed State B exactly across repository, authority, Goal, Evidence, Progress, Memory, Notion, Brain, and Git. Historical Ask/Brain excluded later current state, deliberate Evidence loss produced truthful source-level PARTIAL status, exact restoration recovered all sources, and Return to Now selected CURRENT with exact sources. The browser path therefore meets R-050's qualification boundary while the other rows retain explicit incomplete criteria.
- Affected areas: `Dockerfile.core`, `src/prime_core/git_history.py`, `src/prime_core/history_service.py`, `scripts/phase15_qualify_continuation_026.py`, `evidence/phase15/qualification-continuation-026.md`, the three governed requirement views, and append-only `.agent` records.
- Supersedes record: DEC-PRIME-PHASE15-025

## DEC-PRIME-PHASE15-027

- Date: 2026-08-12
- Record or decision ID: DEC-PRIME-PHASE15-027
- Status: CLOSED
- Decision or event: Promote R-043 and R-048 to VERIFIED from Continuation 027's production-path disposable evidence. Preserve R-045 as partial because the system lacks complete parser/index/stale-job, retention-pressure, and usage/cost qualification boundaries. Keep R-044 and R-053 partial, R-056 OPEN, and Phase 15/V1 FAIL at 16/26.
- Rationale: R-043 used a genuinely new PostgreSQL target, complete representative source state, production restore route, unconditional replacement step-up, safety checkpoint, populated-target refusal, and durable interruption state. R-048 independently removed and restored every required historical source class and proved the P1/P2 correction timeline without backward leakage. A real sustained parser load did not establish the missing R-045 normative boundaries, so no over-promotion was made. Hindsight retain is unavailable because no Hindsight process/listener or Docker runtime exists on the qualification host; no external AT environment is available.
- Affected areas: `apps/core/main.py`, `src/prime_core/backup_service.py`, `src/prime_core/history_service.py`, `scripts/phase15_qualify_continuation_027.py`, `evidence/phase15/qualification-continuation-027.md`, the three governed requirement views, and append-only `.agent` records.
- Supersedes record: DEC-PRIME-PHASE15-026

## DEC-PRIME-PHASE15-028

- Date: 2026-08-12
- Record or decision ID: DEC-PRIME-PHASE15-028
- Status: CLOSED
- Decision or event: Continuation 028 audited all 81 frozen §26 Definition-of-Done items, fixed the CSP-blocked operator shell and the first highest-value product slice, promoted only Home and Since You Were Here to user-usable status, and kept `V1_PRODUCT_GOAL_ALIGNMENT` FAIL.
- Rationale: A fresh disposable PostgreSQL/browser run exercised initialization, sign-in, project creation, live Home/Overview/Needs Attention/Recently Active/Activity, checkpoint advancement, safe UNKNOWN Ask, grouped Search, derived-only Brain, and Time Lens controls. The remaining data-backed workflows, integrations, lifecycle paths, and environment-bounded evidence are not complete, so no blanket remediation-row reopen or release promotion is justified.
- Affected areas: `apps/core/main.py`, `apps/web/index.html`, `docs/v1-product-goal-alignment-audit.yaml`, `docs/requirements-traceability.yaml`, `docs/phase15-remediation-matrix.yaml`, `docs/phase15-remediation-qualification-ledger.yaml`, `evidence/phase15/product-goal-alignment-continuation-028.md`, and append-only `.agent` records.
- Supersedes record: DEC-PRIME-PHASE15-027

## DEC-PRIME-PHASE15-029

- Date: 2026-08-12
- Record or decision ID: DEC-PRIME-PHASE15-029
- Status: CLOSED
- Decision or event: Complete the first V1 product-understandability wave with a production-backed durable fixture, repository/authority/search/context-export operator slice, interpreter-portable qualification, and architecture-aware §26 audit. Preserve the frozen baseline, keep the V1 product gate FAIL, keep R-056 OPEN, and do not deploy.
- Rationale: Fresh qualification passed 86 tests and Phases 1–14. The browser path loaded real Project A state, exposed goal/progress/integrity/repository/authority/memory/evidence/activity, returned bounded Markdown/JSON context, and proved Project A/B search/export isolation. Seven architecture-only invariants are now PRODUCT_VERIFIED with explicit evidence; all remaining user-facing and environment-bound gaps remain visible.
- Affected areas: `apps/core/main.py`, `apps/web/index.html`, `src/prime_core/indexer.py`, `src/prime_core/intelligence_service.py`, `scripts/seed_product_completion_029.py`, `tests/phase0/test_harness.py`, `tests/phase15/test_product_completion_029.py`, `docs/v1-product-goal-alignment-audit.yaml`, the three governed views, Continuation 029 evidence, and append-only `.agent` records.
- Supersedes record: DEC-PRIME-PHASE15-028

## DEC-PRIME-PHASE15-030

- Date: 2026-08-12
- Record or decision ID: DEC-PRIME-PHASE15-030
- Status: CLOSED
- Decision or event: Close the bounded Continuation 030 Wave-2 onboarding slice as PARTIAL. Preserve the frozen V1 baseline, keep the V1 product gate FAIL, keep R-056 OPEN, and do not deploy.
- Rationale: Fresh disposable PostgreSQL/browser qualification proved setup status, enrolled-root rejection, safe non-bare repository creation, authority-template bootstrap, reviewed goal approval, initial index request, truthful `UNBORN` Git identity, provenance/redacted Markdown and JSON export, and Project A/B isolation. It did not prove the complete interrupted-resume, GoalModel-bound progress, AGENTS-chain, activity filtering, or external/native integration requirements.
- Affected areas: `apps/core/main.py`, `apps/web/index.html`, `src/prime_core/service.py`, `src/prime_core/indexer.py`, `migrations/prime/0025_product_onboarding.sql`, `docs/v1-product-goal-alignment-audit.yaml`, Continuation 030 evidence, and append-only `.agent` records.
- Supersedes record: DEC-PRIME-PHASE15-029
