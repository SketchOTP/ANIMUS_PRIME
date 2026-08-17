# ANIMUS PRIME — Phase 15 Qualification Continuation 085

## Verdict

`PARTIAL` — the bounded Warm Start implementation is now present in the persistent Atlas product and the real browser path executes with project isolation, explicit selection, deduplication, secret refusal, and native Hindsight reread evidence. The complete frozen DOD-031/R-054 warm-start clause remains open because the existing selected Notion source is retracted/blank. No other open DOD was promoted in this continuation.

## Baseline

- Frozen specification: `PRIME-SPEC-V1.0.0`
- Starting governed HEAD: `710dcef10cfa7ffd3f8bf64a5f550aed1e72de2f`
- Starting qualified implementation: `02d93dead9ad9479a38a3ed16171b12f3594d2b7`
- Starting queue: `68 complete / 13 open`
- Starting open DODs: `DOD-004, DOD-013, DOD-016, DOD-031, DOD-044, DOD-047, DOD-049, DOD-053, DOD-055, DOD-077, DOD-079, DOD-080, DOD-081`; aggregate `R-056` remains gated.
- Direct Atlas execution: `/home/sketch/Projects/ANIMUS_PRIME`; no `Z:` execution.
- Worktree status at start: only preserved untracked `.codebase-memory/`, `.prime-evidence/`, and `.vscode/`.
- Existing unrelated services and Funnel configuration were not changed.

## Runtime topology

| Component | Runtime / identity | Interface | Result |
|---|---|---|---|
| PostgreSQL | Existing `animus-prime-phase0-postgres-1` | private Docker network | `PASSED` — persistent schema remained attached |
| Hindsight | Existing `mimir-hindsight-production` | `127.0.0.1:8888` | `PASSED` — healthy/connected; native consolidation settled |
| PRIME Core | user `animus-prime-core.service`, image `animus-prime-core:continuation-085-warm-start-final` | `127.0.0.1:8000` | `PASSED` — readiness and live health |
| PRIME UI | genuine browser UI through existing private UI path | browser `http://127.0.0.1:28000` | `PASSED` — authenticated operator path |
| Repository Node | existing `animus-prime-node.service` | `127.0.0.1:18001` | `PASSED` — service active; heartbeat/repository callbacks continued |

Final Core container restart proof: started `2026-08-17T21:53:40.985856445Z`, container PID `3219193`, service active. `/health/ready` reported build commit `d8c80e08715d6dbf9a95e3066dee71d2d3067437`, image identity `animus-prime-core:continuation-085-warm-start-final`, and schema `0039_usage_limits_and_upgrade_preflights.sql`. `/health/live` returned `{"status":"live","service":"prime-core"}` after startup. Public exposure and deployment were not performed.

## Warm Start qualification

The operator selected the existing Qualification Project through the genuine PRIME UI, opened the Warm Start surface, previewed the bounded source list, and selected only:

- `.agent/PROJECT_GOAL.md` — authoritative, current, revision `3dec45e1b225840398379113e83391dba03866ac`.
- `.agent/CURRENT.md` — authoritative, current, revision `3dec45e1b225840398379113e83391dba03866ac`.

The existing Notion candidate was shown as `RETRACTED` and disabled. No Notion content was admitted and no replacement page/source was created.

Initial execution exposed one product defect: the route attempted invalid database content classes `AUTHORITY` and `KNOWLEDGE`, producing a PostgreSQL check-constraint failure. The minimal repair mapped the bounded sources to existing classes: Goal=`CONSTRAINT`, Current/other state=`OBSERVATION`, Learning=`LEARNING`, records/directives=`DECISION`.

After the repair, the real browser execution completed with no browser console errors. Hindsight was concurrently consolidating the long selected authority payload, so the first durable admissions carried adapter status `UNAVAILABLE/DEGRADED`; the primary PRIME memory records and Warm Start events persisted. After native Hindsight consolidation completed (`22 processed`, `131.811s`), PRIME memory reread returned both Warm Start documents with `status=CURRENT`, the expected `CONSTRAINT`/`OBSERVATION` classes, source revisions, source references, and the existing project bank `prime-project_d9a1a5b609394282b62fc12c0d04634d`.

