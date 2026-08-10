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

## D-PRIME-PHASE0-001 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE2-001
- Supersedes outcome: OUT-PRIME-PHASE1-001
- Closed: 2026-08-10T17:05:00Z
- Acceptance: PARTIAL
- Summary: Phase 2 Node/repository read-only control plane implemented and qualified; overall directive remains active.
- Changed areas: apps/node, src/prime_node, migrations/prime/0002_nodes.sql, Dockerfile.node, tests/phase2, docs
- Validation:
  - pytest tests/phase0 tests/phase1 tests/phase2 - PASSED (13 tests in the qualification run)
  - phase1/phase2 migration qualification - PASSED
  - Core and Node pinned container build and health - PASSED
- Remaining risks: Windows native packaging and full repository compatibility matrix continue through later phases.
- Blockers: none
- Follow-up directive: none

## D-PRIME-PHASE0-001 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE3-001
- Supersedes outcome: OUT-PRIME-PHASE2-001
- Closed: 2026-08-10T17:20:00Z
- Acceptance: PARTIAL
- Summary: Phase 3 onboarding, authority provisioning and approved goal revisions implemented and qualified; overall directive remains active.
- Changed areas: src/prime_core/authority.py, migrations/prime/0003_onboarding.sql, tests/phase3, apps/core, docs
- Validation:
  - pytest tests/phase0 tests/phase1 tests/phase2 tests/phase3 - PASSED (15 tests)
  - Phase 1/2/3 migration qualification - PASSED
- Remaining risks: Phases 4–15 remain unimplemented and unqualified.
- Blockers: none
- Follow-up directive: none

## D-PRIME-PHASE0-001 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE4-001
- Supersedes outcome: OUT-PRIME-PHASE3-001
- Closed: 2026-08-10T17:35:00Z
- Acceptance: PARTIAL
- Summary: Phase 4 deterministic repository index and source freshness foundation implemented and qualified; overall directive remains active.
- Changed areas: src/prime_core/indexer.py, migrations/prime/0004_indexing.sql, tests/phase4, apps/core, docs
- Validation:
  - pytest tests/phase4 - PASSED
  - phase4 migration qualification - PASSED
  - Phase 0–3 prior qualification records retained - PASSED
- Remaining risks: Hindsight memory and later feature phases remain unimplemented.
- Blockers: none
- Follow-up directive: none
