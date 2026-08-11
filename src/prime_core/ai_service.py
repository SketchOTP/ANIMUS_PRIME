"""Bounded, project-scoped AI execution and evaluation boundary.

The model is an untrusted implementation detail.  This module owns profile
selection, source admission, privacy checks, structured-output validation,
durable provenance, and usage attribution.  Provider credentials and raw
provider payloads never leave the Core process or enter durable records.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import time
import uuid
from dataclasses import dataclass
from typing import Any, Callable, Protocol

from .db import connect, transaction
from .service import now

PRIVACY_MODES = {"CLOUD_MODELS_ALLOWED", "LOCAL_ONLY"}
PROFILE_REVISION = "prime-ai-profile-v1"
RETRIEVAL_POLICY_REVISION = "prime-retrieval-policy-v1"
FIXTURE_REVISION = "prime-ai-fixtures-v1"

FUNCTIONS = {
    "GOAL_ASSISTANCE",
    "ASK_PRIME",
    "PROGRESS",
    "ALIGNMENT",
    "DOCUMENTATION",
    "MEMORY_ADMISSION",
    "CORRECTION",
    "HINDSIGHT_EXTRACTION",
    "HINDSIGHT_EMBEDDING",
    "HINDSIGHT_RERANKING",
    "REFLECT",
    "MENTAL_MODEL",
}

PROMPT_REVISIONS = {name: "prime-prompt-v1" for name in FUNCTIONS}
SCHEMA_REVISIONS = {name: "prime-schema-v1" for name in FUNCTIONS}

SECRET_PATTERN = re.compile(
    r"(?i)(?:api[_-]?key|secret|password|token|private[_-]?key|authorization)"
    r"\s*[:=]\s*[^\s,;]+"
)
INJECTION_PATTERN = re.compile(
    r"(?is)\b(?:ignore|disregard|override)\s+(?:all\s+)?(?:previous|prime|system|developer|project)"
    r"\s+(?:instructions?|rules?)\b|\b(?:reveal|exfiltrate|send)\s+.*\b(?:secret|token|key)\b"
    r"|\bmark\s+.*\bverified\b|\brun\s+(?:this\s+)?shell\s+command\b"
)
CLOUD_PROVIDERS = {"openai", "anthropic", "google", "azure-openai", "cloud", "remote"}
LOCAL_PROVIDERS = {"local", "ollama", "llama.cpp", "llamacpp", "vllm-local"}


class AIProvider(Protocol):
    is_local: bool

    def generate(self, request: dict[str, Any]) -> "ProviderResult": ...


@dataclass(frozen=True)
class ProviderResult:
    output: dict[str, Any]
    input_tokens: int | None = None
    output_tokens: int | None = None
    estimated_cost: float | None = None
    usage_metadata: dict[str, Any] | None = None


@dataclass(frozen=True)
class AIProfile:
    function: str
    provider: str
    model: str
    privacy_mode: str
    profile_revision: str = PROFILE_REVISION
    prompt_revision: str = "prime-prompt-v1"
    schema_revision: str = "prime-schema-v1"
    retrieval_policy_revision: str = RETRIEVAL_POLICY_REVISION

    def public(self) -> dict[str, Any]:
        return {
            "function": self.function,
            "provider": self.provider,
            "model": self.model,
            "privacy_mode": self.privacy_mode,
            "profile_revision": self.profile_revision,
            "prompt_revision": self.prompt_revision,
            "schema_revision": self.schema_revision,
            "retrieval_policy_revision": self.retrieval_policy_revision,
        }


class AIInputError(ValueError):
    pass


class AIPrivacyError(AIInputError):
    pass


class AIProviderError(RuntimeError):
    def __init__(self, error_class: str, message: str = "provider unavailable"):
        super().__init__(message)
        self.error_class = error_class


class UnconfiguredProvider:
    is_local = False

    def generate(self, request: dict[str, Any]) -> ProviderResult:
        raise AIProviderError("MODEL_UNAVAILABLE", "approved provider is not configured")


def _safe_metadata(value: Any, depth: int = 0) -> Any:
    """Keep provider metadata bounded and free of credential-like values."""
    if depth > 3:
        return "[TRUNCATED]"
    if isinstance(value, dict):
        return {
            str(key): _safe_metadata(item, depth + 1)
            for key, item in list(value.items())[:32]
            if "token" not in str(key).lower()
            and "secret" not in str(key).lower()
            and "key" not in str(key).lower()
            and "password" not in str(key).lower()
        }
    if isinstance(value, (list, tuple)):
        return [_safe_metadata(item, depth + 1) for item in list(value)[:32]]
    if isinstance(value, (str, int, float, bool)) or value is None:
        text = str(value)
        if SECRET_PATTERN.search(text):
            return "[REDACTED]"
        return value
    return str(type(value).__name__)


def redact_text(value: str) -> str:
    return SECRET_PATTERN.sub(lambda match: f"{match.group(0).split('=')[0].split(':')[0]}=[REDACTED]", value)


def _contains_chain_of_thought(value: Any) -> bool:
    if isinstance(value, dict):
        return any(
            str(key).lower().replace("-", "_") in {"chain_of_thought", "cot", "reasoning_trace", "hidden_reasoning"}
            or _contains_chain_of_thought(item)
            for key, item in value.items()
        )
    if isinstance(value, list):
        return any(_contains_chain_of_thought(item) for item in value)
    return False


def _provider_is_local(provider_name: str, provider: AIProvider | None) -> bool:
    if provider is not None:
        return bool(getattr(provider, "is_local", False))
    return provider_name.lower() in LOCAL_PROVIDERS or provider_name.lower().endswith("-local")


def _source_identity(source: dict[str, Any]) -> dict[str, Any]:
    allowed = {
        "source_class",
        "source_id",
        "source_revision",
        "content_hash",
        "locator",
        "privacy_class",
        "project_id",
        "freshness_state",
        "historical_boundary",
    }
    result = {key: source.get(key) for key in allowed if source.get(key) is not None}
    if not result.get("source_class"):
        raise AIInputError("every admitted source requires source_class")
    if not result.get("source_id") and not result.get("locator"):
        raise AIInputError("every admitted source requires source_id or locator")
    return result


def admit_sources(project_id: str, sources: list[dict[str, Any]], *, privacy_mode: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Return bounded model context and durable source identities.

    Source text is data only.  It is wrapped as untrusted content and never
    becomes an instruction or authorization signal.
    """
    if privacy_mode not in PRIVACY_MODES:
        raise AIPrivacyError("unsupported privacy mode")
    if len(sources) > 32:
        raise AIInputError("AI source set exceeds the bounded source limit")
    context: list[dict[str, Any]] = []
    identities: list[dict[str, Any]] = []
    for source in sources:
        if source.get("project_id") not in (None, project_id):
            raise AIInputError("cross-project source admission rejected")
        identity = _source_identity(source)
        privacy_class = str(source.get("privacy_class", "PROJECT_PRIVATE")).upper()
        if privacy_class in {"SECRET", "CREDENTIAL", "OPERATOR_SECRET"}:
            raise AIPrivacyError("secret-classified source cannot enter model context")
        raw = str(source.get("text", ""))
        if len(raw) > 12000:
            raw = raw[:12000] + " [TRUNCATED]"
        redacted = redact_text(raw)
        context.append({
            "source": identity,
            "untrusted_data": redacted,
            "contains_prompt_injection": bool(INJECTION_PATTERN.search(redacted)),
        })
        identities.append(identity)
    return context, identities


