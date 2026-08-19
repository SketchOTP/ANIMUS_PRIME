# Phase 15 Qualification — Continuation 094

Date: 2026-08-18
Frozen specification: `PRIME-SPEC-V1.0.0`
Starting governed HEAD: `2d7be12c5e032cfe0b47c4236e3ef9a02ee21b81`
Qualified implementation: `65e553f084f5c5fba970ad7bf25c581ab15066ff`
Disposition: **BLOCKED at the external machine/service boundary**

## Objective and result

Continuation 094 was authorized to use one genuine Windows machine to qualify DOD-079 (native Windows Node), DOD-053 (second enrolled LAN machine/project), and DOD-013 (private second-device Tailscale Serve). A genuine Windows candidate was identified, but the bounded qualification could not proceed from this session because the required Windows Service Control Manager elevation was unavailable. The current Atlas Tailscale Serve map also contains no PRIME UI route to exercise for DOD-013.

No DOD/R row was promoted. The governed queue remains **76 complete / 5 open**. DOD-013, DOD-053, and DOD-079 remain external prerequisites; DOD-047 remains the separate provider-cost prerequisite; DOD-081/R-056 remains gated.

## Baseline and preservation

- Atlas checkout: `/home/sketch/Projects/ANIMUS_PRIME`
- Atlas local `main`, `origin/main`, and starting GitHub `main`: `2d7be12c5e032cfe0b47c4236e3ef9a02ee21b81`
- Starting worktree: only preserved untracked `.codebase-memory/`, `.prime-evidence/`, and `.vscode/`
- Qualified runtime: `animus-prime-core:continuation-093-65e553f`, implementation `65e553f084f5c5fba970ad7bf25c581ab15066ff`
- Existing PRIME Core, PostgreSQL, Hindsight, canonical Node, Funnel, and unrelated services: preserved
- PRIME source/product code: unchanged
- Public exposure, Funnel configuration, deployment, Phase 16: not performed

## Genuine Windows candidate

Read-only host facts from the current operator Windows machine:

| Fact | Result |
|---|---|
| Hostname | `SKETCH` |
| OS | Microsoft Windows 11 Pro, version `10.0.26200`, build `26200`, 64-bit |
| Hardware | ASUS, `System Product Name`, x64-based PC |
| Memory | approximately 31.89 GiB |
| C: capacity | approximately 953.07 GiB total / 163.91 GiB free |
| Active LAN | Ethernet 4, `192.168.254.5/24`, gateway `192.168.254.254` |
| Atlas LAN | Atlas `192.168.254.49/24`; same active LAN boundary |
| Tailscale | `1.102.2`, device `sketch`, `100.80.17.40` |
| Existing PRIME services | none found on the Windows host |
| Existing qualification root | `C:\PRIME-V1-Qualification` was absent before this run |

The host is physically distinct from Atlas and is not a container or compatibility layer. The exact operator approval and an interactive elevated session remain required before service installation and reboot qualification.

## Unchanged-first installer result

The exact governed source was obtained from GitHub at `65e553f084f5c5fba970ad7bf25c581ab15066ff` into the expendable external root `C:\PRIME-V1-Qualification\source`. A Python 3.12.10 virtual environment was created under `C:\PRIME-V1-Qualification\Node\.venv` and the pinned `requirements-phase1.txt` dependencies installed.

The unchanged `packaging/node/install-node.ps1` was then run with `-InstallRoot C:\PRIME-V1-Qualification\Node`. It created the install/data directories but failed at genuine service registration:

```text
[SC] OpenSCManager FAILED 5:

Access is denied.
```

The current PowerShell process has Administrators group membership only as a deny-only token (`ADMIN_TOKEN_AVAILABLE=False`). The normal UAC `RunAs` launch was blocked by the Codex execution policy before an elevated process started. No service was created, started, or modified. This is an environment/elevation stop, not evidence of a successful Windows installation.

## Atlas remote-access baseline

Read-only Atlas checks showed:

- PRIME Core listener: `127.0.0.1:8000`
- canonical Atlas Node listener: `127.0.0.1:18001`
- Hindsight listener: `127.0.0.1:8888`
- existing Tailscale Funnel: `https://atlas-2.tail1a5964.ts.net:10000` -> `127.0.0.1:4117`
- existing tailnet-only Serve routes: ports `47821`, `8082`, `8443`, `8789`, `8791`, `9420`, `9443`, and `9545`
- no current Tailscale Serve route maps to PRIME `127.0.0.1:8000`

The existing Funnel and Serve routes were not changed. The Funnel route is not claimed as PRIME, and it was not used as a substitute for private PRIME Serve qualification. DOD-013 therefore cannot be promoted from the current topology.

## Acceptance matrix

| Gate | Result | Reason |
|---|---|---|
| E0 baseline/host identity/LAN | PASSED | Genuine Windows host and same-LAN relationship observed read-only |
| E1 unchanged installer | BLOCKED | Windows Service Control Manager requires an elevated token unavailable to this session |
| E2 product/governance validation | NOT APPLICABLE | No PRIME product-code change or governed implementation change |
| E3 native Windows Node/reboot/project | BLOCKED | Cannot register the required Windows service; no reboot or Node enrollment attempted |
| E4 second-device PRIME Serve/browser | BLOCKED | No PRIME-owned private Serve route exists; existing Funnel/other routes preserved |
| E5 independent DOD review | BLOCKED | Complete frozen clauses cannot be satisfied from the stopped boundary |

## Exact operator prerequisites

1. Run the unchanged Windows installer from an interactive elevated PowerShell/UAC session, or provide an approved equivalent elevation boundary for the same host. Do not bypass Windows security controls.
2. Provide or authorize the existing PRIME-owned private remote-access workflow to map the genuine PRIME UI privately inside the approved tailnet. Do not enable Funnel or reuse the unrelated `:10000` route.
3. Confirm the candidate Windows host is approved for the required service lifecycle, expendable repository, and actual OS reboot.

After those prerequisites are available, resume the same bounded 094 packages. Do not manufacture DOD-013, DOD-053, or DOD-079 evidence from the current partial setup.

## Closeout state

- DOD-013: remains open/external; no private PRIME Serve qualification
- DOD-047: unchanged, provider-backed authoritative cost remains open
- DOD-053: remains open/external; no Windows Node enrollment or second-machine project qualification
- DOD-079: remains `BLOCKED_BY_ENVIRONMENT`; Linux qualification is preserved, Windows native service/reboot remains unqualified
- DOD-081/R-056: remains gated
- Phase 15/V1: incomplete
- Deployment/public exposure: NOT PERFORMED
- Continuation 095: not started
