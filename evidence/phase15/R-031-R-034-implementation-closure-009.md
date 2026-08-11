# R-031–R-034 local implementation closure — Continuation 009

Baseline: `PRIME-SPEC-V1.0.0`
Directive: `D-PRIME-PHASE15-REMEDIATION-009`
Implementation commit: `084ea85d19d3c56df6c14601e532e9bc346862b6`

## Implemented locally

- Node state persists outside the repository with restrictive replacement-file permissions; identity survives service-object reload.
- Bootstrap enrollment, credential rotation, revocation, explicit re-enrollment, protocol rejection, TLS/mTLS fail-closed startup, private-bind validation, bounded client responses, and authenticated identity binding are implemented.
- Heartbeat persists last-seen state and reports node version, protocol versions, capabilities, approval state, and ONLINE/STALE/OFFLINE health.
- Allowed roots are normalized and persisted; resolved path checks reject traversal and symlink escapes. Repository snapshots are read-only Git observations.
- Linux systemd and Windows `sc.exe` install/repair/uninstall paths are versioned; state and credentials are kept outside the repository and uninstall preserves state pending explicit operator disposition.
- Diagnostics exclude credential material and expose bounded operational state.

## Validation

- `python3 -m pytest tests/phase2/test_node.py tests/phase2/test_node_client.py tests/phase2/test_node_continuation009.py -q` — PASSED (`6 passed`).
- `python3 -m pytest tests -q` — PASSED (`32 passed`, `17 skipped`).
- `python3 -m compileall -q src apps scripts` — PASSED.
- `git diff --check` — PASSED.
- codebase-memory MCP indexing — BLOCKED (`Transport closed`); targeted local inspection used.

## Qualification boundary

R-031–R-034 remain `qualification_status=blocked_by_environment`, not `VERIFIED`. Native Linux service install/start/restart/reboot, actual Windows service/reboot, qualified private deployment, watcher/offline reconciliation, and Core/Node upgrade compatibility evidence were not executed in this environment. No native or live evidence was fabricated.

Regression protection for R-042–R-050 remains intact through the full local suite. Deployment was NOT PERFORMED. V1 remains FAIL.
