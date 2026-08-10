# Phase 5 qualification

Phase 5 keeps Hindsight behind the PRIME memory adapter and adds the canonical PRIME memory ledger:

- one bank identity `prime-{project_id}` per project;
- verified retain status (`STORED`, `DEGRADED`, `QUEUED`) rather than trusting an HTTP acknowledgement;
- source revision, branch context, content class and document provenance;
- duplicate suppression, secret-sensitive rejection, tombstone/correction state;
- recall results filtered through the authenticated project's ledger before exposure.

Reflect/Mental Model outputs remain derived and are not part of the authoritative ledger.
