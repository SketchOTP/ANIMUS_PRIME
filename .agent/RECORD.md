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

## DEC-PRIME-PHASE15-031

- Date: 2026-08-12
- Record or decision ID: DEC-PRIME-PHASE15-031
- Status: ACTIVE
- Decision or event: Continue Continuation 031 as a bounded partial implementation slice. Add durable GoalModel/progress, AGENTS-chain, activity, project-scoped AI grant lifecycle, source-labelled Brain, and protected committed-revision Fork/Clone boundaries, but do not promote product rows without authenticated qualification evidence.
- Rationale: The frozen product objective requires durable lifecycle state and independent project resources. The implementation now makes those boundaries explicit while the fresh database/browser journey, interactive 3D behavior, live Brain update, and A/B isolation remain unverified. Keeping the audit at implementation-open status preserves truthful release gating.
- Affected areas: `apps/core/main.py`, `apps/web/index.html`, `src/prime_core/service.py`, `src/prime_core/progress_service.py`, `src/prime_core/indexer.py`, `src/prime_core/mcp_service.py`, `src/prime_core/brain_service.py`, `migrations/prime/0026_product_completion_wave3.sql`, `docs/v1-product-goal-alignment-audit.yaml`, Continuation 031 evidence, and append-only `.agent` records.
- Supersedes record: DEC-PRIME-PHASE15-030

## DEC-PRIME-PHASE15-032

- Date: 2026-08-12
- Record or decision ID: DEC-PRIME-PHASE15-032
- Status: ACTIVE
- Decision or event: Continue Continuation 032 as a bounded qualification and repair cycle. Classify the fresh startup path before changing migrations; retain the migration set because fresh PostgreSQL/pgvector startup and restart passed; apply only the demonstrated project-scoped MCP revocation type-safety repair; keep Wave-3 product and external gaps unpromoted.
- Rationale: The prior startup block was caused by unavailable Docker Desktop, not a failed migration. Authenticated two-project evidence proves substantial backend and browser surfaces, but not the frozen full interactive 3D Brain, live Brain update, complete browser AI Connections workflow, Activity source drill-down, or all external/native requirements. The frozen baseline, V1/Phase 15 gate, and R-056 must remain truthful.
- Affected areas: `src/prime_core/mcp_service.py`, `tests/phase15/test_product_completion_032.py`, `apps/web/index.html`, Continuation 032 evidence, and append-only `.agent` records.
- Supersedes record: DEC-PRIME-PHASE15-031

## DEC-PRIME-PHASE15-033

- Date: 2026-08-12
- Record or decision ID: DEC-PRIME-PHASE15-033
- Status: CLOSED
- Decision or event: Close Continuation 033 as PARTIAL after a fresh native-Atlas regression gate and bounded V1 product completion work. Keep the frozen baseline, V1/Phase 15 gate, external blockers, R-056, and deployment boundary unchanged.
- Rationale: Fresh PostgreSQL/pgvector with all 26 migrations, full pytest, Phases 1–14, governance, compile, diff, YAML, audit, and secret checks passed. The cycle repaired demonstrated Git bundle verification and GoalModel progress enforcement, and added bounded Brain, Activity provenance, and AI Connections UI surfaces. Direct browser evidence only supports fixture-scale Brain qualification; remaining complete workflows and external environments are not proven.
- Affected areas: `src/prime_core/git_history.py`, `src/prime_core/service.py`, `src/prime_core/progress_service.py`, `apps/core/main.py`, `apps/web/index.html`, `tests/phase15/test_product_completion_033.py`, `docs/v1-product-goal-alignment-audit.yaml`, `docs/v1-product-gap-burndown.yaml`, Continuation 033 evidence, and append-only `.agent` records.
- Supersedes record: DEC-PRIME-PHASE15-032

## DEC-PRIME-PHASE15-034

- Date: 2026-08-13
- Record or decision ID: DEC-PRIME-PHASE15-034
- Status: CLOSED
- Decision or event: Close Continuation 034 as PARTIAL. Classify the published artifact as clean and unbroken under the normal unprivileged Core image, replace the generic 70-row gap view with a concrete execution queue, and keep all unproven product and external requirements open.
- Rationale: Exact clean checkout `b325390f` built and started with `USER nobody`, 26 migrations applied, and Core restart/live health passed. The previous mode-660 condition is isolated to the long-lived development worktree. Current authenticated browser regression proved truthful setup, project, Goal/Progress, Brain fixture-scale, Search partial, degraded Ask, unavailable Time Lens, safe AI empty state, and Activity no-source behavior, but not complete frozen acceptance. Atlas has systemd and Tailscale, while native Node installer evidence, Windows, second device, approved PRIME Hindsight retain, live Notion, and external AT remain unavailable or incomplete.
- Affected areas: `docs/v1-product-gap-burndown.yaml`, `docs/v1-product-goal-alignment-audit.yaml`, `scripts/validate_product_gap_burndown.py`, Continuation 034 evidence, and append-only `.agent` records.
- Supersedes record: DEC-PRIME-PHASE15-033


