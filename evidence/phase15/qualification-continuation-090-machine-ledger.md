# Continuation 090 — Machine Ledger

The independent qualification machine was Firecracker `v1.16.1` with 2 vCPU, 1536 MiB RAM, and a sparse 6 GiB ext4 root filesystem stored only beneath `/mnt/storage1tb/ANIMUS_PRIME_V1_QUALIFICATION_LAB/090`.

Identity and persistence evidence:

- hostname `prime090-fc`;
- machine-id `47503fee235148548392fc7d77f494ac`;
- root filesystem UUID `287486fe-a329-46ab-8fff-d19fc187a33c`;
- MAC `06:00:0a:fa:5a:02`;
- guest IP `10.250.90.2/30`;
- native Node `node-090-firecracker-linux`;
- approved root `/srv/prime-projects`;
- Node state hash `fe4883ed01219cec417dab7b3d66ac1d52f4c050e41ab92d2787a27a2b64b620` unchanged across power cycle;
- repository and approved Goal remained present across relaunch.

The guest disk and non-secret evidence remain preserved. The guest is stopped after qualification. See `qualification-continuation-090-machine-network-ledger.md` for artifact hashes and host-boundary comparison.
