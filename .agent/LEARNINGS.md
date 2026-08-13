# Project Learnings Template

After adoption, use this append-only file for durable, verified project knowledge only.

## Entry guidance after adoption

Each live entry should include:

- Learning ID.
- Date.
- Fact or lesson.
- Evidence location.
- Confidence: `VERIFIED` or `PROVISIONAL`.
- Scope.
- Supersedes or superseded-by reference when applicable.

Do not add live entries to this template. Exclude temporary narration, raw logs, full source files, secrets, unsupported guesses, and facts already obvious from stable project documentation.

## L-PRIME-PHASE0-001

- Date: 2026-08-10
- Learning ID: L-PRIME-PHASE0-001
- Fact or lesson: Hindsight 0.6.1 may return a successful retain response while provider extraction stores no memory; PRIME must verify a durable, recallable postcondition and expose DEGRADED when it is absent.
- Evidence location: evidence/phase0/qualification-report.md; src/prime_memory_adapter.py
- Confidence: VERIFIED
- Scope: PRIME Hindsight adapter and all future memory writes.
- Supersedes learning: none

## L-PRIME-PHASE15-010

- Date: 2026-08-11
- Learning ID: L-PRIME-PHASE15-010
- Fact or lesson: Node identity state must be constructed from environment at instance creation, not captured in dataclass class defaults; otherwise test order or service reuse can silently point multiple Node instances at one state file. Native packaging must keep identity/configuration outside the repository and make repair idempotent.
- Evidence location: src/prime_node/config.py; packaging/node/install-node.sh; packaging/node/install-node.ps1; tests/phase2/test_node_continuation009.py; evidence/phase15/R-031-R-034-implementation-closure-009.md.
- Confidence: VERIFIED
- Scope: R-031–R-034 Node lifecycle and packaging.
- Supersedes learning: none

## L-PRIME-PHASE15-001

- Date: 2026-08-10
- Learning ID: L-PRIME-PHASE15-001
- Fact or lesson: Phase-15 remediation is governed by the individual R-031 through R-056 qualification ledger; implementation presence or automated tests alone cannot move a requirement to VERIFIED, and unavailable native/live prerequisites must be recorded exactly rather than simulated.
- Evidence location: docs/phase15-remediation-qualification-ledger.yaml; evidence/phase15/remediation-qualification-003.md; attached Phase 15 Remediation Continuation 004 instruction.
- Confidence: VERIFIED
- Scope: Phase-15 remediation, release gating, and all future qualification runs.
- Supersedes learning: none

## L-PRIME-PHASE15-002

- Date: 2026-08-10
- Learning ID: L-PRIME-PHASE15-002
- Fact or lesson: The canonical repository has progressed beyond the original Phase-0 skeleton: apps, src, migrations, packaging, tests, scripts, evidence, contracts, baseline exports, and phase records must all remain discoverable in the maintained repository map.
- Evidence location: .agent/REPO_MAP.md; git ls-files; docs/phase15-remediation-qualification-ledger.yaml.
- Confidence: VERIFIED
- Scope: Repository navigation and governance maintenance.
- Supersedes learning: none

## L-PRIME-PHASE15-003

- Date: 2026-08-10
- Learning ID: L-PRIME-PHASE15-003
- Fact or lesson: A skipped PostgreSQL integration test is not release evidence; it must retain its affected requirement mapping, exact missing environment, release-blocking effect, and deterministic qualification method until exercised.
- Evidence location: docs/phase15-skipped-test-inventory.md; Continuation 005 qualification directive.
- Confidence: VERIFIED
- Scope: Phase-15 skipped-test handling and all requirement-level release decisions.
- Supersedes learning: none

## L-PRIME-PHASE15-004

- Date: 2026-08-10
- Learning ID: L-PRIME-PHASE15-004
- Fact or lesson: Evidence metadata and retraction can be implemented locally without proving R-046/R-047; PostgreSQL migration, parser/index, citation, backup/restore, and live project-isolation evidence remain separate qualification obligations.
- Evidence location: evidence/phase15/R-046-R-047-implementation-preflight.md; src/prime_core/history_service.py; migrations/prime/0015_evidence_lifecycle.sql.
- Confidence: VERIFIED
- Scope: R-046/R-047 implementation and Phase-15 evidence qualification.
- Supersedes learning: none

## L-PRIME-PHASE15-005

- Date: 2026-08-11
- Learning ID: L-PRIME-PHASE15-005
- Fact or lesson: A Git bundle created directly from a live repository can be empty when the selected checkpoint is still reachable from a normal ref. PRIME checkpoint preservation must pack the selected commit graph into an isolated temporary object store before creating the retained bundle, and must verify the retained hash/status independently after ref removal and GC.
- Evidence location: src/prime_core/git_history.py; tests/phase11/test_history_primitives.py; evidence/phase15/R-049-git-checkpoint-implementation.md
- Confidence: VERIFIED
- Scope: R-049 Git checkpoint preservation and Time Lens historical storage.
- Supersedes learning: none