## DEC-PRIME-PHASE15-035

- Date: 2026-08-13
- Record or decision ID: DEC-PRIME-PHASE15-035
- Status: CLOSED
- Decision or event: Close Continuation 035 as PARTIAL. Reconcile acceptance semantics across the audit and burndown, promote only DOD-001, repair stale project-scoped browser state, and preserve all unsupported product and external rows as open.
- Rationale: Fresh native Atlas database qualification passed 91 tests and Phases 1–14. The ordinary pytest collection collision is fixed. Browser qualification proved current project surfaces, fixture-scale Brain, truthful Time Lens PARTIAL/CURRENT behavior, repository/activity surfaces, and safe provider/integration degradation. It also exposed and fixed stale Brain state across project switching. Fork correctly refused a dirty source tree, historical Goal/Brain reconstruction is incomplete, representative/live Brain evidence is absent, Hindsight retain remains non-recallable, and Notion/AT/native/second-device boundaries remain external or unavailable.
- Affected areas: pytest.ini; apps/web/index.html; docs/v1-product-goal-alignment-audit.yaml; docs/v1-product-gap-burndown.yaml; scripts/validate_product_gap_burndown.py; evidence/phase15/product-goal-alignment-continuation-035.md; append-only .agent records.
- Supersedes record: DEC-PRIME-PHASE15-034
## DEC-PRIME-PHASE15-036

- Date: 2026-08-13
- Record or decision ID: DEC-PRIME-PHASE15-036
- Status: CLOSED
- Decision or event: Continue closure with semantic truth first. Architecture-only rows retain their exact invariant residuals and do not acquire invented UI requirements. Hindsight configuration is centralized in Settings and compose topology. Historical Time Lens explicitly loads historical Brain and Goal state. No Phase 16, deployment, or R-056 closure; the prior publication facts are retained as governed evidence.
- Rationale: Continuation 036 corrected semantic audit claims and published its implementation/evidence parent at de96e42ccde0d5294a9ab1c70a25690158f08397, followed by the corrected governed tip 5fa9007d951e3a698233515506424e0be069c982 with local/origin/advertised parity MATCHED and Notion confirmation.
- Affected areas: Hindsight configuration, historical Time Lens, §26 audit/burndown semantics, Continuation 036 evidence, GitHub publication, Notion execution record.
- Supersedes record: DEC-PRIME-PHASE15-035

## DEC-PRIME-PHASE15-037

- Date: 2026-08-13
- Record or decision ID: DEC-PRIME-PHASE15-037
- Status: CLOSED
- Decision or event: Close Continuation 037 as PARTIAL. Promote R-044, authenticated historical Time Lens/Ask, AI Connections grant lifecycle, and the qualified Hindsight bank/contract/durable-memory invariants; keep DOD-068, browser Fork completion, Brain focus-state, remaining local workflows, external environments, and R-056 open.
- Rationale: Native Atlas qualification used fresh disposable PostgreSQL/pgvector and the live Hindsight service. Hindsight outage truthfulness, source-ledger rebuild labeling, exact managed Evidence/Git restoration, correction/tombstone/supersession, authenticated historical reconstruction, and negative component cases passed. Browser Fork exposed a client path-normalization defect, and the approved Hindsight Mental Models/reflect path remains unavailable. The frozen V1 gate remains FAIL.
- Affected areas: src/prime_core/memory_service.py; apps/web/index.html; tests/phase5/test_memory_service.py; scripts/phase15_qualify_continuation_037.py; three governed views; Continuation 037 evidence; append-only .agent records.
- Supersedes record: DEC-PRIME-PHASE15-036

## DEC-PRIME-PHASE15-038

- Date: 2026-08-13
- Record or decision ID: DEC-PRIME-PHASE15-038
- Status: CLOSED
- Decision or event: Close Continuation 038 as PARTIAL. Reconcile the burndown derived view to 81 audit rows, 18 complete, and 63 open with mechanically enforced work-class totals. Record the native Atlas path boundary as a harness-level MSYS conversion issue, retain opaque path handling in PRIME, and record browser Fork A1/A2 as bounded evidence without promoting DOD-016/DOD-017. Keep Brain focus/state, Hindsight reflect/Mental Models, remaining local workflows, external environments, R-045, and R-056 open.
- Rationale: Native SSH execution and disposable browser/Core qualification produced direct evidence. The correct MSYS-disabled invocation preserved `/tmp/prime038-source` through field, JavaScript, JSON, Core, and service boundaries; no product normalization patch was justified. Browser Fork selected revisions and real destinations passed, but the full resource-isolation matrix was not completed. Brain returned UNAVAILABLE in the disposable fixture and Hindsight reflect timed out/unavailable through the configured routerbot-local provider.
- Affected areas: docs/v1-product-gap-burndown.yaml; scripts/validate_product_gap_burndown.py; tests/phase15; Continuation 038 evidence; append-only .agent records; GitHub and Notion publication.
- Supersedes record: DEC-PRIME-PHASE15-037

