# ANIMUS PRIME — Continuation 048 Evidence

Baseline: PRIME-SPEC-V1.0.0
Authoritative execution: direct SSH / native Atlas only
Checkout: /home/sketch/Projects/ANIMUS_PRIME
Starting published main: 004b926e0cf51c521cea1fba8b03734aa024f640
Disposable resources: NONE
Temporary Core: NO
Persistent Core listener: NO
Browser: NO
Deployment: NOT PERFORMED
Phase 16: NOT ENTERED
R-045 pressure: NOT ATTEMPTED
R-056: OPEN

## Storage and services

- Start root free space: 31455404032 bytes.
- After full regression: 29378330624 bytes.
- Secondary /mnt/storage1tb: 159130316800 bytes and stable.
- PostgreSQL: PASSED through the existing approved persistent service at 172.24.0.2:5432/prime.
- Hindsight: PASSED; persistent health returned healthy with database connected.
- DiskFull: NONE; no abnormal growth or cleanup was performed.
- No ANIMUS Core listener was started.

## Regression guards

- DOD-061: PASSED. Focused suite 8 passed; the real persistent method rejected stale caller revision, processed changed paths only, preserved dirty-worktree semantics, advanced canonical revision on committed observation, and returned NOOP on repeat. The persistent project advanced to 004b926e0cf51c521cea1fba8b03734aa024f640 using only the Continuation 047 evidence path.
- DOD-030: PASSED / preserved. Focused authority-admission regression remained green; Continuation 047 persistent admission and repeat-dedupe evidence remains authoritative.
- DOD-063: PASSED / preserved. The incremental committed observation path leaves prior Progress assessments STALE; Continuation 047 evidence remains authoritative.

## DOD-033 — correction provenance: PRODUCT_VERIFIED

Existing verified memory evidence was reused for correction, supersession, tombstone, source-reference preservation, and historical retrieval. On the persistent Atlas project, assessment assessment_6cd2e4b19b9e487ba149a3a1a62943ac remained byte/row-equivalent after correction progress-correction_d17dc6c3094542a3b0b2fd22fe75e600. The correction durably recorded project, assessment, category WRONG_STATUS, reason, operator identity, valid project-bound source reference, created time, and an immutable historical PROGRESS_CORRECTION snapshot.
Reassessment assessment_745c0dca3f2a487cb9a6a1b31393f4e3 was a new row with a new historical PROGRESS snapshot and did not mutate the original assessment. Unknown assessment, cross-project assessment, empty reason, unsupported category, and invalid source-reference cases were rejected. The implementation now validates correction source references against the project ledger.

## DOD-007 — Node enrollment/security: PRODUCT_VERIFIED

Direct in-process qualification against the real Atlas project root passed short-lived single-use bootstrap, rotation invalidating the prior token, replacement-token authentication, revocation, re-enrollment with a new Node identity, allowed-root normal access, outside-root rejection, traversal rejection, and symlink escape rejection. Node security events are durably represented in the Node state audit ledger (ENROLLED, ROTATED, REVOKED, REENROLLED) without recording credentials. Existing TLS/mTLS fail-closed and protocol/identity checks remain preserved. Native service-host, reboot, reconnect, and Windows-specific qualification remains an R-031 boundary and is not claimed here.

## DOD-018 — repository boundary: PRODUCT_VERIFIED

Against the persistent project, inspecting /home/sketch/Projects/ANIMUS_PRIME/src resolved the same primary Git top-level and the same .git common directory as the project root, with one primary project binding and no duplicate identity. The path-identity defect was corrected in both Core onboarding and Node inspection: Git relative --git-common-dir is resolved against the inspected candidate, not incorrectly against the reported top-level. Non-bare enforcement and duplicate identity refusal remain covered by existing direct tests. Nested independent Git metadata remains a distinct repository boundary; no nested repository was created.
## Remaining prioritized rows

- DOD-045: PARTIAL. Persistent login, wrong-credential rejection, missing/expired/revoked session rejection, digest-only token storage, CSRF, origin, management gating, logout, and restore step-up rejection passed. Recovery credential rotation could not be replayed because the one-time credential is unavailable and no fresh/disposable operator store may be created; no promotion.
- DOD-028: PARTIAL. Current valid authority detection, explicit REVIEW, explicit ADOPT, no rewrite, bootstrap overwrite refusal, and repeated same-hash ADOPT idempotency passed. Historical/old authority migration and malformed/conflict review evidence are not present; no promotion.
- DOD-037: PARTIAL. Current main/HEAD/canonical binding, one worktree, dirty-state truthfulness, and preserved untracked state were inspected. Promotion is withheld because the committed observation path lacks an explicit canonical-ref/experimental-branch acceptance gate.
- DOD-006: NOT RUN for promotion. Current listener evidence is not fresh for a running PRIME Core/Node topology, and no Core was started.
- DOD-038, DOD-039, DOD-004: NOT ADDRESSED by directive order. DOD-005 and DOD-009: CONSERVATIVE.

## Validation

Focused regression: PASSED (8 passed).
Compileall: PASSED.
Governance/YAML/product audit/burndown/diff/secret/full regression checks: recorded at closeout.
Core/browser: NOT RUN; no approved persistent Core listener.
Deployment: NOT PERFORMED.

Implementation commit A: e8805f8948d47dcccf45ab31ec32fe797a6b2768.
Evidence/governance publication is the single follow-on commit; no SHA-chasing commit is created.

## Closeout validation

- Persistent full regression: PASSED (109 passed, 3 explicit FRESH_STATE_REQUIRED skips; 112 collected).
- Focused post-fix Node/repository/provenance regression: PASSED (13 passed).
- Compileall: PASSED.
- YAML parsing: PASSED (5 governed YAML documents).
- Product burndown structural validation: PASSED; audit_total=81; complete=38; burndown=43; status counts PRODUCT_VERIFIED=24, USER_USABLE_VERIFIED=14, IMPLEMENTED_NOT_PRODUCT_QUALIFIED=11, BACKEND_ONLY=18, UI_SHELL_ONLY=9, PARTIAL=4, BLOCKED_BY_ENVIRONMENT=1, MISSING=0.
- Product alignment audit: PASS; release alignment remains FAIL because the governed product completion gate is intentionally not closed.
- Adopted governance validation: PASSED. Template governance validation: PASSED.
- Diff and tracked-secret checks: PASSED.
- Persistent PostgreSQL/Hindsight health: PASSED.
- Storage after full validation: root free 29378330624 bytes; /mnt/storage1tb free 159130316800 bytes; DiskFull NONE.

Implementation commit A: e8805f8948d47dcccf45ab31ec32fe797a6b2768. Evidence/governance publication remains the single follow-on commit; no SHA-chasing commit is created.
