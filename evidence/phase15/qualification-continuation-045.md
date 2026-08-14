# ANIMUS PRIME — Continuation 045 Evidence

Date: 2026-08-13
Baseline: PRIME-SPEC-V1.0.0
Execution: direct SSH/native Atlas only
Checkout: /home/sketch/Projects/ANIMUS_PRIME
Disposable resources: none
Deployment: NOT PERFORMED

## Frozen §26 reconciliation

| DOD | Exact frozen requirement | 044 evidence already earned | True remaining gap |
|---|---|---|---|
| DOD-026 | Progress history, Goal Alignment, milestones, and correction/challenge workflows are visible and evidence-backed. | 044 renders Progress history and Challenge controls, and the Progress service stores append-only correction/reassessment structures. | Goal Alignment, milestones, and a truthful complete operator correction/challenge qualification remain jointly open. |
| DOD-030 | Consequential authority events automatically enter the correct Hindsight bank with provenance and deduplication. | 044 persistent Atlas evidence shows record-complete post-baseline admission, multiple same-cycle records, exact source-reference reuse, source revision/hash, branch/worktree metadata, project-bound bank/event metadata, repeat dedupe, revision supersession, and secret rejection. | NONE for the frozen criterion. No dedicated operator Memory Admission screen is required. |
| DOD-062 | Each project has an evidence-backed progress percentage, confidence, and explanation. | 042–044 real project assessments and browser Progress surface expose percentage, confidence, explanation/history, GoalItems, evidence references, approved GoalModel identity, and repository revision. | NONE for the frozen criterion. Correction/challenge is governed by DOD-026. |
| DOD-063 | Progress automatically becomes stale after relevant changes and refreshes appropriately. | 044 real authenticated browser evidence showed STALE, visible Refresh, HTTP 200 production refresh, current canonical revision, CURRENT assessment, retained prior history, and stale-overwrite protection. | NONE for the frozen criterion. Tailscale and a second device are not part of DOD-063. |

## Governance schema repair

Initial 'python3 scripts/validate_governance.py --mode ADOPTED' errors were classified as follows:

- CURRENT_RECORD_INVALID: .agent/CURRENT.md had stale Continuation 042 state, duplicate historical sections, and COMPLETE without the required awaiting-reset wording. It was updated as mutable current state.
- HISTORICAL_VALID_LEGACY_SCHEMA: D-042 compact directive, date-only D-043/D-044 directive timestamps, legacy O-042/O-043/O-044 outcome shapes, the dated R-042 record heading, DEC-043/DEC-044 short records, and the dated L-042/L-043 learning headings.
- HISTORICAL_ACTUALLY_MALFORMED: NONE identified after comparing each reported error with its known historical shape.
- VALIDATOR_FALSE_POSITIVE: NONE after the bounded legacy handlers were added.
- TEMPLATE_SCHEMA_DRIFT: The project checkout is adopted, not a clean template. The reusable clean package at authority-template/v1 is the template validation target.

The validator now carries CURRENT_SCHEMA_VERSION = '2' plus bounded historical signatures and required-field validation. It does not accept arbitrary old content. New Continuation 045 records use the current schema. No historical append-only text was rewritten. Historical ledger hashes were captured before repair and were unchanged after the validator/current-state work.

Validation:

- python3 authority-template/v1/scripts/validate_governance.py --mode TEMPLATE: PASSED.
- python3 scripts/validate_governance.py --mode ADOPTED: PASSED.
- Synthetic malformed legacy record and unknown-shape checks: PASSED, malformed structures rejected.

## Architecture review

DOD-002, DOD-005, DOD-006, DOD-009, DOD-018, DOD-033, DOD-037, DOD-038, and DOD-061 were reviewed against the frozen clauses and existing evidence. No row was promoted without a complete positive/negative direct proof package. Their residuals remain bounded and no unrelated Tailscale/second-device requirement was imported into Progress rows.

DOD-016 remains blocked by the live distinct child Notion record and independently usable child Hindsight boundary. DOD-021 remains EXTERNAL_ENVIRONMENT for the approved model execution environment. DOD-022 remains EXTERNAL_ENVIRONMENT for the live Notion knowledge source in PRIME Core. DOD-068 remains blocked by the approved Hindsight Reflect/Mental Models provider-runtime path; unsupported Mental Models are not treated as satisfying the requirement.

## Persistent validation

Persistent PostgreSQL and Hindsight were reused. No new project, database, container, repository, worktree, Hindsight bank, browser profile, or fixture was created. R-045 sustained pressure was withheld and R-056 remains open.

The final validation and publication record is appended to .agent/CURRENT.md, .agent/OUTCOMES.md, .agent/RECORD.md, and .agent/LEARNINGS.md.

## Validation results and storage

Storage precheck: root available 29,586,534,400 bytes (88% used); /mnt/storage1tb available 149 GiB before focused work. Final check after validators and regression: root available 29,576,478,144 bytes (88% used); /mnt/storage1tb available 159,130,316,800 bytes (84% used). No DiskFull or unexpected workload growth occurred.

Persistent services: PostgreSQL container healthy; Hindsight direct /health returned status healthy and database connected. No Core listener was present at the time of this reconciliation, so no new browser process or temporary Core was started. The real browser STALE-to-CURRENT evidence from Continuation 044 was rechecked against the current implementation and retained as the evidence basis; a fresh browser reopen in 045 was NOT RUN because the persistent-only execution constraint forbids starting a disposable/temporary Core.

Regression:
- tests scripts: PASSED, 104 passed, 3 explicit FRESH_STATE_REQUIRED skips, 0 failures.
- full pytest: PASSED, 104 passed, 3 explicit FRESH_STATE_REQUIRED skips, 0 failures.
- pytest collect-only: PASSED, 107 tests collected.
- compileall: PASSED.
- git diff --check: PASSED.
