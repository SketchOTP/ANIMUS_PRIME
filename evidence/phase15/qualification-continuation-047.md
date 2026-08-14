# ANIMUS PRIME  Continuation 047

## Baseline and execution boundary

- Baseline: PRIME-SPEC-V1.0.0
- Authoritative execution: direct SSH/native Atlas only
- Checkout: /home/sketch/Projects/ANIMUS_PRIME
- Starting GitHub main: f5edeec6d7f793c84fbfc8b534cf9ebba6771922
- Temporary Core started: NO
- Persistent Core listener present: NO
- Browser run: NO
- Disposable resources: NONE
- PostgreSQL and Hindsight: existing persistent services only
- Phase 16: NOT STARTED
- Deployment: NOT PERFORMED
- R-045: OPEN / NOT ATTEMPTED
- R-056: OPEN

## Independent verifier exception

Continuation 046 was accepted except DOD-061 was reopened because the published production method referenced json.dumps without importing json, and the new focused tests did not execute the production method.

Persistent qualification project:

- project_id: project_d9a1a5b609394282b62fc12c0d04634d
- repository_id: repo_1eb92bbce8d44309861368d8690247c6
- repository: /home/sketch/Projects/ANIMUS_PRIME
- canonical revision before repair qualification: 5d2143f03ac205c0dd99d3d3abf281573b4a2bda
- actual HEAD at reproduction: f5edeec6d7f793c84fbfc8b534cf9ebba6771922
- changed path input: README.md

Real method reproduction before repair:

- method: RepositoryIndexer.observe_incremental
- exception: NameError
- message: name 'json' is not defined
- location: src/prime_core/indexer.py line 116 at the production source-snapshot json.dumps call
- transaction: the exception occurred before commit and the reproduction was not used to manufacture state

## DOD-061 repair

Implementation commit A: 0038ebbc80b28a00a4452752ccc295c8a2a3a31c

The repair:

- imported json in src/prime_core/indexer.py;
- added migration 0028_incremental_observation_provenance.sql;
- added observation_basis, canonical_revision, worktree_branch, and worktree_path provenance fields;
- requires source_revision to equal the repository's actual checked-out HEAD, otherwise returns bounded OBSERVATION_REVISION_MISMATCH;
- rejects a canonical A-to-B observation when the affected working-tree paths are dirty;
- detects same-HEAD dirty paths instead of returning NOOP;
- stores dirty bytes under a WORKTREE:<HEAD>:<content-digest> observation revision and never advances project_bindings.canonical_revision;
- preserves branch, canonical revision, worktree path, dirty paths, content hashes, and observation basis in repository rows, snapshots, and events;
- processes only normalized changed paths; no recursive root scan is used by observe_incremental;
- keeps deleted current rows historical but stale and excludes them from search;
- marks current Progress assessments stale on committed canonical revision advance;
- runs the existing AuthorityMemoryAdmission path only for committed canonical ledger changes.

## Direct same-HEAD dirty observation

Before commit A, the legitimate Continuation 047 evidence artifact was authored in the worktree while HEAD remained f5edeec6d7f793c84fbfc8b534cf9ebba6771922.

Observed result:

- status: OBSERVED_INCREMENTALLY
- observation_basis: WORKTREE_DIRTY
- changed_paths: evidence/phase15/qualification-continuation-047.md
- duplicate input paths were reduced to one path
- dirty_paths contained the evidence artifact
- canonical revision before and after remained f5edeec6d7f793c84fbfc8b534cf9ebba6771922
- project freshness became STALE
- current repository row recorded WORKTREE provenance, canonical revision f5edeec6d7f793c84fbfc8b534cf9ebba6771922, branch main, and /home/sketch/Projects/ANIMUS_PRIME
- authority-memory admission was explicitly NOT_RUN for dirty worktree bytes

## Direct committed A-to-B observation

After implementation commit A, the persistent project observed the real changed-file set:

- .agent/CURRENT.md
- .agent/DIRECTIVES.md
- evidence/phase15/qualification-continuation-047.md
- migrations/prime/0028_incremental_observation_provenance.sql
- src/prime_core/indexer.py
- tests/phase4/test_incremental_observation.py

Observed result:

