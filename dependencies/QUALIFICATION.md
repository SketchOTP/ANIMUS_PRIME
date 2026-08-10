# Phase 0 Dependency Qualification

The exact pins are recorded in `pins.yaml`. Registry manifest inspection verified the pinned amd64 image digests. Source release identities were verified from the upstream Hindsight and pgvector Git repositories. PostgreSQL 17.10 is within the upstream supported PostgreSQL 17 series.

## Required smoke matrix

| Component | Normal | Unavailable | Degraded | Recovery | Status |
|---|---|---|---|---|---|
| PostgreSQL 17.10 + pgvector 0.8.2 | migration/extension smoke | connection failure | restart/retry | backup/restore | pending |
| Hindsight 0.6.1 | bank/retain/recall/reflect/model | provider/database outage | adapter status | export/restore | pending |
| Python 3.13.7 | harness | missing runtime | dependency error | clean rebuild | pending |
| Docker/Compose | service start | daemon unavailable | health failure | restart | pending |

Phase 0 cannot record `PASS` until the runnable smoke evidence is attached under `evidence/phase0/` and the status table is updated with commands and results.

The current environment has Docker 29.1.3 and Compose 2.40.3 but no host `psql`; the qualification uses pinned containers.
