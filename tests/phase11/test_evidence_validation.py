from __future__ import annotations

import pytest

from src.prime_core.evidence_validation import (
    safe_parser_result,
    sniff_mime_type,
    validate_evidence,
    validate_filename,
    validate_mime_consistency,
    validate_mime_type,
    validate_privacy_class,
)


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


def test_evidence_parser_is_inert_bounded_and_truthful(monkeypatch):
    assert sniff_mime_type(b"hello", "note.txt") == "text/plain"
    assert validate_mime_consistency(b"hello", "note.txt", "text/plain")
    assert not validate_mime_consistency(b"<html><script>x</script>", "note.txt", "text/plain")
    assert safe_parser_result(b"hello", "text/plain") == ("INDEXED", "hello", None)
    monkeypatch.setenv("PRIME_EVIDENCE_PARSER_AVAILABLE", "0")
    assert safe_parser_result(b"hello", "text/plain")[0] == "UNSUPPORTED"
    monkeypatch.setenv("PRIME_EVIDENCE_PARSER_AVAILABLE", "1")
    assert safe_parser_result(b"#!/bin/sh\necho unsafe", "text/plain")[0] == "FAILED"
    assert safe_parser_result(b"api_key=do-not-index", "text/plain")[0] == "FAILED"
