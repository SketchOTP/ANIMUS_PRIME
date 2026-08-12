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

## D-PRIME-PHASE0-001 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE5-001
- Supersedes outcome: OUT-PRIME-PHASE4-001
- Closed: 2026-08-10T17:50:00Z
- Acceptance: PARTIAL
- Summary: Phase 5 PRIME-owned Hindsight memory ledger and correction semantics implemented and qualified; overall directive remains active.
- Changed areas: src/prime_core/memory_service.py, migrations/prime/0005_memory.sql, tests/phase5, apps/core, docs
- Validation:
  - pytest tests/phase5 - PASSED
  - phase5 migration qualification - PASSED
  - governance validation - PASSED
- Remaining risks: MCP exposure and later phases remain unimplemented.
- Blockers: none
- Follow-up directive: none

## D-PRIME-PHASE0-001 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE6-001
- Supersedes outcome: OUT-PRIME-PHASE5-001
- Closed: 2026-08-10T18:05:00Z
- Acceptance: PARTIAL
- Summary: Phase 6 canonical project-bound PRIME Memory MCP surface implemented and qualified; overall directive remains active.
- Changed areas: src/prime_core/mcp_service.py, migrations/prime/0006_mcp.sql, tests/phase6, apps/core, docs
- Validation:
  - pytest tests/phase6 - PASSED
  - phase6 migration qualification - PASSED
  - governance validation - PASSED
- Remaining risks: Notion, progress, UI, lifecycle and final release phases remain unimplemented.
- Blockers: none
- Follow-up directive: none

## D-PRIME-PHASE0-001 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE7-001
- Supersedes outcome: OUT-PRIME-PHASE6-001
- Closed: 2026-08-10T18:20:00Z
- Acceptance: PARTIAL
- Summary: Phase 7 managed Notion projection foundation implemented and qualified; overall directive remains active.
- Changed areas: src/prime_core/notion_service.py, migrations/prime/0007_notion.sql, tests/phase7, docs
- Validation:
  - pytest tests/phase7 - PASSED
  - phase7 migration qualification - PASSED
  - governance validation - PASSED
- Remaining risks: live Notion dispatch and later operator product phases remain.
- Blockers: none
- Follow-up directive: none

## D-PRIME-PHASE0-001 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE8-001
- Supersedes outcome: OUT-PRIME-PHASE7-001
- Closed: 2026-08-10T18:35:00Z
- Acceptance: PARTIAL
- Summary: Phase 8 deterministic GoalModel baseline and evidence-backed progress foundation implemented and qualified; overall directive remains active.
- Changed areas: src/prime_core/progress_service.py, migrations/prime/0008_progress.sql, tests/phase8, docs
- Validation:
  - pytest tests/phase8 - PASSED
  - phase8 migration qualification - PASSED
- Remaining risks: Ask/UI and final phases remain unimplemented.
- Blockers: none
- Follow-up directive: none

## D-PRIME-PHASE0-001 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE9-001
- Supersedes outcome: OUT-PRIME-PHASE8-001
- Closed: 2026-08-10T18:50:00Z
- Acceptance: PARTIAL
- Summary: Phase 9 project-scoped Ask/Search/activity foundation implemented and qualified; overall directive remains active.
- Changed areas: src/prime_core/intelligence_service.py, migrations/prime/0009_activity.sql, tests/phase9, docs
- Validation:
  - pytest tests/phase9 - PASSED
  - phase9 migration qualification - PASSED
- Remaining risks: Project Brain, lifecycle, UX and release qualification remain.
- Blockers: none
- Follow-up directive: none

## D-PRIME-PHASE0-001 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE10-001
- Supersedes outcome: OUT-PRIME-PHASE9-001
- Closed: 2026-08-10T19:05:00Z
- Acceptance: PARTIAL
- Summary: Phase 10 derived Project Brain topology foundation implemented and qualified; overall directive remains active.
- Changed areas: src/prime_core/brain_service.py, migrations/prime/0010_brain.sql, tests/phase10, docs
- Validation:
  - pytest tests/phase10 - PASSED
  - phase10 migration qualification - PASSED
- Remaining risks: historical evidence, lifecycle, UX and final release phases remain.
- Blockers: none
- Follow-up directive: none

## D-PRIME-PHASE0-001 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE11-001
- Supersedes outcome: OUT-PRIME-PHASE10-001
- Closed: 2026-08-10T19:20:00Z
- Acceptance: PARTIAL
- Summary: Phase 11 evidence, Time Lens and isolated Fork foundation implemented and qualified; overall directive remains active.
- Changed areas: src/prime_core/history_service.py, migrations/prime/0011_evidence_time_lens.sql, tests/phase11, docs
- Validation:
  - pytest tests/phase11 - PASSED
  - phase11 migration qualification - PASSED
- Remaining risks: lifecycle, reliability, UX and final release phases remain.
- Blockers: none
- Follow-up directive: none

## D-PRIME-PHASE0-001 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE12-001
- Supersedes outcome: OUT-PRIME-PHASE11-001
- Closed: 2026-08-10T19:35:00Z
- Acceptance: PARTIAL
- Summary: Phase 12 lifecycle and destructive safety foundation implemented and qualified; overall directive remains active.
- Changed areas: src/prime_core/lifecycle_service.py, migrations/prime/0012_lifecycle.sql, tests/phase12, docs
- Validation:
  - pytest tests/phase12 - PASSED
  - phase12 migration qualification - PASSED
- Remaining risks: backup/reliability, UX and final release phases remain.
- Blockers: none
- Follow-up directive: none

## D-PRIME-PHASE0-001 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE13-001
- Supersedes outcome: OUT-PRIME-PHASE12-001
- Closed: 2026-08-10T19:50:00Z
- Acceptance: PARTIAL
- Summary: Phase 13 backup metadata, diagnostics and queue-health foundation implemented and qualified; overall directive remains active.
- Changed areas: src/prime_core/reliability_service.py, migrations/prime/0013_reliability.sql, tests/phase13, docs
- Validation:
  - pytest tests/phase13 - PASSED
  - phase13 migration qualification - PASSED
- Remaining risks: packaging, final UX and full release suite remain.
- Blockers: none
- Follow-up directive: none

## D-PRIME-PHASE0-001 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE14-001
- Supersedes outcome: OUT-PRIME-PHASE13-001
- Closed: 2026-08-10T20:05:00Z
- Acceptance: PARTIAL
- Summary: Phase 14 accessible responsive operator web shell foundation implemented and qualified; overall directive remains active pending Phase 15.
- Changed areas: apps/web, tests/phase14, docs
- Validation:
  - pytest tests/phase14 - PASSED
  - phase14 shell qualification - PASSED
- Remaining risks: Phase 15 full-system qualification remains.
- Blockers: none
- Follow-up directive: none

## D-PRIME-PHASE0-001 - FAILED

- Outcome ID: OUT-PRIME-PHASE15-001
- Supersedes outcome: OUT-PRIME-PHASE14-001
- Closed: 2026-08-10T20:20:00Z
- Acceptance: NOT MET
- Summary: Phase 15 mechanical regression gate passed, but the approved V1 Definition-of-Done gate failed because the explicit normative gaps remain.
- Changed areas: scripts/phase15_qualify.py, evidence/phase15/qualification-report.md, .agent/phase-records/PHASE-15.md
- Validation:
  - clean full regression suite - PASSED (26 tests)
  - Phase 0–13 migration qualifications - PASSED
  - governance and baseline identity - PASSED
  - V1 Definition-of-Done reconciliation - FAILED
- Remaining risks: see evidence/phase15/qualification-report.md; no release/deployment occurred.
- Blockers: live Notion lifecycle, native Node/control plane packaging, complete UX, Tailscale, automated backup/capacity, historical Evidence, AI/end-to-end release evidence.
- Follow-up directive: none

## D-PRIME-PHASE0-001 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-001
- Supersedes outcome: OUT-PRIME-PHASE15-001
- Closed: 2026-08-10T20:35:00Z
- Acceptance: PARTIAL
- Summary: Reconciled the Phase-15 release failure to exact PRIME-SPEC requirements, reopened affected broad traceability rows, and created a granular R1-R7 remediation matrix. No V1 release claim was made.
- Changed areas: docs/requirements-traceability.yaml, docs/phase15-remediation-matrix.yaml, .agent/CURRENT.md, .agent/phase-records/PHASE-15.md
- Validation:
  - Notion source and Implementation Handoff re-read - PASSED
  - traceability reconciliation - PASSED
  - historical Phase-15 FAIL preserved - PASSED
- Remaining risks: all matrix rows R-031 through R-056 remain OPEN/IMPLEMENTING until implementation and evidence are qualified.
- Blockers: no external blocker asserted; live-provider and real cross-platform evidence require configured environments/credentials.
- Follow-up directive: none

## D-PRIME-PHASE0-001 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-002
- Supersedes outcome: OUT-PRIME-PHASE15-REMEDIATION-001
- Closed: 2026-08-10T20:55:00Z
- Acceptance: PARTIAL
- Summary: Implemented R1-R5 remediation foundations: Node lifecycle/protocol state, fixed-argv private Tailscale Serve control, server-side Notion API retry adapter, encrypted continuity bundle/preflight, Evidence validation/storage primitives, and historical checkpoint schema foundations. V1 remains failed pending real qualification evidence.
- Changed areas: apps/node, src/prime_node, src/prime_core, migrations/prime/0014_remediation_foundations.sql, packaging/node, tests, docs/phase15-remediation.md, scripts/phase15_qualify.py
- Validation:
  - python3 -m pytest tests -q - PASSED (20 passed, 15 skipped due missing psycopg/qualification database)
  - focused remediation tests - PASSED (10 tests)
  - python3 scripts/validate_governance.py --mode ADOPTED - PASSED
  - python3 scripts/phase15_qualify.py - FAILED (DB qualifications unavailable; matrix rows R-031 through R-056 still open)
- Remaining risks: live Notion provider, real Linux/Windows Node, actual Tailscale tailnet, backup/restore drills, complete historical reconstruction, complete UX, and AI/end-to-end evidence remain unverified.
- Blockers: local qualification environment lacks psycopg/PostgreSQL; no configured live Notion/Tailscale/Linux+Windows evidence environments were asserted.
- Follow-up directive: none

## D-PRIME-PHASE0-001 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-003
- Supersedes outcome: OUT-PRIME-PHASE15-REMEDIATION-002
- Closed: 2026-08-10T21:05:00Z
- Acceptance: PARTIAL
- Summary: Expanded the operator UX shell and added authenticated Core remote-access status/configuration plus encrypted backup/preflight routes. These surfaces report explicit degraded/authentication states and do not claim V1 completion.
- Changed areas: apps/web/index.html, apps/core/main.py, tests/phase14/test_web_shell.py
- Validation:
  - python3 -m pytest tests -q - PASSED (20 passed, 15 skipped)
  - python3 -m compileall -q apps src scripts tests - PASSED
  - python3 scripts/validate_governance.py --mode ADOPTED - PASSED
- Remaining risks: complete UX behavior, live Tailscale/Notion/backup operation, cross-platform Node, historical, AI and end-to-end evidence remain open.
- Blockers: PostgreSQL-backed qualification and configured external/cross-platform environments remain unavailable in this run.
- Follow-up directive: none

## D-PRIME-PHASE0-001 - FAILED

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-004
- Supersedes outcome: OUT-PRIME-PHASE15-REMEDIATION-003
- Closed: 2026-08-10T21:15:00Z
- Acceptance: NOT MET
- Summary: Clean PostgreSQL-backed Phase-15 mechanical qualification passed with 35 tests, all Phase 1–14 migration gates, governance, baseline identity, pinned Core/Node builds and healthy containers. The granular V1 release matrix remains open, so the release gate correctly remains failed.
- Changed areas: evidence/phase15/remediation-qualification-001.md, .agent/OUTCOMES.md
- Validation:
  - clean PostgreSQL full test tree - PASSED (35 tests)
  - Phase 1–14 qualification sequence - PASSED
  - Core/Node image build and health - PASSED
  - phase15 release remediation matrix - FAILED (R-031 through R-056 open)