## L-PRIME-PHASE15-006

- Date: 2026-08-11
- Learning ID: L-PRIME-PHASE15-006
- Fact or lesson: A historical Git selector cannot safely include Evidence merely because it exists today. Evidence must carry an explicit source revision association; otherwise Time Lens must exclude it at that commit and report missing source truth rather than infer historical availability.
- Evidence location: migrations/prime/0016_historical_evidence.sql; src/prime_core/history_service.py; tests/phase11/test_history.py
- Confidence: VERIFIED
- Scope: R-046–R-050 Evidence provenance, Time Lens cutoff fidelity, and historical Ask.
- Supersedes learning: L-PRIME-PHASE15-004

## L-PRIME-PHASE15-007

- Date: 2026-08-11
- Learning ID: L-PRIME-PHASE15-007
- Fact or lesson: Historical lifecycle evidence must be append-only at the event-observation boundary. A unique key containing only artifact identity and source revision would overwrite the original fact when a later retraction/correction occurs; lifecycle snapshots must include the observation timestamp and use conflict-safe insertion.
- Evidence location: migrations/prime/0018_historical_snapshot_immutability.sql; src/prime_core/history_primitives.py; tests/phase11/test_history.py
- Confidence: VERIFIED
- Scope: R-047/R-048 citation mutation, Evidence retraction, memory correction, Notion projection, and Time Lens reconstruction.
- Supersedes learning: none

## L-PRIME-PHASE15-008

- Date: 2026-08-11
- Learning ID: L-PRIME-PHASE15-008
- Fact or lesson: A PRIME continuity backup is a multi-component logical checkpoint, not a database dump. The recoverable artifact must preserve canonical PostgreSQL rows, managed Evidence bytes, retained PRIME-owned Git bundles, source-ledger rebuild inputs, configuration references, component hashes, and explicit fidelity/limitation labels while excluding secrets and repository-source claims.
- Evidence location: src/prime_core/backup_service.py; migrations/prime/0020_continuity_capacity.sql; evidence/phase15/R-042-R-045-implementation-closure-008.md
- Confidence: VERIFIED
- Scope: R-042–R-044 backup, restore, Hindsight continuity, Evidence, historical state, Git checkpoints, and recovery reporting.
- Supersedes learning: none

## L-PRIME-PHASE15-009

- Date: 2026-08-11
- Learning ID: L-PRIME-PHASE15-009
- Fact or lesson: Restoring managed Evidence or PRIME-owned Git bundles into a clean environment requires rewriting their restored storage locators; retaining the original source-host path makes metadata appear restored while content remains unavailable.
- Evidence location: src/prime_core/backup_service.py; the Continuation 008 clean-install fixture recorded in evidence/phase15/R-042-R-045-implementation-closure-008.md
- Confidence: VERIFIED
- Scope: R-043/R-044 restore semantics and R-046–R-050 backup regression protection.
- Supersedes learning: none

## L-PRIME-PHASE15-011

- Date: 2026-08-11
- Learning ID: L-PRIME-PHASE15-011
- Fact or lesson: Tailscale Serve lifecycle safety requires separate desired and actual state plus explicit PRIME ownership. A successful CLI invocation is not proof of active private access, and an unowned Serve reset can disrupt unrelated services; local implementation must fail closed while live tailnet evidence remains separate.
- Evidence location: src/prime_core/remote_access_service.py; tests/phase12/test_remote_access.py; evidence/phase15/R-035-R-036-implementation-closure-010.md
- Confidence: VERIFIED
- Scope: R-035/R-036 private remote access and operator-plane isolation.
- Supersedes learning: none

## L-PRIME-PHASE15-012

- Date: 2026-08-11
- Learning ID: L-PRIME-PHASE15-012
- Fact or lesson: Notion synchronization requires two separate provenance boundaries: managed Project Record projections are PRIME-owned and self-write-suppressed, while attached Knowledge Sources are explicit project-scoped read-only observations. Detach, access loss, or deletion must retract current retrieval and mark admitted memory for review without deleting historical provenance silently.
- Evidence location: `src/prime_core/notion_service.py`; `migrations/prime/0022_notion_lifecycle.sql`; `tests/phase7/test_notion_lifecycle.py`; `evidence/phase15/R-037-R-041-implementation-closure-011.md`
- Confidence: VERIFIED
- Scope: R-037–R-041 Notion lifecycle, project isolation, privacy/egress, documentation ordering, source provenance, and historical reconciliation.
- Supersedes learning: none

