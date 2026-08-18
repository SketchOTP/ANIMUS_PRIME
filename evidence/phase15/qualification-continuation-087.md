# ANIMUS PRIME — Phase 15 Qualification Continuation 087

## Acceptance

**PARTIAL — bounded local qualification and resource-gate normalization completed.**

This continuation started from the governed Atlas checkout at
`8b4efaf380285a9712bceab452ce11f1d4dfc00a`, which matched `origin/main` and
GitHub `main`. No PRIME product implementation change was required. The
qualification work used only the existing persistent Atlas topology and the
authorized, explicitly marked Qualification Lab fixtures. The canonical
Qualification Project and enrolled Atlas Node were not replaced or reset.

The 086 evidence body contained a stale final-publication SHA (`8e36ab5...`).
The append-only correction for this continuation is that the actual 086
governed baseline was `8b4efaf380285a9712bceab452ce11f1d4dfc00a`; the final
087 publication is the SHA recorded in the final closeout below. The historical
086 record is not rewritten.

## Baseline and topology

- Frozen specification: `PRIME-SPEC-V1.0.0`
- Atlas checkout: `/home/sketch/Projects/ANIMUS_PRIME`
- Starting local HEAD: `8b4efaf380285a9712bceab452ce11f1d4dfc00a`
- Starting `origin/main`: `8b4efaf380285a9712bceab452ce11f1d4dfc00a`
- Starting worktree: clean except preserved untracked `.codebase-memory/`,
  `.prime-evidence/`, and `.vscode/`
- PostgreSQL: existing `animus-prime-phase0-postgres-1`, reused
- Hindsight: existing `mimir-hindsight-production`, reused
- PRIME Core: existing `animus-prime-core.service` / persistent Core container,
  private Atlas listener and `/health/ready` previously verified 200
- PRIME Web UI: genuine UI served through the persistent Core path and the
  existing authenticated browser tunnel
- Repository Node: existing `node-041-atlas-native` through the existing
  PRIME-owned service; no replacement Node created
- Public exposure: **NOT PERFORMED**; unrelated Tailscale Serve/Funnel state
  was inspected and left untouched

## Qualification work and evidence

### Isolated restore/recovery harness

The existing `/home/sketch/ANIMUS_PRIME_V1_QUALIFICATION_LAB` was reused. The
following isolated fixture databases were created in the existing PostgreSQL
cluster for this bounded run and were not confused with production state:

- `prime087_restore`
- `prime087_fresh`
- `prime087_fork`

The approved continuation-037 harness was rerun with its evidence root at
`/var/lib/animus-prime-core/qualification-087/evidence`. Results:

- Hindsight A/B bank isolation: **PASSED**
- correction supersede and tombstone: **PASSED**
- R-044 restore status: **VERIFIED** within the harness boundary
- backup ID: `backup_f2257be7e3e64cc99fd91f77f5f32611`
- evidence hash: `77eb6e6989e60bc9907af9abd31fe52013bcdeac0a5328e2ddd3276dbd3cccda`
- Git bundle hash: `e73bd876e96dc58ff13f88bd20e7882117e458aaf80e328db8c4765b04bffafa`
- Hindsight outage: `UNAVAILABLE`, with source-ledger recovery `CURRENT`
- restored: `1`; eligible: `1`; superseded/tombstoned sources excluded
- missing component: `REFUSED_MISSING_REQUIRED_COMPONENT`
- corrupt bundle: `REFUSED_CORRUPT_COMPONENT_OR_ARCHIVE`
- component fidelity: PostgreSQL EXACT; evidence EXACT_FOR_MANAGED_BYTES;
  historical state EXACT; retained Git checkpoints EXACT; Hindsight
  SOURCE_LEDGER_REBUILD / REBUILDABLE_NOT_BIT_IDENTICAL; secrets require
  reprovisioning

This harness is not claimed as complete DOD-049 closure: the full frozen
operator restore journey through the browser and restart/requalification of a
restored Core instance remains open.

### Browser qualification

The real authenticated PRIME UI was used against the persistent Core path.
The canonical Qualification Project remained protected. The existing marked
`V1_QUALIFICATION_FIXTURE_083` was used only as the expendable deletion target.

- Project selection and identity: **PASSED** for the canonical project and
  explicitly marked fixture
- Product route sweep: Home, Projects, Needs Attention, System Health,
  Overview, Ask PRIME, Search, Goal, Progress, Repository, Authority, Memory,
  Warm Start, Project Brain, Time Lens, Knowledge, Evidence, Activity, AI
  Connections, and Settings all reached the genuine UI routes
- Browser console errors after the clean sweep: **none observed**
- Keyboard focus: visible focus outline observed on the active button
- Narrow viewport at 375x812: no horizontal overflow observed
- Deletion refusal/step-up: exact fixture identity and recent step-up were
  required and recorded
- Positive deletion initiation: **PASSED** to
  `COMPLETED -> DELETION_PENDING` on the expendable fixture
