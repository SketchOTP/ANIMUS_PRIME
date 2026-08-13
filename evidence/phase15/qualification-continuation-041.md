# ANIMUS PRIME — Continuation 041 native-Atlas qualification

## Boundary

- Execution host: Atlas by direct SSH.
- Authoritative checkout: /home/sketch/Projects/ANIMUS_PRIME.
- Starting published tip: a9efb529dbd9a0bdd9edfd4f33fd54b6c856d609.
- No disposable database, container, project, fixture, or test environment was created in this continuation.
- Existing persistent Atlas PostgreSQL and production Hindsight were observed only; production Hindsight was not changed.
- Browser access used an SSH transport tunnel to the native Atlas Core listener. The tunnel was not a runtime or qualification environment.
- Deployment, Phase 16, R-056 closure, and production Hindsight changes were not performed.

## Native regression and service checks

- .venv/bin/pytest tests scripts -q: 75 passed, 28 skipped — PASSED.
- .venv/bin/pytest -q: 75 passed, 28 skipped — PASSED.
- .venv/bin/pytest --collect-only -q: 103 tests collected — PASSED.
- .venv/bin/python -m compileall -q apps src scripts tests: PASSED.
- Existing persistent Atlas qualification PostgreSQL had all 26 migrations. Direct Phase 0 through Phase 14 execution passed against that existing database without creating a replacement database.
- Native Core was started on Atlas at 127.0.0.1:18000, passed /health/live, and was used for browser qualification. Existing production Hindsight stayed healthy and untouched.

## Real Atlas project onboarding

The existing persistent Qualification Project was bound to the real repository and not replaced:

- repository: /home/sketch/Projects/ANIMUS_PRIME;
- node: Atlas Native Qualification Node;
- branch: main;
- canonical revision: a9efb529dbd9a0bdd9edfd4f33fd54b6c856d609;
- repository inspection: non-bare, current authority, no duplicate active binding;
- .agent authority adoption: VALID;
- goal revision: approved from repository .agent/PROJECT_GOAL.md;
- repository index: 4052 files, freshness CURRENT.

## Browser qualification

Authenticated browser qualification against the persistent Atlas project passed:

- Authority displayed .agent validation, source hash, contract, and observation time.
- Authority displayed the project-scoped AGENTS bridge target, instruction inventory, authority relationship, MCP relationship, and explicit precedence.
- Repository displayed the real Atlas path, identity fingerprint, canonical revision, branch, dirty state, recent commits, and worktrees.
- Repository tree opened .agent; .agent/CURRENT.md rendered bounded exact text with the current canonical revision.
- Activity displayed All, Code, Authority, Memory, Progress, Documentation, Git, and System category filters.
- Native Atlas activity rendered category, event type, sequence, observed time, source revision, payload, and either a source artifact or NO SOURCE ARTIFACT.
- Git filtering returned GIT_COMMIT. Authority filtering returned AUTHORITY_OBSERVED. System rendering returned NO SOURCE ARTIFACT. Source-artifact drill-down opened README.md and returned bounded exact text.
- Project-scoped Search for PROJECT_GOAL returned Repository results with current revision. Notion remained REAUTH_REQUIRED/unavailable in this Core process.
- Ask remained safe UNKNOWN because no approved model execution path was configured.

## Governed promotions

Direct browser evidence supports:
- DOD-041 USER_USABLE_VERIFIED;
- DOD-043 USER_USABLE_VERIFIED;
- DOD-059 USER_USABLE_VERIFIED;
- DOD-060 USER_USABLE_VERIFIED.

DOD-062 and DOD-063 remain open because the real project has no approved progress baseline or assessment. DOD-071 and DOD-073 remain open because native MCP store/recall returned degraded with durability_verified=false and no recalled result. DOD-016, DOD-021, DOD-022, DOD-068, R-045, and R-056 remain open or blocked at their exact existing boundaries.

## Mutation and security boundary

Before and after the browser read-only flow, Atlas git status remained the intended tracked apps/web/index.html modification plus the pre-existing untracked .codebase-memory/, .prime-evidence/, and .vscode/ directories. The browser Repository and Authority surfaces expose no mutation control. No repository or .agent content was changed by browser inspection.

## Validation state

- Full regression: PASSED.
- Collection and compilation: PASSED.
- Native Phase 0–14 persistent-Atlas run: PASSED.
- Browser AGENTS bridge, Activity filters/source drill-down, Repository/Authority, and Git metadata: PASSED.
- Native MCP durability: BLOCKED/DEGRADED.
- Notion capability: BLOCKED/REAUTH_REQUIRED.
- Approved model execution: BLOCKED/UNKNOWN.
- Approved Hindsight Mental Models/reflect: BLOCKED/UNAVAILABLE.
- R-045 sustained-capacity closure: NOT RUN as a promotion gate.
- R-056 and deployment: NOT PERFORMED.
