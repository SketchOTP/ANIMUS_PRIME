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