## L-PRIME-PHASE15-013

- Date: 2026-08-11
- Learning ID: L-PRIME-PHASE15-013
- Fact or lesson: A credential variable name is not a capability declaration. Safe integration reuse needs a durable non-secret reference to the existing runtime source, idempotent no-overwrite import semantics, actual granted-page read checks, and an explicit controlled write probe. Identity discovery alone must not mark Project Record managed writes available.
- Evidence location: `src/prime_core/notion_credentials.py`; `src/prime_core/notion_api.py`; `migrations/prime/0023_notion_credential_reference.sql`; `tests/phase7/test_notion_credentials.py`; `evidence/phase15/R-051-R-053-implementation-closure-012.md`
- Confidence: VERIFIED
- Scope: R-037–R-041 Notion authorization reuse, secret handling, capability reporting, backup metadata, and operator settings UX.
- Supersedes learning: none

## L-PRIME-PHASE15-014

- Date: 2026-08-11
- Learning ID: L-PRIME-PHASE15-014
- Fact or lesson: Operator UX state must be explicit and textual at every boundary. A responsive shell can remain truthful during authentication, empty, stale, degraded, offline, error, and needs-attention conditions only when it loads protected Core state with no-store semantics, keeps project selection below the UI, preserves project-scoped routes, and renders untrusted names through text nodes rather than HTML interpolation.
- Evidence location: `apps/web/index.html`; `apps/core/main.py`; `tests/phase14/test_web_shell.py`; `evidence/phase15/R-051-R-053-implementation-closure-012.md`
- Confidence: VERIFIED
- Scope: R-051–R-053 operator shell, accessibility, responsive behavior, degraded/recovery UX, project isolation, and destructive-action safety.
- Supersedes learning: none

## L-PRIME-PHASE15-015

- Date: 2026-08-11
- Learning ID: L-PRIME-PHASE15-015
- Fact or lesson: AI grounding requires both a durable source identity/revision set and bounded source content admitted as untrusted data. Provider identity, prompt instructions, or generic context labels are not evidence; Ask must validate citations against the exact admitted source set and return UNKNOWN when the provider or policy cannot safely execute.
- Evidence location: `src/prime_core/ai_service.py`; `src/prime_core/intelligence_service.py`; `migrations/prime/0024_ai_execution.sql`; `tests/phase15/test_ai_execution.py`; `evidence/phase15/R-054-R-055-implementation-closure-013.md`
- Confidence: VERIFIED
- Scope: R-054/R-055 AI profiles, source grounding, privacy/egress, citations, prompt injection, project isolation, and usage/provenance.
- Supersedes learning: none

## L-PRIME-PHASE15-016

- Date: 2026-08-11
- Learning ID: L-PRIME-PHASE15-016
- Fact or lesson: A local deterministic provider double proves Core boundary behavior but cannot establish approved provider or LOCAL_ONLY inference qualification. Live model evidence must retain provider/model/profile/prompt/schema/source/privacy revisions and remain a separate qualification result.
- Evidence location: `tests/phase15/test_ai_execution.py`; `docs/phase15-remediation-qualification-ledger.yaml`; `evidence/phase15/R-054-R-055-implementation-closure-013.md`
- Confidence: VERIFIED
- Scope: R-054/R-055 implementation-versus-qualification separation.
- Supersedes learning: none

## L-PRIME-PHASE15-017

- Date: 2026-08-11
- Learning ID: L-PRIME-PHASE15-017
- Fact or lesson: A qualification environment must be recreated from zero before database-backed evidence is trusted. The approved pgvector image provides the vector extension, but a new PostgreSQL database requires explicit `CREATE EXTENSION vector`; once enabled, the full PRIME migration chain applied idempotently through `0024_ai_execution.sql`. Database-backed regression also exposed a real AI persistence placeholder mismatch that unit-only provider tests could not see.
- Evidence location: `docker-compose.phase1.yml`; `evidence/phase15/qualification-continuation-015.md`; `src/prime_core/ai_service.py`; `migrations/prime/0024_ai_execution.sql`
- Confidence: VERIFIED
- Scope: Phase 1–13 database gates, AI execution persistence, migration qualification, and requirement-level Phase-15 evidence.
- Supersedes learning: none

## L-PRIME-PHASE15-018

- Date: 2026-08-11
- Learning ID: L-PRIME-PHASE15-018
- Fact or lesson: Historical Git qualification must distinguish a durable PRIME-owned checkpoint from ordinary repository reachability. After refs, reflogs, and unreachable objects are pruned, Time Lens may report repository `EXACT` only when the retained checkpoint bundle itself is intact; citation resolution must downgrade when that bundle is missing or partial and recover only after the retained artifact is restored.
- Evidence location: `src/prime_core/history_service.py`; `tests/phase15/test_requirement_qualification.py`; `evidence/phase15/qualification-continuation-016.md`
- Confidence: VERIFIED
- Scope: R-047–R-050 Git checkpoints, citations, Time Lens, historical reconstruction, and recovery semantics.
- Supersedes learning: none