- Remaining risks: all unresolved requirements listed in evidence/phase15/remediation-qualification-001.md; no deployment or V1 release claim.
- Blockers: real cross-platform, live-provider, remote-access, recovery, historical, UX and AI/end-to-end evidence is not yet qualified.
- Follow-up directive: none

## D-PRIME-PHASE0-001 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-005
- Supersedes outcome: OUT-PRIME-PHASE15-REMEDIATION-004
- Closed: 2026-08-10T21:25:00Z
- Acceptance: PARTIAL
- Summary: Added the Core-side bounded Node control-plane client with protocol identity headers, TLS CA validation and optional client certificate support, completing the local R1 client/server contract foundation.
- Changed areas: src/prime_core/node_client.py, tests/phase2/test_node_client.py, src/prime_core/remote_access_service.py
- Validation:
  - focused Node client/server and remote-access tests - PASSED (4 tests)
  - git diff --check - PASSED
- Remaining risks: real TLS/mTLS, Linux/Windows native service, restart/reconnect, version upgrade and cross-platform evidence remain open; V1 release remains failed.
- Blockers: no supported Windows environment or live private control-plane qualification environment was asserted.
- Follow-up directive: none

## D-PRIME-PHASE0-001 - FAILED

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-006
- Supersedes outcome: OUT-PRIME-PHASE15-REMEDIATION-005
- Closed: 2026-08-10T21:35:00Z
- Acceptance: NOT MET
- Summary: Reran the complete Phase-15 mechanical gate from clean commit b03d993 on a fresh PostgreSQL state. 36 tests and all Phase 1–14 qualification checks passed; every open release-matrix requirement correctly kept the V1 release gate failed.
- Changed areas: evidence/phase15/remediation-qualification-002.md, .agent/OUTCOMES.md
- Validation:
  - clean PostgreSQL phase15_qualify run - FAILED only at V1 matrix gate; mechanical checks PASSED
  - full regression suite - PASSED (36 tests)
  - Phase 1–14 qualification sequence - PASSED
  - disposable qualification stack teardown - PASSED
- Remaining risks: R-031 through R-056 remain open; no V1 release/deployment claim.
- Blockers: real cross-platform, live-provider, remote-access, recovery, historical, complete UX and AI/end-to-end evidence remains unqualified.
- Follow-up directive: none

## D-PRIME-PHASE0-001 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-007
- Supersedes outcome: OUT-PRIME-PHASE15-REMEDIATION-006
- Closed: 2026-08-10T22:42:18Z
- Acceptance: PARTIAL
- Summary: Added requirement-level qualification records for R-031 through R-056 and tightened the packaged Node entrypoint to fail closed without TLS/mTLS. A real local HTTPS/mTLS process qualified enrollment and authenticated heartbeat; the V1 gate remains failed because native Linux/Windows lifecycle and the other live evidence domains remain open.
- Changed areas: src/prime_node/config.py, apps/node/main.py, packaging/node, docker-compose.phase1.yml, tests/phase2/test_node.py, docs/phase15-remediation-matrix.yaml, docs/phase15-remediation-qualification-ledger.yaml, evidence/phase15/R-031-local-tls-mtls-process.md, .agent/CURRENT.md
- Validation:
  - focused Node tests - PASSED (4 tests)
  - compileall - PASSED
  - git diff --check - PASSED
  - real local HTTPS/mTLS process: PASSED for startup, client-cert enforcement, enrollment, and heartbeat
  - requirement-level release matrix: FAILED/OPEN by design; R-031 through R-056 are not verified
- Remaining risks: native Linux service/reboot, Windows service, live Notion, live Tailscale, backup/restore, historical fidelity, complete UX, AI, and full E2E evidence remain unqualified.
- Blockers: native Windows and configured external qualification environments are unavailable in this coding environment.
- Follow-up directive: none

## D-PRIME-PHASE0-001 - FAILED

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-008
- Supersedes outcome: OUT-PRIME-PHASE15-REMEDIATION-007
- Closed: 2026-08-10T22:48:00Z
- Acceptance: NOT MET
- Summary: Full disposable Phase-15 qualification passed mechanically on `0db5766d99fb8a2bbfb714b1dd64a298f3eaf131` with 38 tests and all Phase 1–14 gates, governance, baseline, and requirement-ledger checks passing. The V1 release gate correctly failed because R-031 through R-056 remain open.
- Changed areas: evidence/phase15/remediation-qualification-003.md, .agent/CURRENT.md, .agent/OUTCOMES.md
- Validation:
  - fresh Docker PostgreSQL/Core/Node qualification - PASSED
  - full test suite - PASSED (38 tests)
  - Phase 1–14 qualification sequence - PASSED
  - V1 requirement gate - FAILED as required while 26 rows remain OPEN
  - deployment - NOT PERFORMED
- Remaining risks: native Linux/Windows lifecycle, live Notion/Tailscale, backup/restore/capacity, historical, complete UX, AI, security, and full E2E evidence remain unqualified.
- Blockers: required native Windows and external-provider/device environments are not available in this coding environment.
- Follow-up directive: none

## D-PRIME-PHASE15-REMEDIATION-004 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-009
- Supersedes outcome: OUT-PRIME-PHASE15-REMEDIATION-008
- Closed: 2026-08-10T23:10:32Z
- Acceptance: PARTIAL
- Summary: Reconciled the Continuation 004 governance requirements. Added the continuation as a distinct directive, updated the mutable current-state record, corrected the R-031–R-056 ledger to the required per-record schema, added durable remediation learnings, and rebuilt the repository map from the current tracked repository. No requirement was marked VERIFIED and no V1 release or deployment claim was made.
- Changed areas: .agent/DIRECTIVES.md, .agent/CURRENT.md, .agent/LEARNINGS.md, .agent/OUTCOMES.md, .agent/REPO_MAP.md, docs/phase15-remediation-qualification-ledger.yaml, scripts/phase15_qualify.py
- Validation:
  - codebase-memory MCP index attempt; transport closed and documented local discovery fallback used - BLOCKED
  - python3 scripts/validate_governance.py --mode ADOPTED; final map validation was pending at record time - NOT RUN
  - R-031 through R-056 verification; no evidence was manufactured - NOT RUN
  - V1 release/deployment; release gate remains open and deployment was not authorized - NOT APPLICABLE
- Remaining risks: R-031 through R-056 remain IMPLEMENTING/OPEN pending their individual implementation and native/live qualification evidence.
- Blockers: native Windows, live Notion, live Tailscale, approved AI provider and other external qualification prerequisites remain unavailable or unqualified in this environment.
- Follow-up directive: none

## D-PRIME-PHASE15-REMEDIATION-004 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-010
- Supersedes outcome: OUT-PRIME-PHASE15-REMEDIATION-009
- Closed: 2026-08-10T23:12:00Z
- Acceptance: PARTIAL
- Summary: Corrected and validated the append-only governance reconciliation for Continuation 004. The repository now records the continuation directive, current state, durable learnings, actual repository map, and the required 26-record R-031–R-056 ledger schema. The project remains below V1 acceptance because no open requirement was promoted to VERIFIED.
- Changed areas: .agent/PROJECT_PROFILE.md, .agent/REPO_MAP.md, .agent/OUTCOMES.md
- Validation:
  - python3 scripts/validate_governance.py --mode ADOPTED - PASSED
  - ledger schema self-check for 26 records R-031 through R-056 - PASSED
  - python3 -m pytest tests -q - PASSED (23 passed, 15 skipped because host PostgreSQL qualification dependencies were unavailable)
  - git diff --check - PASSED
  - V1 release gate - NOT APPLICABLE (R-031 through R-056 remain OPEN/IMPLEMENTING)
- Remaining risks: native Linux/Windows lifecycle, live Notion/Tailscale, backup/restore/capacity, Evidence and historical fidelity, complete UX, AI, and fresh-install end-to-end evidence remain unqualified.
- Blockers: external qualification environments and credentials are still not available in this coding environment; no evidence was fabricated.
- Follow-up directive: none

## D-PRIME-PHASE15-REMEDIATION-005 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-011
- Supersedes outcome: OUT-PRIME-PHASE15-REMEDIATION-010
- Closed: 2026-08-10T23:55:00Z
- Acceptance: PARTIAL
- Summary: Executed Continuation 005 as a ledger-driven work cycle. Recorded all 15 skipped tests with requirement/environment/release-blocking mappings, added deterministic qualification procedures and the A/B/C queue, added Phase-15 status-count reporting, and advanced the R-046/R-047 Evidence implementation boundary in commit `22a85f8`. No requirement was promoted to VERIFIED; V1 remains FAIL and deployment was not performed.
- Changed areas: .agent/DIRECTIVES.md, .agent/CURRENT.md, .agent/LEARNINGS.md, .agent/REPO_MAP.md, .agent/OUTCOMES.md, apps/core/main.py, src/prime_core/evidence_validation.py, src/prime_core/history_service.py, migrations/prime/0015_evidence_lifecycle.sql, tests/phase11/test_evidence_validation.py, docs/phase15-remediation-queue.md, docs/phase15-skipped-test-inventory.md, docs/phase15-qualification-procedures.md, docs/requirements-traceability.yaml, evidence/phase15/R-046-R-047-implementation-preflight.md, scripts/phase15_qualify.py
- Validation:
  - codebase-memory MCP index attempt; transport closed and targeted local fallback used - BLOCKED
  - python3 scripts/validate_governance.py --mode ADOPTED - PASSED
  - python3 -m pytest tests -q -rs - PASSED (24 passed, 15 skipped; skipped PostgreSQL integration remains unproven)
  - python3 -m compileall -q apps src tests - PASSED
  - git diff --check - PASSED
  - phase15_qualify.py status reporting - PASSED for count emission; full qualification - FAILED because host psycopg/PRIME_PHASE1_DB_URL and R-031–R-056 evidence are unavailable
  - R-031–R-056 qualification - NOT RUN; counts IMPLEMENTING=26, OPEN=26, BLOCKED=0, VERIFIED=0; VERIFIED / 26 = 0/26
  - deployment - NOT PERFORMED
- Remaining risks: native Linux/Windows lifecycle, live Tailscale/Notion, backup/restore/capacity, PostgreSQL-backed Evidence/Time Lens, browser UX, approved AI, and full end-to-end evidence remain open.
- Blockers: host `psycopg` and `PRIME_PHASE1_DB_URL` are unavailable; required native/live provider/device/recovery environments remain unqualified.
- Follow-up directive: D-PRIME-PHASE15-REMEDIATION-005

