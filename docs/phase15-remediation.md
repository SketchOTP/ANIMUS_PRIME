# Phase 15 release remediation

This is a remediation cycle against the unchanged `PRIME-SPEC-V1.0.0`. It does
not create a Phase 16 or weaken the V1 Definition of Done.

## Reconciliation

The historical Phase 15 result remains `FAIL` at governed commit
`275bfc69252ebe6506ca6c6d3c35c32da37ad1e2`. Broad rows affected by release-gap
discovery were reopened in `docs/requirements-traceability.yaml`, and the
individual obligations are tracked in `docs/phase15-remediation-matrix.yaml`.

## Remediation foundation implemented

- R1: Node identity persistence, protocol/version and capability reporting,
  heartbeat/status, credential rotation, revocation and explicit re-enrollment;
  Linux systemd and Windows service-installation shape are versioned under
  `packaging/node/`.
- R2: fixed-argv Tailscale Serve controller with local detection, status,
  disable/reset, private loopback target and hard refusal when Funnel exposure
  is detected.
- R3: server-side Notion API adapter using the current pinned API version,
  bounded page/block operations and retry handling for rate limits/transient
  provider failures. Live provider qualification is still open.
- R4: encrypted continuity bundle/preflight foundation with manifest,
  component high-water marks and plaintext-credential rejection; migration
  records schedule/checkpoint and Evidence storage fields. Live restore and
  sustained-capacity qualification are still open.
- R5: bounded Evidence validation/storage primitives and a Git checkpoint schema
  foundation. Full historical reconstruction and production parser evidence are
  still open.

## Validation

- `python3 -m pytest tests -q` — PASSED locally: 20 passed, 15 skipped because
  the host Python environment lacks `psycopg`/a qualification PostgreSQL.
- `python3 scripts/validate_governance.py --mode ADOPTED` — PASSED.
- New remediation-focused tests — PASSED: 10 tests covering Node lifecycle,
  Tailscale refusal, Notion retry/auth behavior, encrypted backup preflight and
  Evidence safety validation.
- Full V1 release gate — NOT RUN to completion; matrix rows remain open.

No deployment occurred and no V1 release claim is authorized.
