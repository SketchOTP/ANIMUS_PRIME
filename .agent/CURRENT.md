# Current State

## Lifecycle

- Status: `ADOPTED`
- Last updated: 2026-08-18T23:55:00-04:00

## Active state after adoption

- Local directive ID: D-PRIME-PHASE15-EXTERNAL-MACHINE-CONSOLIDATION-094
- External directive ID: ANIMUS PRIME - Phase 15 Continuation 094
- Objective: Use one genuine Windows machine to qualify the independent DOD-079 Windows Node lifecycle, DOD-053 second-LAN-machine project boundary, and DOD-013 private second-device Tailscale Serve boundary.
- Current status: `BLOCKED`
- Acceptance: BLOCKED at the required Windows Service Control Manager elevation and PRIME-owned private Serve boundaries. No DOD/R row was promoted; the queue remains 76 complete / 5 open.
- Current phase: PHASE15_EXTERNAL_MACHINE_CONSOLIDATION_094
- Expected or actual touched areas: read-only Windows/LAN/Tailscale discovery, expendable Windows qualification root, exact qualified source clone, unchanged installer attempt, Continuation 094 evidence, and append-only governance records. Canonical PRIME state, existing services, Funnel, and public boundary were preserved.
- Immediate next action: Resume 094 only from an interactive elevated Windows session with explicit host/reboot approval and a PRIME-owned private Serve route. Do not begin DOD-081/R-056 or Continuation 095.

## Temporary task-relevant facts

- Baseline PRIME-SPEC-V1.0.0; authoritative execution is direct SSH/native Atlas at /home/sketch/Projects/ANIMUS_PRIME; Continuation 083 used only the tracked authorized lab `/home/sketch/ANIMUS_PRIME_V1_QUALIFICATION_LAB/083` and fixtures marked `V1_QUALIFICATION_FIXTURE`.
- Starting PRIME state for Continuation 075 was 92e05b5199ea3901d92a1f83902cede0e0bc63e5; no PRIME source change occurred in this continuation.
- Persistent PostgreSQL, Hindsight, PRIME Core/UI, and canonical Node remain preserved. Hindsight remains healthy on 127.0.0.1:8888; the existing Hindsight image and PRIME bank were reused.
- Existing PRIME bank prime-project_d9a1a5b609394282b62fc12c0d04634d contains exactly one legitimate Mental Model, prime-operating-model, with substantive generated content and stored provenance.
- Exact 072 Reflect query remains the accepted source basis from Continuation 073: four native observation/recall calls and substantive provenance-bearing output. Continuation 074 created the model through the supported Hindsight operation.
- Canonical runtime image is `animus-prime-core:continuation-093-65e553f` at qualified implementation `65e553f084f5c5fba970ad7bf25c581ab15066ff`, image ID `sha256:82791590061475955dfbc1962264ee357acfb84066e7ba4bb15f965fdb861cdc`; readiness reports the same build and schema `0040_destructive_lifecycle_sagas.sql`. Prior rollback containers remain recoverable. No public exposure, Funnel change, deployment, or Phase 16 occurred.
- Approved Notion sandbox parent is `3be833cb-27ff-814f-af89-ebfc3a2a8aed`; project record page is `3be833cb-27ff-8159-add6-e883c1cc54af`; controlled probe child is `3be833cb-27ff-81aa-9fe2-ffb4fcf5f980`.
- Runtime Notion capability read/write, production adapter lifecycle, and the complete persistent browser projection/conflict/detach/history operator surface passed. DOD-034/035/036/064/065/066 are USER_USABLE_VERIFIED; detached sources remain RETRACTED and history is idempotent after restart. Continuation 079 Memory surfaces render existing project data with provenance/isolation. Continuation 086 qualified Warm Start selected `.agent` plus selected Notion fixture admission; Hindsight service/retain/recall are current while Reflect is currently unavailable and Mental Models unsupported.
- Continuation 090 established independent guest `prime090-fc`, Node `node-090-firecracker-linux`, approved root `/srv/prime-projects`, project `project_fc46bf826a24410b851ddc860eeb3b49`, repository `repo_760a4120576f4ac7b1c774ffbb0d2497`, and restore `restore_0b0bc75412bf4a85892c84b7b8baab55`. The guest is stopped after rollback; its disk/evidence remain preserved. Untracked `.codebase-memory/`, `.prime-evidence/`, and `.vscode/` remain preserved.
- Continuation 091 qualified live process-death recovery on fixture `project_cd318a4bb4234d99afabc20f2cc3e013`: exit 91 after one live Notion page creation, restart on exact image, exact marker count one, workflow `workflow_79ffaeba9a644fd59492aeac379d5519` SUCCEEDED through PAGE_BOUND.
- Continuation 092 qualified one real expendable project through durable DELETE and PURGE. Live Notion archive, Node repository quarantine, credential revocation, Hindsight bank purge, and local-resource purge each survived injected Core exit 91 and resumed the same workflow without duplicate resources. The real browser also passed Cancel/focus, step-up, exact identity, disclosure, DELETE, PURGE, terminal clearing, refresh, and narrow-viewport checks.
- Continuation 093 created the legitimate child `project_db3ef8c4bc834e68a2e9a9deabbb5a80` at exact source revision `252d71466b92fa3d7979a1b79f02898271b287c1`, with separate repository, Goal/baseline, MCP grant, Notion page, Hindsight bank, Brain, memory, and activity. Replay and restart did not duplicate state. Persistent gstack Playwright tooling lives outside PRIME under `/mnt/storage1tb/prime-tooling/gstack-playwright`.

