# ANIMUS PRIME — Phase 15 Continuation 090 Qualification

## Disposition

`PARTIAL` for Phase 15, `PASS` for the bounded Continuation 090 objective.

Continuation 090 established a genuinely independent Firecracker Linux guest on Atlas, enrolled a fresh native PRIME Node, completed clean Node-backed onboarding and repository creation/recovery, restored a project-bound encrypted backup into the independent B appliance, and qualified the Linux half of DOD-079. DOD-044, DOD-049, and DOD-055 are promoted. DOD-079 remains blocked only by the actual Windows-host half. DOD-081, R-056, Phase 15, V1, deployment, public exposure, and Phase 16 remain open or excluded.

## Governed baseline

- Frozen specification: `PRIME-SPEC-V1.0.0`
- Starting governed/public commit: `2309815bebd56f44cb93c83cc6cfaa9632861a65`
- Starting qualified implementation: `1d1f421e0c6201a49bc2b305c73bd41547237577`
- Starting queue: `69 complete / 12 open`
- Starting supported regression: `125 passed / 29 skipped / 0 failed`
- Canonical checkout: `/home/sketch/Projects/ANIMUS_PRIME`
- Qualification Lab: `/mnt/storage1tb/ANIMUS_PRIME_V1_QUALIFICATION_LAB/090`
- Fixture label: `V1_QUALIFICATION_FIXTURE_FIRECRACKER_090`
- Pre-existing untracked `.codebase-memory/`, `.prime-evidence/`, and `.vscode/` were preserved.

## Firecracker machine boundary

- Firecracker source: official GitHub release `v1.16.1`, x86_64 release archive.
- Archive SHA-256: `382a02a869e4d6d5cb14c40577f9545e8458021ea8b0b2d3fc10ec14d9c242e6`
- Firecracker binary SHA-256: `2fd0171309af7e24cf8dafc8a6f921c1434c49b5f9349bb996b7ed0a4deb8aa7`
- Guest kernel: official Firecracker CI `v1.15` artifact, SHA-256 `e20e46d0c36c55c0d1014eb20576171b3f3d922260d9f792017aeff53af3d4f2`; the `v1.16` public artifact bucket did not contain a guest bundle.
- Upstream Ubuntu 24.04 root filesystem SHA-256: `68321e0482baeb3844dafe8a6b08a6902401a7afc41fbfd8c3d9ea08aadd244f`.
- Qualified ext4 image SHA-256: `6486beb56c4664b9dc53ce3febad56d1e35e15a1f439dfff499933c7b2595ec2`; filesystem UUID `287486fe-a329-46ab-8fff-d19fc187a33c`; logical size 6 GiB.
- Guest identity: hostname `prime090-fc`, machine-id `47503fee235148548392fc7d77f494ac`, MAC `06:00:0a:fa:5a:02`, address `10.250.90.2/30`.
- Resources: 2 vCPU, 1536 MiB RAM; total preserved lab footprint approximately 1.5 GiB.
- Firecracker runtime: official binary inside the bounded `prime090-firecracker` Docker container with only `/dev/kvm` and `/dev/net/tun` passed through. This was necessary because the unprivileged Atlas operator is not a member of the host `kvm` group and no passwordless privilege path exists.
- Jailer was not used because introducing a root/cgroup/chroot ownership path would have expanded host scope beyond this qualification boundary.

The guest had its own kernel, machine-id, ext4 filesystem, service manager, process namespace, Node state, certificate/key material, and repository root. It was not a second container or a renamed host process.

## Network boundary and rollback

- Guest link: dedicated TAP `tap-prime090`, host `10.250.90.1/30`, guest `10.250.90.2/30`.
- Persistent qualification policy: isolated nftables table `inet prime090`; only guest-to-host TCP `18100` was admitted through the PRIME-owned proxy. Forwarding and general guest egress were denied.
- Temporary package egress was enabled only long enough to install missing guest Git, recorded in the lab ledger, then removed before qualification.
- No Tailscale Serve/Funnel, public listener, physical bridge, unrelated firewall rule, or canonical service was changed.
- Rollback: guest halted, `prime090-firecracker` stopped, `prime090-core-proxy.service` disabled/stopped/reset, `tap-prime090` deleted, `inet prime090` absent, and the temporary backup passphrase removed. The qualified ext4 image and non-secret evidence artifacts remain preserved.

