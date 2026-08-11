from __future__ import annotations

import json
from decimal import Decimal
from typing import Any

from .db import connect, transaction
from .service import _id, now
from .history_primitives import record_historical_snapshot


class ProgressService:
    def __init__(self, settings: Any):
        self.settings = settings

    def propose_baseline(self, project_id: str, goal_revision_id: str, items: list[dict[str, Any]]) -> dict[str, Any]:
        if not items or any(float(item.get("weight", 0)) <= 0 for item in items):
            raise ValueError("goal items require positive weights")
        weights = sum(float(item["weight"]) for item in items)
        if abs(weights - 1.0) > 1e-6:
            raise ValueError("goal item weights must sum to 1.0")
        with transaction(self.settings) as db:
            if not db.execute("SELECT 1 FROM prime_core.goal_revisions WHERE project_id=%s AND goal_revision_id=%s AND status='APPROVED'", (project_id, goal_revision_id)).fetchone():
                raise ValueError("baseline requires an approved goal revision")
            review_id = _id("baseline")
            db.execute("INSERT INTO prime_core.progress_baseline_reviews(review_id,project_id,goal_revision_id,items,weights_sum,status,created_at) VALUES (%s,%s,%s,%s,%s,'PENDING',%s)", (review_id, project_id, goal_revision_id, json.dumps(items), weights, now()))
            return {"review_id": review_id, "status": "PENDING", "items": items, "weights_sum": weights}

    def approve_baseline(self, review_id: str) -> dict[str, Any]:
        with transaction(self.settings) as db:
            review = db.execute("SELECT * FROM prime_core.progress_baseline_reviews WHERE review_id=%s FOR UPDATE", (review_id,)).fetchone()
            if not review:
                raise KeyError("baseline review not found")
            items = review["items"] if isinstance(review["items"], list) else json.loads(review["items"])
            db.execute("UPDATE prime_core.progress_baseline_reviews SET status='APPROVED',approved_at=now() WHERE review_id=%s", (review_id,))
            for item in items:
                db.execute("INSERT INTO prime_core.goal_items(goal_item_id,project_id,goal_revision_id,title,description,weight,required,acceptance_expectations) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING", (_id("goalitem"), review["project_id"], review["goal_revision_id"], item["title"], item.get("description", item["title"]), item["weight"], item.get("required", True), json.dumps(item.get("acceptance_expectations", []))))
            return {"review_id": review_id, "status": "APPROVED"}

    def assess(self, project_id: str, goal_revision_id: str, results: list[dict[str, Any]], repository_revision: str | None = None, summary: str = "") -> dict[str, Any]:
        with transaction(self.settings) as db:
            approved = db.execute("SELECT 1 FROM prime_core.progress_baseline_reviews WHERE project_id=%s AND goal_revision_id=%s AND status='APPROVED'", (project_id, goal_revision_id)).fetchone()
            if not approved:
                raise ValueError("progress baseline is pending")
            total = sum(float(item.get("weight", 0)) * max(0.0, min(1.0, float(item.get("completion", 0)))) for item in results)
            confidence = sum(float(item.get("confidence", 0)) for item in results) / len(results) if results else 0.0
            assessment_id = _id("assessment")
            created = now()
            db.execute("INSERT INTO prime_core.progress_assessments(assessment_id,project_id,goal_revision_id,repository_revision,progress_percent,confidence,freshness_state,summary,item_results,created_at) VALUES (%s,%s,%s,%s,%s,%s,'CURRENT',%s,%s,%s)", (assessment_id, project_id, goal_revision_id, repository_revision, total * 100, confidence, summary, json.dumps(results), created))
            record_historical_snapshot(db, project_id, "PROGRESS", assessment_id, repository_revision, {"assessment_id": assessment_id, "goal_revision_id": goal_revision_id, "repository_revision": repository_revision, "progress_percent": total * 100, "confidence": confidence, "summary": summary, "item_results": results}, created)
            return {"assessment_id": assessment_id, "project_id": project_id, "goal_revision_id": goal_revision_id, "progress_percent": total * 100, "confidence": confidence, "freshness_state": "CURRENT", "goal_items": results}
