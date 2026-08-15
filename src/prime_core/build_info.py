from __future__ import annotations

import os
from typing import Any


SPEC_REVISION = "PRIME-SPEC-V1.0.0"


def build_info(schema_version: str | None) -> dict[str, Any]:
    """Return non-secret identity for the code baked into the running image."""
    return {
        "spec_revision": SPEC_REVISION,
        "build_commit": os.getenv("PRIME_BUILD_COMMIT", "UNKNOWN"),
        "build_timestamp": os.getenv("PRIME_BUILD_TIMESTAMP", "UNKNOWN"),
        "image_identity": os.getenv("PRIME_IMAGE_IDENTITY", "UNKNOWN"),
        "schema_version": schema_version or "UNKNOWN",
        "service_version": os.getenv("PRIME_SERVICE_VERSION", "UNKNOWN"),
    }