See `qualification-continuation-090-machine-network-ledger.md` for the compact resource and rollback ledger.

## Native Linux Node qualification

- Node ID: `node-090-firecracker-linux`
- Name: `PRIME 090 Firecracker Linux Qualification Node`
- Approved root: `/srv/prime-projects`
- Guest service: native `animus-prime-node.service`, enabled and active.
- Enrollment: real registration, bootstrap certificate, proof approval, browser enrollment approval, issued Node certificate, and heartbeat against Appliance A.
- Canonical Node remained `node-041-atlas-native`, with unchanged MainPID `2003030` and start time `2026-08-15 07:10:25 EDT` through closeout.

Clean installation exposed three real packaging/product defects and one guest prerequisite:

1. Installer-created files did not consistently transfer to the dedicated service account.
2. The systemd sandbox did not permit writes beneath the configured approved root.
3. Core repository creation/read/authority/Goal/Warm Start paths assumed the repository path was local to Core instead of dispatching through the enrolled Node.
4. The minimal guest image did not include Git; it was installed through the bounded temporary package-egress window.

The smallest frozen-clause-linked repairs were published in these implementation commits:

- `deebec700f88085535be4b810c19a1bf15a64087` — installer ownership.
- `4edef99a7ca745b4b4b3a33f37ed49c13fdd6b25` — Node-backed create/inspect/authority/Goal APIs.
- `09fbcc155d3a0cbe029d52c0c23d524d428cd5d4` — allowed-root systemd write boundary and errors/tests.
- `b330e0d4c09d489c35c5c38d7ad74c101def1406` — idempotent repository workflow repair.
- `0d49a3fcabc814cad0ee29e193548a89c427d800` — authority template in the Core image.
- `f38ffdc0a82ca3b40bd3bb31e6ac8600c766c645` — Node-backed repository state/tree/file and AGENTS chain.
- `39ec5854191caf56b6a4ddfd1d513d702f62694c` — omit ephemeral capability rows from continuity backup.
- `d882d9e0442be66f689911dec9379f8285b446b8` — Node-backed Warm Start authority reads.

After installation and repair, native Node restart changed MainPID while preserving identity and credentials. A full guest poweroff and relaunch preserved hostname, machine-id, filesystem UUID, Node state hash `fe4883ed01219cec417dab7b3d66ac1d52f4c050e41ab92d2787a27a2b64b620`, repository, authority, and approved Goal. The Node service returned enabled/active with a new MainPID and Appliance A reported it `ONLINE`. An idempotent installer/repair pass retained the same identity and approved root.

## DOD-055 — new repository creation

- Project: `project_fc46bf826a24410b851ddc860eeb3b49`, `PRIME 090 Firecracker Qualification Project`.
- Repository: `repo_760a4120576f4ac7b1c774ffbb0d2497`, `/srv/prime-projects/prime090-firecracker-project`.
- Durable workflow: `workflow_5dcd623d86014a3c976c16f531749e6`.
- Approved Goal: `goal_365d04e80aaa42019e4ffef531b64dd0`, revision 1, hash `f62f20e1023369d8a2934b87e17a24e1af6e6f2aa0401e87cb549499c8ad87b0`.

Browser/API qualification proved invalid parent refusal (`/etc`), invalid repository-name refusal (`../prime090-invalid-name`), explicit confirmation, approved-root enforcement, real non-bare Git creation, independent binding, authority bootstrap, Goal review/approval, duplicate-target refusal, repository tree/file reads through the Node, and durable restart/power-cycle persistence.

The first creation attempts failed truthfully at different real boundaries: Core-local path assumption, read-only service sandbox, and absent guest Git. The same durable workflow entered repair-required state and resumed idempotently after each narrow repair. Final state was `SUCCEEDED`, completed steps `DIRECTORY_CREATED`, `GIT_INITIALIZED`, `BOUND`, retry count 3, no orphan resource, and stable workflow identity. DOD-055 is `USER_USABLE_VERIFIED`.

## DOD-044 — complete first-run setup

The clean Appliance A browser journey completed operator initialization/authentication, PostgreSQL/Core storage state, truthful AI/Notion/Hindsight capability rendering, independent Node enrollment, allowed-root selection, first project, repository creation/binding, authority bootstrap, Goal approval, backup status, system health, Node restart, Core restart, guest power cycle, and resumed browser state.

