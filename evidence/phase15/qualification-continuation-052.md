# ANIMUS PRIME — Continuation 052 Evidence

## Bounded outcome

Status: **PARTIAL — convergence reset plus core-independent source/offline continuity advance**.

The strategic assessment "strategically aligned, tactically drifting" is adopted as a priority correction to Continuation 051. DOD-039 rebind, DOD-050 upgrade preflight, and DOD-053 second-LAN-machine implementation remain parked. DOD-004 remains limited to the durable primitives already built and lifecycle paths that are necessary for the actual V1 product.

The next product milestone is a genuine persistent PRIME Core plus the real web UI on Atlas. This run did not start Core, uvicorn, a browser qualification session, or any disposable resource. Persistent runtime start remains an explicit-authorization gate.

## Native Atlas baseline

- Authoritative checkout: `/home/sketch/Projects/ANIMUS_PRIME` over direct SSH.
- Local Atlas `HEAD`, `origin/main`, and GitHub `main`: `dc425cc7582a46f86fe7b35b0889343785bf5c25`.
- Existing untracked `.codebase-memory/`, `.prime-evidence/`, and `.vscode/` were preserved.
- Persistent PostgreSQL container `animus-prime-phase0-postgres-1` remains running.
- Persistent Hindsight container `mimir-hindsight-production` remains running.
- No ANIMUS PRIME Core listener was present on ports 8000 or 18000. Existing listeners on 5173 and 8080 were not treated as PRIME runtime evidence.
- No PRIME project, repository, worktree, Hindsight bank, browser profile, or synthetic A/B environment was created.

## DOD-005 — source lifecycle

The narrow local-code gap was repaired. Evidence retraction now:

1. marks the linked source reference stale;
2. tombstones source-linked current memory records and records a correction plus historical snapshot;
3. marks evidence-backed current Progress assessments stale;
4. excludes stale evidence-backed Progress from current Progress snapshots and Search;
5. excludes memories whose linked source reference is no longer current; and
6. excludes detached/retracted Notion knowledge bindings from current Search.

Historical evidence and memory identity remain retained through the existing historical-revision path. The existing evidence retraction test now asserts that current Progress disappears after retraction while Evidence Search remains empty. DOD-005 remains `BACKEND_ONLY` because the exact full current-derived-view qualification, including generated Documentation/Notion projection behavior, still requires a bounded direct integration qualification; no promotion is claimed here.

## DOD-074 — offline repository Node

Against the existing persistent qualification project `project_d9a1a5b609394282b62fc12c0d04634d` and enrolled Node `node-041-atlas-native`, the Node status was temporarily set from `ENROLLED` to `OFFLINE`, then restored to the exact original status in a `finally` path.

Observed while offline:

- persisted project listing remained available (`722` existing project rows; no project was created);
- persisted Progress snapshot remained readable for the qualification project;
- historical context remained readable for the governed revision `dc425cc7582a46f86fe7b35b0889343785bf5c25`; and
- the Node-required repository inspection refused with the exact fail-closed result `Node is OFFLINE`.

Restoration check: Node status returned to `ENROLLED`. This is direct backend/persistence evidence only. DOD-074 remains `BACKEND_ONLY` because the frozen operator path “Open offline node from PRIME” still requires a persistent Core and real UI qualification.

## Validation

- `PASSED` — direct Atlas Git parity and preserved-worktree check.
- `PASSED` — `git diff --check`.
- `PASSED` — Python compileall for touched source and qualification test module.
- `PASSED` — code-only focused tests: `10 passed`.
- `SKIPPED` — 3 DB integration tests that create qualification projects; not run under the no-disposable constraint.
- `PASSED` — read-only PostgreSQL `EXPLAIN` parsing for the new current Progress, Memory, and Notion filters against the persistent schema.
- `PASSED` — reversible offline-Node persisted-state check and exact status restoration.
- `NOT RUN` — PRIME Core/browser qualification; no persistent Core listener is currently authorized or configured for this run.
- `NOT RUN` — DOD-050, DOD-053, DOD-039, R-045, and R-056 work; all remain parked by the convergence reset.

## Remaining authorization and product gap

The product cannot be judged through the original Home → Attention → Project → Progress → Ask/Search → Memory/Knowledge → Activity journey until a genuine persistent PRIME runtime is explicitly authorized and made available on Atlas. The next run should begin by confirming that authorization and the intended service topology, then qualify the actual operator journey and fix failures in user-impact order.
