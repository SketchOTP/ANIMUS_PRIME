# Phase 2 qualification

Phase 2 establishes the read-only Node boundary:

- one-time bootstrap enrollment and rotating node credential stored as a digest;
- explicit allowed roots with real-path resolution and symlink/path escape rejection;
- bounded UTF-8 file reads with binary and size rejection;
- allowlisted Git subprocess inspection only, including unborn repositories and bare-repository rejection;
- stable Git common-directory identity fingerprint and Core node/repository registry tables;
- separate Node HTTP service and container shape, with repository volume mounted read-only.

Evidence: `tests/phase2`, `scripts/phase2_qualify.py`, and the Phase 0/1 regression suite.
