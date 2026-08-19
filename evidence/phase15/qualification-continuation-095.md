# Phase 15 Qualification — Continuation 095

Date: 2026-08-19
Frozen specification: `PRIME-SPEC-V1.0.0`
Starting governed HEAD: `505a8d01dc6af243e50e7d8748c8719ebbf47544`
Qualified implementation before this continuation: `65e553f084f5c5fba970ad7bf25c581ab15066ff`
Bounded implementation commit: `c9690cac248173b7b3bcaaeb76994f583d0fddc5`
Disposition: **PARTIAL / BLOCKED at the Windows elevation and real private-route qualification boundaries**

## Objective and result

Continuation 095 resumed the genuine Windows/LAN/Tailscale boundary from 094 and repaired the PRIME-owned Tailscale Serve adapter without claiming the external qualifications. The real Windows host and expendable qualification root remain available, but the unchanged Node installer still requires an interactive elevated PowerShell token. Atlas has unrelated Serve/Funnel routes and no PRIME route; the adapter repair was qualified against the actual installed Tailscale 1.102.2 JSON shape and the persistent Core was rebuilt/restarted privately.

No DOD/R row was promoted. The governed queue remains **76 complete / 5 open**. DOD-013, DOD-053, and DOD-079 remain open; DOD-047 remains separate; DOD-081/R-056 remains gated.

## Baseline and preservation

- Atlas checkout: `/home/sketch/Projects/ANIMUS_PRIME`
- Starting local/origin/public baseline: `505a8d01dc6af243e50e7d8748c8719ebbf47544`
- Starting worktree: only preserved untracked `.codebase-memory/`, `.prime-evidence/`, and `.vscode/`
- Existing PostgreSQL, Hindsight, canonical Node, PRIME state, unrelated containers, Tailscale Serve/Funnel routes, and public boundary: preserved
- No frozen specification, canonical project, canonical Node, database, Hindsight bank, unrelated route, firewall, Funnel, deployment, or Phase 16 change

## Genuine Windows candidate and unchanged-first boundary

The same genuine Windows 11 x64 host identified in 094 remains the candidate: hostname `SKETCH`, Ethernet `192.168.254.5/24`, Atlas `192.168.254.49/24`, Tailscale `1.102.2`, Tailscale identity `100.80.17.40`. The exact qualified source remains at `C:\PRIME-V1-Qualification\source` with HEAD `65e553f084f5c5fba970ad7bf25c581ab15066ff`; the Node virtual environment remains at `C:\PRIME-V1-Qualification\Node\.venv`.

The unchanged installer was not rerun from this non-elevated session. The previous first hard failure remains authoritative:

```text
[SC] OpenSCManager FAILED 5: Access is denied.
```

The current session did not bypass UAC, alter Windows security, create a service, or reboot the host. DOD-079 and the Windows half of DOD-053 remain blocked until the operator runs the unchanged installer from an interactive elevated PowerShell and returns non-secret output.

## Atlas persistent runtime

Before replacement, the PRIME-owned user service was active with the 093 image and private health. The new image was built from the bounded implementation commit with full provenance:

| Field | Result |
|---|---|
| Image | `animus-prime-core:continuation-095-c9690cac` |
| Image ID | `sha256:e65cb732d60f720edc7b5b1224ded44f6009d5677f808fb5ac5842bfd83a9a69` |
| Build commit | `c9690cac248173b7b3bcaaeb76994f583d0fddc5` |
| Build timestamp | `2026-08-19T01:45:00Z` |
| Runtime mechanism | existing user `systemd --user` unit `animus-prime-core.service` controlling the PRIME-owned Docker container |
| Listener | existing host-private Core/UI listener `127.0.0.1:8000` |
| State | existing `/home/sketch/.local/share/animus-prime-core` preserved |
| Startup/restart | service restart succeeded; one canonical container remained active |
| Health | `/health/live` and `/health/ready` PASSED; readiness returned the exact 095 build commit/image identity and schema `0040_destructive_lifecycle_sagas.sql` |
| Public exposure | NOT PERFORMED |

The prior 093 container was retained under the rollback name `animus-prime-core-093-rollback`; the intermediate provenance-corrected replacement was swapped into the existing canonical service name. No duplicate active Core remained.

## Tailscale ownership repair

