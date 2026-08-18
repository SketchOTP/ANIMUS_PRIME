# ANIMUS PRIME — Phase 15 Continuation 086

## Verdict

`PARTIAL` for the bounded qualification-lab and reconciliation scope. `DOD-031` is now `USER_USABLE_VERIFIED`. The remaining V1 rows, `DOD-081`, `R-056`, Phase 15, and V1 remain open or gated. No deployment, public exposure, Funnel change, frozen-spec change, or Phase 16 occurred.

## Baseline and scope

- Frozen specification: `PRIME-SPEC-V1.0.0`.
- Authoritative checkout: `/home/sketch/Projects/ANIMUS_PRIME` on Atlas.
- Starting local and published baseline: `f072cfac39b012746a94426343a09e13f3bbd337`.
- Product implementation commit: `1d1f421e0c6201a49bc2b305c73bd41547237577` (`fix warm start current Notion source admission`).
- Final governed publication commit: `8e36ab5394eb70624fad3b3ddb7a504f5d31d973`.
- Starting worktree: preserved untracked `.codebase-memory/`, `.prime-evidence/`, and `.vscode/`; no unrelated files were removed or staged.
- This continuation used only the existing Qualification Project, the existing enrolled Atlas Node, and one explicitly marked qualification fixture.

## Persistent Atlas topology

| Component | Evidence |
|---|---|
| PostgreSQL | Existing persistent `animus-prime-phase0-postgres-1`; reused, not replaced. |
| Hindsight | Existing persistent `mimir-hindsight-production` at private `127.0.0.1:8888`; service/retain/recall were current during this run, while Reflect was currently `UNAVAILABLE` and Mental Models `UNSUPPORTED`. Historical `prime-operating-model` qualification is preserved. |
| Repository Node | Existing enrolled `node-041-atlas-native`; reused for the real Qualification Project. |
| PRIME Core | `animus-prime-core.service`, persistent container `animus-prime-core:continuation-086-warm-start-notion`, container `82a60bc5a051...`, started `2026-08-17T23:44:46.750773716Z`; `/health/ready` passed with build `1d1f421...`, schema `0039`. |
| PRIME UI | Existing genuine Web UI through the persistent Core; browser access used the established SSH private tunnel to `127.0.0.1:8000`. |
| Startup/recovery | Existing Atlas service/runtime path preserved; Core was restarted with the corrected persistent configuration and recovered with the same project/database/runtime state. |
| Public exposure | `NOT PERFORMED`; unrelated existing Tailscale Funnel was not modified. |

The first replacement container attempt exposed stale build-metadata environment variables. It was preserved for rollback, not deleted. The final container uses a protected mode-600 runtime environment with only secure credential references and runtime configuration; no raw token entered Git, evidence, Notion, browser output, or logs.

## DOD-031 Warm Start qualification

The operator-approved fixture page was created under the approved Notion sandbox parent:

- Page: `V1_QUALIFICATION_FIXTURE — PRIME Warm Start Knowledge`.
- Page ID: `3bf833cb-27ff-8135-8df9-db7c90c7f80c`.
- URL: `https://app.notion.com/p/3bf833cb27ff81358df9db7c90c7f80c?pvs=204`.
- The page content explicitly identifies itself as `V1_QUALIFICATION_FIXTURE`, non-authoritative, project-isolated, provenance-bearing, and reversible. It was not used as authoritative project truth.

The real PRIME browser attached the page to the existing Qualification Project (`project_d9a1a5b609394282b62fc12c0d04634d`) with binding `continuation-086-warm-start-knowledge`. Refresh returned `ATTACHED`, revision `232300000`. The final single-submit browser run returned:

```text
Warm Start CURRENT: admitted 3, deduplicated 3, skipped 0, rejected 0.
```

The admitted set was bounded to the selected high-value `.agent` records plus the selected Notion source. `.agent/PROJECT_GOAL.md` and `.agent/CURRENT.md` were current at revision `1d1f421...`; the larger `.agent` records were skipped by the bounded file-size policy. The Notion candidate was current, content-available, and carried revision `232300000`, content hash `a4bfbc...`, source class `NOTION_KNOWLEDGE`, and the fixture binding. A durable PRIME memory row was created with memory ID `memory_e6e3a4632e26407e8af7b954ddd6187a`, source reference `source_9adad...`, and the same source revision/binding. The activity record contained the source locator, class, hash, revision, and truthful `DEGRADED` admission status because Hindsight's current derived capability was unavailable.

