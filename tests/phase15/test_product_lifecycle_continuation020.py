from __future__ import annotations

import hashlib

from src.prime_core.notion_service import NotionApiProvider, NotionLifecycleService, NotionProviderError


class FakeNotionClient:
    def __init__(self):
        self.pages = {}
        self.counter = 0
        self.searches = []

    def provider_health(self):
        return {"status": "CONNECTED", "workspace_id": "qualification"}

    def search_pages(self, query):
        self.searches.append(query)
        return {"results": [{"id": page_id} for page_id, page in self.pages.items() if query in "\n".join(block["text"] for block in page["blocks"])]}

    def create_page(self, parent, properties, children):
        self.counter += 1
        page_id = f"remote-{self.counter}"
        parent_id = parent.get("page_id") if isinstance(parent, dict) else parent
        self.pages[page_id] = {"parent": parent_id, "title": properties["title"]["title"][0]["text"]["content"], "blocks": [{"id": f"block-{self.counter}-{i}", "text": next(iter(block[block["type"]]["rich_text"]))["text"]["content"]} for i, block in enumerate(children)]}
        return {"id": page_id}

    def retrieve_page(self, page_id):
        page = self.pages[page_id]
        return {"id": page_id, "parent": {"page_id": page["parent"]}, "properties": {"title": {"type": "title", "title": [{"plain_text": page["title"]}]}}, "last_edited_time": "2026-08-12T01:00:00.000Z"}

    def retrieve_children(self, page_id):
        return {"results": [{"id": block["id"], "type": "paragraph", "paragraph": {"rich_text": [{"plain_text": block["text"]}]}} for block in self.pages[page_id]["blocks"]]}

    def update_block(self, block_id, properties):
        for page in self.pages.values():
            for block in page["blocks"]:
                if block["id"] == block_id:
                    block["text"] = properties["paragraph"]["rich_text"][0]["text"]["content"]
                    return {"id": block_id}
        raise KeyError(block_id)

    def append_children(self, page_id, children):
        page = self.pages[page_id]
        page["blocks"].extend({"id": f"append-{len(page['blocks'])}-{i}", "text": next(iter(block[block["type"]]["rich_text"]))["text"]["content"]} for i, block in enumerate(children))
        return {"results": []}


def test_production_notion_provider_runs_project_record_projection_conflict_and_restart_idempotency():
    client = FakeNotionClient()
    provider = NotionApiProvider(client)
    service = NotionLifecycleService(provider)
    assert service.configure("project-a", "env/myassistant/notion-readonly")["status"] == "CONNECTED"
    created = service.create_project_record("project-a", "sandbox-parent", "Qualification A")
    assert created["status"] == "BOUND"
    page_id = created["page_id"]
    provider.append_text(page_id, "USER INTRODUCTION\nUSER NOTES\nUSER CHECKLIST")
    synced = service.document("project-a", {"CURRENT_STATUS": "ONLINE", "PROGRESS": "75%"}, "source-b", source_rank=2)
    assert synced["status"] == "SYNCED"
    page_text = "\n".join(block["text"] for block in client.pages[page_id]["blocks"])
    assert "USER INTRODUCTION" in page_text and "USER NOTES" in page_text and "ONLINE" in page_text

    current = client.pages[page_id]["blocks"]
    current[6]["text"] = "operator changed managed status"
    conflict = service.document("project-a", {"CURRENT_STATUS": "OFFLINE"}, "source-c", source_rank=3)
    assert conflict["status"] == "CONFLICT"
    assert "OFFLINE" not in "\n".join(block["text"] for block in current)

    # A fresh adapter instance can discover its prior page by the bounded
    # internal marker instead of creating a duplicate Project Record.
    restarted = NotionLifecycleService(NotionApiProvider(client))
    restarted.configure("project-b", "env/myassistant/notion-readonly")
    rebound = restarted.create_project_record("project-b", "sandbox-parent", "Qualification A", idempotency_key="project-record/project-a")
    assert rebound["page_id"] == page_id
    assert len(client.pages) == 1


def test_production_provider_history_rollover_is_idempotent_and_redacts():
    client = FakeNotionClient()
    service = NotionLifecycleService(NotionApiProvider(client))
    service.configure("project-a", "env/myassistant/notion-readonly")
    page_id = service.create_project_record("project-a", "sandbox-parent", "Qualification A")["page_id"]
    history = service.rollover_history("project-a", "2026-08", "api_key=never-send", "a", "b")
    again = service.rollover_history("project-a", "2026-08", "other", "a", "b")
    assert history["history_page_id"] == again["history_page_id"]
    assert page_id in client.pages and "never-send" not in "\n".join(block["text"] for block in client.pages[history["history_page_id"]]["blocks"])


def test_provider_translation_rejects_ambiguous_managed_region():
    client = FakeNotionClient()
    provider = NotionApiProvider(client)
    page = provider.create_page("parent", "A", "<!-- PRIME_MANAGED_REGION:CURRENT_STATUS:START -->\nA\n<!-- PRIME_MANAGED_REGION:CURRENT_STATUS:END -->", "key")
    client.pages[page.page_id]["blocks"].insert(2, {"id": "extra", "text": "duplicate"})
    try:
        provider.update_region(page.page_id, "CURRENT_STATUS", hashlib.sha256(b"A").hexdigest(), "B", "write")
    except NotionProviderError as exc:
        assert exc.code == "CONFLICT"
    else:
        raise AssertionError("ambiguous managed region was accepted")

def test_idempotency_search_requires_exact_marker_not_relevance_match():
    client = FakeNotionClient()
    provider = NotionApiProvider(client)
    first = provider.create_page("parent", "A", "first", "key-a")
    second = provider.create_page("parent", "B", "second", "key-b")
    assert first.page_id != second.page_id
    assert len(client.pages) == 2