## D-PRIME-PHASE15-REMEDIATION-006 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-012
- Supersedes outcome: OUT-PRIME-PHASE15-REMEDIATION-011
- Closed: 2026-08-11T00:26:43Z
- Acceptance: PARTIAL
- Summary: Executed Continuation 006 against the unchanged PRIME-SPEC-V1.0.0 baseline. Added separate qualification status for every R-031–R-056 row and advanced the first implementation-complete requirement: R-049 now preserves canonical Git checkpoints through isolated object packing, retained bundle hashing, ref removal, reflog expiry, and GC fixture coverage. Advanced the R-046–R-050 Evidence/history foundation with durable SourceReference linkage, explicit Evidence revision association, safe locators, bounded inert-text extraction, quota/annotation/link boundaries, historical cutoff context, and historical Ask context. No requirement was promoted to VERIFIED; V1 remains FAIL and deployment was not performed.
- Changed areas: .agent/CURRENT.md, .agent/DIRECTIVES.md, .agent/LEARNINGS.md, .agent/OUTCOMES.md, .agent/REPO_MAP.md, apps/core/main.py, docs/phase15-remediation-matrix.yaml, docs/phase15-remediation-qualification-ledger.yaml, docs/phase15-remediation-queue.md, docs/requirements-traceability.yaml, evidence/phase15/R-046-R-047-implementation-preflight.md, evidence/phase15/R-049-git-checkpoint-implementation.md, migrations/prime/0016_historical_evidence.sql, scripts/phase15_qualify.py, src/prime_core/evidence_validation.py, src/prime_core/git_history.py, src/prime_core/history_primitives.py, src/prime_core/history_service.py, src/prime_core/intelligence_service.py, tests/phase11/test_history.py, tests/phase11/test_history_primitives.py
- Validation:
  - Notion PRIME source page, handoff record, and Checkpoint 005 reread - PASSED
  - codebase-memory MCP index attempt - BLOCKED (`Transport closed`); targeted local fallback used and recorded
  - focused Evidence/history primitive tests - PASSED (6 tests without PostgreSQL)
  - clean disposable PostgreSQL migration and full regression - PASSED (42 tests)
  - governance validation - PASSED
  - compileall and git diff check - PASSED
  - complete Phase-15 mechanical runner from clean disposable PostgreSQL - PASSED through Phase 14, ledger, baseline, and release checks; V1 requirement checks correctly failed
  - R-049 release qualification - PARTIAL; PostgreSQL registration and full Time Lens qualification remain open
  - implementation convergence - `1/26` complete; `25/26` still incomplete
  - qualification status - `5 partial`, `21 blocked_by_environment`, `0 verified`
  - V1 release gate - FAILED as required; `VERIFIED / 26 = 0/26`
  - deployment - NOT PERFORMED
- Remaining risks: R-046–R-048 and R-050 still need full implementation and qualification; R-031–R-045, R-051–R-056 remain implementation-incomplete and/or native/live/recovery dependent; no V1 release claim is authorized.
- Blockers: native Windows/Linux lifecycle, live Tailscale/Notion, backup/restore/capacity, approved AI, browser acceptance, full historical PostgreSQL qualification, and aggregate E2E environments remain unqualified.
- Follow-up directive: D-PRIME-PHASE15-REMEDIATION-006

## D-PRIME-PHASE15-REMEDIATION-007 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-013
- Supersedes outcome: OUT-PRIME-PHASE15-REMEDIATION-012
- Closed: 2026-08-11T01:26:00Z
- Acceptance: PARTIAL
- Summary: Executed Continuation 007 against the unchanged PRIME-SPEC-V1.0.0 baseline. Closed local implementation for R-046 through R-050 in governed implementation commit `723809e`, with evidence/governance commit `a617ae5`, and preserved the separate implementation/qualification distinction. R-046/R-047/R-048/R-049/R-050 are now IMPLEMENTED; all five remain qualification `partial`, no row is VERIFIED, V1 remains FAIL, and deployment was not performed.
- Changed areas: apps/core/main.py, migrations/prime/0017_historical_revisions.sql, migrations/prime/0018_historical_snapshot_immutability.sql, migrations/prime/0019_evidence_parser_states.sql, src/prime_core/brain_service.py, src/prime_core/evidence_validation.py, src/prime_core/history_primitives.py, src/prime_core/history_service.py, src/prime_core/intelligence_service.py, src/prime_core/memory_service.py, src/prime_core/notion_service.py, src/prime_core/progress_service.py, src/prime_core/service.py, tests/phase11, docs/phase15-remediation-qualification-ledger.yaml, docs/phase15-remediation-matrix.yaml, docs/requirements-traceability.yaml, docs/phase15-remediation-queue.md, evidence/phase15/R-046-R-050-implementation-closure-007.md, .agent/CURRENT.md, .agent/DIRECTIVES.md, .agent/LEARNINGS.md, .agent/REPO_MAP.md
- Validation:
  - PRIME source page, Implementation Handoff Record, and Checkpoint 006 reread - PASSED
  - codebase-memory MCP index attempt - BLOCKED (`Transport closed`); targeted local fallback used
  - focused Evidence/security primitives - PASSED (7 tests without PostgreSQL)
  - Phase-11 PostgreSQL integration - PASSED (8 tests, including actual checkpoint registration/restart/ref removal/reflog expiry/GC, citation/retraction, Time Lens, and historical Brain)
  - clean disposable PostgreSQL full regression - PASSED (43 tests)
  - Python compileall - PASSED
  - git diff --check - PASSED
  - governance validation - PASSED before final outcome append; final post-append validation required
  - Phase 1 through Phase 14 mechanical qualification - PASSED in the clean Phase-15 run
  - R-046 through R-050 release qualification - PARTIAL; native/live parser-index, product citation, complete historical walkthrough, backup/restore, capacity, and isolation evidence remain open
  - implementation convergence - PASSED for this directive at `5/26` complete; `21/26` remain incomplete
  - qualification status - `5 partial`, `21 blocked_by_environment`, `0 verified`, `0 failed`
  - V1 release gate - FAILED as required; `VERIFIED / 26 = 0/26`
  - deployment - NOT PERFORMED
- Remaining risks: R-042 through R-045 backup/restore/capacity must consume the finalized Evidence/history object model; R-031 through R-045 and R-051 through R-056 still require local implementation and/or native/live/recovery qualification; R-046 through R-050 still require complete release evidence.
- Blockers: native Windows/Linux service environments, live Notion/Tailscale, off-machine backup/restore target, approved AI provider, browser acceptance context, and complete end-to-end environment are unavailable or unqualified; no evidence was fabricated.
- Follow-up directive: D-PRIME-PHASE15-REMEDIATION-007

## D-PRIME-PHASE15-REMEDIATION-008 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-016
- Supersedes outcome: OUT-PRIME-PHASE15-REMEDIATION-013
- Closed: 2026-08-11T02:08:00Z
- Acceptance: PARTIAL
- Summary: Finalized Continuation 008 after governed commits `7b5ef0a` (implementation) and `342fc58` (evidence/governance). R-042 through R-045 are IMPLEMENTED with qualification partial; R-046 through R-050 remain IMPLEMENTED with qualification partial; implementation convergence is 9/26, VERIFIED is 0/26, V1 remains FAIL, and deployment was not performed.
- Changed areas: docs/phase15-remediation-qualification-ledger.yaml, docs/phase15-remediation-qualification-queue.md, .agent/CURRENT.md, .agent/OUTCOMES.md
- Validation:
  - final adopted governance validation - PASSED
  - final compileall - PASSED
  - final diff check - PASSED
  - clean Phase-15 runner - PASSED mechanically through Phases 1–14 and 47 tests; VERIFIED requirement gate FAILED as required
  - implementation/qualification separation - PASSED
  - final worktree check - PASSED
  - V1 release gate - FAILED by design at 0/26 VERIFIED
  - deployment - NOT PERFORMED
- Remaining risks: separate off-machine target, fresh-install destructive safety and interrupted restore, live Hindsight loss/rebuild, sustained capacity/disk-pressure, native/live integrations, browser, AI, and aggregate end-to-end evidence remain unqualified.
- Blockers: system Python lacks psycopg; native Windows/Linux, live Notion/Tailscale/Hindsight, approved AI, browser, off-machine recovery target, and sustained capacity environments are unavailable or unqualified.
- Follow-up directive: D-PRIME-PHASE15-REMEDIATION-008

## D-PRIME-PHASE15-REMEDIATION-011 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-024
- Supersedes outcome: OUT-PRIME-PHASE15-REMEDIATION-016
- Closed: 2026-08-11T11:45:00Z
- Acceptance: PARTIAL
- Summary: Continuation 011 persistence correction adds atomic non-secret Notion lifecycle state snapshot/load and simulated restart coverage in `659fc3ce9659611e34dedf3d6e2b4b892088d355`. The R-037–R-041 local implementation boundary remains complete; live Notion qualification is blocked_by_environment, implementation convergence is 20/26, VERIFIED is 0/26, V1 remains FAIL, and deployment was not performed.
- Changed areas: `src/prime_core/notion_service.py`, `tests/phase7/test_notion_lifecycle.py`, `evidence/phase15/R-037-R-041-implementation-closure-011.md`, `.agent/CURRENT.md`
- Validation:
  - focused lifecycle tests - PASSED (`8 passed`)
  - focused lifecycle/API tests - PASSED (`11 passed`)
  - full local test suite - PASSED (`43 passed`, `17 skipped`)
  - compileall - PASSED
  - adopted governance validation - NOT RUN until final correction commit
  - live Notion provider lifecycle - NOT RUN
  - V1 release gate - FAILED by design at 0/26 VERIFIED
  - deployment - NOT PERFORMED
- Remaining risks: live Notion provider/access, actual block revision, source deletion/permission, long-running rollover, and aggregate Phase-15 evidence remain unqualified.
- Blockers: controlled live Notion workspace, codebase-memory transport, and remaining native/live/recovery/browser/AI release environments.
- Follow-up directive: D-PRIME-PHASE15-REMEDIATION-011

## D-PRIME-PHASE15-REMEDIATION-011 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-023
- Supersedes outcome: OUT-PRIME-PHASE15-REMEDIATION-016
- Closed: 2026-08-11T11:42:00Z
- Acceptance: PARTIAL
- Summary: Final validation correction for Continuation 011. The governed implementation commit `a4d22635f7036ca4f86029c8e681c08923aaf157`, evidence/governance commit `d1ade44e44558ec2b1c6e94368a05c84efe8bb5a`, and final correction commit are recorded. R-037–R-041 remain IMPLEMENTED with live qualification blocked_by_environment; implementation convergence is 20/26, VERIFIED is 0/26, V1 remains FAIL, and deployment was not performed.
- Changed areas: `.agent/CURRENT.md`, `.agent/OUTCOMES.md`
- Validation:
  - final adopted governance validation - PASSED
  - final full local test suite - PASSED (`42 passed`, `17 skipped`)
  - final compileall - PASSED
  - final diff check - PASSED
  - final worktree check - PASSED (clean)
  - live Notion provider/workspace/page lifecycle - NOT RUN
  - V1 release gate - FAILED by design at 0/26 VERIFIED
  - deployment - NOT PERFORMED
- Remaining risks: live Notion provider auth/access, actual block revision evidence, source permission/deletion/retraction qualification, long-running rollover, and aggregate Phase-15 release evidence remain unqualified.
- Blockers: controlled live Notion environment, codebase-memory transport, and the remaining native/live/recovery/browser/AI release environments.
- Follow-up directive: D-PRIME-PHASE15-REMEDIATION-011

## D-PRIME-PHASE15-REMEDIATION-011 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-022
- Supersedes outcome: OUT-PRIME-PHASE15-REMEDIATION-016
- Closed: 2026-08-11T11:38:59Z
- Acceptance: PARTIAL
- Summary: Continuation 011 closes the local implementation boundary for R-037 through R-041 at implementation commit `a4d22635f7036ca4f86029c8e681c08923aaf157`; evidence/governance commit `d1ade44e44558ec2b1c6e94368a05c84efe8bb5a`. Core-owned Notion credential references, Project Record creation/binding, targeted managed regions, user-content preservation, documentation source ordering, privacy/self-write controls, project-scoped read-only Knowledge Sources, source retraction/reconciliation, provider fault states, and idempotent managed history rollover are implemented and locally tested. Live Notion qualification remains blocked_by_environment; implementation convergence is 20/26, VERIFIED is 0/26, V1 remains FAIL, and deployment was not performed.
- Changed areas: `src/prime_core/notion_service.py`, `src/prime_core/notion_api.py`, `migrations/prime/0022_notion_lifecycle.sql`, `tests/phase7/test_notion_lifecycle.py`, `docs/requirements-traceability.yaml`, `docs/phase15-remediation-matrix.yaml`, `docs/phase15-remediation-qualification-ledger.yaml`, `evidence/phase15/R-037-R-041-implementation-closure-011.md`, `.agent/`
- Validation:
  - PRIME source and Implementation Handoff reread - PASSED
  - Checkpoint 010 workspace search found the recorded page; direct fetch returned `object_not_found` - NOT RUN as a live page read
  - codebase-memory MCP index - BLOCKED (`Transport closed`); targeted local fallback used
  - focused Notion lifecycle/API tests - PASSED (`10 passed`)
  - full local test suite - PASSED (`43 passed`, `17 skipped`)
  - compileall - PASSED
  - live Notion provider/workspace/page lifecycle - NOT RUN
  - adopted governance validation - NOT RUN until final evidence commit
  - V1 release gate - FAILED by design at 0/26 VERIFIED
  - deployment - NOT PERFORMED
