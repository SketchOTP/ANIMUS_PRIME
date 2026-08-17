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

## L-PRIME-PHASE15-049

- Date: 2026-08-13
- Learning ID: L-PRIME-PHASE15-049
- Fact or lesson: Fork authority must be provisioned from the current versioned template after cloning the selected committed revision; copying the parent's `.agent` and replacing Git history with one synthetic commit creates a false child boundary. The child goal is intentionally DRAFT until explicit approval.
- Evidence location: `src/prime_core/service.py`; `scripts/phase15_fork_qualification_continuation_040.py`; `evidence/phase15/qualification-continuation-040.md`
- Confidence: VERIFIED
- Scope: DOD-016/DOD-017 Fork/Clone authority and history boundary.
- Supersedes learning: none

## L-PRIME-PHASE15-050

- Date: 2026-08-13
- Learning ID: L-PRIME-PHASE15-050
- Fact or lesson: gstack browser qualification must run from a local Windows filesystem working directory when the app is served through an Atlas SSH tunnel; invoking it from the Z: SSHFS checkout causes the browser harness to attempt a nested malformed path and reproduces the original ENOENT/EPERM class of failure.
- Evidence location: `evidence/phase15/qualification-continuation-040.md`; Atlas direct-SSH/browser qualification log
- Confidence: VERIFIED
- Scope: Atlas execution and browser qualification routing.
- Supersedes learning: none

## L-PRIME-CONTINUATION-041

- Date: 2026-08-13
- Learning ID: L-PRIME-CONTINUATION-041
- Fact or lesson: The authoritative ANIMUS PRIME qualification path is direct Atlas SSH at /home/sketch/Projects/ANIMUS_PRIME; browser access may use an SSH transport tunnel, but no disposable runtime or test environment is required for this path.
- Evidence location: evidence/phase15/qualification-continuation-041.md; docs/v1-product-goal-alignment-audit.yaml.
- Confidence: VERIFIED
- Scope: Atlas-native continuation qualification.
- Supersedes learning: none

## 2026-08-13 — L-PRIME-042-COUNT-AND-ATLAS-MCP

- Learning ID: L-PRIME-042-COUNT-AND-ATLAS-MCP
- Fact or lesson: Continuation 041 governed totals were 24 complete and 57 open; its §26 audit BACKEND_ONLY count was 27 and burndown EXTERNAL_ENVIRONMENT was 23. The discrepancy was summary-text confusion. Native MCP qualification requires preserving source/provenance and working-context metadata through the public mapping, with the real Atlas persistent database target explicitly configured.
- Evidence location: evidence/phase15/qualification-continuation-042.md; 505ba76b05b0528f27d60c9bfb39da582778bc88; docs/v1-product-gap-burndown.yaml; scripts/validate_product_gap_burndown.py
- Confidence: HIGH
- Scope: ANIMUS PRIME native Atlas execution and governed Phase 15 qualification
- Supersedes learning: None

## L-PRIME-CONTINUATION-043

- Date: 2026-08-13
- Learning ID: L-PRIME-CONTINUATION-043
- Fact or lesson: Repository-only emergency recovery is safe when regeneration caches are copied to a positively identified external filesystem, source/archive checksums match, and only then are bounded cache paths removed. PostgreSQL recovered automatically after the existing container restarted.
- Evidence location: /mnt/storage1tb/project-archives/ANIMUS_PRIME/2026-08-13; evidence/phase15/qualification-continuation-043.md
- Confidence: VERIFIED

## L-PRIME-CONTINUATION-044

- Date: 2026-08-13
- Learning ID: L-PRIME-CONTINUATION-044
- Fact or lesson: Automatic authority admission must observe only the post-baseline ledger delta, parse every logical record in that delta, and reuse source references before emitting a deduplicated event. Otherwise persistent re-observation creates unique-key failures or turns DOD-030 into uncontrolled warm start.
- Evidence location: src/prime_core/authority_memory_admission.py; tests/phase15/test_authority_memory_admission.py; persistent Atlas index response for project_d9a1a5b609394282b62fc12c0d04634d
- Confidence: VERIFIED
- Scope: PRIME Hindsight adapter and future authority memory writes.
- Supersedes learning: none

## L-PRIME-CONTINUATION-045

- Date: 2026-08-13
- Learning ID: L-PRIME-CONTINUATION-045
- Fact or lesson: Frozen §26 reconciliation must precede score changes. Historical .agent records are validated by identified legacy schema signatures, while new entries use the current schema; no historical text rewrite is needed.
- Evidence location: scripts/validate_governance.py; evidence/phase15/qualification-continuation-045.md; GitHub publication.
- Confidence: VERIFIED
- Scope: ANIMUS PRIME governance and requirement qualification.
- Supersedes learning: none
## L-PRIME-CONTINUATION-046

