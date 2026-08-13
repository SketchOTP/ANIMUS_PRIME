# ANIMUS PRIME — Continuation 032 Qualification and Publication Evidence

## Scope and lineage

- Directive: `D-PRIME-PHASE15-PRODUCT-COMPLETION-032`
- Frozen baseline: `PRIME-SPEC-V1.0.0`
- Continuation 031 published baseline: `2f9fcc3d55a61788bffb45a7d0555161fb3708c4`
- Prior bounded evidence: `evidence/phase15/product-goal-alignment-continuation-031.md`
- Notion execution record: page `3ba833cb-27ff-8176-b7f6-cd00f2de016e`, appended after publication and re-fetched for verification.

Continuation 031 publication closure occurred after its bounded evidence file was authored. This record reconciles that publication timing without rewriting the earlier evidence or outcome.

## Fresh startup diagnosis

The approved disposable stack was recreated from zero with Docker Desktop, PostgreSQL `17.10`, and the pinned pgvector image exposing extension version `0.8.2`. Before Core startup, `prime_core.schema_migrations` did not exist. Core then applied all 26 migrations in order: `0001_core.sql`, `0002_nodes.sql`, `0003_onboarding.sql`, `0004_indexing.sql`, `0005_memory.sql`, `0006_mcp.sql`, `0007_notion.sql`, `0008_progress.sql`, `0009_activity.sql`, `0010_brain.sql`, `0011_evidence_time_lens.sql`, `0012_lifecycle.sql`, `0013_reliability.sql`, `0014_remediation_foundations.sql`, `0015_evidence_lifecycle.sql`, `0016_historical_evidence.sql`, `0017_historical_revisions.sql`, `0018_historical_snapshot_immutability.sql`, `0019_evidence_parser_states.sql`, `0020_continuity_capacity.sql`, `0021_node_lifecycle.sql`, `0022_notion_lifecycle.sql`, `0023_notion_credential_reference.sql`, `0024_ai_execution.sql`, `0025_product_onboarding.sql`, and `0026_product_completion_wave3.sql`; lifespan startup logged `Application startup complete.` A Core restart returned `/health/live` with `{"status":"live","service":"prime-core"}`.

Result: fresh migration-from-zero `PASSED`; Core lifespan startup `PASSED`; Core restart `PASSED`. No migration SQLSTATE, exception, or failing statement was reproduced, so no migration repair or schema redesign was made. The earlier startup block was classified as unavailable Docker Desktop/disposable environment, not a migration defect.

## Demonstrated repair

The authenticated project-scoped MCP revoke path reproduced PostgreSQL `IndeterminateDatatype: could not determine the data type of parameter $2` from the nullable predicate `%s IS NULL`. `src/prime_core/mcp_service.py` now uses separate typed queries for global and project-scoped lookup. The regression proves wrong-project revoke is rejected, the grant remains usable, correct-project revoke succeeds, and the old token receives `PROJECT_SCOPE_VIOLATION`.

- Repair: project-scoped MCP revoke query branching.
- Migration repair: `NONE REQUIRED`.
- Regression: `tests/phase15/test_product_completion_032.py`.
- Repair commit: `015dbeefecaddab8f9b953142975961e0bae1d0d`.

## Authenticated fixture and qualification

One fresh authenticated operator session exercised two Git-backed projects, `Continuation 032 Fixture A2` and `Continuation 032 Fixture B2`, on enrolled Node roots. Credentials were ephemeral and were not recorded.

### Qualified

