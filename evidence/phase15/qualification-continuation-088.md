# ANIMUS PRIME — Phase 15 Continuation 088

## Acceptance

`PARTIAL` — the authorized Release Qualification Appliance was created and exercised on Atlas. The clean-install and restore-target boundaries produced direct browser evidence, and an expendable fixture reached terminal `DELETED` through the protected lifecycle API. The complete frozen clauses for the remaining twelve open DODs were not all satisfied. No V1, Phase 15, DOD-081, R-056, deployment, public exposure, or Phase 16 claim is made.

## Baseline

- Starting governed HEAD: `d20dc30e20532a4d1984a4b70baf8d4c59435142`
- Starting qualified implementation: `1d1f421e0c6201a49bc2b305c73bd41547237577`
- Final governed HEAD: `TO_BE_REPLACED`
- Repository: `/home/sketch/Projects/ANIMUS_PRIME`
- Worktree baseline: only preserved untracked `.codebase-memory/`, `.prime-evidence/`, `.vscode/`; the intentional appliance helper was added by this continuation.
- Canonical PRIME Core, PostgreSQL, Hindsight, and `node-041-atlas-native` remained running and untouched. No canonical Qualification Project record or repository was mutated.

## Runtime and appliance ledger

| Instance | Container / image | Database | State/evidence root | Listener | Result |
|---|---|---|---|---|---|
| Canonical | `animus-prime-core` / `animus-prime-core:continuation-086-warm-start-notion` | persistent `prime` | existing Atlas runtime | private `127.0.0.1:8000` | preserved; live health passed |
| A clean | `prime-qual-088-a-clean` / same pinned image | isolated `prime088_a` | `/home/sketch/ANIMUS_PRIME_V1_QUALIFICATION_LAB/088/a-clean/{state,evidence}` | private `127.0.0.1:18100` | live health passed; authenticated fresh setup |
| B restore | `prime-qual-088-b-restore` / same pinned image | isolated `prime088_b` | `/home/sketch/ANIMUS_PRIME_V1_QUALIFICATION_LAB/088/b-restore/{state,evidence}` | private `127.0.0.1:18200` | live health passed; authenticated empty restore target |

All appliance containers carry `animus.prime.qualification=V1_QUALIFICATION_FIXTURE` and `animus.prime.continuation=088`. The appliance helper uses separate databases, state roots, evidence roots, ports, and operator identities. It does not replace or restart unrelated services. PostgreSQL is the existing persistent Atlas PostgreSQL container and Hindsight is the existing `mimir-hindsight-production` service.

The existing canonical Node remains `node-041-atlas-native` and enrolled on the canonical Core. A and B each report zero enrolled Nodes. Re-enrolling that same persistent Node into a second Core would mutate its durable trust identity, so no duplicate or synthetic Node was created. This is the concrete clean-appliance onboarding boundary, not a missing-target claim.

## Browser/operator evidence

Browser: gstack `/browse` real Chromium through Atlas SSH tunnels; A `http://127.0.0.1:18100/`, B `http://127.0.0.1:18200/`.

### A — fresh setup and project lifecycle

- Fresh initialization succeeded; protected state loaded after password sign-in.
- Home/System Health showed Core connected, schema `0039_usage_limits_and_upgrade_preflights.sql`, build `1d1f421e0c6201a49bc2b305c73bd41547237577`, and the pinned image.
- Setup status truthfully reported `UNCONFIGURED` Notion, `DEGRADED` Hindsight (`service_connectivity=CURRENT; retain=DEGRADED; recall=DEGRADED; reflect=UNAVAILABLE; mental_models=UNSUPPORTED`), and `REQUIRES_ACTION` for Nodes/allowed roots/first project.
- A real expendable project fixture was created through the browser and marked `V1_QUALIFICATION_FIXTURE`; no repository or Node was attached because the appliance had no enrolled Node.
- Delete preflight exposed exact target, no repository, no Node, and recent-step-up requirement. Wrong identity was refused with no mutation.
- After browser step-up and exact identity confirmation, the protected `DELETE` phase reached `DELETION_PENDING`. The normal UI does not expose the terminal `PURGE` action; the protected product API was exercised with the same session and exact confirmation, and the fixture reached `DELETED`.
- A second attempt to reuse the first preflight was rejected as stale, and the UI's repeated `DELETE` action correctly refused the invalid `DELETION_PENDING → DELETION_PENDING` transition. This is an operator-surface gap for complete browser-only DOD-077 closure, not a fabricated pass.

### B — empty restore target

