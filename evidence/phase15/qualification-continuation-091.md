# ANIMUS PRIME Phase 15 Qualification Continuation 091

Acceptance: **PASS / COMPLETE for the bounded DOD-004 scope**  
Phase 15: **PARTIAL**

## Baseline and implementation

- Frozen specification: `PRIME-SPEC-V1.0.0`.
- Starting governed/public baseline: `eb39fb51ed45e5b70c8bd0f7612e0e881cfb3c98`.
- Primary durable-workflow implementation: `d00830ec8dde5debec2c7391a28fe3e3d2b09b51`.
- Live restart defect repair and final qualified implementation: `f3772ee560651d998e31ff46bf373983894f0e94`.
- Worktree before work contained only preserved user-owned untracked `.codebase-memory/`, `.prime-evidence/`, and `.vscode/`.

## Result

DOD-004 is `PRODUCT_VERIFIED`. R-012 Phase 15 validation is `VERIFIED`.

PRIME now applies the existing durable workflow primitives to every current V1 path that actually crosses a non-transactional side-effect boundary: Fork/Clone, live Notion Project Record creation, Hindsight bank creation, Node repository creation, authority/Goal provisioning, MCP scope issuance, and restore. Each converted path has a stable workflow identity, ordered durable steps, explicit replay policy, expected/created resource records, and a truthful reconciliation path.

Current archive/remove/delete/purge operations are canonical PostgreSQL state/audit/event transitions and deliberately preserve external repositories/resources. Rebind performs read-only external inspection before an atomic canonical switch. These were not wrapped in artificial external workflows.

## Product defect found and repaired

The live process-death run exposed a narrow restart defect in `execute_product_ai`: persisted Notion configuration state was treated as proof that a Project Record page already existed. After a crash between page creation and durable checkpoint, retry skipped `create_project_record`, leaving the workflow RUNNING.

The repair checks the actual persisted `page_id`. If it is absent, the route re-enters the durable creation path. The live retry then found the exact PRIME idempotency marker in Notion, adopted the one existing page, checkpointed `PAGE_CREATED`, bound it, and completed the workflow.

## Runtime qualification

- Canonical Core image: `animus-prime-core:continuation-091-f3772ee`.
- Build commit: `f3772ee560651d998e31ff46bf373983894f0e94`.
- Build timestamp: `2026-08-18T18:38:00Z`.
- Persistent Core service remained private on `127.0.0.1:8000` under the established user service and UID `1000:1000`.
- Prior canonical image/container state was retained as recoverable rollback state; secrets and owner-only credential references were not printed or permission-weakened.
- Browser authentication used PRIME's trusted-host challenge. CSRF refusal was observed before the valid protected request; no security control was disabled.
- Live Notion crash/restart/reconciliation and exact one-marker page evidence are recorded in the interruption matrix.
- Real persistent Hindsight was exercised by the Fork qualification; stable bank creation/replay remained idempotent.
- Restore qualified a real encrypted continuity bundle from Appliance A into the approved independent Appliance B restore target. Resume returned the same restore/workflow identity and did not replay canonical replacement.

## Validation

- Focused static/default 091 suite: `3 passed / 5 skipped` — PASSED.
- Focused persistent integration before the final route-only fix: `8 passed` — PASSED.
- Final supported regression using repository `.venv`: `137 passed / 34 skipped / 0 failed` — PASSED.
- The skip delta from the previous `134 / 29` baseline is five explicit persistent-DB tests plus three new default tests; skips are environment-gated, not claimed as passes.
- A host integration rerun first used an invalid guessed Appliance-A password and failed authentication before test execution. This is recorded as an invalid invocation, not a product regression; no credential was exposed or changed.
- Live canonical Notion process death/restart: PASSED.
- Exact Notion marker count: `1` — PASSED.
- Persistent Core health/build provenance after repair: PASSED.
- No public exposure, Funnel change, deployment, Phase 16, history rewrite, canonical project mutation, synthetic bank, or duplicate product stack was performed.

## Governed result

- Queue changes from `72 complete / 9 open` to `73 complete / 8 open`.
- Work classes change from `1 LOCAL_CODE / 3 LOCAL_BROWSER_QUALIFICATION / 5 EXTERNAL_ENVIRONMENT` to `0 / 3 / 5`.
- DOD-004: `BACKEND_ONLY` -> `PRODUCT_VERIFIED`.
- R-012: Phase 15 `VERIFIED`.
- DOD-016 is not promoted automatically; its complete child-resource/operator contract remains governed separately.
- DOD-081, R-056, Phase 15, V1, and deployment remain open or gated.
