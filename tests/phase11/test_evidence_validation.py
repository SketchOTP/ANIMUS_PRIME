from __future__ import annotations

import pytest

from src.prime_core.evidence_validation import validate_evidence


def test_evidence_rejects_active_content_and_accepts_bounded_data():
    assert validate_evidence(b"validation report", "UPLOAD")
    assert not validate_evidence(b"<script>alert(1)</script>", "UPLOAD")
    with pytest.raises(ValueError):
        validate_evidence(b"x", "UNKNOWN")


def test_evidence_size_is_bounded():
    with pytest.raises(ValueError):
        validate_evidence(b"x" * 10, "UPLOAD", max_bytes=4)
