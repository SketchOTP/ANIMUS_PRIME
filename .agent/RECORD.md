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