## L-PRIME-PHASE15-019

- Date: 2026-08-11
- Learning ID: L-PRIME-PHASE15-019
- Fact or lesson: A citation linked to retracted Evidence is historical and must expose the retraction; a citation whose managed bytes were purged is `UNAVAILABLE`, not `EXACT`. Current revision/hash equality alone is insufficient to determine citation availability.
- Evidence location: `src/prime_core/history_service.py`; `tests/phase15/test_requirement_qualification.py`; `evidence/phase15/qualification-continuation-016.md`
- Confidence: VERIFIED
- Scope: R-046/R-047 Evidence lifecycle, citation durability, retraction, privacy purge, and project isolation.
- Supersedes learning: none

## L-PRIME-PHASE15-020

- Date: 2026-08-11
- Learning ID: L-PRIME-PHASE15-020
- Fact or lesson: Product-level Evidence qualification must admit the durable Evidence identity and SourceReference below the AI boundary. Search, Ask, Progress, and Documentation can each expose the same E1/S1 identity while retraction removes current retrieval and restore/reindex returns only when the exact bytes are present.
- Evidence location: `src/prime_core/intelligence_service.py`; `src/prime_core/progress_service.py`; `apps/core/main.py`; `tests/phase15/test_requirement_qualification.py`; `evidence/phase15/qualification-continuation-017.md`
- Confidence: VERIFIED
- Scope: R-046/R-047 product citations, Evidence provenance, retraction, restore, and project isolation.
- Supersedes learning: none

## L-PRIME-PHASE15-021

- Date: 2026-08-11
- Learning ID: L-PRIME-PHASE15-021
- Fact or lesson: Backup destination classification must compare filesystem device identity, not path anchors. Separate mounts share `/` as an anchor; device IDs are required to truthfully label an off-machine qualification target. Interrupted restore state must be committed outside the failed transaction so `REPAIR_REQUIRED` survives rollback.
- Evidence location: `src/prime_core/backup_service.py`; `tests/phase15/test_requirement_qualification.py`; `evidence/phase15/qualification-continuation-017.md`
- Confidence: VERIFIED
- Scope: R-042/R-043 Continuity-v2 destination, clean restore, interruption, and recovery semantics.
- Supersedes learning: none

## L-PRIME-PHASE15-022

- Date: 2026-08-11
- Learning ID: L-PRIME-PHASE15-022
- Fact or lesson: A local OpenAI-compatible model can satisfy PRIME's existing AI boundary without new architecture when the adapter is environment-backed, marks the provider local for LOCAL_ONLY policy, sends bounded untrusted-source context, parses only structured JSON, records usage/provenance, and never persists endpoint or key material. Provider outage and recovery must be qualified separately from model success.
- Evidence location: `src/prime_core/ai_service.py`; `tests/phase15/test_ai_execution.py`; `evidence/phase15/qualification-continuation-018.md`
- Confidence: VERIFIED
- Scope: R-054/R-055 local provider/profile, privacy, structured output, usage, outage/recovery, prompt-injection, project isolation, and secret-safety qualification.
- Supersedes learning: none

## L-PRIME-PHASE15-023

- Date: 2026-08-11
- Learning ID: L-PRIME-PHASE15-023
- Fact or lesson: A valid Notion credential removes the credential-environment blocker but does not prove PRIME's live documentation lifecycle. Read capability can be qualified safely against frozen pages; project-record writes, managed-region conflict/replay, Knowledge Source lifecycle, outage reconciliation, and history rollover require an explicitly controlled disposable target.
- Evidence location: `src/prime_core/notion_credentials.py`; `src/prime_core/notion_api.py`; `evidence/phase15/qualification-continuation-018.md`
- Confidence: VERIFIED
- Scope: R-037–R-041 Notion authentication, read capability, write safety, and remaining lifecycle qualification.
- Supersedes learning: none

## L-PRIME-PHASE15-024

- Date: 2026-08-12
- Learning ID: L-PRIME-PHASE15-024
- Fact or lesson: Live local-model qualification is sensitive to provider concurrency and output-shape drift. Explicit per-function schema instructions plus exact admitted-source citation rules allow the existing Core boundary to accept real Goal, Progress, Alignment, Documentation, Ask, and memory results without introducing a second provider architecture; controlled serial retries distinguish provider rate limiting from product failure.
- Evidence location: `src/prime_core/ai_service.py`; `scripts/phase15_qualify_continuation_019.py`; `evidence/phase15/qualification-continuation-019.md`
- Confidence: VERIFIED
- Scope: R-055 Paragon cross-surface execution, structured output, source citation, rate-limit/degraded handling, and recovery.
- Supersedes learning: none

