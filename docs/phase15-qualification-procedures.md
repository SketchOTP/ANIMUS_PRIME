# Phase 15 deterministic qualification procedures

These procedures are the Continuation 005 external-qualification queue. A procedure is not evidence of execution. The operator records command output, provider before/after state, timestamps, environment identity, and the exact implementation/evidence commits only after a real run.

## R-031/R-032/R-033 — native Node lifecycle

Prerequisites: supported native Linux host and supported Windows host, Core/TLS material, disposable repository fixture, reboot permission, and the exact package under qualification.

Setup: install through `packaging/node/README.md` and the platform installer; bind a repository under an approved root; enroll the Node with mTLS; save service status, identity, version, and repository-root evidence.

Commands/actions: start; enroll; heartbeat; restart; kill the service; reboot the host; verify automatic startup and reconnect; reconcile watcher/offline state; rotate credentials; reject the old credential; revoke; reject the revoked Node; re-enroll; execute the documented upgrade path.

Expected results: persistent identity and repository-root boundary survive restart/reboot; authenticated heartbeat resumes; offline/reconnect and watcher reconciliation are explicit; old/revoked credentials fail; re-enrollment and upgrade report the expected version.

Negative test: missing/incompatible TLS material, path escape, symlink/junction escape, old credential, revoked Node, and incompatible protocol must fail closed.

Recovery test: service crash, host reboot, Core outage, credential rotation, revocation, re-enrollment, and upgrade must recover without changing project identity.

Evidence: native OS/service identity, install output, service status before/after, reboot timestamps, authenticated heartbeat, failure responses, credential lifecycle, repository binding, version/upgrade output.

PASS criteria: Linux and Windows each satisfy every listed action with captured evidence. FAIL criteria: any platform is simulated, any recovery path is absent, or any credential/path boundary fails.

## R-035/R-036 — Tailscale Serve

Prerequisites: signed-in tailnet, an approved second tailnet device, running PRIME Core, and permission to toggle Serve. Never use Funnel.

Setup: record `tailscale status`, `tailscale serve status`, Core listener binding, PRIME authentication state, and the second-device identity.

Commands/actions: configure the fixed private Serve path; access HTTPS from the second device; authenticate to PRIME; disable/re-enable Serve; restart Core; verify recovery; inspect Funnel/public-listener state.

Expected results: only private tailnet HTTPS reaches PRIME; PRIME auth remains required; local access works when Serve is unavailable; restart and re-enable recover.

Negative test: Funnel/public exposure and arbitrary CLI input are refused; unauthenticated remote access is denied.

Recovery test: Serve disabled, Tailscale unavailable, and Core restarted; local functionality remains available and private access returns after reconciliation.

Evidence: both-device timestamps/screenshots or HTTP captures, Serve status before/after, auth responses, listener exposure, fixed argv audit, and recovery output.

PASS criteria: second authorized device reaches private HTTPS and no public listener exists. FAIL criteria: no second-device evidence, Funnel enabled, public bind, or missing PRIME auth.

## R-037–R-041 — live Notion lifecycle

Prerequisites: controlled Notion workspace/token with least privilege, disposable Project Record, managed and user-authored regions, Knowledge Source, and transport fault injection.

Setup: capture provider page ID/revision and content before PRIME writes; record managed-block identities separately from user content.

Commands/actions: create/bind/render; repeat idempotently; update managed blocks; edit user content; induce managed conflict, stale revision, missing permission, outage, moved/deleted page; reconnect/reconcile; attach/refresh/detach/retract Knowledge Source; exercise history rollover threshold.

Expected results: managed writes preserve user content, self-writes are suppressed, conflicts are surfaced, retries queue durably, reconnect reconciles, detach retracts current retrieval without claiming external deletion, and rollover preserves linked history.

Negative test: invalid token, permission loss, moved/deleted page, conflict, and stale revision.

Recovery test: provider outage and reconnect, queued work replay, reconciliation, and resumed rollover.

Evidence: provider before/after JSON or screenshots, page IDs/revisions, managed-block map, queue/retry records, source attach/refresh/detach state, and historical rollover pages.

PASS criteria: all lifecycle actions run against real Notion and preserve ownership boundaries. FAIL criteria: adapter-only tests, fabricated provider state, lost user content, or silent conflict/retraction.

## R-042–R-045 — backup, restore, and capacity

Prerequisites: populated disposable PRIME state, off-machine backup target, clean install host, representative Hindsight/Evidence/Git/Notion metadata, disk/queue pressure harness, and recovery key custody.

Setup: capture IDs, bindings, progress, memory continuity, evidence, history, settings, Notion bindings, events, quotas, and baseline health.

Commands/actions: create encrypted backup; verify manifest/high-water checkpoint; restore to clean install; compare all captured state; run corrupt, wrong-key, version-mismatch, interrupted, collision, quota, disk-pressure, queue-backpressure, retention, and referenced-evidence cases.

Expected results: clean restore preserves identity/bindings/history or labels explicitly degraded components; invalid backups fail before destructive mutation; capacity controls backpressure and protect referenced evidence.

