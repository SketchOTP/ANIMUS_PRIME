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


def test_remote_repository_reads_do_not_resolve_the_node_path_on_core():
    app = (ROOT / "apps/core/main.py").read_text(encoding="utf-8")
    tree = app[app.index("def repository_tree("):app.index("def repository_file(")]
    file_view = app[app.index("def repository_file("):app.index("def authority_view(")]
    git_state = app[app.index("def _git_state("):app.index("def _context_markdown(")]

    assert tree.index("node_client_for_project") < tree.index("_safe_repository_path")
    assert file_view.index("node_client_for_project") < file_view.index("_safe_repository_path")
    assert git_state.index("node_client_for_project") < git_state.index("_safe_repository_path")
    assert '".." in relative.parts' in app


def test_remote_agent_chain_uses_bounded_node_reads():
    service = (ROOT / "src/prime_core/service.py").read_text(encoding="utf-8")
    chain = service[service.index("def agent_instruction_chain("):service.index("def _safe_archive_extract(")]

    assert chain.index("node_client_for_project") < chain.index("Path(row")
    assert "client.list_directory" in chain
    assert "client.read_file" in chain
    assert '"source": "LIVE_NODE"' in chain


def test_continuity_backup_omits_installation_local_capability_rows():
    backup = (ROOT / "src/prime_core/backup_service.py").read_text(encoding="utf-8")

    for table in (
        "operators",
        "sessions",
        "auth_challenges",
        "lifecycle_preflights",
        "mcp_grants",
        "node_enrollment_challenges",
        "repository_rebind_preflights",
    ):
        assert f'"{table}"' in backup
    assert "Reissue them after restore" in backup


def test_warm_start_reads_remote_authority_through_the_enrolled_node():
    source = (ROOT / "src/prime_core/warm_start_service.py").read_text(encoding="utf-8")

    assert "node_client_for_project" in source
    assert "client.repository_snapshot" in source
    assert "client.read_file" in source
    assert source.index("node_client_for_project") < source.index("self._root(project_id)")
