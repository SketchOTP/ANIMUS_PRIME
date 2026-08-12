# ANIMUS PRIME — Phase 15 Qualification Continuation 026

- Date: 2026-08-12
- Baseline: `PRIME-SPEC-V1.0.0`
- Starting governed commit: `260cba8c207c5dd3036b2ee3094d92ccf47d980a`
- Qualification implementation commit: `5c2ec8e`
- Deployment: `NOT PERFORMED`

## Scope and decision

Continuation 026 continued the locally actionable historical and recovery work. R-042 and R-052 were not rerun. R-050 is promoted to `VERIFIED` because the complete populated State-B browser boundary, historical Ask/Brain cutoff, source-loss degradation, exact source restoration, and Return to Now path were exercised against a real disposable PRIME fixture. R-043, R-045, and R-048 remain `partial`; their exact normative gaps remain open below.

## Native regression

Against a freshly recreated disposable PostgreSQL/pgvector stack:

- R-049 retained checkpoint regression: `PASSED`.
- R-043 continuity backup/clean restore/interruption regression: `PASSED`.
- R-045 queue/quota/disk-pressure regression: `PASSED`.
- R-048/R-050 historical A/B/C/D Ask/Brain/Return-to-Now regression: `PASSED`.
- Focused result: `4 passed`.
- Fresh full regression: `PASSED` (`86 passed`, `--import-mode=importlib`).
- `tests/phase14/test_web_shell.py`: `PASSED` (`1 passed`).
- Native `compileall` for `src`, `apps`, and `scripts`: `PASSED`.
- Phase 1 through Phase 14 qualification scripts: `PASSED`.

## Real historical fixture and browser evidence

A disposable database fixture created a real Git repository with four commits and durable PRIME records for repository, authority, Goal, Progress, Evidence, Memory, Notion projection, Brain, and retained Git checkpoint state:

- Project: `project_3d010409db8347898f8c083a23ce7e8f`.
- State A: `e07214ced9185951be2487b8dca81c57491c5810`.
- State B: `a553fba826a184034fe846e4a74a4a51013bda18`.
- State C: `70b4250302d43547de4610210be3b791b371a9b8`.
- State D: `39e94a9c012de8d9849979364765f819234966ee`.
- State-B cutoff: `2026-08-12T19:37:33.329631+00:00`.

The supported-browser Time Lens displayed State B as `HISTORICAL` and `EXACT`, with repository, authority, Goal, Evidence, Progress, Memory, Notion, Brain, and Git all `EXACT`. Historical Ask returned HTTP `200`, `reconstruction_status=EXACT`, cited only State-A/State-B material, and reported `later_current_state_used=false`. Brain returned HTTP `200` with State-B source revision and `EXACT` availability.

The exact State-B Evidence file was removed from the host and container. The same Time Lens request then truthfully displayed `PARTIAL` with only the Evidence source `PARTIAL`; all other source classes stayed `EXACT`. The exact file was restored and hash-checked identically in host and container; the same request returned all source classes `EXACT` again.

The browser `Return to Now` control then selected the latest current repository boundary and displayed `CURRENT` with all source classes `EXACT`. The history service now derives that current boundary from the latest repository observation rather than incorrectly requiring a revision-shaped timestamp lookup.

## Runtime corrections

- The Core image now includes the Git executable required for retained bundle verification.
- Retained bundle verification now uses an isolated temporary bare Git verifier, which is valid for the Core container and remains bounded on verification failure.
- Return to Now now selects the latest repository observation boundary, preserving current Goal/Authority/Memory records that do not use Git SHA identifiers.

## Requirement disposition

- `R-050`: `VERIFIED` — populated historical browser fixture, exact State-B reconstruction, historical Ask/Brain cutoff, later-state exclusion, source-loss `PARTIAL` truthfulness, exact source restoration, and browser Return to Now passed.
- `R-043`: `partial` — local clean restore/interruption regression passed, but the complete fresh-install destructive-safety and interrupted-restore qualification remains incomplete.
- `R-045`: `partial` — local queue/quota/disk-pressure regression passed, but sustained duration, parser/index interaction, stale-job cleanup, retention, and bounded cost/usage qualification remain incomplete.
- `R-048`: `partial` — real A/B/C/D reconstruction and source-loss truthfulness passed, but the full independent source-class loss/recovery matrix and complete normative recovery walkthrough remain incomplete.
- `R-053`: `partial` — available browser keyboard, responsive, reduced-motion, text-state, and untrusted-text checks remain recorded; external assistive-technology evidence is unavailable.
- `R-044`: `partial` — approved Hindsight `retain` remains `UNAVAILABLE`; no promotion was made.
- `R-056`: `blocked_by_environment` / `OPEN` — complete clean-install integrated V1 release qualification remains outstanding.

## Governed result

The three governed views were reconciled mechanically after this continuation:

- `14 VERIFIED`.
- `11 partial`.
- `1 blocked_by_environment` (`R-056`).
- `0 failed`.
- `26` total requirements.

The thirteen previously verified rows were preserved: `R-037`, `R-038`, `R-039`, `R-040`, `R-041`, `R-042`, `R-046`, `R-047`, `R-049`, `R-051`, `R-052`, `R-054`, and `R-055`.

Governance validation, YAML parsing, diff checks, and tracked-secret checks passed before publication. The connected Notion page was fetched successfully and is writable; the Continuation 026 execution record is appended after the final GitHub SHA is known. GitHub publication and local/origin parity are required. Phase 15/V1 remains `FAIL`; deployment remains `NOT PERFORMED`.
