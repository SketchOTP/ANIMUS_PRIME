# ANIMUS PRIME Phase 15 Qualification Continuation 065

## Result

PARTIAL / DONE_WITH_CONCERNS for the bounded local V1 convergence scope. The genuine persistent Atlas product qualified the requested security-negative, onboarding-refusal, authority/Goal-protection, Progress-negative, backup-preflight, and narrow-screen checks. One minimal product repair was required for approved Goal protection. No full requirement was promoted because positive/destructive or legitimate-target clauses remain open.

## Baseline and execution boundary

- Spec: PRIME-SPEC-V1.0.0
- Authoritative checkout: /home/sketch/Projects/ANIMUS_PRIME
- Starting governed baseline: 90b9edbe37702a5a03a1d8098d8e66d72618e6ba
- Qualified implementation candidate: 43fcba400819a1f03c642a4e2ac43c62cc4bb5ad
- Final governed publication SHA: recorded after final publication parity
- Execution: direct SSH/native Atlas only; no Z: execution
- Preserved untracked directories: .codebase-memory/, .prime-evidence/, .vscode/
- Canonical Qualification Project: project_d9a1a5b609394282b62fc12c0d04634d
- Canonical repository binding: repo_1eb92bbce8d44309861368d8690247c6, /home/sketch/Projects/ANIMUS_PRIME
- Canonical project before and after bounded probes: ACTIVE / ONLINE / CURRENT / NORMAL
- Canonical Goal identity before and after: goal_a6fb1f34a58e4048951cf690048c255f, content hash eddb2380abd4be86bc97ec0f6713ed2c8418825d23c7c697f3d130cb0732bd2a
- No project, repository, Node, backup destination, Goal revision, authority file, destructive lifecycle state, or synthetic target was created.

## Persistent Atlas runtime

| Component | Runtime mechanism | Identity / listener | Result |
|---|---|---|---|
| PostgreSQL | Existing persistent Docker service | animus-prime-phase0-postgres-1 | Reused; no reset |
| Hindsight | Existing persistent service | Existing approved Atlas Hindsight | Reused; service connectivity/retain/recall CURRENT; Reflect UNAVAILABLE; Mental Models UNSUPPORTED |
| Repository Node | Existing user service | node-041-atlas-native, private 127.0.0.1:18001 | Preserved healthy/enrolled |
| PRIME Core | systemd --user -> PRIME-owned Docker container | animus-prime-core:continuation-065, private 127.0.0.1:18000 | Active and ready |
| PRIME Web UI | Genuine Core-served UI | private 127.0.0.1:18000, reached through existing narrow SSH forward | Loaded and authenticated |
| Service manager | systemd --user | animus-prime-core.service, animus-prime-node.service | Active |
| Persistent state | Existing bind | /home/sketch/.local/share/animus-prime-core -> /var/lib/animus-prime-core | Preserved |
| Repository bind | Existing read-only bind | /home/sketch/Projects/ANIMUS_PRIME -> /home/sketch/Projects/ANIMUS_PRIME:ro | Preserved |
| Readiness | /health/ready | schema 0036_operator_workflows.sql | PASSED |
| Runtime provenance | image build metadata | commit 43fcba400819a1f03c642a4e2ac43c62cc4bb5ad | Exact candidate match |
| Rollback | stopped PRIME-owned container | animus-prime-core-rollback-065 | Recoverable, not deleted |

No public listener, Funnel change, deployment, or unrelated service change occurred.

## Browser and operator qualification

Browser: existing gstack browse Chromium installation with persistent state, using the genuine Core-served UI through the existing private SSH forward. No disposable browser profile or PRIME dependency was created.

### Lifecycle and destructive security-negative matrix

Using the canonical project and restoring it to its exact pre-probe lifecycle state:

- Missing CSRF header: HTTP 403 CSRF validation failed; no mutation.
- DELETE without recent step-up: preflight returned the exact DELETE target/consequence and requires_step_up=true, step_up_recent=false; no action executed.
- Wrong typed confirmation: HTTP 409 explicit confirmation is required; project remained ACTIVE.
- PAUSE then RESUME: reversible transition passed and returned the project to ACTIVE.
- Replayed single-use preflight: HTTP 409 lifecycle preflight has already been used; no mutation.
- Stale preflight after a real state transition: HTTP 409 lifecycle preflight is stale because project state changed; no mutation.
- Wrong project target: HTTP 409 lifecycle preflight is invalid; no mutation.
- Final canonical state: ACTIVE / ONLINE / CURRENT / NORMAL.
- Audit table contains lifecycle actions for PAUSE, RESUME, ENTER_COMPLETION_REVIEW, and CANCEL_COMPLETION_REVIEW. No canonical DELETE, ARCHIVE, REMOVE, PURGE, or completion request was executed.

### Registration and onboarding refusals

Inspection used existing enrolled Node node-041-atlas-native and did not bind anything.

- Canonical repository inspection: HTTP 200, REVIEW_AUTHORITY, authority CURRENT; no binding mutation.
- Traversal path: HTTP 400, repository path traversal is not allowed.
- Outside enrolled root: HTTP 400, path is outside the enrolled Node allowed roots.
- Nonexistent path: HTTP 400, repository path does not exist or is not a directory.
- Existing-repository registration with confirm=false: HTTP 400, operator confirmation is required before binding a repository.
- Canonical repository binding and project identity remained unchanged.

