# Continuation 087 Qualification Fixture Ledger

All entries in this ledger are explicitly marked `V1_QUALIFICATION_FIXTURE`
and are isolated from canonical production project state.

## Existing tracked lab

- Root: `/home/sketch/ANIMUS_PRIME_V1_QUALIFICATION_LAB`
- Existing continuation-083 fixture: `V1_QUALIFICATION_FIXTURE_083`
- Project ID: `project_ab2cb29717864418a05352542fc5ac19`
- Repository ID: `repo_b1fcb6db7e70492eaaf77c312dd4db0e`
- Repository path: `/home/sketch/Projects/ANIMUS_PRIME_V1_QUALIFICATION_FIXTURE_083`
- Node: `node-041-atlas-native`
- Canonical project protected: `true`
- Fixture lifecycle after bounded deletion qualification: `DELETION_PENDING`

## Continuation-087 isolated databases

- `prime087_restore`: isolated restore/recovery qualification database
- `prime087_fresh`: isolated fresh/onboarding boundary database
- `prime087_fork`: isolated fork/child-resource boundary database
- Runtime evidence root: `/var/lib/animus-prime-core/qualification-087/evidence`

These fixtures must not be treated as canonical project state or as evidence
of external-resource clauses. Retention/cleanup remains governed by the next
explicitly authorized closeout and must not touch the canonical installation.
