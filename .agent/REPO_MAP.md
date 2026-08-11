# Repository Map

## Entry points

- `README.md` — project boundary, operator orientation, and phase-gate context.
- `apps/core/main.py` — Core HTTP application entry point and authenticated operator/control-plane routes.
- `apps/node/main.py` — packaged Node service entry point with configured TLS/mTLS startup.
- `apps/web/index.html` — accessible responsive operator web shell.
- `scripts/phase0_qualify.py` — Phase 0 source-lock qualification entry point.
- `scripts/phase1_qualify.py` — Phase 1 migration and service qualification entry point.
- `scripts/phase2_qualify.py` — Phase 2 Node qualification entry point.
- `scripts/phase3_qualify.py` — Phase 3 onboarding qualification entry point.
- `scripts/phase4_qualify.py` — Phase 4 indexing qualification entry point.
- `scripts/phase5_qualify.py` — Phase 5 memory qualification entry point.
- `scripts/phase6_qualify.py` — Phase 6 MCP qualification entry point.
- `scripts/phase7_qualify.py` — Phase 7 Notion qualification entry point.
- `scripts/phase8_qualify.py` — Phase 8 progress qualification entry point.
- `scripts/phase9_qualify.py` — Phase 9 intelligence qualification entry point.
- `scripts/phase10_qualify.py` — Phase 10 Project Brain qualification entry point.
- `scripts/phase11_qualify.py` — Phase 11 Evidence and Time Lens qualification entry point.
- `scripts/phase12_qualify.py` — Phase 12 lifecycle and remote-access qualification entry point.
- `scripts/phase13_qualify.py` — Phase 13 reliability qualification entry point.
- `scripts/phase14_qualify.py` — Phase 14 web-shell qualification entry point.
- `scripts/phase15_qualify.py` — full regression, ledger, and V1 release-gate entry point.

## Core modules

- `src/prime_core/service.py` — Core service composition and project-scoped application services.
- `src/prime_core/config.py` — Core configuration and environment boundaries.
- `src/prime_core/db.py` — PostgreSQL connection and migration support.
- `src/prime_core/security.py` — operator authentication and security primitives.
- `src/prime_core/authority.py` — authority bootstrap and governed project authority.
- `src/prime_core/indexer.py` — repository index and source-freshness model.
- `src/prime_core/memory_service.py` — PRIME-owned memory ledger and correction semantics.
- `src/prime_memory_adapter.py` — Hindsight adapter boundary and durable-write verification.
- `src/prime_core/mcp_service.py` — project-scoped PRIME Memory MCP surface.
- `src/prime_core/notion_api.py` — server-side Notion transport, retry, and provider boundary.
- `src/prime_core/notion_service.py` — managed Notion projection and lifecycle foundation.
- `src/prime_core/progress_service.py` — deterministic GoalModel and evidence-backed progress.
- `src/prime_core/intelligence_service.py` — project-scoped Ask/Search/activity foundation.
- `src/prime_core/brain_service.py` — derived Project Brain topology.
- `src/prime_core/history_service.py` — Evidence, Time Lens, Fork, and historical checkpoint foundation.
- `src/prime_core/git_history.py` — isolated canonical-commit object packing, PRIME-owned bundle creation, hash verification, and truthful checkpoint status.
- `src/prime_core/history_primitives.py` — pure EXACT/PARTIAL/UNAVAILABLE historical coverage aggregation.
- `src/prime_core/evidence_validation.py` — Evidence filename, MIME, privacy, size, content, and locator validation.
- `src/prime_core/lifecycle_service.py` — lifecycle and destructive-action safety.
- `src/prime_core/backup_service.py` — authenticated Continuity v2 backup snapshots, manifest/content verification, clean restore, managed Evidence/Git payload recovery, and fidelity labels.
- `src/prime_core/reliability_service.py` — durable backup records/schedules, capacity health, retention, queue pressure, and reference-aware cleanup controls.
- `src/prime_core/remote_access_service.py` — private Tailscale Serve control and status boundary.
- `src/prime_core/node_client.py` — Core-to-Node protocol client with identity and TLS support.
- `src/prime_node/service.py` — Node lifecycle, repository boundary, heartbeat, and enrollment behavior.
- `src/prime_node/config.py` — Node bind, TLS/mTLS, and service-mode configuration.

## Interfaces and contracts

- `contracts/authority-file-contract-v1.md` — AuthorityFileContract.
- `contracts/shared-domain-contracts-v1.yaml` — shared project, node, event, and MCP contracts.
- `contracts/project-isolation-v1.md` — project isolation contract.
- `contracts/storage-architecture-v1.md` — canonical PostgreSQL and component storage architecture.
- `contracts/privacy-egress-v1.md` — deny-by-default privacy and egress policy.
- `baseline/PRIME-SPEC-V1.0.0.notion.md` — immutable exported normative specification.
- `baseline/Implementation-Handoff-Record-PRIME-SPEC-V1.0.0.notion.md` — immutable implementation handoff.
- `baseline/implementation-baseline.yaml` — approved baseline identity and source-lock hashes.
- `docs/requirements-traceability.yaml` — requirements traceability ledger.
- `docs/phase15-remediation-matrix.yaml` — broad remediation mapping and release reconciliation.
- `docs/phase15-remediation-qualification-ledger.yaml` — individual R-031 through R-056 qualification queue.
- `docs/phase15-remediation-queue.md` — Continuation 005 A/B/C work queue and VERIFIED/26 counts.
- `docs/phase15-qualification-procedures.md` — deterministic procedures for every external qualification domain.
- `docs/phase15-skipped-test-inventory.md` — all 15 skipped tests mapped to requirements and prerequisites.
- `threat-model/PRIME-V1.md` — V1 threat model and security assumptions.