- Date: 2026-08-14
- Learning ID: L-PRIME-CONTINUATION-046
- Fact or lesson: Incremental repository qualification must carry changed relative paths and a Git revision, reject stale ancestry and diverged revisions before projection, mark deleted current rows stale while preserving historical rows, and filter retrieval to current rows. A full recursive scan remains an explicit rebuild path, not the change-observation path.
- Evidence location: src/prime_core/indexer.py; apps/core/main.py; tests/phase4/test_incremental_observation.py; evidence/phase15/qualification-continuation-046.md
- Confidence: VERIFIED
- Scope: PRIME repository observation/index projection and section-26.61 qualification.
- Supersedes learning: none

## L-PRIME-CONTINUATION-047

- Date: 2026-08-14
- Learning ID: L-PRIME-CONTINUATION-047
- Fact or lesson: Incremental repository observation must validate caller revision against the actual checked-out HEAD, distinguish committed canonical bytes from dirty working-tree bytes, preserve branch/path/hash provenance, and avoid automatic authority admission for dirty bytes. Persistent Hindsight authority admission is real but can be slow because retain/recall/consolidation runs against large ledger content; qualification must capture completion rather than infer it from health alone.
- Evidence location: src/prime_core/indexer.py; migrations/prime/0028_incremental_observation_provenance.sql; evidence/phase15/qualification-continuation-047.md; persistent project_d9a1a5b609394282b62fc12c0d04634d.
- Confidence: VERIFIED
- Scope: PRIME repository observation, Progress freshness, automatic authority admission, and persistent Atlas qualification.
- Supersedes learning: none


## L-PRIME-CONTINUATION-048

- Date: 2026-08-14
- Learning ID: L-PRIME-CONTINUATION-048
- Fact or lesson: Direct Atlas qualification found that Git --git-common-dir can be relative to the inspected candidate path. Resolving it against the reported repository top-level creates a false identity for subdirectory inspection; Core and Node now resolve it against the candidate. Progress correction source references must be project-bound before a correction is durable. Node lifecycle security events are durable only when the state ledger retains non-secret event metadata; credential digests remain the only credential representation. DOD-037 cannot be promoted from branch name/main alone; canonical acceptance needs an explicit configured ref/event relationship.
- Evidence location: src/prime_core/progress_service.py; src/prime_core/service.py; src/prime_node/service.py; evidence/phase15/qualification-continuation-048.md; persistent Atlas qualification project.
- Confidence: VERIFIED
- Scope: PRIME provenance, Node security lifecycle, repository identity, and Continuation 048 qualification.
- Supersedes learning: none

## L-PRIME-CONTINUATION-049

- Date: 2026-08-14
- Learning ID: L-PRIME-CONTINUATION-049
- Fact or lesson: The DOD-045 operator-session boundary is distinct from DOD-008 break-glass recovery and must not inherit its unavailable replay evidence. Canonical Git truth must persist an explicit fully qualified ref and resolved commit independently of the active worktree; Git graph plus dirty state supports fail-closed acceptance classifications. Memory capture should preserve canonical, active, worktree, and acceptance-overlay provenance without rewriting historical records. Authority migration must expose CURRENT, LEGACY, CONFLICT, and NONE states, require confirmation for recognized legacy migration, and leave malformed/conflicting input for review.
- Evidence location: src/prime_core/git_provenance.py; src/prime_core/authority.py; src/prime_core/service.py; src/prime_core/memory_service.py; src/prime_core/mcp_service.py; apps/core/main.py; scripts/phase15_qualify_continuation_049.py; evidence/phase15/qualification-continuation-049.md; persistent project_d9a1a5b609394282b62fc12c0d04634d.
- Confidence: VERIFIED
- Scope: PRIME authentication boundary, canonical Git provenance, memory provenance, authority migration, and direct Atlas qualification.
- Supersedes learning: none

## L-PRIME-CONTINUATION-050

- Date: 2026-08-14
- Learning ID: L-PRIME-CONTINUATION-050
- Fact or lesson: Repository relocation must preserve logical continuity through stable project_id and repository_id, explicit canonical ref/commit/tree and authority evidence, and a location fingerprint that is only candidate evidence rather than identity. A non-mutating preflight plus explicit confirmation, stale detection, transactionally recorded history, and fail-closed refusal is safer than inventing a cutover when no legitimate alternate exists. Durable workflows need per-step replay policy, resource references, resume decisions, and REPAIR_REQUIRED for ambiguous non-idempotent effects; this supports resumability but does not prove exactly-once execution. CREATE_REPOSITORY is checkpointed; fork/provider/restore/archive paths remain to be converted and qualified.
- Evidence location: src/prime_core/git_provenance.py; src/prime_core/service.py; src/prime_core/workflow_primitives.py; migrations/prime/0030_rebind_and_workflow_steps.sql; tests/phase15/test_continuation050.py; scripts/phase15_qualify_continuation_050.py; evidence/phase15/qualification-continuation-050.md; persistent project_d9a1a5b609394282b62fc12c0d04634d.
- Confidence: VERIFIED
- Scope: PRIME repository continuity, relocation safety, durable workflow checkpoints, replay/resume policy, and direct Atlas qualification.
- Supersedes learning: none

