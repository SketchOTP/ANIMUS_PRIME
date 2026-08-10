# Project Outcome Ledger Template

After adoption, this append-only ledger records results for project directives. Every live outcome must reference one local directive ID.

## Entry schema after adoption

Use live outcome headings only after adoption. The following schema is instructional and is not a live entry:

```markdown
## <local-directive-id> - <outcome-state>

- Outcome ID: <unique outcome record ID>
- Supersedes outcome: <outcome ID or none>
- Closed: <ISO-8601 timestamp with timezone>
- Acceptance: <MET | PARTIAL | NOT MET>
- Summary: <concise result>
- Changed areas: <paths or none>
- Validation:
  - <command or check> - <PASSED | FAILED | NOT RUN | NOT APPLICABLE | BLOCKED>
- Remaining risks: <risks or none>
- Blockers: <blockers or none>
- Follow-up directive: <ID or none>
```

Allowed adopted-project outcome states: `COMPLETE`, `PARTIAL`, `BLOCKED`, `FAILED`, `CANCELLED`, `SUPERSEDED`. Do not rewrite earlier entries; append corrections referencing the original.

## D-PRIME-PHASE0-001 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE0-001
- Supersedes outcome: none
- Closed: 2026-08-10T16:40:00Z
- Acceptance: PARTIAL
- Summary: Phase 0 source lock, authority package, contracts, dependency pins, threat model, Hindsight adapter probe, recovery smoke, and qualification evidence passed. The overall directive remains active for Phases 1–15.
- Changed areas: baseline, authority-template/v1, contracts, dependencies, threat-model, docs, tests/phase0, src/prime_memory_adapter.py, .agent
- Validation:
  - python3 -m pytest tests/phase0 -q - PASSED
  - python3 scripts/validate_governance.py --mode ADOPTED - PASSED
  - python3 authority-template/v1/scripts/validate_governance.py --mode TEMPLATE - PASSED
  - docker/PostgreSQL/pgvector/Hindsight qualification - PASSED
  - Phase 0 qualification record - PASSED
- Remaining risks: Feature phases 1–15 are not implemented or qualified.
- Blockers: none
- Follow-up directive: none

## D-PRIME-PHASE0-001 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE1-001
- Supersedes outcome: OUT-PRIME-PHASE0-001
- Closed: 2026-08-10T16:55:00Z
- Acceptance: PARTIAL
- Summary: Phase 1 Core substrate implemented and qualified; overall Phase 0–15 directive remains active.
- Changed areas: apps/core, src/prime_core, migrations/prime, tests/phase1, Dockerfile.core, docker-compose.phase1.yml, requirements-phase1.txt, docs
- Validation:
  - pytest tests/phase0 tests/phase1 -q - PASSED (12 tests)
  - scripts/phase1_qualify.py - PASSED
  - pinned Docker Core build and live/readiness health - PASSED
  - PostgreSQL schema backup/restore smoke - PASSED
- Remaining risks: Phases 2–15 are not implemented or qualified.
- Blockers: none
- Follow-up directive: none
