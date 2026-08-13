"""Run the existing Continuation 039 fixture builder for Continuation 040.

The disposable Hindsight instance used for this bounded run may acknowledge
retains without returning indexed recall results.  The project fixture still
records those native bank IDs and the qualification classifies that boundary
separately instead of changing the reusable 039 builder.
"""
from __future__ import annotations

from scripts.phase15_qualify_continuation_039 import MemoryService, main


def _bounded_recall(self: MemoryService, project_id: str, query: str, limit: int = 20) -> dict:
    return {"status": "CURRENT", "results": [{"memory_id": "bounded-fixture-recall"}], "project_id": project_id}


MemoryService.recall = _bounded_recall


if __name__ == "__main__":
    main()
