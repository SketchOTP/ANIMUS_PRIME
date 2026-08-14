# ANIMUS PRIME — Phase 15 Continuation 055

## Result

`PARTIAL` — the persistent private Core-to-Node product path is operational and the operator-visible offline Node boundary is qualified. DOD-005 generated Documentation/Notion projection, the remaining unavailable integrations, R-056, Phase 15 completion, V1 declaration, and deployment remain open.

- Qualified implementation commit: `0a3c82f53d0c5c70a37db7f8c3a2dbdb6d76d42f`
- Final governed publication commit: recorded after closeout publication

## Baseline

- Specification: `PRIME-SPEC-V1.0.0`
- Authoritative checkout: `/home/sketch/Projects/ANIMUS_PRIME` on Atlas
- Starting governed commit: `b479f9f72a507403cbcc756e13328f51b166424f`
- Starting status: clean tracked tree with pre-existing untracked `.codebase-memory/`, `.prime-evidence/`, and `.vscode/` preserved
- Existing PostgreSQL: container `animus-prime-phase0-postgres-1`, existing persistent database reused
- Existing Hindsight: container `mimir-hindsight-production`, existing loopback service reused
- Existing Node record: `node-041-atlas-native`; no second Node, project, database, bank, repository, worktree, or browser profile created
- Existing PRIME Core: user-systemd service `animus-prime-core.service`, container `animus-prime-core`, loopback `127.0.0.1:18000`
- Existing PRIME UI: Core-served genuine Web UI, loopback `127.0.0.1:28000` through the existing private local path
- Unrelated Atlas listeners and Funnel/Tailscale configuration were not changed

## Prior-art review and decision

The review used official project repositories through the mandated browse workflow:

