from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).parents[1]


def run(argv: list[str], env: dict[str, str] | None = None) -> bool:
    result = subprocess.run(argv, cwd=ROOT, env=env, text=True)
    return result.returncode == 0


def main() -> int:
    env = os.environ.copy()
    passed = True
    checks: list[tuple[str, bool]] = []
    checks.append(("governance", run(["python3", "scripts/validate_governance.py", "--mode", "ADOPTED"], env)))
    checks.append(("full phase regression suite", run([sys.executable, "-m", "pytest", "tests", "-q"], env)))
    checks.append(("phase 1 migration qualification", run([sys.executable, "scripts/phase1_qualify.py"], env)))
    for phase in range(2, 14):
        checks.append((f"phase {phase} migration qualification", run([sys.executable, f"scripts/phase{phase}_qualify.py"], env)))
    baseline = (ROOT / "baseline" / "implementation-baseline.yaml").read_text(encoding="utf-8")
    checks.append(("approved baseline identity", "spec_revision: PRIME-SPEC-V1.0.0" in baseline and "operator_approval: APPROVED" in baseline))
    release_gaps = [
        "live Notion API dispatch/credential lifecycle",
        "native Linux/Windows Node packaging and authenticated Core↔Node encrypted control plane",
        "full operator product UX (Home, Integrity, Progress, Memory Inspector, Ask/Search workflows)",
        "Tailscale Serve setup/diagnostics and Funnel refusal integration",
        "automated scheduled encrypted backup/restore drills and full capacity/cost controls",
        "complete historical Git cache/Time Lens reconstruction and production Evidence parsers",
        "full AI evaluation/regression suite and V1 end-to-end release evidence",
    ]
    for gap in release_gaps:
        checks.append(("V1 DoD gap: " + gap, False))
    for name, result in checks:
        print(("PASS" if result else "FAIL") + ": " + name)
        passed = passed and result
    print("PHASE 15 QUALIFICATION: " + ("PASS" if passed else "FAIL"))
    if not passed:
        print("V1 release result: FAIL — inspect the failing gate evidence before claiming completion.")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
