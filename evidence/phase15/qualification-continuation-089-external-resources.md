# Continuation 089 — External Resource Ledger

| Requirement | Required legitimate resource | Current evidence | Disposition |
|---|---|---|---|
| DOD-013 | Approved second tailnet device and PRIME enrollment path | Existing tailnet peers are visible, but no new PRIME device enrollment was approved or exercised; unrelated Funnel remained untouched. | OPEN — operator resource required |
| DOD-044 | Fresh independent Linux installation/VM with an independently enrolled PRIME Node | Atlas has `/dev/kvm` but no installed approved guest runtime, existing guest, or safe guest network boundary. | BLOCKED — approved VM/runtime or independent Linux target required |
| DOD-047 | Authoritative provider/model cost attribution | No change. | PARTIAL/BLOCKED |
| DOD-049 | Independent restore destination containing a legitimate Node-backed project backup | No bound-project source could be produced without the missing independent Node/project boundary. | OPEN — Node-backed source and independent destination required |
| DOD-053 | Legitimate second enrolled LAN machine/project | No independent LAN-equivalent guest or second machine was established. | OPEN — approved independent LAN machine/VM required |
| DOD-055 | Legitimate Node-backed repository creation/recovery target | No clean Node-backed target was available. | PARTIAL — approved independent Linux target required |
| DOD-079 | Live native Linux lifecycle target plus actual supported Windows host | Repository Linux/Windows installer and service files exist. Live Linux install/restart/reboot/repair and Windows qualification remain unverified. | BLOCKED_BY_ENVIRONMENT |
| DOD-081/R-056 | Complete integrated V1 environment | Node/machine, Windows, Tailscale, provider-cost, restore, and remaining product gates are incomplete. | GATED — last |

Atlas resource facts for the VM branch: KVM device available, no QEMU/libvirt/LXD/equivalent runtime installed, approximately 17 GiB root free at 93% used, approximately 7.2 GiB available RAM, Wi-Fi-only active physical interface, and no pre-existing physical LAN bridge. Installing the simulated 92-package QEMU/libvirt set was not performed.
