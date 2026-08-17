# ANIMUS PRIME — Phase 15 Qualification Continuation 081

## Acceptance

`PARTIAL` for the bounded consolidated local completion sweep.

Continuation 081 began from governed `7e6fa8ecffac71f1ef97b030b64294dffbe18cbf`. The qualified product implementation is `b58c94d50ad488de444b1a68309154000fdc26ee`. The qualification publication commit carrying this evidence is `31406b3d9d733948c59408d450d0f1aad27f3c37`; the final governed closeout commit is the subsequent metadata reconciliation commit. The initial governed queue was 59 complete / 22 open. After this continuation, the reconciled queue is 61 complete / 20 open.

Only DOD-026 and DOD-076 were promoted. DOD-024, DOD-054, DOD-057, and DOD-077 were requalified as truthful partials. No V1, Phase 15, deployment, public-exposure, Funnel, DOD-081, or R-056 claim is made.

## Baseline and execution boundary

- Specification: `PRIME-SPEC-V1.0.0` (unchanged).
- Authoritative checkout: `/home/sketch/Projects/ANIMUS_PRIME` on Atlas.
- Starting local/origin/main: `7e6fa8ecffac71f1ef97b030b64294dffbe18cbf`.
- Product commits: `855e70a4126e2c06ef052c667656b12fbbbfd921` and `b58c94d50ad488de444b1a68309154000fdc26ee`.
- Existing untracked `.codebase-memory/`, `.prime-evidence/`, and `.vscode/` were preserved. Existing unrelated dirty files were not staged or overwritten.
- No synthetic project, repository, Node, bank, Notion source, machine, or backup target was created.
- No history rewrite, destructive canonical-project mutation, public ingress, Funnel change, deployment, or Phase 16 work occurred.

## Persistent Atlas topology

| Component | Identity and runtime | Result |
|---|---|---|
| PostgreSQL | Existing `animus-prime-phase0-postgres-1`, container `528492d428b73656423758c2c51b4fb1dfddd8ec1cad158525be7d4fcca49a17`, persistent pgvector image | PASSED — running/healthy; reused |
| Hindsight | Existing `mimir-hindsight-production`, container `f55064ac0441cef0032afb6b7da3d5cc5017eebb787067372a0da2de46127552`, private `127.0.0.1:8888` | PASSED — existing health 200; reused |
| Repository Node | `animus-prime-node.service`, user systemd, MainPID `2003030`, private `127.0.0.1:18001`, canonical identity `node-041-atlas-native` | PASSED — active/enabled and used for live revision |
| PRIME Core | `animus-prime-core.service`, user systemd, container `eeb48ecbd20716c6df4e37838067d0d84f131dc1f112a08d93f82d5b0013b5a5`, image `animus-prime-core:continuation-081-final`, image revision label `b58c94d50ad488de444b1a68309154000fdc26ee` | PASSED — active, one instance, `/health/ready` and `/health/live` 200 |
| PRIME Web UI | Genuine UI served by the persistent Core on `127.0.0.1:18000`; browser reached it through local SSH tunnel `127.0.0.1:28000` | PASSED — real authenticated UI |

The Core image was rebuilt from the qualified implementation and the persistent service was replaced through the existing PRIME-owned service path while preserving mounts, environment references, database, Hindsight, Node, and project state. Core listener ownership remained private and unique. Public exposure is `NOT PERFORMED`; existing unrelated Funnel configuration was untouched. Startup persistence and Core restart recovery were `PASSED`.

## Operator qualification

Browser: real Chromium controlled through the approved gstack browser path. Interface: local SSH tunnel to the persistent Atlas Core. Authentication used the established trusted-host sign-in flow without recording the one-time approval code.

The real existing project was selected:

- Project: `Qualification Project`
- Project ID: `project_d9a1a5b609394282b62fc12c0d04634d`
- Bound repository: `/home/sketch/Projects/ANIMUS_PRIME`
- Node: `node-041-atlas-native`, ONLINE

Home, Needs Attention, Projects, System Health, Overview, Progress, Ask, Search, Memory, Knowledge, Evidence, Activity, Goal, Repository, Authority, Brain, Time Lens, AI Connections, and Settings were inspected where available. Existing provider/Notion/Hindsight degraded states remained truthful; no unavailable integration was papered over.

## Per-DOD results

### DOD-024 — lifecycle and destructive-action boundaries

`PARTIAL` / user-usable for the qualified reversible and preflight clauses. The real project successfully entered PAUSED, resumed, entered completion review, and canceled completion review; the final project state was ACTIVE and no terminal completion was executed. Delete, Remove, and Archive preflights were visibly distinct. Delete required exact project identity and recent step-up; a wrong target returned `WRONG_TARGET` without mutation. Remove and Archive preflights were canceled. Positive terminal completion and full destructive recovery remain open.

### DOD-026 — Progress / Goal Alignment / correction challenge

`USER_USABLE_VERIFIED` — promoted. The real Qualification Project exposed progress history, Goal Items, milestones, alignment state, stale-source correction, and reassessment history. The first live refresh exposed a product defect: Core used its checkout revision and then refused a persisted binding revision mismatch. The minimal repair made the refresh route obtain the canonical revision through `_git_state(project_id)`, allowed live revision reconciliation, marked older assessments stale, and linked an open stale-source correction to the new reassessment with `status: REASSESSED`.

