from __future__ import annotations

import ipaddress
import re
from pathlib import Path
from urllib.parse import urlparse


SUPPORTED_PRIVACY_CLASSES = {"PROJECT_PRIVATE", "SENSITIVE", "PUBLIC"}
SUPPORTED_MIME_TYPES = {
    "application/json",
    "application/pdf",
    "application/octet-stream",
    "text/csv",
    "text/markdown",
    "text/plain",
    "text/tab-separated-values",
    "image/jpeg",
    "image/png",
    "image/webp",
    "video/mp4",
    "audio/mpeg",
}
TEXT_MIME_TYPES = {"application/json", "text/csv", "text/markdown", "text/plain", "text/tab-separated-values"}


def validate_filename(filename: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", filename))


def validate_mime_type(mime_type: str) -> bool:
    return mime_type.strip().lower() in SUPPORTED_MIME_TYPES


def validate_privacy_class(privacy_class: str) -> bool:
    return privacy_class in SUPPORTED_PRIVACY_CLASSES


def validate_external_locator(locator: str) -> bool:
    """Accept only HTTPS references that do not target local/private networks.

    DNS resolution is intentionally deferred to the provider fetcher, which must
    re-check every redirect and resolved address immediately before connecting.
    """
    try:
        parsed = urlparse(locator)
        if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
            return False
        hostname = parsed.hostname.rstrip(".").lower()
        if hostname in {"localhost", "localhost.localdomain"}:
            return False
        try:
            address = ipaddress.ip_address(hostname)
        except ValueError:
            return True
        return not (address.is_private or address.is_loopback or address.is_link_local or address.is_multicast or address.is_reserved)
    except ValueError:
        return False


def validate_node_locator(locator: str, approved_roots: list[str] | tuple[str, ...]) -> bool:
    """Ensure a Node-path Evidence reference stays inside an approved root."""
    path = Path(locator)
    if not path.is_absolute():
        return False
    candidate = path.resolve(strict=False)
    for root in approved_roots:
        approved = Path(root).resolve(strict=False)
        if candidate == approved or approved in candidate.parents:
            return True
    return False


def validate_evidence(content: bytes, source_type: str, max_bytes: int = 50 * 1024 * 1024) -> bool:
    if source_type not in {"UPLOAD", "NODE_PATH", "EXTERNAL_REFERENCE"}:
        raise ValueError("unsupported Evidence source type")
    if len(content) > max_bytes:
        raise ValueError("Evidence exceeds the configured size limit")
    if source_type == "EXTERNAL_REFERENCE":
        return True
    # Evidence is data. Never execute or parse active script content.
    lowered = content[:4096].lower()
    if b"<script" in lowered or b"javascript:" in lowered or b"<?php" in lowered:
        return False
    if lowered.startswith((b"#!", b"mz")):
        return False
    if b"<svg" in lowered and (b"<script" in lowered or b"onload=" in lowered or b"href=" in lowered):
        return False
    if b"\x00" in content and content[:4] not in {b"%PDF", b"\x89PNG", b"\xff\xd8\xff\xe0", b"\xff\xd8\xff\xe1"}:
        return False
    return True


def extract_safe_text(content: bytes, mime_type: str, max_chars: int = 200_000) -> str | None:
    """Extract only bounded inert text; binary and active formats stay unindexed."""
    normalized = mime_type.strip().lower()
    if normalized not in TEXT_MIME_TYPES or not validate_evidence(content, "UPLOAD"):
        return None
    try:
        return content.decode("utf-8")[:max_chars]
    except UnicodeDecodeError:
        return None
