# ANIMUS PRIME — Phase 15 Qualification Continuation 078

## Acceptance

**Bounded result: PASS for the shared retrieval / grounding repair.** DOD-021 and DOD-022 are promoted only for the complete operator-visible behavior exercised here. DOD-005, DOD-081, R-056, Phase 16, deployment, and public exposure remain outside scope.

## Baseline and authority

- Frozen specification: `PRIME-SPEC-V1.0.0`
- Atlas checkout: `/home/sketch/Projects/ANIMUS_PRIME`
- Starting governed commit: `87f94c44e0e46f9121c49803d763633ea008bd0e`
- Qualified implementation lineage: `20971fc4fd0d4f57ae191a751888f60b34f2f53b` through `ed6b9f8b5ffae8a4fe73532f10fc162013da10a0`
- Final governed commit is the publication commit recorded at closeout; the implementation tip above is the runtime build input.
- The pre-existing untracked `.codebase-memory/`, `.prime-evidence/`, and `.vscode/` directories were preserved and were not staged.
- Execution and runtime verification used direct Atlas/SSH. No `Z:` path was used for runtime execution.

## Bounded repair

The repair creates one typed `RetrievalHit` contract shared by Search and Ask; retains searchable repository text in the existing repository index and uses PostgreSQL full-text matching; classifies nested `AGENTS.md`/`PROJECT_GOAL.md` authority material; reads canonical Git history through the existing read-only Git boundary; projects attached Notion source state into the derived Search representation and retracts it on detach; applies a PRIME-side Memory relevance floor using the score returned by pinned Hindsight; passes all qualified source groups to Ask; normalizes provider category spelling; requires citations for grounded answers; and enriches citations with admitted source identity, revision, hash, freshness, and authority classification.

No replacement search service, bank, project, repository, Node, provider, or synthetic qualification target was created.

## Persistent runtime topology

| Component | Result |
|---|---|
| PostgreSQL | Existing persistent `animus-prime-phase0-postgres-1`, preserved and reused |
| Hindsight | Existing persistent `mimir-hindsight-production`, preserved and reused |
| Repository Node | Existing enrolled canonical Node, preserved |
| PRIME Core | Existing `animus-prime-core`, rebuilt/recreated in place only |
| Core image | `animus-prime-core:continuation-078-r9` |
| Runtime build | `ed6b9f8b5ffae8a4fe73532f10fc162013da10a0` |
| Schema | `0037_shared_retrieval_projection.sql` |
| Core listener | `127.0.0.1:18000` (private) |
| Web UI | Existing persistent PRIME UI served by Core at `127.0.0.1:18000` |
| Public exposure | None; Funnel/Tailscale/unrelated listeners untouched |

Core readiness returned `status=ready`, `spec_revision=PRIME-SPEC-V1.0.0`, the runtime build commit above, image identity `animus-prime-core:continuation-078-r9`, schema `0037_shared_retrieval_projection.sql`, and service version `1.0.0`. The existing persistent mounts and database/Hindsight targets remained attached. No raw credential was printed or committed.

## Browser qualification

Browser: authenticated real Chromium through the approved gstack browser workflow. The supported architecture serves `apps/web/index.html` from the Core private listener at `http://127.0.0.1:18000/`; any local browser forwarding is transport only and is not a second UI service. Existing Qualification Project: `project_d9a1a5b609394282b62fc12c0d04634d`.

### Unified Search

