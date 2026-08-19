from contextlib import contextmanager

from prime_core.service import CoreService
from prime_core.indexer import RepositoryIndexer
from prime_core.intelligence_service import IntelligenceService
from apps.core.main import _remote_repository_path


class _Result:
    def fetchone(self):
        return {"canonical_path": r"C:\PRIME-V1-Qualification\WindowsRepos\project"}


class _Database:
    def execute(self, *_args, **_kwargs):
        return _Result()


class _WindowsNodeClient:
    def list_directory(self, path):
        assert path == r"C:\PRIME-V1-Qualification\WindowsRepos\project"
        return {
            "entries": [
                {
                    "name": "AGENTS.md",
                    "kind": "file",
                    "path": rf"{path}\AGENTS.md",
                }
            ]
        }

    def read_file(self, path):
        assert path.endswith(r"\AGENTS.md")
        return {"content_hash": "windows-agent-hash"}


def test_live_windows_node_agent_chain_uses_windows_path_semantics(monkeypatch):
    @contextmanager
    def fake_connect(_settings):
        yield _Database()

    service = CoreService.__new__(CoreService)
    service.settings = object()
    monkeypatch.setattr("prime_core.service.connect", fake_connect)
    monkeypatch.setattr(
        service,
        "node_client_for_project",
        lambda _project_id: ({"node_id": "node-windows"}, _WindowsNodeClient()),
    )

    result = service.agent_instruction_chain("project-windows")

    assert result["source"] == "LIVE_NODE"
    assert result["target"] == "."
    assert result["instructions"] == [
        {
            "path": "AGENTS.md",
            "scope": ".",
            "content_hash": "windows-agent-hash",
        }
    ]


def test_remote_windows_repository_path_preserves_node_path_semantics():
    binding = {
        "canonical_path": r"C:\PRIME-V1-Qualification\WindowsRepos\project"
    }

    candidate, normalized = _remote_repository_path(binding, ".agent/PROJECT_GOAL.md")

    assert candidate == (
        r"C:\PRIME-V1-Qualification\WindowsRepos\project\.agent\PROJECT_GOAL.md"
    )
    assert normalized == ".agent/PROJECT_GOAL.md"


def test_remote_windows_index_walks_node_tree_without_local_path_resolution():
    class Client:
        def list_directory(self, path):
            if path.endswith("project"):
                return {
                    "entries": [
                        {"name": ".agent", "kind": "directory", "path": rf"{path}\.agent"},
                        {"name": "AGENTS.md", "kind": "file", "path": rf"{path}\AGENTS.md"},
                    ]
                }
            return {
                "entries": [
                    {"name": "PROJECT_GOAL.md", "kind": "file", "path": rf"{path}\PROJECT_GOAL.md"}
                ]
            }

        def read_file(self, path):
            return {"content": f"content from {path}"}

    indexer = RepositoryIndexer(object())

    files = list(
        indexer._remote_files(
            Client(), r"C:\PRIME-V1-Qualification\WindowsRepos\project"
        )
    )

    assert [item[0] for item in files] == ["AGENTS.md", ".agent/PROJECT_GOAL.md"]


def test_remote_git_snapshot_is_searchable_without_resolving_windows_path_locally():
    rows = IntelligenceService._search_remote_git_snapshot(
        {"head": "2ccf8a2b3addd63b472722936130765e0117193c", "branch": "main"},
        "2ccf8a2",
    )

    assert rows[0]["commit_id"] == "2ccf8a2b3addd63b472722936130765e0117193c"
    assert rows[0]["canonical_ref"] == "main"
    assert IntelligenceService._search_remote_git_snapshot(
        {"head": rows[0]["commit_id"], "branch": "main"}, "nonsense"
    ) == []
