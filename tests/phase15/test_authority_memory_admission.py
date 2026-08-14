from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from src.prime_core.authority_memory_admission import AuthorityMemoryAdmission


class FakeHistory:
    def __init__(self) -> None:
        self.counter = 0

    def create_source_reference(self, project_id, source_class, locator, revision, content_hash, metadata):
        self.counter += 1
        return {"source_reference_id": f"source-{self.counter}"}


class FakeMemory:
    def __init__(self) -> None:
        self.calls = []

    def store(self, project_id, content, content_class, **kwargs):
        self.calls.append((project_id, content, content_class, kwargs))
        return {"status": "STORED", "memory_id": f"memory-{len(self.calls)}", "bank_id": f"prime-{project_id}"}


class FakeService:
    def __init__(self) -> None:
        self.settings = SimpleNamespace()
        self.events = []

    def emit_event(self, event_type, payload, **kwargs):
        self.events.append((event_type, payload, kwargs))
        return {"event_id": f"event-{len(self.events)}"}


def test_multi_record_admission_is_complete_and_idempotent(tmp_path: Path, monkeypatch):
    ledger = tmp_path / ".agent"
    ledger.mkdir()
    (ledger / "DIRECTIVES.md").write_text(
        "## A-044 - First consequential record\n\n"
        "This first consequential record contains enough evidence for admission.\n\n"
        "## B-044 - Second consequential record\n\n"
        "This second consequential record must not be lost before the next index.\n",
        encoding="utf-8",
    )
    service = FakeService()
    admission = AuthorityMemoryAdmission(service.settings, service)
    admission.history = FakeHistory()
    admission.memory = FakeMemory()
    monkeypatch.setattr(AuthorityMemoryAdmission, "_branch", staticmethod(lambda _root: "main"))
    monkeypatch.setattr(admission, "_source_reference", lambda *args, **kwargs: {"source_reference_id": "source-test"})
    existing = {"A-044": {"memory_id": "old-a", "content_hash": "old-hash"}}
    monkeypatch.setattr(admission, "_existing_admissions", lambda project_id, source_path: existing)

    first = admission.admit("project-a", tmp_path, "revision-a")
    assert [row["record_id"] for row in first["records"]] == ["A-044", "B-044"]
    assert [call[0] for call in admission.memory.calls] == ["project-a", "project-a"]
    assert admission.memory.calls[0][3]["supersedes_memory_id"] == "old-a"
    assert admission.memory.calls[1][3]["supersedes_memory_id"] is None
    assert all(call[3]["metadata"]["authority_source_path"] == ".agent/DIRECTIVES.md" for call in admission.memory.calls)
    assert all(call[3]["metadata"]["canonical_commit"] == "revision-a" for call in admission.memory.calls)

    existing.update({
        "B-044": {"memory_id": "memory-2", "content_hash": admission.memory.calls[1][3]["metadata"]["authority_source_hash"]},
        "A-044": {"memory_id": "memory-1", "content_hash": admission.memory.calls[0][3]["metadata"]["authority_source_hash"]},
    })
    second = admission.admit("project-a", tmp_path, "revision-a")
    assert len(admission.memory.calls) == 2
    assert second["status"] == "CURRENT"


def test_secret_authority_record_is_not_admitted(tmp_path: Path, monkeypatch):
    ledger = tmp_path / ".agent"
    ledger.mkdir()
    (ledger / "DIRECTIVES.md").write_text(
        "## A-044 - Consequential record\n\nThis is the existing admitted record with enough content.\n\n"
        "## B-044 - Sensitive record\n\nThis contains password: forbidden-value and must not be admitted.\n",
        encoding="utf-8",
    )
    service = FakeService()
    admission = AuthorityMemoryAdmission(service.settings, service)
    admission.history = FakeHistory()
    admission.memory = FakeMemory()
    monkeypatch.setattr(AuthorityMemoryAdmission, "_branch", staticmethod(lambda _root: "main"))
    monkeypatch.setattr(admission, "_source_reference", lambda *args, **kwargs: {"source_reference_id": "source-test"})
    monkeypatch.setattr(admission, "_existing_admissions", lambda project_id, source_path: {"A-044": {"memory_id": "old-a", "content_hash": "old-hash"}})

    result = admission.admit("project-a", tmp_path, "revision-a")
    sensitive = next(row for row in result["records"] if row["record_id"] == "B-044")
    assert sensitive["status"] == "REJECTED"
    assert admission.memory.calls == [] or all(call[1].find("password:") < 0 for call in admission.memory.calls)