- Natural-language repository/authority query: `What does AGENTS.md say about code exploration?` returned content-aware Repository hits and Authority hits including `AGENTS.md` and the nested `authority-template/v1/AGENTS.md`.
- A returned admitted hit carried source revision `20971fc4fd0d4f57ae191a751888f60b34f2f53b` and content hash `c224850c34b17d013dccfde3253e1bf66d8920d9d6899f08fdd5b9b85ae8f99e`.
- Git query against the current implementation history returned canonical Git hits rather than treating `git_history_checkpoints` as the only source.
- Real Hindsight Memory query `ANIMUS PRIME` returned eight qualified hits with nested score extraction; representative final relevance was approximately `1.098`, above the PRIME-side `0.25` floor.
- Activity query `REPOSITORY_CHANGED` returned grouped Activity hits with source revisions.
- An approved Notion source page was attached and refreshed through the real UI. Search returned one Notion Knowledge hit with binding `continuation-078-search-source`, page locator `https://www.notion.so/3be833cb27ff81aa9fe2ffb4fc5f980`, revision `201100000`, current freshness, and derived knowledge classification. The same source was then detached through the real UI with confirmation; the binding became `DETACHED`, retrieval became `RETRACTED`, and the page-ID Search query returned zero Notion Knowledge hits.
- Exact unique no-result query `zzzxylophoneonlyqv` returned zero hits for every group: Repository, Authority, Git, Notion Knowledge, Activity, Progress, Memory, and Evidence.
- Evidence remained truthfully empty because the project has no admitted current `evidence_records`; Progress remained truthfully empty because the current assessment was stale. Neither was fabricated or presented as a current hit.

### Ask

- Grounded question: `What does AGENTS.md say about code exploration?`
- Result: returned the AGENTS.md statement that unfamiliar code should use the configured symbol/graph navigation and strings/configuration/non-code files should use targeted text search.
- Citation: source class `Authority`; source ID `AGENTS.md`; source revision `20971fc4fd0d4f57ae191a751888f60b34f2f53b`; content hash `c224850c34b17d013dccfde3253e1bf66d8920d9d6899f08fdd5b9b85ae8f99e`; epistemic class `SOURCE FACT`.
- Unknown question: `What is the private operator's favorite color?` returned `UNKNOWN: available evidence does not support this claim.` with `State: No data available`.
- Provider category normalization accepts the routed provider's `SOURCE_FACT` spelling as the frozen `SOURCE FACT` class; no citation-free grounded answer was accepted.

## Project isolation and lifecycle

All exercised results were scoped to the existing Qualification Project. No second project or synthetic target was created. Notion detach/retraction excluded the source from subsequent Search results without deleting the external page. Source revision, hash, freshness, and authority metadata remained derived/non-authoritative and were included for citation resolution.

## Validation

- Focused retrieval/Ask/Notion/runtime tests: **PASSED — 20 passed, 4 skipped**.
- Full supported PRIME regression: **PASSED — 113 passed, 28 skipped**. Skips are the established integration/environment skips; no new skip was used to claim success.
- Python compile check for changed modules: **PASSED**.
- `git diff --check`: **PASSED**.
- Governance validator: **PASSED**.
- Product gap burndown validator: **PASSED**.
- Secret scan / tracked-content review: **PASSED**; no raw Notion or other credential is present in source, evidence, `.agent`, or Git.
- Persistent Core readiness and private listener: **PASSED**.
- Browser Search/Ask qualification: **PASSED for the bounded DOD-021/DOD-022 clauses above**.

## Governed status change

- DOD-021: `USER_USABLE_VERIFIED`; current grounding, source classes, citation requirement, admitted source identity, revision/hash resolution, and safe UNKNOWN behavior qualified.
- DOD-022: `USER_USABLE_VERIFIED`; grouped Repository/.agent, Git, Notion Knowledge, Memory, Activity, freshness/retraction, project scoping, drill-down metadata, and truthful no-result behavior qualified. Evidence/Progress remain explicitly empty/stale where the real project has no current admitted records.
- R-047 and R-054 remain `VERIFIED`; Continuation 078 evidence was added to their traceability support.
- Burndown totals reduced `LOCAL_BROWSER_QUALIFICATION` from 12 to 10 and `EXTERNAL_ENVIRONMENT` from 8 to 6.

## Remaining boundary

Notion runtime qualification remains available through the approved secure Atlas reference, but the Continuation 078 probe source was deliberately detached and remains retracted. DOD-005 remains parked. Remaining external/provider/legitimate-target requirements, DOD-081, R-056, Phase 15 completion, and V1 declaration remain open. No automatic Continuation 079 is issued by this evidence. No deployment or public exposure occurred.