## DEC-PRIME-PHASE15-039

- Date: 2026-08-13
- Record or decision ID: DEC-PRIME-PHASE15-039
- Status: CLOSED
- Decision or event: Close Continuation 039 as PARTIAL. Retain the minimal browser fixes that clear project-scoped Brain/query/filter/detail state on project switch and when a filter removes the selected node. Record the reusable native-Atlas A/B fixture, exact Brain topology/interactions, Activity/Repository/Search/Progress/Ask-safe result, Fork A1/A2, and clean-source refusal as bounded evidence without promoting DOD-016, DOD-017, DOD-021, DOD-022, or DOD-051.
- Rationale: The direct Atlas fixture produced real repositories, authority, goals, progress, evidence, activity, MCP grants, PRIME memory, retained checkpoints, and independently recallable Hindsight banks for A and B. Approved `PrimeMemoryAdapter.reflect()` remained `UNAVAILABLE` at the bounded timeout, and the exact Brain query contract, complete resource-isolation matrix, approved model execution, external/native environments, R-045, and R-056 remain unqualified.
- Affected areas: `apps/web/index.html`; Continuation 039 fixture and reflect probe; Continuation 039 evidence; append-only `.agent` records.
- Supersedes record: DEC-PRIME-PHASE15-038

## DEC-PRIME-PHASE15-040

- Date: 2026-08-13
- Record or decision ID: DEC-PRIME-PHASE15-040
- Status: CLOSED
- Decision or event: Close Continuation 040 as PARTIAL. Promote DOD-017 after direct Fork resource-isolation qualification and DOD-051 after exact Brain/operator qualification; retain DOD-016, DOD-068, R-045, R-056, and all external/native/Notion/AT/provider boundaries as open or blocked.
- Rationale: The stale DOD-017 Windows-path audit wording was replaced by the actual remaining governed boundary, and Fork now clones selected history, clears remotes, provisions current authority, and creates a DRAFT child goal. Native Atlas evidence proved independent authority, progress, memory, MCP grant, Hindsight bank, and dirty-source behavior. Browser evidence proved exact Brain topology, accessible node/file drill-down, camera/filter/search controls, A/B reset, Activity filters, read-only Repository/Authority, grouped Search, and safe Ask UNKNOWN. The disposable Hindsight provider remained degraded and Notion was not configured, so no external integration or release-gate overclaim was made.
- Affected areas: `src/prime_core/service.py`; Continuation 040 qualification scripts/evidence; all three requirement/governance views; append-only `.agent` records; GitHub and Notion publication.
- Supersedes record: DEC-PRIME-PHASE15-039

## DEC-PRIME-PHASE15-041

- Date: 2026-08-13
- Record or decision ID: DEC-PRIME-PHASE15-041
- Status: CLOSED
- Decision or event: Atlas-native qualification is the governing execution mode for Continuation 041. Activity category filters, source drill-down/no-source truth, AGENTS bridge metadata, and Git metadata are now visible in the operator surfaces.
- Rationale: The prior Z:/disposable workflow obscured the authoritative repository and caused path/environment drift. The real Atlas repository and persistent Core state are directly reachable over SSH.
- Affected areas: apps/web/index.html; Phase 15 governance; native Atlas qualification evidence.
- Supersedes record: DEC-PRIME-PHASE15-040

## 2026-08-13 — R-PRIME-042-NATIVE-MCP-PROGRESS

- Record or decision ID: R-PRIME-042-NATIVE-MCP-PROGRESS
- Status: CLOSED
- Decision or event: Native Atlas MCP durability/provenance and real GoalModel/Progress stale-refresh were qualified, and DOD-071/DOD-073 were promoted to PRODUCT_VERIFIED.
- Rationale: Public MCP calls returned stored/durability-verified project-scoped memory with provenance; a real code change caused the prior progress assessment to become STALE and a current reassessment was recorded.
- Affected areas: Native MCP, durable memory metadata, GoalModel/Progress, Phase 15 governance.
- Supersedes record: R-PRIME-041-NATIVE-MCP-PROGRESS

## DEC-PRIME-PHASE15-043

- Date: 2026-08-13
- Record or decision ID: DEC-PRIME-PHASE15-043
- Status: CLOSED
- Decision or event: Direct native Atlas SSH and persistent services are the qualification authority. Archive only verified repository-local regeneration caches to the attached external filesystem when storage exhaustion blocks PostgreSQL; keep uncertain state, evidence, authority, .git, PostgreSQL, and Hindsight local.
- Rationale: The root filesystem reached zero free bytes and PostgreSQL failed on WAL/checkpoint writes. Only 2.6 MB of clearly safe caches were archived and verified before removal; PostgreSQL recovered with 26 migrations.

