# R-035/R-036 — Continuation 010 local implementation closure

Baseline: `PRIME-SPEC-V1.0.0`  
Directive: `D-PRIME-PHASE15-REMEDIATION-010`  
Scope: bounded private Tailscale Serve lifecycle implementation only.

## Implemented boundary

- Tailscale status is inspected through fixed, allowlisted operations and distinguishes missing, signed-out, connecting, error, degraded, Serve-disabled, and Serve-active states.
- PRIME Serve configuration accepts only a loopback Web target and refuses unsafe Web binds, Funnel/public exposure, and ambiguous existing Serve ownership.
- No generic command runner, shell interpolation, Funnel configuration, router forwarding, or public listener was added.
- PRIME-owned desired state and target are persisted when configured; reconciliation reports an active desired state with unavailable or missing actual Serve as degraded without weakening local access.
- Disable refuses to reset an unidentifiable/unowned Serve configuration. Operator routes remain behind the existing PRIME session requirement.
- A verified private URL is exposed only when an actual DNS name and Serve target are observed.

## Local evidence

- `tests/phase12/test_remote_access.py`: fixed private loopback command, Funnel hard refusal, signed-out state, unsafe bind, ambiguous ownership, and unowned disable behavior.
- Focused result: `5 passed`.
- Full local result: `35 passed, 17 skipped`.

## Qualification boundary

Live signed-in tailnet access, approved second-device HTTPS reachability, daemon restart/recovery, and public-path absence were **NOT RUN**. The required environment is unavailable, so R-035 and R-036 remain qualification `blocked_by_environment`, not VERIFIED. No native/live evidence is claimed.
