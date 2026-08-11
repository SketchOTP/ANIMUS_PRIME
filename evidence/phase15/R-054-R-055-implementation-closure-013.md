# Phase 15 R-054/R-055 local implementation closure — Continuation 013

- Baseline: `PRIME-SPEC-V1.0.0`
- Directive: `D-PRIME-PHASE15-REMEDIATION-013`
- Implementation commit: `10e0650a6fd14df3837baa7b45ff60d9ec33693b`
- Evidence/governance commit: `e81010f27ef74b34e6bdc7d2618a219ac61ba2bb`
- Implementation result: `R-054 IMPLEMENTED`, `R-055 IMPLEMENTED`
- Implementation convergence: `25/26`
- R-056: remains `OPEN` and is not marked implementation-complete
- Qualification result: `R-054/R-055 blocked_by_environment`; no requirement is `VERIFIED`
- V1 result: `ANIMUS PRIME V1 QUALIFICATION: FAIL`
- Deployment: `NOT PERFORMED`

## Implemented boundary

`src/prime_core/ai_service.py` is the Core-owned AI execution boundary. It provides:

- function-specific profiles for the approved model-backed functions;
- profile, prompt, schema, retrieval-policy, and fixture revisions;
- explicit `CLOUD_MODELS_ALLOWED` and `LOCAL_ONLY` policy checks;
- no automatic provider or local-to-cloud fallback;
- bounded source admission with project-ID isolation, source identity/revision capture, path/context bounds, secret redaction, and inert untrusted-data wrapping;
- structured output validation for Ask, Progress/Alignment, memory admission, and Documentation paths;
- Ask epistemic categories `SOURCE FACT`, `DERIVED INTERPRETATION`, and `UNKNOWN`;
- citation validation against the admitted source set;
- rejection of chain-of-thought/reasoning fields and whole-page documentation rewrite requests;
- deterministic degraded/unknown behavior for provider absence, provider failure, privacy blocks, and invalid output;
- durable `ai_runs` provenance and `usage_records` attribution without raw provider credentials or hidden reasoning;
- version-controlled machine-readable golden AI fixtures.

Ask PRIME now supplies bounded repository and memory text from the current project only and routes model execution through this boundary. If the configured provider is unavailable or privacy policy blocks it, Ask returns `UNKNOWN` with an explicit degraded run status rather than a fabricated project fact.

## Focused evidence

`tests/phase15/test_ai_execution.py` covers:

- fixture revision and machine-readable expected properties;
- successful profile execution and durable source/profile/usage provenance;
- prompt-injection text remaining data with no tool authority and secret redaction;
- citation rejection outside the admitted source set;
- Project A rejecting a Project B source;
- `LOCAL_ONLY` blocking a cloud provider without fallback;
- reasoning-field rejection and non-persistence.

## Qualification separation and blockers

The focused tests exercise a deterministic local provider double. They do not qualify an approved live provider or approved local inference stack. Live qualification remains blocked because no approved AI provider/model credentials or local inference environment were configured in this runtime. No provider key was printed, persisted, sent to the browser, Node, MCP, Notion, `.agent`, evidence, or backup.

The full regression result for this continuation is `54 passed, 17 skipped`. Database-backed phase qualification, live provider/local model execution, isolated Project A/B end-to-end fixtures, browser qualification, and aggregate R-056 clean-install qualification remain unverified. Codebase-memory indexing again returned `Transport closed`; targeted local inspection was used as the documented fallback.

## MyAssistant Notion secret-source trace

The existing `NOTION_READONLY_KEY` source was not present in PRIME's runtime environment. Local configuration and launcher inspection found no usable existing source. The factual state is `NOT FOUND IN INSPECTED SOURCES`; no secret value was displayed or recorded. PRIME's prior secret-safe credential-reference import remains present and live Notion capability remains blocked.
