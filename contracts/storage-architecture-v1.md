# Storage Architecture v1

## Canonical persistence

PRIME Core canonical state, migrations, durable jobs/workflows, audit records, project registry, node registry, events, settings metadata, and source-reference metadata use PostgreSQL. PRIME does not introduce SQLite, Redis, or a second durable queue.

Hindsight remains a separately owned memory service/database/schema behind the PRIME adapter. PRIME owns project binding, provenance, admission, correction/tombstone semantics, and public contracts; Hindsight internals never leak into PRIME APIs.

## Durability

- All cross-system operations use durable workflow records with idempotency keys, bounded retries, stale-result rejection, and explicit recovery state.
- Database migrations are versioned and reversible where supported.
- Backups cover PRIME canonical state and Hindsight data independently, with restore verification before release qualification.
- Cache, index, Brain layout, and other derived projections are disposable and never authority.

## Data separation

The Core PostgreSQL ownership boundary and Hindsight ownership boundary are distinct even when deployed in one supported PostgreSQL cluster. Credentials, schemas, retention, backup, and health status are independently tracked.