## L-PRIME-CONVERGENCE-RESET-052

- Date: 2026-08-14
- Learning ID: L-PRIME-CONVERGENCE-RESET-052
- Fact or lesson: A persistent PostgreSQL/Hindsight substrate and backend continuity checks do not constitute a running PRIME product. Other Atlas listeners must not be mistaken for PRIME Core/UI. When Core is unavailable, keep source lifecycle and offline-node continuity bounded, park qualification-edge architecture, and require explicit authorization before starting the persistent PRIME runtime.
- Evidence location: evidence/phase15/qualification-continuation-052.md; .agent/CURRENT.md; direct Atlas listener/container inspection.
- Confidence: VERIFIED
- Scope: PRIME Phase 15 prioritization, persistent Atlas runtime readiness, source lifecycle, and offline Node qualification.
- Supersedes learning: none

## L-PRIME-PERSISTENT-RUNTIME-053

- Date: 2026-08-14
- Learning ID: L-PRIME-PERSISTENT-RUNTIME-053
- Fact or lesson: The supported V1 topology serves the genuine Web UI from the PRIME Core process, so a second Web server is unnecessary. A PRIME-owned user-level systemd service can manage one persistent Core container against the existing PostgreSQL/Hindsight without recreating qualification dependencies. Source files with owner-only modes can break a non-root Docker image at import time; normalizing application read/execute permissions in the image preserves the non-root contract. An enrolled Node database row is not a live Node process, and the packaged Node must remain stopped when approved mTLS material is absent; the disposable-only insecure HTTP override is not an acceptable persistent workaround.
- Evidence location: Dockerfile.core; packaging/core/prime-core.service; evidence/phase15/qualification-continuation-053.md; direct Atlas service/listener/container inspection.
- Confidence: VERIFIED
- Scope: PRIME persistent Core/UI runtime, Atlas service ownership, Docker packaging, and Node security boundary.
- Supersedes learning: L-PRIME-CONVERGENCE-RESET-052

## L-PRIME-OPERATOR-RECOVERY-054

- Date: 2026-08-14
- Learning ID: L-PRIME-OPERATOR-RECOVERY-054
- Fact or lesson: When the original one-time recovery reference is absent, a single-operator installation can regain access without an SQL credential edit by adding a nullable local-recovery digest, restricting recovery endpoints to loopback, requiring a high-entropy host-held secret, rotating both recovery references, revoking sessions, and recording audit metadata. This does not replace the need for a complete operator-facing recovery and step-up qualification. A database Node enrollment row and a packaged Node client are not a governed mTLS lifecycle; without approved CA/certificate material and Core wiring, Node startup must remain blocked.
- Evidence location: migrations/prime/0031_local_recovery.sql; src/prime_core/service.py; apps/core/main.py; packaging/core/local-recovery.sh; tests/phase1/test_local_recovery.py; evidence/phase15/qualification-continuation-054.md.
- Confidence: VERIFIED
- Scope: PRIME single-operator recovery, session security, Atlas persistent runtime, and Node activation boundary.
- Supersedes learning: L-PRIME-PERSISTENT-RUNTIME-053

## L-PRIME-NODE-TRUST-LIFECYCLE-055

- Date: 2026-08-14
- Learning ID: L-PRIME-NODE-TRUST-LIFECYCLE-055
- Fact or lesson: A database Node row is not an enrolled control-plane identity. The governed lifecycle must issue a short-lived Core-signed bootstrap proof, accept a one-use CSR proof from the canonical Node, require authenticated operator approval, deliver the CA-signed certificate and bearer credential over mTLS, and retain only secure credential references. Rotation, revocation, re-enrollment, and restart recovery must use the same stable Node identity; when the Node is offline, Core must preserve persisted project state but fail Node-required repository operations closed.
- Evidence location: src/prime_core/node_trust.py; src/prime_core/service.py; src/prime_node/service.py; migrations/prime/0032_node_trust_lifecycle.sql; packaging/node; evidence/phase15/qualification-continuation-055.md.
- Confidence: VERIFIED
- Scope: PRIME Core/Node private Atlas control plane and browser operator continuity.
- Supersedes learning: L-PRIME-OPERATOR-RECOVERY-054

## L-PRIME-LOCAL-CONVERGENCE-056

- Date: 2026-08-14
- Learning ID: L-PRIME-LOCAL-CONVERGENCE-056
- Fact or lesson: A persistent recovery control is not operator-qualified until the real Core-served UI exposes a secret-safe recovery path and high-risk actions require recent step-up authentication. Backup restore now fails closed without recent step-up. Source retraction must stale the current Documentation projection while retaining the previous projection as historical provenance. DOD-005 remains a local direct-qualification item even when live Notion is unavailable; external integration absence must not be used to inflate or block the exact local invariant.
- Evidence location: migrations/prime/0033_step_up_authentication.sql; apps/core/main.py; apps/web/index.html; src/prime_core/history_service.py; tests/phase15/test_recovery_secret_regression.py; tests/phase15/test_requirement_qualification.py; evidence/phase15/qualification-continuation-056.md.
- Confidence: VERIFIED
- Scope: PRIME persistent Core/UI recovery, backup privacy, source lifecycle, and local V1 convergence.
- Supersedes learning: L-PRIME-NODE-TRUST-LIFECYCLE-055

