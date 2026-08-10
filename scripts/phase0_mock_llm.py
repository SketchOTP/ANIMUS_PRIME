#!/usr/bin/env python3
"""Deterministic OpenAI-compatible fixture for local Hindsight qualification."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:  # noqa: N802 - stdlib hook
        length = int(self.headers.get("content-length", "0"))
        request = json.loads(self.rfile.read(length) or b"{}")
        messages = request.get("messages", [])
        prompt = "\n".join(str(item.get("content", "")) for item in messages)
        if "Extract facts" in prompt or "extract facts" in prompt:
            content = json.dumps(
                {
                    "facts": [
                        {
                            "what": "Phase 0 adapter smoke fact was retained.",
                            "when": "N/A",
                            "where": "N/A",
                            "who": "ANIMUS PRIME",
                            "why": "It verifies the Hindsight compatibility path.",
                            "fact_kind": "conversation",
                            "fact_type": "world",
                            "entities": [],
                        }
                    ]
                }
            )
        else:
            content = json.dumps({"text": "Phase 0 qualification fixture response."})
        response = {
            "id": "phase0-mock",
            "object": "chat.completion",
            "created": 0,
            "model": request.get("model", "phase0-mock"),
            "choices": [{"index": 0, "message": {"role": "assistant", "content": content}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2},
        }
        encoded = json.dumps(response).encode()
        self.send_response(200)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, format: str, *args: object) -> None:
        return


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 18080), Handler).serve_forever()
