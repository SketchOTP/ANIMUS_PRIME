# ANIMUS PRIME V1 Threat Model

Status: `PHASE_0_BASELINE`

## Trust boundaries

| Boundary | Assets | Primary threats | Required controls |
|---|---|---|---|
| Operator UI/Core | project registry, credentials, lifecycle state | auth bypass, CSRF, destructive misuse | secure sessions, origin checks, step-up auth, audit, confirmation |
| Core/Node control plane | repository paths and contents | node spoofing, arbitrary shell, path escape | enrollment, mTLS/private transport, roots, path canonicalization, read-only APIs |
| Project MCP | memory/context and project identity | namespace spoofing, prompt injection, data leak | session-bound project scope, capability limits, provenance, untrusted-input handling |
| Core/PostgreSQL | canonical state and jobs | injection, corruption, replay, outage | parameterized access, migrations, transactions, idempotency, backups |
| PRIME/Hindsight | durable memory | cross-bank retrieval, stale authority, provider egress | adapter boundary, bank binding, source ledger, tombstones, privacy policy |
| Core/Notion | managed/user content | overwrite, wrong-page write, prompt injection | managed-section ownership, page binding, untrusted content, retry/degraded states |
| Model providers | prompts, derived outputs, credentials | exfiltration, hallucinated authority, fallback | explicit profile, deny-by-default egress, citations, no model authority |
| Tailscale | remote operator access | public exposure, lateral access | tailnet-only allowlist, no Funnel, auth, health/reporting |
| Evidence/browser | imported URLs, HTML/SVG/Markdown | SSRF, XSS, prompt injection | fetch allowlist, sandboxed rendering, size/type limits, data-only semantics |
| Backup/destructive workflows | recoverable project data | deletion, tampering, unverified restore | explicit command, step-up auth, encrypted backup, restore rehearsal, audit |

## High-risk decisions

No high-risk boundary is unowned. Each boundary has an owning implementation phase and final adversarial validation in Phase 15. A failed isolation, path, credential, public-exposure, or destructive-safety test is release-blocking.

## Failure truthfulness

Unavailable dependencies are represented as `OFFLINE`, `DEGRADED`, `PARTIAL`, or `UNAVAILABLE`; the system never fabricates freshness, progress, citations, or successful memory writes.
