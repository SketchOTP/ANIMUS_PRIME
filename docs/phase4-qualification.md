# Phase 4 qualification

Phase 4 provides deterministic, disposable repository indexing:

- one canonical repository snapshot revision per index run;
- file path/content hash/size/kind/source revision/freshness records;
- project-scoped path search over indexed metadata;
- no execution of repository content and no second durable memory store;
- idempotent re-indexing and rebuildable derived records.

The Core API returns explicit `CURRENT` source freshness and rejects indexing without a bound working repository.
