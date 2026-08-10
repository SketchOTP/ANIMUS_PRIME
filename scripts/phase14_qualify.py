from __future__ import annotations

from pathlib import Path


def main() -> int:
    html = Path("apps/web/index.html").read_text(encoding="utf-8")
    required = ('lang="en"', 'meta name="viewport"', 'no-store', 'aria-live', 'prefers-reduced-motion')
    passed = all(item in html for item in required)
    print(("PASS" if passed else "FAIL") + ": accessible responsive web shell")
    print("PHASE 14 QUALIFICATION: " + ("PASS" if passed else "FAIL"))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