Unavailable optional integrations were shown truthfully rather than converted to success. The repaired Warm Start preview read the real Node-backed `.agent` files; selecting only `.agent/PROJECT_GOAL.md` produced `Warm Start CURRENT: admitted 1, deduplicated 1, skipped 0, rejected 0`. This used the legitimate approved Goal and existing project bank, not synthetic content. DOD-044 is `USER_USABLE_VERIFIED`.

## DOD-049 — independent backup/restore

- Source backup ID: `backup_6b2017b89305412e9e287c8bf3c91bd1`.
- Artifact: `prime090-v2.continuity`.
- SHA-256: `9cb7be2b0ecab325f2beab531214e51db072ec4605a9334d37025561170cecd3`.
- Format: `prime-continuity/v2`, AES-256-GCM with PBKDF2-HMAC-SHA256.
- Restore ID: `restore_0b0bc75412bf4a85892c84b7b8baab55`.

The first restore exposed a real defect: the backup redacted an ephemeral lifecycle token hash but retained a row whose schema required that value. PostgreSQL rejected it and the transaction rolled back cleanly, leaving B empty. The repair omits authentication/install-local capability state (`operators`, `sessions`, `auth_challenges`, `lifecycle_preflights`, `mcp_grants`, `node_enrollment_challenges`, and `repository_rebind_preflights`) from the continuity payload while preserving canonical project data and the explicit secret-reprovision boundary.

The regenerated encrypted artifact was copied to independent empty Appliance B. The real browser preflight returned ready; protected restore required authenticated step-up; wrong-passphrase preflight refused without mutation. Restore completed as `RESTORED`, with exact PostgreSQL state, source-ledger Hindsight fidelity, retained Evidence/history/Git bundles, and secret-reprovision labeling. B re-opened three project records including the original project, approved Goal, valid authority, repository binding, and intentional Node `OFFLINE` status until its local secret boundary is reprovisioned. A B-Core restart preserved the restored project and Goal with no duplicate data. DOD-049 is `USER_USABLE_VERIFIED`.

## DOD-079 — Linux half

The independent Ubuntu guest qualifies the Linux installer/service half: clean install, dedicated service account, protected state, allowed-root write boundary, real enrollment, repository operations, service restart, guest power cycle, state/identity persistence, idempotent repair, and reconnect. The complete DOD remains `BLOCKED_BY_ENVIRONMENT` because no actual supported Windows host was authorized or available.

Exact remaining operator resource: a supported Windows host for native install, service identity, enrollment, approved-root repository operations, restart/reboot, repair, and reconnect qualification.

## Validation

- Focused implementation tests: `PASSED` throughout the eight bounded implementation commits.
- Full supported regression at final implementation `d882d9e0442be66f689911dec9379f8285b446b8`: `134 passed / 29 skipped / 0 failed` in 6.81 seconds.
- Appliance A/B readiness at exact final build: `PASSED`.
- Firecracker independent-machine identity, native Node lifecycle, restart, and power-cycle: `PASSED`.
- DOD-055 browser/runtime creation and recovery: `PASSED`.
- DOD-044 browser onboarding/restart/Warm Start: `PASSED`.
- DOD-049 browser preflight/protected restore/fidelity/restart/wrong-passphrase refusal: `PASSED`.
- Canonical PRIME Core and canonical Node preservation: `PASSED`.
- Host network rollback and temporary-passphrase removal: `PASSED`.
- Governance, YAML, burndown, diff, and secret checks: recorded at final publication closeout.

The increased pass count is explained by added focused tests for the Node-backed product repairs. The 29 skips remain integration/environment skips and are not represented as passes.

## Governed result

- Qualified implementation: `d882d9e0442be66f689911dec9379f8285b446b8`.
- DOD-044: `USER_USABLE_VERIFIED`.
- DOD-049: `USER_USABLE_VERIFIED`.
- DOD-055: `USER_USABLE_VERIFIED`.
- DOD-079: `BLOCKED_BY_ENVIRONMENT`, Linux half qualified, Windows half outstanding.
- Queue after reconciliation: `72 complete / 9 open`.
- DOD-081/R-056: still gated.
- Phase 15/V1: incomplete.
- Deployment/public exposure/Phase 16: not performed.