## DEC-PRIME-PHASE15-044

- Date: 2026-08-13
- Record or decision ID: DEC-PRIME-PHASE15-044
- Status: PARTIAL
- Decision or event: Continuation 044 keeps native Atlas persistent services authoritative while completing record-complete authority admission, Progress operator controls, and capability-level Hindsight truth without disposable environments or sustained capacity qualification.
- Rationale: The latest-record-only admission path was proven to lose earlier consequential records; Progress lacked production-backed refresh and challenge controls; direct Hindsight health was healthy while Core reported a blanket degraded state.

## DEC-PRIME-PHASE15-044-CLOSEOUT

- Date: 2026-08-13
- Record or decision ID: DEC-PRIME-PHASE15-044-CLOSEOUT
- Status: CLOSED
- Decision or event: Close Continuation 044 for its bounded persistent-Atlas scope. Preserve the §26 26/55 counts and do not promote incomplete operator/environment rows.
- Rationale: Record-complete authority admission and production Progress refresh are now evidenced on the real Atlas project. The truthful boundary is preserved: no fabricated Progress correction, no approved Hindsight reflect/Mental Models claim, no R-045 sustained-capacity qualification, no Phase 16, and no deployment. Evidence is `evidence/phase15/qualification-continuation-044.md`.
- Affected areas: authority admission; Progress service/API/UI; Hindsight capability health; migration 0027; governed audit/matrix/ledger; native Atlas qualification evidence.
- Supersedes record: DEC-PRIME-PHASE15-044

## DEC-PRIME-PHASE15-045

- Date: 2026-08-13
- Record or decision ID: DEC-PRIME-PHASE15-045
- Status: CLOSED
- Decision or event: Continuation 045 reconciles the frozen §26 semantics before implementation, adopts bounded historical governance schema support, and promotes only exact DOD-030, DOD-062, and DOD-063 evidence.
- Rationale: The frozen specification places automatic authority admission in DOD-030, evidence-backed percentage/confidence/explanation in DOD-062, stale/refresh in DOD-063, and correction/challenge with history, Goal Alignment, and milestones in DOD-026. Continuation 044 directly evidenced the first three boundaries.
- Affected areas: scripts/validate_governance.py; governed audit and burndown; Continuation 045 evidence; .agent ledgers.
- Supersedes record: DEC-PRIME-PHASE15-044-CLOSEOUT
## DEC-PRIME-PHASE15-046

- Date: 2026-08-14
- Record or decision ID: DEC-PRIME-PHASE15-046
- Status: CLOSED
- Decision or event: Continuation 046 treats the frozen section-26 sentence as the acceptance authority, removes invented operator paths from architecture/documentation rows, implements bounded incremental repository observation, and keeps Core/browser work blocked when no persistent Core listener exists.
- Rationale: The audit found a real full-rescan/incremental-observation product gap and a direct duplicate-binding API gap. Both were repaired and covered by persistent Atlas regression; the remaining open rows require their exact external, browser, workflow, or aggregate boundaries.
- Affected areas: repository indexing and change intake; repository binding preflight; frozen section-26 audit/burndown; R-011 traceability; Continuation 046 evidence.
- Supersedes record: DEC-PRIME-PHASE15-045

## DEC-PRIME-PHASE15-047

- Date: 2026-08-14
- Record or decision ID: DEC-PRIME-PHASE15-047
- Status: CLOSED
- Decision or event: Reopen and re-earn DOD-061 after independent verification found the published incremental production path unexecutable and under-tested. Preserve DOD-061 as PRODUCT_VERIFIED only after direct persistent execution proves source-revision coherence, dirty worktree provenance, canonical commit advance, Progress staleness, and authority-memory admission.
- Rationale: The real persistent project reproduced the missing-json defect. The bounded repair and direct qualification now prove canonical versus active worktree state without creating a second authority. Other Core-independent rows remain unchanged because their exact acceptance evidence was not completed in this continuation.
- Affected areas: incremental repository observer; repository-file provenance migration; Progress freshness integration; automatic authority-memory admission; Continuation 047 evidence and governed records.
- Supersedes record: DEC-PRIME-PHASE15-046


## DEC-PRIME-PHASE15-048

- Date: 2026-08-14
- Record or decision ID: DEC-PRIME-PHASE15-048
- Status: CLOSED
- Decision or event: Promote only DOD-033, DOD-007, and DOD-018 after exact direct evidence; keep recovery, legacy authority migration, canonical-ref acceptance, and current topology rows open.
- Rationale: The three promoted rows have direct persistent or in-process evidence, while withheld rows retain concrete unreconciled acceptance clauses. Continuation 048 therefore closes only its bounded scope and preserves the remaining blockers.
- Affected areas: progress correction provenance, Node state audit and repository identity, governed DOD audit/burndown, Continuation 048 evidence, and append-only .agent records.
- Supersedes record: DEC-PRIME-PHASE15-047

