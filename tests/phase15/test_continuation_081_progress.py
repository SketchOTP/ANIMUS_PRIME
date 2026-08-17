from pathlib import Path


def test_progress_refresh_uses_live_canonical_repository_revision():
    source = (Path(__file__).parents[2] / "apps" / "core" / "main.py").read_text()
    route = source.split("def refresh_project_progress", 1)[1].split("@app.post", 1)[0]

    assert "git_state = _git_state(project_id)" in route
    assert 'revision = git_state.get("canonical_revision")' in route
    assert 'revision = _git(root, "rev-parse", "HEAD")' not in route


def test_progress_refresh_links_open_correction_to_reassessment():
    source = (Path(__file__).parents[2] / "src" / "prime_core" / "progress_service.py").read_text()
    refresh = source.split("    def refresh(", 1)[1].split("    def challenge(", 1)[0]

    assert "status='OPEN'" in refresh
    assert "reassessment_id=%s,status='REASSESSED'" in refresh
    assert 'result["correction_id"] = correction["correction_id"]' in refresh