- Remaining risks: live provider auth/access, actual Notion block revisions, outage/reconnect, page move/deletion, long-running rollover, backup restore of durable Notion rows, and full Phase-15 evidence remain unqualified.
- Blockers: live controlled Notion workspace, production adapter credentials/configuration, codebase-memory transport, PostgreSQL-dependent host environment, and aggregate release qualification environment.
- Follow-up directive: D-PRIME-PHASE15-REMEDIATION-011

## D-PRIME-PHASE15-REMEDIATION-010 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-021
- Supersedes outcome: OUT-PRIME-PHASE15-REMEDIATION-016
- Closed: 2026-08-11T11:25:00Z
- Acceptance: PARTIAL
- Summary: Final append-only correction for Continuation 010. R-035 and R-036 now record implementation commit `f72315271fbb3e60166784e9cb433711a2aeb900` and evidence/governance commit `b2bbf47aab0477518fdf57a7718457fd0b5cd1ed`; live Tailscale qualification remains blocked_by_environment, implementation convergence is 15/26, VERIFIED is 0/26, V1 remains FAIL, and deployment was not performed.
- Changed areas: docs/phase15-remediation-qualification-ledger.yaml, .agent/OUTCOMES.md
- Validation:
  - adopted governance validation after correction - NOT RUN until final commit
  - focused remote-access tests - PASSED (`5 passed`)
  - full local test suite - PASSED (`35 passed`, `17 skipped`)
  - compileall - PASSED
  - git diff check - PASSED
  - live signed-in Tailscale/approved second-device qualification - NOT RUN
  - V1 release gate - FAILED by design at 0/26 VERIFIED
  - deployment - NOT PERFORMED
- Remaining risks: live Serve HTTPS, second-device/private-path, daemon restart/recovery, Funnel/public exposure, and all previously recorded native/live/recovery/browser/AI/end-to-end evidence remain unqualified.
- Blockers: signed-in tailnet and approved second device, codebase-memory transport, system Python PostgreSQL dependency, native/live integrations, browser, AI, and aggregate release environment.
- Follow-up directive: D-PRIME-PHASE15-REMEDIATION-010

## D-PRIME-PHASE15-REMEDIATION-010 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-020
- Supersedes outcome: OUT-PRIME-PHASE15-REMEDIATION-016
- Closed: 2026-08-11T11:20:14Z
- Acceptance: PARTIAL
- Summary: Continuation 010 closes the local implementation boundary for R-035 and R-036 at implementation commit `f72315271fbb3e60166784e9cb433711a2aeb900`. The bounded Tailscale Serve adapter now has fixed allowlisted argv, actual-state vocabulary, loopback/public-bind safety, Funnel refusal, explicit PRIME ownership, persisted desired state, reconciliation, truthful private URL semantics, and authenticated Core routes. Live tailnet qualification remains blocked_by_environment; implementation convergence is 15/26; VERIFIED is 0/26; V1 remains FAIL; deployment was not performed.
- Changed areas: src/prime_core/remote_access_service.py, apps/core/main.py, tests/phase12/test_remote_access.py, docs/requirements-traceability.yaml, docs/phase15-remediation-matrix.yaml, docs/phase15-remediation-qualification-ledger.yaml, evidence/phase15/R-035-R-036-implementation-closure-010.md, .agent/CURRENT.md, .agent/DIRECTIVES.md, .agent/LEARNINGS.md, .agent/RECORD.md
- Validation:
  - PRIME source, Implementation Handoff Record, and Checkpoint 009 reread - PASSED
  - codebase-memory MCP index - BLOCKED (`Transport closed`); targeted local fallback used
  - focused remote-access tests - PASSED (`5 passed`)
  - full local test suite - PASSED (`35 passed`, `17 skipped`)
  - live signed-in Tailscale/approved second-device qualification - NOT RUN
  - V1 release gate - FAILED by design at 0/26 VERIFIED
  - deployment - NOT PERFORMED
- Remaining risks: live Serve HTTPS, second-device/private-path, daemon restart/recovery, Funnel/public exposure, native/live integrations, PostgreSQL-dependent checks, browser, AI, and aggregate end-to-end evidence remain unqualified.
- Blockers: codebase-memory transport, signed-in tailnet and approved second device, system Python PostgreSQL dependency, native/live integrations, browser, AI, and aggregate release environment.
- Follow-up directive: D-PRIME-PHASE15-REMEDIATION-010

## D-PRIME-PHASE15-REMEDIATION-009 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-019
- Supersedes outcome: OUT-PRIME-PHASE15-REMEDIATION-016
- Closed: 2026-08-11T04:02:00Z
- Acceptance: PARTIAL
- Summary: Final correction for Continuation 009. The R-031–R-034 ledger now records exact implementation commit `084ea85d19d3c56df6c14601e532e9bc346862b6` and exact evidence/governance commit `954dddf1de51b4a3d8450d4080707c1dfa63def0`; final adopted governance validation passed. Native qualification remains blocked_by_environment, implementation convergence is 13/26, VERIFIED is 0/26, V1 remains FAIL, and deployment was not performed.
- Changed areas: `docs/phase15-remediation-qualification-ledger.yaml`, `.agent/OUTCOMES.md`
- Validation:
  - final adopted governance validation - PASSED
  - final diff check - PASSED
  - focused Node/control-plane tests - PASSED (`6 passed`)
  - full local test suite - PASSED (`32 passed`, `17 skipped`)
  - native Linux/Windows and qualified private deployment - NOT RUN
  - V1 release gate - FAILED by design at 0/26 VERIFIED
  - deployment - NOT PERFORMED
- Remaining risks: native service/reboot/reconnect/upgrade evidence and all previously recorded live/recovery/browser/AI/end-to-end evidence remain unqualified.
- Blockers: native Windows/Linux hosts, qualified private deployment, PostgreSQL-dependent environment gaps, live integrations, browser, AI, and aggregate release environment.
- Follow-up directive: D-PRIME-PHASE15-REMEDIATION-009

## D-PRIME-PHASE15-REMEDIATION-009 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-018
- Supersedes outcome: OUT-PRIME-PHASE15-REMEDIATION-016
- Closed: 2026-08-11T03:55:00Z
- Acceptance: PARTIAL
- Summary: Continuation 009 closes the local implementation boundary for R-031 through R-034 at implementation commit `084ea85d19d3c56df6c14601e532e9bc346862b6`. Node identity/health/protocol lifecycle, secure root boundaries, bounded diagnostics/snapshots, private-bind/TLS controls, Linux systemd packaging, Windows service registration, and lifecycle migration are implemented. R-031–R-034 remain qualification `blocked_by_environment`; R-042–R-050 remain IMPLEMENTED with partial qualification; implementation convergence is 13/26; VERIFIED is 0/26; V1 remains FAIL; deployment was not performed.
- Changed areas: `src/prime_node`, `apps/node/main.py`, `src/prime_core/node_client.py`, `migrations/prime/0021_node_lifecycle.sql`, `packaging/node`, `tests/phase2/test_node_continuation009.py`, `docs/phase15-remediation-qualification-ledger.yaml`, `docs/phase15-remediation-matrix.yaml`, `docs/requirements-traceability.yaml`, `evidence/phase15/R-031-R-034-implementation-closure-009.md`, `.agent/CURRENT.md`, `.agent/DIRECTIVES.md`, `.agent/LEARNINGS.md`, `.agent/RECORD.md`, `.agent/REPO_MAP.md`
- Validation:
  - PRIME source, Implementation Handoff, and Checkpoint 008 reread - PASSED
  - codebase-memory MCP index - BLOCKED (`Transport closed`); targeted local fallback used
  - focused Node/control-plane tests - PASSED (`6 passed`)
  - full local test suite - PASSED (`32 passed`, `17 skipped`)
  - compileall - PASSED
  - diff check - PASSED
  - governance validation - NOT RUN until final evidence commit
  - native Linux qualification - NOT RUN
  - native Windows qualification - NOT RUN
  - qualified private deployment/upgrade - NOT RUN
  - V1 release gate - FAILED by design at 0/26 VERIFIED
  - deployment - NOT PERFORMED
- Remaining risks: native service/reboot/reconnect/upgrade evidence, qualified private deployment, live integrations, recovery/capacity, browser, AI, and aggregate end-to-end evidence remain unqualified.
- Blockers: codebase-memory transport, native Windows/Linux host qualification, private deployment environment, PostgreSQL-dependent tests on system Python, live Notion/Tailscale/Hindsight/AI, browser, and aggregate release environment.
- Follow-up directive: D-PRIME-PHASE15-REMEDIATION-009

## D-PRIME-PHASE15-REMEDIATION-008 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-015
- Supersedes outcome: OUT-PRIME-PHASE15-REMEDIATION-013
- Closed: 2026-08-11T02:01:00Z
- Acceptance: PARTIAL
- Summary: Executed Continuation 008 against the unchanged PRIME-SPEC-V1.0.0 baseline. Closed the local implementation boundary for R-042 through R-045 with authenticated Continuity v2 backup/manifest creation, clean restore workflow and component fidelity, managed Evidence/Git bundle recovery, durable schedule state, active capacity/retention/backpressure controls, and R-046–R-050 recovery regression protection. R-042–R-045 are IMPLEMENTED but qualification partial; no requirement is VERIFIED, V1 remains FAIL, and deployment was not performed.
- Changed areas: src/prime_core/backup_service.py, src/prime_core/reliability_service.py, src/prime_core/service.py, apps/core/main.py, migrations/prime/0020_continuity_capacity.sql, requirements-phase1.txt, dependencies/pins.yaml, dependencies/SBOM.cdx.json, dependencies/QUALIFICATION.md, tests/phase13, docs/phase15-remediation-qualification-ledger.yaml, docs/phase15-remediation-matrix.yaml, docs/requirements-traceability.yaml, docs/phase15-remediation-queue.md, evidence/phase15/R-042-R-045-implementation-closure-008.md, .agent/CURRENT.md, .agent/DIRECTIVES.md, .agent/LEARNINGS.md, .agent/REPO_MAP.md
- Validation:
  - PRIME source page, Implementation Handoff Record, and Checkpoint 007 reread - PASSED
  - codebase-memory MCP index/search - BLOCKED (`Transport closed`); targeted local fallback used
  - focused backup tests - PASSED (4 tests)
  - clean disposable PostgreSQL regression - PASSED (47 tests)
  - clean-install separate-database continuity fixture - PASSED (project, Evidence hash/file, historical rows, Git checkpoint bundle, wrong-key failure)
  - implementation/qualification separation - PASSED; R-042–R-045 qualification remains partial
  - V1 release gate - FAILED as required; VERIFIED / 26 remains 0/26
  - deployment - NOT PERFORMED
- Remaining risks: genuinely separate off-machine target, fresh-install destructive safety and interrupted restore, live Hindsight loss/rebuild, sustained capacity/disk-pressure, native/live integrations, browser, AI, and aggregate end-to-end evidence remain unqualified.
- Blockers: system Python lacks psycopg; native Windows/Linux, live Notion/Tailscale/Hindsight, approved AI, browser, off-machine recovery target, and sustained capacity environments are unavailable or unqualified.
- Follow-up directive: D-PRIME-PHASE15-REMEDIATION-008

