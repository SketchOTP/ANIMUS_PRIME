# Continuation 091 durable workflow matrix

Baseline: `eb39fb51ed45e5b70c8bd0f7612e0e881cfb3c98`  
Qualified implementation: `f3772ee560651d998e31ff46bf373983894f0e94`

| Operation | External side effect | Durable identity / steps | Replay policy | Resource ledger | Recovery disposition |
|---|---|---|---|---|---|
| Fork / Clone | Git clone, authority files, MCP scope, Hindsight bank | Stable Fork key; reserve, clone, checkout, sanitize, authority, repository, Goal, index, MCP, Hindsight, finalize | clone/authority/MCP are non-idempotent and reconciled; checkout/index/Hindsight are idempotent | child project, repository, MCP scope, Hindsight bank | Adopt a valid existing clone; refuse an invalid target; never create a duplicate child |
| Notion Project Record | Live Notion page creation | Stable `project-record/<project>` key; expected, created, bound | idempotent external | exact Notion page locator plus marker discovery metadata | Search exact PRIME idempotency marker after lost response/process death, then bind the existing page |
| Hindsight bank | Persistent bank creation | Stable project bank key; expected, created, bound | idempotent external | bank locator | Stable PUT and durable reread prevent duplicate banks |
| Repository creation | Node filesystem/Git creation | expected, created, final completion | non-idempotent external | repository path/identity | Resume plan requires reconciliation rather than blind recreation |
| Authority / Goal provisioning | Node repository writes | dedicated durable workflow/step records | non-idempotent external where writes occur | repository-bound workflow metadata | Completed checkpoints skip replay; interrupted writes require explicit reconciliation |
| MCP scope | Durable credential/scope issuance | Fork MCP step | non-idempotent external | scope identity, never secret material | Missing one-time secret is surfaced as reconciliation/rotation required |
| Restore | Canonical database replacement from verified bundle | deterministic backup/bundle key; validate, apply, verify | canonical apply is non-idempotent | restore identity and surviving restore record | Surviving restore ledger is discovered after schema replacement; completed restore is adopted, not replayed |
| Archive/remove/delete/purge | No external mutation in current V1 implementation | canonical DB transaction, audit, event | database transaction | canonical lifecycle state | No fake multi-system workflow added; external resources are preserved/untouched by contract |
| Rebind | Read-only Node inspection plus canonical DB switch | existing protected preflight + DB transaction | no external mutation | repository identity/history | Stale confirmation refuses; no external orphan can be created |

The matrix distinguishes actual multi-system side effects from atomic canonical-state transitions. It does not claim that every lifecycle button creates an external resource.
