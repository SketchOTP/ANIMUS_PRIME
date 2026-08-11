from __future__ import annotations


def reconstruction_status(statuses: dict[str, str]) -> str:
    """Combine per-source historical coverage without inventing missing state."""
    values = list(statuses.values())
    if not values or all(value == "UNAVAILABLE" for value in values):
        return "UNAVAILABLE"
    if all(value == "EXACT" for value in values):
        return "EXACT"
    return "PARTIAL"