## L-PRIME-PHASE15-025

- Date: 2026-08-12
- Learning ID: L-PRIME-PHASE15-025
- Fact or lesson: Connected Notion write capability can be safely established without mutating canonical PRIME content by using a standalone qualification page and disposable child source. Create/read/update, managed-region preservation, and source revision refresh are useful capability evidence, but they do not substitute for exercising the local PRIME Notion adapter's project binding, reconciliation, and history lifecycle.
- Evidence location: `evidence/phase15/qualification-continuation-019.md`; disposable page identity is recorded there.
- Confidence: VERIFIED
- Scope: R-037–R-041 Notion write capability, managed-region ownership, source refresh, and lifecycle evidence boundaries.
- Supersedes learning: L-PRIME-PHASE15-023

## L-PRIME-PHASE15-026

- Date: 2026-08-12
- Learning ID: L-PRIME-PHASE15-026
- Fact or lesson: The integrated AI acceptance boundary must be exercised through IntelligenceService, not only AIExecutionService. The product path must preserve durable ai_runs identity, admitted source sets, citations, managed Documentation projection, and memory correction history. A live invalid citation must reject the complete result before projection; silently dropping the citation would violate the frozen contract.
- Evidence location: `src/prime_core/intelligence_service.py`; `src/prime_core/memory_service.py`; `scripts/phase15_qualify_continuation_020.py`; `evidence/phase15/qualification-continuation-020.md`
- Confidence: VERIFIED
- Scope: R-055 integrated product AI lifecycle, projection, citation validation, correction/supersession, and provenance.
- Supersedes learning: none

## L-PRIME-PHASE15-027

- Date: 2026-08-12
- Learning ID: L-PRIME-PHASE15-027
- Fact or lesson: Notion search is relevance-ranked, not an exact idempotency lookup. PRIME must fetch candidate pages and require an exact internal marker before recovering an ambiguous create; otherwise Project A/B can bind to the same remote page. Live qualification also requires a non-archived disposable parent: read authorization alone cannot create a page under an archived target.
- Evidence location: `src/prime_core/notion_service.py`; `src/prime_core/notion_api.py`; `evidence/phase15/qualification-continuation-020.md`
- Confidence: VERIFIED
- Scope: R-037–R-041 production Notion adapter idempotency, isolation, and live write qualification.
- Supersedes learning: L-PRIME-PHASE15-025

## L-PRIME-PHASE15-028

- Date: 2026-08-12
- Learning ID: L-PRIME-PHASE15-028
- Fact or lesson: ANIMUS PRIME's full regression is database-state sensitive. The default environment ran 61 passed and 25 skipped because database variables were unset; the existing populated disposable database ran 83 passed and 3 deterministic state-collision failures. Those failures are not equivalent to a fresh qualification run and must not be used to replace the recorded fresh 86-pass Continuation 020 evidence. A future rerun must use a newly recreated disposable database and record the reset explicitly.
- Evidence location: `.agent/OUTCOMES.md`; `tests/phase1/test_core.py`; `tests/phase4/test_indexer.py`; `tests/phase9/test_intelligence.py`; `evidence/phase15/qualification-continuation-020.md`
- Confidence: VERIFIED
- Scope: qualification execution, database isolation, and takeover verification.
- Supersedes learning: none

## L-PRIME-PHASE15-029

- Date: 2026-08-12
- Learning ID: L-PRIME-PHASE15-029
- Fact or lesson: A static PRIME shell is not a qualified product. Browser qualification found the global CSP blocking the inline shell, and after a per-response nonce fix the real operator path verified Home, project snapshot state, normalized Since You Were Here recap/advance, safe UNKNOWN Ask output, grouped Search empty state, derived-only Brain unavailable state, and Time Lens controls. Product alignment must classify frozen §26 items from exercised user paths, not headings or backend symbols.
- Evidence location: `apps/core/main.py`; `apps/web/index.html`; `docs/v1-product-goal-alignment-audit.yaml`; `evidence/phase15/product-goal-alignment-continuation-028.md`
- Confidence: VERIFIED
- Scope: Continuation 028 product-goal alignment, CSP serving boundary, Home and Since You Were Here qualification.
- Supersedes learning: none

## L-PRIME-PHASE15-030

