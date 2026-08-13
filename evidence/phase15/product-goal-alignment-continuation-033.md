# ANIMUS PRIME — Continuation 033 Product Closure Evidence

## Scope and authority

- Directive: `D-PRIME-PHASE15-PRODUCT-COMPLETION-033`
- External continuation: `Continuation 033`
- Frozen baseline: `PRIME-SPEC-V1.0.0`
- Qualification authority: native Atlas checkout `/home/sketch/Projects/ANIMUS_PRIME`
- Windows SSHFS path was not used for Docker, repository binds, or qualification. The earlier ENOENT came from combining the SSHFS UNC root with an already-prefixed `Z:\` path. Atlas-native SSH and bind mounts avoid that malformed path class.
- No specification change, Phase 16, deployment, R-056 closure, or fabricated external evidence was performed.

## Mandatory regression gate

Fresh qualification used a disposable Compose project and PostgreSQL/pgvector database on Atlas. All 26 migrations applied from zero. Full repository regression passed:

```text
90 passed, 1 skipped
```

Phases 1 through 14 all passed, including migration/idempotence/schema, node migration, onboarding, indexing/source freshness, memory, MCP, Notion, progress, activity, Brain, Evidence/Time Lens/Fork, lifecycle, reliability, and accessible responsive shell checks.

The normal Core image startup path reported a permission-degraded dependency because the existing uncommitted migration files `migrations/prime/0025_product_onboarding.sql` and `migrations/prime/0026_product_completion_wave3.sql` are mode `660` while `Dockerfile.core` runs as `nobody`. This is a native worktree file-mode condition, not a migration or SQL failure. The files were not chmodded, overwritten, or otherwise changed for this qualification. The fresh migration and qualification process ran as root inside the disposable container so the project’s existing user changes remained intact.

Additional gates:

- `python scripts/validate_governance.py --mode ADOPTED` — PASSED.
- `python scripts/validate_product_alignment.py` — PASSED structurally; the V1 product gate remains `FAIL` as required.
- Native Python `compileall` for `apps`, `src`, `scripts`, and `tests` — PASSED.
- Web JavaScript extraction/parse check — PASSED.
- `git diff --check` — PASSED.
- Precise tracked secret scan excluding evidence fixtures — PASSED.
- Mechanical YAML reconciliation of the audit, gap burndown, traceability, remediation matrix, and qualification ledger — PASSED; no requirement promotion was justified by this cycle.

## Demonstrated local repairs and product work

The following bounded changes were made only after the regression gate:

1. Git checkpoint bundle verification now uses a disposable bare repository context, matching the existing bundle-status verification path. This removes the false `need a repository to verify a bundle` failure without changing repository ownership or mutation policy.
2. Approved GoalModel progress now uses approved item weights and refuses a non-zero required item whose acceptance contract requires evidence when no evidence reference is supplied. A focused regression proves refusal, valid evidence admission, weighted 80% assessment, and retained evidence identity.
3. Core event ingestion accepts and persists optional `project_id`, `source_revision`, and `source_ref` provenance.
4. The Wave-3 Brain surface now has a real deterministic source-grounded canvas, orbit/pan/zoom/reset controls, selection, source filtering/search, keyboard controls, source details, repository-view action, and accessible node-list fallback.
5. Activity now exposes source revision/artifact provenance and truthfully labels source-free events `NO SOURCE ARTIFACT`; source-backed events provide an artifact action.
6. AI Connections now exposes project-scoped connection metadata and rotate/revoke/reissue controls while keeping one-time secrets outside the DOM.
7. `docs/v1-product-gap-burndown.yaml` provides the derived 70-item non-complete §26 view and points back to the authoritative audit for normative missing behavior.

Focused Progress evidence passed (`1 passed`) and the browser Brain check passed at fixture scale: canvas present, one source-grounded node rendered, accessible node list present, node selection/details worked, repository source action was available, orbit/pan/zoom/reset controls responded, source filtering worked, and the final browser console-error check was clean.

The Brain result remains `IMPLEMENTED_NOT_PRODUCT_QUALIFIED`: representative-scale performance, live-update advancement, and complete project-isolation qualification were not demonstrated. AI Connections, Activity drill-down, and the other remaining product workflows likewise remain unpromoted until their complete frozen acceptance paths are directly qualified.

## Reconciled release state

The §26 audit remains:

```text
4 USER_USABLE_VERIFIED
7 PRODUCT_VERIFIED
22 IMPLEMENTED_NOT_PRODUCT_QUALIFIED
31 BACKEND_ONLY
9 UI_SHELL_ONLY
7 PARTIAL
0 MISSING
1 BLOCKED_BY_ENVIRONMENT
```

The governed remediation state remains:

```text
16 VERIFIED / 9 partial / R-056 blocked-open / 0 failed
```

R-044 Hindsight, R-053 external assistive technology, R-031–R-034 native Node lifecycle, R-035–R-036 Tailscale/second-device qualification, and R-056 remain explicitly open or environment-bound. V1 and Phase 15 remain `FAIL`. Deployment is `NOT PERFORMED`.

## Publication note

This evidence file, the append-only `.agent` records, the bounded code repairs, the audit update, and the derived gap burndown are published together with the Continuation 033 closure commit. Exact final local/origin parity is recorded after publication in `.agent/OUTCOMES.md` and `.agent/CURRENT.md`.
