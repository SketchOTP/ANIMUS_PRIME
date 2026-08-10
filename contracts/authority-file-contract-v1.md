# AuthorityFileContract v1

Status: `FROZEN_FOR_PHASE_0`

The materialized package at `authority-template/v1/` is the approved source for project authority bootstrap. It is versioned, manifest-backed, and validated independently of the implementation.

## Required artifacts

The package contains the required root instruction files, `.agent` ledgers, Cursor integration files, Mimir skill, and dependency-free governance validator. The package must validate in `TEMPLATE` mode before it can be provisioned into a project.

## Authority rules

1. `.agent/PROJECT_GOAL.md` is the authoritative project goal after adoption.
2. `.agent` files are observed even when repository ignore rules exclude them.
3. PRIME may provision or repair authority only through explicit lifecycle operations.
4. PRIME must not silently rewrite an adopted goal or authority file.
5. Codex bridge creation must not overwrite an existing root `AGENTS.md`.
6. Conflicting nested `AGENTS.md` / `AGENTS.override.md` instructions are surfaced as integrity conditions.
7. Every authority observation carries project identity, source path, content hash, observed time, and authority revision.
8. The package is an implementation input, not a replacement for repository or project authority.

## Validation

The reference validator is `authority-template/v1/scripts/validate_governance.py`. Phase 0 qualification requires exact file-set, content-hash, and validator checks. A missing or mismatched manifest is a hard failure.