def _validate_output(function: str, output: dict[str, Any], source_ids: set[str]) -> dict[str, Any]:
    if not isinstance(output, dict):
        raise AIInputError("model output must be an object")
    if _contains_chain_of_thought(output):
        raise AIInputError("chain-of-thought fields are not accepted")
    output = _safe_metadata(output)
    if function == "ASK_PRIME":
        category = str(output.get("category", "UNKNOWN")).upper()
        if category not in {"SOURCE FACT", "DERIVED INTERPRETATION", "UNKNOWN"}:
            raise AIInputError("Ask output has an invalid epistemic category")
        output["category"] = category
        if category == "UNKNOWN":
            output["answer"] = "UNKNOWN: available evidence does not support this claim."
        citations = output.get("citations", [])
        if not isinstance(citations, list) or len(citations) > 16:
            raise AIInputError("Ask citations must be a bounded list")
        for citation in citations:
            if not isinstance(citation, dict) or str(citation.get("source_id", "")) not in source_ids:
                raise AIInputError("Ask citation is not in the admitted source set")
    elif function in {"PROGRESS", "ALIGNMENT"}:
        if not any(key in output for key in ("status", "assessment", "goal_items", "alignment", "unknown")):
            raise AIInputError("assessment output is missing a structured result")
        for citation in output.get("citations", []) or []:
            if not isinstance(citation, dict) or str(citation.get("source_id", "")) not in source_ids:
                raise AIInputError("assessment citation is not in the admitted source set")
    elif function == "MEMORY_ADMISSION":
        if not isinstance(output.get("admit"), bool):
            raise AIInputError("memory admission requires an explicit admit boolean")
        for citation in output.get("citations", []) or []:
            if not isinstance(citation, dict) or str(citation.get("source_id", "")) not in source_ids:
                raise AIInputError("memory citation is not in the admitted source set")
    elif function == "DOCUMENTATION":
        if not isinstance(output.get("sections", {}), dict):
            raise AIInputError("documentation output requires targeted sections")
        if output.get("whole_page_rewrite") is True:
            raise AIInputError("whole-page documentation rewrites are prohibited")
    return output