Read-only inspection of the installed Atlas client showed Tailscale `1.102.2`. The actual Serve JSON contains unrelated routes on ports `10000`, `47821`, `8082`, `8443`, `8789`, `8791`, `9420`, `9443`, and `9545`; only `10000` is Funnel-allowed. No route targets PRIME `127.0.0.1:8000`.

The bounded repair in `src/prime_core/remote_access_service.py`:

- identifies PRIME's default HTTPS endpoint by the actual tailnet DNS name and endpoint port;
- extracts route targets from the installed nested `Handlers`/`Proxy` JSON shape;
- reports PRIME-owned Serve/Funnel state separately from unrelated Serve/Funnel routes;
- allows unrelated Serve/Funnel routes to coexist without treating them as PRIME exposure;
- refuses PRIME Funnel exposure, loopback violations, conflicting endpoint targets, and unknown ownership;
- persists the owned target/endpoint and disables only the PRIME endpoint with `tailscale serve clear 443`;
- removes the previous global `tailscale serve reset --yes` operation and keeps the command surface fixed and bounded.

The real Atlas status after restart reports PRIME Serve `DISABLED`, PRIME Funnel `NOT_DETECTED`, unrelated Serve routes present, and the unrelated Funnel route preserved. PRIME Serve was not configured because the complete operator/browser route qualification was not reachable through the current product path and no qualification evidence was manufactured.

## Validation

| Check | Result |
|---|---|
| Focused remote-access tests | **PASSED** — `13 passed` on Atlas |
| Functional supported regression subset | **PASSED** — `152 passed / 35 skipped` in the existing persistent Core image environment, excluding only the dependency-blocked YAML burndown test |
| Full supported regression | **BLOCKED** during collection — Atlas host Python lacks `psycopg`; the existing Core image lacks `PyYAML` for `tests/phase15/test_product_gap_burndown.py`; no package was installed and no substitute environment was created |
| Compile/static syntax | **PASSED** — `python3 -m compileall -q src apps scripts` |
| `git diff --check` | **PASSED** |
| Governance validator | **PASSED** — `python3 scripts/validate_governance.py --mode ADOPTED` |
| Governance validator self-test | **FAILED** — existing clean-template assertion failed in `scripts/test_validate_governance.py`; no project source failure was inferred |
| Browser DOD-013 qualification | **NOT RUN / BLOCKED** — no PRIME-owned private route exists; unrelated routes were preserved |
| Windows service/LAN qualification | **BLOCKED** — interactive elevation prerequisite unavailable |

The full regression and governance self-test limitations are recorded truthfully; they do not promote any requirement.

## Changed files

- `src/prime_core/remote_access_service.py`
- `tests/phase12/test_remote_access.py`
- `.agent/DIRECTIVES.md`
- `.agent/CURRENT.md`
- `.agent/OUTCOMES.md`
- `.agent/LEARNINGS.md`
- `.agent/RECORD.md`
- `docs/v1-product-gap-burndown.yaml` (external-gate evidence reconciliation only)
- `docs/v1-product-goal-alignment-audit.yaml` (DOD-013 evidence/blocker reconciliation only)
- `docs/requirements-traceability.yaml` (R-035/R-036 evidence reconciliation only)
- `docs/phase15-remediation-matrix.yaml` (R-035 evidence reconciliation only)
- `evidence/phase15/qualification-continuation-095.md`
- `evidence/phase15/qualification-continuation-093-external-gates.md` (append-only 095 reconciliation)

## Exact operator prerequisite

Open a new interactive PowerShell **as Administrator** on `SKETCH`, verify elevation, then run the unchanged installer from the preserved qualification root. Return only non-secret output:

```powershell
$ErrorActionPreference = 'Stop'
$identity = [Security.Principal.WindowsIdentity]::GetCurrent()
$principal = [Security.Principal.WindowsPrincipal]::new($identity)
if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) { throw 'NOT_ELEVATED' }
Set-Location 'C:\PRIME-V1-Qualification\source'
& '.\packaging\node\install-node.ps1' -InstallRoot 'C:\PRIME-V1-Qualification\Node'
Get-Service -Name 'AnimusPrimeNode' | Select-Object Name,Status,StartType
```

