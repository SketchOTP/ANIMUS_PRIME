from pathlib import Path


ROOT = Path(__file__).parents[2]


def test_local_identity_runtime_contract_is_separate_from_recovery():
    migration = (ROOT / "migrations/prime/0034_local_identity_authentication.sql").read_text()
    script = (ROOT / "packaging/core/prime-local-auth").read_text()
    assert "local_identity_hash" in migration
    assert "auth_challenges" in migration
    assert "local-identity.secret" in script
    assert "local-recovery.secret" in script
    assert "X-PRIME-Local-Identity" in script
    assert "approval_code" in script
    service = (ROOT / "src/prime_core/service.py").read_text()
    assert "local_recovery_hash" in service
    assert "local_identity_hash" in service


def test_local_identity_browser_contract_preserves_ordinary_session_and_step_up():
    core = (ROOT / "apps/core/main.py").read_text()
    service = (ROOT / "src/prime_core/service.py").read_text()
    web = (ROOT / "apps/web/index.html").read_text()
    assert "/v1/auth/local-identity/challenge" in core
    assert "/v1/auth/local-identity/approve" in core
    assert "/v1/auth/local-identity/redeem" in core
    assert 'metadata={"auth_method": "LOCAL_IDENTITY"' in service
    assert "set_auth_cookies(response" in core
    assert "prime_local_identity_nonce" in core
    assert "prime-local-auth approve" in web
    assert "STEP_UP" in web
