# Continuation 090 — Host Network Mutation and Rollback Ledger

Before mutation, no `tap-prime090`, `inet prime090`, or `prime090-core-proxy.service` boundary existed.

During qualification:

- TAP `tap-prime090` connected host `10.250.90.1/30` to guest `10.250.90.2/30`;
- nftables table `inet prime090` admitted only guest-to-host TCP 18100 and denied general forwarding;
- user service `prime090-core-proxy.service` mapped the guest-facing qualification address to Appliance A only;
- a separate temporary package-egress rule existed only long enough to install Git, then was removed before product qualification;
- no physical bridge, public listener, Tailscale Serve/Funnel, canonical Core listener, or unrelated firewall rule changed.

Rollback result:

- Firecracker guest/container stopped;
- proxy service disabled, stopped, and reset to inactive;
- `tap-prime090` absent;
- `inet prime090` absent;
- temporary backup passphrase absent;
- canonical Node remained active with MainPID `2003030` and original start time;
- canonical Core remained healthy at build `1d1f421e0c6201a49bc2b305c73bd41547237577`.