## D-PRIME-PHASE15-REMEDIATION-007 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-014
- Supersedes outcome: OUT-PRIME-PHASE15-REMEDIATION-013
- Closed: 2026-08-11T01:29:00Z
- Acceptance: PARTIAL
- Summary: Corrected the Continuation 007 validation record after its outcome append. The final adopted governance check, compile check, diff check, and clean-worktree check all passed; the clean Phase-15 run independently passed 43 tests and Phases 1–14 while correctly retaining V1 `FAIL` at 0/26 VERIFIED.
- Changed areas: .agent/OUTCOMES.md, .agent/CURRENT.md
- Validation:
  - final `python3 scripts/validate_governance.py --mode ADOPTED` - PASSED
  - final compileall - PASSED
  - final git diff check - PASSED
  - final worktree status - PASSED (clean)
  - final disposable qualification teardown - PASSED
  - V1 release/deployment - FAIL / NOT PERFORMED by design; no requirement was falsely promoted
- Remaining risks: unchanged from OUT-PRIME-PHASE15-REMEDIATION-013; R-042 through R-045 and R-051 through R-056 remain implementation/qualification work, and R-046 through R-050 remain qualification `partial`.
- Blockers: unchanged from OUT-PRIME-PHASE15-REMEDIATION-013; required native/live/recovery environments remain unavailable or unqualified.
- Follow-up directive: D-PRIME-PHASE15-REMEDIATION-007

## D-PRIME-PHASE15-REMEDIATION-008 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-017
- Supersedes outcome: OUT-PRIME-PHASE15-REMEDIATION-016
- Closed: 2026-08-11T02:10:00Z
- Acceptance: PARTIAL
- Summary: Final append-only correction for Continuation 008. Governed implementation commit `7b5ef0a`, evidence/governance commit `342fc58`, and milestone record commit `3135df8` are recorded; R-042–R-045 are IMPLEMENTED with qualification partial, R-046–R-050 remain IMPLEMENTED with qualification partial, implementation convergence is 9/26, VERIFIED is 0/26, V1 remains FAIL, and deployment was not performed.
- Changed areas: .agent/OUTCOMES.md, .agent/RECORD.md
- Validation:
  - adopted governance validation after correction - PASSED
  - compileall - PASSED
  - git diff check - PASSED
  - clean Phase-15 mechanical run - PASSED through Phases 1–14 and 47 tests; VERIFIED gate FAILED as required
  - final worktree check - PASSED
  - V1 release gate - FAILED by design at 0/26 VERIFIED
  - deployment - NOT PERFORMED
- Remaining risks: separate off-machine target, fresh-install destructive safety and interrupted restore, live Hindsight loss/rebuild, sustained capacity/disk-pressure, native/live integrations, browser, AI, and aggregate end-to-end evidence remain unqualified.
- Blockers: system Python lacks psycopg; native Windows/Linux, live Notion/Tailscale/Hindsight, approved AI, browser, off-machine recovery target, and sustained capacity environments are unavailable or unqualified.
- Follow-up directive: D-PRIME-PHASE15-REMEDIATION-008
## D-PRIME-PHASE15-REMEDIATION-012 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-025
- Supersedes outcome: OUT-PRIME-PHASE15-REMEDIATION-024
- Closed: 2026-08-11T13:28:00Z
- Acceptance: PARTIAL
- Summary: Continuation 012 closes the local implementation boundary for R-051 through R-053 at implementation commit `3fd09a10aad5b2fff4856b6e75fac5e893e08b3b` and establishes secret-safe, idempotent MyAssistant Notion credential-reference reuse. Implementation convergence is 23/26. Live Notion capability remains blocked because `NOTION_READONLY_KEY` is absent from this runtime; supported-browser, mobile, keyboard-only, and assistive-technology qualification was not run. V1 remains FAIL at 0/26 VERIFIED and deployment was not performed.
- Changed areas: `src/prime_core/notion_credentials.py`, `src/prime_core/notion_api.py`, `migrations/prime/0023_notion_credential_reference.sql`, `apps/core/main.py`, `apps/web/index.html`, `tests/phase7`, `tests/phase14`, `docs/requirements-traceability.yaml`, `docs/phase15-remediation-matrix.yaml`, `docs/phase15-remediation-qualification-ledger.yaml`, `evidence/phase15/R-051-R-053-implementation-closure-012.md`, and `.agent` governance files.
- Validation:
  - PRIME source and Implementation Handoff reread - PASSED
  - Checkpoint 011 direct fetch - BLOCKED (`object_not_found` in connected Notion workspace); attached directive used as supplied
  - codebase-memory MCP index - BLOCKED (`Transport closed`); targeted local fallback used
  - MyAssistant credential discovery - BLOCKED (`NOTION_READONLY_KEY` absent; no secret printed or persisted)
  - focused credential/Notion/API/web tests - PASSED (`17 passed`, `1 skipped`)
  - full local test suite - PASSED (`48 passed`, `17 skipped`)
  - compileall - PASSED
  - adopted governance validation - PASSED
  - diff check - PASSED
  - Phase-15 qualification gate - FAILED truthfully: database URL unavailable, 0/26 VERIFIED
  - supported-browser desktop/mobile/assistive technology walkthrough - NOT RUN
  - live PRIME Notion import/read/write/provider lifecycle - BLOCKED
  - deployment - NOT PERFORMED
- Remaining risks: live Notion provider capability and lifecycle evidence, supported browser/device accessibility evidence, native/live Node/Tailscale/Hindsight/recovery/capacity/AI environments, and aggregate end-to-end qualification remain open.
- Blockers: absent `NOTION_READONLY_KEY` in this runtime, missing `PRIME_PHASE1_DB_URL`/`PRIME_DATABASE_URL` for database-backed phase gates, codebase-memory MCP transport, supported browser/device qualification environment, and prior native/live release environments.
- Follow-up directive: D-PRIME-PHASE15-REMEDIATION-012

## D-PRIME-PHASE15-REMEDIATION-013 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-026
- Supersedes outcome: OUT-PRIME-PHASE15-REMEDIATION-025
- Closed: 2026-08-11T18:00:00Z
- Acceptance: PARTIAL
- Summary: Continuation 013 closes the local implementation boundary for R-054 and R-055 at implementation commit `10e0650a6fd14df3837baa7b45ff60d9ec33693b`. Core now provides function-specific AI profiles, durable run/source/profile/usage provenance, privacy and no-fallback enforcement, grounded Ask integration, structured output/citation checks, prompt-injection and project-isolation defenses, and versioned golden fixtures. Implementation convergence is 25/26; R-056 remains OPEN; no requirement is VERIFIED; V1 remains FAIL; deployment was not performed.
- Changed areas: `src/prime_core/ai_service.py`, `src/prime_core/intelligence_service.py`, `apps/core/main.py`, `migrations/prime/0024_ai_execution.sql`, `tests/phase15/fixtures/ai_golden.json`, `tests/phase15/test_ai_execution.py`, `docs/requirements-traceability.yaml`, `docs/phase15-remediation-matrix.yaml`, `docs/phase15-remediation-qualification-ledger.yaml`, `docs/phase15-remediation-queue.md`, `evidence/phase15/R-054-R-055-implementation-closure-013.md`, and `.agent` governance files.
- Validation:
  - PRIME source and Implementation Handoff reread - PASSED
  - Checkpoint 012 direct fetch - BLOCKED (`object_not_found` in connected Notion workspace); attached directive used as supplied
  - codebase-memory MCP index/search - BLOCKED (`Transport closed`); targeted local fallback used
  - MyAssistant secret-source trace - NOT FOUND IN INSPECTED SOURCES; no secret value printed or persisted
  - focused AI fixture tests - PASSED (6 passed)
  - full local test suite - PASSED (54 passed, 17 skipped)
  - compileall - PASSED
  - adopted governance validation before final correction - PASSED
  - diff check before final correction - PASSED
  - approved live provider qualification - BLOCKED (no approved provider/model configured)
  - LOCAL_ONLY qualification - NOT RUN (no approved local inference stack configured)
  - browser qualification - NOT RUN
  - Phase-15 qualification gate - NOT RUN at outcome append; expected to remain FAIL with external/database prerequisites unavailable
  - deployment - NOT PERFORMED
- Remaining risks: approved provider/local-model qualification, full cross-surface AI evaluation, isolated Project A/B live fixtures, database-backed phase gates, native/live integrations, browser, recovery/capacity, and aggregate R-056 clean-install evidence remain open.
- Blockers: missing approved AI provider/local inference environment, missing `PRIME_PHASE1_DB_URL`/`PRIME_DATABASE_URL` for database-backed gates, codebase-memory transport, supported browser/device qualification, and prior native/live release environments.
- Follow-up directive: none

## D-PRIME-PHASE15-REMEDIATION-014 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-028
- Supersedes outcome: none
- Closed: 2026-08-11T19:12:00Z
- Acceptance: PARTIAL
- Summary: Published the complete governed ANIMUS PRIME repository to canonical GitHub `SketchOTP/ANIMUS_PRIME`. The verified disposable remote placeholder was reconciled with explicit force-with-lease; local `main` and remote `main` matched at publication commit `a8300cf0b649940f0036b53a29a717a4c94ee798`. No secrets were published. R-056 remains OPEN, 0/26 requirements are VERIFIED, V1 remains FAIL, and deployment was not performed.
- Changed areas: canonical Git remote configuration, `.agent/PROJECT_PROFILE.md`, `.agent/CURRENT.md`, `.agent/REPO_MAP.md`, `.agent/RECORD.md`, `.agent/OUTCOMES.md`, and `evidence/phase15/github-publication-014.md`.
- Validation:
  - local/remote prepublication history inspection - PASSED
  - GitHub authentication and repository access - PASSED
  - tracked-file secret-safety inspection - PASSED
  - explicit force-with-lease publication against verified placeholder - PASSED
  - local `main` / `origin/main` / `ls-remote` parity - PASSED
  - representative remote path verification - PASSED
  - GitHub connector representative-file verification - PASSED
  - governed tag inspection - PASSED (none present)
  - deployment - NOT PERFORMED
- Remaining risks: all previously recorded native/live/provider/browser/recovery/capacity qualification gaps and aggregate R-056 clean-install evidence remain open.
- Blockers: no publication blocker remains; Phase-15 qualification still lacks database URL, approved AI/local inference, native/live integrations, supported browser/device, recovery/capacity, and aggregate end-to-end environments.
- Follow-up directive: none

## D-PRIME-PHASE15-REMEDIATION-013 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-027
- Supersedes outcome: OUT-PRIME-PHASE15-REMEDIATION-026
- Closed: 2026-08-11T18:07:00Z
- Acceptance: PARTIAL
- Summary: Final Continuation 013 qualification correction. The local R-054/R-055 implementation remains complete at 25/26, R-056 remains OPEN, and no requirement is VERIFIED. The final Phase-15 runner completed its available mechanical checks and correctly returned V1 FAIL because database-backed phase gates and required live/native/browser/provider environments are unavailable. Deployment was not performed.
- Changed areas: `.agent/CURRENT.md`, `.agent/OUTCOMES.md`; final qualification state only; no normative or product change.
- Validation:
  - adopted governance validation - PASSED
  - full local regression suite - PASSED (54 passed, 17 skipped)
  - compileall - PASSED
  - diff check - PASSED
  - Phase-15 full qualification runner - FAILED truthfully (database URL unavailable; 25/26 implementation-complete; 0/26 VERIFIED)
  - approved live provider qualification - BLOCKED
  - LOCAL_ONLY qualification - NOT RUN
  - browser/native/live/recovery qualification - NOT RUN
  - deployment - NOT PERFORMED