- Terminal deletion and downstream cleanup: **NOT QUALIFIED**; a second
  attempt remained `DELETION_PENDING` and was not forced

The UI contains 734 historical project/node records in the current persistent
installation. That is preserved user state, not a reason to delete records;
it also prevents claiming the complete visual-polish acceptance for DOD-080.

## Complete 087 disposition matrix

| DOD | Starting status | 087 disposition | Exact remaining gate |
|---|---|---|---|
| DOD-004 | `BACKEND_ONLY` | Remains open; no complete cross-system promotion | `FULL_DURABLE_MULTI_SYSTEM_INTERRUPTION_RECONCILIATION_REQUIRED` |
| DOD-013 | `BACKEND_ONLY` | External gate confirmed; unrelated Tailscale listeners preserved | `ACTUAL_SECOND_APPROVED_TAILNET_DEVICE_REQUIRED` |
| DOD-016 | `IMPLEMENTED_NOT_PRODUCT_QUALIFIED` | Local fork foundations observed; complete child-resource contract not proven | `LEGITIMATE_DISTINCT_CHILD_NOTION_PROJECT_RECORD_AND_CHILD_HINDSIGHT_TARGET_REQUIRED` |
| DOD-044 | `IMPLEMENTED_NOT_PRODUCT_QUALIFIED` | Isolated fresh database exists, but no complete fresh browser/restart journey | `LEGITIMATE_FRESH_INSTALL_BROWSER_TARGET_REQUIRED_FOR_COMPLETE_ONBOARDING` |
| DOD-047 | `PARTIAL` | Provider is reachable, but authoritative cost attribution is absent | `APPROVED_PROVIDER_PROFILE_WITH_AUTHORITATIVE_COST_ATTRIBUTION_REQUIRED_FOR_REMAINING_CLAUSE` |
| DOD-049 | `PARTIAL` | Harness restore/recovery passed; browser restore/restart remains open | `RESTORE_BROWSER_RESTART_OPERATOR_REQUALIFICATION_REQUIRED` |
| DOD-053 | `BACKEND_ONLY` | Second-machine clause remains external; no second device invented | `ACTUAL_SECOND_ENROLLED_LAN_MACHINE_REQUIRED` |
| DOD-055 | `IMPLEMENTED_NOT_PRODUCT_QUALIFIED` | Creation foundations and negative paths preserved; interrupted browser journey not complete | `LEGITIMATE_BROWSER_CREATION_INTERRUPTION_TARGET_REQUIRED` |
| DOD-077 | `PARTIAL` | Exact identity, step-up, audit initiation, and pending state verified; terminal positive deletion not complete | `PRODUCT_TERMINAL_DESTRUCTIVE_DELETE_COMPLETION_REQUIRED_ON_EXPENDABLE_FIXTURE` |
| DOD-079 | `BLOCKED_BY_ENVIRONMENT` | Existing native Atlas Node inspected; clean installer walk-through not run | `CLEAN_NATIVE_LINUX_INSTALL_TARGET_REQUIRED; ACTUAL_SUPPORTED_WINDOWS_HOST_REQUIRED` |
| DOD-080 | `PARTIAL` | Route, focus, narrow viewport, and console checks passed; complete visual matrix remains open | `COMPLETE_FROZEN_VISUAL_OPERATOR_POLISH_ACCEPTANCE_REQUIRED` |
| DOD-081 | `IMPLEMENTED_NOT_PRODUCT_QUALIFIED` | Aggregate gate remains open because the rows above remain open | `R-056_COMPLETE_FROZEN_RELEASE_QUALIFICATION_REQUIRED` |

R-056 remains open. Phase 15 remains incomplete. V1 is not declared. Phase 16
and deployment/public exposure were not performed.

## External-resource ledger

The following are concrete prerequisites, not invitations to manufacture
fixtures: an approved second Tailscale device and private PRIME target; a
legitimate second enrolled LAN machine/project target; an approved provider
profile with authoritative usage/cost attribution; a supported Windows host; a
clean supported Linux install target; a legitimate fresh/unbound onboarding
target; and a browser/restart target for complete restore qualification.

## Validation

- Isolated restore/recovery harness: **PASSED** within stated fixture boundary
- Real browser bounded route/security/responsive checks: **PASSED**
- Full supported regression: **PASSED — 125 passed / 29 skipped / 0 failed**
- Governance and burndown validation: **PASSED**
- Compile/static and diff checks: **PASSED**
- Secret scan: **PASSED** — no raw credential values detected; pattern hits were repository detection logic or historical non-secret text
- Final Git parity: **PASSED** after publication; local HEAD, `origin/main`, and GitHub `main` matched

Notion checkpoint: [Phase 15 Product Completion Checkpoint 087 — 8f99cec](https://app.notion.com/p/3c0833cb27ff813c84a7f6a8b17225a5?pvs=204). The checkpoint and main SOT were updated and read back against the final governed publication.

No raw credentials, tokens, or secret values are present in this evidence.
