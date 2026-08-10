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
