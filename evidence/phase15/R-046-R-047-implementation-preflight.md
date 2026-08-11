# R-046/R-047 implementation preflight

Status: implementation slice only; not qualification evidence and not a VERIFIED claim.  
Baseline: `PRIME-SPEC-V1.0.0`  
Directive: `D-PRIME-PHASE15-REMEDIATION-007` (supersedes Continuation 006 preflight)

Continuation 007 closes the local R-046/R-047 implementation boundary with explicit managed-copy/Node-reference/external-reference storage modes, actual managed retrieval and reindex, MIME sniff/consistency checks, secret pre-scan, parser-unavailable recovery, global/project quota refusal, reference-aware purge protection, durable citation mutation/retraction reporting, and source-linked historical snapshots. It remains implementation evidence only.

Implemented locally:

- safe filename, MIME, privacy-class, size, active-content, and NUL validation;
- persisted Evidence `privacy_class`, `content_hash`, `storage_path`, `mime_type`, `size_bytes`, `parser_status`, and explicit `index_status`;
- project-scoped upload/reference/listing routes;
- explicit project-scoped Evidence retraction with reason and timestamp;
- regression coverage for safe metadata values and active/unknown values.

Qualification still required:

- real PostgreSQL migration and populated Evidence records;
- real parser/index execution and recovery status;
- citation resolution and validation association;
- backup/restore participation and retraction propagation into retrieval;
- project-isolation and live product-surface evidence.

Validation in this run:

- focused Evidence/history primitive tests: `PASSED` (8 tests without PostgreSQL);
- clean disposable PostgreSQL full regression: `PASSED` (43 passed);
- Python compile check: `PASSED`;
- PostgreSQL migration/history integration: `PASSED` in the disposable Phase-1 database;
- requirement qualification: `PARTIAL`; R-046/R-047 are now `IMPLEMENTED` / `OPEN` because parser/index recovery, citation-backed product runs, backup/restore and live isolation evidence are still open.
