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

## L-PRIME-PHASE15-010

- Date: 2026-08-11
- Learning ID: L-PRIME-PHASE15-010
- Fact or lesson: Node identity state must be constructed from environment at instance creation, not captured in dataclass class defaults; otherwise test order or service reuse can silently point multiple Node instances at one state file. Native packaging must keep identity/configuration outside the repository and make repair idempotent.
- Evidence location: src/prime_node/config.py; packaging/node/install-node.sh; packaging/node/install-node.ps1; tests/phase2/test_node_continuation009.py; evidence/phase15/R-031-R-034-implementation-closure-009.md.
- Confidence: VERIFIED
- Scope: R-031–R-034 Node lifecycle and packaging.
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

## L-PRIME-PHASE15-005

- Date: 2026-08-11
- Learning ID: L-PRIME-PHASE15-005
- Fact or lesson: A Git bundle created directly from a live repository can be empty when the selected checkpoint is still reachable from a normal ref. PRIME checkpoint preservation must pack the selected commit graph into an isolated temporary object store before creating the retained bundle, and must verify the retained hash/status independently after ref removal and GC.
- Evidence location: src/prime_core/git_history.py; tests/phase11/test_history_primitives.py; evidence/phase15/R-049-git-checkpoint-implementation.md
- Confidence: VERIFIED
- Scope: R-049 Git checkpoint preservation and Time Lens historical storage.
- Supersedes learning: none

## L-PRIME-PHASE15-006

- Date: 2026-08-11
- Learning ID: L-PRIME-PHASE15-006
- Fact or lesson: A historical Git selector cannot safely include Evidence merely because it exists today. Evidence must carry an explicit source revision association; otherwise Time Lens must exclude it at that commit and report missing source truth rather than infer historical availability.
- Evidence location: migrations/prime/0016_historical_evidence.sql; src/prime_core/history_service.py; tests/phase11/test_history.py
- Confidence: VERIFIED
- Scope: R-046–R-050 Evidence provenance, Time Lens cutoff fidelity, and historical Ask.
- Supersedes learning: L-PRIME-PHASE15-004

## L-PRIME-PHASE15-007

- Date: 2026-08-11
- Learning ID: L-PRIME-PHASE15-007
- Fact or lesson: Historical lifecycle evidence must be append-only at the event-observation boundary. A unique key containing only artifact identity and source revision would overwrite the original fact when a later retraction/correction occurs; lifecycle snapshots must include the observation timestamp and use conflict-safe insertion.
- Evidence location: migrations/prime/0018_historical_snapshot_immutability.sql; src/prime_core/history_primitives.py; tests/phase11/test_history.py
- Confidence: VERIFIED
- Scope: R-047/R-048 citation mutation, Evidence retraction, memory correction, Notion projection, and Time Lens reconstruction.
- Supersedes learning: none

## L-PRIME-PHASE15-008

- Date: 2026-08-11
- Learning ID: L-PRIME-PHASE15-008
- Fact or lesson: A PRIME continuity backup is a multi-component logical checkpoint, not a database dump. The recoverable artifact must preserve canonical PostgreSQL rows, managed Evidence bytes, retained PRIME-owned Git bundles, source-ledger rebuild inputs, configuration references, component hashes, and explicit fidelity/limitation labels while excluding secrets and repository-source claims.
- Evidence location: src/prime_core/backup_service.py; migrations/prime/0020_continuity_capacity.sql; evidence/phase15/R-042-R-045-implementation-closure-008.md
- Confidence: VERIFIED
- Scope: R-042–R-044 backup, restore, Hindsight continuity, Evidence, historical state, Git checkpoints, and recovery reporting.
- Supersedes learning: none

## L-PRIME-PHASE15-009

- Date: 2026-08-11
- Learning ID: L-PRIME-PHASE15-009
- Fact or lesson: Restoring managed Evidence or PRIME-owned Git bundles into a clean environment requires rewriting their restored storage locators; retaining the original source-host path makes metadata appear restored while content remains unavailable.
- Evidence location: src/prime_core/backup_service.py; the Continuation 008 clean-install fixture recorded in evidence/phase15/R-042-R-045-implementation-closure-008.md
- Confidence: VERIFIED
- Scope: R-043/R-044 restore semantics and R-046–R-050 backup regression protection.
- Supersedes learning: none
