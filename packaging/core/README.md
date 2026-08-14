# PRIME persistent Core/Web UI service

The V1 Web UI is served by the PRIME Core process from `apps/web/index.html`;
there is no separate UI server in the supported architecture. On Atlas, the
Core is a PRIME-owned Docker container attached to the host network and bound
to `127.0.0.1:18000`. The existing PostgreSQL and Hindsight services remain
external persistent dependencies and are not recreated by this service.

The service unit is intended for the enrolled Atlas user-level systemd
instance. The persistent container is created once by the Atlas operator with
an environment file outside the repository and then managed by
`packaging/core/prime-core.service`.

Required private configuration is kept outside Git, for example:

- `/home/sketch/.config/animus-prime/core.env` (mode `600`)
- `/home/sketch/.local/share/animus-prime-core/` (persistent runtime state)

The container must use the approved existing PostgreSQL and Hindsight targets,
must not publish a host port, and must not enable Tailscale Funnel or other
public ingress. The unit owns only the PRIME Core container named
`animus-prime-core`.

`local-recovery.sh` is the supported Atlas break-glass path when the original
one-time recovery credential is unavailable. It stores the local recovery
secret and replacement recovery credential outside the repository with mode
`0600`; the API accepts the path only from loopback, rotates both recovery
credentials, revokes sessions, and records an audit event. It does not create
another operator identity.
