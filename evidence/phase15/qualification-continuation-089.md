# ANIMUS PRIME — Phase 15 Continuation 089

## Acceptance

`BLOCKED` for the qualification-machine work package. The VM approach was not disproven by the frozen specification, but Atlas cannot provide an already-installed, approved VM runtime or a safe LAN-equivalent guest network boundary without introducing new host infrastructure. No VM, second Node, or product qualification was manufactured.

## E0 — authority and baseline

- Frozen specification: `PRIME-SPEC-V1.0.0`; unchanged. No SpecChangeRecord.
- Starting governed HEAD: `5d0e8dd2d1d4a8cf9adb433f95ebb27fb6695e5c`.
- Starting qualified implementation: `1d1f421e0c6201a49bc2b305c73bd41547237577`.
- Local/origin parity at intake: exact parity.
- Preserved untracked artifacts: `.codebase-memory/`, `.prime-evidence/`, `.vscode/`.
- Canonical Node: `node-041-atlas-native`, user service `animus-prime-node`, active before and after inspection. No canonical trust, certificate, state, database, project, repository, or network configuration was changed.

## Work Package A — machine-boundary investigation

The frozen text requires an independently enrolled Node and allows projects from an enrolled LAN machine. It does not expressly require physical hardware, so a VM remains a valid interpretation only if it supplies an independent guest OS, machine identity, filesystem, network identity, Node identity, trust material, and enrollment lifecycle.

Atlas facts gathered read-only:

- Hardware virtualization is available: `/dev/kvm` exists with `root:kvm` ownership and mode `0660`; `sketch` is a member of `kvm`.
- No approved guest runtime is installed: `qemu-system-x86_64`, `qemu-img`, `virsh`, `virt-install`, `virt-manager`, `lxc`, `incus`, `multipass`, and `systemd-nspawn` were not present; no libvirt/LXD service or existing guest was found.
- Apt simulation shows the requested QEMU/libvirt stack would add 92 new packages, including `qemu-system-x86`, libvirt daemons, storage/network drivers, firmware, and related host services. No installation was performed.
- Root capacity is constrained at approximately 17 GiB free / 93% used. Available memory was approximately 7.2 GiB from 30 GiB total. No resource reservation or host infrastructure change was made.
- Atlas has Wi-Fi `wlp0s20f3` on `192.168.254.49/24`; the wired interface is down and no pre-existing physical LAN bridge is present. Existing Docker bridges are unrelated application networks. No bridge, route, firewall, or Tailscale configuration was changed.
- Tailscale has existing devices and unrelated Funnel state, but no newly approved PRIME qualification-device enrollment path was established. Funnel remained untouched.

Primary documentation reviewed:

- [libvirt network XML](https://libvirt.org/formatnetwork.html): NAT, routed, isolated, host-bridge, and direct/macvtap boundaries were compared. A host bridge/direct attachment is not present; NAT would not establish the requested LAN-equivalent second-machine evidence.
- [systemd machine-id upstream source](https://github.com/systemd/systemd/blob/main/man/machine-id.xml): a guest needs its own persistent machine ID; cloned identity is not acceptable. The supplied freedesktop page was inaccessible to the browser due to site protection, so the upstream systemd source was used.
- [Tailscale VM/tailnet documentation](https://tailscale.com/kb/1136/tailscale-vm): a VM authenticated as a device is a distinct tailnet device only after an approved device authentication/enrollment path; no such PRIME path was exercised here.

## Work Package B result

`BLOCKED — ATLAS_APPROVED_VM_RUNTIME_UNAVAILABLE`

The VM interpretation remains theoretically valid, but this Atlas host currently has only hardware virtualization capability, not an installed approved VM runtime or existing safe guest network. Installing a large new QEMU/libvirt stack and configuring host networking would be a new host-infrastructure change, not an already-approved equivalent discovered by this continuation. It was not performed.

The existing Node packaging was inspected and exists in the repository: `packaging/node/install-node.sh`, `packaging/node/install-node.ps1`, `packaging/node/prime-node.service`, `packaging/node/animus-prime-node.service`, and `packaging/node/enroll-atlas.sh`. No packaging defect was observed because no clean guest installation was available to execute it.

## DOD results

No DOD was promoted. The twelve-row queue remains 69 complete / 12 open:

- DOD-004: OPEN, durable multi-system interruption/reconciliation remains gated.
- DOD-013: OPEN, approved second tailnet device/enrollment path unavailable.
- DOD-016: OPEN, complete child-resource path remains unqualified.
- DOD-044: PARTIAL, clean-install Node-backed onboarding remains unexercised.
- DOD-047: PARTIAL, authoritative provider cost attribution remains unavailable.
- DOD-049: PARTIAL, bound-project independent restore remains unexercised.
- DOD-053: OPEN, no legitimate second enrolled LAN machine was established.
- DOD-055: PARTIAL, Node-backed repository creation/interruption/recovery remains unexercised.
- DOD-077: PARTIAL, browser terminal PURGE surface remains absent.
- DOD-079: BLOCKED_BY_ENVIRONMENT, repository Linux/Windows packaging exists, but native Linux lifecycle qualification and Windows qualification remain open.
- DOD-080: OPEN, complete polish qualification remains open.
- DOD-081/R-056: OPEN/GATED, aggregate release qualification remains last.

## Derived-governance correction

The prior DOD-079 audit statement that the repository exposes no deterministic native installer/unit was stale. This continuation records the correction append-only: Linux and Windows installer/service files are present, while live Linux install/restart/reboot/repair qualification and the actual Windows host qualification remain unverified. Historical checkpoints are unchanged.

## Validation

- Read-only Atlas virtualization, resource, network, service, packaging, and Tailscale inventory: `PASSED`.
- Frozen-spec and primary-document review: `PASSED` with the freedesktop-page access limitation noted above.
- Product-code change: `NOT APPLICABLE`; no product code changed.
- VM creation, guest identity, Node enrollment, browser onboarding, repository creation, backup/restore, DOD-053, and DOD-079 live qualification: `BLOCKED` by the missing approved VM/runtime/network boundary.
- Regression: `NOT RUN`; no product code or runtime changed.
- Deployment/public exposure/Phase 16: `NOT PERFORMED`.

## Exact operator prerequisite

Provide one of:

1. an operator-approved installed VM runtime and bounded storage/network allocation on Atlas, with a safe guest network path; or
2. a legitimately approved independent Linux machine/VM already available for PRIME Node enrollment.

The next run must re-check the resource boundary before creating a guest. Do not install the simulated QEMU/libvirt package set, configure a bridge, enroll a new Node, or begin Continuation 090 without that explicit environment decision.
