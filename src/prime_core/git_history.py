from __future__ import annotations

import hashlib
import subprocess
import tempfile
from pathlib import Path


def create_checkpoint_bundle(repository_path: str, commit_id: str, output_path: str) -> dict[str, str]:
    """Preserve a canonical commit in a PRIME-owned bundle without mutating refs."""
    repo = Path(repository_path).resolve()
    output = Path(output_path).resolve()
    if not repo.is_dir() or not (repo / ".git").exists():
        raise ValueError("Git checkpoint requires a working repository")
    try:
        verified = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "--verify", f"{commit_id}^{{commit}}"],
            check=True,
            capture_output=True,
            text=True,
            timeout=15,
        ).stdout.strip()
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        raise ValueError("requested Git checkpoint is not a canonical commit") from exc
    output.parent.mkdir(parents=True, exist_ok=True)
    # A bundle made directly from the working repository can be empty when the
    # selected commit is still reachable from a branch. Pack the selected
    # history into a disposable bare cache first, then create the durable
    # PRIME-owned bundle from that isolated object store.
    with tempfile.TemporaryDirectory(prefix="prime-git-checkpoint-") as temp_dir:
        bare = Path(temp_dir) / "objects.git"
        subprocess.run(["git", "init", "--bare", "-q", str(bare)], check=True, capture_output=True, text=True, timeout=15)
        packed = subprocess.run(
            ["git", "-C", str(repo), "pack-objects", "--stdout", "--revs"],
            input=f"{verified}\n".encode(),
            check=True,
            capture_output=True,
            text=False,
            timeout=30,
        ).stdout
        subprocess.run(
            ["git", "--git-dir", str(bare), "index-pack", "--stdin", "--fix-thin", "--keep=prime-checkpoint"],
            input=packed,
            check=True,
            capture_output=True,
            timeout=30,
        )
        subprocess.run(["git", "--git-dir", str(bare), "update-ref", "refs/prime/checkpoint", verified], check=True, capture_output=True, text=True, timeout=15)
        subprocess.run(
            ["git", "--git-dir", str(bare), "bundle", "create", str(output), "refs/prime/checkpoint"],
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
    subprocess.run(["git", "bundle", "verify", str(output)], check=True, capture_output=True, text=True, timeout=30)
    return {"commit_id": verified, "bundle_locator": str(output), "content_hash": hashlib.sha256(output.read_bytes()).hexdigest()}


def checkpoint_bundle_status(bundle_path: str, expected_hash: str | None = None) -> str:
    bundle = Path(bundle_path)
    if not bundle.is_file():
        return "UNAVAILABLE"
    if expected_hash and hashlib.sha256(bundle.read_bytes()).hexdigest() != expected_hash:
        return "PARTIAL"
    try:
        subprocess.run(["git", "bundle", "verify", str(bundle)], check=True, capture_output=True, text=True, timeout=30)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return "PARTIAL"
    return "EXACT"
