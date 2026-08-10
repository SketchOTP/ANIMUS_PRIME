# Phase 7 qualification

Phase 7 establishes a safe Notion projection boundary:

- PRIME-managed markers are updated in place;
- user-authored content outside the markers is preserved;
- missing/ambiguous markers produce `CONFLICT` without replacement;
- provider outage produces retryable `DEGRADED` state;
- projection revisions and content hashes are durable and idempotent.

The provider adapter remains separate from canonical project state; a Notion outage does not block repository or memory work.