## DEC-PRIME-PHASE15-049

- Date: 2026-08-14
- Record or decision ID: DEC-PRIME-PHASE15-049
- Status: CLOSED
- Decision or event: Promote only DOD-045, DOD-037, DOD-038, and DOD-028 after direct persistent Atlas qualification. Keep DOD-008 partial, DOD-006 topology-unqualified, DOD-039 and DOD-004 reference-only, and R-045/R-056 open; do not start Core, browser qualification, disposable state, Phase 16, or deployment.
- Rationale: The four promoted rows have exact product-boundary evidence and reconciled governed records. The remaining rows retain concrete unavailable recovery, topology, external-provider, browser/Core, sustained-capacity, or aggregate acceptance clauses and must not be papered over.
- Affected areas: canonical Git provenance and authority migration controls; memory provenance; DOD audit/burndown/traceability; Continuation 049 evidence; append-only .agent records.
- Supersedes record: DEC-PRIME-PHASE15-048

## DEC-PRIME-PHASE15-050

- Date: 2026-08-14
- Record or decision ID: DEC-PRIME-PHASE15-050
- Status: CLOSED
- Decision or event: Keep DOD-006 topology-unqualified, implement bounded stable-ID repository continuity and fail-closed rebind controls for DOD-039, and add durable workflow step/resource/replay/resume primitives with CREATE_REPOSITORY checkpointing for DOD-004 without claiming exactly-once or a real relocation cutover.
- Rationale: Direct persistent Atlas evidence confirms the existing canonical repository and logical identity, but no legitimate alternate repository candidate or current persistent Core/Node topology is available. The implementation therefore records what can be proven, refuses unsafe or stale transitions, and leaves provider/fork/restore/archive and full interruption qualification open.
- Affected areas: repository candidate/provenance inspection; repository rebind service/API and migration 0030; durable workflow primitives and CREATE_REPOSITORY path; Continuation 050 qualification/evidence; governed DOD audit/burndown/traceability; append-only .agent records.
- Supersedes record: DEC-PRIME-PHASE15-049

## DEC-PRIME-PHASE15-053

- Date: 2026-08-14
- Record or decision ID: DEC-PRIME-PHASE15-053
- Status: CLOSED
- Decision or event: Authorize and establish the persistent private PRIME Core-served Web UI on Atlas with user-systemd ownership, existing PostgreSQL/Hindsight reuse, and no public ingress. Keep authenticated operator qualification, live Node control-plane qualification, DOD-005/DOD-074 operator promotion, R-056, Phase 15 completion, and V1 declaration open.
- Rationale: Core health, readiness, listener ownership, real UI serving, clean stop/start recovery, and bounded browser behavior are directly proven. The existing operator credential is not available through approved references, and no approved Node mTLS installation exists; neither gap may be hidden with a password reset, synthetic session, insecure Node override, or disposable replacement environment.
- Affected areas: Dockerfile.core; packaging/core/prime-core.service; persistent Atlas runtime; DOD-006/DOD-005/DOD-074 evidence references; Continuation 053 evidence; append-only .agent records.
- Supersedes record: DEC-PRIME-PHASE15-050

## DEC-PRIME-PHASE15-054

- Date: 2026-08-14
- Record or decision ID: DEC-PRIME-PHASE15-054
- Status: CLOSED
- Decision or event: Establish a spec-compliant loopback/platform-local break-glass path for the existing single operator when the original one-time recovery reference is unavailable; qualify the real authenticated private Core/UI; keep Node activation blocked without governed mTLS enrollment material.
- Rationale: The permanent operator already exists, so bootstrap and direct password/recovery hash replacement are forbidden. The new recovery digest and service path preserve that identity, rotate secrets, revoke sessions, and audit recovery. The existing Node row cannot prove a live control-plane identity; the repository lacks a governed certificate lifecycle and the directive forbids insecure HTTP or fabricated trust material.
- Affected areas: local recovery migration/service/API; Atlas Core environment and persistent image; authenticated browser qualification; Node activation boundary; Continuation 054 evidence and append-only records.
- Supersedes record: DEC-PRIME-PHASE15-053

## DEC-PRIME-PHASE15-055

