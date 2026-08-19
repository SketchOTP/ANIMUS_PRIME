# ANIMUS PRIME — Phase 15 Qualification Continuation 096

## Baseline

- Directive: `D-PRIME-PHASE15-PRODUCTION-READINESS-CLOSURE-096`
- Frozen specification: `PRIME-SPEC-V1.0.0`
- Starting governed/local HEAD: `1d1947c19af18f0d28daf323650cb99577c509b1`
- Starting `origin/main`: `1d1947c19af18f0d28daf323650cb99577c509b1`
- Starting qualified implementation/runtime: `c9690cac248173b7b3bcaaeb76994f583d0fddc5` / `animus-prime-core:continuation-095-c9690cac`
- Starting governed queue: `76 complete / 5 open`
- Preserved untracked operator state: `.codebase-memory/`, `.prime-evidence/`, `.vscode/`

## Frozen-baseline corrections adopted prospectively

- `REBOOT_DERIVED_GATE_REMOVED — NOT IN FROZEN SPEC`: frozen Node and packaging criteria require startup/restart plus disconnect/reconnect, not Windows OS reboot.
- `AUTHORITATIVE_COST_HARD_GATE_REMOVED — FROZEN CONTRACT IS WHERE AVAILABLE`: frozen usage/cost attribution is conditional where provider monetary data is available; truthful unsupported/unavailable cost and usage-limit behavior remain required.

Historical 094/095/095A evidence remains append-only and is not rewritten.

## Qualified implementation lineage

- `0b290ceb3de7f6018430db1e8d867230ce4f9a59` — genuine Windows SCM wrapper, installer/environment/ACL handling, and CSR-derived enrollment certificate support.
- `a3ad57a2a4b4ae3f521e134bb54c455ed175f357` — Windows path semantics for the live `AGENTS.md` chain.
- `818c7ea1d8344b6f42c6eda610c975b2c85533bd` — Windows repository tree and file browsing semantics.
- `13eb75b82071eb8b79a93565d3f0c8489c1dc28f` — remote indexing through the enrolled Windows Node.
- `1b780b706bc140afef886ad0ecd33a2991e9d283` — Git retrieval from the Node snapshot rather than an invalid Atlas-local Windows path.
- Final qualified implementation: `6f7ef776c6fadc82771a952e81313ff18eee7295` — installed Tailscale 1.102.2 scoped-disable syntax.
- Qualification evidence/governance commit: `0128fcc086dcbdf9cb37b17a410099ec544ae2a6`.
- Persistent image: `animus-prime-core:continuation-096-6f7ef77`; runtime build provenance reports the same implementation.

## Genuine Windows Node

- Host: `SKETCH`, Windows 11 x64, LAN `192.168.254.5`.
- Service: `AnimusPrimeNode`, genuine Windows SCM, `Automatic`, `LocalSystem`, currently `Running`.
- Node: `node-095-sketch-windows`, distinct from Atlas and Firecracker identities, `ACTIVE / ONLINE`.
- Listener: `192.168.254.5:18001` only; no wildcard or public listener.
- Approved root: `C:\PRIME-V1-Qualification\WindowsRepos`; outside-root traversal `../..` was refused with `REPOSITORY_PATH_REJECTED`.
- Enrollment used the normal one-time bootstrap, CSR proof, operator approval, final certificate, and protected bearer lifecycle. The final certificate contains only the Node identity, loopback, and Windows LAN SANs. No CA private key or copied Node identity entered Windows.
- Windows private-key/data ACLs are restricted to SYSTEM and Administrators. No secret value is included in this record.
- The first attempted SCM command accidentally parsed `Windows` as a service name; that empty accidental registration was immediately removed before the real service was configured. It never became a PRIME Node.

### Remaining lifecycle boundary

The service stop required an interactive Administrator/UAC approval. The operator cancelled that elevation prompt. The stop operation returned cancelled and the service remained `Running`; there was no service or identity mutation. In accordance with the no-bypass boundary, Continuation 096 did not retry, schedule, or otherwise circumvent elevation.

Therefore the frozen Windows `stop -> offline recognition -> start -> reconnect -> restart -> reconnect` and installer Repair/idempotent rerun remain unqualified. No OS reboot is required. This is the one exact remaining operator action boundary.

## Windows-hosted LAN project

- Project: `V1_QUALIFICATION_FIXTURE_096_WINDOWS_LAN`
- Project ID: `project_d95b88f969bc44caa9cf39818d0ae9b5`
- Physical repository: `C:\PRIME-V1-Qualification\WindowsRepos\V1_QUALIFICATION_FIXTURE_096_WINDOWS_LAN` on SKETCH.
- Current Git revision: `2ccf8a2b3addd63b472722936130765e0117193c`; clean `main` branch.
- Network path: Atlas Core `192.168.254.49` reached SKETCH Node `192.168.254.5:18001` over the real LAN. The Node listener is the Windows LAN address and is not a Tailscale address or same-host substitute.
- Normal PRIME workflow passed repository inspection/binding, authority review, Goal approval, tree/file reads, remote indexing, current-revision search, and allowed-root refusal.
- Goal revision 1 is approved with content hash `eb6811090058e3bb11ad367757bda16716e2a16e811b58e72ffd6d1de31c9b8b7`.
- Authority is `VALID`; the live `AGENTS.md` chain is exposed with Windows path semantics.
- Remote index is `CURRENT` at the same Git revision with 12 files. Search for `private LAN` returned only current project-scoped Authority hits.
- The actual browser showed the Windows repository path/revision, approved Goal, and valid authority state through the persistent Core.
- Project isolation and normal LAN operation pass. The explicit service-offline/reconnect subclause remains blocked by the same cancelled elevation action, so DOD-053 is not promoted prematurely.

