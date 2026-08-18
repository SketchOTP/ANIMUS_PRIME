from __future__ import annotations

import json

from src.prime_core.node_client import NodeClient, NodeClientSettings


class Response:
    def __init__(self, payload):
        self.payload = json.dumps(payload).encode()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return self.payload


def test_core_node_client_sends_identity_and_protocol_headers():
    seen = {}

    def opener(request, timeout, context):
        seen["headers"] = dict(request.headers)
        seen["context"] = context
        return Response({"status": "ONLINE"})

    client = NodeClient(NodeClientSettings("https://node.private", "node-1", "credential"), opener=opener)
    assert client.heartbeat()["status"] == "ONLINE"
    assert seen["headers"]["X-prime-node-id"] == "node-1"
    assert seen["headers"]["X-prime-protocol"] == "node-control-v1"
    assert seen["context"].check_hostname


def test_core_node_client_delegates_repository_creation():
    seen = {}

    def opener(request, timeout, context):
        seen["url"] = request.full_url
        seen["body"] = json.loads(request.data)
        return Response({"canonical_path": "/srv/prime-projects/example", "created": True})

    client = NodeClient(NodeClientSettings("https://node.private", "node-1", "credential"), opener=opener)
    result = client.create_repository("/srv/prime-projects", "example", "workflow-1")
    assert result["created"] is True
    assert seen == {
        "url": "https://node.private/v1/repositories/create",
        "body": {
            "parent_path": "/srv/prime-projects",
            "repository_name": "example",
            "operation_id": "workflow-1",
        },
    }


def test_core_node_client_delegates_authority_and_goal_writes():
    seen = []

    def opener(request, timeout, context):
        seen.append((request.full_url, json.loads(request.data)))
        return Response({"written": True})

    client = NodeClient(NodeClientSettings("https://node.private", "node-1", "credential"), opener=opener)
    assert client.bootstrap_authority("/repo", {"AGENTS.md": "rules"}, "authority-1")["written"] is True
    assert client.write_project_goal("/repo", "goal", "a" * 64)["written"] is True
    assert seen == [
        (
            "https://node.private/v1/repositories/authority/bootstrap",
            {"repository_path": "/repo", "files": {"AGENTS.md": "rules"}, "operation_id": "authority-1"},
        ),
        (
            "https://node.private/v1/repositories/goal",
            {"repository_path": "/repo", "content": "goal", "content_hash": "a" * 64},
        ),
    ]