- Date: 2026-08-14
- Record or decision ID: DEC-PRIME-PHASE15-055
- Status: CLOSED
- Decision or event: Establish the persistent private Core-to-Node trust lifecycle on Atlas for canonical Node `node-041-atlas-native`. Core owns bootstrap signing and approval; the Node proves possession of its key; certificate and bearer references remain outside Git; operator rotation, revocation, re-enrollment, and restart recovery are explicit. Keep DOD-005 projection, R-056, Phase 15 completion, V1 declaration, and deployment open.
- Rationale: The former enrolled database record did not prove a live secure control plane. The real Atlas Node now submits a signed proof, receives an operator-approved mTLS certificate, and survives service and Core restart. Browser qualification confirms persisted project continuity during legitimate Node outage and truthful fail-closed repository behavior.
- Affected areas: Core/Node trust lifecycle; persistent Node user service; private Core/UI runtime; browser offline continuity; recovery-secret regression guard; Continuation 055 evidence.
- Supersedes record: DEC-PRIME-PHASE15-054

## DEC-PRIME-PHASE15-056

- Date: 2026-08-14
- Record or decision ID: DEC-PRIME-PHASE15-056
- Status: CLOSED
- Decision or event: Correct the Continuation 055 qualified implementation SHA as governed metadata without rewriting Git history; promote only the locally qualified recovery/step-up and backup/privacy behavior; retain DOD-005 as BACKEND_ONLY until a safe direct persistent mutation qualification is completed.
- Rationale: GitHub independently resolves the actual qualified implementation commit, while the prior transcription does not. The real persistent Core/UI now proves recent step-up enforcement and secret-safe recovery controls, and source retraction preserves historical projection provenance while staling current documentation. No disposable replacement state or live Notion dependency was used to make local claims.
- Affected areas: recovery/step-up migration/service/API/UI; backup restore security boundary; source-lifecycle projection; governed qualification records; Continuation 056 evidence; persistent Atlas service state.
- Supersedes record: DEC-PRIME-PHASE15-055

## DEC-PRIME-PHASE15-057

- Date: 2026-08-14
- Record or decision ID: DEC-PRIME-PHASE15-057
- Status: CLOSED
- Decision or event: Treat `0a3c82f0c606fb80f914eb59116dd5f46b9d5ec5` as Continuation 055 implementation provenance and `066bec5fb8041734cf28314090344bd7bb777f14` as Continuation 056 governed qualification. Keep DOD-005 BACKEND_ONLY because the real Qualification Project has no safe non-authority source with a supported reversible retraction/restoration path. Do not rotate operator credentials or mutate canonical state merely to force browser evidence.
- Rationale: The project is bound to the canonical Atlas repository and must be distinguished from persistent regression residue. The directive requires a hard stop when safe restoration cannot be guaranteed. Protected-entry UI behavior can be observed without making an unapproved credential change; authenticated clauses remain truthful and open.
- Affected areas: qualification provenance; DOD-005 evidence; browser qualification boundary; Continuation 057 governance records.
- Supersedes record: DEC-PRIME-PHASE15-056

## DEC-PRIME-PHASE15-058

- Date: 2026-08-14
- Record or decision ID: DEC-PRIME-PHASE15-058
- Status: CLOSED
- Decision or event: Establish the spec-compliant trusted-host local identity flow on the existing persistent Atlas installation. Keep the browser secret-free: the browser creates a 120-second SIGN_IN or STEP_UP challenge, the Atlas host helper approves it with the separate local identity secret, and Core redeems the browser-bound nonce into ordinary session/CSRF state.
- Rationale: The existing operator password must not be read, rotated, or replaced. A separate high-entropy host-held secret and purpose-isolated challenge lifecycle preserve the existing operator identity while keeping approval outside the browser. The flow was qualified through the real private Core/UI, including fail-closed negatives and Core restart recovery, without creating disposable state or changing public exposure.
- Affected areas: local identity migration/service/API/UI; Atlas host approval helper; persistent Core image/service; browser authentication and step-up qualification; Continuation 058 evidence and governed records.
- Supersedes record: DEC-PRIME-PHASE15-057

## DEC-PRIME-PHASE15-059

- Date: 2026-08-15
- Record or decision ID: DEC-PRIME-PHASE15-059
- Status: CLOSED
- Decision or event: Rebuild the existing persistent PRIME Core image through the approved Atlas systemd/container topology so the safe browser wave exercises the actual current implementation. Promote only directly supported product states: DOD-056 metadata continuity is user-verified; DOD-026, DOD-027, DOD-047, and DOD-049 advance to PARTIAL; DOD-048 remains shell-only; DOD-005 and R-056 remain gated.
- Rationale: The running service initially imported the prior image, so checkout edits were not live despite the canonical repository mount. The same persistent state mount and service identity were preserved while the image was rebuilt and swapped; metadata was tested through the real UI across Core restart and restored exactly. No disposable database/project/Node/browser profile, public exposure, or unrelated service change was used.
- Affected areas: Core Usage endpoint; reliability Backup diagnostics; project metadata UI/API; mobile navigation CSS; focused safe-wave regression; Continuation 058/059 evidence; governed records.
- Supersedes record: DEC-PRIME-PHASE15-058

