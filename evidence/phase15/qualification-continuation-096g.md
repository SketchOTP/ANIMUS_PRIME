# ANIMUS PRIME — Continuation 096G R-045 capacity closure

Date: 2026-08-19

Disposition: **PASS**

Frozen baseline: `PRIME-SPEC-V1.0.0`

Starting governed/public commit: `08bdb6f15d3aca92d2f841c7402aa11c981ca5b4`

Qualified implementation commit: `d067a247dbeea47eb8b061111db04e7cd95bebe2`

## Frozen-clause classification

The pre-implementation classification is preserved in `evidence/phase15/r045-frozen-clause-matrix-096g.md`. Existing evidence already covered global queue refusal/drain, canonical-write priority, Evidence quotas, reconnect/current-truth semantics, and usage/cost refusal/recovery. Direct qualification was still required for index coalescing/stale revisions and retention. Investigation proved narrow implementation gaps in per-project running limits, enforceable durable capacity policies, disk-pressure admission, protected retention, and operator diagnostics; no replacement queue or storage architecture was required.

## Minimal implementation

- Added migration `0041_capacity_controls.sql` for durable global/project capacity policy, including `running_limit`.
- Enforced bounded global and per-project admission and PostgreSQL-backed project-aware worker claims.
- Added durable source-key coalescing and stale-revision refusal without a second scheduler.
- Refused derived work under simulated CRITICAL disk pressure while allowing canonical continuity work.
- Added a complete eight-class retention impact plan; automatic pruning is restricted to rebuildable Brain cache. Time Lens, Notion history, citations, checkpoints, Goal/Progress/corrections, SourceReferences, and durable Hindsight memory remain protected.
- Added authenticated capacity-policy configuration and bounded Diagnostics telemetry in Core and the genuine Web UI.

## Integrated pressure qualification

Qualification database/project was isolated from persistent canonical state. The representative repository was generated under `/mnt/storage1tb/prime-qualification/continuation-096g/representative-repo` and marked as a qualification fixture.

- Repository corpus: 6,001 files.
- Final fixture revision: `fa1b57f343bd7c4cb50198f7c54774fe4981e2ac`.
- Full index: 6,001 files in 2.408 seconds.
- Post-index known-target search: 0.359 seconds; expected target found.
- Bounded incremental refresh: 100 changed files.
- Stale-revision behavior: an older observation was refused both before and after current projection; canonical revision remained current.
- Source-key coalescing: 1,000 identical requests produced exactly one durable job.
- Per-project queue cap: 24; 23 distinct jobs accepted and 77 refused after the coalesced job occupied one slot.
- Per-project running cap: 2; a third claim returned none while two jobs were running.
- Fairness: project-aware claiming allowed another project to progress without exceeding either project limit.
- Drain/recovery: running and queued qualification work drained to zero and capacity returned to normal.
- Retention: durable policies existed for all eight frozen resource classes; rebuildable Brain rows reduced from 4 to 1 while Time Lens remained 4 of 4.
- Pinned/protected continuity: ordinary cleanup did not release protected historical/provenance state.
- Hindsight: health remained CURRENT; no automatic memory deletion occurred.
- Disk simulation: HEALTHY to CRITICAL refused derived work, admitted a canonical backup job, then returned to HEALTHY after controlled reset. No physical disk-fill test or persistent host mutation occurred.
- Reconnect/current truth: final index remained bound to the current Git revision and repository manifest; no watcher history was fabricated.

Qualification identities:

- project: `project_baaf48ec96064052b99b96c0159b96ae`
- repository: `repo_d34bc92f84f54b0ca12eb6a2d318e8fd`
- node: `node-096g-atlas-external`

After validation, the exact transient databases `prime_096g_capacity` and `prime_096g_qualification` and transient role `prime_096g_test` were removed. The marked external repository fixture and screenshot were retained for reproducibility; canonical PRIME data was not deleted or reset.

## Browser/operator qualification

Browser: persistent gstack Playwright Chromium installed outside the repository at `/mnt/storage1tb/prime-tooling/gstack-playwright`.

Private URL: `https://atlas-2.tail1a5964.ts.net/`

Trusted-host authentication passed. The genuine persistent System Health/Diagnostics UI rendered:

- queue status `NORMAL`, queued `32`, queue limit `1000`;
- disk status `HEALTHY` and free-byte telemetry;
- PostgreSQL database bytes `71718579`;
- durable memory records `253`;
- Hindsight health `CURRENT`;
- protected auto purge `DISABLED`.

After clearing pre-auth polling history and reloading the authenticated page, the browser console had no errors. Screenshot evidence is retained outside the repository at `/mnt/storage1tb/prime-qualification/continuation-096g/browser-diagnostics.png`, SHA-256 `46c456745b314b92d5b617168d42efa58e8076df51fa1e1ef679fa5c8b354108`.

## Validation

- Focused database-backed 096G plus burndown tests: **11 passed / 0 failed**.
- Full supported regression: **167 passed / 41 skipped / 0 failed**.
- Skip explanation: the historical 35 environment/integration skips remain; six new isolated PostgreSQL-backed 096G checks skip in the environment-free full run and passed separately against the approved isolated qualification database.
- Integrated qualification script: PASSED.
- Compile/static imports: PASSED.
- YAML/governance/burndown/cross-view validation: recorded at governed closeout.
- Diff and secret review: PASSED; no credential was printed or committed.

## Persistent runtime provenance and recovery

- Image: `animus-prime-core:continuation-096g-d067a24`.
- OCI revision: `d067a247dbeea47eb8b061111db04e7cd95bebe2`.
- Build timestamp: `2026-08-19T18:57:00Z`.
- Schema: `0041_capacity_controls.sql`.
- systemd restart changed MainPID from `3508331` to `3513951` and ActiveEnterTimestamp from `14:56:32 EDT` to `14:59:04 EDT`.
- Post-restart readiness returned exact spec/build/image/schema identity.
- The prior stopped Core container remains preserved as a bounded rollback artifact; it is not active.

## Frozen disposition

R-045: **VERIFIED**. The complete frozen capacity, backpressure, coalescing, stale-job, retention-protection, disk-pressure, representative-repository, drain/recovery, current-truth, and preserved usage/cost boundary is directly supported.

DOD-081: **PRODUCT_VERIFIED**.

R-056: **VERIFIED**.

Definition of Done: **81 complete / 0 open**.

Phase 15: **COMPLETE**.

V1: **QUALIFIED against PRIME-SPEC-V1.0.0 for private production use**.

No public deployment, Funnel change, Windows action, Phase 16, or Continuation 097 occurred.
