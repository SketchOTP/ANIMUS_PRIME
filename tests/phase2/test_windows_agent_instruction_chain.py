from contextlib import contextmanager

from prime_core.service import CoreService
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
