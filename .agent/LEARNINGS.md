# Project Learnings Template

After adoption, use this append-only file for durable, verified project knowledge only.

## Entry guidance after adoption

Each live entry should include:

- Learning ID.
- Date.
- Fact or lesson.
- Evidence location.
- Confidence: `VERIFIED` or `PROVISIONAL`.
- Scope.
- Supersedes or superseded-by reference when applicable.

Do not add live entries to this template. Exclude temporary narration, raw logs, full source files, secrets, unsupported guesses, and facts already obvious from stable project documentation.

## L-PRIME-PHASE0-001

- Date: 2026-08-10
- Learning ID: L-PRIME-PHASE0-001
- Fact or lesson: Hindsight 0.6.1 may return a successful retain response while provider extraction stores no memory; PRIME must verify a durable, recallable postcondition and expose DEGRADED when it is absent.
- Evidence location: evidence/phase0/qualification-report.md; src/prime_memory_adapter.py
- Confidence: VERIFIED
- Scope: PRIME Hindsight adapter and all future memory writes.
- Supersedes learning: none

## L-PRIME-PHASE15-001

- Date: 2026-08-10
- Learning ID: L-PRIME-PHASE15-001
- Fact or lesson: Phase-15 remediation is governed by the individual R-031 through R-056 qualification ledger; implementation presence or automated tests alone cannot move a requirement to VERIFIED, and unavailable native/live prerequisites must be recorded exactly rather than simulated.
- Evidence location: docs/phase15-remediation-qualification-ledger.yaml; evidence/phase15/remediation-qualification-003.md; attached Phase 15 Remediation Continuation 004 instruction.
- Confidence: VERIFIED
- Scope: Phase-15 remediation, release gating, and all future qualification runs.
- Supersedes learning: none

## L-PRIME-PHASE15-002

- Date: 2026-08-10
- Learning ID: L-PRIME-PHASE15-002
- Fact or lesson: The canonical repository has progressed beyond the original Phase-0 skeleton: apps, src, migrations, packaging, tests, scripts, evidence, contracts, baseline exports, and phase records must all remain discoverable in the maintained repository map.
- Evidence location: .agent/REPO_MAP.md; git ls-files; docs/phase15-remediation-qualification-ledger.yaml.
- Confidence: VERIFIED
- Scope: Repository navigation and governance maintenance.
- Supersedes learning: none

## L-PRIME-PHASE15-003

- Date: 2026-08-10
- Learning ID: L-PRIME-PHASE15-003
- Fact or lesson: A skipped PostgreSQL integration test is not release evidence; it must retain its affected requirement mapping, exact missing environment, release-blocking effect, and deterministic qualification method until exercised.
- Evidence location: docs/phase15-skipped-test-inventory.md; Continuation 005 qualification directive.
- Confidence: VERIFIED
- Scope: Phase-15 skipped-test handling and all requirement-level release decisions.
- Supersedes learning: none

## L-PRIME-PHASE15-004

- Date: 2026-08-10
- Learning ID: L-PRIME-PHASE15-004
- Fact or lesson: Evidence metadata and retraction can be implemented locally without proving R-046/R-047; PostgreSQL migration, parser/index, citation, backup/restore, and live project-isolation evidence remain separate qualification obligations.
- Evidence location: evidence/phase15/R-046-R-047-implementation-preflight.md; src/prime_core/history_service.py; migrations/prime/0015_evidence_lifecycle.sql.
- Confidence: VERIFIED
- Scope: R-046/R-047 implementation and Phase-15 evidence qualification.
- Supersedes learning: none
