# Phase 15 Remediation Continuation 012 — R-051–R-053 and Notion credential reuse

- Baseline: `PRIME-SPEC-V1.0.0`
- Directive: `D-PRIME-PHASE15-REMEDIATION-012`
- Date: 2026-08-11
- Scope: local implementation boundary only; live qualification is separate.

## Credential reuse boundary

The runtime environment inspected for this run did not contain `NOTION_READONLY_KEY`, and no local MyAssistant configuration file referencing that variable was found. The variable value was never printed, copied, logged, persisted, or included in this record. The implementation adds an idempotent `NotionCredentialRegistry` that stores only `env/myassistant/notion-readonly`, the source variable name, migration state, and capability metadata. A deliberate alternate PRIME reference is never overwritten.

`NotionApiClient.capability_test` now performs actual `/users/me`, granted-page, and block-child reads. Write probing is explicit and requires a controlled parent; the client no longer claims write capability from identity alone. The Core routes expose import, status, and capability-test results without returning token material. The approved granted-page identity remains `3b3833cb-27ff-8039-bf9e-f4f731df0633`.

The connected assistant Notion workspace was re-read for source/handoff context, but that connector authorization is not PRIME production-adapter evidence. No live PRIME credential import, page read, write probe, Project Record lifecycle, or Notion qualification was run.

## R-051–R-053 local implementation

- R-051: complete local operator shell, first-run bootstrap/login, project creation, global navigation, `/v1/operator/state`, and explicit authenticated/degraded state loading.
- R-052: required project surfaces, project selection, project-scoped Ask/Search calls, accessible Project Brain list alternative, protected lifecycle confirmation, and real backend-state summaries.
- R-053: responsive desktop/mobile layout, keyboard/focus behavior, reduced-motion support, visible textual status vocabulary (`LOADING`, `EMPTY`, `HEALTHY`, `STALE`, `DEGRADED`, `OFFLINE`, `ERROR`, `NEEDS_ATTENTION`), safe untrusted project-name rendering, no-store behavior, and no-terminal setup path.

## Validation and qualification truth

- Implementation commit: `3fd09a10aad5b2fff4856b6e75fac5e893e08b3b`.
- Focused credential/Notion/API/web tests: PASSED (`17 passed, 1 skipped`).
- Full local suite: PASSED (`48 passed, 17 skipped`).
- Governance validator: PASSED (`scripts/validate_governance.py --mode ADOPTED`).
- Compileall: PASSED.
- Diff check: PASSED.
- Supported-browser desktop/mobile, keyboard-only, assistive-technology, and fresh setup walkthrough: NOT RUN.
- Live PRIME Notion credential discovery/import and capability test: BLOCKED (`NOTION_READONLY_KEY` absent from this runtime).
- R-051–R-053 qualification: `blocked_by_environment`; implementation is `IMPLEMENTED`.
- Evidence/governance commit: `e2f50703e88689a035b686d4eed89234fb2f1c8d`.
- V1 qualification: remains `FAIL`; deployment: `NOT PERFORMED`.
