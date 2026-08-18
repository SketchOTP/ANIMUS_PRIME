# Continuation 092 Destructive Lifecycle Interruption Matrix

Date: 2026-08-18

Fixture: `project_1921e46142c54a63bdddf4ecea5dca0b`

| Lifecycle | Interruption boundary | Observed stopped state | Resume/reconciliation result | Duplicate/orphan result |
|---|---|---|---|---|
| DELETE | Live Notion archive returned but response was treated as lost | Core exited 91; `NOTION_DISPOSITION` remained RUNNING | Restart inspected the archived live page and completed the same DELETE workflow | One page identity; external survival recorded; no duplicate page |
| DELETE | Repository quarantine completed before response persistence | Core exited 91; original path absent and recorded quarantine path present | Restart adopted the recorded quarantine and completed the same DELETE workflow | One quarantine path; canonical repository unaffected |
| DELETE | Project credentials/grants revoked before step completion persisted | Core exited 91 | Restart re-ran idempotent revocation and completed the same DELETE workflow | Existing grant remained revoked; no new grant |
| PURGE | Hindsight bank deleted before response persistence | Core exited 91 | Restart confirmed absence and completed the same PURGE workflow | Bank absent; no substitute bank or memory |
| PURGE | Local project-controlled rows deleted before step completion persisted | Core exited 91 while durable workflow/project identity remained recoverable | Restart used the completed purge plan, finished local cleanup, wrote one tombstone, and completed the same workflow | One tombstone; no duplicate project/resource recreation |

## Step outcomes

DELETE final ordered steps all SUCCEEDED: `PREFLIGHT_VERIFIED`, `SNAPSHOT_DISPOSITION`, `NOTION_DISPOSITION`, `REPOSITORY_QUARANTINED`, `ACTIVE_WORK_STOPPED`, `CREDENTIALS_REVOKED`, `RESOURCE_DISPOSITION_RECORDED`, `STATE_TRANSITIONED`.

PURGE final ordered steps all SUCCEEDED: `PURGE_PLAN_VERIFIED`, `HINDSIGHT_PURGED`, `REPOSITORY_PURGED`, `LOCAL_RESOURCES_PURGED`, `MINIMAL_TOMBSTONE_WRITTEN`, `PURGE_COMPLETED`.

Expected retry attempts were visible only at injected interruption seams. All final dispositions are explicit; no step was silently treated as complete, no external resource was recreated to manufacture recovery, and no canonical project or repository was used as a destructive target.

## Refusal matrix

| Negative | Result | Mutation guarantee |
|---|---|---|
| Missing/invalid CSRF | 403 | Project remained PROVISIONING |
| Wrong project identity | 403 | State unchanged |
| Wrong repository identity/path confirmation | 403 | Project remained DELETION_PENDING; PURGE did not begin |
| Stale/replayed preflight | Refused | Existing workflow did not advance until a fresh authorized preflight was supplied |
| Symlink/unrecorded quarantine target | Refused by Node boundary | No unrecorded filesystem deletion |
| Canonical repository target | Outside authorized fixture and protected by exact binding/root checks | Canonical repository intact |
