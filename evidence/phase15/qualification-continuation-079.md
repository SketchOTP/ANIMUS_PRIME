# ANIMUS PRIME — Phase 15 Qualification Continuation 079

Status: PARTIAL — DOD-031 blocked by the absence of a legitimate non-empty selected Notion source; DOD-032 received a bounded persistent UI repair but remains unqualified for its complete frozen AI Memory Activity contract.

## Baseline and authority

- Frozen specification: `PRIME-SPEC-V1.0.0`
- Starting governed/public SHA: `aafeca7abbbfaa6db39dc1b44673fc8c48d8c08b`
- Product implementation commit: `7800f55afbabc217e858a4546b910760f1db2d71`
- Starting local HEAD/origin: `aafeca7abbbfaa6db39dc1b44673fc8c48d8c08b`
- Starting worktree state: preserved untracked `.codebase-memory/`, `.prime-evidence/`, and `.vscode/`; no unrelated files were staged.
- Execution authority: direct Atlas SSH at `/home/sketch/Projects/ANIMUS_PRIME`; no `Z:`/SSHFS runtime execution.
- Existing Qualification Project: `project_d9a1a5b609394282b62fc12c0d04634d`
- Existing PRIME bank: `prime-project_d9a1a5b609394282b62fc12c0d04634d`

## Notion source gate

The existing managed project record was inspected through the approved Notion capability:

- Managed record: `3be833cb-27ff-8159-add6-e883c1cc54af`
- Managed record state: BOUND; content contains PRIME-managed project overview/status/progress/history markers and operator-owned history child-page links.
- Approved probe page: `3be833cb-27ff-81aa-9fe2-ffb4fcf5f980`
- Probe page content: blank; PRIME bindings for continuations 075–078 are DETACHED/RETRACTED.
- Result: no legitimate, non-empty operator-selected Notion knowledge payload is available for Warm Start.
- No Notion page, memory, project, bank, repository, or synthetic source was created.

## Product repair

Observed gap: the existing `/v1/projects/{project_id}/context-export` data contained durable memory rows and AI runs, but the operator Memory surface rendered only a summary/partial row shape. The frozen §26.32 contract could not be directly inspected from the product.

Minimal repair in `7800f55`:

- `apps/core/main.py` now includes existing memory `content_hash`/`bank_id` and existing AI-run `input_tokens`/`output_tokens` in the bounded context export.
- `apps/web/index.html` now renders project-scoped `MEMORY_INSPECTOR`, `MEMORY_TIMELINE`, and `AI_MEMORY_ACTIVITY` rows from that existing durable context export.
- The UI displays source identity, revision, hash, status, class, bank, branch, timestamps, supersession, event payload, AI source-revision sets, token counts, provider/model/status, and the derived/non-authoritative Mental Model boundary.
- Raw model output, credentials, session tokens, authorization headers, and chain of thought remain omitted.
- No new memory record, event, Hindsight bank, Notion source, or project state was written by this repair.

## Persistent Atlas runtime

| Component | Result |
|---|---|
| PostgreSQL | Existing `animus-prime-phase0-postgres-1`; reused; healthy |
| Hindsight | Existing `mimir-hindsight-production`; reused; PRIME snapshot reports service/retain/recall/Reflect/Mental Models CURRENT |
| Repository Node | Existing `node-041-atlas-native`; ONLINE/ENROLLED; reused |
| PRIME Core | Existing PRIME-owned container rebuilt as `animus-prime-core:continuation-079` |
| Service manager | Existing user `animus-prime-core.service`; enabled and active after restart |
| Core listener | `127.0.0.1:18000`; private/local only |
| Health | `/health/ready` returned `status=ready`, spec `PRIME-SPEC-V1.0.0`, build commit `7800f55`, schema `0037_shared_retrieval_projection.sql` |
| Restart | Old Core container stopped/replaced with the same persistent state mount; service start at `2026-08-17T02:20:21.507767157Z`; health and project state recovered |
| Public exposure | None; no Funnel, firewall, or unrelated listener change |

## DOD-031 — Warm Start

Result: BLOCKED / NOT PROMOTED.

The existing `.agent` authority chain is available and the existing PRIME bank is populated, but the frozen criterion requires high-value `.agent` history plus explicitly selected Notion knowledge. The only approved probe page is blank and retracted; the managed project record contains PRIME-managed status/history metadata rather than a legitimate knowledge payload. Continuing would require fabricating or inventing a source, which is forbidden.

Exact operator prerequisite:

`LEGITIMATE_NONEMPTY_OPERATOR_SELECTED_NOTION_KNOWLEDGE_SOURCE_REQUIRED_FOR_WARM_START`

