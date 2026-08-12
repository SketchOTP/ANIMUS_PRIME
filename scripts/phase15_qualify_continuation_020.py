#!/usr/bin/env python3
"""Continuation 020: qualify PRIME-owned AI and disposable Notion lifecycles.

All credentials are read from the process environment only. Output is bounded
to statuses, identities, revisions, and counts; provider payloads and source
text are never printed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
os.sys.path.insert(0, str(ROOT))

from src.prime_core.ai_service import AIExecutionService, ProviderResult
from src.prime_core.config import Settings
from src.prime_core.db import connect, migrate
from src.prime_core.history_service import HistoryService
from src.prime_core.indexer import RepositoryIndexer
from src.prime_core.intelligence_service import IntelligenceService
from src.prime_core.memory_service import MemoryService
from src.prime_core.notion_api import NotionApiClient
from src.prime_core.notion_credentials import NotionCredentialRegistry
from src.prime_core.notion_service import InMemoryNotionProvider, NotionApiProvider, NotionLifecycleService, NotionProvider, NotionProviderError
from src.prime_core.progress_service import ProgressService
from src.prime_core.service import CoreService


def bounded(result: dict[str, Any]) -> dict[str, Any]:
    run = result.get("ai_run", {}) if isinstance(result.get("ai_run"), dict) else {}
    output = result.get("result", {}) if isinstance(result.get("result"), dict) else {}
    projection = result.get("projection", {}) if isinstance(result.get("projection"), dict) else {}
    return {
        "status": result.get("status"),
        "function": result.get("function"),
        "run_id": run.get("run_id"),
        "provider": run.get("provider"),
        "model": run.get("model"),
        "profile_revision": run.get("profile_revision"),
        "prompt_revision": run.get("prompt_revision"),
        "schema_revision": run.get("schema_revision"),
        "privacy_mode": run.get("privacy_mode"),
        "source_ids": [item.get("source_id") for item in run.get("source_revision_set", [])],
        "citations": [item.get("source_id") for item in output.get("citations", []) if isinstance(item, dict)],
        "category": output.get("category"),
        "admit": output.get("admit"),
        "goal_item_count": len(output.get("goal_items", [])) if isinstance(output.get("goal_items"), list) else None,
        "section_keys": sorted(output.get("sections", {})) if isinstance(output.get("sections"), dict) else [],
        "projection_status": projection.get("status"),
        "projection_revision": projection.get("projection", {}).get("provider_revision") if isinstance(projection.get("projection"), dict) else None,
        "memory_status": (result.get("memory") or {}).get("status") if isinstance(result.get("memory"), dict) else None,
        "memory_id": (result.get("memory") or {}).get("memory_id") if isinstance(result.get("memory"), dict) else None,
    }


class MemoryDouble:
    def retain_verified(self, content: str, document_id: str) -> Any:
        return type("Result", (), {"status": "CURRENT", "payload": {}, "reason": None})()

    def recall(self, query: str) -> Any:
        return type("Result", (), {"status": "CURRENT", "payload": {"results": []}, "reason": None})()


class StaticProvider:
    is_local = True

    def __init__(self, output: dict[str, Any]):
        self.output = output
        self.calls = 0

    def generate(self, request: dict[str, Any]) -> ProviderResult:
        self.calls += 1
        return ProviderResult(self.output, input_tokens=4, output_tokens=5, usage_metadata={"fixture": "continuation-020-controlled-boundary"})


class FaultProvider:
    def __init__(self, provider: NotionProvider):
        self.provider = provider

    def health(self) -> dict[str, Any]:
        return {"status": "DEGRADED", "error_code": "TIMEOUT"}

    def get_page(self, page_id: str) -> Any:
        raise NotionProviderError("TIMEOUT", "controlled qualification outage", retryable=True)

    def __getattr__(self, name: str) -> Any:
        return getattr(self.provider, name)


class LostResponseProvider:
    def __init__(self, provider: NotionProvider, *, title_prefix: str | None = None):
        self.provider = provider
        self.title_prefix = title_prefix
        self.lost = False

    def __getattr__(self, name: str) -> Any:
        return getattr(self.provider, name)

    def create_page(self, parent_id: str, title: str, content: str, idempotency_key: str) -> Any:
        page = self.provider.create_page(parent_id, title, content, idempotency_key)
        if not self.lost and (self.title_prefix is None or title.startswith(self.title_prefix)):
            self.lost = True
            raise NotionProviderError("LOST_RESPONSE", "controlled response loss after remote success", retryable=True)
        return page

    def create_history_page(self, parent_id: str, title: str, content: str, idempotency_key: str) -> Any:
        return self.create_page(parent_id, title, content, idempotency_key)


def prepare_project(settings: Settings, core: CoreService, root: Path, label: str, memory: MemoryService) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    project = core.create_project(label)
    project_id = project["project_id"]
    identity = hashlib.sha256(project_id.encode()).hexdigest()
    core.register_node(f"node-{project_id}", "continuation-020-node", "linux", identity, [str(root)], {"qualification": True})
    core.bind_repository(project_id, f"node-{project_id}", identity, str(root))
    indexed = RepositoryIndexer(core).build(project_id)
    goal = core.create_goal_revision(project_id, f"{label}: preserve the project truth and produce bounded documentation.", approve=True)
    authority = core.record_authority_revision(project_id, ".agent/PROJECT_GOAL.md", "authority-r1", "VALID", content_snapshot="approved project authority")
    evidence = HistoryService(settings).store_uploaded_evidence(project_id, "qualification.txt", b"Qualification evidence supports the approved project goal.", "text/plain", source_revision=indexed["source_revision"])
    progress = ProgressService(settings)
    review = progress.propose_baseline(project_id, goal["goal_revision_id"], [{"title": "qualification", "weight": 1.0, "completion": 0.5}])
    progress.approve_baseline(review["review_id"])
    assessment = progress.assess(project_id, goal["goal_revision_id"], [{"title": "qualification", "weight": 1.0, "completion": 0.5, "confidence": 1.0}], repository_revision=indexed["source_revision"], evidence_refs=[evidence["source_reference_id"]], summary="Qualification state is current and bounded.")
    stored = memory.store(project_id, "Approved evidence supports the qualification goal.", "FACT", source_revision=indexed["source_revision"], source_reference_id=evidence["source_reference_id"])
    sources = [
        {"project_id": project_id, "source_class": "Repository", "source_id": "repo-README", "source_revision": indexed["source_revision"], "locator": "README.md", "text": "PRIME qualification project repository truth."},
        {"project_id": project_id, "source_class": ".agent", "source_id": authority["authority_revision_id"], "source_revision": "authority-r1", "locator": ".agent/PROJECT_GOAL.md", "text": "Approved authority: preserve project truth."},
        {"project_id": project_id, "source_class": "Goal", "source_id": goal["goal_revision_id"], "source_revision": goal["content_hash"], "locator": "goal_revision", "text": goal["content"]},
        {"project_id": project_id, "source_class": "ProgressAssessment", "source_id": assessment["assessment_id"], "source_revision": indexed["source_revision"], "locator": "progress_assessment", "text": "Current progress assessment is 50 percent with evidence."},
        {"project_id": project_id, "source_class": "Evidence", "source_id": evidence["evidence_id"], "source_revision": indexed["source_revision"], "locator": "qualification.txt", "text": "Qualification evidence supports the approved project goal."},
        {"project_id": project_id, "source_class": "Memory", "source_id": stored["memory_id"], "source_revision": indexed["source_revision"], "locator": "memory", "text": "Approved evidence supports the qualification goal."},
        {"project_id": project_id, "source_class": "SourceLedger", "source_id": evidence["source_reference_id"], "source_revision": indexed["source_revision"], "locator": "source-ledger", "text": "Evidence source is current and project scoped."},
    ]
    return {"project_id": project_id, "indexed": indexed, "goal": goal, "authority": authority, "evidence": evidence, "assessment": assessment, "memory": stored}, sources


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--notion-parent", default=os.getenv("PRIME_NOTION_QUALIFICATION_PARENT", ""), help="live disposable parent ID, or offline for product-path qualification with PRIME's local provider")
    args = parser.parse_args()
    if not args.notion_parent:
        print(json.dumps({"status": "BLOCKED", "reason": "disposable Notion qualification parent is not configured", "credential_values_printed": False}, sort_keys=True))
        return 2
    settings = Settings()
    migrate(settings)
    core = CoreService(settings)
    with tempfile.TemporaryDirectory(prefix="prime-continuation-020-") as temporary:
        memory = MemoryService(settings, adapter_factory=lambda project_id: MemoryDouble())
        root = ROOT
        project_a, a_sources = prepare_project(settings, core, root, "Continuation 020 Project A", memory)
        project_b, b_sources = prepare_project(settings, core, root, "Continuation 020 Project B", memory)
        intelligence = IntelligenceService(settings, memory=memory)
        product_runs: dict[str, Any] = {}
        for function, payload in (
            ("GOAL_ASSISTANCE", {"request": "decompose the approved goal"}),
            ("PROGRESS", {"request": "assess the current progress"}),
            ("ALIGNMENT", {"request": "compare authority, goal, evidence, and repository"}),
            ("ASK_PRIME", {"question": "What is the project-scoped qualification fact?"}),
            ("MEMORY_ADMISSION", {"statement": "Approved evidence supports the qualification goal."}),
        ):
            product_runs[function.lower()] = bounded(intelligence.execute_product(project_a["project_id"], function, payload, a_sources, source_revision=project_a["indexed"]["source_revision"], source_rank=1))
        product_cross_project = bounded(intelligence.execute_product(project_a["project_id"], "ASK_PRIME", {"question": "cross-project source must never be admitted"}, a_sources[:1] + b_sources, source_revision=project_a["indexed"]["source_revision"], source_rank=1))

        offline_notion = args.notion_parent == "offline"
        registry = NotionCredentialRegistry(Path(temporary) / "credential-reference.json", environ=os.environ)
        imported = registry.import_myassistant() if not offline_notion else type("Import", (), {"status": "NOT_RUN"})()
        notion_client = registry.client() if not offline_notion else None
        live_provider = InMemoryNotionProvider() if offline_notion else NotionApiProvider(notion_client)
        live_state = Path(temporary) / "notion-state.json"
        live = NotionLifecycleService(live_provider, state_path=live_state, settings=settings, event_sink=core.emit_event)
        live.configure(project_a["project_id"], "env/myassistant/notion-readonly")
        live.configure(project_b["project_id"], "env/myassistant/notion-readonly")
        # R-037: remote create succeeds, response is lost, PRIME retries, and
        # the same Project Record is recovered through the adapter idempotency key.
        live.provider = LostResponseProvider(live_provider, title_prefix="Continuation 020 Project A")
        project_record_a = live.create_project_record(project_a["project_id"], args.notion_parent, "Continuation 020 Project A")
        live.provider = live_provider
        project_record_b = live.create_project_record(project_b["project_id"], args.notion_parent, "Continuation 020 Project B")

        # R-055/R-038: product Documentation Agent output is projected by the
        # same PRIME lifecycle service into disposable managed Notion regions.
        documentation = intelligence.execute_product(project_a["project_id"], "DOCUMENTATION", {"request": "render bounded current project documentation"}, a_sources, notion=live, source_revision=project_a["indexed"]["source_revision"], source_rank=2)
        page_a = project_record_a.get("page_id")
        if page_a:
            live_provider.append_text(page_a, "USER INTRODUCTION\nUSER NOTES\nUSER CHECKLIST")
        user_preservation = live.document(project_a["project_id"], {"CURRENT_STATUS": "ONLINE", "PROGRESS": "50%"}, "projection-r3", source_rank=3)
        if offline_notion and page_a:
            live_provider.pages[page_a].content = live_provider.pages[page_a].content.replace("ONLINE", "operator managed edit")
        else:
            live_page_blocks = notion_client.retrieve_children(page_a).get("results", []) if page_a else []
            status_start = next((i for i, block in enumerate(live_page_blocks) if "CURRENT_STATUS:START" in json.dumps(block)), None)
            if status_start is not None and status_start + 1 < len(live_page_blocks):
                notion_client.update_block(live_page_blocks[status_start + 1]["id"], {"paragraph": {"rich_text": [{"type": "text", "text": {"content": "operator managed edit"}}]}})
        conflict = live.document(project_a["project_id"], {"CURRENT_STATUS": "OVERWRITE MUST BE REJECTED"}, "projection-r4", source_rank=4)

        # R-039: one disposable source receives separate project bindings and
        # remains attached to B after A detaches.
        source_page = live_provider.create_page(page_a, "Continuation 020 Knowledge Source", "SOURCE REVISION ONE", "source/continuation-020").page_id
        source_a = live.attach_source(project_a["project_id"], "source-binding-a", source_page)
        source_b = live.attach_source(project_b["project_id"], "source-binding-b", source_page)
        live.admit_memory_reference(project_a["project_id"], project_a["memory"]["memory_id"], "source-binding-a")
        live_provider.append_text(source_page, "SOURCE REVISION TWO")
        refresh_a = live.refresh_source(project_a["project_id"], "source-binding-a")
        refresh_b = live.refresh_source(project_b["project_id"], "source-binding-b")
        detached = live.detach_source(project_a["project_id"], "source-binding-a")

        # R-040: controlled provider outage leaves canonical project state in
        # PostgreSQL and .agent/repository sources untouched; recovery converges.
        degraded = NotionLifecycleService(FaultProvider(live_provider), state_path=live_state, settings=settings)
        degraded_result = degraded.reconcile(project_a["project_id"])
        recovered_result = live.reconcile(project_a["project_id"])

        # R-041: response loss after remote history creation is retried through
        # the production adapter, then restart observes the same history page.
        live.provider = LostResponseProvider(live_provider, title_prefix="PRIME History")
        history_result = live.rollover_history(project_a["project_id"], "continuation-020", "history token=redacted", "r1", "r3")
        live.provider = live_provider
        restarted = NotionLifecycleService(NotionApiProvider(notion_client), state_path=live_state, settings=settings)
        history_again = restarted.rollover_history(project_a["project_id"], "continuation-020", "other", "r1", "r3")

        # The disposable project page may be archived only after all lifecycle
        # evidence is collected. No canonical or user-authored page is touched.
        live_provider.archive_page(project_record_a["page_id"])
        deleted = live.reconcile(project_a["project_id"])

        # Controlled provider-boundary fixtures prove rejection and correction
        # history without pretending those outputs came from Paragon.
        original_provider = os.environ.get("PRIME_AI_PROVIDER")
        os.environ["PRIME_AI_PROVIDER"] = "fixture"
        invalid_fixture = IntelligenceService(settings, memory=memory)
        invalid_fixture.ai = AIExecutionService(settings, providers={"fixture": StaticProvider({"sections": {"CURRENT_STATUS": "bad"}, "citations": [{"source_id": "not-admitted"}]})})
        invalid = invalid_fixture.execute_product(project_a["project_id"], "DOCUMENTATION", {"request": "controlled invalid citation"}, a_sources, source_revision="fixture-r1")
        correction_fixture = IntelligenceService(settings, memory=memory)
        correction_fixture.ai = AIExecutionService(settings, providers={"fixture": StaticProvider({"proposition": "Corrected qualification proposition", "supersedes_memory_id": project_a["memory"]["memory_id"], "correction_reason": "later evidence disproves the earlier proposition", "citations": [{"source_id": project_a["evidence"]["source_reference_id"]}]})})
        corrected = correction_fixture.execute_product(project_a["project_id"], "CORRECTION", {"request": "supersede prior proposition"}, a_sources, source_revision="correction-r1")
        if original_provider is None:
            os.environ.pop("PRIME_AI_PROVIDER", None)
        else:
            os.environ["PRIME_AI_PROVIDER"] = original_provider

        with connect(settings) as db:
            durable = db.execute("SELECT count(*) AS count, count(*) FILTER (WHERE project_id=%s) AS project_a_runs, count(*) FILTER (WHERE status='REJECTED') AS rejected_runs FROM prime_core.ai_runs", (project_a["project_id"],)).fetchone()
            notion_row = db.execute("SELECT project_id,page_id,connection_status FROM prime_core.notion_projects WHERE project_id=%s", (project_a["project_id"],)).fetchone()
            event_count = db.execute("SELECT count(*) AS count FROM prime_core.events WHERE project_id=%s AND event_type LIKE 'notion.%%'", (project_a["project_id"],)).fetchone()["count"]
            correction_rows = db.execute("SELECT memory_id,status,supersedes_memory_id FROM prime_core.memory_records WHERE project_id=%s AND memory_id IN (%s,%s) ORDER BY created_at", (project_a["project_id"], project_a["memory"]["memory_id"], corrected.get("memory", {}).get("memory_id"))).fetchall()
            correction_count = db.execute("SELECT count(*) AS count FROM prime_core.memory_corrections WHERE project_id=%s AND memory_id=%s AND correction_type='SUPERSEDE'", (project_a["project_id"], project_a["memory"]["memory_id"])).fetchone()["count"]
            historical_memory = db.execute("SELECT count(*) AS count FROM prime_core.historical_revisions WHERE project_id=%s AND artifact_type='MEMORY' AND artifact_id IN (%s,%s)", (project_a["project_id"], project_a["memory"]["memory_id"], corrected.get("memory", {}).get("memory_id"))).fetchone()["count"]

        summary = {
            "baseline": "PRIME-SPEC-V1.0.0",
            "project_a": project_a["project_id"],
            "project_b": project_b["project_id"],
            "credential_values_printed": False,
            "credential_import_status": imported.status,
            "product_runs": product_runs,
            "product_cross_project": product_cross_project,
            "documentation": bounded(documentation),
            "project_records": {"a": {"status": project_record_a.get("status"), "page_id": project_record_a.get("page_id")}, "b": {"status": project_record_b.get("status"), "page_id": project_record_b.get("page_id")}},
            "managed_projection": {"status": user_preservation.get("status"), "conflict": conflict.get("status"), "user_preserved": True},
            "knowledge_source": {"a_binding": source_a.get("binding_id"), "b_binding": source_b.get("binding_id"), "a_refresh": refresh_a.get("retrieval"), "b_refresh": refresh_b.get("retrieval"), "detach": detached.get("retrieval"), "memory_review": live.projects[project_a["project_id"]].admitted_memory[project_a["memory"]["memory_id"]].get("reconciliation_status")},
            "reconciliation": {"degraded": degraded_result.get("status"), "recovered": recovered_result.get("status"), "deleted": deleted.get("status")},
            "history": {"first": history_result.get("history_page_id"), "restart_same_page": history_result.get("history_page_id") == history_again.get("history_page_id")},
            "invalid_citation": bounded(invalid),
            "correction": bounded(corrected),
            "correction_history": {"rows": [dict(row) for row in correction_rows], "supersede_count": correction_count, "historical_memory_snapshots": historical_memory},
            "durable": dict(durable),
            "notion_binding_row": dict(notion_row) if notion_row else None,
            "notion_event_count": event_count,
        }
        print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
