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
            return {"review_id": review_id, "project_id": review["project_id"], "goal_revision_id": review["goal_revision_id"], "status": "APPROVED"}

    def assess(self, project_id: str, goal_revision_id: str, results: list[dict[str, Any]], repository_revision: str | None = None, summary: str = "", evidence_refs: list[str] | None = None) -> dict[str, Any]:
        with transaction(self.settings) as db:
            approved = db.execute("SELECT 1 FROM prime_core.progress_baseline_reviews WHERE project_id=%s AND goal_revision_id=%s AND status='APPROVED'", (project_id, goal_revision_id)).fetchone()
            if not approved:
                raise ValueError("progress baseline is pending")
            goal_items = db.execute(
                "SELECT title, weight, required, acceptance_expectations FROM prime_core.goal_items WHERE project_id=%s AND goal_revision_id=%s",
                (project_id, goal_revision_id),
            ).fetchall()
            refs = list(evidence_refs or [])
            by_title = {str(item.get("title", "")): item for item in results}
            weights = {str(item["title"]): float(item["weight"]) for item in goal_items}
            for goal_item in goal_items:
                expectations = goal_item["acceptance_expectations"]
                if isinstance(expectations, str):
                    expectations = json.loads(expectations)
                requires_evidence = bool(goal_item["required"]) and any("evidence" in str(expectation).lower() for expectation in (expectations or []))
                result = by_title.get(str(goal_item["title"])) or {}
                item_refs = result.get("evidence_refs") or []
                completion = float(result.get("completion", 0))
                if requires_evidence and completion > 0 and not (refs or item_refs):
                    raise ValueError(f"required evidence missing for goal item: {goal_item['title']}")
            total = sum(float(item.get("weight", weights.get(str(item.get("title", "")), 0))) * max(0.0, min(1.0, float(item.get("completion", 0)))) for item in results)
            confidence = sum(float(item.get("confidence", 0)) for item in results) / len(results) if results else 0.0
            assessment_id = _id("assessment")
            created = now()
            db.execute("INSERT INTO prime_core.progress_assessments(assessment_id,project_id,goal_revision_id,repository_revision,progress_percent,confidence,freshness_state,summary,item_results,evidence_refs,created_at) VALUES (%s,%s,%s,%s,%s,%s,'CURRENT',%s,%s,%s,%s)", (assessment_id, project_id, goal_revision_id, repository_revision, total * 100, confidence, summary, json.dumps(results), json.dumps(refs), created))
            record_historical_snapshot(db, project_id, "PROGRESS", assessment_id, repository_revision, {"assessment_id": assessment_id, "goal_revision_id": goal_revision_id, "repository_revision": repository_revision, "progress_percent": total * 100, "confidence": confidence, "summary": summary, "item_results": results}, created)
            return {"assessment_id": assessment_id, "project_id": project_id, "goal_revision_id": goal_revision_id, "progress_percent": total * 100, "confidence": confidence, "freshness_state": "CURRENT", "goal_items": results, "evidence_refs": refs}

    def snapshot(self, project_id: str) -> dict[str, Any]:
        """Return the durable GoalModel and explainable latest assessment."""
        with connect(self.settings) as db:
            goal = db.execute("SELECT goal_revision_id,revision_number,status,content_hash FROM prime_core.goal_revisions WHERE project_id=%s AND status='APPROVED' ORDER BY revision_number DESC LIMIT 1", (project_id,)).fetchone()
            items = db.execute("SELECT goal_item_id,goal_revision_id,title,description,weight,required,acceptance_expectations FROM prime_core.goal_items WHERE project_id=%s ORDER BY goal_item_id", (project_id,)).fetchall()
            assessment = db.execute("SELECT assessment_id,goal_revision_id,repository_revision,progress_percent,confidence,freshness_state,summary,item_results,evidence_refs,created_at FROM prime_core.progress_assessments WHERE project_id=%s ORDER BY created_at DESC LIMIT 1", (project_id,)).fetchone()
        parsed_items = [dict(row) for row in items]
        for item in parsed_items:
            if isinstance(item.get("acceptance_expectations"), str):
                item["acceptance_expectations"] = json.loads(item["acceptance_expectations"])
        result = dict(assessment) if assessment else None
        if result:
            for key in ("item_results", "evidence_refs"):
                if isinstance(result.get(key), str):
                    result[key] = json.loads(result[key])
            if hasattr(result.get("created_at"), "isoformat"):
                result["created_at"] = result["created_at"].isoformat()
        return {
            "project_id": project_id,
            "goal_model": {"goal_revision": dict(goal) if goal else None, "items": parsed_items, "status": "APPROVED" if goal and parsed_items else "AWAITING_BASELINE"},
            "assessment": result,
            "explanation": result.get("summary") if result else "UNKNOWN: no evidence-backed assessment exists.",
        }