Focused Continuation 081 checks passed 2/2. The final browser result created assessment `assessment_b99ee2e17bd3458a8d32c7127ae48083` against live revision `b58c94d50ad488de444b1a68309154000fdc26ee` and preserved correction `progress-correction_097c3abc859b4fb3b74a81726935fce8` with reassessment linkage. No false correction or synthetic goal was created.

### DOD-047 — usage and limits

`PARTIAL`. Existing usage/cost surfaces were inspected. Provider/cost-limit clauses that require unavailable provider/runtime resources remain unqualified; the UI reported bounded unavailable state rather than inventing values.

### DOD-049 — backup and recovery

`PARTIAL`. The real backup record `backup_c8e2ddbd53fd4c2a88d836c7fd5b77b9` exposed AES-256-GCM/PBKDF2-HMAC-SHA256 metadata and a restore preflight with recent step-up protection. No passphrase was recorded, and no export or destructive restore was executed. Full backup/recovery acceptance remains open.

### DOD-050 — upgrade behavior

`BACKEND_ONLY` / open. The UI contains upgrade-related text but no qualified operator upgrade endpoint/workflow. Upgrade implementation remains outside this sweep.

### DOD-053 — second LAN machine

`BACKEND_ONLY` / open. No legitimate second LAN machine was available. No substitute machine or synthetic target was created.

### DOD-054 — repository registration and binding safety

`PARTIAL`. Against the existing enrolled Node, canonical project inspection returned 200, `is_bare:false`, `authority_state:CURRENT`, and no duplicate binding. `/tmp`, traversal, nonexistent, and unknown-node cases were refused with 400/404 and no mutation. Registration with `confirm=false` correctly required operator confirmation. A fresh legitimate positive registration/binding target was not performed, so the complete row remains partial.

### DOD-057 — authority provisioning and idempotence

`PARTIAL`. The real current authority review returned `VALID` under `authority-file-contract-v1`, hash `2f1f7bbc...`; Adopt Current returned `CURRENT` with `rewrite NONE` and did not rewrite `.agent`. Fresh authority provisioning against a new legitimate target was unavailable and was not manufactured.

### DOD-058 — guided Goal workflow

`PARTIAL` / open. The existing Goal and project-goal state were visible. A fresh guided Goal creation/provisioning workflow was not executed because doing so would rewrite governed Qualification Project state without a necessary acceptance target.

### DOD-076 — reversible workflow controls

`USER_USABLE_VERIFIED` — promoted for its complete bounded contract. The real operator successfully exercised PAUSE, RESUME, completion review entry, and completion review cancellation; state persisted and returned to ACTIVE. No terminal completion was performed, and no destructive state was created.

### DOD-077 — destructive lifecycle security negatives

`PARTIAL`. Delete preflight required exact identity and recent step-up. A wrong target was refused safely with no mutation. The UI distinguished Delete from Remove and Archive. Positive deletion, full audit/recovery, and complete replay/CSRF matrix remain open.

### DOD-080 — responsive/accessibility polish

`PARTIAL`. At viewport `375x812`, `scrollWidth` equaled viewport width (`375`) with no horizontal overflow. Keyboard focus reached a critical control and computed focus outline was visible (`3px`, solid). The browser console was not clean because expected prior authentication/Notion/negative-case errors remained; this was recorded as partial rather than overstated.

## Conditional and external rows reassessed

The following remained honestly open because the required legitimate target or environment was absent: DOD-013 (second device/Tailscale), DOD-016 (distinct child Notion and Hindsight target), DOD-031 (real non-empty operator-selected Notion knowledge source), DOD-039 (alternate repository relocation), DOD-044 (fresh-install target), DOD-055 (clean-install target), and DOD-079 (native Windows/installer environment). DOD-005 remains deliberately parked because no real reversible source appeared. DOD-081 and R-056 remain aggregate and gated.

## Validation

- Focused Continuation 081 checks: `PASSED` — 2 passed.
- Phase 15 suite: `PASSED` — 52 passed, 10 skipped.
- Full supported Atlas regression: `PASSED` — 115 passed, 29 skipped. The increase from the 113-pass baseline is the two focused Continuation 081 tests; the skip count is unchanged.
- Persistent Core rebuild, service health, listener uniqueness, and runtime build provenance: `PASSED`.
- `compileall`: `PASSED`.
- `git diff --check`: `PASSED`.
- Governance validation: `PASSED` after correcting the Continuation 081 directive schema.
- Burndown validation: `PASSED` — audit total 81, complete 61, burndown 20, IDs/counts/status vocabulary consistent.
- Product alignment audit: `PASSED`; overall V1 product gate: `FAILED` because Phase 15 remains incomplete.
- Secret scan: run at final publication; no raw credential is included in this evidence.
- Git parity: run after final publication; final SHA is recorded in the governed ledger/matrix and publication record.

## Governance result

The audit now records 61 complete and 20 open, with DOD-026 and DOD-076 promoted to `USER_USABLE_VERIFIED`, DOD-024/054/057/077 reconciled as `PARTIAL`, and no change to parked/external/aggregate gates. The qualification ledger, remediation matrix, requirements traceability, burndown, `.agent/CURRENT.md`, and append-only outcome/learning/record entries are updated for Continuation 081. The main Notion SOT and Checkpoint 081 are updated only after final Git publication.

Deployment/public exposure: `NOT PERFORMED`.
