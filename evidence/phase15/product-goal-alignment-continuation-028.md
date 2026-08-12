# ANIMUS PRIME — Continuation 028 Product-Goal Alignment Audit

## Baseline and control question

- Frozen product contract: `PRIME-SPEC-V1.0.0`.
- Frozen Definition of Done source: `baseline/PRIME-SPEC-V1.0.0.notion.md`, §26.
- Mechanical inventory: `81` unchecked §26 items, retained in `docs/v1-product-goal-alignment-audit.yaml`.
- The controlling gate is `V1_PRODUCT_GOAL_ALIGNMENT`. It is `FAIL` unless every item is `USER_USABLE_VERIFIED` or its frozen criterion's genuinely required environment is qualified.
- No frozen baseline, v1.0.1, SpecChangeRecord, Phase 16, or deployment was created.

## Audit result

The initial inspection found a protected, accessible web shell with real authentication, project creation/listing, system-state probes, Ask/Search submission, Time Lens controls, and Notion capability buttons. Most named project surfaces were descriptive cards without live data, loading/empty/degraded/error handling, drill-down, or user action. The backend contained useful primitives that were not exposed through the intended product path.

The first local product slice now exposes a bounded project snapshot, normalized Since You Were Here events and checkpoint advance, live Home/Overview/Needs Attention/Recently Active/Activity data, grouped Search results, Ask citations and safe UNKNOWN output, an on-demand derived Brain response, and explicit NOT AVAILABLE Fork/Clone behavior. A CSP defect found during browser qualification was fixed by serving the existing inline shell with a per-response nonce. The policy was not weakened with `unsafe-inline`.

Final mechanical status:

| Status | Count |
|---|---:|
| `USER_USABLE_VERIFIED` | 3 |
| `IMPLEMENTED_NOT_PRODUCT_QUALIFIED` | 6 |
| `BACKEND_ONLY` | 43 |
| `UI_SHELL_ONLY` | 15 |
| `PARTIAL` | 10 |
| `MISSING` | 3 |
| `BLOCKED_BY_ENVIRONMENT` | 1 |
| **Total** | **81** |

The three user-usable items are the single-operator boundary, Home’s four required global surfaces, and the project-scoped Since You Were Here recap. This does not imply V1 is complete.

## Browser and API qualification

Qualification used a fresh disposable PostgreSQL database (`prime_product_028`) and a browser-served Core instance on `127.0.0.1:18028`. No authoritative project data was changed.

- `PASSED` — migrations completed on the disposable database.
- `PASSED` — `/` returned `200` with `Cache-Control: no-store` and a nonce-bearing CSP that allowed the shell to execute without console CSP errors.
- `PASSED` — first-run initialization, operator sign-in, and protected project creation worked through the visible UI.
- `PASSED` — Home rendered Projects, Needs Attention, Recently Active, and System Health from live state.
- `PASSED` — project snapshot rendered independent lifecycle/connectivity/freshness/work-condition values and actionable attention records for an unbound, unapproved project.
- `PASSED` — a normalized project event rendered in Since You Were Here and Recently Active; `Mark recap reviewed` advanced the checkpoint and the recap became empty.
- `PASSED` — Ask rendered `UNKNOWN` plus the degraded/privacy-safe state when no configured model was available; no citation was fabricated.
- `PASSED` — Search rendered grouped project-scoped results and the empty state.
- `PASSED` — Project Brain rendered `UNAVAILABLE` with zero nodes/edges and the derived-only layout; no claim of graph availability was made.
- `PASSED` — Time Lens exposed an actual historical-boundary selector and form; historical reconstruction remains partial until the remaining evidence path is complete.
- `PASSED` — final browser console had no errors after the CSP fix and product-path reload.

The browser initially `FAILED` on the CSP check because the pre-fix response blocked the inline style and script. That failure is retained as a diagnostic finding; the final run passed after the nonce fix.

## Highest-value remaining gaps

1. Goal, Progress, Alignment, Milestones, Integrity, Repository, Authority, Memory, Knowledge, Evidence, and most Settings surfaces still need complete data-backed operator workflows and source drill-down.
2. Search still lacks the complete frozen source model in the product result set, including `.agent`, Git, and Notion knowledge paths.
3. Ask has the safe UNKNOWN and citation container, but needs populated evidence-backed citation qualification and revision-aware historical resolution.
4. Project Brain remains a derived-only safe response with an accessible fallback, not the required interactive 3D graph and grounded drill-down.
5. Fork/Clone, guided onboarding, context export, lifecycle controls, backup/restore UI, usage/cost, and notification workflows remain incomplete or unavailable.
6. Node, Hindsight, external assistive-technology, and remote integration qualification remains environment-bounded where prior records say so.

## Remediation and governance boundary

This continuation did not blanket-reopen the 16 verified remediation rows. Product gaps are mapped to their owning phases and R rows in the YAML. R-050 remains validly qualified for its prior supported-browser evidence while §26 historical product coverage remains partial. R-044 remains partial without approved Hindsight `retain`; R-053 remains partial without external assistive-technology evidence; R-056 remains open until the remaining product gaps are addressed.

The authoritative governed release state remains `V1_PRODUCT_GOAL_ALIGNMENT: FAIL`, `Phase 15: FAIL`, `16/26 VERIFIED`, `9 partial`, `R-056 OPEN`, `0 failed`, and deployment `NOT PERFORMED`.

## Environment boundaries

- R-044: approved Hindsight retain remains partial unless the pinned Hindsight process/listener and provider environment become available.
- R-053: external assistive-technology evidence remains unavailable; existing keyboard, responsive, and reduced-motion evidence is preserved.
- R-031–R-036 and §26 native-node items remain environment-dependent and are not fabricated.
- Deployment: `NOT PERFORMED`.
