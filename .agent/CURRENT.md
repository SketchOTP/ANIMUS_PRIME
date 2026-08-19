# Current State

## Lifecycle

- Status: `ADOPTED`
- Last updated: 2026-08-19T15:15:00-04:00

## Active state after adoption

- Local directive ID: D-PRIME-PHASE15-R045-CAPACITY-CLOSURE-096G
- External directive ID: ANIMUS PRIME - Phase 15 Continuation 096G
- Objective: Close the sole remaining R-045 capacity/retention/backpressure and representative-large-repository boundary, then reconcile final V1 gates only if the frozen clause passes.
- Current status: `COMPLETE`
- Acceptance: All frozen V1 requirements directly verified or truthfully conditional by their normative wording; full release validation has no unexplained failures; R-056, DOD-081, Phase 15, and private V1 pass; the persistent private product remains operator-usable with no Funnel/public exposure.
- Current phase: PHASE15_PRODUCTION_READINESS_CLOSURE_096
- Expected or actual touched areas: PostgreSQL durable capacity controls, job admission/claims, index coalescing/stale protection, retention safety, disk-pressure admission, Diagnostics, isolated representative repository qualification, complete V1 ledgers, final evidence, persistent runtime, GitHub parity, and Notion SOT.
- Immediate next action: Preserve the qualified private V1 runtime and await an explicit post-V1 directive. Do not start Phase 16, public deployment, or Continuation 097.

## Temporary task-relevant facts

- Baseline PRIME-SPEC-V1.0.0; authoritative execution is direct SSH/native Atlas at /home/sketch/Projects/ANIMUS_PRIME; Continuation 083 used only the tracked authorized lab `/home/sketch/ANIMUS_PRIME_V1_QUALIFICATION_LAB/083` and fixtures marked `V1_QUALIFICATION_FIXTURE`.
- Starting PRIME state for Continuation 075 was 92e05b5199ea3901d92a1f83902cede0e0bc63e5; no PRIME source change occurred in this continuation.
- Persistent PostgreSQL, Hindsight, PRIME Core/UI, and canonical Node remain preserved. Hindsight remains healthy on 127.0.0.1:8888; the existing Hindsight image and PRIME bank were reused.
- Existing PRIME bank prime-project_d9a1a5b609394282b62fc12c0d04634d contains exactly one legitimate Mental Model, prime-operating-model, with substantive generated content and stored provenance.
- Exact 072 Reflect query remains the accepted source basis from Continuation 073: four native observation/recall calls and substantive provenance-bearing output. Continuation 074 created the model through the supported Hindsight operation.
- Canonical runtime image is `animus-prime-core:continuation-096-6f7ef77` at qualified implementation `6f7ef776c6fadc82771a952e81313ff18eee7295`; persistent PostgreSQL/state/mounts are preserved. Core remains loopback-only on `127.0.0.1:8000` and reports the exact build. No public exposure, deployment, or Phase 16 occurred.
- PRIME owns the private tailnet-only route `https://atlas-2.tail1a5964.ts.net/` to Core loopback. SKETCH gstack Chromium passed protected entry, Atlas-approved trusted-host sign-in, authenticated Windows-project use, and logout protection. No PRIME Funnel exists; all unrelated Serve routes and the pre-existing unrelated port-10000 Funnel remain untouched.
- Genuine Windows service `AnimusPrimeNode` is Automatic/LocalSystem/Running on SKETCH. Node `node-095-sketch-windows` is ACTIVE/ONLINE at LAN `192.168.254.5:18001`, with final enrollment identity and allowed root `C:\PRIME-V1-Qualification\WindowsRepos`.
- Real Windows project `project_d95b88f969bc44caa9cf39818d0ae9b5` binds `C:\PRIME-V1-Qualification\WindowsRepos\V1_QUALIFICATION_FIXTURE_096_WINDOWS_LAN` at Git `2ccf8a2b3addd63b472722936130765e0117193c`; Goal, authority, tree/files, remote indexing/search, LAN transport, and outside-root refusal pass.
- Approved Notion sandbox parent is `3be833cb-27ff-814f-af89-ebfc3a2a8aed`; project record page is `3be833cb-27ff-8159-add6-e883c1cc54af`; controlled probe child is `3be833cb-27ff-81aa-9fe2-ffb4fcf5f980`.
- Runtime Notion capability read/write, production adapter lifecycle, and the complete persistent browser projection/conflict/detach/history operator surface passed. DOD-034/035/036/064/065/066 are USER_USABLE_VERIFIED; detached sources remain RETRACTED and history is idempotent after restart. Continuation 079 Memory surfaces render existing project data with provenance/isolation. Continuation 086 qualified Warm Start selected `.agent` plus selected Notion fixture admission; Hindsight service/retain/recall are current while Reflect is currently unavailable and Mental Models unsupported.
- Continuation 090 established independent guest `prime090-fc`, Node `node-090-firecracker-linux`, approved root `/srv/prime-projects`, project `project_fc46bf826a24410b851ddc860eeb3b49`, repository `repo_760a4120576f4ac7b1c774ffbb0d2497`, and restore `restore_0b0bc75412bf4a85892c84b7b8baab55`. The guest is stopped after rollback; its disk/evidence remain preserved. Untracked `.codebase-memory/`, `.prime-evidence/`, and `.vscode/` remain preserved.
- Continuation 091 qualified live process-death recovery on fixture `project_cd318a4bb4234d99afabc20f2cc3e013`: exit 91 after one live Notion page creation, restart on exact image, exact marker count one, workflow `workflow_79ffaeba9a644fd59492aeac379d5519` SUCCEEDED through PAGE_BOUND.
- Continuation 092 qualified one real expendable project through durable DELETE and PURGE. Live Notion archive, Node repository quarantine, credential revocation, Hindsight bank purge, and local-resource purge each survived injected Core exit 91 and resumed the same workflow without duplicate resources. The real browser also passed Cancel/focus, step-up, exact identity, disclosure, DELETE, PURGE, terminal clearing, refresh, and narrow-viewport checks.
- Continuation 093 created the legitimate child `project_db3ef8c4bc834e68a2e9a9deabbb5a80` at exact source revision `252d71466b92fa3d7979a1b79f02898271b287c1`, with separate repository, Goal/baseline, MCP grant, Notion page, Hindsight bank, Brain, memory, and activity. Replay and restart did not duplicate state. Persistent gstack Playwright tooling lives outside PRIME under `/mnt/storage1tb/prime-tooling/gstack-playwright`.