## L-PRIME-RESTORATION-BOUNDED-LOCAL-QUALIFICATION-057

- Date: 2026-08-14
- Learning ID: L-PRIME-RESTORATION-BOUNDED-LOCAL-QUALIFICATION-057
- Fact or lesson: The persistent PRIME database can contain historical regression rows that must not be mistaken for the real managed project. Identify the governed project by its canonical repository binding first. For DOD-005, authority-only source references do not satisfy the safe retraction/restoration candidate contract when no evidence record or Documentation projection is present; the correct result is a truthful hard stop without SQL mutation or synthetic evidence.
- Evidence location: evidence/phase15/qualification-continuation-057.md; docs/requirements-traceability.yaml; docs/phase15-remediation-qualification-ledger.yaml.
- Confidence: VERIFIED
- Scope: PRIME persistent Atlas project identity, DOD-005 preflight, and local browser qualification boundary.
- Supersedes learning: L-PRIME-LOCAL-CONVERGENCE-056

## L-PRIME-TRUSTED-HOST-LOCAL-IDENTITY-058

- Date: 2026-08-14
- Learning ID: L-PRIME-TRUSTED-HOST-LOCAL-IDENTITY-058
- Fact or lesson: A trusted Atlas host can provide a bounded local identity path without storing or transmitting an operator password when the browser only creates a short-lived challenge, the host command reads a separate mode-0600 secret, and Core redeems a browser nonce into ordinary session/CSRF state. SIGN_IN and STEP_UP must remain purpose-isolated, approval must require the dedicated host secret, and consumed or expired challenges must fail closed. Loopback transport is only a transport boundary; it is not sufficient identity proof without the separate secret.
- Evidence location: migrations/prime/0034_local_identity_authentication.sql; src/prime_core/service.py; apps/core/main.py; apps/web/index.html; packaging/core/prime-local-auth; tests/phase15/test_local_identity_authentication.py; evidence/phase15/qualification-continuation-058.md.
- Confidence: VERIFIED
- Scope: PRIME persistent Atlas Core/UI trusted-host authentication and single-operator browser continuity.
- Supersedes learning: L-PRIME-RESTORATION-BOUNDED-LOCAL-QUALIFICATION-057

## L-PRIME-SAFE-PRODUCT-WAVE-059

- Date: 2026-08-15
- Learning ID: L-PRIME-SAFE-PRODUCT-WAVE-059
- Fact or lesson: A persistent Core image must be rebuilt and swapped through the existing PRIME-owned systemd/container path before checkout edits are live; a read-only repository mount does not change the image import tree. Safe operator qualification is strongest when UI mutations are bounded, restarted against the same persistent state mount, and restored exactly. Truthful product panels should render existing records and explicit unavailable provider/limit states rather than invent cost or capability.
- Evidence location: Dockerfile.core; packaging/core/prime-core.service; apps/core/main.py; apps/web/index.html; src/prime_core/reliability_service.py; tests/phase15/test_continuation059_safe_wave.py; evidence/phase15/qualification-continuation-059.md
- Confidence: VERIFIED
- Scope: PRIME persistent Atlas Core/UI image lifecycle, safe browser qualification, data-backed Usage/Backup/Metadata surfaces, and responsive navigation.
- Supersedes learning: L-PRIME-TRUSTED-HOST-LOCAL-IDENTITY-058

## L-PRIME-RUNTIME-PROVENANCE-060

- Date: 2026-08-15
- Learning ID: L-PRIME-RUNTIME-PROVENANCE-060
- Fact or lesson: A read-only checkout mount does not change code imported by an already-built Core image. Runtime provenance must be injected at image build time and exposed through health/operator state. Inherited container environment variables can shadow new image defaults, so stale provenance variables must be removed during a persistent swap while other runtime references are preserved. Long diagnostic identifiers need overflow containment for narrow-screen usability.
- Evidence location: Dockerfile.core; src/prime_core/build_info.py; apps/core/main.py; apps/web/index.html; tests/phase15/test_runtime_provenance.py; evidence/phase15/qualification-continuation-060.md
- Confidence: VERIFIED
- Scope: persistent Core image provenance, service swap, operator diagnostics, and responsive browser behavior.
- Supersedes learning: L-PRIME-SAFE-PRODUCT-WAVE-059

## L-PRIME-SAFE-LOCAL-PRODUCT-COMPLETION-061