- canonical revision advanced from f5edeec6d7f793c84fbfc8b534cf9ebba6771922 to 0038ebbc80b28a00a4452752ccc295c8a2a3a31c
- observation basis: COMMITTED_CANONICAL
- dirty_paths: none
- changed paths only: yes
- source snapshot metadata recorded the exact changed paths, revision, branch, and repository path
- one project-scoped REPOSITORY_CHANGED event was emitted
- 11 authority-memory records and 11 AUTHORITY_MEMORY_ADMISSION events were persisted at revision 0038ebb
- Progress assessments at prior revisions became STALE
- repeat of the same committed observation returned NOOP and memory count remained unchanged at 25

## Negative and direct-method matrix

- path traversal: PASSED
- absolute path: PASSED
- .git path: PASSED
- symlink/root boundary: PASSED
- invalid revision helper and real-method caller mismatch: PASSED; bounded ValueError / OBSERVATION_REVISION_MISMATCH
- stale/diverged caller revision: fail-closed before projection through actual-HEAD mismatch
- duplicate changed paths: PASSED
- same-HEAD dirty change: PASSED
- deleted changed path: PASSED; current row retraction path exercised without deleting a valuable source
- event coalescing: PASSED by project-scoped coalesced event key
- public route error boundary: preserved deliberate KeyError/ValueError/FileNotFoundError/OSError handling; no broad catch added

Focused direct-method tests: 5 passed.

## Integration gates

DOD-030 regression: PASSED for the incremental path. A committed .agent change caused automatic project-bound admission with source revision, source reference, content hash, record identity, dedupe key, and secret filtering behavior inherited from AuthorityMemoryAdmission. Repeating the same observation produced no second current memory record. Persistent Hindsight remained the approved backend; its slow retain/recall/consolidation behavior was observed directly.

DOD-063 regression: PASSED. The committed A-to-B incremental observation marked prior current Progress assessments STALE, while canonical binding advanced to B.

DOD-061 final: PRODUCT_VERIFIED. The real method executes, dirty same-HEAD state is not lost or mislabeled as clean Git truth, committed revision advance works, changed paths are bounded, stale/diverged input fails closed, deletion is retracted with historical provenance, Progress freshness is coherent, and DOD-030 admission is not regressed.

Other Continuation 047 harvest rows (DOD-033, DOD-045, DOD-007, DOD-028, DOD-018, DOD-006, DOD-037, DOD-038, DOD-039, DOD-004, DOD-005, DOD-009) were not promoted in this bounded publication. Existing exact blockers and evidence boundaries remain preserved; no browser/Core, native, second-device, Reflect/Mental-Models, or destructive workflow evidence was fabricated.

## Persistent validation

- pytest tests scripts -q -rs: PASSED  109 passed, 3 explicit FRESH_STATE_REQUIRED skips, 0 failures
- pytest -q -rs: PASSED  109 passed, 3 explicit FRESH_STATE_REQUIRED skips, 0 failures
- pytest --collect-only -q: PASSED  112 collected
- focused incremental tests: PASSED  5 passed
- py_compile: PASSED
- compileall: PASSED
- PostgreSQL health: PASSED
- Hindsight health/database connected: PASSED
- Core listener check: PASSED  no ANIMUS Core listener
- browser qualification: NOT RUN  no persistent Core listener
- TEMPLATE governance: PASSED
- ADOPTED governance: PASSED
- YAML/product/burndown/diff/secret checks: PASSED
- deployment: NOT PERFORMED

## Storage checkpoints

- root free at start: 28,428,435,456 bytes
- root free after focused work: 28,397,031,424 bytes
- root free after full regression: 28,395,769,856 bytes
- secondary free throughout: 159,130,316,800 bytes
- DiskFull recurrence: NO

## Final governed boundary for this continuation

DOD-061 returns to PRODUCT_VERIFIED. The published governed totals remain:

- USER_USABLE_VERIFIED: 14
- PRODUCT_VERIFIED: 21
- IMPLEMENTED_NOT_PRODUCT_QUALIFIED: 11
- BACKEND_ONLY: 21
- UI_SHELL_ONLY: 9
- PARTIAL: 4
- MISSING: 0
- BLOCKED_BY_ENVIRONMENT: 1
- TOTAL: 81
- COMPLETE: 35
- OPEN: 46

Burndown:

- LOCAL_CODE: 13
- LOCAL_BROWSER_QUALIFICATION: 16
- LOCAL_NATIVE_QUALIFICATION: 0
- EVIDENCE_RECONCILIATION: 2
- EXTERNAL_ENVIRONMENT: 15
- AGGREGATE_RELEASE_GATE: 0

V1_PRODUCT_GOAL_ALIGNMENT: FAIL because open requirements remain.
Phase 15: PARTIAL.
V1 release: FAIL.
