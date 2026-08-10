# Phase 15 skipped-test inventory

Baseline: `PRIME-SPEC-V1.0.0`  
Checkpoint: Continuation 005  
Observed command: `python3 -m pytest tests -q -rs`  
Observed result: `23 passed, 15 skipped`

Skipped tests are unproven release evidence. The PostgreSQL integration prerequisite is not available on this host because `PRIME_PHASE1_DB_URL` is unset. The test-level mapping below is conservative: a skipped integration test keeps the listed requirement open and does not promote it to `VERIFIED`.

| Test | Requirement(s) | Reason skipped | Required environment | Release blocking | Qualification method |
| --- | --- | --- | --- | --- | --- |
| `tests/phase1/test_core.py::test_bootstrap_and_login`, `::test_project_creation`, `::test_auth_recovery` | R-001, R-002, R-003, R-056 | `PRIME_PHASE1_DB_URL` unset | Qualified PostgreSQL/pgvector/Core stack | Yes for full V1 integration | Run against a fresh qualified Phase-1 database; capture bootstrap, auth, recovery and isolation results. |
| `tests/phase3/test_onboarding.py::test_onboarding_creates_project`, `::test_onboarding_rejects_bad_authority` | R-003, R-006, R-034, R-056 | `PRIME_PHASE1_DB_URL` unset | Fresh Core database plus repository/authority fixtures | Yes | Run onboarding from clean state; capture success, invalid-authority rejection, and persisted bindings. |
| `tests/phase4/test_indexer.py::test_indexer_builds_manifest` | R-011, R-046, R-048, R-049 | `PRIME_PHASE1_DB_URL` unset | PostgreSQL plus repository Git fixture | Yes | Build and search an indexed repository; capture revision, provenance, and historical checkpoint behavior. |
| `tests/phase5/test_memory_service.py::test_memory_is_project_scoped` | R-009, R-010, R-047, R-050, R-055 | `PRIME_PHASE1_DB_URL` unset | PostgreSQL plus qualified Hindsight adapter | Yes | Store/recall across isolated projects and correction/tombstone fixtures; capture source references and cutoff behavior. |
| `tests/phase6/test_mcp.py::test_mcp_grant_is_project_bound` | R-010, R-013, R-055 | `PRIME_PHASE1_DB_URL` unset | PostgreSQL and Core MCP grant service | Yes | Issue grants for Project A/B; assert cross-project denial and revocation/recovery behavior. |
| `tests/phase7/test_notion_projection.py::test_projection_round_trip` | R-008, R-037, R-038, R-039, R-040, R-041, R-056 | `PRIME_PHASE1_DB_URL` unset | PostgreSQL plus configured live Notion workspace/token | Yes | Execute real provider create/update/refresh/detach/reconcile/rollover lifecycle; retain before/after provider state. |
| `tests/phase8/test_progress.py::test_progress_requires_approved_baseline` | R-007, R-055 | `PRIME_PHASE1_DB_URL` unset | PostgreSQL and progress fixtures | Yes | Run pending/approved/rejected baseline and assessment flows with evidence references. |
| `tests/phase9/test_intelligence.py::test_search_is_project_scoped` | R-011, R-047, R-050, R-055 | `PRIME_PHASE1_DB_URL` unset | PostgreSQL, index, memory, and Evidence fixtures | Yes | Search/Ask Project A/B with retracted and historical sources; capture citations and isolation result. |
| `tests/phase10/test_brain.py::test_brain_is_derived_and_project_bound` | R-014, R-050, R-052, R-055 | `PRIME_PHASE1_DB_URL` unset | PostgreSQL and repository/history fixtures | Yes | Build current and historical Brain views; verify project binding and truthful missing-history state. |
| `tests/phase11/test_history.py::test_evidence_timelens_and_isolated_fork` | R-046, R-047, R-048, R-049, R-050, R-052, R-056 | `PRIME_PHASE1_DB_URL` unset | PostgreSQL, Git checkpoints, Evidence, and Hindsight fixtures | Yes | Run multi-commit Time Lens scenario, evidence capture/retraction, fork isolation, and partial/unavailable branches. |
| `tests/phase12/test_lifecycle.py::test_lifecycle_completion_and_destructive_step_up` | R-004, R-012, R-013, R-056 | `PRIME_PHASE1_DB_URL` unset | PostgreSQL and lifecycle fixture | Yes | Exercise lifecycle state machine and step-up destructive controls with audit/event evidence. |
| `tests/phase13/test_reliability.py::test_backup_record_and_diagnostics` | R-042, R-043, R-044, R-045, R-056 | `PRIME_PHASE1_DB_URL` unset | PostgreSQL, populated state, off-machine target, clean restore host | Yes | Run backup, corruption/wrong-key/interruption/collision and clean restore scenarios; capture manifests and state comparison. |

The two non-skipped Phase-12 remote-access unit tests and Phase-13 backup unit tests are local adapter evidence only. They do not replace the live Tailscale, native-service, or clean-restore qualifications required by R-031–R-056.
