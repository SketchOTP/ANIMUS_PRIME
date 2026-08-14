# ANIMUS PRIME — Phase 15 Qualification Continuation 057

Status: **PARTIAL — Restoration-bounded local product qualification**  
Date: 2026-08-14

## Baseline and execution boundary

- Specification: `PRIME-SPEC-V1.0.0`.
- Starting governed HEAD: `066bec5fb8041734cf28314090344bd7bb777f14`.
- Execution: direct native SSH on Atlas at `/home/sketch/Projects/ANIMUS_PRIME`; the `Z:`/SSHFS representation was not used for execution.
- Worktree: only preserved untracked `.codebase-memory/`, `.prime-evidence/`, and `.vscode/` were present; no unrelated tracked state was overwritten.
- Persistent PostgreSQL, Hindsight, PRIME Core/UI, and canonical Node were preserved. No replacement database, Hindsight bank, project, repository, Node, worktree, or browser profile was created.
- Local regression floor: `94 passed / 28 skipped`.

## Qualification-ledger provenance correction

The ledger previously paired Continuation 056 evidence with the corrected Continuation 055 implementation SHA. The semantics are now explicit without rewriting history:

- Continuation 055 qualified implementation: `0a3c82f0c606fb80f914eb59116dd5f46b9d5ec5` (`feat-persistent-node-trust-lifecycle`).
- Continuation 056 governed qualification: `066bec5fb8041734cf28314090344bd7bb777f14`.
- `latest_qualification_evidence` now points to this Continuation 057 record and `latest_qualification_commit` remains the governed 056 qualification baseline because this continuation made no product implementation change.

## Persistent runtime preflight

- `animus-prime-core.service`: active and enabled user systemd service; private Core listener `127.0.0.1:18000`; `/health/live` and `/health/ready` returned healthy responses.
- `animus-prime-node.service`: active and enabled user systemd service; canonical Node `node-041-atlas-native`; private listener `127.0.0.1:18001`.
- Existing PostgreSQL container: `animus-prime-phase0-postgres-1`, healthy and preserved.
- Existing Hindsight container: `mimir-hindsight-production`, preserved.
- Public exposure: none; no Funnel or unrelated service was changed.

## Real Qualification Project preflight

The persistent database was inspected read-only to identify the real project, not test residue:

- Project: `project_d9a1a5b609394282b62fc12c0d04634d`, `Qualification Project`.
- Repository binding: `/home/sketch/Projects/ANIMUS_PRIME`.
- Node binding: `node-041-atlas-native`, state `ONLINE`.
- Current source references: authority records such as `.agent/RECORD.md`, `.agent/LEARNINGS.md`, `.agent/OUTCOMES.md`, and `.agent/DIRECTIVES.md`, with current source state and linked Memory records.
- No current `evidence_records` exist for this project, and no current Documentation projection candidate exists for this project.
- The persistent database also contains historical regression-created project rows with `/tmp/pytest-*` and `/srv/repo` paths. Those rows were not used as qualification targets and were not changed.

## DOD-005

Result: **BACKEND_ONLY — hard stop under the directive's restoration rule**.

The real project has current authority sources and linked Memory, but no existing non-authority evidence source that simultaneously participates in the required derived views and has a supported retraction plus proven restoration/re-index path. The supported retraction API is evidence-oriented, while the real project has no evidence record or Documentation projection candidate to exercise. There is therefore no safe reversible candidate.

No retraction, direct SQL mutation, synthetic source, replacement project, negative mutation test, or restoration attempt was run. This preserves the canonical project and avoids manufacturing evidence. The exact remaining clause is to qualify the complete positive retraction, historical provenance preservation, negative/fail-closed cases, and restoration path against a naturally available supported source.

## Local browser qualification

The actual Core-served UI was reached through the private Windows SSH tunnel at `http://127.0.0.1:28000/` using the gstack `/browse` skill. The protected entry surface, recovery controls, sign-in control, project navigation, and critical surface links rendered. The stale browser session cookie did not authenticate against the current Core, and the current operator password was not available through the approved run context. No password reset or credential rotation was performed merely to manufacture an authenticated run.

Consequently, DOD-024, DOD-026, DOD-027, DOD-047, DOD-048, DOD-049, DOD-054, DOD-055, DOD-056, DOD-057, DOD-058, DOD-076, DOD-077, DOD-080, and DOD-081 were not promoted. Protected-entry behavior is observed; authenticated operator clauses remain open.

## Newly verified and preserved

- Newly USER_USABLE_VERIFIED: none.
- Newly PRODUCT_VERIFIED: none.
- Preserved: DOD-008 `USER_USABLE_VERIFIED`; DOD-009 `PRODUCT_VERIFIED`; persistent Core/Node topology; prior qualified rows and exact external blockers.

## Validation

- Runtime health and listener identity: **PASSED**.
- DOD-005 read-only preflight: **PASSED**; safe-candidate hard stop recorded.
- Browser protected-entry snapshot: **PASSED**; authenticated browser wave: **BLOCKED** by unavailable current operator credential; no password mutation performed.
- Focused regression: **NOT RUN**; no implementation change was made in this bounded phase at time of closeout.
- Full regression: **NOT RUN**; no implementation change was made in this bounded phase at time of closeout.
- Governance: **PASSED** — adopted governance validation.
- Burndown: **PASSED** — 81 audit items, 46 complete, 35 burndown; local totals remain 5 code / 15 browser / 15 external.
- Product alignment audit: **PASSED**; broader V1 gate remains intentionally FAIL while open.
- Compile/static and diff checks: **PASSED**.
- Secret scan: **PASSED** — no secret values were recorded.
- Deployment/public exposure: **NOT PERFORMED**.

## Remaining state

- Local queue: 5 `LOCAL_CODE`, 15 `LOCAL_BROWSER_QUALIFICATION`.
- External queue: 15 `EXTERNAL_ENVIRONMENT`.
- R-056: `OPEN`.
- Phase 15: incomplete.
- V1: not declared.
- Deployment: `NOT PERFORMED`.