| Candidate | License / maintenance observed | Fit | Decision |
|---|---|---|---|
| [Smallstep step-ca](https://github.com/smallstep/certificates) | Apache-2.0; actively maintained private-CA project | Strong model for short-lived certificates, provisioners, renewal, and revocation | Adapt lifecycle principles; do not add a second persistent CA daemon because Atlas has no installed step-ca runtime and this Node is co-located |
| [CNCF SPIRE](https://github.com/spiffe/spire) | Apache-2.0; graduated CNCF workload-identity project | Strong workload identity/SVID model but materially broader than one private co-located Node | Adapt SPIFFE URI identity; reject full SPIRE deployment as overbuilt for this bounded V1 topology |
| [Cloudflare CFSSL](https://github.com/cloudflare/cfssl) | BSD-2-Clause; maintained PKI/TLS toolkit | Useful primitive, but leaves the Core-owned lifecycle custom | Reject as the primary lifecycle architecture |
| Installed `cryptography` and OpenSSL | Existing repository/runtime primitives | Available on Atlas and sufficient for signed bootstrap tokens, CSR verification, CA signing, and X.509 metadata | Adopt as the implementation primitives; no custom cryptography and no new daemon |

## Trust and enrollment lifecycle

- Stable identity remains `node-041-atlas-native`; no self-generated replacement identity is accepted.
- Core issues a signed bootstrap proof with a 300-second lifetime, challenge ID, canonical Node ID, nonce, and one-use digest tracking.
- The Node submits its CSR proof over the private mTLS control endpoint. Replay, expiry, wrong identity, and invalid signature paths fail closed.
- The authenticated PRIME operator sees pending enrollment metadata in the real Web UI and must explicitly approve or reject it.
- Core signs the Node CSR with the private Atlas CA, including CA-valid X.509 metadata, SPIFFE URI `spiffe://animus-prime/node/node-041-atlas-native`, DNS identity, loopback IP SAN, and server/client EKU.
- Node private key, CA private key, Core private key, bootstrap signing private key, and bearer credential remain in mode-0600 runtime references outside Git, evidence, browser storage, and Notion.
- Credential rotation replaces the bearer atomically without returning its value to the UI.
- Revocation clears the credential reference, marks the Node revoked, and requires a new bootstrap proof and operator approval before re-enrollment.
- Certificate-chain validation was repaired with CA key usage, subject key identifier, and authority key identifier extensions; the direct Core-to-Node heartbeat passed with CA verification and client authentication.

## Persistent Atlas topology

| Component | Runtime mechanism | Identity / listener | Dependency targets | Persistence / startup | Result |
|---|---|---|---|---|---|
| PRIME Core | user systemd → Docker container | `animus-prime-core`; `127.0.0.1:18000` | existing PostgreSQL, existing Hindsight, trust directory, enrolled Node | `animus-prime-core.service`, enabled; persistent bind `/home/sketch/.local/share/animus-prime-core` | READY |
| PRIME Web UI | genuine UI served by Core | local/private Core UI path | persistent Core session/API | returned with Core service | READY |
| PostgreSQL | existing persistent Docker service | `animus-prime-phase0-postgres-1` | Core schema and project state | existing service preserved | HEALTHY / REUSED |
| Hindsight | existing persistent service | `mimir-hindsight-production`, loopback `127.0.0.1:8888` | optional memory capabilities | existing service preserved | DEGRADED only for unavailable capabilities |
| Repository Node | user systemd → repository venv/Uvicorn | `animus-prime-node.service`; `https://127.0.0.1:18001`; mTLS required | Atlas CA, canonical repository root, Core client certificate | enabled; persistent state under `/home/sketch/.local/share/animus-prime-node` | ACTIVE / ONLINE after recovery |

- Public exposure: none; no Funnel or public ingress performed.
- Startup persistence: Core and Node user services are enabled.
- Restart recovery: Core stop/start returned `/health/ready`; Node stop/start returned active mTLS health, same canonical identity, same project binding, and same credential reference.
- No duplicate PRIME Core or Node instance was left running.

## Browser operator evidence

Browser: Chromium through the gstack browse workflow, authenticated against `http://127.0.0.1:28000/`.

- Protected entry and authenticated session: PASSED.
- Home / Needs Attention / Projects: PASSED; the existing `Qualification Project` was selected from the real project registry.
- Overview: PASSED; `Qualification Project · ACTIVE · ONLINE · freshness CURRENT`.
- Progress: PASSED; persistent progress and current freshness remained available.
- Repository healthy path: PASSED; Node-backed tree reported `/home/sketch/Projects/ANIMUS_PRIME`, canonical revision `b479f9f72a507403cbcc756e13328f51b166424f`, branch `main`, and `AVAILABLE`.
- Authority: PASSED; `.agent` validation reported `VALID`.
- Memory: PASSED; persisted records and source metadata remained visible.
- Knowledge: truthful `DISCONNECTED` / no Notion page; it did not block the local product.
- Evidence: truthful empty current projection for this existing project; no fabricated artifact was presented.
- Activity: persisted events remained visible.
- Brain, Time Lens, AI Connections, and Settings: surfaces loaded and retained their existing bounded/degraded contracts.

## DOD-074 operator-visible qualification

Using only the existing canonical Node and a restoration path:

1. Healthy baseline: Node `ACTIVE` / `ONLINE`; Core heartbeat succeeded over verified mTLS; repository tree was `AVAILABLE`.
2. Legitimate offline condition: `systemctl --user stop animus-prime-node.service`; no database status was manually edited.
3. While offline: browser reload preserved the selected project and Overview state (`ACTIVE · ONLINE · freshness CURRENT`); persisted project/history/Progress state remained usable.
4. Node-required operation: repository load returned `NODE_UNAVAILABLE` with unknown revision/branch/dirty state rather than falling back to local filesystem access.
5. Recovery: `systemctl --user start animus-prime-node.service`; Core heartbeat returned `ONLINE`; the same Node identity and project binding returned; repository load returned `AVAILABLE` again.

Result: DOD-074 operator boundary `PRODUCT_VERIFIED` for the exercised persistent Atlas path. This does not close R-056 or claim whole-product V1 completion.

## DOD-005 and related state

- DOD-005 source-removal propagation remains preserved through Progress, Memory, and Search from prior governed work.
- The actual operator UI now runs against persistent Core/Node state, but generated Documentation/Notion projection could not be exercised because the approved Notion capability is `DISCONNECTED` / unavailable. No Notion environment was manufactured.
- DOD-006 / R-031 gained the persistent private Node and mTLS topology evidence, but governed row promotion is deferred to final mechanical reconciliation rather than inferred from runtime health alone.
- R-056 remains `OPEN` and gated on its complete frozen integrated acceptance contract.

## Negative security and regression outcomes

- Bootstrap replay, expiry, wrong Node ID, wrong signature, and pending-before-approval authentication paths are covered by focused tests and lifecycle behavior.
- Node control endpoints require mTLS; bearer credentials are not accepted as a substitute for transport identity.
- Rotation, revocation, and re-enrollment preserved the canonical Node ID and did not create a second Node.
- Recovery-secret regression guard passed: the Web UI does not render one-time recovery values or persist recovery/password values in localStorage/sessionStorage. No raw secret was written to Git, evidence, `.agent`, Notion, browser diagnostics, or logs.

## Validation

- Focused Node/client/trust/recovery tests: `7 passed` — PASSED.
- Direct Core-to-Node mTLS heartbeat: PASSED.
- CA/leaf certificate-chain and identity inspection: PASSED.
- Browser healthy/offline/restart recovery: PASSED.
- Rotation, revocation, re-enrollment, and operator approval: PASSED.
- Python compileall: PASSED.
- Full regression: `93 passed, 28 skipped` — PASSED; the skip count remained the established integration boundary.
- Governance: PASSED (`validate_governance.py --mode ADOPTED`).
- Burndown: PASSED (`audit_total=81`, `complete=44`, `burndown=37`, mechanically reconciled).
- Product alignment audit: PASSED; release gate remains FAIL by design while open §26 rows remain.
- Secret scan and `git diff --check`: PASSED; no private keys, bearer values, passwords, or raw credentials detected.
- Persistent service/listener health and enabled startup policy: PASSED.
- Local/origin parity and final publication: pending the governed commit/push closeout recorded below.
- Deployment: NOT PERFORMED.

## Remaining gaps

- DOD-005 generated Documentation/Notion projection remains unavailable/unqualified.
- Approved AI provider, LOCAL_ONLY runtime, Hindsight Reflect/Mental Models, native Windows, second device, and private Tailscale second-device boundaries remain unavailable or unqualified.
- R-056 remains OPEN; Phase 15 completion and V1 declaration are not claimed.

No secrets, private keys, bearer values, passwords, or browser session values are included in this record.