The final repeat through the browser returned:

`Warm Start CURRENT: admitted 2, deduplicated 2, skipped 0, rejected 0.`

This proves explicit-selection behavior and content-hash/project deduplication. The service now reports `PARTIAL` whenever a newly admitted item itself is degraded, so a transient adapter delay cannot be presented as a false current success.

## Operator/runtime checks

- Protected UI/authentication: `PASSED`.
- Existing Qualification Project selection: `PASSED`.
- Warm Start preview and explicit selection: `PASSED`.
- Warm Start execution and repeat deduplication: `PASSED`.
- Secret-looking content refusal policy: covered by focused static contract; no secret was printed or persisted in evidence.
- Project isolation: `PASSED` by existing project-scoped bank and source-reference paths; no other project was selected or mutated.
- Core restart and build provenance: `PASSED`.
- Hindsight settle/reread: `PASSED` after native consolidation.
- Browser console errors during final Warm Start flow: none observed.

## Governance result

No complete frozen requirement was promoted in this continuation. DOD-031 remains open because the complete clause requires a legitimate non-empty operator-selected Notion source; the only existing candidate is retracted/blank. The queue therefore remains `68 complete / 13 open`. DOD-005 remains already `PRODUCT_VERIFIED`; DOD-081, R-056, Phase 15, V1, public exposure, deployment, and Phase 16 remain unchanged.

## Validation

- Warm Start focused tests plus Continuation 084 focused tests: `PASSED` — `3 passed`.
- Compileall: `PASSED`.
- Diff check: `PASSED`.
- Supported full regression using Atlas repository virtualenv: `PASSED` — `124 passed / 29 skipped / 0 failed`.
- System Python full regression attempt: `NOT APPLICABLE` to governed result — collection failed because system Python lacks repository `psycopg`; rerun with established `.venv` passed.
- Governance validation `--mode ADOPTED`: `PASSED`.
- Product gap burndown validation: `PASSED` — `81 total`, `68 complete`, `13 burndown`.
- Product alignment audit: existing audit output remains `PRODUCT_ALIGNMENT_AUDIT: PASS`; its historical `V1_PRODUCT_GOAL_ALIGNMENT: FAIL` is the known non-release gate.
- Core/Hindsight/PostgreSQL/Node health: `PASSED`.
- Browser operator qualification: `PASSED` for the bounded Warm Start flow; complete DOD-031 remains open.
- Public deployment/exposure/Funnel change: `NOT PERFORMED`.

## Changed files and commits

- `src/prime_core/warm_start_service.py`
- `apps/core/main.py`
- `apps/web/index.html`
- `tests/phase15/test_continuation085_warm_start.py`
- this evidence file and append-only governance records

Product implementation lineage:

- `6085d52e20dcd7173ec28868785a3852bd25f5df` — bounded Warm Start route/service/UI.
- `3dec45e1b225840398379113e83391dba03866ac` — valid memory-class mapping repair.
- `d8c80e08715d6dbf9a95e3066dee71d2d3067437` — truthful degraded-admission status repair and final qualified runtime provenance.

## Remaining blockers

- DOD-031: operator-approved legitimate non-empty Notion knowledge source is still required; do not manufacture one.
- DOD-004: full multi-system interruption/orphan/reconciliation breadth.
- DOD-013: approved private Tailscale Serve and second-device qualification.
- DOD-016: complete fork isolation with independent live Notion/Hindsight targets.
- DOD-044: fresh-install target and complete setup recovery browser matrix.
- DOD-047: authoritative provider-backed cost attribution.
- DOD-049: approved independent restore target.
- DOD-053: legitimate second enrolled LAN machine.
- DOD-055: legitimate fresh creation target and complete interruption/recovery negatives.
- DOD-077: authorized positive destructive deletion and complete audit/recovery matrix.
- DOD-079: Linux native install/service qualification and separate supported Windows host evidence.
- DOD-080: complete frozen visual/operator polish acceptance.
- DOD-081/R-056: aggregate release qualification remains last and gated.

No synthetic project, repository, Node, Notion page, bank, public listener, deployment, or Phase 16 artifact was created.
