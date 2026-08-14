# ANIMUS PRIME — Continuation 050 Evidence

Baseline: PRIME-SPEC-V1.0.0
Authoritative execution: direct SSH / native Atlas only
Checkout: /home/sketch/Projects/ANIMUS_PRIME
Starting published main: 48927a2e9e9e07d01e8a6cf0bb9a0e6317a7ac78
Implementation commit A: b6c94b7378966d42912277e6c861c3cd75f4846c
Disposable resources: NONE
Temporary Core: NO
Persistent Core listener: NO
Browser: NO
Deployment: NOT PERFORMED
Phase 16: NOT ENTERED
R-045 pressure: NOT ATTEMPTED
R-056: OPEN

## External discovery record

- DOD-039: REFERENCE + BUILD using Git-native worktree/common-dir/ref/object primitives; no new dependency and no GitPython/libgit2/repository-management layer.
- DOD-004: REFERENCE + BUILD using DBOS-style durable step/checkpoint/resume semantics; DBOS adoption DEFERRED because PRIME remains PostgreSQL-owned; no new dependency.
- Temporal: DEFER/REJECT_FOR_V1 because it is a materially larger orchestration architecture than the bounded PRIME workflow contract.

## DOD-006 — IMPLEMENTED_NOT_PRODUCT_QUALIFIED

The latest genuine runtime/listener evidence is Continuation 041 at revision `a9efb529dbd9a0bdd9edfd4f33fd54b6c856d609`, which exercised the native Atlas Core/private runtime boundary. The network-relevant comparison from that revision to current main found only `apps/core/main.py` changed; the changed hunks are provenance, progress, authority, memory, and Git-state routes, with no bind/listener/CORS/network-plane semantic change. Classification: `UNRELATED_CHANGE` / network semantics unchanged by equivalence.

Current runtime topology was not available: no persistent Core/Node listener was present, and Core was not started. Exact residual: `CURRENT_RUNTIME_TOPOLOGY_QUALIFICATION_REQUIRED`. DOD-006 remains unpromoted.

## DOD-039 — BACKEND_ONLY / IMPLEMENTED_NOT_PRODUCT_QUALIFIED

The persistent ANIMUS PRIME binding remained stable at project `project_d9a1a5b609394282b62fc12c0d04634d` and repository `repo_1eb92bbce8d44309861368d8690247c6`, with canonical ref `refs/heads/main` and canonical commit equal to the implementation tip during qualification. The new continuity anchor records canonical ref/commit/tree, known Git objects, authority/project hash, worktree path, and location fingerprint without mutating `.git`.

The non-mutating preflight returned `LOGICAL_REPOSITORY_CONTINUITY_VERIFIED` for the existing binding, preserved stable project/repository IDs, verified canonical ref/commit/object/authority continuity, detected no duplicate active binding, and recorded a versioned preflight token. A missing destination returned `DESTINATION_ABSENT` without changing the binding. The cutover path uses stale-preflight checks, atomic repository/binding updates, prior/new location history, project event, audit event, and rollback-by-transaction semantics. Dirty relocated candidates refuse with `DIRTY_REBIND_REQUIRES_VERIFIABLE_WORKTREE_CONTINUITY`; Git repair is detected but never invoked automatically.

No legitimate alternate Atlas location/copy naturally existed. No repository, clone, worktree, or fixture was created. Exact residual: `REAL_RELOCATION_CUTOVER_NOT_AVAILABLE_UNDER_CURRENT_NONDISPOSABLE_CONSTRAINT`. DOD-039 remains unpromoted.

## DOD-004 — BACKEND_ONLY

Migration `0030_rebind_and_workflow_steps.sql` adds persistent `workflow_steps`, `workflow_resources`, binding revisioning, and repository rebind continuity tables. Workflow primitives provide bounded statuses, replay policies (`PURE_OR_DB_TRANSACTION`, `IDEMPOTENT_EXTERNAL`, `NON_IDEMPOTENT_EXTERNAL`), completed-step non-reexecution, retryable failure, ambiguous external outcome to `REPAIR_REQUIRED`, resource references without secrets, resume planning, and explicit repair reset.

`CREATE_REPOSITORY` now checkpoints directory creation, Git initialization, and binding through the existing WorkflowRun model. Focused contract tests cover completed-step skipping, retry policy, ambiguous non-idempotent effects, resume plans, canonical continuity refusal, and non-mutating candidate inspection.

Production inventory remains incomplete for promotion: `FORK_PROJECT`, Notion/Hindsight provider workflows, restore, archive/delete/purge, and full interruption/orphan qualification remain outside the generic durable step contract. DOD-004 remains BACKEND_ONLY with that exact residual; no persistent resource interruption or destructive recovery test was run.

## Conservative boundaries

- DOD-005: NOT ATTEMPTED; no source deletion or valuable-source retraction was performed.
- DOD-009: CONSERVATIVE; no Core/browser cache qualification was attempted.
- DOD-008: PARTIAL; no disposable recovery store and no reconstruction of the unavailable one-time credential.
- R-045: OPEN / NOT ATTEMPTED; no pressure, saturation, or artificial backlog.
- R-056: OPEN; no aggregate release run.

## Validation

- Direct Continuation 050 qualification: PASSED.
- Focused Continuation 050 contracts: PASSED — 6 passed.
- Persistent full regression: PASSED — 115 passed, 3 explicit `FRESH_STATE_REQUIRED` skips.
- Compileall: PASSED.
- `git diff --check`: PASSED.
- PostgreSQL migration `0030`: PASSED on the approved persistent Atlas database.
- Adopted governance validation: PASSED.
- Template governance validation: PASSED.
- Product gap burndown validation: PASSED; counts remain 81 total / 42 complete / 39 open.
- Product alignment audit: PASSED; broader `V1_PRODUCT_GOAL_ALIGNMENT: FAIL` remains by design.
- Secret scan: PASSED; matches were declarations, redacted/test fixtures, or token-handling code, with no committed credential-shaped value exposed.
- Hindsight health: PASSED; PostgreSQL connected.
- Listener check: PASSED for the bounded check; no listeners on ports 8000 or 18000.
- Storage checkpoint: PASSED; root available `24404140032` bytes and `/mnt/storage1tb` available `159130316800` bytes; no cleanup performed.
- Publication: implementation A is committed; evidence/governance commit B is the closeout commit for this record, followed by one push and parity verification.

## Closeout boundary

The continuation remains PARTIAL. No Core, browser, disposable resource, deployment, Phase 16, R-045 pressure, or R-056 aggregate run was performed. Evidence/governance commit B is the final tracked edit for this continuation; no post-publication tracked edits are permitted.
