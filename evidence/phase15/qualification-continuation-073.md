# ANIMUS PRIME — Phase 15 Qualification Continuation 073

## Result

BLOCKED — ATLAS_PARAGON_SERVICE_RESTART_REQUIRES_INTERACTIVE_AUTH

The first hard routing divergence was objectively identified and the smallest PARAGON correction was implemented, regression-tested, committed, and published. The existing persistent PARAGON service could not be restarted from the authorized SSH session because Atlas requires interactive authentication for both systemctl restart and sudo -n systemctl restart. The running process still serves the pre-repair code. The exact original Continuation 072 Reflect query was therefore not rerun against the repaired runtime.

No Mental Model was created.

## Baseline

- Frozen specification: PRIME-SPEC-V1.0.0.
- PRIME starting governed SHA: 25ac64dc891224f7592f3b1d016787b83bbb2e49.
- PRIME final SHA after this evidence closeout: recorded by the final governed publication.
- PARAGON starting published SHA: a5d1485c7b61b3328d028db299d24aadf60c894f.
- PARAGON published repair SHA: 60c1668de0af459629d8f1e6148b46f167d08ad9.
- PARAGON GitHub main: verified at 60c1668de0af459629d8f1e6148b46f167d08ad9.
- PRIME execution: direct SSH/native Atlas at /home/sketch/Projects/ANIMUS_PRIME; no Z: execution.
- PRIME source and persistent runtime were not changed.
- PARAGON existing service: paragon.service, /usr/bin/node /home/sketch/Projects/paragon-production/src/server.js, pre-attempt MainPID 4123592, active since 2026-08-16 05:36:44 EDT, private health {"ok":true}.
- Hindsight and PRIME bank were not touched in this continuation.

## Phase A — routing differential

The live read-only /api/diagnostics/routing/preview path was used against the existing PARAGON process. Results were summarized without prompts, secrets, or raw provider payloads.

### A. Known-good tool-mediated shape

- workType: unknown.
- estimatedRequiredContextTokens: 16000.
- candidates: 150.
- eligible: 129.
- exclusions: 19 lacked verified OpenAI tool calls; 2 were unhealthy.
- result: PASSED as a routing-eligible differential control.

### B. Exact original 072 query

Exact query:

What recurring architectural invariants, safety boundaries, proven failure modes, recovery practices, and qualification rules should future ANIMUS PRIME engineering sessions understand to preserve project continuity and avoid repeating previously solved or disproven work?

With the same bounded tool request shape:

- workType: architecture.
- workTypeScores: {"architecture":3}.
- estimatedInputTokens: 1000.
- requestedMaxOutputTokens: 1024.
- estimatedRequiredContextTokens: 200000.
- candidates: 150.
- eligible: 0.
- exclusions: 129 routing.unknownContextForLargeRequest, 19 routing.capabilityUnsupported.toolCalls, 2 eligibility.unhealthyProvider.
- result: BLOCKED at routing eligibility before provider dispatch.

The first hard divergence from A is the architecture semantic context floor, not Hindsight bank state, tool semantics, or provider dispatch.

### C. Controlled lexical perturbation

Only architectural invariants was replaced with system invariants. The remainder of the query and tool request shape stayed the same.

- workType: unknown.
- estimatedRequiredContextTokens: 16000.
- candidates: 150.
- eligible: 129.
- exclusions: 19 lacked verified OpenAI tool calls; 2 were unhealthy.
- result: PASSED as classifier evidence only.

This was not used as a production workaround.

## Root cause and repair

PARAGON's estimatedContextRequirementTokens treated the semantic architecture demand of 200000 as a hard context requirement even when the request contract was a small tool-mediated call. Hindsight Reflect retrieves source state incrementally through native tools, so the initial model context must be gated by actual request and output capacity, not by assuming the full retrieved project corpus is already present.

Published PARAGON repair 60c1668:

- src/routing/taskProfile.js: when the output contract is tool_call, semantic work-type context demand is excluded from the hard requirement; actual estimated input plus requested output remains.
- ordinary non-tool semantic context floors remain unchanged.
- test/automaticRouting.test.js: added a small architecture-labeled tool request regression and a large tool request regression proving real capacity protection remains.

No word-specific, Hindsight-specific, global threshold, tool-verification, catalog, CLI-routing, or provider semantics were weakened.

## Validation

