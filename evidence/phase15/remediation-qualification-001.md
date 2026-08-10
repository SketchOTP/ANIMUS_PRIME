# Phase 15 remediation qualification — increment 001

Recorded: `2026-08-10T21:15:00Z`  
Baseline: `PRIME-SPEC-V1.0.0`  
Historical failed release commit: `275bfc69252ebe6506ca6c6d3c35c32da37ad1e2`

## Result

```text
mechanical_gate = PASS
v1_release_gate = FAIL
qualified_release_commit = NONE
deployment = NOT PERFORMED
```

This record preserves the earlier Phase-15 failure and records the first
remediation increment. It is not a V1 release qualification.

## Mechanical evidence

- `PRIME_PHASE1_DB_URL=... /tmp/animus-prime-venv/bin/python -m pytest tests -q` — PASSED, 35 tests.
- `PRIME_PHASE1_DB_URL=... /tmp/animus-prime-venv/bin/python scripts/phase15_qualify.py` — mechanical checks PASSED; release matrix checks FAILED.
- Phase 1–14 migration/qualification scripts — PASSED on clean disposable PostgreSQL state.
- `python3 scripts/validate_governance.py --mode ADOPTED` — PASSED.
- `docker compose -f docker-compose.phase1.yml build core node` — PASSED.
- Core and Node container health — PASSED (`/health/live`, both healthy).
- New remediation tests — PASSED: Node lifecycle, Tailscale refusal, Notion retry/auth, encrypted backup/preflight and Evidence safety.

## Remediation state

R1–R6 implementation foundations are present in the governed history. The
release-remediation matrix still has R-031 through R-056 as `IMPLEMENTING`/
`OPEN` because the required real evidence is not yet available or complete:

- real supported Linux and Windows Node installation/control-plane lifecycle;
- live Tailscale Serve/Funnel and approved-device verification;
- live Notion provider/project-record/Knowledge Source lifecycle;
- scheduled encrypted backup, clean-install restore, retention and capacity drills;
- complete Evidence and historical Git/Time Lens reconstruction;
- complete operator walkthrough behavior beyond the static shell;
- approved AI regression fixtures and full integrated end-to-end evidence.

## Release decision

`ANIMUS PRIME V1 QUALIFICATION: FAIL` — no release or deployment claim is
authorized. Continue the Phase-15 remediation cycle against the unchanged
baseline.
