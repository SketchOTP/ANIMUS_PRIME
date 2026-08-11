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