- GoalModel: approved goal revision, two required weighted GoalItems, baseline and assessment identity were visible.
- Progress: initial `68%` assessment and refreshed `90%` assessment were persisted with confidence `0.925`, goal revision identity, history, and `CURRENT` freshness.
- Stale-to-refresh: a controlled committed source change produced `STALE`; approved refresh returned `CURRENT`.
- AGENTS chain: API inventory returned nested `src/AGENTS.md` plus root `AGENTS.md` with ordered chain metadata.
- Activity filter: project activity returned `GIT_QUALIFICATION` and `PROGRESS_QUALIFICATION`; browser filter/load displayed the selected event.
- AI grant lifecycle: project scope, rotation, wrong-project isolation, revocation, and reissue were exercised; the narrow revoke repair passed.
- Repository/Authority/Git: canonical revision, branch, file tree, authority validity, hashes, and read-only state were visible after indexing.
- Brain source surface: API and browser controls loaded a source-labelled derived graph with `18` nodes, `10` edges, `derived-3d` layout, `SOURCE_BASED_ONLY` policy, and accessible node list.
- Fork selected revision: clean committed source `63a72d9003742a020201039633f774bfe4823286` was copied to an independent destination project; destination content matched the selected source revision and excluded later A2 content. Provenance reported memory `NONE`, Notion `NOT_COPIED`, and Hindsight `DEGRADED_OR_UNAVAILABLE`.
- A/B isolation: source and destination private markers were not recalled across projects; MCP context returned each project’s own ID; source progress was `CURRENT` while the destination awaited baseline.
- Browser integrity: authenticated project overview, Goal, Progress, Repository, Authority, Activity, Brain, and Fork controls loaded without console errors. The stale duplicate `NOT AVAILABLE` Fork claim was removed; the UI now directs operators to the Wave 3 controls.

### Not promoted

- DOD-016/017: backend selected-revision fork and isolation qualified, but the frozen complete browser workflow and non-copied external integration acceptance remain incomplete.
- DOD-040: API grant lifecycle qualified; complete visible AI Connections list/rotate/revoke workflow remains unqualified.
- DOD-041: AGENTS inventory qualified; external coding-agent precedence/conflict semantics remain unqualified.
- DOD-043: filter and project-bound events qualified; source drill-down remains incomplete because event `source_revision` is `NONE` in the current event insert path.
- DOD-050: Time Lens remains a descriptive surface with no demonstrated interactive historical selector completion.
- DOD-051: graph API/source labelling/accessibility fallback qualified; genuine interactive 3D orbit/pan/zoom, live update, and performance acceptance remain unqualified.
- DOD-062/063: GoalModel/progress and stale-refresh behavior qualified, but required-evidence enforcement and complete browser correction acceptance remain unqualified.
- Search exact frozen acceptance remains unpromoted pending its complete product-path reconciliation.

## Governed counts and preserved gaps

Mechanical qualification ledger state after this cycle remains:

- `16/26 VERIFIED`
- `9 partial`
- `1 blocked_by_environment` — `R-056 OPEN`
- `0 failed`

The §26 product audit count remains exactly `4 USER_USABLE_VERIFIED / 7 PRODUCT_VERIFIED / 22 IMPLEMENTED_NOT_PRODUCT_QUALIFIED / 31 BACKEND_ONLY / 9 UI_SHELL_ONLY / 7 PARTIAL / 0 MISSING / 1 BLOCKED_BY_ENVIRONMENT`. V1 Product Goal Alignment, Phase 15, and the overall V1 gate remain `FAIL`. No Phase 16/spec change or deployment occurred.

Preserved gaps: R-044 Hindsight retain remains unavailable; R-053 assistive-technology evidence remains unavailable; R-031–R-034 native Node qualification remains outstanding; R-035–R-036 signed-in Tailscale/second-device qualification remains outstanding; R-045 remains open for normative observability/enforcement; R-056 remains `KEEP OPEN`.

## Validation state

- Fresh PostgreSQL/pgvector migration and Core restart: `PASSED`
- MCP revoke regression: `PASSED`
- Python AST checks for modified Python: `PASSED`
- Web script parse: `PASSED`
- Authenticated browser controls and console error check: `PASSED`
- Governed-view status/count reconciliation: `PASSED`
- `git diff --check`: `PASSED`
- Full repository regression suite: `NOT RUN`
- Native Node, Tailscale/second device, live Notion write, approved Hindsight, assistive technology, full interactive 3D Brain/live update, and deployment: `NOT RUN`

## Publication closure

Publication commit SHA, local/origin parity, and Notion append verification are recorded in the final Continuation 032 publication update. Existing unrelated worktree changes were preserved and excluded from the governed commit.