- Remaining risks: all external/native/provider/browser/recovery/capacity qualification gaps and aggregate R-056 clean-install evidence remain open.
- Blockers: missing database qualification URL, approved AI/local inference environment, codebase-memory transport, supported browser/device, and prior native/live release environments.
- Follow-up directive: none

## D-PRIME-PHASE15-REMEDIATION-014 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-029
- Supersedes outcome: OUT-PRIME-PHASE15-REMEDIATION-028
- Closed: 2026-08-11T19:16:18Z
- Acceptance: PARTIAL
- Summary: Completed the post-publication qualification continuation. The canonical GitHub publication remains exact and secret-safe; the available Phase-15 runner correctly returned FAIL because database-backed gates are blocked by the missing database URL and all 26 remediation requirements remain unverified. R-056 remains OPEN and deployment was not performed.
- Changed areas: `.agent/CURRENT.md`, `.agent/OUTCOMES.md`, and `evidence/phase15/github-publication-014.md`; qualification evidence only, with no normative or product architecture change.
- Validation:
  - adopted governance validation - PASSED
  - full regression suite - PASSED (54 passed, 17 skipped)
  - Phase 1–13 database-backed migration qualification - BLOCKED (database URL unavailable)
  - Phase 14 qualification - PASSED
  - approved baseline identity and remediation ledger structure - PASSED
  - Phase-15 available qualification runner - FAILED truthfully (25/26 implementation-complete; 0/26 VERIFIED)
  - deployment - NOT PERFORMED
- Remaining risks: approved provider/local-model, live Notion/Tailscale/Hindsight, native Linux/Windows, browser/accessibility, recovery/capacity, historical, and aggregate clean-install/end-to-end qualification remain open.
- Blockers: missing `PRIME_PHASE1_DB_URL`/`PRIME_DATABASE_URL`, approved AI/local inference environment, live/native/browser/recovery environments, and codebase-memory transport.
- Follow-up directive: none

## D-PRIME-PHASE15-REMEDIATION-015 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-030
- Supersedes outcome: OUT-PRIME-PHASE15-REMEDIATION-029
- Closed: 2026-08-11T17:08:17-04:00
- Acceptance: PARTIAL
- Summary: Continuation 015 removed the locally solvable database qualification blocker using a freshly recreated disposable PostgreSQL/pgvector environment. PostgreSQL `17.10`, pgvector `0.8.2`, empty-database prechecks, all 24 migrations from zero, and Phases 1–14 passed. The first real database-backed Ask execution exposed an `ai_runs` placeholder mismatch; the minimum repair was committed at `344efd6`, and a fresh rerun passed `71` tests. The Phase-15/V1 gate remains FAIL with `0/26 VERIFIED`; R-056 remains OPEN; deployment was not performed.
- Changed areas: `.agent/DIRECTIVES.md`, `.agent/CURRENT.md`, `.agent/LEARNINGS.md`, `.agent/RECORD.md`, `.agent/REPO_MAP.md`, `.agent/OUTCOMES.md`, `.agent/phase-records/PHASE-15.md`, `docs/requirements-traceability.yaml`, `docs/phase15-remediation-matrix.yaml`, `docs/phase15-remediation-qualification-ledger.yaml`, `src/prime_core/ai_service.py`, and `evidence/phase15/qualification-continuation-015.md`.
- Validation:
  - codebase-memory MCP index/search - BLOCKED (`Transport closed`); targeted local inspection used for configuration and governance fallback
  - fresh disposable PostgreSQL/pgvector precheck - PASSED
  - PostgreSQL version/role/reachability/empty-schema checks - PASSED
  - pgvector extension availability and enablement - PASSED (`0.8.2`)
  - migration chain from zero through `0024_ai_execution.sql` - PASSED
  - migration idempotence/schema/table checks - PASSED
  - first database-backed full run - FAILED on real `ai_runs` placeholder mismatch
  - minimum defect repair at `344efd6` - PASSED
  - focused requalification - PASSED (`7 passed`)
  - reused populated-database suite invocation - FAILED (three state-collision failures; not used as qualification evidence)
  - fresh complete regression - PASSED (`71 passed`)
  - Phase 1–14 gates - PASSED
  - Phase-15/V1 release gate - FAILED truthfully (`0/26 VERIFIED`; implementation `25/26`; R-056 OPEN)
  - deployment - NOT PERFORMED
- Remaining risks: R-042–R-050 remain `partial` because off-machine/fresh-install, live Hindsight, sustained capacity, and complete historical/product-path evidence remains absent; R-031–R-041 and R-051–R-056 retain their exact environment blockers. Native Linux/Windows, Tailscale, live Notion, off-machine/interrupted restore, live Hindsight, sustained capacity, supported browser/accessibility, approved model/local inference, and aggregate R-056 remain unqualified.
- Blockers: external qualification environments remain unavailable; default host database variables are unset but are no longer a blocker when the approved disposable stack is created.
- Follow-up directive: none

## D-PRIME-PHASE15-REMEDIATION-016 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-031
- Supersedes outcome: OUT-PRIME-PHASE15-REMEDIATION-030
- Closed: 2026-08-11T17:54:50-04:00
- Acceptance: PARTIAL
- Summary: Continuation 016 reconciled stale qualification blockers, repaired citation and retained-checkpoint status defects, and produced the first genuine VERIFIED requirement. R-049 is VERIFIED from a real PostgreSQL/Git/Time Lens fixture with positive, negative, degraded, recovery, citation, and security evidence. The fresh complete run passed 73 tests and Phases 1–14; V1 remains FAIL at 1/26 because the remaining rows and R-056 are not fully qualified.
- Changed areas: `src/prime_core/history_service.py`, `tests/phase15/test_requirement_qualification.py`, `.agent/`, `docs/requirements-traceability.yaml`, `docs/phase15-remediation-matrix.yaml`, `docs/phase15-remediation-qualification-ledger.yaml`, and `evidence/phase15/qualification-continuation-016.md`.
- Validation:
  - codebase-memory MCP discovery - BLOCKED (`Transport closed`); targeted fallback used and recorded
  - fresh disposable PostgreSQL/pgvector precheck - PASSED
  - migrations from zero - PASSED (`24/24`)
  - full regression - PASSED (`73 passed`)
  - Phases 1–14 - PASSED
  - R-049 exact qualification fixture - PASSED; row promoted
  - real Evidence/citation focused qualification - PASSED for exercised cases; row remains PARTIAL for remaining matrix
  - Hindsight real backend probe - PARTIAL/DEGRADED without approved model/provider
  - Tailscale real status/refusal probe - PASSED safety refusal; private qualification remains PARTIAL
  - Chromium real shell load - PASSED; full interactive browser matrix remains PARTIAL
  - native Linux installer/systemd - PARTIAL; service registration not run without root
  - Notion credential discovery - PASSED as `NOT FOUND`; no secret exposed
  - aggregate Phase-15/V1 gate - FAILED truthfully (`1/26 VERIFIED`; R-056 OPEN)
  - deployment - NOT PERFORMED
- Remaining risks: R-031–R-036, R-042–R-048, and R-050–R-053 remain partial; R-037–R-041 and R-054–R-056 remain environment constrained; off-machine/interrupted restore, complete A/B/C/D history, full product citation flow, capacity, native Windows, live Notion, approved Hindsight/AI, and full browser interaction remain open.
- Blockers: exact external/native/provider criteria listed in `evidence/phase15/qualification-continuation-016.md`; codebase-memory transport remains unavailable.
- Follow-up directive: none

## D-PRIME-PHASE15-REMEDIATION-017 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-032
- Supersedes outcome: OUT-PRIME-PHASE15-REMEDIATION-031
- Closed: 2026-08-11T18:35:00-04:00
- Acceptance: PARTIAL
- Summary: Continuation 017 repaired the minimum production defects needed for product Evidence citations, separate-mount backup classification, historical Evidence availability, and durable interrupted-restore state. Real PostgreSQL-backed qualification promoted R-046 and R-047 to VERIFIED while preserving R-049 VERIFIED. R-042, R-043, R-045, R-048, and R-050 were exercised but remain partial where exact scheduled, fresh-install, sustained, correction-overlay, and browser criteria remain open. Full regression passed 79 tests and V1 remains FAIL.
- Changed areas: `src/prime_core/backup_service.py`, `src/prime_core/history_service.py`, `src/prime_core/intelligence_service.py`, `src/prime_core/progress_service.py`, `apps/core/main.py`, `tests/phase15/test_requirement_qualification.py`, `.agent/`, `docs/`, and `evidence/phase15/qualification-continuation-017.md`.
- Validation:
  - codebase-memory MCP discovery - BLOCKED (`Transport closed`); targeted fallback used and recorded
  - focused qualification - PASSED (`9 passed`)
  - fresh complete regression - PASSED (`79 passed`)
  - Phases 1–14 - PASSED
  - real `/dev/sdb1` off-machine backup manifest - PASSED
  - Chromium CDP operator paths - PASSED/partial; full assistive-technology and historical browser path remains partial
  - Hindsight probe - PARTIAL (`CURRENT/DEGRADED/CURRENT/UNAVAILABLE`)
  - native Linux root lifecycle - NOT RUN
  - Notion secret source - PASSED as `NOT FOUND`; no secret exposed
  - approved AI - NOT CONFIGURED
  - aggregate Phase-15/V1 gate - FAILED truthfully (`3/26 VERIFIED`; R-056 OPEN)
  - deployment - NOT PERFORMED
- Remaining risks: R-031–R-045, R-048, and R-050–R-053 remain partial or environment constrained; live Notion, native Windows/root lifecycle, private second-device Tailscale, approved Hindsight/AI, complete browser accessibility/history, and aggregate R-056 remain open.
- Blockers: exact external/native/provider criteria listed in `evidence/phase15/qualification-continuation-017.md`; codebase-memory transport remains unavailable.
- Follow-up directive: none

## D-PRIME-PHASE15-REMEDIATION-017 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-033
- Supersedes outcome: OUT-PRIME-PHASE15-REMEDIATION-032
- Closed: 2026-08-11T18:55:00-04:00
- Acceptance: PARTIAL
- Summary: Publication and validation correction for Continuation 017. The first Compose attempt was non-authoritative because it used an absent filename; the subsequent explicit pinned PostgreSQL/pgvector run passed 79 tests, Phases 1–14, and governance. Evidence/checkpoint commit `ccc3f2b30d60d09629b31c82d65289e68d2e671f`; final HEAD and `origin/main` are `e60728b5ec5b367625ca7a82edb37a93401c3c29`; Notion execution record was appended and re-fetched.
- Changed areas: `.agent/CURRENT.md`, `.agent/OUTCOMES.md`, Notion Implementation Execution Record, and GitHub publication state.
- Validation:
  - explicit pinned PostgreSQL/pgvector Phase-15 runner - PASSED
  - full regression - PASSED (`79 passed`)
  - Phases 1–14 - PASSED
  - adopted governance - PASSED
  - GitHub local/origin parity - PASSED
  - Notion append and re-fetch - PASSED
  - aggregate Phase-15/V1 gate - FAILED truthfully (`3/26 VERIFIED`; R-056 OPEN)
  - deployment - NOT PERFORMED
- Remaining risks: R-031–R-045, R-048, and R-050–R-053 remain partial or environment constrained; live Notion, native Windows/root lifecycle, private second-device Tailscale, approved Hindsight/AI, complete browser accessibility/history, and aggregate R-056 remain open.
- Blockers: exact external/native/provider criteria listed in `evidence/phase15/qualification-continuation-017.md`; codebase-memory transport remains unavailable.
- Follow-up directive: none

