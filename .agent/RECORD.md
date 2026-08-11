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