Negative test: corrupt/truncated backup, wrong key, version mismatch, destination failure, restore collision, quota overrun, and public/plaintext secret exposure.

Recovery test: retry destination, resume interrupted restore, reconcile queue/checkpoint, and recover from disk pressure.

Evidence: encrypted artifact hash, manifest, state comparison, restore logs, failure responses, disk/queue metrics, retention decisions, and rollback/safety checkpoint.

PASS criteria: restore succeeds into a clean environment and every failure path is safe. FAIL criteria: backup-only evidence, missing component continuity, destructive partial restore, or unbounded pressure.

## R-046–R-050 — Evidence and Time Lens

Prerequisites: qualified PostgreSQL, representative real artifacts, parser/index execution, multi-commit repository, authority/progress/GoalModel/Notion/Hindsight history, and a reversible historical-removal fixture.

Setup: create commits at multiple boundaries; record authority, progress, memory, Evidence, and Notion projection revisions; capture hashes and source references.

Commands/actions: upload/reference artifacts; validate MIME/content/size/privacy; retrieve/cite; associate validation; retract; index/reindex; reconstruct each boundary; remove historical information; ask/search/Brain at `as_of`; rewrite/prune/GC Git objects and restore PRIME-owned checkpoints.

Expected results: hashes/provenance/citations resolve to the used artifact; retracted content leaves current retrieval; historical views report `EXACT`, `PARTIAL`, or `UNAVAILABLE`; later data is excluded; no state is invented.

Negative test: active content, bad MIME, oversize, missing parser, retracted source, unavailable checkpoint, later correction, and pruned Git history.

Recovery test: parser/index recovery, restored checkpoint, reindex, and return-to-current.

Evidence: artifact metadata/content hashes, parser/index status, citations, retraction events, per-source Time Lens status, Git bundle/object hash, and historical Ask/Brain output.

PASS criteria: every source class is truthful and project-bound at each selected boundary. FAIL criteria: current data substituted for historical data, retracted evidence remains current, or citations drift silently.

## R-051–R-053 — browser/operator UX

Prerequisites: running qualified Core/Web stack and supported desktop/mobile browser contexts.

Setup: start from clean setup state; capture viewport/device, browser version, keyboard-only mode, reduced-motion preference, and health state.

Commands/actions: complete first-run setup; navigate global and project surfaces; run normal, empty, loading, stale, offline, degraded, error, destructive, Brain-fallback, keyboard, responsive, and reduced-motion flows.

Expected results: operator can complete the workflow without terminal/database knowledge; states are truthful and recoverable; destructive actions require confirmation.

Negative test: invalid setup/lifecycle action, offline service, stale health, empty/error state, and inaccessible Brain canvas.

Recovery test: retry/reconnect/restart and resume without losing project state.

Evidence: browser version/viewport, screenshots or equivalent acceptance captures, network/error state, keyboard path, and recovery results.

PASS criteria: desktop and mobile/responsive journeys satisfy the baseline. FAIL criteria: endpoint-only evidence, inaccessible state, silent stale/offline state, or destructive action without confirmation.

## R-054/R-055 — approved AI qualification

Prerequisites: approved provider/model/profile, configuration revision, isolated Project A/B fixtures, privacy/egress policy, and usage/cost capture.

Setup: freeze provider/model/profile/configuration and fixtures; record source set and project identity; ensure prompt-injection fixtures are treated as untrusted data.

Commands/actions: execute Goal decomposition, Progress, Ask, Documentation Agent, Alignment, memory admission/correction, UNKNOWN, citation, privacy, injection, and project-isolation flows.

Expected results: outputs are source-labeled, cited, project-bound, privacy-compliant, cost-attributed, and fail/degrade honestly; corrections and UNKNOWN remain explicit.

Negative test: invalid output, provider failure, prompt injection, cross-project retrieval, absent citation, and unauthorized egress.

Recovery test: retry/fallback and replay with same frozen fixture/configuration.

Evidence: provider/model/profile/config revision, fixture hash, prompt/source IDs, output, usage/cost, privacy decision, and PASS/FAIL per flow.

PASS criteria: all approved flows pass with reproducible evidence. FAIL criteria: provider/profile drift, uncited/inferred state, cross-project leakage, or unbounded egress.

## R-056 — full V1 walkthrough

Prerequisites: all R-031–R-055 verified, fresh install, Linux/Windows, Notion, Tailscale, Hindsight, approved AI, backup/restore, and browser environments.

Setup: freeze the governed candidate commit and capture all environment versions/identities.

Commands/actions: execute the complete operator journey, all failure/degraded/recovery branches, clean restore/reconnect, and security/isolation/egress/destructive checks.

Expected results: every requirement is exercised from fresh install through continuity and recovery.

Negative/recovery/security tests: use the complete branch set from R-031–R-055.

Evidence: end-to-end report with exact commits, environment manifests, captures, and per-requirement traceability.

PASS criteria: 26/26 VERIFIED, OPEN/IMPLEMENTING/BLOCKED all zero, Phase-15 PASS. FAIL criteria: any missing evidence or unresolved row.
