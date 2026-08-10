# R-031 local encrypted control-plane qualification

Status: `IMPLEMENTING` / release verification `OPEN`

This record is implementation evidence only. It does not qualify native Linux
service lifecycle, Windows service lifecycle, reboot persistence, or the V1
release gate.

## Environment

- Host: disposable local Linux process on 2026-08-10
- Python/uvicorn: repository-pinned `uvicorn==0.46.0`
- Node entrypoint: `python3 -m apps.node.main`
- Bind: `127.0.0.1:18443`
- TLS: ephemeral CA, server certificate, and client certificate generated for
  this run; no private key or credential is retained in this evidence
- Control protocol: `node-control-v1`

## Execution

| Check | Result | Observed output |
|---|---|---|
| Node starts with certificate, key, and CA configuration | PASS | Process reached HTTPS health endpoint |
| mTLS client certificate required | PASS | Request without client certificate failed during TLS handshake |
| One-time enrollment over mTLS | PASS | Returned a node identity and short-lived response credential |
| Authenticated heartbeat over mTLS | PASS | `status=ONLINE`, protocol `node-control-v1` |
| Packaging entrypoint | PASS | `python -m apps.node.main` starts the configured service |
| Disposable Compose Node image/health check | PASS | Pinned Node image started with the corrected `0.0.0.0:8001` qualification mapping and reported live health |
| Missing TLS configuration fails closed in service mode | PASS | `NodeSettings.uvicorn_kwargs()` raises before startup |

Observed heartbeat response (credential and certificate material omitted):

```json
{"status":"ONLINE","node_id":"<ephemeral>","protocol_version":"node-control-v1"}
```

## Remaining R-031 evidence

- Native Linux install, systemd restart, reboot, and reconnect: `OPEN`
- Native Windows service install, restart, reboot, and reconnect: `OPEN`
- Rotation, revocation, re-enrollment, offline recovery, and version upgrade
  on supported service installations: `OPEN`
- Qualified Git commit: `NONE` (working-tree increment; release qualification
  requires a later immutable candidate commit)
