from __future__ import annotations

from src.prime_core.config import Settings
from src.prime_core.memory_service import MemoryService


def test_memory_service_uses_approved_settings_endpoint(monkeypatch):
    monkeypatch.delenv("PRIME_HINDSIGHT_BASE_URL", raising=False)
    monkeypatch.delenv("PRIME_HINDSIGHT_TIMEOUT_SECONDS", raising=False)
    settings = Settings()
    assert settings.hindsight_base_url == "http://127.0.0.1:8888"
    assert settings.hindsight_timeout_seconds == 30.0
    adapter = MemoryService(settings).adapter_factory("project-config")
    assert adapter.base_url == settings.hindsight_base_url
    assert adapter.timeout_seconds == settings.hindsight_timeout_seconds


def test_memory_endpoint_can_be_configured_without_secret_material(monkeypatch):
    monkeypatch.setenv("PRIME_HINDSIGHT_BASE_URL", "http://hindsight.internal:8888/")
    monkeypatch.setenv("PRIME_HINDSIGHT_TIMEOUT_SECONDS", "45")
    settings = Settings()
    assert settings.hindsight_base_url == "http://hindsight.internal:8888"
    assert settings.hindsight_timeout_seconds == 45.0