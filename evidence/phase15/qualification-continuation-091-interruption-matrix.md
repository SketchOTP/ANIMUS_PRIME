# Continuation 091 interruption and reconciliation matrix

| Boundary | Forced condition | First hard state | Independent resume/restart result | Duplicate/orphan result | Status |
|---|---|---|---|---|---|
| Fork clone | external clone succeeds before checkpoint | workflow RUNNING, clone exists | new Core service adopts valid clone and continues | one child project, one repository, exact source revision | PASS |
| Notion page | live page succeeds before checkpoint, Core exits with code 91 | PAGE_CREATED RUNNING, resource EXPECTED, process dead | exact authenticated request after service restart finds marker, records page, completes PAGE_BOUND | exact marker count 1; one durable page locator | PASS |
| Hindsight bank | repeated create after service instance change | stable bank identity | stable PUT/reread returns same project bank | one bank identity | PASS |
| Restore apply | canonical apply succeeds before generic checkpoint | generic workflow row is removed by intentional schema replacement; separate restore ledger survives | new process discovers completed restore and recreates/completes deterministic generic workflow | same restore ID and workflow ID; no second destructive apply | PASS |
| Compensation | supported reversible resource action | step/resource durable | compensation checkpoint plus RELEASED resource survives reread | no hidden CREATED resource | PASS |
| Unknown non-idempotent result | RUNNING step with only EXPECTED resource | replay refused | resume plan returns REPAIR_REQUIRED and diagnostics require operator action | orphan candidate is visible, never silently deleted | PASS |

Canonical live Notion proof:

- Fixture project: `project_cd318a4bb4234d99afabc20f2cc3e013` (`V1_QUALIFICATION_FIXTURE Continuation 091 Canonical Notion crash`).
- Workflow: `workflow_79ffaeba9a644fd59492aeac379d5519`.
- Crash process start: `2026-08-18T18:15:13.488969518Z`; finish: `2026-08-18T18:33:24.656213254Z`; exit code: `91`.
- Recovery process: PID `839775`, started `2026-08-18T18:37:59.394409365Z` on exact image `animus-prime-core:continuation-091-f3772ee`.
- Reconciled page: `3c0833cb-27ff-81db-8b72-c2b6abed8a30`; exact marker search count: `1`.
- Final workflow: `SUCCEEDED`, current step `PAGE_BOUND`, completed steps `PAGE_EXPECTED`, `PAGE_CREATED`, `PAGE_BOUND`; resource status `CREATED`.

Pre-existing canonical workflow shells remain visible and were not deleted or relabelled: `bootstrap`, `LOCAL_RELEASE_CLOSURE_082`, and `QUALIFICATION_MULTI_SYSTEM` are RUNNING historical/qualification records. They contain no newly hidden 091 external resource and are recorded as inherited state, not 091 success.
