# Phase 15 qualification continuation 016

- Baseline: `PRIME-SPEC-V1.0.0`
- Directive: `D-PRIME-PHASE15-REMEDIATION-016`
- Qualified implementation commit: `8893b2b5a6612eaa85b5767a80fe4b462069d4f1`
- Qualification date: `2026-08-11`
- Deployment: `NOT PERFORMED`

## Qualification gate

The approved disposable PostgreSQL/pgvector environment was recreated from zero before the authoritative run. The complete Phase-15 runner passed the database-backed regression and Phases 1–14. The aggregate Phase-15/V1 gate remains a truthful FAIL because only one requirement has complete row-level evidence and R-056 remains open.

| Check | Result | Evidence |
|---|---|---|
| Governance validation | PASS | `scripts/validate_governance.py --mode ADOPTED` |
| PostgreSQL | PASS | `17.10`; fresh application database |
| pgvector | PASS | `0.8.2`; explicitly enabled in the fresh database |
| Migrations from zero | PASS | `24/24`, final `0024_ai_execution.sql` |
| Full database-backed regression | PASS | `73 passed` |
| Phases 1–14 | PASS | phase runner gates 1 through 14 |
| Implementation convergence | PASS | `25/26`; R-056 remains open |
| Aggregate Phase 15/V1 | FAIL | `VERIFIED 1/26`; not a release pass |

## Newly verified requirement: R-049

`tests/phase15/test_requirement_qualification.py::test_r049_retained_checkpoint_survives_rewrite_gc_and_time_lens` passed against the real PostgreSQL service and a disposable real Git repository.

| Criterion | Result | Evidence |
|---|---|---|
| Positive — canonical checkpoint through `HistoryService` and PostgreSQL `SourceReference` | PASS | checkpoint row and source-reference identity were queried after registration |
| Positive — retained checkpoint survives process/service reopen | PASS | a new `HistoryService` instance reported `EXACT` |
| Negative — ordinary history no longer reconstructs State A | PASS | later B/C/D commits, ref deletion, reflog expiry, and `git gc --prune=now`; `git cat-file` rejected State A |
| Positive — PRIME-owned retained checkpoint remains available | PASS | checkpoint bundle status remained `EXACT` |
| Time Lens | PASS | actual `HistoryService.time_lens` selected `PRIME_GIT_CHECKPOINT` and reported repository/Git `EXACT` |
| Citation | PASS | Git `SourceReference` resolved `EXACT` against the retained revision |
| Degraded — missing/non-retained checkpoint | PASS | status was `UNAVAILABLE`; Time Lens was `PARTIAL`/`UNAVAILABLE`, never `EXACT` |
| Recovery — retained bundle removed and restored | PASS | citation changed to `UNAVAILABLE`, then returned to `EXACT` only after bundle restoration |
| Security — PRIME-owned boundary | PASS | retained bundle was outside the managed repository; no managed repository refs were created or mutated |

R-049 is therefore promoted independently:

```text
current_status: VERIFIED
qualification_status: verified
final_status: VERIFIED
remaining_gap: NONE
```

## R-046/R-047 evidence executed but not promoted

The real Evidence service test passed for managed-copy ingestion, SHA-256 identity, metadata/provenance, extraction/indexing, project isolation, current-to-historical citation drift, retraction visibility, purge-to-`UNAVAILABLE`, parser-unavailable degradation, and reindex recovery. The rows remain `PARTIAL` because the complete normative matrix also requires the remaining active-content/size/malformed fixtures, product-level Ask/Search/Progress/Documentation citation run, and continuity/reindex qualification evidence.

## Environment qualification observations

- Hindsight: real approved image/backend health was `CURRENT`; a disposable real bank was created and deleted after the probe. Retain verification degraded because no approved model/provider was configured, so this is not exact Hindsight qualification evidence. R-044 remains `PARTIAL` with that exact gap.
- Tailscale: real daemon `1.102.2` was signed in. Actual status was `DEGRADED` because an existing public Funnel was exposed; PRIME's actual `configure_serve` path refused with the required public-exposure safety error. No existing Serve/Funnel configuration was changed. R-035/R-036 remain `PARTIAL`; the exact remaining gap is private Serve qualification without the unrelated public Funnel and approved second-device reachability.
- Browser: real Chromium `150.0.7871.128` loaded the Core/Web qualification proxy and rendered the operator shell; `/health/live` returned `200`. Full fresh setup/auth/project/global-navigation, service-restart, keyboard, assistive-technology, and mobile interaction walkthrough was not completed, so R-051–R-053 remain `PARTIAL` with that exact interactive gap.
- Native Linux: the host is Linux with systemd running; installer syntax passed and no `prime-node.service` is installed. Actual service registration/start/reboot/upgrade was not run because the current operator lacks root and the installer writes `/etc`, `/opt`, and `/var`. R-031–R-034 remain `PARTIAL`/environment constrained; Windows remains independently unavailable.
- Notion: final bounded runtime/configuration discovery found no usable `NOTION_READONLY_KEY` or MyAssistant secret source. No secret value was printed or persisted. R-037–R-041 remain blocked by the exact missing live authorization/provider.
- AI: no approved PRIME provider/profile or approved local inference runtime was configured. Ambient unrelated credentials were not reused. R-054/R-055 remain blocked by that exact missing approved runtime.
- Off-machine recovery: no separately mounted physical/network target satisfying the specification was found. R-042 remains `PARTIAL` with the exact gap of an independent target.

## Reconciled qualification state

```text
VERIFIED: 1/26 — R-049
PARTIAL: R-031–R-036, R-042–R-048, R-050–R-053
BLOCKED_BY_ENVIRONMENT: R-037–R-041, R-054–R-056
FAILED: none
R-056: OPEN
Deployment: NOT PERFORMED
V1: FAIL
```

Codebase-memory MCP was attempted before code discovery and returned `Transport closed`; targeted local inspection was used only as the documented fallback. No normative requirement or baseline was changed.
