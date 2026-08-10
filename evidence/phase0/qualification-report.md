# Phase 0 Qualification Evidence

Baseline: `PRIME-SPEC-V1.0.0`

Qualification host: Linux amd64, Docker 29.1.3, Compose 2.40.3.

## Source lock

- Specification export: `baseline/PRIME-SPEC-V1.0.0.notion.md`
- Specification SHA-256: `557dcd7e96325f59910d8cdd74dc5c933b680389bbe5ef35f0d9b83920ee6c5c`
- Handoff export SHA-256: `f47fffa6a7e3ca00299d6840e06648bd7756b7a3d67bf4ce6c8fa7464be716dd`
- Operator handoff manifest SHA-256: `48306047cbd84df583bca6530f25d3dd3c1674d490d11a6e621add0238f36ec9`
- Authority manifest SHA-256: `42b977f29a830988cd5531e7ffcae381e55d210c0b34b583763d1c4984075362`
- Authority file hashes: `sha256sum -c authority-template/v1/MANIFEST.sha256` — PASSED.
- Deliberate mutated specification hash mismatch — PASSED (mismatch rejected).

## Contract and governance checks

- Reference authority validator — PASSED.
- Adopted project governance validator — PASSED.
- Requirements traceability: 30 assigned records; zero `UNASSIGNED` records — PASSED.
- Project-isolation contract tests — PASSED.
- SBOM JSON parse — PASSED.

## Dependency and persistence smoke

- Pinned Hindsight 0.6.1 image pulled at `sha256:2b92…5217` — PASSED.
- Pinned PostgreSQL 17.10 image pulled at `sha256:dbbe…e99b` — PASSED.
- Pinned pgvector 0.8.2 image pulled at `sha256:e04a…a93` — PASSED.
- Hindsight migrations against PostgreSQL completed — PASSED.
- `vector` extension reported version `0.8.2` — PASSED.
- Hindsight `/health` reported `{"status":"healthy","database":"connected"}` — PASSED.

## Hindsight adapter smoke

Using the local deterministic OpenAI-compatible fixture (no external provider egress):

- bank create — PASSED;
- retain with durable recall verification — PASSED;
- recall — PASSED;
- Reflect — PASSED;
- Mental Model create/refresh — PASSED;
- export template — PASSED;
- delete and import template — PASSED;
- two-bank project isolation — PASSED.

Using an unavailable provider configuration:

- Hindsight upstream acknowledged retain but stored no memory — observed;
- PRIME adapter postcondition check returned `DEGRADED` — PASSED;
- no false durable-write success was exposed through the adapter — PASSED.

## Tests

- `python3 -m pytest tests/phase0 -q` — PASSED, 9 tests.
- `python3 scripts/validate_governance.py --mode ADOPTED` — PASSED.
- `python3 authority-template/v1/scripts/validate_governance.py --mode TEMPLATE` — PASSED.
- `python3 scripts/phase0_qualify.py` — pending final governed qualification commit.

## Security and recovery

- Project scope derives the Hindsight bank identifier; caller-supplied bank switching is not exposed — PASSED.
- Path-like project IDs are rejected — PASSED.
- Export/import/delete recovery path — PASSED.
- No secrets or raw provider logs are stored in evidence — PASSED.

## Result

Phase 0 is ready for final governed qualification commit. Phase 1 remains gated until the phase record contains `result: PASS` and the exact qualified commit.
