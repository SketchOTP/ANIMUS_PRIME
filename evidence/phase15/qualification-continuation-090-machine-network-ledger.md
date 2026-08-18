# Continuation 090 — Machine and Network Ledger

| Item | Before | During qualification | After rollback |
|---|---|---|---|
| Firecracker | absent | `v1.16.1`, container `prime090-firecracker`, 2 vCPU, 1536 MiB | container preserved but exited |
| Guest identity | absent | `prime090-fc`, machine-id `47503fee235148548392fc7d77f494ac`, ext4 UUID `287486fe-a329-46ab-8fff-d19fc187a33c` | disk/artifacts preserved |
| Guest Node | absent | `node-090-firecracker-linux`, enabled/active, `/srv/prime-projects` | offline because guest is stopped; state preserved in ext4 |
| TAP | absent | `tap-prime090`, host `10.250.90.1/30`, guest `10.250.90.2/30` | absent |
| nftables | no PRIME 090 table | `inet prime090`, guest only to host TCP 18100, no general forward | table absent |
| Core proxy | absent | `prime090-core-proxy.service`, host guest-facing 18100 to isolated A | disabled, inactive, reset from failed state |
| Package egress | absent | temporary bounded guest package egress for Git only | absent before product qualification |
| Tailscale/public ingress | unchanged | untouched | unchanged |
| Canonical Node | active, MainPID 2003030, start 2026-08-15 07:10:25 EDT | untouched | same MainPID/start, active |
| Canonical Core | healthy build `1d1f421e...` | untouched | healthy same build |
| Temporary backup passphrase | absent | mode-restricted runtime file | removed |

## Hash and resource ledger

- Firecracker archive: `382a02a869e4d6d5cb14c40577f9545e8458021ea8b0b2d3fc10ec14d9c242e6`.
- Firecracker binary: `2fd0171309af7e24cf8dafc8a6f921c1434c49b5f9349bb996b7ed0a4deb8aa7`.
- Kernel: `e20e46d0c36c55c0d1014eb20576171b3f3d922260d9f792017aeff53af3d4f2`.
- Qualified ext4: `6486beb56c4664b9dc53ce3febad56d1e35e15a1f439dfff499933c7b2595ec2`.
- Preserved lab footprint: approximately 1.5 GiB.
- Root filesystem logical allocation: 6 GiB sparse ext4; actual file usage is bounded within the lab footprint.

No host package installation, host bridge, public exposure, Funnel rule, or unrelated service mutation remains.
