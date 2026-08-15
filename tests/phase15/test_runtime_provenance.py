from src.prime_core.build_info import build_info


def test_build_info_exposes_non_secret_runtime_identity(monkeypatch):
    monkeypatch.setenv("PRIME_BUILD_COMMIT", "98b94732106955c246fca025f73116f56b58b5cf")
    monkeypatch.setenv("PRIME_BUILD_TIMESTAMP", "2026-08-15T00:00:00Z")
    monkeypatch.setenv("PRIME_IMAGE_IDENTITY", "animus-prime-core:test")
    monkeypatch.setenv("PRIME_SERVICE_VERSION", "1.0.0")

    result = build_info("0034_local_identity_authentication.sql")

    assert result == {
        "spec_revision": "PRIME-SPEC-V1.0.0",
        "build_commit": "98b94732106955c246fca025f73116f56b58b5cf",
        "build_timestamp": "2026-08-15T00:00:00Z",
        "image_identity": "animus-prime-core:test",
        "schema_version": "0034_local_identity_authentication.sql",
        "service_version": "1.0.0",
    }


def test_build_info_never_reads_checkout_git_state(monkeypatch):
    monkeypatch.delenv("PRIME_BUILD_COMMIT", raising=False)
    monkeypatch.setenv("PRIME_IMAGE_IDENTITY", "animus-prime-core:unknown")

    result = build_info("schema")

    assert result["build_commit"] == "UNKNOWN"
    assert result["image_identity"] == "animus-prime-core:unknown"
