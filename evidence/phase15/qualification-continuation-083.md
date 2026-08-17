# ANIMUS PRIME — Phase 15 Qualification Continuation 083

## Outcome

`PARTIAL` — the authorized Atlas qualification lab produced real product evidence and closed two local architectural gaps, but the supported regression remains `112 passed / 29 skipped / 6 failed`, and several complete frozen clauses still require legitimate external environments or browser-positive paths. No V1, Phase 16, deployment, or public exposure claim is made.

## Baseline and governed state

- Starting governed PRIME commit: `48567c8da47df12ab91a404177157f59fa36864b`
- Starting qualification queue: `62 complete / 19 open`
- Starting implementation: `c850aa947882cf78138bb245f9cd42d11323decb`
- Working Atlas checkout: `/home/sketch/Projects/ANIMUS_PRIME`
- Execution boundary: direct Atlas SSH; no `Z:` path used for runtime execution
- Canonical Qualification Project: preserved and not terminally completed, deleted, rebound, or destructively restored
- Unrelated pre-existing untracked `.codebase-memory/`, `.prime-evidence/`, and `.vscode/` were preserved

## Persistent runtime

| Component | Result |
| --- | --- |
| PRIME Core | `animus-prime-core:continuation-083`, container running |
| Core build commit | `b72b6534e1d7a9d25be631a35ed926fd1fda8dcd` |
| Core readiness | `READY`, `PRIME-SPEC-V1.0.0`, schema `0039_usage_limits_and_upgrade_preflights.sql` |
| Core service | `animus-prime-core.service`, user systemd, active; MainPID observed `2606391` |
| Core listener | private `127.0.0.1:8000` inside the established Atlas tunnel |
| Web UI | genuine `apps/web/index.html` served by PRIME Core |
| PostgreSQL | existing persistent PRIME database, reused |
| Hindsight | existing persistent service, reused; current browser health reported connectivity/retain/recall/Reflect/Mental Models available after runtime restart |
| Repository Node | existing `node-041-atlas-native`, ONLINE through the enrolled private control plane |
| Core mounts | read-only `/home/sketch/Projects` plus existing writable `/var/lib/animus-prime-core` state mount |
| Notion credential | existing host file `/home/sketch/.config/animus-prime/notion-runtime.env`, mode `0600`; passed to the PRIME-owned container without recording its value |
| Public exposure | not performed; Funnel/Tailscale configuration not changed |
| Rollback | prior PRIME containers retained stopped as rollback artifacts; no unrelated service replaced |

## Qualification lab and fixtures

The user-authorized lab is durable and tracked at:

`/home/sketch/ANIMUS_PRIME_V1_QUALIFICATION_LAB/083`

The lab ledger carries the marker `V1_QUALIFICATION_FIXTURE`. The canonical fixture project was created through the normal PRIME path:

- project: `project_ab2cb29717864418a05352542fc5ac19`
- name: `V1_QUALIFICATION_FIXTURE_083`
- repository: `repo_b1fcb6db7e70492eaaf77c312dd4db0e`
- repository path: `/home/sketch/Projects/ANIMUS_PRIME_V1_QUALIFICATION_FIXTURE_083`
- committed source revision: `392e728eff4ea7437a5214e1d15173229ba8e85c`
- approved GoalRevision: `goal_0936938e650644039000b558e5505daf`
- goal hash: `49180a3052c0af4b17002f96786f3c9e9806412f26395d4f90185faa3d06d4fa`

A normal PRIME fork was also created and its temporary MCP grant was revoked immediately after the bounded fork/isolation check. No token was written to evidence, Git, Notion, or PRIME durable state.

The rebind fixture used two no-hardlink Git clones under the enrolled Atlas root. It was intentionally separate from the primary fixture and was not used as production truth.

## Product evidence

### Goal, authority, registration, and lifecycle

- Existing fixture Goal was reviewed and approved; an unchanged approved Goal replacement was refused unless explicit new-revision intent was supplied.
- An explicit Goal revision was then approved on the fork fixture with a new content hash; the prior approved revision became `SUPERSEDED`.
- Existing authority review/adoption remained idempotent and did not rewrite valid authority files.
- Registration refusal paths passed for traversal, outside allowed root, missing path, duplicate repository, missing confirmation, malformed repository name, outside parent, and existing target.
- Lifecycle direct qualification passed `ACTIVE → PAUSED → ACTIVE → COMPLETION_REVIEW → ACTIVE → COMPLETION_REVIEW → COMPLETED` on the isolated fork fixture. Completion required exact project identity and recent step-up.
- Wrong-target completion was refused without mutation; replaying a consumed lifecycle preflight was refused.
- The real browser qualified fixture selection, Overview, Goal, Integrity, repository tree, Authority, lifecycle PAUSE preflight/confirmation, and RESUME.

