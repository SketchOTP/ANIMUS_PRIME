# Phase 1 qualification

Status: `PASS` once the recorded qualified commit is reached.

Phase 1 establishes the trusted Core substrate required by later feature phases:

- FastAPI Core bound to loopback by default;
- PostgreSQL-backed `prime_core` schema and reproducible migration runner;
- canonical project, source-reference, event, job, workflow, audit, notification, usage, settings, operator and session records;
- idempotent event/job/workflow primitives and PostgreSQL row/advisory-lock ordering;
- single-operator bootstrap, password sessions, offline recovery rotation, session revocation, CSRF/origin checks and authentication throttling;
- no-store/security headers and JSON structured logs that do not serialize request bodies or credentials;
- liveness/readiness health endpoints and a pinned containerized Core shape.

Evidence commands:

```text
PRIME_PHASE1_DB_URL=postgresql://prime:phase1-local-only@127.0.0.1:15432/prime \
  .venv/bin/python -m pytest tests/phase0 tests/phase1 -q
PRIME_PHASE1_DB_URL=postgresql://prime:phase1-local-only@127.0.0.1:15432/prime \
  .venv/bin/python scripts/phase1_qualify.py
```

The qualification database is disposable test state. Production-shaped state is kept in the `prime_core` schema and is distinct from Hindsight-owned state; no Redis or second durable queue is introduced.
