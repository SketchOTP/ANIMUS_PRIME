# Phase 15 qualification continuation 015

- Baseline: `PRIME-SPEC-V1.0.0`
- Directive: `D-PRIME-PHASE15-REMEDIATION-015`
- Qualification date: `2026-08-11`
- Implementation defect repair commit: `344efd6`
- Deployment: `NOT PERFORMED`

## Objective

Remove the locally solvable PostgreSQL qualification blocker, execute the clean database-backed qualification matrix, repair any actual defect exposed by that execution, and preserve the implementation/qualification distinction.

## Disposable database precheck

The existing approved `docker-compose.phase1.yml` path was used. The PostgreSQL service was recreated from a fresh container with no host volume. No production data was used.

| Check | Result | Non-secret evidence |
|---|---|---|
| PostgreSQL reachable | PASS | Container health `healthy`; application role connected |
| PostgreSQL version | PASS | `17.10 (Debian 17.10-1.pgdg12+1)` |
| pgvector available | PASS | Available/default version `0.8.2`; enabled extension version `0.8.2` |
| Empty disposable database | PASS | `prime_core` user tables `0`; `schema_migrations` absent before migration |
| Application role connection | PASS | role `prime`, database `prime`; password omitted |
| Migrations from zero | PASS | all 24 migrations applied |

The image contains pgvector but a new database does not enable the extension automatically. The approved `vector` extension was explicitly enabled in this disposable database before migration. No credential or connection-string secret is retained in this evidence.

## Qualification execution

The complete runner was executed with both `PRIME_PHASE1_DB_URL` and `PRIME_DATABASE_URL` pointing at the disposable host-mapped database. The values are intentionally not recorded.

| Area | Result |
|---|---|
| Phase 1 migration gate | PASS |
| Phase 2 migration gate | PASS |
| Phase 3 migration gate | PASS |
| Phase 4 migration gate | PASS |
| Phase 5 migration gate | PASS |
| Phase 6 migration gate | PASS |
| Phase 7 migration gate | PASS |
| Phase 8 migration gate | PASS |
| Phase 9 migration gate | PASS |
| Phase 10 migration gate | PASS |
| Phase 11 migration gate | PASS |
| Phase 12 migration gate | PASS |
| Phase 13 migration gate | PASS |
| Phase 14 qualification | PASS |
| Full regression with database available | PASS — `71 passed` |
| Governance validation before runner | PASS |
| Final Phase 15/V1 gate | FAIL — truthful; `0/26 VERIFIED` |

Post-run non-secret database metadata: schema revision `0024_ai_execution.sql`, migration rows `24`, `prime_core` user tables `51`, populated qualification projects `13`, and persisted AI runs `1`.

An additional suite invocation against that already-populated database produced three expected state-collision failures (bootstrap already initialized, duplicate fixed repository fingerprint, and an event checkpoint already consumed). That invocation was not used as qualification evidence. The database was recreated again and the complete runner was rerun from zero; that authoritative fresh run passed all `71` tests.

## Defect found and repaired

The first database-backed run exposed a real defect in `src/prime_core/ai_service.py`: the `ai_runs` INSERT declared 21 columns but supplied 22 PostgreSQL placeholders, causing the actual Ask path to fail before returning its required UNKNOWN result. The extra placeholder was removed. Focused requalification passed (`7 passed`), followed by the fresh-from-zero complete run (`71 passed`).

## Requirement-centric state

- Implementation convergence: `25/26`; R-056 remains `OPEN`.
- Qualification: `VERIFIED 0/26`; `partial 9`; `blocked_by_environment 17`; `failed 0`.
- R-042–R-050 database-backed smoke and migration paths are now executable and passed their available local regression coverage, but remain `partial` because their ledger criteria still require off-machine/fresh-install, live Hindsight, sustained capacity, full historical, recovery, and/or product-path evidence.
- R-031–R-041 remain `BLOCKED_BY_ENVIRONMENT` for native Linux/Windows, Tailscale, and live Notion criteria.
- R-051–R-055 remain `BLOCKED_BY_ENVIRONMENT` for supported browser, approved provider/local inference, and live cross-surface criteria.
- R-056 remains `BLOCKED_BY_ENVIRONMENT`/`OPEN` pending the required fresh-install integrated environment.

No requirement was promoted to `VERIFIED` solely because the regression suite passed. No normative requirement, architecture, or baseline was changed.

## Remaining environment gaps

The following were not available and are not simulated: native Linux service/reboot, Windows service/reboot, approved second-device Tailscale tailnet, live Notion credential/provider capability, off-machine recovery target, live Hindsight, sustained capacity fixture, supported browser/accessibility acceptance, approved model or approved local inference runtime, and fresh-install R-056 environment. Codebase-memory MCP remained unavailable with `Transport closed`; targeted inspection was used only for non-code/configuration and governance reconciliation.

## Final result

```text
database qualification: PASS
Phase 1–14: PASS
full database-backed regression: PASS (71 passed)
Phase 15: FAIL
VERIFIED: 0/26
R-056: OPEN
Deployment: NOT PERFORMED
V1: FAIL
```
