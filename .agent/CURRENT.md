# Current State

## Lifecycle

- Status: `ADOPTED`
- Last updated: 2026-08-18T14:00:00-04:00

## Active state after adoption

- Local directive ID: D-PRIME-PHASE15-FIRECRACKER-QUALIFICATION-090
- External directive ID: ANIMUS PRIME - Phase 15 Continuation 090
- Objective: Establish a bounded independent Firecracker Linux guest and exhaust the unlocked Node-backed onboarding, repository-creation/recovery, restore, and native-Linux qualification cluster.
- Current status: `COMPLETE`
- Acceptance: PASS for the bounded 090 objective, PARTIAL for Phase 15 — independent Firecracker guest and native Node qualified; DOD-044, DOD-049, and DOD-055 promoted; DOD-079 Linux half passed and Windows remains blocked. Governed queue is 72 complete / 9 open. DOD-081, R-056, Phase 15, V1, and deployment remain open or gated.
- Current phase: PHASE15_FIRECRACKER_QUALIFICATION_090
- Expected or actual touched areas: bounded Firecracker qualification infrastructure on /mnt/storage1tb, private TAP/nft/proxy with complete rollback, native Linux Node packaging and enrollment, Node-backed Core repository/authority/Goal/Warm Start repairs, continuity-backup repair, browser onboarding/creation/restore qualification, governed evidence, and append-only records. Canonical project, canonical Node, public exposure, deployment, and Phase 16 were preserved.
- Immediate next action: Awaiting reset and Architect review of the 9-row queue. DOD-004 is the expected next bounded engineering bottleneck; do not start Continuation 091 automatically.

## Temporary task-relevant facts

- Baseline PRIME-SPEC-V1.0.0; authoritative execution is direct SSH/native Atlas at /home/sketch/Projects/ANIMUS_PRIME; Continuation 083 used only the tracked authorized lab `/home/sketch/ANIMUS_PRIME_V1_QUALIFICATION_LAB/083` and fixtures marked `V1_QUALIFICATION_FIXTURE`.
- Starting PRIME state for Continuation 075 was 92e05b5199ea3901d92a1f83902cede0e0bc63e5; no PRIME source change occurred in this continuation.
- Persistent PostgreSQL, Hindsight, PRIME Core/UI, and canonical Node remain preserved. Hindsight remains healthy on 127.0.0.1:8888; the existing Hindsight image and PRIME bank were reused.
- Existing PRIME bank prime-project_d9a1a5b609394282b62fc12c0d04634d contains exactly one legitimate Mental Model, prime-operating-model, with substantive generated content and stored provenance.
- Exact 072 Reflect query remains the accepted source basis from Continuation 073: four native observation/recall calls and substantive provenance-bearing output. Continuation 074 created the model through the supported Hindsight operation.
- Canonical runtime image remains `animus-prime-core:continuation-086-warm-start-notion` at `1d1f421e0c6201a49bc2b305c73bd41547237577`. Qualification Appliances A/B ran exact bounded implementation `d882d9e0442be66f689911dec9379f8285b446b8`; no public exposure, Funnel change, canonical runtime replacement, or Phase 16 occurred.
- Approved Notion sandbox parent is `3be833cb-27ff-814f-af89-ebfc3a2a8aed`; project record page is `3be833cb-27ff-8159-add6-e883c1cc54af`; controlled probe child is `3be833cb-27ff-81aa-9fe2-ffb4fcf5f980`.
- Runtime Notion capability read/write, production adapter lifecycle, and the complete persistent browser projection/conflict/detach/history operator surface passed. DOD-034/035/036/064/065/066 are USER_USABLE_VERIFIED; detached sources remain RETRACTED and history is idempotent after restart. Continuation 079 Memory surfaces render existing project data with provenance/isolation. Continuation 086 qualified Warm Start selected `.agent` plus selected Notion fixture admission; Hindsight service/retain/recall are current while Reflect is currently unavailable and Mental Models unsupported.
- Continuation 090 established independent guest `prime090-fc`, Node `node-090-firecracker-linux`, approved root `/srv/prime-projects`, project `project_fc46bf826a24410b851ddc860eeb3b49`, repository `repo_760a4120576f4ac7b1c774ffbb0d2497`, and restore `restore_0b0bc75412bf4a85892c84b7b8baab55`. The guest is stopped after rollback; its disk/evidence remain preserved. Untracked `.codebase-memory/`, `.prime-evidence/`, and `.vscode/` remain preserved.

## Last validation after adoption

- Command or check: Continuation 090 Firecracker/native Node/browser qualification plus supported regression
- Result: `PASSED`

## Risks

- Durable multi-system workflows; R-045/DOD-047 provider cost; second LAN machine; Windows native lifecycle; Tailscale/second device; child Notion/Hindsight fork resources; terminal browser PURGE; complete polish; DOD-081; R-056; Phase 15/V1.

## Blockers

- ATLAS_PARAGON_SERVICE_RESTART_REQUIRES_INTERACTIVE_AUTH: RESOLVED by operator restart; new MainPID 607574 and private health verified.
- PRIME_RUNTIME_NOTION_CREDENTIAL_UNAVAILABLE: RESOLVED for the approved bounded credential path; raw token remains Atlas-only and is not governed data.
- PRIME_RUNTIME_NOTION_OPERATOR_WORKFLOW_UNQUALIFIED: RESOLVED by Continuation 076 persistent browser qualification and minimal lifecycle/idempotence repairs.
- AI_MEMORY_ACTIVITY_QUERY_RETURNED_MEMORY_AND_SESSION_IDENTITY_NOT_PERSISTED: RESOLVED by Continuation 080 durable MCP activity projection and restart qualification.
- PRIME_WARM_START_SELECTED_NOTION_SOURCE_UNAVAILABLE: RESOLVED for bounded Continuation 086 — explicit selected Notion fixture admitted through the real browser with source/revision/hash provenance; fixture remains non-authoritative.
- PRIME_QUALIFICATION_VM_RUNTIME_UNAVAILABLE: RESOLVED for Linux qualification by the bounded Firecracker 1.16.1 guest; no QEMU/libvirt stack was installed.
- PRIME_NATIVE_WINDOWS_QUALIFICATION_HOST_UNAVAILABLE: BLOCKED — DOD-079 requires an actual supported Windows host for native lifecycle qualification.

## Pending decisions

- Runtime Notion credential and backend lifecycle remain qualified; DOD-021/DOD-022 shared retrieval and grounding remain qualified; DOD-026 and DOD-076 remain promoted from 081; DOD-050 is promoted by 082; DOD-005 and DOD-039 are promoted by 083; DOD-031 is promoted by 086. Keep DOD-081/R-056 last and preserve exact external-resource gates.
- Keep the persistent topology preserved, provider/second-LAN/Windows/Tailscale gates truthful, DOD-081/R-056 last, and Phase 16/deployment out of scope. The independent restore, fresh Node-backed onboarding, repository-creation recovery, and Linux-native gates are now closed.

## Status vocabulary

ADOPTED is the repository governance lifecycle state. COMPLETE means the current directive is closed for its bounded scope and awaiting reset. PARTIAL records bounded acceptance with explicit remaining gaps.
