from __future__ import annotations

import io
import json
import urllib.error

import pytest

from src.prime_core.notion_api import NotionApiClient, NotionApiError, NotionApiSettings


class Response:
    def __init__(self, payload):
        self.payload = json.dumps(payload).encode()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return self.payload


def test_notion_client_sends_current_version_and_bounded_children():
    seen = {}

    def opener(request, timeout):
        seen.update({"headers": dict(request.headers), "timeout": timeout, "body": json.loads(request.data)})
        return Response({"id": "page-1"})

    client = NotionApiClient(NotionApiSettings("token-not-logged"), opener=opener)
    assert client.create_page({"page_id": "parent"}, {"title": {"title": []}}, [{"object": "block"}])["id"] == "page-1"
    assert seen["headers"]["Notion-version"] == "2026-03-11"
    assert seen["timeout"] == 15


def test_notion_client_retries_rate_limit_then_succeeds():
    attempts = {"count": 0}

    def opener(request, timeout):
        attempts["count"] += 1
        if attempts["count"] == 1:
            raise urllib.error.HTTPError(request.full_url, 429, "slow", {"Retry-After": "0.1"}, io.BytesIO(b"{}"))
        return Response({"results": []})

    slept = []
    client = NotionApiClient(NotionApiSettings("token"), opener=opener, sleeper=slept.append)
    assert client.retrieve_children("block")["results"] == []
    assert attempts["count"] == 2 and slept


def test_notion_client_does_not_retry_permission_failures():
    def opener(request, timeout):
        raise urllib.error.HTTPError(request.full_url, 403, "forbidden", {}, io.BytesIO(b"{}"))

    with pytest.raises(NotionApiError) as error:
        NotionApiClient(NotionApiSettings("token"), opener=opener).retrieve_page("page")
    assert error.value.status == 403 and not error.value.retryable


def test_capability_test_distinguishes_read_and_explicit_write_probe():
    paths = []

    def opener(request, timeout):
        paths.append(request.full_url)
        if request.full_url.endswith("/users/me"):
            return Response({"id": "actor-1", "workspace_id": "workspace-1"})
        if "/pages/approved" in request.full_url:
            return Response({"id": "approved"})
        if "/blocks/approved/children" in request.full_url:
            return Response({"results": []})
        if request.full_url.endswith("/pages"):
            return Response({"id": "probe-page"})
        raise AssertionError(request.full_url)

    client = NotionApiClient(NotionApiSettings("token"), opener=opener)
    read = client.capability_test("approved")
    assert read["page_read"] is True and read["block_read"] is True
    assert read["page_write"] == "NOT_TESTED"
    write = client.capability_test("approved", write_probe=True, probe_parent_id="approved")
    assert write["page_write"] is True and write["managed_write"] == "CAPABILITY_PRESENT"
    assert all("token" not in path for path in paths)