- Date: 2026-08-12
- Learning ID: L-PRIME-PHASE15-030
- Fact or lesson: A durable project handoff must be qualified through production Core services with real Git-backed repository state, approved goal identity, authority health, progress history, evidence, memory provenance, activity, integration metadata, and explicit Project A/B isolation. On Windows SSHFS, Python bytecode and gstack session writes can fail even when source access works, so qualification must use the active interpreter and a local writable browser-session directory without changing the authoritative Atlas checkout.
- Evidence location: `scripts/seed_product_completion_029.py`; `tests/phase0/test_harness.py`; `evidence/phase15/product-goal-alignment-continuation-029.md`
- Confidence: VERIFIED
- Scope: Continuation 029 fixture durability, interpreter portability, browser qualification, project context export, and Atlas SSHFS environment boundary.
- Supersedes learning: none

## L-PRIME-PHASE15-031

- Date: 2026-08-12
- Learning ID: L-PRIME-PHASE15-031
- Fact or lesson: Frozen §26 audit rows that specify architecture or security invariants can be PRODUCT_VERIFIED when the invariant is exercised and evidenced through production boundaries, even when no dedicated screen is required. This does not turn the remaining user-facing workflows into verified product behavior and must not move the V1 release gate while other rows remain incomplete.
- Evidence location: `docs/v1-product-goal-alignment-audit.yaml`; `evidence/phase15/product-goal-alignment-continuation-029.md`
- Confidence: VERIFIED
- Scope: DOD-003, DOD-010, DOD-025, DOD-029, DOD-046, DOD-072, and DOD-078 audit classification.
- Supersedes learning: none

## L-PRIME-PHASE15-032

- Date: 2026-08-12
- Learning ID: L-PRIME-PHASE15-032
- Fact or lesson: Onboarding must treat an enrolled Node root as a real security boundary: an approved-root child can be created and bound, while a parent outside the enrolled root is rejected before mutation. A newly initialized repository is valid Git state but has no `HEAD`; handoff and export must report `UNBORN`, not `UNAVAILABLE`. Fresh browser qualification also requires a local writable session directory when the authoritative Atlas SSHFS checkout cannot accept browser artifacts.
- Evidence location: `src/prime_core/service.py`; `apps/core/main.py`; `evidence/phase15/product-goal-alignment-continuation-030.md`
- Confidence: VERIFIED
- Scope: Continuation 030 repository onboarding, Git identity, browser export, and Atlas SSHFS boundary.
- Supersedes learning: none
## L-PRIME-PHASE15-033

- Date: 2026-08-12
- Learning ID: L-PRIME-PHASE15-033
- Fact or lesson: A product implementation must expose its durable lifecycle identity at the API boundary before browser qualification can prove restart/resume. GoalModel baseline, progress assessment, source revision, and freshness are separate persisted facts; an opaque percentage or a shell control is not evidence of a complete workflow.
- Evidence location: `src/prime_core/progress_service.py`; `src/prime_core/indexer.py`; `apps/core/main.py`; `evidence/phase15/product-goal-alignment-continuation-031.md`
- Confidence: VERIFIED
- Scope: Continuation 031 GoalModel/progress and freshness implementation slice.
- Supersedes learning: none

## L-PRIME-PHASE15-034

- Date: 2026-08-12
- Learning ID: L-PRIME-PHASE15-034
- Fact or lesson: Fork safety requires a clean committed source revision, approved destination root, safe archive extraction, explicit new identity, and explicit non-copy provenance. Creating a UI form or database fork row without these boundaries is not a fork qualification.
- Evidence location: `src/prime_core/service.py`; `migrations/prime/0026_product_completion_wave3.sql`; `tests/phase15/test_product_completion_031.py`; `evidence/phase15/product-goal-alignment-continuation-031.md`
- Confidence: VERIFIED
- Scope: Continuation 031 Fork/Clone implementation slice.
- Supersedes learning: none

## L-PRIME-PHASE15-035

- Date: 2026-08-12
- Learning ID: L-PRIME-PHASE15-035
- Fact or lesson: The fresh Continuation 032 startup block was environmental, not a migration defect: a zero-state PostgreSQL 17.10/pgvector 0.8.2 database applied all 26 migrations, Core lifespan startup completed, and Core restart remained healthy. Separately, PostgreSQL can reject a nullable project-scope parameter used in `%s IS NULL` with `IndeterminateDatatype`; branching the query for the nullable and non-null cases is the narrow type-safe repair.
- Evidence location: `docker compose -p prime032 -f docker-compose.phase1.yml`; `src/prime_core/mcp_service.py`; `tests/phase15/test_product_completion_032.py`; `evidence/phase15/product-goal-alignment-continuation-032.md`
- Confidence: VERIFIED
- Scope: Continuation 032 fresh startup diagnosis and project-scoped AI grant revocation.
- Supersedes learning: none

## L-PRIME-PHASE15-036

