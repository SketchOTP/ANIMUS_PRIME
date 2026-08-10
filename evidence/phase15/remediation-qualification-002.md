# Phase 15 remediation qualification — increment 002

Recorded: `2026-08-10T21:35:00Z`  
Candidate commit: `b03d993`  
Baseline: `PRIME-SPEC-V1.0.0`

```text
mechanical_gate = PASS
v1_release_gate = FAIL
qualified_release_commit = NONE
deployment = NOT PERFORMED
```

On a fresh disposable PostgreSQL state, `scripts/phase15_qualify.py` passed:

- governance and baseline identity;
- full regression suite: 36 tests;
- Phase 1–14 qualification sequence;
- Core/Node contract and remediation tests;
- release-matrix presence check.

The same run failed every release-matrix row R-031 through R-056 because those
requirements remain `IMPLEMENTING`/`OPEN`. This is a truthful release failure,
not a mechanical failure. The current commit is not a V1 release commit.

The disposable PostgreSQL/Core/Node qualification stack was removed after the
run. No deployment occurred.
