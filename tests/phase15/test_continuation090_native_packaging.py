from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_linux_node_installer_grants_only_service_identity_required_access():
    installer = (ROOT / "packaging/node/install-node.sh").read_text(encoding="utf-8")

    assert "id -u prime-node" in installer
    assert "getent group prime-node" in installer
    assert 'install -d -o root -g prime-node -m 0750 "$PREFIX"' in installer
    assert 'install -d -o prime-node -g prime-node -m 0750 "$DATA"' in installer
    assert 'install -d -o root -g root -m 0750 /etc/animus-prime' in installer
    assert 'readwrite_paths="$DATA"' in installer
    assert 'readwrite_paths+=" $root"' in installer
    assert "configured allowed root does not exist" in installer


def test_remote_repository_creation_reconciles_only_through_node_idempotency():
    service = (ROOT / "src/prime_core/service.py").read_text(encoding="utf-8")

    assert "NODE_IDEMPOTENCY_CONFIRMED" in service
    assert 'create_repository(str(parent), repository_name, workflow["workflow_id"])' in service
    assert "ambiguous_external_effect=False" in service


def test_core_image_contains_the_frozen_authority_template():
    dockerfile = (ROOT / "Dockerfile.core").read_text(encoding="utf-8")

    assert "COPY authority-template ./authority-template" in dockerfile