## Last validation after adoption

- Command or check: Continuation 096G frozen matrix, focused 11-test database-backed suite, representative 6,001-file pressure qualification, complete 167-pass supported regression, persistent runtime/browser qualification, compile, governance, burndown, alignment, and secret/diff review
- Result: `PASSED`

## Risks

- No frozen V1 blocker remains. The governed audit is 81 complete / 0 open; DOD-081 and R-056 are verified; Phase 15 is complete; V1 is qualified for private production use only. Public deployment and Phase 16 remain unauthorized.

## Blockers

- ATLAS_PARAGON_SERVICE_RESTART_REQUIRES_INTERACTIVE_AUTH: RESOLVED by operator restart; new MainPID 607574 and private health verified.
- PRIME_RUNTIME_NOTION_CREDENTIAL_UNAVAILABLE: RESOLVED for the approved bounded credential path; raw token remains Atlas-only and is not governed data.
- PRIME_RUNTIME_NOTION_OPERATOR_WORKFLOW_UNQUALIFIED: RESOLVED by Continuation 076 persistent browser qualification and minimal lifecycle/idempotence repairs.
- AI_MEMORY_ACTIVITY_QUERY_RETURNED_MEMORY_AND_SESSION_IDENTITY_NOT_PERSISTED: RESOLVED by Continuation 080 durable MCP activity projection and restart qualification.
- PRIME_WARM_START_SELECTED_NOTION_SOURCE_UNAVAILABLE: RESOLVED for bounded Continuation 086 — explicit selected Notion fixture admitted through the real browser with source/revision/hash provenance; fixture remains non-authoritative.
- PRIME_QUALIFICATION_VM_RUNTIME_UNAVAILABLE: RESOLVED for Linux qualification by the bounded Firecracker 1.16.1 guest; no QEMU/libvirt stack was installed.
- PRIME_NATIVE_WINDOWS_QUALIFICATION_HOST_UNAVAILABLE: RESOLVED as a host-discovery blocker — a genuine supported Windows host is identified; native qualification remains blocked by the separate elevation/service boundary.
- PRIME_NATIVE_WINDOWS_SERVICE_ELEVATION_UNAVAILABLE: RESOLVED — the genuine Windows service is registered with Automatic start; the service remains stopped pending the operator-approved corrected first-start sequence.
- PRIME_NATIVE_WINDOWS_FIRST_ENROLLMENT_START_PAUSED: RESOLVED — genuine service, secure enrollment, final certificate/bearer, heartbeat, ACTIVE/ONLINE state, listener, and Windows-hosted project passed.
- PRIME_PRIVATE_SERVE_ROUTE_UNAVAILABLE: RESOLVED — PRIME-owned private HTTPS Serve is active and qualified from SKETCH with authentication and no PRIME Funnel/public listener.
- DOD_047_AUTHORITATIVE_COST_HARD_GATE: RESOLVED AS DERIVED DRIFT — frozen monetary cost is conditional where available; truthful UNAVAILABLE plus usage attribution/limits/refusal/recovery pass.
- WINDOWS_INTERACTIVE_ELEVATION_CANCELLED: RESOLVED / SUPERSEDED — subsequent authorized lifecycle and Repair passed; the missed literal Windows-window response remains historical evidence but is not a DOD-053 or DOD-079 frozen blocker.
- FROZEN_CAPACITY_QUALIFICATION_INCOMPLETE: RESOLVED — Continuation 096G qualifies durable per-project concurrency, bounded admission/fairness, coalescing, stale-job refusal, protected retention, simulated disk pressure, representative repository capacity, diagnostics, restart and drain recovery.