## DOD-032 — Memory Inspector / Timeline / AI Memory Activity

Result: PARTIAL / NOT PROMOTED.

Authenticated browser: gstack `/browse`, through the real Core-served UI at `http://127.0.0.1:28000/`, trusted PRIME host sign-in, existing Qualification Project.

Observed after reload:

- `MEMORY_INSPECTOR`: 16 existing durable records rendered with memory ID, class, status, content, source reference, source revision, content hash, bank, branch, timestamp, supersession, project scope, and authority truth boundary.
- `MEMORY_TIMELINE`: 20 existing project events rendered in observed-time order with event type, sequence, timestamp, source revision, source reference, payload, and project scope.
- `AI_MEMORY_ACTIVITY`: 8 existing persisted AI runs rendered with run ID, capability, provider/model, status, source-revision identity set, input/output token counts, timestamp, and error state.
- Mental Model state rendered as `DERIVED_NON_AUTHORITATIVE`, authoritative `NO`, with the existing PRIME bank identity.
- Project isolation: all inspected rows carried the existing Qualification Project ID; no other project’s bank or records were returned.
- Restart/reload: the same project, bank, memory count, model identity, repository binding, and history remained available after the persistent Core service restart.
- Browser network after the restart: snapshot/context export, health, setup, agent chain, usage, activity, and project UI routes returned 200. The separate `/v1/projects/{project_id}/notion` request returned 503 and remains a truthful degraded boundary; no stale Notion payload was presented as current.
- Browser console: no new JavaScript exception; the isolated 503 was recorded as a service response.

Remaining complete-contract gap:

The frozen AI Memory Activity clause requires the originating objective/query, returned memory IDs, and session/client identity. The current durable `ai_runs`/event schema does not retain/display those fields. The UI therefore does not claim them and DOD-032 remains `IMPLEMENTED_NOT_PRODUCT_QUALIFIED` with blocker `AI_MEMORY_ACTIVITY_QUERY_RETURNED_MEMORY_AND_SESSION_IDENTITY_NOT_PERSISTED`.

## Governed reconciliation

- DOD-016 remains `IMPLEMENTED_NOT_PRODUCT_QUALIFIED`; stale Hindsight wording was replaced with `LEGITIMATE_DISTINCT_CHILD_NOTION_PROJECT_RECORD_AND_CHILD_HINDSIGHT_TARGET_REQUIRED`.
- DOD-031 remains `BACKEND_ONLY`; blocker now identifies the exact legitimate non-empty Notion source prerequisite.
- DOD-032 is now `IMPLEMENTED_NOT_PRODUCT_QUALIFIED`; stale Hindsight/UI-shell wording was replaced with the exact durable AI activity schema gap.
- DOD-044 remains `IMPLEMENTED_NOT_PRODUCT_QUALIFIED`; stale Hindsight wording was replaced with `LEGITIMATE_FRESH_INSTALL_BROWSER_TARGET_REQUIRED_FOR_COMPLETE_ONBOARDING`.
- No requirement was promoted by this continuation.
- Queue remains 58 complete / 23 open; this run changed classification and evidence, not the governed complete/open count.
- DOD-005, DOD-016 completion, DOD-044 completion, DOD-081, R-056, Phase 16, deployment, and public exposure remain outside this bounded closure.

## Validation

- Focused phase15 tests: PASSED — 50 passed, 10 skipped.
- Full repository regression: PASSED — 113 passed, 28 skipped. The skip count remains the established integration boundary; no new skip was treated as an improvement.
- Python compileall: PASSED.
- Git diff check: PASSED.
- Persistent Core image build: PASSED with exact build commit `7800f55afbabc217e858a4546b910760f1db2d71`.
- Persistent Core service restart/recovery: PASSED.
- Authenticated browser Memory Inspector/Timeline/AI Memory Activity requalification: PASSED for the bounded data-backed surfaces; complete DOD-032 acceptance remains OPEN.
- Hindsight/PRIME bank and Mental Model durability: PASSED by existing persistent state; no new model was created.
- Governance validation: PASSED (ADOPTED).
- Burndown validation: PASSED (58 complete, 23 open; status and work-class totals match).
- Alignment audit reconciliation: PASSED.
- Git diff check: PASSED.
- Secret scan: PASSED; no tracked credential pattern found.
- Local/origin parity: PASSED at publication closeout.
- Deployment/public exposure: NOT PERFORMED.

## Acceptance

Continuation 079 is PARTIAL. It establishes the real persistent data-backed Memory surfaces and removes the obsolete Hindsight blocker wording, but it does not fabricate the missing Notion Warm Start source or the missing AI Memory Activity identity fields. No automatic Continuation 080 is authorized by this record.