- Date: 2026-08-15
- Learning ID: L-PRIME-SAFE-LOCAL-PRODUCT-COMPLETION-061
- Fact or lesson: Product implementation must be exercised through the persistent runtime before qualification. The 061 snapshot addition initially shadowed the ProgressService with a database row and failed only on the real authenticated snapshot path; the minimal rename-and-regression-test repair restored the service call. The gstack browser executable must run from a local writable state location, but the bundled server currently lacks the Playwright package; direct SSHFS execution fails with EPERM and is not an acceptable substitute.
- Evidence location: apps/core/main.py; tests/phase15/test_continuation_061_product.py; Dockerfile.core; packaging/core/prime-core.service; evidence/phase15/qualification-continuation-061.md
- Confidence: VERIFIED
- Scope: PRIME persistent Atlas product runtime, safe local product surfaces, authenticated API qualification, and browser-tool boundary.
- Supersedes learning: L-PRIME-RUNTIME-PROVENANCE-060

## L-PRIME-BROWSER-HARNESS-OPERATOR-QUALIFICATION-062

- Date: 2026-08-15
- Learning ID: L-PRIME-BROWSER-HARNESS-OPERATOR-QUALIFICATION-062
- Fact or lesson: The approved gstack harness must be run from its local writable installation root with its existing pinned runtime and state. The existing Atlas SSH forward can prove the genuine persistent PRIME topology without using the Z: SSHFS path, and an authenticated browser journey is materially stronger evidence than isolated API checks. A canonical Node outage must preserve the operator shell, surface one truthful material NODE_DEGRADED notification, fail closed on Node-required repository control, and restore the exact healthy/enrolled state without authority-hash mutation.
- Evidence location: C:\\Users\\sketc\\.agents\\skills\\gstack; evidence/phase15/qualification-continuation-062.md; docs/v1-product-goal-alignment-audit.yaml; docs/v1-product-gap-burndown.yaml
- Confidence: VERIFIED
- Scope: existing gstack browser harness, persistent Atlas PRIME UI/Core route, authenticated operator qualification, Node outage/recovery, and browser state continuity.
- Supersedes learning: L-PRIME-SAFE-LOCAL-PRODUCT-COMPLETION-061

## L-PRIME-RESTORATION-BOUNDED-LIFECYCLE-ONBOARDING-063

- Date: 2026-08-15
- Learning ID: L-PRIME-RESTORATION-BOUNDED-LIFECYCLE-ONBOARDING-063
- Fact or lesson: A real persistent product can be qualified safely without manufacturing positive state. The current PRIME UI's generic protected-action dialog refuses because no specific lifecycle workflow is wired; empty correction input is blocked before network submission; incomplete backup preflight returns HTTP 422 without mutation. When a supported inverse or legitimate Class-B target is absent, the correct result is an exact remaining gap, not a synthetic project, repository, Goal, authority rewrite, backup destination, or destructive restore.
- Evidence location: apps/web/index.html; apps/core/main.py; evidence/phase15/qualification-continuation-063.md; docs/v1-product-goal-alignment-audit.yaml; docs/v1-product-gap-burndown.yaml
- Confidence: VERIFIED
- Scope: persistent Atlas PRIME browser qualification, restoration ledger, lifecycle/refusal boundaries, correction validation, backup preflight, onboarding safety, and destructive-action preservation.
- Supersedes learning: L-PRIME-BROWSER-HARNESS-OPERATOR-QUALIFICATION-062

## L-PRIME-EXPLICIT-OPERATOR-WORKFLOWS-064

- Date: 2026-08-15
- Learning ID: L-PRIME-EXPLICIT-OPERATOR-WORKFLOWS-064
- Fact or lesson: Durable lifecycle operations need a server-issued, expiring, single-use preflight bound to the observed project/repository/node identity. The real persistent browser path can qualify reversible actions and exact-target refusal without creating a secondary project. A rollback-safe container rename preserves recovery while a user-scoped systemd unit restarts the same persistent state bind. The Core-served UI is the actual private web product on `127.0.0.1:18000`; the previously assumed `28000` route is not a PRIME listener in the current Atlas topology.
- Evidence location: src/prime_core/lifecycle_service.py; migrations/prime/0036_operator_workflows.sql; apps/core/main.py; apps/web/index.html; evidence/phase15/qualification-continuation-064.md
- Confidence: VERIFIED
- Scope: persistent Atlas PRIME Core/UI, lifecycle safety, onboarding boundaries, authority review, guided Goal controls, and browser operator qualification.
- Supersedes learning: L-PRIME-RESTORATION-BOUNDED-LIFECYCLE-ONBOARDING-063

## L-PRIME-LOCAL-V1-CONVERGENCE-065

- Date: 2026-08-15
- Learning ID: L-PRIME-LOCAL-V1-CONVERGENCE-065
- Fact or lesson: Security-negative qualification is only complete when CSRF, stale and replayed single-use preflights, exact-target mismatch, typed confirmation, recent step-up requirements, and post-refusal state identity are all checked against the persistent project. Approved Goal protection must precede content validation so legacy governed Goal text cannot turn a protected overwrite into a misleading validation error. Safe authority adoption can be idempotent and file-preserving while still advancing onboarding metadata, so that side effect must be restored or explicitly surfaced.
- Evidence location: src/prime_core/service.py; tests/phase15/test_continuation_065_local_convergence.py; evidence/phase15/qualification-continuation-065.md; persistent Core readiness and browser network evidence.
- Confidence: VERIFIED
- Scope: PRIME persistent Atlas lifecycle/security-negative matrix, onboarding refusal, authority adoption, Goal protection, Progress correction refusal, backup preflight, and browser polish.
- Supersedes learning: L-PRIME-EXPLICIT-OPERATOR-WORKFLOWS-064


