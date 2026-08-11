# R-046/R-047 implementation preflight

Status: implementation slice only; not qualification evidence and not a VERIFIED claim.  
Baseline: `PRIME-SPEC-V1.0.0`  
Directive: `D-PRIME-PHASE15-REMEDIATION-006`

Continuation 006 extended this boundary with durable `SourceReference` linkage, bounded inert-text extraction for approved text MIME types, project quota enforcement, explicit Evidence links/annotations, safe HTTPS/approved-Node locators, historical cutoff context, and a read-only historical Ask context that records reconstruction status and never reuses current search results.

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

- focused Evidence validation tests: `PASSED` (3 tests);
- full regression: `PASSED` (24 passed, 15 skipped);
- Python compile check: `PASSED`;
- PostgreSQL integration qualification: `NOT RUN` (`PRIME_PHASE1_DB_URL` unset);
- requirement qualification: `NOT RUN`; R-046/R-047 remain `IMPLEMENTING` / `OPEN`.
