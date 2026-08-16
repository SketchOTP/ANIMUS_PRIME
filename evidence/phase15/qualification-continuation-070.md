# ANIMUS PRIME - Phase 15 Continuation 070 Evidence

Status: PARTIAL / BLOCKED
Date: 2026-08-16 Atlas local execution
Directive: Continuation 070 - PARAGON general AI activation and Hindsight native-tool compatibility

## Baseline

- Frozen specification: PRIME-SPEC-V1.0.0.
- Canonical Atlas checkout: /home/sketch/Projects/ANIMUS_PRIME.
- Starting/local HEAD: fc8700561520906de643018e2cd7f5c37b587699.
- origin/main after fetch: fc8700561520906de643018e2cd7f5c37b587699.
- Worktree: only pre-existing untracked .codebase-memory/, .prime-evidence/, and .vscode/; no tracked source changes.
- Existing PostgreSQL, Hindsight, PRIME Qualification Project, PRIME bank, and enrolled Node were preserved.
- The protected PARAGON credential was reused through the existing mode-0600 Atlas runtime secret path. Its raw value was never printed, logged, committed, or written here.

## Persistent topology

- PostgreSQL: existing persistent Atlas PostgreSQL; Core readiness reported CONNECTED.
- PRIME Core: existing user service animus-prime-core.service; container animus-prime-core; image animus-prime-core:continuation-065; UID/GID 1000:1000; private listener 127.0.0.1:18000; durable state mount preserved.
- PRIME Web UI: genuine Core-served UI at the private Core interface; no replacement UI.
- Hindsight: existing user service mimir-hindsight.service; container mimir-hindsight-production; image ghcr.io/vectorize-io/hindsight@sha256:ffa391a77284e49f6b55e32c86f33529ac4257831407b14038a72b6a0a232039; private listener 127.0.0.1:8888; durable data mount preserved.
- Hindsight after restart: provider=openai, base URL=https://atlas-2.tail1a5964.ts.net:10000/v1, model=paragon.
- Repository Node: existing 127.0.0.1:18001 identity/state preserved and not changed.
- Both user services remained enabled. Old Core/Hindsight containers were retained as named rollback artifacts after controlled swaps.
- Public exposure: none; no Funnel, firewall, Tailscale, or public ingress change.

The first Core replacement failed closed because it inherited image user nobody and could not read the existing durable state file. It was removed as the failed replacement only; no data/database reset occurred. The replacement was recreated with UID/GID 1000:1000 and passed readiness. Hindsight was swapped through its existing service and same image/data mount.

## Core and general PRIME AI

- /health/live: PASSED - prime-core live.
- /health/ready: PASSED - PRIME-SPEC-V1.0.0, schema 0036_operator_workflows.sql, build commit fc8700561520906de643018e2cd7f5c37b587699.
- Authenticated local-identity session: PASSED; operator password was not changed.
- /v1/system/ai/profiles: PASSED - provider_configured=true; provider=paragon; model=paragon; privacy_mode=LOCAL_ONLY; fallback_policy=NONE_UNLESS_EXPLICIT_PROFILE; credential_policy=CORE_ONLY.
- /v1/system/setup: PASSED - ai_provider READY, storage READY, Hindsight service_connectivity CURRENT, Notion UNCONFIGURED.
- Existing Qualification Project: project_d9a1a5b609394282b62fc12c0d04634d.
- ASK_PRIME through /v1/projects/.../ai/execute with LOCAL_ONLY: PASSED.
- Result: SUCCEEDED, provider/model paragon/paragon, structured category UNKNOWN with bounded UNKNOWN answer and empty citations; durable run ai_180883b195ef4447a9430e328385d16d.
- Provider usage metadata was returned; estimated cost was null and correctly remained unknown.

PRIME_GENERAL_AI_PARAGON = PASS. This proves ordinary persistent Core completion/structured JSON. It does not claim native Hindsight tool calling or R-045/DOD-047 limits/cost enforcement.

## Hindsight and PARAGON capability

- Hindsight /health: PASSED - healthy, database connected.
- Existing PRIME bank: prime-project_d9a1a5b609394282b62fc12c0d04634d; bank isolation present; no substitute bank created.
- Existing bank retain/store: PASSED; actual Qualification Project runtime fact retained under document_id continuation-070-runtime.
- Existing bank recall: PASSED; retained document identity was returned.
- Direct harmless single-function PARAGON probe: PASSED - HTTP 200, finish_reason=tool_calls, one message.tool_calls entry, function prime_hindsight_probe, JSON argument value probe-070; route provider=openrouter, routedProvider=openrouter, fallback=false.
- Exact Hindsight native tool set (search_mental_models, search_observations, recall, expand, done), tested with automatic choice and forced recall: BLOCKED - HTTP 503 no_eligible_model; no message.tool_calls.
- Hindsight Reflect: HTTP 200 response, but not a pass. Logs show repeated 503 reflect_tool_call failures, then a no-tool fallback; reflect completed with tools=none and 0 tool calls.
- Hindsight Mental Models: endpoint HTTP 200 with {"items":[]}; no model exists in the existing bank. No synthetic model was created.

HINDSIGHT_REFLECT_VIA_PARAGON = BLOCKED
HINDSIGHT_MENTAL_MODELS = BLOCKED

## Governance and scope

- No requirement or DOD promoted.
- R-054/R-055 prior governed status remains unchanged.
- R-045/DOD-047 remain OPEN/PARTIAL: provider profile is available, but usage/cost throttling/refusal and configurable limits remain unqualified.
- DOD-068 remains BACKEND_ONLY and blocked by the exact Hindsight native-tool boundary.
- Notion prerequisite from 067 remains pending and untouched; DOD-005 remains parked.
- DOD-081 and R-056 remain gated/open. Phase 15 remains incomplete; V1 is not declared.
- No deployment, public exposure, Funnel change, or Phase 16 activity occurred.

## Validation

- Core and Hindsight controlled service swaps/restart recovery: PASSED.
- Core live/readiness, private listener ownership, and authenticated protected API: PASSED.
- PRIME general AI structured execution: PASSED.
- PARAGON single-function native tool-call structure: PASSED.
- Exact Hindsight five-tool payload compatibility: BLOCKED.
- Hindsight health/database/bank/retain/recall: PASSED.
- Hindsight Reflect native tool execution: BLOCKED.
- Mental Models positive qualification: BLOCKED.
- Governance validation and diff checks: PASSED. Focused and full regression tests: BLOCKED because Atlas Python test collection lacks psycopg; no dependencies were installed or persistent runtime altered.
- Deployment/public exposure: NOT PERFORMED.

## Exact blocker

BLOCKED - HINDSIGHT_NATIVE_TOOL_SET_UNAVAILABLE

Current capability: PARAGON emits genuine tool calls for a compatible single-function request, but rejects the exact Hindsight five-tool Reflect request with HTTP 503 no_eligible_model. Hindsight Reflect falls back without tools; the existing bank has no Mental Models.

Operator action required: provide or approve a PARAGON HTTP routing/model capability that accepts the existing Hindsight tool set and returns message.tool_calls, or provide an explicitly approved Hindsight-backed tool-calling model/profile. Do not replace Hindsight or mimic its tools inside PRIME.

## Closeout classification

- PRIME_GENERAL_AI_PARAGON = PASS
- HINDSIGHT_REFLECT_VIA_PARAGON = BLOCKED
- HINDSIGHT_MENTAL_MODELS = BLOCKED
- Continuation 070 = PARTIAL / BLOCKED