### Shared operator retrieval

Against the real persistent UI and fixture:

- Ask query: `What does AGENTS.md say about code exploration?`
- Result: substantive grounded answer, source class `Authority`, source id `AGENTS.md`, source revision `0cbc5d01bf304d532676aeb0ca5d80cd99d7abba`, content hash present, epistemic class `SOURCE FACT`.
- Search query: `project isolation`
- Result: `10 project-scoped result(s)` with grouped Repository, Authority, and current Notion Knowledge hits; Notion source id `continuation-083-warm-start-knowledge-v2`, revision `143600000`, freshness `CURRENT`.
- Repository tree used the live Node path after the Core container received the approved read-only `/home/sketch/Projects` mount.
- Browser Notion status was `CONNECTED` after the existing secure credential reference was made available inside the PRIME container. No raw credential was displayed.

### Source lifecycle / DOD-005

Using the existing PRIME project fixture and approved Notion sandbox pages:

1. attached source state was refreshed as `CURRENT`;
2. detaching the same source made the derived Search result disappear while one historical observation remained;
3. reuse of the terminal detached binding was refused by the established lifecycle contract;
4. a separate operator-approved v2 sandbox page attached under a new binding and returned as current Search Knowledge.

This qualifies the current-view retraction and retained historical provenance invariant. It does not claim purge qualification.

### Backup / restore boundary

- Product backup created an encrypted fixture continuity bundle at `/home/sketch/ANIMUS_PRIME_V1_QUALIFICATION_LAB/083/restore/fixture-083-continuity.bundle`.
- SHA-256: `40ce30b627a60cfe3ee935626089400b8426a978d6ef1eddc97b98b6c6aeb459`
- Product preflight returned `READY`, continuity `true`, schema `0039_usage_limits_and_upgrade_preflights.sql`, seven components.
- Restore against the live shared PRIME database refused safely with `restore collision: target PRIME already contains projects`; no replacement restore was attempted.
- A separate approved restore target remains required for complete DOD-049/R-042 closure.

### Durable workflow interruption and recovery

An actual PRIME workflow on the fixture recorded a repository resource, completed a preparation step, entered a non-idempotent external step, and was interrupted. Resume planning returned `REPAIR_REQUIRED` with an explicit ambiguity. After operator reconciliation, the step was repaired and the workflow completed all steps. The resource was then marked `RELEASED` with a retained fixture locator.

### Rebind repair and qualification

Observed failure: a valid relocation preflight returned `LOGICAL_REPOSITORY_CONTINUITY_VERIFIED`, but confirmation rejected it as `STALE_REBIND_PREFLIGHT`.

Root cause: the preflight snapshot omitted `candidate_path` and `candidate_location_fingerprint` even though confirmation compared both fields.

Minimal repair:

- `src/prime_core/service.py` now records both fields in the preflight snapshot;
- `tests/phase15/test_continuation050.py` contains a regression guard for the snapshot/confirmation contract.

Requalification passed: missing and outside-root destinations were refused; a real alternate fixture clone returned verified canonical commit and authority continuity; confirmation changed only the fixture binding to `REBOUND`, preserved project/repository identity, recorded history/audit, and replay was refused as stale.

## Starting 19-row qualification matrix

