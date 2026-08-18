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
