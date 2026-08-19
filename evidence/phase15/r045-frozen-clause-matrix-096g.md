# Continuation 096G — R-045 Frozen-Clause Classification

Baseline: `08bdb6f15d3aca92d2f841c7402aa11c981ca5b4`

Authority: `PRIME-SPEC-V1.0.0` §19.6 and the Phase-15 mandatory large-repository/performance/capacity qualification.

This matrix was completed before product-code changes. It distinguishes implemented behavior from qualification debt and implementation gaps; related files are evidence pointers, not independent authority.

| Frozen clause | Classification | Current evidence | Required 096G action |
|---|---|---|---|
| Configurable global queue limits | ALREADY_QUALIFIED_BY_VALID_EXISTING_EVIDENCE | `CoreService.create_job`; Continuation 027 bounded 300-event parser burst at queue limit 32 with refusal and drain | Preserve and include in integrated rerun |
| Configurable per-project queue limits | IMPLEMENTATION_GAP | `capacity_policies` exists but is never read; admission uses only `PRIME_QUEUE_LIMIT` | Activate durable global/project policy resolution and enforce project admission |
| Per-project RUNNING concurrency | IMPLEMENTATION_GAP | `claim_job` claims the oldest queued job without project-aware running-job admission | Add durable project-aware claim bound and telemetry |
| Burst/reconnect bounded queues and backpressure | ALREADY_QUALIFIED_BY_VALID_EXISTING_EVIDENCE | Continuation 027 global bound/refusal/drain; canonical writes are not refused by derived-work saturation | Preserve and rerun with multiple projects |
| Coalescing | ALREADY_IMPLEMENTED_AND_NEEDS_QUALIFICATION | `create_coalesced_job`, `emit_coalesced_event`, and incremental observation dedupe exist | Exercise same-source burst collapse and bounded distinct-source backlog |
| Stale queued index work cannot overwrite current truth | ALREADY_IMPLEMENTED_AND_NEEDS_QUALIFICATION | Incremental observation rejects source-revision mismatch before projection, but no queued stale-job pressure evidence exists | Exercise current revision, queued stale revision, rejection, and current-state preservation |
| Reconnect reconciles current Git/manifests/authority rather than replaying assumed watcher history | ALREADY_QUALIFIED_BY_VALID_EXISTING_EVIDENCE | Continuations 090, 093, and 096 prove reconnect with unchanged Git, repository identity, Goal, Authority, and current-state reads | Preserve; no new reconnect architecture |
| Disk health visibility | ALREADY_IMPLEMENTED_AND_NEEDS_QUALIFICATION | `ReliabilityService.capacity_status` reports free bytes and HEALTHY/WARNING/CRITICAL | Simulate thresholds only and verify operator diagnostics |
| Disk-pressure suppression of rebuildable derived work | IMPLEMENTATION_GAP | `derived_work_allowed` is telemetry only; `create_job` does not enforce it | Refuse derived admission at simulated CRITICAL while allowing canonical writes; recover when healthy |
| Evidence global/per-project quotas | ALREADY_QUALIFIED_BY_VALID_EXISTING_EVIDENCE | `HistoryService._quota`; Continuation 027 and requirement tests cover refusal | Preserve and include in integrated matrix |
| Usage limits/refusal/recovery and truthful cost where available | ALREADY_QUALIFIED_BY_VALID_EXISTING_EVIDENCE | Continuations 082 and 096; DOD-047 is USER_USABLE_VERIFIED | Preserve; do not fabricate provider monetary data |
| Project Brain rebuildable-cache compaction | ALREADY_IMPLEMENTED_AND_NEEDS_QUALIFICATION | `prune_derived` retains a bounded number of Brain snapshots | Exercise rebuildable-first cleanup and regeneration/current-state behavior |
| Time Lens/history protection | IMPLEMENTATION_GAP | `retention_inventory` marks Time Lens pinned, but `prune_derived` deletes old Time Lens checkpoints | Remove Time Lens from automatic derived pruning and prove unchanged pinned history |
| Notion managed projection retention | ALREADY_IMPLEMENTED_AND_NEEDS_QUALIFICATION | Bounded projection cleanup exists; source/history records remain separate | Prove projection cleanup does not remove authoritative source/history references |
| Normalized events, audit logs, model traces/summaries, notifications, terminal/dead-letter jobs, and retained-source ledgers have configurable retention/compaction policy | IMPLEMENTATION_GAP | Existing `capacity_policies` schema is unused and there is no policy inventory/impact plan across these classes | Add bounded policy configuration and a reference-aware compaction plan; do not automatically delete protected classes |
| Reference-aware pruning and consequence disclosure | IMPLEMENTATION_GAP | Git checkpoint release checks one historical dependency; there is no general impact plan; automatic Time Lens deletion contradicts the clause | Add class inventory/impact reporting and fail closed for protected data unless explicit operator acceptance is supplied |
| Durable Hindsight memory is not deleted to satisfy cache limits | ALREADY_IMPLEMENTED_AND_NEEDS_QUALIFICATION | Existing cleanup code does not call Hindsight deletion, but pressure evidence has not asserted this boundary | Capture bank/model identity before/after cleanup and verify unchanged |
| UI exposes memory/storage growth and Hindsight/backend disk health | IMPLEMENTATION_GAP | Reliability diagnostics are returned by Core, but the web Diagnostics card does not render capacity/storage growth; Hindsight status is not included in the storage-health view | Extend the existing diagnostics surface only; no new monitoring subsystem |
| Rebuildable caches are removed before non-rebuildable history | IMPLEMENTATION_GAP | Brain cleanup exists, but Time Lens is incorrectly mixed into `prune_derived` | Restrict automatic cleanup to rebuildable projections and prove protected counts/hashes unchanged |
| Representative large-repository performance/capacity release test | ALREADY_IMPLEMENTED_AND_NEEDS_QUALIFICATION | Repository indexer and persistent external storage are available; no current governed representative-large-repository evidence exists | Create an isolated external-storage qualification repository/project, measure index/backlog/drain/search/reconnect, then retain or clean up per fixture governance |

## Scope decision

The implementation gaps form one bounded capacity-control boundary around the existing `capacity_policies`, job admission/claim path, retention service, and existing diagnostics surface. No second queue, search engine, monitoring service, database, Core stack, Node, Hindsight bank, or public route is justified.