| DOD | 083 result | Governed disposition |
| --- | --- | --- |
| DOD-004 | Durable interruption/reconciliation fixture path passed; remaining fork/Notion/Hindsight/restore/archive/orphan breadth remains | Open, `BACKEND_ONLY` |
| DOD-005 | Current derived Notion/Search view retracted while historical provenance remained; separate current source reattached | Promote to `PRODUCT_VERIFIED` |
| DOD-013 | No private Tailscale Serve/second-device qualification performed | External gate |
| DOD-016 | Fork/project identity path passed; independent child Notion/Hindsight and complete browser contract not closed | External gate |
| DOD-024 | Fixture terminal completion passed directly; browser pause/resume passed; complete browser terminal contract remains | Partial |
| DOD-031 | Legitimate sandbox source exists and is searchable; complete warm-start operator path remains | External/resource gate |
| DOD-039 | Real alternate fixture relocation/rebind passed after minimal repair | Promote to `PRODUCT_VERIFIED` |
| DOD-044 | No fresh-install external browser target | External gate |
| DOD-047 | Provider-authoritative cost attribution remains unavailable | External gate |
| DOD-049 | Encrypted backup, hash, preflight, and collision refusal passed; independent restore target absent | Partial/resource gate |
| DOD-053 | No second enrolled LAN machine/project | External gate |
| DOD-054 | Registration refusal matrix and direct fixture binding passed; browser-positive registration remains | Partial |
| DOD-055 | Creation refusal paths and durable fixture creation passed; complete browser interruption/recovery remains | Partial |
| DOD-057 | Fresh fixture authority bootstrap plus adopt/review protection passed; complete browser provisioning remains | Partial |
| DOD-058 | Goal approval/protection and browser Goal rendering passed; guided browser workflow remains | Partial |
| DOD-077 | Wrong-target, step-up, confirmation, replay, and no-mutation negatives passed; positive deletion remains intentionally unrun | Partial |
| DOD-079 | Atlas Linux is available; supported native installer/reboot and Windows host remain absent | External gate |
| DOD-080 | Authenticated fixture flow, responsive product shell, visible status/focus, and clean browser path rechecked; full visual acceptance remains | Partial |
| DOD-081 | Aggregate release gate not attempted | Open/gated |

Expected governed queue after reconciliation: `64 complete / 17 open`; two newly promoted local architectural DODs are DOD-005 and DOD-039. R-056 remains open.

## Validation

- Rebind-focused tests: `6 passed`.
- Full supported regression: `112 passed / 29 skipped / 6 failed`.
- Phase 15 test collection: phase15 focused run `49 passed / 10 skipped / 6 failed`; the six failures are the same pre-existing AI execution and Continuation-059 source-assertion failures and are not caused by the rebind patch.
- Established `scripts/phase15_qualify.py` with `/home/sketch/.config/animus-prime/core.env` loaded: migration qualifications 1–14 passed, governance passed, the full regression failed with the same six failures, and the mechanically derived V1 alignment/release gate remained failed at `17/26` verified requirements. This is qualification evidence, not release clearance.
- Governance validator before 083 reconciliation: structural checks passed; product-goal alignment remained `FAIL` because the governed open queue and product audit had not yet been reconciled.
- Persistent readiness after final image swap: `PASSED`; no duplicate active Core.
- Browser operator qualification after final image: `PASSED` for the stated fixture flow; Ask/Search returned grounded/provenance-bearing results.
- Secret scan: raw credentials were not written to Git/evidence/Notion; the Notion env file remained host-only mode `0600` and was used only as a secure runtime reference.
- Public exposure/deployment: `NOT PERFORMED`.

## Changed files

- `.agent/DIRECTIVES.md` — append-only 083 directive entry
- `.agent/CURRENT.md`, `.agent/OUTCOMES.md`, `.agent/LEARNINGS.md`, `.agent/RECORD.md` — append-only 083 state and closure records
- `docs/v1-product-gap-burndown.yaml`, `docs/v1-product-goal-alignment-audit.yaml` — reconciled 64 complete / 17 open governed state and DOD-005/DOD-039 promotions
- `src/prime_core/service.py` — rebind snapshot continuity repair
- `tests/phase15/test_continuation050.py` — regression guard
- `evidence/phase15/qualification-continuation-083.md` — this record

## Remaining gates

- Six full-regression failures must be resolved or explicitly dispositioned before any release claim.
- DOD-013: approved private Tailscale Serve and second device.
- DOD-016/DOD-031: complete distinct child/project Notion/Hindsight warm-start qualification.
- DOD-044: fresh-install operator target.
- DOD-047/R-045: authoritative provider cost attribution.
- DOD-049/R-042: independent restore target.
- DOD-053: second enrolled LAN machine/project.
- DOD-054/055/057/058/077/080: remaining complete browser-positive or destructive clauses.
- DOD-079: supported native Linux installer/reboot plus an actual Windows host.
- DOD-081/R-056: aggregate end-to-end gate, only after prerequisites close.
- Phase 15 and V1: not complete.