Do not bypass UAC, expose PRIME publicly, reset Tailscale Serve, or reboot until separately approved. After elevation succeeds, resume the same 095 Windows/LAN packages; do not start Continuation 096.

## Closeout state

- DOD-013: remains `BACKEND_ONLY` / external; ownership repair is qualified, private second-device operator route is not
- DOD-047: unchanged and open
- DOD-053: remains external; no second enrolled LAN project qualification
- DOD-079: remains `BLOCKED_BY_ENVIRONMENT`; Windows service/reboot remains unqualified
- DOD-081/R-056: remains gated
- Phase 15/V1: incomplete
- Deployment/public exposure: NOT PERFORMED

## Append-only 095A — native first-enrollment bootstrap investigation

### Disposition

`PARTIAL / PAUSED` before Windows service start. The supported bootstrap sequence is reconstructed and the apparent TLS enrollment cycle is refuted for the Linux precedent. No Windows service, enrollment, LAN project, reboot, private Serve route, DOD promotion, or publication was performed in this bounded investigation.

### E0 — Continuation 090 reconstruction

Preserved Continuation 090 artifacts show a fresh guest CSR at `090/guest/bootstrap-node.csr`, a short-lived certificate at `090/guest/bootstrap-node.crt`, and the later guest copy `090/guest/appliance-a-node-bootstrap.crt`. The certificate was issued by `CN=ANIMUS PRIME Atlas Local CA`, had the fresh Node identity as subject/SAN, and existed before the Node's first mandatory TLS/mTLS service start. The guest retained only public CA/bootstrap-verification material and its own identity material; no CA private key was placed in the guest.

The repository precedent is `packaging/node/provision-atlas-trust.sh`: trust is provisioned on the trusted host, the Node receives the CA public certificate and bootstrap-signing public key, and a short-lived Node certificate is present before service startup. This is classified as **C — direct out-of-band certificate provisioning through the approved product trust-provisioning path**, not insecure HTTP and not the later operator-approval certificate.

### E1 — current code-path/trust-boundary map

1. Core `issue_node_bootstrap()` creates the canonical Node challenge and one-time signed bootstrap credential.
2. A pre-enrollment Node server certificate is required because `NodeSettings.uvicorn_kwargs()` refuses service mode without complete TLS files; the listener requires client certificates.
3. Core's `NodeClient` uses the Core client certificate/key and the Atlas CA to call `/v1/enroll` over mTLS. The Node verifies the signed bootstrap credential and fresh Node identity/CSR, persists proof state, and consumes the bootstrap digest.
4. Core `sync_node_proof()` records the CSR and moves the canonical record to pending operator approval.
5. Core `approve_node_enrollment()` signs the final certificate, calls Node `/v1/enrollment/approve` over the still-running mTLS channel, and stores the bearer credential by secure reference.
6. The Node atomically installs the final certificate, stores only its digest/state, and requires restart before normal active heartbeat. The first heartbeat then transitions the Node to ACTIVE/ONLINE.

The initial bootstrap certificate and final approval certificate are therefore distinct trust artifacts. The one-time bootstrap credential is not a substitute for the server certificate.

### E2 — circularity result

`SUPPORTED_SEQUENCE_CONFIRMED` for the established Linux/native sequence: no circular deadlock exists when the approved pre-enrollment certificate is provisioned from the fresh CSR on the trusted Atlas side. The Windows candidate was prepared with a distinct Windows-local key/CSR and a CSR-derived short-lived certificate whose SANs are `node-095-sketch-windows`, `SKETCH`, and `192.168.254.5`; the CA private key was not copied to Windows.

### E3/E4/E5 status

- Real Windows first enrollment and heartbeat: **NOT RUN** — the user explicitly stopped the Administrator start step pending this investigation.
- Windows service stop/start/restart, allowed-root checks, LAN-hosted project, and private Serve/second-device path: **NOT RUN**.
- Windows reboot persistence: **NOT RUN** and remains a separate approval boundary.
- Product code changes: **NONE**.
- DOD/R promotions: **NONE**.

### Next bounded action

Resume the same Continuation 095 only after the operator authorizes the corrected elevated start using the already-prepared bootstrap certificate and machine-scoped environment. Start no service in this investigation; do not reboot, change Tailscale routes, expose PRIME publicly, promote DOD-013/DOD-053/DOD-079, or begin Continuation 096.
