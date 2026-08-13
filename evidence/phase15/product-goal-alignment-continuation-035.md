# ANIMUS PRIME — Continuation 035 Evidence

- Directive: D-PRIME-PHASE15-V1-LOCAL-CLOSURE-035
- Date: 2026-08-13
- Checkout: /home/sketch/Projects/ANIMUS_PRIME
- Baseline: PRIME-SPEC-V1.0.0 (unchanged)
- Scope: deterministic pytest contract, semantic section 26 reconciliation, bounded local product qualification, exact environment boundaries
- Deployment: NOT PERFORMED

## 1. Test-contract repair and regression

The ordinary pytest command previously failed during collection because both scripts/test_validate_governance.py and authority-template/v1/scripts/test_validate_governance.py imported as the same top-level module name.

The smallest repair was committed in pytest.ini:

[pytest]
addopts = --import-mode=importlib

Validation:

- pytest tests scripts -q — PASSED (64 passed, 27 skipped) without the database gate.
- pytest -q — PASSED (64 passed, 27 skipped) without the database gate.
- pytest --collect-only -q — PASSED (91 tests collected).
- Fresh disposable PostgreSQL 17.10 + pgvector 0.8.2, database prime035, all 26 migrations — PASSED.
- Fresh database-backed pytest -q -rs — PASSED (91 passed in 21.64s).
- Phases 1–14 — PASSED.
- python -m compileall -q apps/core src scripts tests — PASSED.
- Web inline JavaScript extraction and node --check — PASSED.
- Focused Brain/Wave-3 regression — PASSED (4 passed).
- Disposable PostgreSQL container prime035-postgres was used only for qualification and is scheduled for cleanup after publication.

## 2. Semantic section 26 reconciliation

Every audit row now has an explicit acceptance_kind:

- ARCHITECTURAL_INVARIANT
- OPERATOR_WORKFLOW
- EXTERNAL_DEPENDENCY
- MIXED
- AGGREGATE_RELEASE_GATE

DOD-001 was reconciled from IMPLEMENTED_NOT_PRODUCT_QUALIFIED to PRODUCT_VERIFIED. The basis is the approved implementation baseline, governance-file contract, validator, and baseline-identity evidence. It is an architectural invariant and does not require a dedicated UI screen.

No other semantic promotion was made. DOD-002, DOD-004, DOD-005, DOD-006, DOD-014, DOD-015, DOD-017, DOD-018, DOD-021, DOD-022, DOD-040, DOD-043, DOD-051, DOD-059, DOD-060, DOD-061, DOD-062, DOD-063, and all remaining rows retain their prior truthful statuses.

Mechanical validation:

- Audit rows: 81.
- Complete rows: 12.
- Open burndown rows: 69.
- 12 + 69 = 81 — PASSED.
- IDs, required fields, statuses, work classes, concrete actions, and acceptance kinds — PASSED.
- PRODUCT_ALIGNMENT_AUDIT: PASS.
- V1_PRODUCT_GOAL_ALIGNMENT: FAIL remains the correct release result.
- Section 26 status counts: 4 USER_USABLE_VERIFIED / 8 PRODUCT_VERIFIED / 21 IMPLEMENTED_NOT_PRODUCT_QUALIFIED / 31 BACKEND_ONLY / 9 UI_SHELL_ONLY / 7 PARTIAL / 0 MISSING / 1 BLOCKED_BY_ENVIRONMENT.

## 3. Authenticated browser qualification

The browser used the required gstack browse wrapper against the native Atlas Core through a local SSH tunnel. No Z: path or SSHFS bind mount was used.

Project A (Continuity Handoff Fixture A) showed:

- authenticated current Overview and Since You Were Here;
- approved Goal revision and weighted Progress assessment;
- valid Authority files and read-only Repository tree;
- bounded context/export redaction;
- source-labelled Brain graph with EXACT, revision 59efcfeaa256fceaa41fce33f7883165b7f47de3, 10 nodes, 6 edges, SOURCE_BASED_ONLY, and accessible node list;
- safe UNKNOWN Ask because the configured model provider was unavailable;
- Activity events with explicit NO SOURCE ARTIFACT where the fixture emitted source-free events;
- Hindsight UNKNOWN/degraded-safe state and Notion REAUTH_REQUIRED/fixture-degraded state.

