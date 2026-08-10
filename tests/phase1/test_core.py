from __future__ import annotations

import os

import pytest
from fastapi.testclient import TestClient


pytestmark = pytest.mark.skipif(
    not os.getenv("PRIME_PHASE1_DB_URL"), reason="set PRIME_PHASE1_DB_URL for PostgreSQL integration tests"
)


@pytest.fixture()
def client(monkeypatch):
    monkeypatch.setenv("PRIME_DATABASE_URL", os.environ["PRIME_PHASE1_DB_URL"])
    from apps.core import main
    main.settings = main.Settings()
    main.service = main.CoreService(main.settings)
    with TestClient(main.app) as test_client:
        yield test_client


def test_bootstrap_login_csrf_and_recovery(client):
    password = "phase1 operator password"
    boot = client.post("/v1/auth/bootstrap", json={"password": password})
    assert boot.status_code == 200
    recovery = boot.json()["recovery_credential"]
    login = client.post("/v1/auth/login", json={"password": password}, headers={"Origin": "http://localhost:8000"})
    assert login.status_code == 200
    assert client.get("/v1/core/status").status_code == 200
    assert client.post("/v1/events", json={"event_type": "test"}).status_code == 403
    csrf = login.json()["csrf_token"]
    event = client.post("/v1/events", json={"event_type": "test", "dedupe_key": "phase1-test"}, headers={"X-PRIME-CSRF": csrf})
    assert event.status_code == 200
    duplicate = client.post("/v1/events", json={"event_type": "test", "dedupe_key": "phase1-test"}, headers={"X-PRIME-CSRF": csrf})
    assert duplicate.json()["event_id"] == event.json()["event_id"]
    reset = client.post("/v1/auth/recover", json={"recovery_credential": recovery, "new_password": "new phase1 password"})
    assert reset.status_code == 200
    assert client.get("/v1/core/status").status_code == 401


def test_job_idempotency_and_claim_completion(client):
    client.post("/v1/auth/login", json={"password": "new phase1 password"})
    csrf = client.cookies.get("prime_csrf")
    headers = {"X-PRIME-CSRF": csrf}
    first = client.post("/v1/jobs", json={"job_type": "qualification", "idempotency_key": "job-1"}, headers=headers)
    second = client.post("/v1/jobs", json={"job_type": "qualification", "idempotency_key": "job-1"}, headers=headers)
    assert first.json()["job_id"] == second.json()["job_id"]


def test_project_workflow_and_security_headers(client):
    client.post("/v1/auth/login", json={"password": "new phase1 password"})
    csrf = client.cookies.get("prime_csrf")
    headers = {"X-PRIME-CSRF": csrf}
    project = client.post("/v1/projects", json={"name": "Qualification Project"}, headers=headers)
    assert project.status_code == 200
    assert project.json()["lifecycle_state"] == "DRAFT"
    workflow = client.post(
        "/v1/workflows",
        json={"workflow_type": "bootstrap", "idempotency_key": "workflow-1", "project_id": project.json()["project_id"]},
        headers=headers,
    )
    assert workflow.status_code == 200
    assert workflow.json()["status"] == "RUNNING"
    rejected = client.post("/v1/projects", json={"name": "bad origin"}, headers={"Origin": "https://evil.example", **headers})
    assert rejected.status_code == 403
    assert rejected.headers["cache-control"] == "no-store"