## L-PRIME-V1-RELEASE-BLOCKER-CLASSIFICATION-066

- Date: 2026-08-15
- Learning ID: L-PRIME-V1-RELEASE-BLOCKER-CLASSIFICATION-066
- Fact or lesson: After the negative/refusal wave is complete, an unchanged burndown is not evidence of a missing test. The remaining rows must be separated into exact frozen clauses that are resource-available, require a real external capability, require a legitimate durable target, or are parked/gated. Existing Hindsight, a running Tailscale daemon, or the Notion journal connector do not by themselves prove that PRIME's approved runtime integrations or qualification targets are available.
- Evidence location: evidence/phase15/qualification-continuation-066.md; docs/v1-product-gap-burndown.yaml; docs/phase15-remediation-matrix.yaml; docs/phase15-remediation-qualification-ledger.yaml; docs/requirements-traceability.yaml
- Confidence: VERIFIED
- Scope: Continuation 066 release-blocker classification and persistent Atlas resource inspection.
- Supersedes learning: L-PRIME-LOCAL-V1-CONVERGENCE-065

## L-PRIME-PRIME-RUNTIME-NOTION-UNBLOCK-067

- Date: 2026-08-15
- Learning ID: L-PRIME-PRIME-RUNTIME-NOTION-UNBLOCK-067
- Fact or lesson: The Notion journal connector being available to an assistant does not establish PRIME runtime Notion capability. PRIME must receive the approved MyAssistant source NOTION_READONLY_KEY and retain only env/myassistant/notion-readonly. When that source is absent, the live registry correctly returns SOURCE_ABSENT and UNCONFIGURED without mutating state; qualification must stop rather than search broadly or create a substitute resource.
- Evidence location: evidence/phase15/qualification-continuation-067.md; src/prime_core/notion_credentials.py; live animus-prime-core container environment and registry check
- Confidence: VERIFIED
- Scope: PRIME runtime Notion credential/resource capability boundary.
- Supersedes learning: L-PRIME-V1-RELEASE-BLOCKER-CLASSIFICATION-066
## L-PRIME-HINDSIGHT-CAPABILITY-UNBLOCK-068

- Date: 2026-08-16
- Learning ID: L-PRIME-HINDSIGHT-CAPABILITY-UNBLOCK-068
- Fact or lesson: A healthy persistent Hindsight API and successful PRIME recall do not establish Reflect or Mental Models. The service can be reachable while Reflect fails at the configured model transport because no usable tool call is produced. Mental Models must be observed in the project bank, not inferred from endpoint existence or container health.
- Evidence location: evidence/phase15/qualification-continuation-068.md; live mimir-hindsight-production health, bank, recall, Reflect, and Mental Models probes
- Confidence: VERIFIED
- Scope: Hindsight capability qualification for PRIME V1.
- Supersedes learning: L-PRIME-PRIME-RUNTIME-NOTION-UNBLOCK-067
## L-PRIME-PARAGON-PROVIDER-HINDSIGHT-UNBLOCK-069

- Date: 2026-08-16
- Learning ID: L-PRIME-PARAGON-PROVIDER-HINDSIGHT-UNBLOCK-069
- Fact or lesson: PARAGON authentication, model discovery, ordinary completion, and structured JSON do not establish OpenAI-compatible function calling. The live endpoint returned HTTP 200 for a forced harmless tool request but emitted ordinary assistant text with no tool_calls, so Hindsight Reflect cannot be qualified from this profile.
- Evidence location: evidence/phase15/qualification-continuation-069.md; protected PARAGON smoke through the existing Hindsight runtime secret; live Hindsight model profile
- Confidence: VERIFIED
- Scope: PRIME provider capability gate for Hindsight Reflect/Mental Models and provider-backed V1 clauses.

- Supersedes learning: L-PRIME-HINDSIGHT-CAPABILITY-UNBLOCK-068

## L-PRIME-PARAGON-GENERAL-AI-HINDSIGHT-TOOL-BOUNDARY-070

- Date: 2026-08-16
- Learning ID: L-PRIME-PARAGON-GENERAL-AI-HINDSIGHT-TOOL-BOUNDARY-070
- Fact or lesson: The persistent PRIME Core can use the existing PARAGON endpoint for ordinary structured general AI while preserving LOCAL_ONLY semantics. A harmless single-function PARAGON request emitted a valid OpenAI-compatible tool_call, but the exact native Hindsight tool set (search_mental_models, search_observations, recall, expand, done) returned no_eligible_model. Therefore single-tool support does not establish Hindsight native tool compatibility.
- Evidence location: evidence/phase15/qualification-continuation-070.md; persistent Core profile and ASK_PRIME result; direct protected PARAGON/Hindsight runtime probes.
- Confidence: VERIFIED
- Scope: PRIME general AI provider activation and Hindsight Reflect/Mental Models capability boundary.
- Supersedes learning: L-PRIME-PARAGON-PROVIDER-HINDSIGHT-UNBLOCK-069