## Tests and validation

- `tests/phase0/` — source-lock, contract, harness, and Hindsight adapter tests.
- `tests/phase1/` — Core substrate and persistence tests.
- `tests/phase2/` — Node service, protocol, TLS/mTLS, and client tests.
- `tests/phase3/` — onboarding and authority provisioning tests.
- `tests/phase4/` — indexer and source-freshness tests.
- `tests/phase5/` — memory ledger and correction tests.
- `tests/phase6/` — PRIME Memory MCP tests.
- `tests/phase7/` — Notion API and projection tests.
- `tests/phase8/` — progress model tests.
- `tests/phase9/` — Ask/Search/intelligence tests.
- `tests/phase10/` — Project Brain tests.
- `tests/phase11/` — Evidence and historical tests.
- `tests/phase12/` — lifecycle and remote-access tests.
- `tests/phase13/` — backup and reliability tests.
- `tests/phase14/` — web-shell tests.
- `scripts/test_validate_governance.py` — governance validator regression tests.
- `scripts/validate_governance.py` — adopted/template governance validator.
- `.github/workflows/phase0.yml` — repository qualification workflow.
- `evidence/phase0/` — Phase 0 qualification evidence.
- `evidence/phase15/` — Phase 15 release, remediation, and R-031 evidence.
- `.agent/phase-records/` — append-only phase records for Phases 0–15.

## Configuration

- `Dockerfile.core` — pinned Core image build.
- `Dockerfile.node` — pinned Node image build.
- `docker-compose.phase0.yml` — Phase 0 PostgreSQL/pgvector/Hindsight qualification stack.
- `docker-compose.phase0.mock-llm.yml` — Phase 0 mock-LLM qualification stack.
- `docker-compose.phase1.yml` — disposable Core/Node/PostgreSQL qualification stack.
- `requirements-phase1.txt` — Phase 1–15 Python runtime dependency set.
- `dependencies/pins.yaml` — qualified dependency and image pins.
- `dependencies/SBOM.cdx.json` — dependency SBOM.
- `dependencies/QUALIFICATION.md` — dependency/license qualification evidence.
- `migrations/prime/` — ordered PostgreSQL migrations from Core through remediation foundations.
- `migrations/prime/0015_evidence_lifecycle.sql` — Evidence retraction and explicit parser/index lifecycle fields.
- `migrations/prime/0016_historical_evidence.sql` — Evidence source identity/annotations/links, observed metadata, and retained Git checkpoint metadata.
- `migrations/prime/0017_historical_revisions.sql` — explicit Evidence storage modes, authority/Notion snapshots, historical revision ledger, and Git source linkage.
- `migrations/prime/0018_historical_snapshot_immutability.sql` — append-only lifecycle snapshot identity correction.
- `migrations/prime/0019_evidence_parser_states.sql` — explicit parser lifecycle states including retraction.
- `migrations/prime/0020_continuity_capacity.sql` — continuity backup manifest fields, durable restore workflow, schedule state, and capacity policies.
- `packaging/node/prime-node.service` — Linux service definition.
- `packaging/node/install-node.ps1` — Windows installation guidance.
- `packaging/node/README.md` — Node packaging and TLS/mTLS configuration contract.

## Generated areas

- `authority-template/v1/` — materialized approved authority template and its governed package metadata.
- `authority-template/v1/MANIFEST.sha256` — authority-template content manifest.
- `evidence/phase15/remediation-qualification-001.md` — first clean PostgreSQL remediation qualification record.
- `evidence/phase15/remediation-qualification-002.md` — second clean PostgreSQL remediation qualification record.
- `evidence/phase15/remediation-qualification-003.md` — latest 38-test remediation qualification record.
- `evidence/phase15/R-031-local-tls-mtls-process.md` — real local HTTPS/mTLS process evidence.
- `evidence/phase15/R-046-R-047-implementation-preflight.md` — implementation-only Evidence preflight; not release qualification.
- `evidence/phase15/R-049-git-checkpoint-implementation.md` — implementation-only Git checkpoint preservation record; not release qualification.
- `evidence/phase15/R-046-R-050-implementation-closure-007.md` — Continuation 007 local implementation closure evidence; not release qualification.
- `evidence/phase15/R-042-R-045-implementation-closure-008.md` — Continuation 008 local backup/restore/capacity implementation closure; not release qualification.
- `.pytest_cache/` — local pytest cache and not a release artifact.
- `src/**/__pycache__/` — local Python bytecode cache and not a release artifact.

## External integration points

- `src/prime_core/notion_api.py` — live Notion API integration boundary.
- `src/prime_core/remote_access_service.py` — Tailscale CLI/Serve integration boundary.
- `src/prime_memory_adapter.py` — Hindsight service integration boundary.
- `src/prime_core/node_client.py` — Core-to-Node network integration boundary.
- `baseline/*.notion.md` — frozen external Notion source exports.
- `packaging/node/` — native Linux and Windows installation integration points.
- `docker-compose.phase0*.yml` — PostgreSQL, pgvector, Hindsight, Core, and Node integration environments.
- `.cursor/` — editor/tool integration rules and local MCP configuration.

## Areas that must not be edited manually

- `baseline/` — immutable source-lock artifacts; changes require a new approved baseline.
- `authority-template/v1/` — approved template package; changes require a new template version and manifest.
- `baseline/implementation-baseline.yaml` — governed baseline identity; changes require the SpecChangeRecord/new-baseline process.
- `authority-template/v1/MANIFEST.sha256` — generated manifest; regenerate only through the authority-template qualification workflow.
- `evidence/phase0/` — historical qualification evidence; append corrections rather than rewriting results.
- `evidence/phase15/qualification-report.md` — historical Phase-15 release result; preserve the recorded FAIL while adding new qualification records.
