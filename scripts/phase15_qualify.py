from __future__ import annotations

import os
import re
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
    for phase in range(2, 15):
        checks.append((f"phase {phase} migration qualification", run([sys.executable, f"scripts/phase{phase}_qualify.py"], env)))
    baseline = (ROOT / "baseline" / "implementation-baseline.yaml").read_text(encoding="utf-8")
    checks.append(("approved baseline identity", "spec_revision: PRIME-SPEC-V1.0.0" in baseline and "operator_approval: APPROVED" in baseline))
    matrix = (ROOT / "docs" / "phase15-remediation-matrix.yaml").read_text(encoding="utf-8")
    matrix_rows = re.findall(r"- \{requirement_id: (R-\d+),.*?current_status: ([A-Z_]+),.*?final_status: ([A-Z_]+)\}", matrix)
    checks.append(("release remediation matrix is populated", bool(matrix_rows)))
    ledger = (ROOT / "docs" / "phase15-remediation-qualification-ledger.yaml").read_text(encoding="utf-8")
    ledger_rows = [line for line in ledger.splitlines() if line.lstrip().startswith("- {requirement_id:")]
    required_fields = (
        "spec_section",
        "original_owning_phase",
        "current_status",
        "implementation_complete",
        "native_or_live_execution_required",
        "environment_required",
        "positive_test",
        "negative_test",
        "degraded_test",
        "recovery_test",
        "security_test",
        "evidence_paths",
        "implementation_commit",
        "evidence_commit",
        "remaining_gap",
        "final_status",
    )
    ledger_ids = {re.search(r"requirement_id: (R-\d+)", line).group(1) for line in ledger_rows if re.search(r"requirement_id: (R-\d+)", line)}
    expected_ids = {f"R-{number:03d}" for number in range(31, 57)}
    checks.append(("requirement-level qualification ledger is complete", ledger_ids == expected_ids and all(all(f"{field}:" in line for field in required_fields) for line in ledger_rows)))
    for requirement_id, current_status, final_status in matrix_rows:
        checks.append((f"V1 requirement {requirement_id} VERIFIED", current_status == "VERIFIED" and final_status == "VERIFIED"))
    for name, result in checks:
        print(("PASS" if result else "FAIL") + ": " + name)
        passed = passed and result
    print("PHASE 15 QUALIFICATION: " + ("PASS" if passed else "FAIL"))
    if not passed:
        print("V1 release result: FAIL — inspect the failing gate evidence before claiming completion.")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