- A/B/lexical routing differential: PASSED.
- focused PARAGON routing tests: PASSED; 59 selected tests, including both new regressions.
- syntax checks: PASSED.
- full PARAGON regression: FAILED; 440 passed, 1 failed, the unrelated pre-existing submitAuthCode timing test (test/authCodeSubmit.test.js); no failure implicated the changed files.
- PARAGON release scan: PASSED.
- staged secret scan: PASSED; no credential material in the published diff.
- staged diff review: PASSED; only the intended routing source and two focused tests were staged/committed. Pre-existing unrelated PARAGON worktree changes remain unstaged and preserved.
- PARAGON GitHub publication: PASSED; GitHub main equals 60c1668de0af459629d8f1e6148b46f167d08ad9.
- existing PARAGON health before restart attempt: PASSED.
- existing PARAGON service restart: BLOCKED; direct systemctl reported interactive authentication required and sudo -n systemctl reported the same.
- repaired PARAGON runtime health: NOT RUN.
- exact original 072 Reflect preflight after repair: NOT RUN.
- current stale-runtime exact-query preview: BLOCKED with the old architecture/200000/0 eligible profile. This was not treated as repaired-runtime evidence.
- PRIME product tests/runtime qualification: NOT APPLICABLE; no PRIME product/runtime change.
- Mental Model creation/read/persistence: NOT RUN.
- deployment/public exposure: NOT PERFORMED.

## Governance disposition

- DOD-068 remains BACKEND_ONLY.
- R-054 and all other DOD/R statuses remain unchanged.
- Continuation 072 historical blocker label is preserved. Continuation 073 records the append-only correction that the source bank was sufficient and the actual blocker was routing eligibility.
- PRIME runtime Notion prerequisite remains pending and untouched.
- DOD-005 remains parked.
- DOD-081 and R-056 remain gated/last.
- Phase 15 remains incomplete; V1 is not declared.
- No Notion change was made by this run.
- No Hindsight data/configuration, bank, project, Core/UI, Tailscale/Funnel, public exposure, or Phase 16 state was changed.

## Exact operator action required

Provide the existing approved non-interactive Atlas authority for restarting the PRIME-approved PARAGON service, or perform this exact bounded operation on Atlas:

systemctl restart paragon.service

Then verify the new MainPID/start time and private health, and rerun only the exact original 072 Reflect source query. Do not create the Mental Model until that preflight produces genuine native Hindsight tool calls and a substantive response.

## Closeout

Continuation 073 is BLOCKED, not FAILED. The PARAGON root cause is fixed and published, but the running service has not loaded it. No stale-runtime result is being relabeled as success.

## Post-restart resumption — runtime qualification

Resumption date: 2026-08-16.

The operator-provided restart resolved the previous 073 deployment gate without any code or configuration change in this run.

- paragon.service ActiveState/SubState: active/running.
- new MainPID: 607574.
- new ActiveEnterTimestamp: 2026-08-16 14:03:00 EDT.
- established private health: PASSED, GET http://127.0.0.1:4117/health returned {"ok":true}.
- live repaired routing preview for the exact query shape: PASSED; architecture classification retained, output contract tool_call, estimated required context 2024, 150 candidates, 129 eligible.
- existing Hindsight health/database: PASSED.
- existing PRIME bank: prime-project_d9a1a5b609394282b62fc12c0d04634d.
- exact original Continuation 072 query: used verbatim, with no lexical or semantic rewrite.

### Exact Reflect result

- HTTP status: 200.
- answer: substantive markdown response, 7897 characters.
- native tool-call trace: 4 calls.
- native tool names: search_observations, search_observations, recall, recall.
- LLM calls: 3.
- provenance-bearing memories in based_on: 198.
- mental models in based_on: 0.
- directives in based_on: 0.
- result: PASSED; no no_eligible_model, unavailable fallback, or prose-only tool substitution occurred.
- answer began with a continuity-preserving architectural summary and was grounded in prior PRIME records.

This proves the repaired persistent PARAGON runtime can support the exact Hindsight Reflect source preflight. It does not create or qualify a Mental Model.

### Mental Model safety boundary

- Mental Model listing after Reflect: 0 items.
- Mental Model creation: NOT RUN by instruction.
- Hindsight bank/project isolation: PASSED for this read-only qualification.
- DOD-068: remains BACKEND_ONLY.
- No DOD/R promotion, PRIME source change, Hindsight mutation, Notion change, deployment, public exposure, Phase 16, DOD-005, DOD-081, or R-056 activity occurred.

### Resumption disposition

- Continuation 073 post-restart runtime qualification: PASSED.
- Original 073 full-suite concern remains recorded: 440 passed and one pre-existing unrelated submitAuthCode timing failure.
- The prior ATLAS_PARAGON_SERVICE_RESTART_REQUIRES_INTERACTIVE_AUTH blocker is resolved by the operator restart and is preserved as historical evidence.
- Do not create the Mental Model in this continuation.
- Do not begin Continuation 074 automatically.