Time Lens:

- historical revision B returned HISTORICAL, PARTIAL, with repository/authority/evidence/progress/memory/Notion/Brain/Git source statuses visible;
- historical Goal reconstruction was unavailable and the basic Brain endpoint returned current, not historical, data;
- Ask at historical B returned safe UNKNOWN with no-data citations;
- Return to Now returned CURRENT, EXACT, with all current source statuses exact;
- DOD-014 and DOD-015 remain open.

Project isolation:

- selecting Project B and loading its graph returned UNAVAILABLE, UNKNOWN, zero nodes, zero edges, and no Project A source data;
- before this fix, the client retained the previously rendered A Brain graph until the operator clicked Load graph;
- apps/web/index.html now clears project-scoped Search, Brain, Activity, Repository, AI Connections, and Fork result state at the start of loadProject;
- after the fix, switching A to B immediately showed Load the graph for the selected project, with no stale A graph;
- browser reload plus the A to B state-reset regression had no console errors;
- Project B remains incomplete/unindexed, so DOD-017 is not promoted.

Repository and Activity surfaces loaded successfully. Mutation-proof, complete source-backed Activity drill-down, Progress correction, complete Search corpus, and provider-backed Ask remain unqualified.

## 4. Brain scale/live boundaries

Fixture-scale Brain qualification passed with 10 nodes and 6 edges, interactive controls, accessible list, source labels, revision identity, and source-only relationship policy.

Representative-scale capacity, live source observation/index refresh, and complete A/B independent Brain qualification were not established. They remain open.

## 5. Fork boundary

Fork submission correctly refused the disposable Project A fixture with:

fork requires a clean source working tree

Native Git confirmed the exact reason:

## main
?? .agent/PROJECT_GOAL.md
59efcfe fixture experiment progress

This is a truthful safety refusal, not a successful Fork/Clone qualification. DOD-017 remains open; no forked project was created.

## 6. Hindsight diagnosis

Atlas Hindsight is present and healthy at http://127.0.0.1:8888/health; the production container is mimir-hindsight-production and its database is connected.

The PRIME adapter and default MemoryService path currently hard-code http://127.0.0.1:18888, where no listener exists. This is a local adapter configuration defect.

A disposable direct probe against port 8888 established:

- health — CURRENT;
- bank create/delete — CURRENT;
- memory POST — HTTP 200 acknowledgment;
- recall — HTTP 200 with zero results.

Hindsight logs identify the remaining integration dependency: openai/routerbot-local retain extraction is slow (about 10–12 seconds) and extracts zero facts. Therefore an acknowledged retain is not a durable recallable result and remains DEGRADED. No Hindsight schema, service, or production data was changed. R-044 remains partial/open.

## 7. Exact external boundaries

- Linux/systemd: present, but no deterministic PRIME native Node installer/unit and no qualified PRIME service lifecycle evidence; no unrelated system service was adopted.
- Tailscale: existing Serve/Funnel state was not changed; no approved second-device/private-Serve qualification was available.
- Notion: Core remained REAUTH_REQUIRED/fixture-degraded; no token was printed or persisted. External Notion publication was attempted only through the configured connector and remains pending if the connector is unavailable.
- Assistive technology: no genuine approved AT environment was available; R-053 remains partial.
- No Phase 16, frozen-spec change, force-push, destructive project cleanup, or deployment occurred.

## 8. Governed result

Remediation remains:

- 16/26 VERIFIED
- 9 partial
- R-056 blocked/open
- 0 failed

The V1 and Phase 15 gates remain FAIL. Follow-up work is the remaining local qualification queue, the Brain/Fork completeness gaps, the Hindsight adapter/provider boundary, and the exact external environments.