## PRIME-owned private Tailscale Serve

- Installed Tailscale: `1.102.2`, daemon `Running`.
- PRIME-owned route: `https://atlas-2.tail1a5964.ts.net/` on HTTPS 443 to `http://127.0.0.1:8000`.
- Core remains loopback-only; no raw LAN or public Core listener was added.
- Adapter/UI status: `SERVE_ACTIVE`, `private_only=true`; Funnel for the PRIME route is refused.
- The persistent Core origin allowlist was extended only with the exact PRIME private HTTPS origin. Persistent database/state/mounts/image were preserved across restart.
- All unrelated Serve routes remained present. The pre-existing unrelated Funnel allowance at `atlas-2.tail1a5964.ts.net:10000` remained mapped to `127.0.0.1:4117`; Continuation 096 neither disabled nor modified it.
- A real gstack Chromium browser running on SKETCH reached the private URL, first saw protected unauthenticated state, and did not receive stale project data.
- Trusted-host sign-in required a short-lived browser challenge and Atlas-local approval. After approval the SKETCH browser loaded the authenticated dashboard, the real Windows project, Goal, Repository, and Authority surfaces.
- Logout removed the protected project payload; the same private URL returned authentication-required state.
- Local Core remained healthy on loopback. Tailscale was not globally stopped because doing so would disrupt unrelated Atlas routes; unavailable/degraded behavior remains covered by the existing ownership/refusal qualification.

DOD-013 is `USER_USABLE_VERIFIED`. R-035 and R-036 are `VERIFIED` for the frozen private Serve/Funnel boundary.

## DOD-047 frozen cost reconciliation

Frozen §14 and §16A.20 require usage and estimated cost by function/project/provider/model **where available**. Continuation 082 already qualified persistent project-scoped usage, provider/model/function attribution, a visible truthful `UNAVAILABLE` monetary-cost state, configurable limits, over-limit refusal, and recovery after disabling the limit. No monetary amount was fabricated and no provider credential was added.

DOD-047 is `USER_USABLE_VERIFIED`. R-045 remains independently open for its parser-concurrency, index-backlog/stale-job, and retention-pressure clauses; unavailable provider monetary data is no longer listed as a hard blocker.

## Browser and runtime qualification

- Browser: gstack Chromium/Bun on genuine SKETCH, state isolated outside PRIME product/runtime data.
- URL: `https://atlas-2.tail1a5964.ts.net/`.
- Protected entry: PASS.
- Trusted-host authentication: PASS after exact-origin runtime configuration repair.
- Unified dashboard: PASS; projects from multiple machines are visible through one Core.
- Windows project Goal/Repository/Authority: PASS.
- Logout/session protection: PASS.
- Private Serve/no PRIME Funnel/no public Core listener: PASS.
- Persistent Core health/restart/build provenance: PASS.
- Windows service lifecycle and installer Repair: BLOCKED by cancelled interactive elevation; no bypass attempted.

## Validation

- Focused Windows service/certificate/path suites: PASS (`7 passed`, then `8 passed`).
- Remote indexing focused suite: PASS (`9 passed / 1 skipped`).
- Shared retrieval focused suite: PASS (`7 passed / 1 skipped`).
- Remote access and Windows path affected suite: PASS (`17 passed`).
- Full supported regression: PASS (`167 passed / 35 skipped / 0 failed`). The 35 skips are the repository's explicit integration/environment skips; no failed or unexplained test was hidden.
- Compile/static import check: PASS (`python -m compileall -q src apps packaging`).
- Governance validation: PASS (`ADOPTED`, 17 required files, 6 Cursor rules).
- Burndown structural validation: PASS (`78 complete + 3 open = 81`, exact IDs/statuses/work classes).
- YAML parse: PASS for all five governed YAML views.
- Product alignment: remains FAIL until DOD-053/DOD-079 and aggregate DOD-081 close.
- Secret review: no raw bootstrap, bearer, private key, database credential, Notion token, or provider credential is included in the diff/evidence.

## Frozen disposition

- DOD-013: `USER_USABLE_VERIFIED`.
- DOD-047: `USER_USABLE_VERIFIED`.
- DOD-053: remains `BACKEND_ONLY`; genuine second-machine project operation passed, but the directive's explicit offline/reconnect proof remains blocked by cancelled Windows elevation.
- DOD-079: remains `BLOCKED_BY_ENVIRONMENT`; native Windows install/enrollment/operation pass, while frozen service stop/start/restart/reconnect and Repair/idempotence remain blocked by the same elevation boundary.
- DOD-081 / R-056: remain open because DOD-053 and DOD-079 are not fully qualified.
- Governed queue after reconciliation: `78 complete / 3 open`.
- Phase 15: `INCOMPLETE`.
- V1: `NOT YET QUALIFIED`.
- Phase 16: not created.
- Deployment/public exposure: not performed.

## One exact blocker

`BLOCKED — WINDOWS_INTERACTIVE_ELEVATION_CANCELLED`

Frozen clause requiring it: Phase 2/Phase 14 native Node and installer/service qualification requires Windows service startup/restart plus Node disconnect/reconnect and installer/service repair behavior. The supported SCM operations require an Administrator/UAC-approved Windows session. The cancelled prompt prevented those checks while leaving the service safely running.

Minimal operator action: approve one bounded Administrator/UAC block that performs only `AnimusPrimeNode` stop/status/start/restart and the unchanged installer `-Repair` rerun, while Codex observes offline/reconnect, identity persistence, and LAN-project recovery. No reboot, public exposure, third machine, or spec change is required.
