# Continuation 093 — Remaining External Gates

After DOD-016 and DOD-080 promotion, the mechanically reconciled V1 queue is 76 complete / 5 open:

| Row | Exact remaining prerequisite |
|---|---|
| DOD-013 | Approved second device for private Tailscale Serve qualification and public/Funnel refusal proof |
| DOD-047 | Approved provider/profile with authoritative cost attribution |
| DOD-053 | Legitimate second enrolled LAN machine and real project target |
| DOD-079 | Actual supported Windows host for native installation, service, reboot, repair, enrollment, allowed-root, and reconnect qualification |
| DOD-081 / R-056 | Final integrated release qualification after the four prerequisite rows close |

Mechanical work classes:

- local code: 0
- local browser qualification: 0
- local native qualification: 0
- evidence reconciliation: 0
- external environment: 4
- aggregate release gate: 1

These are resource and release gates, not authorization for synthetic machines, projects, providers, cost data, public exposure, specification weakening, or Phase 16. `DOD-081` and `R-056` remain open. Phase 15 and V1 remain incomplete.

## Continuation 094 reconciliation

Continuation 094 inspected one genuine Windows 11 x64 host on Atlas's active LAN and the existing Atlas Tailscale state. The unchanged Windows installer stopped at Service Control Manager elevation (`OpenSCManager FAILED 5: Access is denied`) from the non-elevated Codex shell, and the existing Tailscale Serve map contained no PRIME UI route. Therefore DOD-013, DOD-053, and DOD-079 remain open with their original external prerequisites; no row is promoted. Full detail is in `evidence/phase15/qualification-continuation-094.md`.

## Continuation 095 reconciliation

Continuation 095 repaired the PRIME-owned Tailscale Serve boundary and rebuilt/restarted the persistent Core from implementation `c9690cac248173b7b3bcaaeb76994f583d0fddc5`. The live Atlas route map still has no PRIME `127.0.0.1:8000` route, while unrelated Serve routes and the existing Funnel route remain unchanged. The adapter repair is therefore qualified as a local safety prerequisite only; DOD-013 remains open until the actual product path creates a private PRIME route and a real second device completes authenticated browser/outage/recovery qualification.

The genuine Windows host and preserved qualification root remain available, but native service installation still requires an interactive elevated PowerShell token. DOD-053 and DOD-079 remain open. DOD-047 and the aggregate DOD-081/R-056 gate are unchanged. Queue remains **76 complete / 5 open**. Full detail is in `evidence/phase15/qualification-continuation-095.md`.
