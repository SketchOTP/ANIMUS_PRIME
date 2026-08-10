# Phase 3 qualification

Phase 3 adds explicit repository-backed onboarding foundations:

- project binding to an enrolled Node/repository identity;
- lifecycle transition into `PROVISIONING`, with online/current/normal state only after an explicit binding;
- immutable goal revision content hashes and operator approval status;
- authority revision observations carrying contract version, path, hash and validation status;
- narrowly scoped authority-template provisioning that refuses to overwrite existing authority;
- onboarding tables owned by PRIME Core migrations.

The phase does not treat model output or a request payload as authority; the operator approval bit and authority validator are explicit.