class AIExecutionService:
    def __init__(self, settings: Any, providers: dict[str, AIProvider] | None = None, clock: Callable[[], Any] = now):
        self.settings = settings
        self.providers = providers or {}
        self.clock = clock
        self.default_provider = os.getenv("PRIME_AI_PROVIDER", "unconfigured").strip() or "unconfigured"
        self.default_model = os.getenv("PRIME_AI_MODEL", "unconfigured").strip() or "unconfigured"
        self.default_privacy = os.getenv("PRIME_AI_PRIVACY_MODE", "LOCAL_ONLY").strip().upper() or "LOCAL_ONLY"

    def profile(self, function: str, *, project_privacy_mode: str | None = None) -> AIProfile:
        function = function.upper()
        if function not in FUNCTIONS:
            raise AIInputError("unsupported AI function")
        prefix = "PRIME_AI_" + function
        provider = os.getenv(prefix + "_PROVIDER", self.default_provider).strip() or "unconfigured"
        model = os.getenv(prefix + "_MODEL", self.default_model).strip() or "unconfigured"
        privacy = os.getenv(prefix + "_PRIVACY_MODE", project_privacy_mode or self.default_privacy).strip().upper()
        if privacy not in PRIVACY_MODES:
            raise AIPrivacyError("unsupported privacy mode")
        return AIProfile(function, provider, model, privacy, prompt_revision=PROMPT_REVISIONS[function], schema_revision=SCHEMA_REVISIONS[function])

    def public_profiles(self) -> list[dict[str, Any]]:
        return [self.profile(function).public() for function in sorted(FUNCTIONS)]

    def execute(
        self,
        project_id: str,
        function: str,
        prompt_input: dict[str, Any],
        sources: list[dict[str, Any]],
        *,
        project_privacy_mode: str | None = None,
    ) -> dict[str, Any]:
        profile = self.profile(function, project_privacy_mode=project_privacy_mode)
        started = time.monotonic()
        run_id = "ai_" + uuid.uuid4().hex
        provider = self.providers.get(profile.provider)
        try:
            context, source_set = admit_sources(project_id, sources, privacy_mode=profile.privacy_mode)
            if profile.privacy_mode == "LOCAL_ONLY" and not _provider_is_local(profile.provider, provider):
                raise AIPrivacyError("LOCAL_ONLY blocks non-local model provider")
            if provider is None:
                provider = UnconfiguredProvider()
            request = {
                "project_id": project_id,
                "function": profile.function,
                "profile": profile.public(),
                "input": _safe_metadata(prompt_input),
                "sources": context,
                "source_policy": "untrusted-data-no-authority-no-tools",
            }
            result = provider.generate(request)
            output = _validate_output(profile.function, result.output, {str(item.get("source_id")) for item in source_set})
            status = "SUCCEEDED"
            error_class = None
            input_tokens = result.input_tokens
            output_tokens = result.output_tokens
            estimated_cost = result.estimated_cost
            usage_metadata = _safe_metadata(result.usage_metadata or {})
        except AIPrivacyError as exc:
            status, error_class, output = "DEGRADED", "PRIVACY_BLOCKED", {"category": "UNKNOWN", "answer": "UNKNOWN: privacy policy prevents this model run.", "citations": []}
            input_tokens = output_tokens = estimated_cost = None
            usage_metadata = {"message": str(exc)}
        except AIProviderError as exc:
            status, error_class, output = "DEGRADED", exc.error_class, {"category": "UNKNOWN", "answer": "UNKNOWN: model provider unavailable.", "citations": []}
            input_tokens = output_tokens = estimated_cost = None
            usage_metadata = {"message": "provider unavailable"}
        except (AIInputError, ValueError) as exc:
            status, error_class, output = "REJECTED", "INVALID_OUTPUT_OR_INPUT", {"category": "UNKNOWN", "answer": "UNKNOWN: model output or input was rejected.", "citations": []}
            input_tokens = output_tokens = estimated_cost = None
            usage_metadata = {"message": str(exc)}
        except Exception:
            status, error_class, output = "DEGRADED", "PROVIDER_ERROR", {"category": "UNKNOWN", "answer": "UNKNOWN: model execution failed.", "citations": []}
            input_tokens = output_tokens = estimated_cost = None
            usage_metadata = {"message": "provider failure"}
        latency_ms = round((time.monotonic() - started) * 1000, 3)
        record = {
            "run_id": run_id,
            "project_id": project_id,
            "function": profile.function,
            "provider": profile.provider,
            "model": profile.model,
            "profile_revision": profile.profile_revision,
            "prompt_revision": profile.prompt_revision,
            "schema_revision": profile.schema_revision,
            "retrieval_policy_revision": profile.retrieval_policy_revision,
            "fixture_revision": FIXTURE_REVISION,
            "privacy_mode": profile.privacy_mode,
            "source_revision_set": source_set if "source_set" in locals() else [],
            "created_at": self.clock(),
            "status": status,
            "latency_ms": latency_ms,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "estimated_cost": estimated_cost,
            "provider_usage": usage_metadata,
            "error_class": error_class,
            "result": output,
        }
        self._persist(record)
        return _public_record(record)

    def _persist(self, record: dict[str, Any]) -> None:
        with transaction(self.settings) as db:
            db.execute(
                "INSERT INTO prime_core.ai_runs(run_id,project_id,function,provider,model,profile_revision,prompt_revision,schema_revision,retrieval_policy_revision,fixture_revision,privacy_mode,source_revision_set,created_at,status,latency_ms,input_tokens,output_tokens,estimated_cost,provider_usage,error_class,result) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (record["run_id"], record["project_id"], record["function"], record["provider"], record["model"], record["profile_revision"], record["prompt_revision"], record["schema_revision"], record["retrieval_policy_revision"], record["fixture_revision"], record["privacy_mode"], json.dumps(record["source_revision_set"]), record["created_at"], record["status"], record["latency_ms"], record["input_tokens"], record["output_tokens"], record["estimated_cost"], json.dumps(record["provider_usage"]), record["error_class"], json.dumps(record["result"])),
            )
            units = (record["input_tokens"] or 0) + (record["output_tokens"] or 0)
            db.execute(
                "INSERT INTO prime_core.usage_records(usage_id,project_id,capability,provider,units,estimated_cost,occurred_at,metadata) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                ("usage_" + uuid.uuid4().hex, record["project_id"], record["function"], record["provider"], units, record["estimated_cost"], record["created_at"], json.dumps({"run_id": record["run_id"], "model": record["model"], "status": record["status"], "usage_state": "known" if record["input_tokens"] is not None or record["output_tokens"] is not None else "unknown", "cost_state": "known" if record["estimated_cost"] is not None else "unavailable"})),
            )


def _public_record(record: dict[str, Any]) -> dict[str, Any]:
    result = dict(record)
    result["created_at"] = result["created_at"].isoformat() if hasattr(result["created_at"], "isoformat") else result["created_at"]
    return result


def fixture_fingerprint(fixture: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(fixture, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
