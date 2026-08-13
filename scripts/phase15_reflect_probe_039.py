"""Bounded native-Hindsight reflect probe for Continuation 039 evidence."""

from __future__ import annotations

import json
import os
import time

from src.prime_memory_adapter import PrimeMemoryAdapter


def main() -> None:
    project_id = os.environ["PRIME039_PROJECT_ID"]
    adapter = PrimeMemoryAdapter(
        os.environ.get("PRIME_HINDSIGHT_BASE_URL", "http://host.docker.internal:18888"),
        project_id,
        30,
    )
    started = time.monotonic()
    result = adapter.reflect(os.environ.get("PRIME039_QUERY", "What is the current marker?"))
    print(
        json.dumps(
            {
                "status": result.status,
                "reason": result.reason,
                "elapsed_seconds": round(time.monotonic() - started, 2),
                "payload_keys": sorted(result.payload) if isinstance(result.payload, dict) else [],
            }
        )
    )


if __name__ == "__main__":
    main()