## D-PRIME-PHASE15-REMEDIATION-017 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-034
- Supersedes outcome: OUT-PRIME-PHASE15-REMEDIATION-033
- Closed: 2026-08-11T19:00:00-04:00
- Acceptance: PARTIAL
- Summary: Final Continuation 017 state correction. The governed documentation closure was published successfully; final local `HEAD` and GitHub `origin/main` both resolve to `4819d2c3a4c63301d4a0c7136ab1b41d0bf08527`. The qualification evidence checkpoint remains `ccc3f2b30d60d09629b31c82d65289e68d2e671f`.
- Changed areas: `.agent/CURRENT.md`, `.agent/OUTCOMES.md`, and final GitHub publication state.
- Validation:
  - governance validation - PASSED
  - GitHub local/origin parity - PASSED
  - Notion Continuation 017 record - PASSED before final hash closure; final hash closure is recorded in the next Notion append
  - aggregate Phase-15/V1 gate - FAILED truthfully (`3/26 VERIFIED`; R-056 OPEN)
  - deployment - NOT PERFORMED
- Remaining risks: all previously recorded open and environment-constrained requirements remain unchanged; V1 is not qualified.
- Blockers: exact external/native/provider criteria listed in `evidence/phase15/qualification-continuation-017.md`; codebase-memory transport remains unavailable.
- Follow-up directive: none

## D-PRIME-PHASE15-REMEDIATION-018 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-035
- Supersedes outcome: OUT-PRIME-PHASE15-REMEDIATION-034
- Closed: 2026-08-11T20:45:00-04:00
- Acceptance: PARTIAL
- Summary: Continuation 018 used the operator-approved Paragon local model and PRIME Notion authorization ephemerally. The minimum OpenAI-compatible adapter was added and real Paragon Ask/Progress/Documentation/memory-admission, privacy, injection, isolation, outage/recovery, usage, and secret-safety paths passed. PRIME Notion health and frozen-page read capability passed; live Notion writes were intentionally not run without a disposable target. R-054 is VERIFIED; R-037–R-041 and R-055 are partial; R-056 remains OPEN.
- Changed areas: `src/prime_core/ai_service.py`, `tests/phase15/test_ai_execution.py`, `.agent/`, `docs/`, and `evidence/phase15/qualification-continuation-018.md`.
- Validation:
  - codebase-memory MCP discovery - BLOCKED (`Transport closed`); targeted fallback used and recorded
  - provider endpoint/model probe - PASSED (`HTTP 200`)
  - PRIME Paragon execution - PASSED (Ask, Progress, Documentation, memory admission)
  - provider outage/recovery - PASSED
  - durable secret-redaction review - PASSED
  - PRIME Notion health/page/block read - PASSED
  - PRIME Notion write probe - NOT RUN (no disposable target authorized)
  - focused AI tests - PASSED (`7 passed`)
  - fresh complete regression - PASSED (`80 passed`)
  - Phases 1–14 - PASSED
  - adopted governance - PASSED
  - aggregate Phase-15/V1 gate - FAILED truthfully (`4/26 VERIFIED`; R-056 OPEN)
  - deployment - NOT PERFORMED
- Remaining risks: R-031–R-045, R-048, R-050–R-053, R-055, and R-056 remain partial or environment constrained; live Notion writes/lifecycle, native Windows/root lifecycle, private second-device Tailscale, full Hindsight/provider-dependent paths, complete browser accessibility/history, and aggregate R-056 remain open.
- Blockers: exact external/native/provider criteria listed in `evidence/phase15/qualification-continuation-018.md`; codebase-memory transport remains unavailable.
- Follow-up directive: none

## D-PRIME-PHASE15-REMEDIATION-019 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-036
- Supersedes outcome: OUT-PRIME-PHASE15-REMEDIATION-035
- Closed: 2026-08-12T00:55:00-04:00
- Acceptance: PARTIAL
- Summary: Continuation 019 qualified real Project A/B-scoped Paragon Goal, Progress, Ask, Documentation, Alignment, and memory execution. Ask produced a grounded Project A fact and UNKNOWN for absent Project B evidence; cross-project source admission was rejected; prompt injection remained inert; supported and unsupported memory outcomes were correct; outage degraded all exercised surfaces without fallback; recovery produced a new durable run. A disposable connected Notion sandbox proved create/read/update, managed-region preservation, and source revision refresh without touching canonical or user-authored pages. R-055 remains partial for integrated projection/correction/invalid-citation lifecycle closure; R-037–R-041 remain partial for the local PRIME adapter lifecycle.
- Changed areas: `src/prime_core/ai_service.py`, `tests/phase15/test_ai_execution.py`, `scripts/phase15_qualify_continuation_019.py`, `.agent/`, `docs/`, and `evidence/phase15/qualification-continuation-019.md`.
- Validation:
  - codebase-memory MCP discovery - BLOCKED (`Transport closed`); targeted fallback used and recorded
  - real Paragon cross-surface matrix - PASSED for exercised paths
  - Project A/B isolation and UNKNOWN behavior - PASSED
  - provider outage/degraded and explicit recovery - PASSED
  - durable provenance and secret-safety review - PASSED
  - connected Notion disposable write/read/managed-region/source-refresh probe - PASSED
  - focused AI tests - PASSED (`7 passed`)
  - Notion API/credential/lifecycle tests - PASSED (`16 passed`)
  - fresh complete regression - PASSED (`80 passed`)
  - Phases 1–14 - PASSED
  - adopted governance - PASSED
  - aggregate Phase-15/V1 gate - FAILED truthfully (`4/26 VERIFIED`; R-056 OPEN)
  - deployment - NOT PERFORMED
- Remaining risks: R-031–R-045, R-048, R-050–R-053, R-055, and R-056 remain partial or environment constrained; local PRIME Notion adapter lifecycle, full integrated AI projection/correction, native Windows/root lifecycle, private second-device Tailscale, full Hindsight/provider-dependent paths, complete browser accessibility/history, and aggregate R-056 remain open.
- Blockers: exact external/native/provider criteria listed in `evidence/phase15/qualification-continuation-019.md`; codebase-memory transport remains unavailable.
- Follow-up directive: none

## D-PRIME-PHASE15-REMEDIATION-020 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-037
- Supersedes outcome: OUT-PRIME-PHASE15-REMEDIATION-036
- Closed: 2026-08-12T02:20:00Z
- Acceptance: PARTIAL
- Summary: Continuation 020 completed the real Paragon AI lifecycle through PRIME's IntelligenceService and promoted R-055 to VERIFIED. Product Goal, Progress, Ask, Alignment, Documentation, memory admission, Project A/B source rejection, durable ai_runs, managed projection/conflict, invalid-citation rejection, correction/supersession history, provider degradation/recovery, and history rollover/restart passed. R-037–R-041 remain partial because the approved live disposable Notion parent is in trash and the production API rejects writes against archived targets; no canonical or user-authored page was mutated.
- Changed areas: `src/prime_core/intelligence_service.py`, `src/prime_core/memory_service.py`, `src/prime_core/notion_api.py`, `src/prime_core/notion_service.py`, `scripts/phase15_qualify_continuation_020.py`, focused tests, `docs/`, `.agent/`, and `evidence/phase15/qualification-continuation-020.md`.
- Validation:
  - codebase-memory MCP discovery - BLOCKED (`Transport closed`); targeted fallback used and recorded
  - focused provider/lifecycle tests - PASSED (`25 passed`)
  - real Paragon product lifecycle - PASSED; one Alignment rate-limit degradation recovered with a new durable run
  - product Project A/B isolation - PASSED; cross-project source set rejected before provider dispatch
  - invalid citation - PASSED; durable run rejected and no projection accepted
  - correction/supersession/history - PASSED; earlier memory superseded, correction recorded, historical snapshots retained
  - offline PRIME Notion lifecycle - PASSED; managed projection, user-content preservation, conflict, outage/recovery, source detach/review, and history restart passed
  - live PRIME Notion adapter - PARTIAL; reads worked, create returned archived-parent validation because the approved target is in trash
  - canonical Notion execution-record append - BLOCKED; the adopted source page is archived and no canonical or user-authored page workaround was attempted
  - governance validation - PASSED
  - fresh authoritative regression - PASSED (`86 passed`)
  - Phases 1–14 - PASSED
  - tracked-file secret scan - PASSED after final publication review; no supplied credential values recorded
  - aggregate Phase-15/V1 gate - FAILED truthfully (`5/26 VERIFIED`; R-056 OPEN)
  - deployment - NOT PERFORMED
- Remaining risks: R-037–R-041, R-042–R-053 except R-046/R-047/R-049, and R-056 remain partial/open as recorded in the qualification ledger; V1 is not qualified.
- Blockers: a non-archived operator-approved disposable Notion parent with write scope is required to close R-037–R-041; codebase-memory transport remains unavailable.
- Follow-up directive: none

## D-PRIME-TAKEOVER-VERIFY-021 - PARTIAL

- Outcome ID: OUT-PRIME-TAKEOVER-VERIFY-038
- Supersedes outcome: none
- Closed: 2026-08-12T12:10:00Z
- Acceptance: PARTIAL
- Summary: Took over the authoritative Atlas checkout and independently reconciled inherited Continuation 020 work. The inherited qualification state is at `e7f6099679a982d9708c3a4c96d87fa900a0e89d`; the status-only takeover publication advanced Atlas `/home/sketch/Projects/ANIMUS_PRIME`, local `main`, and GitHub `origin/main` to `e7b70d26f1016bde2d5479cd3adeadda9ee4d725`. Continuation 020 remains the current governed state: R-055 is VERIFIED; R-046, R-047, R-049, and R-054 remain VERIFIED; R-037–R-041 remain PARTIAL because the approved live Notion parent is archived; R-056 remains OPEN; Phase 15/V1 remains FAIL at 5/26; deployment was not performed.
- Validation:
  - adopted governance validator - PASSED
  - compileall and diff-check - PASSED
  - default regression invocation - PASSED (`61 passed`, `25 skipped` because database variables were unset)
  - reused populated disposable database invocation - FAILED (83 passed, 3 deterministic persistent-state collisions; not a fresh qualification run and not used to overturn the recorded fresh 86-pass result)
  - GitHub connector repository, current commit, and e1a9ebd-to-e7f6099 comparison - PASSED
  - Architect Notion root and handoff fetch - PASSED; Checkpoint 019 is deleted/archived and no canonical or user-authored page was mutated
- Changed areas: `.agent/CURRENT.md`, `.agent/DIRECTIVES.md`, `.agent/OUTCOMES.md`, `.agent/LEARNINGS.md`, `.agent/RECORD.md`.
- Remaining risks: the fresh 86-pass qualification was not rerun during takeover; live Notion R-037–R-041 still require an operator-approved non-archived disposable parent; all other Continuation 020 gaps remain as recorded.
- Blockers: a fresh disposable database rerun was not performed during takeover because the current database is populated and resetting it was outside this read/verify pass; live Notion R-037–R-041 still require an operator-approved non-archived disposable parent; all other Continuation 020 gaps remain as recorded.
- Follow-up directive: none

## D-PRIME-PHASE15-REMEDIATION-022 - BLOCKED

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-039
- Supersedes outcome: none
- Closed: 2026-08-12T20:00:00Z
- Acceptance: PARTIAL
- Summary: Continuation 022 accepted the takeover correction, found a current non-archived disposable Notion sandbox, corrected stale R-042 gap wording using the existing Continuation 017 off-machine evidence, and attempted the required environment preflight. The real R-037–R-041 PRIME production adapter qualification could not start because `NOTION_READONLY_KEY` was absent from the Atlas process and Docker was unavailable for the fresh disposable PostgreSQL/pgvector environment. No substitute connector evidence was claimed.
- Changed areas: `docs/phase15-remediation-qualification-ledger.yaml`, `docs/phase15-remediation-matrix.yaml`, `.agent/DIRECTIVES.md`, `.agent/CURRENT.md`, `.agent/OUTCOMES.md`, `evidence/phase15/qualification-continuation-022.md`, and the Architect Notion execution record.
- Validation:
  - non-archived disposable Notion sandbox fetch - PASSED
  - PRIME runtime authorization preflight - BLOCKED (`NOTION_READONLY_KEY` absent; no secret exposed)
  - approved disposable PostgreSQL/pgvector preflight - BLOCKED (Docker unavailable)
  - R-042 Continuation 017 evidence reconciliation - PASSED
  - R-042 ledger/matrix correction - PASSED
  - adopted governance validator - NOT RUN after final edits
  - fresh authoritative regression - NOT RUN (required environment unavailable)
  - deployment - NOT PERFORMED
