from __future__ import annotations

import pytest

from src.prime_core.evidence_validation import validate_evidence, validate_filename, validate_mime_type, validate_privacy_class


def test_evidence_rejects_active_content_and_accepts_bounded_data():
    assert validate_evidence(b"validation report", "UPLOAD")
    assert not validate_evidence(b"<script>alert(1)</script>", "UPLOAD")
    with pytest.raises(ValueError):
        validate_evidence(b"x", "UNKNOWN")


def test_evidence_size_is_bounded():
    with pytest.raises(ValueError):
        validate_evidence(b"x" * 10, "UPLOAD", max_bytes=4)


def test_evidence_metadata_accepts_safe_values_and_rejects_active_or_unknown_values():
    assert validate_filename("report.pdf")
    assert not validate_filename("../report.pdf")
    assert validate_mime_type("application/pdf")
    assert not validate_mime_type("text/html")
    assert validate_privacy_class("PROJECT_PRIVATE")
    assert not validate_privacy_class("CROSS_PROJECT")
