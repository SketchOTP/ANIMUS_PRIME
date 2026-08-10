# ANIMUS PRIME Repository Map

This map covers the Phase 0 governance/source-lock surface. Feature modules are added only in their owning phases.

## Recommended sections after adoption

- `baseline/` — frozen specification, handoff, and implementation-baseline identity.
- `authority-template/v1/` — approved materialized authority package and manifest.
- `contracts/` — shared domain, authority, isolation, storage, and privacy contracts.
- `dependencies/` — pinned release/image identities, licenses, and SBOM inputs.
- `threat-model/` — V1 trust boundaries and controls.
- `docs/requirements-traceability.yaml` — normative requirement ownership and verification ledger.
- `tests/phase0/` — source-lock and contract tests.
- `.agent/phase-records/` — qualification records.
- `src/` — reserved for Phase 1+ implementation.

## Inclusion rules

- Explain why every mapped path matters.
- Prefer important entry points and boundaries over exhaustive listings.
- Exclude vendored dependencies, caches, temporary task notes, and generated files unless their role matters.
- Update the map when a touched or newly understood area changes.

## Entry format after adoption

Use entries like this only in an adopted repository:

```text
<path/to/important-area> — why the path matters
```