## DEC-PRIME-PHASE15-060

- Date: 2026-08-15
- Record or decision ID: DEC-PRIME-PHASE15-060
- Status: CLOSED
- Decision or event: Establish runtime build provenance in the existing persistent PRIME Core image/service path and qualify only safe local product behavior through the real browser. Preserve the Atlas topology and keep aggregate qualification, DOD-005, high-risk rows, external boundaries, R-056, Phase 15 completion, V1, and deployment gated.
- Rationale: The persistent service initially imported its prior image despite the canonical checkout mount. Build-time identity and health/operator exposure provide truthful runtime evidence; the existing database/environment boundary does not permit the aggregate qualifier to run safely without substitute state. The browser wave advanced bounded UI evidence and repaired narrow-screen diagnostics.
- Affected areas: Core build metadata; health/operator state; persistent Core image/service; responsive UI diagnostics; focused regression; Continuation 060 evidence and governed records.
- Supersedes record: DEC-PRIME-PHASE15-059

## DEC-PRIME-PHASE15-061

- Date: 2026-08-15
- Record or decision ID: DEC-PRIME-PHASE15-061
- Status: CLOSED
- Decision or event: Publish Continuation 061 as PARTIAL with the final qualified implementation `6dd5d805` and persistent runtime image `animus-prime-core:continuation-061-local-product3`. Treat the authenticated snapshot repair, persistent restart recovery, and safe product/API boundaries as qualified; keep browser qualification blocked, DOD-005 parked, R-056 open, and deployment unperformed.
- Rationale: The first real API probe found a user-impacting snapshot crash that structural tests did not catch. Fixing and requalifying the persistent image produced a truthful product boundary without modifying persistent project data or substituting an environment. The approved browser tool cannot currently start because its bundled server lacks Playwright, so browser claims remain unpromoted.
- Affected areas: persistent Core image/service; snapshot/progress alignment; Notifications; Backup controls; Continuation 061 evidence and governed records.
- Supersedes record: DEC-PRIME-PHASE15-060

## DEC-PRIME-PHASE15-062

- Date: 2026-08-15
- Record or decision ID: DEC-PRIME-PHASE15-062
- Status: CLOSED
- Decision or event: Publish Continuation 062 as PARTIAL after recovering the existing external gstack browser harness and qualifying the persistent Atlas PRIME operator journey. Promote DOD-027 and DOD-048 only for their directly exercised boundaries; preserve DOD-005 as parked, keep high-risk registration/restore and external/provider work open, keep R-056 open, and do not deploy.
- Rationale: The existing harness was present and usable once invoked from its local installation root with its pinned Playwright dependency and persistent state. The real browser reached the persistent 061 Core through the existing private SSH forward, and the reversible canonical Node outage demonstrated usable degraded operation, fail-closed Node control, restoration, and unchanged authority state without substitute resources or public exposure.
- Affected areas: Continuation 062 browser evidence; product alignment and gap-burndown records; append-only project state; persistent Atlas operator qualification.
- Supersedes record: DEC-PRIME-PHASE15-061

## DEC-PRIME-PHASE15-063

- Date: 2026-08-15
- Record or decision ID: DEC-PRIME-PHASE15-063
- Status: CLOSED
- Decision or event: Publish Continuation 063 as PARTIAL after restoration-bounded qualification of the existing persistent product. Preserve the canonical Qualification Project and promote no new requirement because lifecycle, correction-positive, export/restore, onboarding, authority, Goal, remove/archive/delete, and release workflows were not safely available as supported browser paths.
- Rationale: The UI's generic protected-action shell safely refuses without a specific lifecycle workflow, and the remaining Class-B/destructive paths lack legitimate durable targets or proven inverses. Empty correction and incomplete backup preflight failed closed without mutation. The exact canonical state and runtime provenance were rechecked after every exercised path.
- Affected areas: Continuation 063 evidence; product alignment/burndown remaining-gap wording; append-only project records.
- Supersedes record: DEC-PRIME-PHASE15-062

## DEC-PRIME-PHASE15-064

- Date: 2026-08-15
- Record or decision ID: DEC-PRIME-PHASE15-064
- Status: CLOSED
- Decision or event: Publish Continuation 064 as PARTIAL after implementing the authorized explicit operator workflows and qualifying them through the genuine persistent Atlas Core-served UI. Keep canonical destructive actions, positive Class-B target creation, DOD-005, R-056, Phase 16, and deployment outside scope.
- Rationale: The persistent product now has explicit preflight/action boundaries instead of a generic protected-action shell. PAUSE survived a real Core restart, RESUME and completion-review cancel restored the canonical project to ACTIVE, and delete refused wrong-target input while requiring recent step-up. The existing project, repository, Node, PostgreSQL, Hindsight, and authority state were preserved without manufacturing evidence.
- Affected areas: lifecycle preflight/action migration and service; Core API; web UI; Goal and authority controls; persistent Core image; Continuation 064 evidence and governed records.
- Supersedes record: DEC-PRIME-PHASE15-063

