# Phase 0 Qualification Plan and Evidence Index

Baseline: `PRIME-SPEC-V1.0.0`

Phase 0 may pass only when every required output has a verifiable artifact and every required test has an explicit result.

## Gate checklist

- [ ] Frozen specification export and exact SHA-256 verified.
- [ ] Handoff identity verified against operator-provided tuple.
- [ ] `authority-template/v1` materialized, manifest verified, and validator passes.
- [ ] Traceability contains zero `UNASSIGNED` records.
- [ ] Shared domain, authority, isolation, storage, privacy, and error contracts reviewed.
- [ ] Threat model has an owner for every high-risk trust boundary.
- [ ] Exact dependency pins and license/SBOM inputs recorded.
- [ ] PostgreSQL/pgvector migration and restore smoke passes.
- [ ] Hindsight adapter compatibility smoke passes for normal, failure, degraded, recovery, and isolation semantics.
- [ ] Baseline mismatch tests fail closed.
- [ ] Test harness and CI entry point run cleanly.
- [ ] Initial governed Git commit exists and is recorded.
- [ ] Phase qualification record is `PASS` with exact qualified commit.

Evidence belongs under `evidence/phase0/` and must never contain secrets, provider credentials, raw memory, or unredacted logs.
