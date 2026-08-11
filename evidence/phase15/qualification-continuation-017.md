# ANIMUS PRIME — Phase 15 Qualification Continuation 017

- Baseline: `PRIME-SPEC-V1.0.0`
- Freeze: `2026-08-10T15:41:00Z`
- Directive: `D-PRIME-PHASE15-REMEDIATION-017`
- Qualified implementation commit: `dbf94f7eab521c4a0973681654a83fddec8470db`
- Deployment: `NOT PERFORMED`
- R-056: `OPEN`

## Fresh qualification environment

- PostgreSQL: `17.10`
- pgvector: `0.8.2`
- Approved image: `pgvector/pgvector@sha256:e04af45eb526378554a24ed05b37d9ea56fd623feca9adf264d4f47d875c9a93`
- Migrations: `24/24` from a recreated empty database
- Full regression and Phase 1–14 gates: `PASS` — `79 passed`
- Adopted governance, compileall, and diff checks: recorded with the governed checkpoint

## Newly verified requirements

### R-046 — Evidence storage and parser/index boundary

The real PostgreSQL-backed fixture exercised:

- active HTML and active SVG rejection;
- MIME/extension disagreement and unsupported MIME rejection;
- oversize refusal;
- bounded 200,000-character extraction;
- inert compressed/binary content remaining unsupported rather than executed;
- Node-reference root escape rejection and stale/missing Node-reference degradation;
- managed-copy SHA-256 identity, provenance, project isolation, and retrieval;
- parser unavailable → reindex recovery;
- Evidence → encrypted Continuity-v2 backup → clean separate database restore → same Evidence identity/hash/source reference → reindex with the same durable identity.

R-046 promotion is based on the complete exercised file, parser, boundary, isolation, backup, restore, and recovery matrix.

### R-047 — Product-level Evidence citations

The real PostgreSQL-backed fixture exercised:

- Search returning project-scoped Evidence and its durable `SourceReference`;
- Ask admitting Evidence as untrusted source data and returning a citation containing E1 and S1;
- Progress assessment retaining the Evidence source reference;
- Documentation-source projection rendering the Evidence/SourceReference citation in the managed projection;
- retraction removing the source from current Search while historical citation state remains explicit;
- restored/reindexed Evidence retaining the original content hash;
- Project A attempting Project B Evidence access being rejected.

The implementation repair adds Evidence to the production Intelligence Search/Ask source set and preserves the citation identity through the Progress path.

## Exercised but not promoted

- R-042: a real `/mnt/storage1tb` `/dev/sdb1` target passed encrypted backup and manifest classification as `off-machine`; complete scheduled failure/recovery evidence remains open.
- R-043: clean separate PostgreSQL restore, identity/hash/provenance comparison, wrong-key/tamper/truncation/collision preflight coverage, and deterministic interruption with durable `REPAIR_REQUIRED` state passed; the full representative-state/fresh-install replacement matrix remains open.
- R-045: 256-event burst, queue cap/refusal, quota refusal, disk warning, and health recovery passed; parser-concurrency, indexing backlog, retention, stale-job, and cost-limit sustained evidence remains open.
- R-048: A/B/C/D PostgreSQL-backed historical repository, authority, goal, progress, Evidence, memory, Notion projection, Git, historical Ask/Brain, no-future-leakage, source-removal `PARTIAL`, restoration/reindex `EXACT`, and Return-to-Now fixture passed; correction overlays and complete source-class removal/recovery evidence remain open.
- R-050: backend historical Ask/Brain fixture passed; the required real browser historical representation remains open.

## Browser, native, provider, and remote checks

- Chromium `150.0.7871.128`: shell load, fresh setup/bootstrap, operator auth, project creation, protected state, project selection, Search/Ask degraded state, all required surface IDs, desktop-to-390px responsive layout, keyboard focus movement, reduced-motion emulation, textual status semantics, untrusted project-name text rendering, destructive confirmation open/cancel, logout protection, and relogin were exercised. The prescribed `agent-browser` executable was not installed; Chromium CDP/headless interaction was used. Full assistive-technology and historical browser walkthrough remains partial.
- Native Linux: host/systemd present and installer syntax passed; UID is non-root, `/etc` is not writable, `prime-node.service` is absent. Native install/service/reboot/credential lifecycle was not run. Windows unavailable.
- Tailscale `1.102.2`: existing unrelated Funnel remains; PRIME correctly refuses unsafe configuration and reports `FUNNEL_EXPOSED`/`REFUSED`. No external configuration was changed; private second-device qualification remains partial.
- Hindsight: real backend health/create/recall passed; retain was `DEGRADED` because no durable recallable result was returned and reflect was `UNAVAILABLE`. Disposable bank was deleted. Approved model/provider qualification remains partial.
- Notion: existing MyAssistant credential source remains `NOT FOUND`; no secret was printed, persisted, or reused. R-037–R-041 remain environment-blocked.
- AI: no approved provider/profile or approved local inference runtime is configured; ambient credentials were not reused. R-054/R-055 remain environment-blocked.
- Off-machine: independent `/dev/sdb1` target was found and exercised for R-042; R-042 remains partial for complete scheduled/recovery acceptance.
- Codebase-memory MCP: `Transport closed`; targeted local fallback was used and this limitation was recorded.

## Reconciled release state

```text
IMPLEMENTATION: 25/26
VERIFIED: 3/26 — R-046, R-047, R-049
PARTIAL: 15/26
BLOCKED_BY_ENVIRONMENT: 8/26
FAILED: 0
R-056: OPEN
PHASE 15 / V1: FAIL
DEPLOYMENT: NOT PERFORMED
```

The aggregate gate remains `FAIL`; no V1 release claim is made.
