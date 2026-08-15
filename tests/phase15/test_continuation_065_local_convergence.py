import pytest

from src.prime_core import service as service_module
from src.prime_core.service import CoreService
from src.prime_core.config import Settings


def test_approved_goal_protection_precedes_legacy_content_validation(monkeypatch):
    class FakeDB:
        def __init__(self):
            self.calls = 0

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def execute(self, *_args):
            self.calls += 1
            return self

        def fetchone(self):
            return {"goal_revision_id": "approved"} if self.calls == 1 else None

    db = FakeDB()

    def unexpected_validation(_content):
        raise AssertionError("legacy approved Goal content must not be revalidated before protection")

    monkeypatch.setattr(service_module, "connect", lambda _settings: db)
    monkeypatch.setattr(CoreService, "validate_goal_content", staticmethod(unexpected_validation))

    with pytest.raises(ValueError, match="approved GoalRevision is protected"):
        CoreService(Settings()).create_goal_revision(
            "project-065",
            "legacy governed Goal content",
            approve=True,
            new_revision=False,
        )

    assert db.calls == 2
