# Continuation 029 — V1 Product Completion Wave 1

## Scope and boundary

Continuation 029 completed the authorized first product-understandability wave. The frozen baseline remains `PRIME-SPEC-V1.0.0`; no v1.0.1, SpecChangeRecord, Phase 16, deployment, or R-056 closure was created. The work covered the project handoff slice, interpreter-portable qualification, a durable disposable fixture, and an architecture-aware audit of the §26 inventory.

## Harness portability

The qualification harness no longer invokes a literal `python3` executable. `tests/phase0/test_harness.py`, `scripts/phase15_qualify.py`, and `scripts/test_validate_governance.py` use the active interpreter identity. The phase-0 compile check now compiles source in memory, avoiding an SSHFS `__pycache__` write that fails with Windows `Access is denied` while still validating Python syntax.

Evidence:

- `tests/phase0/test_harness.py`
- `scripts/phase15_qualify.py`
- `scripts/test_validate_governance.py`

## Durable disposable fixture

`scripts/seed_product_completion_029.py` creates two real Git repositories and binds them through production Core services. The fixture contains approved goal content and GoalItems, progress history, authority revisions, Git checkpoint/repository state, activity including a prior failure and environment quirk, memory classes, Evidence, degraded Notion metadata, AI provenance, a blocked work condition, and a Project A/B private marker used only for isolation testing. Fixture credentials are ephemeral and are not recorded here.

The fresh browser qualification observed Project A with `BLOCKED · ACTIVE · ONLINE · CURRENT`, approved goal revision 1, current progress 68%, repository canonical revision `735a6cf6096e0f7a9441c0a9aedb68790b3076e3`, valid `.agent/CURRENT.md`, three memory records, one current evidence record, and degraded Notion status.

## Product operator slice

The production-backed operator path now exposes and qualifies:

- project overview, goal, progress, integrity, work condition, and activity;
- repository state, bounded tree, bounded text-file reads, canonical revision, branches, and worktrees;
- authority health, contract version, latest/history, hashes, and read-only authority files;
- grouped project-scoped Search across Repository, Authority, Git, Notion Knowledge, Activity, Progress, Memory, and Evidence;
- bounded Markdown and JSON context export with `prime.project-context.v1` schema, attachment disposition, no-store caching, freshness markers, and explicit redaction markers;
- Project A/B isolation, including a negative A query for B's private marker and a positive B query returning only B's private activity.

Browser evidence used the required gstack `/browse` runner. After clearing the console and reloading the authenticated project path, browser console errors were empty. Direct browser fetches returned HTTP 200 for both exports and the project-scoped search routes. Project A JSON export contained no Project B identifier or private marker; export size was 17,456 bytes. Markdown content type was `text/markdown; charset=utf-8`; JSON content type was `application/json`.

## §26 audit semantics

The audit now distinguishes user-facing criteria from architectural/security invariants. Seven architecture-only rows were promoted to `PRODUCT_VERIFIED` with frozen rationales and evidence, while the release gate still requires every §26 item to be `USER_USABLE_VERIFIED` or `PRODUCT_VERIFIED` and still fails truthfully:

- DOD-003 PostgreSQL/Core and separately owned memory persistence
- DOD-010 no vendor/product telemetry by default
- DOD-025 stable GoalModel structure
- DOD-029 versioned AuthorityFileContract semantics
- DOD-046 model-egress privacy enforcement
- DOD-072 MCP project isolation
- DOD-078 backup/restore coverage of canonical PRIME and durable memory

Final §26 counts are: `USER_USABLE_VERIFIED=3`, `PRODUCT_VERIFIED=7`, `IMPLEMENTED_NOT_PRODUCT_QUALIFIED=5`, `BACKEND_ONLY=37`, `UI_SHELL_ONLY=15`, `PARTIAL=10`, `MISSING=3`, and `BLOCKED_BY_ENVIRONMENT=1`. The gate remains `FAIL`; this is not a release claim.

## Remediation state and unresolved boundaries

The fresh qualification database produced `16 VERIFIED / 9 partial / 1 blocked_by_environment / 0 failed` for R-031 through R-056, with R-056 still OPEN. R-044 remains partial because approved Hindsight retain is unavailable. R-053 remains partial because external assistive technology is unavailable. R-031–R-036 retain native/Tailscale qualification gaps. Remaining product gaps, including onboarding/setup resume, interactive historical selection, deeper alignment/milestones, and complete release surfaces, remain visible and were not papered over.

## Validation ledger

- phase-0 harness: **PASSED** (`62 passed, 25 skipped`)
- focused phase 14/15 regression excluding duplicated phase-0 selection: **PASSED** (`122 passed, 50 skipped, 2 deselected`)
- fresh full regression and Phases 1–14: **PASSED** (`86 passed, 1 skipped`; all phase gates passed)
- adopted governance: **PASSED**
- product alignment structural validation: **PASSED**; V1 product gate **FAILED truthfully**
- browser project path, repository, authority, search, export, A/B isolation, console: **PASSED**
- YAML/AST/diff/secret checks: **PASSED**
- deployment: **NOT PERFORMED**

Publication: implementation/evidence/governance commit `23b504a5a322f3fd98da021dfd35b03c84adf593` is published to GitHub `main`; local/origin parity matched.

The Python `distutils-precedence.pth` warning from the host installation is environmental and did not change any qualification result. The SSHFS session-directory limitation for gstack was handled by using a local writable browser-session working directory; the repository remained the native Atlas checkout.