## DEC-PRIME-PHASE15-065

- Date: 2026-08-15
- Record or decision ID: DEC-PRIME-PHASE15-065
- Status: CLOSED
- Decision or event: Publish Continuation 065 as PARTIAL after completing the bounded local security-negative and refusal qualification wave on the persistent Atlas product. Keep all positive/destructive target-gated work, DOD-005, DOD-081, R-056, Phase 15 completion, V1 declaration, Phase 16, and deployment outside scope.
- Rationale: The live product proved the requested no-mutation boundaries and one Goal-protection defect was repaired at the smallest clause-linked point. The canonical project returned to ACTIVE / ONLINE / CURRENT / NORMAL, Goal identity/hash remained unchanged, the approved authority files were not rewritten, and no synthetic resource or public exposure was used. A safe authority-adoption observation advanced onboarding metadata, so the exact pre-probe values were restored and the side effect was recorded as a remaining product concern.
- Affected areas: CoreService Goal protection; focused regression; persistent Core image; local browser/API qualification; Continuation 065 evidence; append-only governed records.
- Supersedes record: DEC-PRIME-PHASE15-064


## DEC-PRIME-PHASE15-066

- Date: 2026-08-15
- Record or decision ID: DEC-PRIME-PHASE15-066
- Status: CLOSED
- Decision or event: Publish Continuation 066 as PARTIAL with no governed release-blocker reduction after classifying every open burndown item against actual Atlas resources and frozen acceptance boundaries.
- Rationale: The current persistent product and evidence already cover the completed negative/refusal boundaries. Remaining local items require legitimate durable targets or broad unbounded implementation; remaining external items require unavailable approved integrations, hosts, devices, or capabilities. No synthetic state, public exposure, or scope expansion was used.
- Affected areas: Continuation 066 evidence; .agent directive/outcome/learning/record state; current release-blocker classification.
- Supersedes record: DEC-PRIME-PHASE15-065

## DEC-PRIME-PHASE15-067

- Date: 2026-08-15
- Record or decision ID: DEC-PRIME-PHASE15-067
- Status: CLOSED
- Decision or event: Publish Continuation 067 as PARTIAL/BLOCKED after the bounded PRIME runtime Notion check found no approved runtime credential source.
- Rationale: PRIME explicitly requires NOTION_READONLY_KEY from the approved MyAssistant path and stores only env/myassistant/notion-readonly. The live Core process had no source variable and no credential-reference state file; the in-process registry failed closed with SOURCE_ABSENT and UNCONFIGURED. The assistant-side Notion connector was deliberately not treated as product evidence. No code, runtime, persistent data, network exposure, or qualification target changed.
- Affected areas: Continuation 067 evidence; append-only .agent records; exact PRIME runtime Notion prerequisite.
- Supersedes record: DEC-PRIME-PHASE15-066
## DEC-PRIME-PHASE15-068

- Date: 2026-08-16
- Record or decision ID: DEC-PRIME-PHASE15-068
- Status: CLOSED
- Decision or event: Publish Continuation 068 as PARTIAL/BLOCKED after bounded qualification of the existing persistent Hindsight environment.
- Rationale: Hindsight health, private identity, PRIME bank isolation, and recall are real, but Reflect fails with the exact openai/routerbot-local tool-calling capability error and the PRIME bank contains no Mental Models. DOD-068/R-054 remain open because retain/recall evidence alone cannot satisfy the frozen Hindsight semantics clause. No Hindsight state, provider configuration, product code, runtime, or network state was changed.
- Affected areas: Continuation 068 evidence; append-only .agent records; exact Hindsight operator prerequisite.
- Supersedes record: DEC-PRIME-PHASE15-067
## DEC-PRIME-PHASE15-069

- Date: 2026-08-16
- Record or decision ID: DEC-PRIME-PHASE15-069
- Status: CLOSED
- Decision or event: Publish Continuation 069 as PARTIAL/BLOCKED after the approved PARAGON endpoint passed authentication, model discovery, ordinary completion, and structured JSON but failed the required function/tool-calling smoke.
- Rationale: The endpoint returned HTTP 200 with no tool_calls and explicitly said the harmless probe tool was unavailable. This is an exact provider capability boundary. The directive required stopping before changing PRIME Core or Hindsight when the PARAGON tool-call smoke failed. No persistent state, product code, provider profile, bank, network, or qualification target was changed.
- Affected areas: Continuation 069 evidence; append-only .agent directive/outcome/learning/record state; exact PARAGON tool-calling prerequisite.

- Supersedes record: DEC-PRIME-PHASE15-068