### Repair

- Observed failure: a real current attached Notion source was shown as unavailable to Warm Start.
- Root cause: `warm_start_service.py` admitted content only when lifecycle status equaled `ATTACHED`, while the canonical search projection correctly reported an attached source as `CURRENT`.
- Minimal repair: accept both `ATTACHED` and `CURRENT` for content-available selected Notion candidates; no new integration or source system was added.
- Test: `tests/phase15/test_continuation085_warm_start.py` focused suite passed, including the current-source admission case.
- Requalification: real browser attach, refresh, preview, one clean submit, durable memory query, and activity/source provenance inspection passed.

Earlier stale concurrent browser submissions remain recorded in the network history, including one duplicate-hash `500` from overlapping requests. The clean reloaded single-submit run passed and the durable result is append-safe; this history was not erased or relabeled.

## Other bounded dispositions

- `DOD-004`: remains `BACKEND_ONLY`; the Qualification Lab did not complete the full multi-system interruption/orphan/reconciliation breadth across Fork, Notion, Hindsight, restore, archive, and recovery.
- `DOD-013`: remains open; private second-device/Tailscale qualification requires a separately owned legitimate target. Existing unrelated Funnel was untouched.
- `DOD-016`: remains open/partial. The real UI fork attempt safely refused because the canonical source worktree contains preserved untracked artifacts. No artifacts were deleted and no child project was created.
- `DOD-031`: promoted to `USER_USABLE_VERIFIED`; complete bounded Warm Start clause passed with selected `.agent` and selected Notion knowledge, provenance, isolation, durable admission, and truthful degraded behavior.
- `DOD-044`: remains partial; no fresh install target was manufactured.
- `DOD-047`: remains partial; authoritative provider cost data is still unavailable.
- `DOD-049`: remains open; no independent restore target exists and canonical persistent data was not destructively restored.
- `DOD-053`: remains open; no legitimate second enrolled LAN machine/project target exists.
- `DOD-055`: remains partial; creation-negative/recovery behavior still needs a legitimate fresh target.
- `DOD-077`: remains partial; protected negative deletion paths passed, but no explicit approved destructive target was available for a positive deletion.
- `DOD-079`: remains blocked by environment; packaging files exist, but complete Linux service-install and Windows native qualification were not claimed.
- `DOD-080`: remains partial; complete frozen visual/operator polish acceptance is not yet qualified.
- `DOD-081` / `R-056`: remain gated; no aggregate release claim was made.
- `DOD-005`: remains closed and was not reopened.

## Validation

- Focused Warm Start tests: `PASSED` — 3 passed.
- Phase 15 suite: `PASSED` — `62 passed, 10 skipped` using the established Atlas `PYTHONPATH` and isolated lab `TMPDIR`.
- Full supported regression: `PASSED` — `125 passed, 29 skipped, 0 failed`.
- Browser: `PASSED` for the bounded real Chromium Warm Start workflow through the established private Atlas tunnel; stale concurrent request history is preserved as a concern, clean single-submit qualification passed.
- Runtime health: `PASSED` for PRIME Core readiness and persistent topology recovery.
- Governance/burndown/alignment/diff/secret checks: recorded at closeout after this evidence reconciliation.

An initial test invocation without the established Atlas environment failed collection or later encountered the host `/tmp` quota. It was not treated as governed qualification. The supported rerun used `/home/sketch/ANIMUS_PRIME_V1_QUALIFICATION_LAB/086/tmp` and passed without deleting unrelated data.

## Queue and closeout

The governed queue changes from `68 complete / 13 open` to `69 complete / 12 open` by promoting only `DOD-031`. The external-environment class reduces from 6 to 5. Final governed parity is `8e36ab5394eb70624fad3b3ddb7a504f5d31d973 == origin/main == GitHub main`.
