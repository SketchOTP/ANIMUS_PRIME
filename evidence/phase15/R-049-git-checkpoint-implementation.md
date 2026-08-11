# R-049 Git checkpoint implementation record

This is implementation evidence only. It is not a VERIFIED release qualification record.

The implementation now validates a canonical commit, packs only the selected commit graph into a disposable bare object store, creates a PRIME-owned bundle outside the managed repository, records the bundle hash and commit identity, and reports `EXACT`, `PARTIAL`, or `UNAVAILABLE` when the retained bundle is checked. The managed repository's refs are never mutated.

Focused evidence:

- `src/prime_core/git_history.py` — isolated object packing, bundle creation, hash verification, and truthful bundle status.
- `src/prime_core/history_service.py` — project-scoped PostgreSQL checkpoint registration and source-reference linkage.
- `tests/phase11/test_history_primitives.py::test_git_checkpoint_bundle_survives_ref_removal` — commits a fixture, retains commit A, removes normal refs, runs reflog expiry/GC, and verifies the retained bundle remains `EXACT`.

Remaining qualification: exercise `HistoryService.add_git_checkpoint` and `git_checkpoint_status` against qualified PostgreSQL, prove source-reconstruction after repository rewrite/GC through the full Time Lens flow, and record the exact qualification commit/evidence. Until then R-049 remains `IMPLEMENTED` / `partial` / `OPEN`.