## L-PRIME-HINDSIGHT-REFLECT-ELIGIBILITY-DIFFERENTIAL-071

- Date: 2026-08-16
- Learning ID: L-PRIME-HINDSIGHT-REFLECT-ELIGIBILITY-DIFFERENTIAL-071
- Fact or lesson: Hindsight Reflect request classification must use only operator `user` messages for routing task identity. System/client instructions and accumulated assistant/tool history remain part of provider payload and context estimation, but including them in task classification can falsely produce a high context demand and exclude every unknown-context OpenRouter candidate before capability selection. A representative tool-call probe must also preserve Hindsight's bank attribution; a stripped request is not equivalent evidence. Native observation/recall Reflect success still does not establish Mental Models, which must be observed in the legitimate project bank rather than synthesized.
- Evidence location: evidence/phase15/qualification-continuation-071.md; published PARAGON commits `9b6dec4` and `a5d1485`; persistent Hindsight Reflect result and Mental Models listing
- Confidence: VERIFIED
- Scope: PARAGON routing eligibility boundary and persistent Hindsight Reflect/Mental Models qualification.
- Supersedes learning: L-PRIME-PARAGON-GENERAL-AI-HINDSIGHT-TOOL-BOUNDARY-070

## L-PRIME-LEGITIMATE-MENTAL-MODEL-SOURCE-GATE-072

- Date: 2026-08-16
- Learning ID: L-PRIME-LEGITIMATE-MENTAL-MODEL-SOURCE-GATE-072
- Fact or lesson: A persistent Hindsight bank can contain substantial real project memories and pass Recall while the exact Reflect tool-call path is unavailable. Mental Model creation must therefore be gated on successful source-query Reflect synthesis, not on bank non-emptiness or manually assembled content. A current no_eligible_model result is a truthful blocker for creation, even when prior bounded Reflect evidence passed.
- Evidence location: evidence/phase15/qualification-continuation-072.md; persistent Hindsight Recall result; Hindsight Reflect logs for the exact authorized source query
- Confidence: VERIFIED
- Scope: PRIME legitimate Mental Model creation gate and Hindsight Reflect/Recall capability boundary.
- Supersedes learning: L-PRIME-HINDSIGHT-REFLECT-ELIGIBILITY-DIFFERENTIAL-071

## L-PRIME-PARAGON-TOOL-MEDIATED-CONTEXT-GATE-073

- Date: 2026-08-16
- Learning ID: L-PRIME-PARAGON-TOOL-MEDIATED-CONTEXT-GATE-073
- Fact or lesson: A semantic architecture label must not impose a large hard context requirement on a tool-mediated request whose retrieved project state arrives incrementally. The exact 072 query was a small request with 1000 estimated input tokens and 1024 requested output tokens, yet PARAGON assigned 200000 required context and excluded all 129 unknown-context candidates. The corrected contract uses actual request/output capacity for tool-call requests and keeps large-request capacity gates active.
- Evidence location: evidence/phase15/qualification-continuation-073.md; PARAGON commit 60c1668; src/routing/taskProfile.js; test/automaticRouting.test.js; live routing preview A/B/lexical differential.
- Confidence: VERIFIED
- Scope: Continuation 073 PARAGON routing eligibility correction.
- Supersedes learning: L-PRIME-HINDSIGHT-REFLECT-ELIGIBILITY-DIFFERENTIAL-071

## L-PRIME-PARAGON-EXACT-REFLECT-POST-RESTART-073

- Date: 2026-08-16
- Learning ID: L-PRIME-PARAGON-EXACT-REFLECT-POST-RESTART-073
- Fact or lesson: After the published tool-mediated context-gate correction is loaded by the persistent PARAGON service, the exact original 072 Hindsight Reflect query succeeds without wording changes. The real result used four native observation/recall tool calls and returned 198 provenance-bearing memories in based_on. A successful Reflect preflight still does not authorize Mental Model creation.
- Evidence location: evidence/phase15/qualification-continuation-073.md; PARAGON MainPID 607574; Hindsight Reflect response trace and based_on summary.
- Confidence: VERIFIED
- Scope: 073 post-restart runtime qualification only.
- Supersedes learning: L-PRIME-PARAGON-TOOL-MEDIATED-CONTEXT-GATE-073

## L-PRIME-LEGITIMATE-MENTAL-MODEL-QUALIFICATION-074

