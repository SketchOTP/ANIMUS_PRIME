# ANIMUS PRIME — Phase 15 Continuation 080

## Scope and acceptance

Continuation 080 closes only DOD-032: durable, project-scoped AI Memory Activity for the existing PRIME MCP boundary. DOD-031 remains blocked by the absence of a legitimate non-empty operator-selected Notion knowledge source. DOD-005, DOD-081, R-056, Phase 16, deployment, and public exposure remain out of scope.

Acceptance: `MET` for DOD-032. The complete activity contract is now product-qualified through the existing persistent Atlas PRIME path. No synthetic project, repository, bank, memory, Notion page, Node, or replacement service was created.

## Baseline

- Frozen specification: `PRIME-SPEC-V1.0.0`.
- Starting governed/public PRIME HEAD: `824367aa70fe7205feb6fbcf3b32ceca7d27dca7`.
- Qualified implementation commit: `6852fe643b9e820e52f43f35f43590ca5ec289eb` (`feat(memory): persist MCP activity audit`).
- Starting worktree: tracked files clean; preserved untracked `.codebase-memory/`, `.prime-evidence/`, and `.vscode/`.
- Execution authority: direct Atlas SSH, `/home/sketch/Projects/ANIMUS_PRIME`; no `Z:` runtime path and no disposable environment.
- Existing Qualification Project: `project_d9a1a5b609394282b62fc12c0d04634d`.
- Existing Hindsight bank: `prime-project_d9a1a5b609394282b62fc12c0d04634d`.
- PostgreSQL, Hindsight, enrolled repository Node, PRIME Core, and PRIME Web UI were preserved.

## Repair

The previous Memory UI used generic `ai_runs` rows and could not prove the frozen AI Memory Activity identity contract. The bounded repair adds the PRIME-owned `prime_core.mcp_memory_activity` projection and records each public MCP call with:

- project, grant, and client/session identity;
- tool and request kind (`QUERY` or `OBJECTIVE`);
- bounded objective/query text with credential-like text redacted;
- returned memory IDs, source types, result count, and bounded request budgets;
- stored/reported memory IDs when applicable;
- status, response status, error code, and timestamp.

The Core project context exposes this derived activity projection. The real Memory UI renders it as `PROJECT_BOUND_MCP_MEMORY_CALLS` under `AI_MEMORY_ACTIVITY`; generic model executions remain a separate explicitly labelled surface. Raw tokens, raw model output, and chain of thought are not rendered or stored in this activity projection.

Changed implementation files:

- `migrations/prime/0038_mcp_memory_activity.sql`
- `src/prime_core/mcp_service.py`
- `apps/core/main.py`
- `apps/web/index.html`
- `tests/phase6/test_mcp.py`

## Real PRIME qualification

The authenticated PRIME operator console was opened against `http://127.0.0.1:28000/` using gstack. The existing Qualification Project was selected; its real bank and project identity were displayed. Before the real interaction, the UI showed `AI_MEMORY_ACTIVITY`, `project id: project_d9a1a5b609394282b62fc12c0d04634d`, `mcp call count: 0`, `primary source: PROJECT_BOUND_MCP_MEMORY_CALLS`, `model runs are separate: true`, and raw model output/chain of thought omitted.

Using a fresh bounded project grant through the actual PRIME API path, the following real public MCP calls were made against the existing Qualification Project:

1. `prime_memory_recall`, query: `What project continuity rules and recovery practices should the next coding session remember?`, `max_results: 4`.
2. `prime_memory_context`, objective: `Resume the existing ANIMUS PRIME project safely with its approved constraints and current continuity state.`, `max_tokens: 1200`.
3. `prime_memory_timeline`, `max_results: 4`.
4. `prime_memory_get` for the first returned memory ID.

The successful run returned genuine project memory results. The durable rows recorded:

- `prime_memory_recall`: `QUERY`, 4 returned IDs, source types `OBSERVATION` and `DECISION`, `response_status: CURRENT`, `status: SUCCEEDED`.
- `prime_memory_context`: `OBJECTIVE`, 8 returned IDs, source types `DECISION` and `OBSERVATION`, `max_tokens: 1200`, `status: SUCCEEDED`.
- `prime_memory_timeline`: 4 returned IDs, source type `OBSERVATION`, `max_results: 4`, `status: SUCCEEDED`.
- `prime_memory_get`: 1 returned ID, source type `OBSERVATION`, `status: SUCCEEDED`.

The Core context after restart exposed eight 080 activity rows for this project, including retries caused by the browser control boundary. All persisted rows were `SUCCEEDED`; the successful records retained project, grant, client, tool, request, result IDs, source types, and bounded budgets. Temporary 080 grants were revoked after qualification; activity history remained durable.

The UI/browser daemon was concurrently redirected to an unrelated GitHub tab between some commands. That environment issue prevented a clean second DOM snapshot after restart; it did not alter the PRIME result. The post-restart Core context is the exact persisted payload consumed by the Memory UI, and the pre-restart authenticated UI rendered the same activity surface contract and project scope. No unrelated browser tab or service was modified.

## Persistence and restart

Before restart:

- PRIME-owned container: `animus-prime-core`.
- Image: `animus-prime-core:continuation-080`.
- Container PID: `2018218`.
- Container start: `2026-08-17T08:20:18.094164652Z`.
- Service MainPID: `2018171`.
- Ready health: `schema_version: 0038_mcp_memory_activity.sql`, build commit `6852fe643b9e820e52f43f35f43590ca5ec289eb`.

After `systemctl --user restart animus-prime-core.service`:

- Container PID: `2041902`.
- Container start: `2026-08-17T08:36:56.093575097Z`.
- Service MainPID: `2041856`.
- Service state: `active`.
- Ready health: `status: ready`, same spec, image, build commit, build timestamp, service version, and schema 0038.
- Project context after restart: 8 durable `mcp_memory_activity` rows for the Qualification Project, all `SUCCEEDED`.

No duplicate Core instance, ephemeral database, mock service, duplicate project, or public listener was introduced.

## Governance reconciliation

- DOD-032: `USER_USABLE_VERIFIED`; missing behavior `NONE`; blocker `NONE`.
- DOD-031: unchanged `BACKEND_ONLY`, blocked by `LEGITIMATE_NONEMPTY_OPERATOR_SELECTED_NOTION_KNOWLEDGE_SOURCE_REQUIRED_FOR_WARM_START`.
- R-054: remains `VERIFIED`; Continuation 080 is added as supporting evidence.
- Burndown: DOD-032 removed from the actionable queue; `LOCAL_CODE` decreases from 6 to 5.
- DOD-005, DOD-081, R-056, Phase 16, deployment, and public exposure: unchanged/gated.
- Final governed publication commit: recorded in the final publication metadata update after commit.

## Validation

- Focused MCP tests: passed with approved integration test skipped when no explicit `PRIME_MCP_TEST_PROJECT_ID` is supplied; no test creates a persistent synthetic project.
- `compileall`: passed.
- `git diff --check`: passed.
- Persistent Core image build: passed.
- Persistent Core readiness before and after restart: passed.
- Real MCP API calls and durable activity projection: passed.
- Project scope/isolation: passed by existing grant boundary and Qualification Project identity.
- Governance, burndown, secret, regression, and parity checks: recorded at publication closeout.
- Deployment/public exposure: not performed.

## Remaining gaps

- DOD-031: legitimate non-empty operator-selected Notion knowledge source required.
- DOD-005: remains parked.
- Remaining external/provider/legitimate-target clauses, DOD-081, and R-056 remain open/gated.
- Phase 15 and V1 remain incomplete. No automatic Continuation 081 is authorized by this record.