## Pending decisions

- Continuation 096G closes R-045, DOD-081 and R-056. Governed §26 queue is 81 complete / 0 open; Phase 15 is complete and V1 is qualified against PRIME-SPEC-V1.0.0 for private production use.
- Preserve the running private Core, Windows Node/project, private Serve route, external qualification fixture, and stopped rollback container. No public exposure, Funnel change, Phase 16, or Continuation 097 is authorized.

- 095A correction: Continuation 090's Linux first-start mechanism is confirmed by preserved artifacts and the repository provisioning precedent: a fresh Node CSR was signed on the trusted Atlas side into a short-lived pre-enrollment server certificate, while the guest received only its own private key, that certificate, the Atlas CA public certificate, and the bootstrap-signing public key.
- 095A correction: The Node then started with mandatory TLS/mTLS, used the Core-issued short-lived bootstrap credential over that channel, submitted CSR proof, and received the long-lived certificate and bearer credential only after operator approval.
- 095A correction: The prepared Windows candidate has a distinct CSR-derived bootstrap certificate with SANs for `node-095-sketch-windows`, `SKETCH`, and `192.168.254.5`; no CA private key or Atlas/Firecracker private identity was copied to Windows.
- 095A correction: This confirms the supported sequence is not circular, but the Windows service remains intentionally stopped in this session pending the operator's explicit corrected-start step. E3/E4 (Windows enrollment, restart, LAN project, and pre-reboot qualification) remain NOT RUN.
- 096 correction: `REBOOT_DERIVED_GATE_REMOVED — NOT IN FROZEN SPEC`. Frozen Node/packaging acceptance requires startup/restart and disconnect/reconnect, not an operating-system reboot.
- 096 correction: `AUTHORITATIVE_COST_HARD_GATE_REMOVED — FROZEN CONTRACT IS WHERE AVAILABLE`. Usage attribution, truthful unavailable monetary cost, and limits remain required; unavailable provider monetary data is not itself a frozen blocker.

## Status vocabulary

ADOPTED is the repository governance lifecycle state. COMPLETE means the current directive is closed for its bounded scope and awaiting reset. PARTIAL records bounded acceptance with explicit remaining gaps.