- Fresh initialization and authenticated browser entry succeeded.
- The restore surface showed no verified backup (`records=0`, `latest verified=NONE`) and guarded restore with recent step-up.
- Empty-input restore preflight was refused with HTTP 422. A nonexistent path inside the marked B restore root was also refused with HTTP 422. No restore mutation occurred.
- A complete browser restore/restart fidelity run was not claimed because no valid appliance backup containing a bound project could be produced without a legitimate enrolled Node/repository operation.

## Hindsight and integrations

- Existing Hindsight `/health` returned healthy and connected. The fresh appliance product status remained `retain=DEGRADED`, `recall=DEGRADED`, `Reflect=UNAVAILABLE`, `Mental Models=UNSUPPORTED` because no project-bound bank with admitted source data was available in the clean instance. Historical canonical Mental Model qualification was not rewritten.
- Notion was not configured in the appliance. No credential was printed, copied into evidence, or placed in fixture state.
- Public exposure remained absent; unrelated Tailscale Serve/Funnel state was not changed.

## Twelve-row open DOD matrix

| DOD | Continuation-088 result | Governed disposition |
|---|---|---|
| DOD-004 | No new durable interruption/reconciliation promotion; appliance cannot execute bound multi-system flow without a Node/repository. | OPEN — durable workflow breadth |
| DOD-013 | No second approved tailnet device; no Funnel changes. | OPEN — `ACTUAL_SECOND_APPROVED_TAILNET_DEVICE_REQUIRED` |
| DOD-016 | No fork run; clean appliance has no enrolled Node and complete child Notion/Hindsight isolation remains unqualified. | OPEN — child resources plus complete browser path |
| DOD-044 | Fresh A onboarding/auth/setup status passed; Node, roots, Hindsight recovery, and full restart/resume matrix did not. | PARTIAL — clean-install Node/Hindsight continuation required |
| DOD-047 | No provider cost change. | PARTIAL — `APPROVED_PROVIDER_PROFILE_WITH_AUTHORITATIVE_COST_ATTRIBUTION_REQUIRED_FOR_REMAINING_CLAUSE` |
| DOD-049 | B is a real empty restore target; invalid/missing restore inputs refused. No bound-project backup restore/restart fidelity run. | PARTIAL — bound-project restore source and complete browser/restart path remain |
| DOD-053 | No second physical LAN machine was invented. | OPEN — `ACTUAL_SECOND_ENROLLED_LAN_MACHINE_REQUIRED` |
| DOD-055 | Fresh A project creation and protected refusal boundary exercised; no enrolled Node means approved repository creation/interruption side effect could not begin. | PARTIAL — real Node-backed creation/recovery path required |
| DOD-077 | Wrong target, step-up, exact confirmation, stale preflight, protected PURGE, and terminal fixture deletion exercised. | PARTIAL — terminal path is API-only in current UI; full browser audit/recovery matrix remains |
| DOD-079 | Atlas Linux host/package inventory inspected; no native installer/restart qualification and no supported Windows host. | BLOCKED_BY_ENVIRONMENT — Linux installer/restart and Windows target remain |
| DOD-080 | No new full clean-session visual/accessibility sweep. | OPEN — complete product polish qualification |
| DOD-081 / R-056 | Aggregate gate intentionally not attempted until all prerequisites and external resources close. | OPEN / GATED |

## Validation

- Supported regression: `PASSED` — `125 passed / 29 skipped / 0 failed`; run with `.venv/bin/python` and isolated `/dev/shm` pytest temp root after removing only disposable `/tmp/pytest-of-sketch` artifacts. The earlier host-Python invocation failed at collection because system Python lacked `psycopg`; it is recorded as an unsupported invocation, not regression evidence.
- Compileall: `PASSED`.
- Governance validator `--mode ADOPTED`: `PASSED`.
- Burndown validator: `PASSED` — 69 complete / 12 open; audit total 81; work classes `1 LOCAL_CODE / 5 LOCAL_BROWSER_QUALIFICATION / 6 EXTERNAL_ENVIRONMENT`.
- `git diff --check`: `PASSED`.
- Product alignment: `NOT PASSED` — correctly remains incomplete because the frozen V1 gate is not closed.
- Browser: `PASSED` for the bounded A/B setup, restore-negative, and deletion fixture checks; complete DOD closure remains partial as stated above.
- Secret scan: `PASSED` — no raw credentials or session/preflight values were written to repository/evidence.

## Changed files

- `scripts/phase15_qualification_appliance_088.py` — marked A/B appliance creation with isolated state/evidence roots and fixture-local Notion credential state override.
- `evidence/phase15/qualification-continuation-088.md`.
- Governed status and append-only `.agent` records updated only with Continuation-088 evidence and exact remaining gates.

## Release boundary

- No PRIME product implementation change.
- No deployment performed.
- No public exposure or Funnel change.
- No Phase 16.
- DOD-005 untouched.
- DOD-081/R-056 remain last and open.
