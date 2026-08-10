# Project Isolation Contract v1

Every project-scoped read, write, job, event, index, memory bank, Notion binding, MCP grant, progress assessment, Evidence record, historical reconstruction, and Brain projection is keyed by exactly one authenticated `project_id`.

## Invariants

- A session's project scope is bound below the model and cannot be changed by request payload.
- Repository paths are resolved against the registered project/node root; symlink, junction, case, and Unicode escapes are rejected.
- Memory retrieval and writes are bank-scoped and source-ledger-scoped to the authenticated project.
- A project-scoped MCP connection cannot enumerate, select, or infer another project.
- Derived indexes and Brain snapshots contain only the bound project's sources.
- Notion Documentation Agent writes only its bound managed page and never user Knowledge Sources.
- Fork/Clone creates fresh credentials, memory, progress, events, and Notion state.
- Cross-project reasoning and merged graph views are not V1 capabilities.

## Contract-test cases

1. Project A token requesting Project B returns `FORBIDDEN` without revealing existence.
2. A memory query with a forged project ID uses the authenticated scope and cannot return B.
3. A path containing `..`, symlink, junction, alternate worktree, or case-folded escape is rejected.
4. A queued job with a mismatched project scope is rejected as stale/forbidden.
5. A Brain projection containing a foreign node fails snapshot validation.
6. A Notion write to an unbound page fails before provider dispatch.
