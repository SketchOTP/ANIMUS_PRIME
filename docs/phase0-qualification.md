# Phase 0 Qualification Plan and Evidence Index

Baseline: `PRIME-SPEC-V1.0.0`

Phase 0 may pass only when every required output has a verifiable artifact and every required test has an explicit result.

## Gate checklist

- [x] Frozen specification export and exact SHA-256 verified.
- [x] Handoff identity verified against operator-provided tuple.
- [x] `authority-template/v1` materialized, manifest verified, and validator passes.
- [x] Traceability contains zero `UNASSIGNED` records.
- [x] Shared domain, authority, isolation, storage, privacy, and error contracts reviewed.
- [x] Threat model has an owner for every high-risk trust boundary.
- [x] Exact dependency pins and license/SBOM inputs recorded.
- [x] PostgreSQL/pgvector migration and restore smoke passes.
- [x] Hindsight adapter compatibility smoke passes for normal, failure, degraded, recovery, and isolation semantics.
- [x] Baseline mismatch tests fail closed.
- [x] Test harness and CI entry point run cleanly.
- [x] Initial governed Git commit exists and is recorded.
- [x] Phase qualification record is `PASS` with exact qualified commit `8ce35b857c428a8139ca4b988a2db2f11680f09c`.

Evidence belongs under `evidence/phase0/` and must never contain secrets, provider credentials, raw memory, or unredacted logs.