- Date: 2026-08-12
- Learning ID: L-PRIME-PHASE15-036
- Fact or lesson: Selected-revision Fork/Clone safety depends on both a clean committed source tree and the required authority package being present in the selected revision; later authority files do not retroactively make an earlier revision forkable. Successful fork evidence must also prove distinct project-scoped memory/progress/grant state and explicit non-copy provenance.
- Evidence location: `src/prime_core/service.py`; `evidence/phase15/product-goal-alignment-continuation-032.md`
- Confidence: VERIFIED
- Scope: Continuation 032 selected-revision fork and A/B isolation qualification.
- Supersedes learning: none

- 2026-08-12 — Atlas-native qualification: direct SSH to `/home/sketch/Projects/ANIMUS_PRIME` avoids the malformed SSHFS/`Z:\` doubled path and avoids Z: bind mounts for Docker. A native bind mount still exposes worktree file modes; the existing uncommitted 660 migration files are unreadable to the image's `nobody` user, so the safe qualification workaround was a root-owned disposable process without changing the user's files.
- 2026-08-12 — Git bundle verification requires repository context: verify a bundle through a disposable bare Git directory, not a context-free `git bundle verify` invocation.
- 2026-08-12 — Progress qualification must enforce the approved GoalModel contract: required evidence-bearing items cannot claim non-zero completion without evidence, and approved item weights must be applied when result payloads omit weight.
- 2026-08-13 — A clean checkout of the published tip is the decisive packaging test: committed migration mode 664 is readable by the normal Core image user `nobody`, so the long-lived uncommitted mode-660 condition is development-worktree permission contamination, not a packaging defect.
- 2026-08-13 — Direct SSH makes Atlas Linux reality inspectable, but a running systemd host and sudo membership do not prove PRIME native Node qualification. The repository must expose a deterministic installer/unit and lifecycle evidence; none was present in the current Node surfaces.
- 2026-08-13 — Browser fixture qualification must mount the fixture path into the Core process with matching permissions. Indexed metadata can render while Repository/Git drill-down fails if the Core container cannot traverse the host-side fixture or cannot perform read-only Git inspection.
- 2026-08-13 — A derived burndown is only actionable when every open DOD has exact residual behavior, explicit work class, environment flags, evidence already available, qualification needed, blocker, and dependency fields that mechanically match the authoritative audit.


## L-PRIME-PHASE15-037

- Date: 2026-08-13
- Learning ID: L-PRIME-PHASE15-037
- Fact or lesson: Native Atlas qualification exposed two distinct continuity boundaries: the ordinary pytest collision is deterministically repaired with importlib collection, and project-scoped browser state must be cleared when changing projects or stale Brain data remains visible. Hindsight is listening on port 8888, while PRIME's default adapter still targets 18888; correcting that endpoint alone is insufficient because the configured routerbot-local retain extractor acknowledges requests but currently extracts zero recallable facts.
- Evidence location: pytest.ini; apps/web/index.html; src/prime_core/memory_service.py; evidence/phase15/product-goal-alignment-continuation-035.md
- Confidence: VERIFIED
- Scope: Continuation 035 test contract, browser A/B state isolation, and Hindsight diagnosis.
- Supersedes learning: none

- `L-PRIME-PHASE15-038` — The Hindsight service topology is a configuration contract, not an adapter constant. The Atlas service listens on 127.0.0.1:8888; PRIME now reads `PRIME_HINDSIGHT_BASE_URL` through Settings and uses a configurable timeout. A 10-second client timeout caused a false unavailable result while Hindsight was still extracting and storing a fact in about 13.7 seconds. Durable retain remains CURRENT only after recall returns a result.
- `L-PRIME-PHASE15-039` — Historical repository revisions and Goal hashes are different identities. Direct historical revision selection must reconstruct the Goal revision observed before that repository revision; otherwise Time Lens reports a historical repository while silently losing the valid Goal.
    
## L-PRIME-PHASE15-040

- Date: 2026-08-13
- Learning ID: L-PRIME-PHASE15-040
- Fact or lesson: Hindsight recovery is a PRIME source-ledger replay with explicit SOURCE_LEDGER_REBUILD and REBUILDABLE_NOT_BIT_IDENTICAL fidelity, not a backend bit-identical Hindsight restore. Superseded and tombstoned ledger rows must be excluded from the current rebuild.
- Evidence location: evidence/phase15/qualification-continuation-037.md; src/prime_core/memory_service.py; scripts/phase15_qualify_continuation_037.py
- Confidence: VERIFIED
- Scope: R-044 and DOD-067/DOD-068/DOD-069/DOD-070 on native Atlas.
- Supersedes learning: none

## L-PRIME-PHASE15-041

- Date: 2026-08-13
- Learning ID: L-PRIME-PHASE15-041
- Fact or lesson: Browser path fields can be client-normalized incorrectly when a Windows-origin path is submitted to native Atlas; the observed failure prepended C: to an Atlas destination path. Direct native/API qualification remains valid, but browser Fork cannot be promoted until the boundary is repaired.
- Evidence location: evidence/phase15/qualification-continuation-037.md; authenticated browser Fork attempt during Continuation 037
- Confidence: VERIFIED
- Scope: DOD-016/DOD-017 and native Atlas browser tunnel.
- Supersedes learning: none

## L-PRIME-PHASE15-042

- Date: 2026-08-13
- Learning ID: L-PRIME-PHASE15-042
- Fact or lesson: When the Hindsight provider is unavailable, PRIME must report UNAVAILABLE/degraded state while canonical PRIME PostgreSQL state remains queryable; recovery can rebuild from the source ledger without claiming exact Hindsight identity.
- Evidence location: evidence/phase15/qualification-continuation-037.md; scripts/phase15_qualify_continuation_037.py
- Confidence: VERIFIED
- Scope: R-044 external-component failure and recovery contract.
- Supersedes learning: none

## L-PRIME-PHASE15-043

- Date: 2026-08-13
- Learning ID: L-PRIME-PHASE15-043
- Fact or lesson: Git Bash/MSYS path conversion can mutate a native Atlas Linux path before the browser receives it. Browser CLI path tests must set `MSYS_NO_PATHCONV=1`; PRIME should preserve opaque Node paths and must not accept a client-local `C:/Users/...` mutation as an Atlas path.
- Evidence location: evidence/phase15/qualification-continuation-038.md; tests/phase15/test_product_completion_031.py
- Confidence: VERIFIED
- Scope: DOD-016/DOD-017 native Atlas browser-to-Node path contract.
- Supersedes learning: L-PRIME-PHASE15-041

## L-PRIME-PHASE15-044

- Date: 2026-08-13
- Learning ID: L-PRIME-PHASE15-044
- Fact or lesson: Burndown header totals are derived state and must be validator-enforced against the authoritative audit row set, including duplicate, complete-row, missing-row, status, acceptance-kind, and work-class invariants.
- Evidence location: docs/v1-product-gap-burndown.yaml; scripts/validate_product_gap_burndown.py; tests/phase15/test_product_gap_burndown.py; evidence/phase15/qualification-continuation-038.md
- Confidence: VERIFIED
- Scope: V1 product-gap governance.
- Supersedes learning: none

## L-PRIME-PHASE15-045

- Date: 2026-08-13
- Learning ID: L-PRIME-PHASE15-045
- Fact or lesson: The approved Hindsight reflect/Mental Models path currently starts through `openai/routerbot-local` but does not complete within the bounded adapter call, so PRIME must keep the result UNAVAILABLE and DOD-068 open.
- Evidence location: evidence/phase15/qualification-continuation-038.md; Atlas Hindsight service logs observed during Continuation 038
- Confidence: VERIFIED
- Scope: DOD-068 approved Hindsight reflect/provider qualification.
- Supersedes learning: none

## L-PRIME-PHASE15-046

- Date: 2026-08-13
- Learning ID: L-PRIME-PHASE15-046
- Fact or lesson: A reusable qualification fixture must keep one current durable ledger fact while storing correction seeds and tombstoned corrections as separate rows; otherwise a correction test can accidentally leave recall with no current fact.
- Evidence location: `scripts/phase15_qualify_continuation_039.py`; `evidence/phase15/qualification-continuation-039.md`
- Confidence: VERIFIED
- Scope: Continuation 039 fixture construction and PRIME/Hindsight qualification.
- Supersedes learning: none

## L-PRIME-PHASE15-047

- Date: 2026-08-13
- Learning ID: L-PRIME-PHASE15-047
- Fact or lesson: Project-scoped browser state must clear query, filter, custom historical boundary, source selection, selected node, and detail panes when the active project changes or a filter removes the selected node.
- Evidence location: `apps/web/index.html`; `evidence/phase15/qualification-continuation-039.md`
- Confidence: VERIFIED
- Scope: Wave 3 Brain and project-switch browser behavior.
- Supersedes learning: none

## L-PRIME-PHASE15-048

- Date: 2026-08-13
- Learning ID: L-PRIME-PHASE15-048
- Fact or lesson: The approved local Hindsight provider can complete fixture retain/recall but the bounded `PrimeMemoryAdapter.reflect()` call still returns `UNAVAILABLE`; retain/recall success must not be generalized into reflect or Mental Models qualification.
- Evidence location: `scripts/phase15_reflect_probe_039.py`; `evidence/phase15/qualification-continuation-039.md`
- Confidence: VERIFIED
- Scope: DOD-068 approved Hindsight reflect/provider qualification.
- Supersedes learning: L-PRIME-PHASE15-045