## Last validation after adoption

- Command or check: Continuation 094 host discovery, exact-source acquisition, unchanged Windows installer attempt, Atlas listener/Serve ownership inspection
- Result: BLOCKED

## Risks

- R-045/DOD-047 authoritative provider cost; DOD-053 second enrolled LAN machine; DOD-079 Windows native lifecycle/elevation; DOD-013 PRIME-owned private Serve/second device; DOD-081/R-056; Phase 15/V1.

## Blockers

- ATLAS_PARAGON_SERVICE_RESTART_REQUIRES_INTERACTIVE_AUTH: RESOLVED by operator restart; new MainPID 607574 and private health verified.
- PRIME_RUNTIME_NOTION_CREDENTIAL_UNAVAILABLE: RESOLVED for the approved bounded credential path; raw token remains Atlas-only and is not governed data.
- PRIME_RUNTIME_NOTION_OPERATOR_WORKFLOW_UNQUALIFIED: RESOLVED by Continuation 076 persistent browser qualification and minimal lifecycle/idempotence repairs.
- AI_MEMORY_ACTIVITY_QUERY_RETURNED_MEMORY_AND_SESSION_IDENTITY_NOT_PERSISTED: RESOLVED by Continuation 080 durable MCP activity projection and restart qualification.
- PRIME_WARM_START_SELECTED_NOTION_SOURCE_UNAVAILABLE: RESOLVED for bounded Continuation 086 — explicit selected Notion fixture admitted through the real browser with source/revision/hash provenance; fixture remains non-authoritative.
- PRIME_QUALIFICATION_VM_RUNTIME_UNAVAILABLE: RESOLVED for Linux qualification by the bounded Firecracker 1.16.1 guest; no QEMU/libvirt stack was installed.
- PRIME_NATIVE_WINDOWS_QUALIFICATION_HOST_UNAVAILABLE: RESOLVED as a host-discovery blocker — a genuine supported Windows host is identified; native qualification remains blocked by the separate elevation/service boundary.
- PRIME_NATIVE_WINDOWS_SERVICE_ELEVATION_UNAVAILABLE: BLOCKED — a genuine Windows host was identified, but the current Codex shell cannot cross the interactive UAC boundary; the unchanged installer failed at OpenSCManager with Access denied.
- PRIME_PRIVATE_SERVE_ROUTE_UNAVAILABLE: BLOCKED — the current Tailscale Serve map has no PRIME UI route; existing Funnel and other routes were preserved and not reused.
- PRIME_EXTERNAL_RELEASE_PREREQUISITES: BLOCKED — DOD-013, DOD-047, DOD-053, and DOD-079 require legitimate external resources; local code/browser qualification is exhausted.

## Pending decisions

- Runtime Notion credential and backend lifecycle remain qualified; DOD-016 and DOD-080 are promoted by 093. Keep DOD-081/R-056 last and preserve the four exact external-resource gates. Continuation 094's Windows candidate is not yet a qualified target because the required elevation and PRIME-owned Serve path are unavailable.
- Keep the persistent topology preserved, provider/second-LAN/Windows/Tailscale gates truthful, DOD-081/R-056 last, and Phase 16/deployment out of scope. The independent restore, fresh Node-backed onboarding, repository-creation recovery, and Linux-native gates are now closed.

## Status vocabulary

ADOPTED is the repository governance lifecycle state. COMPLETE means the current directive is closed for its bounded scope and awaiting reset. PARTIAL records bounded acceptance with explicit remaining gaps.