### Authority protection and idempotency

- Review returned VALID, contract authority-file-contract-v1, and no rewrite.
- First explicit ADOPT returned rewrite=NONE.
- Repeated ADOPT returned rewrite=NONE, adoption_status=ALREADY_ADOPTED.
- .agent file bytes were not rewritten. The append-only authority observation changed the latest authority revision metadata as designed.
- The adoption implementation advanced onboarding metadata as a side effect. 065 restored the exact pre-probe BASELINE / AWAITING_BASELINE values and verified them in the final snapshot. This remains a product concern for future qualification, not a hidden mutation.

### Goal protection and Progress negatives

After rebuilding the persistent Core with the 065 candidate:

- Attempting to approve replacement content without explicit new_revision=true returned HTTP 400 approved GoalRevision is protected; explicit new-revision intent is required.
- Missing draft approval returned HTTP 400 draft GoalRevision not found.
- Approved Goal revision ID/hash remained unchanged.
- Empty Progress correction reason was rejected at validation with HTTP 422.
- Unsupported correction category returned HTTP 400.
- Invalid source reference returned HTTP 400 source reference does not belong to project.
- No correction record was created by the negative probes.
- No false Progress correction was submitted.

### Backup and polish

- Restore preflight against a nonexistent destination returned HTTP 400 backup bundle does not exist; no backup destination was created and no restore ran.
- Authenticated reload after the persistent Core swap succeeded.
- At 375px viewport: scrollWidth=375, clientWidth=375, overflow=false.
- After clearing the browser console and reloading the authenticated UI: no console errors.
- Expected negative-probe HTTP 401/403/409/400/422 responses were observed in the earlier console/network history and are recorded as expected refusal traffic, not JavaScript failures.

## Minimal repair

Observed user-impacting failure: attempting to protect the existing approved Goal revision first ran the stricter content validator, producing an incomplete Goal error instead of the required protected-revision refusal because the governed Goal predates the validator.

Root cause: CoreService.create_goal_revision validated new content before checking whether an approved Goal existed and whether explicit new-revision intent was present.

Repair: moved the approved-revision protection check before content validation. No schema change or canonical Goal rewrite.

Test: tests/phase15/test_continuation_065_local_convergence.py asserts the protection branch wins without invoking legacy content validation.

Requalification: focused test passed; the live persistent Core returned the required protected-revision refusal and preserved Goal identity/hash.

## Validation

- Focused 065 test: PASSED, 1 passed.
- Full regression: PASSED, 108 passed / 28 skipped. The prior floor was 107 / 28; the one additional pass is the new 065 repair test. Skip count is unchanged.
- Compile/static: PASSED.
- git diff --check: PASSED.
- Governance validate_governance.py --mode ADOPTED: PASSED.
- Burndown validator: PASSED, audit total 81, complete 49, burndown 32; local queue remains 5 LOCAL_CODE / 12 LOCAL_BROWSER_QUALIFICATION / 15 EXTERNAL_ENVIRONMENT.
- Product alignment audit: PASSED structurally; V1_PRODUCT_GOAL_ALIGNMENT: FAIL remains truthful.
- Tracked-secret scan: PASSED, no matches.
- Persistent readiness, service identity, private listeners, build provenance, and rollback target: PASSED.
- Browser operator checks: PASSED for this bounded negative/refusal/polish scope.
- Deployment/public exposure: NOT PERFORMED.

## Governed status and remaining gaps

No R row or DOD row was promoted in 065. The local queue count remains unchanged because the qualified negative branches do not satisfy the remaining positive/destructive or legitimate-target clauses.

Remaining local or gated work includes:

- DOD-004 generic workflow expansion and interruption/orphan qualification.
- DOD-005 remains BACKEND_ONLY/PARKED; no real reversible source was available.
- DOD-024/076/077 reversible and refusal boundaries advanced, but operator-confirmed completion and canonical Remove/Archive/Delete/Purge outcomes remain unqualified.
- DOD-026 negative correction validation passed; truthful positive correction/challenge acceptance remains unqualified.
- DOD-049 backup refusal passed; approved export/destructive restore remains unqualified.
- DOD-054 negative onboarding branches passed except a real cross-project duplicate target; positive registration remains unqualified.
- DOD-057 existing authority review/adoption idempotency passed; fresh non-overwriting provisioning remains unqualified.
- DOD-058 approved Goal protection and incomplete draft refusal passed; fresh approved Goal workflow remains unqualified.
- DOD-080 broader frozen polish/accessibility acceptance remains open.
- DOD-047/provider and other external-environment work remains separate.
- DOD-081, R-056, Phase 15 completion, and V1 declaration remain gated.

R-056: OPEN/GATED.
Phase 15: PARTIAL.
V1: NOT DECLARED.
Deployment: NOT PERFORMED.

## Evidence boundary

No raw credentials, tokens, authorization headers, host approval codes, or secret values are recorded. The browser session used an ephemeral trusted-host challenge; its code is intentionally omitted.
