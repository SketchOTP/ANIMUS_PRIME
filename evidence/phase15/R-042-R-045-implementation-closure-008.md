# R-042–R-045 implementation closure — Continuation 008

Baseline: `PRIME-SPEC-V1.0.0`
Directive: `D-PRIME-PHASE15-REMEDIATION-008`
Status: implementation evidence only; not a VERIFIED release result.

## Local implementation boundary

- R-042: Continuity v2 backup manifests record `backup_id`, PRIME/spec/schema revisions, project scope, source high-water mark, component inventory/versions, encryption version, content hashes, destination class, verification state, and durable PostgreSQL metadata. AES-256-GCM with PBKDF2-HMAC-SHA256 fails closed on wrong key, tamper, and truncation. Schedules persist only an external recovery-key reference; credentials are not stored.
- R-043: restore preflight authenticates and validates the archive before mutation; populated targets refuse collision unless an explicitly safety-backed replace flow is selected; `restore_workflows` records durable progress/failure; clean-install restore restores canonical rows and managed file paths. The API requires `X-PRIME-STEP-UP: CONFIRM` for the non-replace restore path.
- R-044: the inventory includes PRIME PostgreSQL, source-ledger rebuild semantics for Hindsight, managed Evidence bytes plus external/node references, historical state, retained PRIME-owned Git bundles, non-secret configuration references, and explicit repository-source protection limitations. Restored fidelity distinguishes `EXACT` from `SOURCE_LEDGER_REBUILD`.
- R-045: active controls now include Evidence quotas already in the finalized Evidence service, derived queue bounds, coalesced event/job helpers, disk-pressure status, rebuildable projection cleanup, provenance-pinned Git release refusal, backup retention preserving the latest verified backup, and retryable schedule state.

## Qualification evidence executed locally

### Focused and regression checks

- `tests/phase13/test_backup_service.py` — 4 passed: authenticated round trip, secret rejection, tamper/truncation fail-closed behavior, and continuity inventory.
- `PRIME_PHASE1_DB_URL=... .venv/bin/python -m pytest tests -q` on a clean disposable PostgreSQL 17.10/pgvector environment — **47 passed**.
- Clean-install fixture: source PRIME database was migrated and populated with project, Node/repository binding, approved goal, managed Evidence, historical rows, and a PRIME-owned Git checkpoint; encrypted backup was created; a separate empty `prime_restore` database was migrated; restore completed; project identity, Evidence hash/file, historical state, and Git checkpoint bundle were preserved.
- Failure cases: wrong key failed closed before restore; archive tamper and truncation failed closed in focused tests.

### Regression protection for R-046–R-050

The clean-install fixture preserved:

- R-046 Evidence metadata, managed content, and content hash;
- R-047 SourceReference linkage;
- R-048 historical revision rows;
- R-049 retained Git checkpoint identity, `EXACT` coverage, and restored bundle bytes;
- R-050 historical reconstruction inputs. Hindsight is explicitly labeled `SOURCE_LEDGER_REBUILD`, not bit-identical memory restore.

## Qualification boundary

R-042–R-045 remain qualification `partial`, not VERIFIED. The local run did not prove a genuinely separate mounted/network/off-machine target, native service restart/reboot, live Hindsight exact-backend recovery, interrupted destructive restore, sustained burst/disk-pressure capacity, or full operator/browser qualification. No external evidence was fabricated. Deployment was not performed and V1 remains `FAIL`.

## Environment note

The codebase-memory MCP index/search transport returned `Transport closed`; targeted local inspection was used and the limitation remains recorded in `.agent/CURRENT.md` and `.agent/OUTCOMES.md`.