- Date: 2026-08-16
- Learning ID: L-PRIME-LEGITIMATE-MENTAL-MODEL-QUALIFICATION-074
- Fact or lesson: A legitimate Hindsight Mental Model must be created through the supported operation from an already-qualified Reflect source, retain stored provenance and exact project-bank identity, remain manually refreshable, and be surfaced by PRIME as derived and non-authoritative. Creation alone is insufficient without durable API/UI re-read and persistent restart evidence.
- Evidence location: evidence/phase15/qualification-continuation-074.md; src/prime_memory_adapter.py; src/prime_core/memory_service.py; apps/core/main.py; apps/web/index.html; tests/phase0/test_prime_memory_adapter.py
- Confidence: VERIFIED
- Scope: PRIME project-scoped Hindsight Mental Model creation and operator boundary.
- Supersedes learning: L-PRIME-LEGITIMATE-MENTAL-MODEL-SOURCE-GATE-072

## L-PRIME-RUNTIME-NOTION-SECURE-LIFECYCLE-075

- Date: 2026-08-16
- Learning ID: L-PRIME-RUNTIME-NOTION-SECURE-LIFECYCLE-075
- Fact or lesson: PRIME can resolve the approved runtime Notion credential from an Atlas-only `0600` environment file while storing only the existing credential reference and `0600` metadata/state files. Against the approved sandbox, the existing production lifecycle preserved operator content, refused conflicts and stale work, supported idempotent history, and carried source provenance through attach/refresh/detach. These backend results do not by themselves qualify a frozen operator-visible workflow when the persistent UI exposes only connection/read health.
- Evidence location: evidence/phase15/qualification-continuation-075.md; `/home/sketch/.config/animus-prime/notion-runtime.env`; PRIME credential-reference and lifecycle-state metadata; persistent adapter probe result.
- Confidence: VERIFIED
- Scope: PRIME runtime Notion credential boundary and backend lifecycle qualification.
- Supersedes learning: L-PRIME-PRIME-RUNTIME-NOTION-UNBLOCK-067

## L-PRIME-RUNTIME-NOTION-OPERATOR-WORKFLOW-076

- Date: 2026-08-16
- Learning ID: L-PRIME-RUNTIME-NOTION-OPERATOR-WORKFLOW-076
- Fact or lesson: The approved Notion lifecycle is product-qualified only when the authenticated persistent UI exposes the existing production actions. Detached sources must remain DETACHED/RETRACTED across reconcile and refresh, and same-period managed history must return the persisted record idempotently instead of attempting a duplicate external create.
- Evidence location: evidence/phase15/qualification-continuation-076.md; apps/core/main.py; src/prime_core/notion_service.py; apps/web/index.html; tests/phase14/test_web_shell.py
- Confidence: VERIFIED
- Scope: Continuation 076 persistent Notion operator workflow only.
- Supersedes learning: L-PRIME-RUNTIME-NOTION-SECURE-LIFECYCLE-075

## L-PRIME-ASK-SEARCH-REQUALIFICATION-077

- Date: 2026-08-16
- Learning ID: L-PRIME-ASK-SEARCH-REQUALIFICATION-077
- Fact or lesson: Passing persistent runtime, provider, and Notion lifecycle gates does not qualify Ask or Unified Search. The current Ask path can return stale memory-derived prose or UNKNOWN without citations because natural-language source selection is not content-aware and several grounded source groups are excluded from model sources. The current Search path can return Repository/Memory results while lacking positive Git/Notion projection and can return unrelated Memory hits for a unique no-result query. Detached Notion sources were correctly excluded. These are product source-indexing/current-grounding defects, not reasons to reopen PARAGON or manufacture qualification targets.
- Evidence location: evidence/phase15/qualification-continuation-077.md; src/prime_core/intelligence_service.py; apps/core/main.py; apps/web/index.html
- Confidence: VERIFIED
- Scope: Continuation 077 Ask/Search operator qualification.
- Supersedes learning: none

## L-PRIME-SHARED-RETRIEVAL-GROUNDING-078

- Date: 2026-08-17
- Learning ID: L-PRIME-SHARED-RETRIEVAL-GROUNDING-078
- Fact or lesson: Ask and Unified Search must consume one typed retrieval-hit contract. PostgreSQL content projection fixes natural-language repository/.agent retrieval without a second search subsystem; canonical Git and live Notion lifecycle state must enter the derived Search projection; detach must retract; pinned Hindsight 0.6 score payloads can be nested and require PRIME-side extraction/flooring; provider category spelling must be normalized before grounded citation validation; and citation resolution must retain source identity, revision, hash, freshness, and authority class. Common-word OR terms can create false positives, so stopword handling is part of truthful no-result behavior.
- Evidence location: evidence/phase15/qualification-continuation-078.md; src/prime_core/retrieval.py; src/prime_core/indexer.py; src/prime_core/intelligence_service.py; src/prime_core/ai_service.py; src/prime_core/memory_service.py; src/prime_core/notion_service.py
- Confidence: VERIFIED
- Scope: Continuation 078 shared retrieval and grounding repair only.
- Supersedes learning: L-PRIME-ASK-SEARCH-REQUALIFICATION-077
