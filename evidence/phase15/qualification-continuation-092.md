# ANIMUS PRIME Phase 15 Qualification Continuation 092

Date: 2026-08-18

Acceptance: PASS for the bounded Continuation 092 scope; Phase 15 and V1 remain incomplete.

## Authority and baseline

- Frozen specification: `PRIME-SPEC-V1.0.0`.
- Starting governed/public commit: `d10fc429387c6922fb4b2098d27b0be0a1f94bf7`.
- Qualified implementation commit: `006258ee4e0fcaa2fb67b179b7ec99e87e551f69`.
- Execution: direct Atlas at `/home/sketch/Projects/ANIMUS_PRIME`; no `Z:` path, disposable product stack, public exposure, deployment, or Phase 16.
- Canonical project, repository, persistent PostgreSQL, persistent Hindsight, and enrolled Node were preserved.
- Qualification used one explicitly named expendable fixture and its real repository, live Notion Project Record, Hindsight bank, MCP grant, and queued job. No synthetic canonical state or replacement service was used.

## Corrective implementation

Continuation 091's valid durable Fork/Notion/Hindsight/repository/provisioning/MCP/restore evidence is retained. Continuation 092 closes the destructive-workflow omission with:

- versioned schema for project deletion tombstones and lifecycle resource dispositions;
- durable ordered DELETE and PURGE workflow steps with stable workflow identity, recorded attempts, retry/reconciliation policy, and operator-visible terminal state;
- exact-bound-repository Node quarantine, restore, and purge constrained to the enrolled Node's approved root;
- Notion archive disposition with explicit disclosure that managed external content survives PRIME deletion;
- Hindsight bank deletion through the approved adapter;
- local project-controlled data purge followed by one minimal non-secret tombstone;
- fresh authorized preflight on resume, including stale/replayed and wrong-target refusal;
- process-death qualification seams that terminate the Core after selected external effects and permit same-workflow restart recovery;
- a real modal browser flow with Cancel first/focused, exact project and repository confirmation, step-up, external-survival/backup disclosure, distinct DELETE and PURGE actions, and terminal project clearing.

## Real fixture result

- Project: `project_1921e46142c54a63bdddf4ecea5dca0b` (`V1_QUALIFICATION_FIXTURE Continuation 092 Destructive Lifecycle`).
- Repository: `/home/sketch/Projects/ANIMUS_PRIME_V1_QUALIFICATION_092`; original commit `695efef...`.
- Node: existing enrolled `node-041-atlas-native`.
- DELETE workflow: `workflow_42786da1fc2f45268d5c8b7dae3d8cde` — SUCCEEDED.
- PURGE workflow: `workflow_13a4a59eb578441a922978ae40c812f3` — SUCCEEDED.
- Notion: the managed page was archived through the live connector and remained externally recoverable; managed content was not represented as physically erased.
- Repository: quarantined through the enrolled Node, then purged; original and quarantine paths are absent after completion.
- Hindsight: the fixture's real bank and retained memory were deleted through the approved adapter.
- Local state: project-controlled rows were removed; the project is scrubbed to `[PURGED]`/`DELETED`; one minimal tombstone and the required lifecycle/preflight/disposition audit records remain.
- Queued work was cancelled with `PROJECT_DELETION`; the project-bound MCP grant was revoked.
- The canonical ANIMUS PRIME repository remains intact.

## Protection and browser qualification

- CSRF refusal: PASSED with no mutation.
- Wrong project identity refusal: PASSED with no mutation.
- Wrong repository confirmation refusal: PASSED with no terminal mutation.
- Stale preflight refusal and fresh-preflight resume of the same active workflow: PASSED.
- Recent step-up: PASSED through the existing trusted-host local identity path.
- Cancel-first and initial focus on Cancel: PASSED.
- Exact project/repository identity, destructive distinction, external-survival, and backup disclosure: PASSED.
- Real browser DELETE then PURGE on an expendable fixture: PASSED; final state was DELETED and the terminal project was cleared from active UI state.
- Refresh, clean console, keyboard focus, and 390x844 no-horizontal-overflow check: PASSED.
- A malformed historical fixture stopped safely on missing disposition data and was not mutated further.

## Interruption and recovery

The exact matrix is recorded in `evidence/phase15/qualification-continuation-092-interruption-matrix.md`. The Core was deliberately terminated with exit code 91 after each authorized seam. Restart used the exact qualified image and resumed the same durable workflow without duplicate external resources or hidden orphan state.

## Runtime provenance

- Persistent Core container: `animus-prime-core`.
- Image: `animus-prime-core:continuation-092-006258e`.
- Image ID: `sha256:c772c18be0846c17e66281c3cee70fbf29b5b1f194c148e7ea91b8080f369f34`.
- Readiness build commit: `006258ee4e0fcaa2fb67b179b7ec99e87e551f69`.
- Schema: `0040_destructive_lifecycle_sagas.sql`.
- Listener: private `127.0.0.1:8000`; readiness `ready`.
- Node service: active/running, existing enrolled identity preserved.
- Rollback containers remain preserved; no unrelated listener or Funnel configuration changed.

## Validation

- Focused persistent destructive lifecycle suite: `6 passed` — PASSED.
- Focused default/browser-support suite after final UI repair: `4 passed / 1 skipped` — PASSED.
- Final supported regression: `141 passed / 35 skipped / 0 failed` — PASSED.
- An initial final-suite invocation found one derived burndown-count mismatch after DOD-004 was removed but DOD-077 was not yet removed. The governed view was corrected; the complete suite then passed. This was governance reconciliation, not a product regression.
- Persistent Core readiness/build/schema provenance: PASSED.
- Canonical repository preservation and fixture repository absence: PASSED.
- Governance, burndown, alignment, compile, diff, secret, and Git parity results are recorded at governed closeout.

## Governed result

- DOD-004: `PARTIAL` -> `PRODUCT_VERIFIED`.
- R-012 Phase 15: `REOPENED` -> `VERIFIED`.
- DOD-077: `PARTIAL` -> `USER_USABLE_VERIFIED`.
- Queue: `72 complete / 9 open` -> `74 complete / 7 open`.
- Remaining work classes: `0 LOCAL_CODE / 2 LOCAL_BROWSER_QUALIFICATION / 5 EXTERNAL_ENVIRONMENT`.
- DOD-081, R-056, Phase 15, V1, and deployment remain open or gated.
