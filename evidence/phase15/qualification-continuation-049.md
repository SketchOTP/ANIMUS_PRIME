# ANIMUS PRIME — Continuation 049 Evidence

Baseline: PRIME-SPEC-V1.0.0
Authoritative execution: direct SSH / native Atlas only
Checkout: `/home/sketch/Projects/ANIMUS_PRIME`
Starting published main: `e08b65538f14623ff80b320013cc9f79bf592e62`
Disposable resources: NONE
Temporary Core: NO
Persistent Core listener: NO
Browser: NO
Deployment: NOT PERFORMED
Phase 16: NOT ENTERED
R-045 pressure: NOT ATTEMPTED
R-056: OPEN

## External discovery decisions

- DOD-038: REFERENCE Git-native worktree/ref/graph primitives; no new dependency.
- DOD-039: REFERENCE Git-native repository/worktree identity and relocation primitives; no new dependency.
- DOD-004: REFERENCE DBOS durable-workflow patterns; adoption DEFERRED because PRIME already owns PostgreSQL-backed workflow state; no architecture change.

## DOD-045 — PRODUCT_VERIFIED

The frozen §26.45 boundary is operator authentication and web-session protection for management and destructive operations. The §18.8 break-glass recovery credential remains owned by DOD-008 and is not duplicated as a DOD-045 blocker.

Direct route-matrix qualification passed for project management, Node management, repository binding, authority changes, Progress correction, and backup/restore. Mutating routes require an authenticated session plus CSRF; the security middleware rejects disallowed origins; restore requires explicit `X-PRIME-STEP-UP: CONFIRM`. Existing 048 evidence remains valid for login, wrong credentials, missing/expired/revoked sessions, digest-only token persistence, logout, CSRF/origin, management gating, and restore step-up rejection.

Exact residual: DOD-008 one-time break-glass recovery replay remains unavailable under the no-disposable-store constraint.
Final: PRODUCT_VERIFIED.

## DOD-008 — PARTIAL

Break-glass recovery and replacement-credential replay remain unqualified because the original one-time recovery credential is unavailable. No disposable operator database or temporary recovery store was created.
Final: PARTIAL.

## DOD-037 — PRODUCT_VERIFIED

Migration `0029_canonical_git_provenance.sql` persists `canonical_ref`, `canonical_ref_commit`, and update time independently of the active worktree. `CoreService.configure_canonical_ref` requires explicit operator confirmation, rejects short/unqualified refs and missing refs, resolves the configured ref to a commit, and never changes canonical truth when the active branch changes. The persistent ANIMUS PRIME binding is explicitly configured as `refs/heads/main` resolving to `b0c1238ca763870812e22dca4fdcd6c8e9abb1c3`.

Direct Atlas qualification observed active ref `main`, active HEAD `b0c1238ca763870812e22dca4fdcd6c8e9abb1c3`, dirty state `true` from preserved untracked `.codebase-memory/`, `.prime-evidence/`, and `.vscode/`, and worktree identity `/home/sketch/Projects/ANIMUS_PRIME/.git`. Dirty bytes classify as `WORKTREE_UNCOMMITTED`; clean graph checks classified HEAD as `CANONICAL_HEAD` and its parent as `ACCEPTED_IN_CANONICAL_HISTORY`; missing/unresolvable relationships return `UNKNOWN`. No new branch or worktree was created.
Final: PRODUCT_VERIFIED.

## DOD-038 — PRODUCT_VERIFIED

The existing memory schema already retained project, source reference/revision, branch context, and metadata. The implementation adds Git-native provenance metadata without a second Git or memory backend. New provenance records preserve project ID, canonical ref/commit, active ref/commit, worktree path/identity, dirty state, `acceptance_at_capture`, and `current_acceptance_overlay`. Historical capture metadata is not rewritten when later Git history changes; unavailable refs, unknown commits, and uncommitted sources remain `UNKNOWN` or `WORKTREE_UNCOMMITTED`. Existing six MCP tools remain unchanged; recall/timeline/get metadata is extended compatibly and project filtering is preserved.

Direct persistent qualification passed canonical, historical-ancestor, dirty-worktree, and unknown-relationship classifications plus authority project scope.
Final: PRODUCT_VERIFIED.

## DOD-028 — PRODUCT_VERIFIED

Authority classification now has explicit non-mutating `CURRENT`, `LEGACY`, `CONFLICT`, and `NONE` states. A recognized legacy snapshot produces `MIGRATE_REQUIRED` with `NONE_UNTIL_CONFIRMED` rewrite semantics and preserves original hashes; malformed/conflicting input produces `REVIEW_REQUIRED` and no rewrite. Explicit migration copies only known missing template files after confirmation. Existing current `REVIEW`, `ADOPT`, bootstrap-overwrite refusal, no-rewrite, and same-hash idempotency evidence remains valid. Historical validator legacy signatures were used as bounded legacy evidence; append-only project ledgers were not rewritten.
Final: PRODUCT_VERIFIED.

## Validation

- Direct Continuation 049 qualification script: PASSED.
- Focused regression with persistent mode: PASSED — 20 passed, 1 explicit `FRESH_STATE_REQUIRED` skip.
- Initial focused run without persistent mode: FAILED as an environment invocation mismatch (fresh bootstrap correctly returned 409); rerun with the required persistent flag passed.
- Compileall and `git diff --check`: PASSED.
- Full persistent suite: PASSED — 109 passed, 3 explicit `FRESH_STATE_REQUIRED` skips, 112 collected.
- Correct adopted governance validation: PASSED — 17 required files and 6 Cursor rules.
- Correct template governance validation: PASSED — 17 required files and 6 Cursor rules.
- Product burndown structural validation: PASSED — 81 audit rows, 42 complete, 39 burndown rows; `PRODUCT_VERIFIED=28`, `USER_USABLE_VERIFIED=14`, `PARTIAL=3`, `MISSING=0`.
- Product alignment audit: PASSED; broader V1 release alignment remains intentionally unmet.
- Compileall: PASSED.
- `git diff --check`: PASSED.
- Secret scan: PASSED — no credential-shaped committed values; matches were declarations or deliberate test/redaction fixtures.
- Persistent service health: PASSED — Hindsight healthy and PostgreSQL connected.
- Storage: PASSED — root available `24,405,065,728` bytes; `/mnt/storage1tb` available `159,130,316,800` bytes; no cleanup performed.

Implementation commit A: `b0c1238ca763870812e22dca4fdcd6c8e9abb1c3`.

## Closeout

Final validation and evidence/governance publication commit are recorded after the full persistent suite. No Core, browser, disposable resource, deployment, R-045 pressure, Phase 16, or R-056 aggregate run was performed. The bounded continuation closes `PARTIAL`: DOD-045, DOD-037, DOD-038, and DOD-028 are `PRODUCT_VERIFIED`; DOD-008 remains `PARTIAL`; DOD-006 remains unqualified by topology; DOD-039 and DOD-004 remain prior-art/reference-only decisions.