- Remaining risks: R-037–R-041 live adapter lifecycle remains unqualified; R-042 scheduled failure/recovery/retention remains open; R-043/R-045/R-048/R-050–R-053 remain as previously recorded; R-056 remains OPEN; Phase 15/V1 remains FAIL at 5/26.
- Blockers: `NOTION_READONLY_KEY` is absent from the Atlas process; Docker is unavailable for the approved disposable PostgreSQL/pgvector environment.
- Follow-up directive: none

## D-PRIME-PHASE15-REMEDIATION-023 - COMPLETE

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-040
- Supersedes outcome: OUT-PRIME-PHASE15-REMEDIATION-039
- Closed: 2026-08-13T00:45:00Z
- Acceptance: MET
- Summary: Native Atlas qualification credentials were injected ephemerally and verified by presence only. A fresh disposable PostgreSQL/pgvector environment was recreated; native compile passed; the fresh authoritative regression passed with 86 tests and Phases 1–14 passed. The prior Continuation 019 sandbox was inaccessible to the supplied PRIME integration, so a new disposable child under the accessible ANIMUS PRIME root was provisioned. PRIME's actual NotionApiClient/NotionApiProvider/NotionLifecycleService path completed with the approved Paragon profile and live Notion target. R-037 through R-041 were promoted independently to VERIFIED; preserved VERIFIED rows remain intact. R-042's off-machine criterion remains satisfied with only scheduled failure/recovery/retention open; R-056 remains OPEN; V1 remains FAIL at 10/26; deployment was not performed. The new evidence is the Continuation 023 qualification and publication record.
- Changed areas: `docs/requirements-traceability.yaml`, `docs/phase15-remediation-matrix.yaml`, `docs/phase15-remediation-qualification-ledger.yaml`, `.agent/DIRECTIVES.md`, `.agent/CURRENT.md`, `.agent/OUTCOMES.md`, `.agent/RECORD.md`, `.agent/REPO_MAP.md`, `.agent/phase-records/PHASE-15.md`, `evidence/phase15/qualification-continuation-023.md`, and the Architect Notion execution record.
- Validation:
  - native credential presence check - PASSED (`PRESENT` only; no values emitted)
  - Docker/pgvector fresh disposable database - PASSED
  - native compile - PASSED
  - fresh database-backed regression - PASSED (`86 passed`)
  - Phases 1–14 - PASSED
  - PRIME live Notion/Paragon adapter harness - PASSED (exit 0)
  - governance, YAML, tracked-secret scan, final diff, GitHub push, fetch, and exact parity - PASSED (`025d64f50718417a5e69e350b59864e6131ae240`)
  - deployment - NOT PERFORMED
- Remaining risks: Newly verified rows are R-037 through R-041; preserved verified rows are R-046, R-047, R-049, R-054, and R-055. R-042 scheduled backup failure/recovery/retention, R-043, R-045, R-048, R-050–R-053, and R-056 remain open; aggregate V1 remains FAIL.
- Blockers: none for Continuation 023 acceptance; publication checks remain before GitHub synchronization.
- Follow-up directive: none

## D-PRIME-PHASE15-REMEDIATION-024 - COMPLETE

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-041
- Supersedes outcome: OUT-PRIME-PHASE15-REMEDIATION-040
- Closed: 2026-08-12T11:45:26-04:00
- Acceptance: MET
- Summary: Native Atlas Continuation 024 qualification completed against a freshly recreated disposable PostgreSQL/pgvector environment and the real Chromium browser path. R-042 was promoted to VERIFIED after durable schedule persistence across Core restart, scheduled execution, destination failure with retry and known-good preservation, destination recovery, subsequent success, retention, and negative backup-security coverage. R-052 was promoted to VERIFIED after the authenticated two-project operator journey, required surfaces, project switching/isolation, restart/session recovery, invalid-project route rejection, healthy/degraded states, responsive rendering, and protected lifecycle entry were exercised in Chromium. The minimum fixes were a PostgreSQL retry interval cast and explicit 404 project-existence guards for Search and Ask. Approved Hindsight health/isolation/rebuild probes passed where available, but retain remained UNAVAILABLE, so R-044 was not promoted. No Notion or Paragon qualification was repeated; no credentials were persisted; deployment was not performed.
- Changed areas: `apps/core/main.py`, `src/prime_core/reliability_service.py`, `scripts/phase15_qualify_continuation_024.py`, `evidence/phase15/qualification-continuation-024.md`, `docs/requirements-traceability.yaml`, `docs/phase15-remediation-matrix.yaml`, `docs/phase15-remediation-qualification-ledger.yaml`, `.agent/DIRECTIVES.md`, `.agent/CURRENT.md`, `.agent/OUTCOMES.md`, `.agent/RECORD.md`, `.agent/REPO_MAP.md`, and `.agent/phase-records/PHASE-15.md`.
- Validation:
  - fresh PostgreSQL/pgvector database and all migrations - PASSED
  - native compile and governance validator - PASSED
  - fresh authoritative regression - PASSED (`86 passed`)
  - Phases 1–14 - PASSED
  - Continuation 024 scheduled recovery/retention harness - PASSED
  - real Chromium operator journey and responsive/security checks - PASSED
  - focused continuation tests - PASSED (`6 passed`)
  - requirements/matrix/ledger YAML parse and tracked-secret scan - PASSED
  - GitHub publication and exact local/origin parity - PASSED after governance commit
  - deployment - NOT PERFORMED
- Remaining risks: R-043, R-044, R-045, R-048, R-050, R-051, and R-053 remain partial for the exact gaps recorded in `evidence/phase15/qualification-continuation-024.md`; R-056 remains OPEN; Phase 15/V1 remains FAIL at 12/26.
- Blockers: approved Hindsight retain is unavailable; complete fresh-install/interrupted restore, sustained capacity/backpressure, independent source-class correction, interactive historical Time Lens, setup-resume, and full keyboard/assistive-technology/untrusted-text acceptance remain unqualified.
- Follow-up directive: none

## D-PRIME-PHASE15-REMEDIATION-025 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-042
- Supersedes outcome: OUT-PRIME-PHASE15-REMEDIATION-041
- Closed: 2026-08-12T14:50:00-04:00
- Acceptance: PARTIAL
- Summary: The Continuation 024 governance inconsistency was corrected without rerunning R-042 or R-052. The qualification ledger's stale top-level status map now marks both rows `verified`; ledger records, remediation matrix, and requirements traceability agree; the mechanical count is 12 VERIFIED, 13 partial, 1 R-056 blocked/open, and 0 failed before new work. Continuation 025 then completed fresh supported-browser setup interruption/resume evidence and promoted R-051 to VERIFIED. The real browser exercised the remaining R-053 keyboard/untrusted-text checks, and the Time Lens UI gap was minimally implemented with a boundary selector, custom revision input, historical status, and Return to Now control. R-053, R-050, R-043, R-045, and R-048 remain partial for exact gaps recorded in the Continuation 025 evidence.
- Changed areas: `apps/web/index.html`, `tests/phase14/test_web_shell.py`, `docs/phase15-remediation-qualification-ledger.yaml`, `docs/phase15-remediation-matrix.yaml`, `docs/requirements-traceability.yaml`, `.agent/DIRECTIVES.md`, `.agent/CURRENT.md`, `.agent/REPO_MAP.md`, `.agent/phase-records/PHASE-15.md`, `evidence/phase15/qualification-continuation-024.md`, and `evidence/phase15/qualification-continuation-025.md`.
- Validation:
  - mechanical YAML reconciliation/count - PASSED (`26 rows; 12 verified, 13 partial, 1 blocked_by_environment`)
  - fresh R-051 browser setup interruption/resume - PASSED (`502` during Core outage, `200` after recovery)
  - R-053 browser focus, keyboard submit, untrusted text, and responsive checks - PASSED for available environment
  - Time Lens browser controls and Return to Now - PASSED for available disposable project; historical fixture returned truthful `UNAVAILABLE`
  - focused R-043/R-045/R-048/R-050 regression - PASSED (`3 passed`)
  - web shell test - PASSED (`1 passed`)
  - native compile - PASSED
  - governance/YAML/diff/secret/GitHub publication checks - PASSED
  - Notion execution-record append - BLOCKED (connected MCP unavailable; published page read-only in bounded browser fallback)
  - deployment - NOT PERFORMED
- Remaining risks: R-050 needs a populated State-B browser fixture and source removal/recovery; R-053 needs external assistive technology; R-043/R-045/R-048 exact normative gaps remain; R-044 retain remains UNAVAILABLE; R-056 remains OPEN; V1 remains FAIL at 13/26.
- Blockers: external assistive technology and complete historical/recovery fixtures are not available in this run.
- Follow-up directive: none

## D-PRIME-PHASE15-REMEDIATION-026 - PARTIAL

- Outcome ID: OUT-PRIME-PHASE15-REMEDIATION-043
- Supersedes outcome: OUT-PRIME-PHASE15-REMEDIATION-042
- Closed: 2026-08-12T15:46:04-04:00
- Acceptance: PARTIAL
- Summary: Continuation 026 qualified a real disposable State-A/B/C/D historical fixture through the supported browser. State B reconstructed exactly; historical Ask and Brain returned HTTP 200 with no later-current-state leakage; deliberate Evidence loss degraded only the Evidence source to PARTIAL; exact restoration returned all sources to EXACT; and Return to Now displayed CURRENT with exact current sources. R-050 is promoted to VERIFIED. R-042, R-052, and the prior thirteen verified rows are preserved. R-043, R-045, R-048, and R-053 remain partial for their explicit normative gaps; R-044 remains partial because approved Hindsight retain is unavailable; R-056 remains OPEN.
- Changed areas: `Dockerfile.core`, `src/prime_core/git_history.py`, `src/prime_core/history_service.py`, `scripts/phase15_qualify_continuation_026.py`, `evidence/phase15/qualification-continuation-026.md`, the three governed requirement views, and append-only `.agent` records.
- Validation:
  - fresh PostgreSQL/pgvector focused qualification regression - PASSED (`4 passed`)
  - web shell test - PASSED (`1 passed`)
  - native compileall - PASSED
  - populated browser State-B reconstruction, Ask/Brain, source-loss/restoration, and Return to Now - PASSED
  - mechanical governance/YAML/count reconciliation - PASSED (`26 rows; 14 verified, 11 partial, 1 blocked_by_environment`)
  - fresh full regression - PASSED (`86 passed`, `--import-mode=importlib`)
  - Phases 1–14 qualification scripts - PASSED
  - tracked-secret scan and final diff checks - PASSED
  - GitHub publication/parity - PENDING publication completion
  - Notion publication - PENDING final publication record
  - deployment - NOT PERFORMED
- Remaining risks: R-043 lacks the complete fresh-install destructive/interrupted restore drill; R-045 lacks sustained capacity/parser/index/stale-job/retention and bounded usage evidence; R-048 lacks the full independent source-class recovery matrix; R-053 lacks external assistive-technology evidence; R-044 retain remains unavailable; R-056 remains OPEN; Phase 15/V1 remains FAIL at 14/26.
- Blockers: authenticated Notion write connector availability and the remaining environment-backed qualification criteria.
- Follow-up directive: none
