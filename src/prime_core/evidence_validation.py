from __future__ import annotations


def validate_evidence(content: bytes, source_type: str, max_bytes: int = 50 * 1024 * 1024) -> bool:
    if source_type not in {"UPLOAD", "NODE_PATH", "EXTERNAL_REFERENCE"}:
        raise ValueError("unsupported Evidence source type")
    if len(content) > max_bytes:
        raise ValueError("Evidence exceeds the configured size limit")
    if source_type == "EXTERNAL_REFERENCE":
        return True
    # Evidence is data. Never execute or parse active script content.
    lowered = content[:4096].lower()
    if b"<script" in lowered or b"javascript:" in lowered:
        return False
    if b"\x00" in content and content[:4] not in {b"%PDF", b"\x89PNG", b"\xff\xd8\xff\xe0", b"\xff\xd8\xff\xe1"}:
        return False
    return True
