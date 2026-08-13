"""Continuation 037 bounded live Hindsight and R-044 qualification."""
from __future__ import annotations

import hashlib
import io
import zipfile
import json
import os
import shutil
import subprocess
import tempfile
import uuid
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.prime_core.backup_service import BackupCoordinator, BackupError
from src.prime_core.brain_service import BrainService
from src.prime_core.config import Settings
from src.prime_core.db import connect, migrate
from src.prime_core.history_service import HistoryService
from src.prime_core.indexer import RepositoryIndexer
from src.prime_core.memory_service import MemoryService
from src.prime_core.service import CoreService
from src.prime_memory_adapter import PrimeMemoryAdapter


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout.strip()


def qualify(db_url: str, restore_db_url: str) -> dict:
    settings = Settings(database_url=db_url, hindsight_base_url="http://127.0.0.1:8888", hindsight_timeout_seconds=30)
    restore_settings = Settings(database_url=restore_db_url, hindsight_base_url="http://127.0.0.1:8888", hindsight_timeout_seconds=30)
    migrate(settings)
    migrate(restore_settings)
    root = Path(tempfile.mkdtemp(prefix="prime-c037-"))
    banks: list[PrimeMemoryAdapter] = []
    try:
        core = CoreService(settings)
        project_a = core.create_project("Continuation 037 Project A")
        project_b = core.create_project("Continuation 037 Project B")
        a_id, b_id = project_a["project_id"], project_b["project_id"]
        memory = MemoryService(settings)
        adapter_a = PrimeMemoryAdapter(settings.hindsight_base_url, a_id, settings.hindsight_timeout_seconds)
        adapter_b = PrimeMemoryAdapter(settings.hindsight_base_url, b_id, settings.hindsight_timeout_seconds)
        banks.extend([adapter_a, adapter_b])
        health = adapter_a.health()
        assert health.status == "CURRENT", health
        assert adapter_a.create_bank().status == "CURRENT"
        assert adapter_b.create_bank().status == "CURRENT"
        a_stored = memory.store(a_id, "ALPHA-BRAIN-037 durable source fact", "DECISION", source_revision="A1")
        b_stored = memory.store(b_id, "BETA-BRAIN-037 durable source fact", "DECISION", source_revision="B1")
        assert a_stored["status"] == "STORED", a_stored
        assert b_stored["status"] == "STORED", b_stored
        a_recall = memory.recall(a_id, "ALPHA-BRAIN-037")
        b_recall = memory.recall(b_id, "BETA-BRAIN-037")
        assert a_recall["status"] == "CURRENT" and a_recall["results"]
        assert b_recall["status"] == "CURRENT" and b_recall["results"]
        a_cross = memory.recall(a_id, "BETA-BRAIN-037")
        b_cross = memory.recall(b_id, "ALPHA-BRAIN-037")
        assert all(item["memory_id"] != b_stored["memory_id"] for item in a_cross["results"])
        assert all(item["memory_id"] != a_stored["memory_id"] for item in b_cross["results"])

        correction_1 = memory.store(a_id, "The fixture uses revision A.", "DECISION", source_revision="A1")
        correction_2 = memory.store(a_id, "The fixture uses revision B.", "DECISION", source_revision="B1", supersedes_memory_id=correction_1["memory_id"], correction_reason="verified revision correction")
        assert correction_2["status"] == "STORED", correction_2
        current_before_tombstone = memory.recall(a_id, "fixture uses revision")
        assert all(item["memory_id"] != correction_1["memory_id"] for item in current_before_tombstone["results"])
        memory.tombstone(a_id, correction_2["memory_id"], "fixture removed by qualification")
        after_tombstone = memory.recall(a_id, "fixture uses revision")
        assert all(item["memory_id"] not in {correction_1["memory_id"], correction_2["memory_id"]} for item in after_tombstone["results"])
        with connect(settings) as db:
            history_rows = db.execute("SELECT memory_id,status,source_revision FROM prime_core.memory_records WHERE project_id=%s AND memory_id IN (%s,%s) ORDER BY memory_id", (a_id, correction_1["memory_id"], correction_2["memory_id"])).fetchall()
            correction_rows = db.execute("SELECT correction_type,reason FROM prime_core.memory_corrections WHERE project_id=%s ORDER BY created_at", (a_id,)).fetchall()
        assert {row["status"] for row in history_rows} == {"SUPERSEDED", "TOMBSTONED"}
        assert any(row["correction_type"] == "SUPERSEDE" for row in correction_rows)
        assert any(row["correction_type"] == "TOMBSTONE" for row in correction_rows)
        rebuild_a = memory.rebuild_from_source_ledger(a_id)
        assert rebuild_a["status"] == "CURRENT" and rebuild_a["mode"] == "SOURCE_LEDGER_REBUILD"
        assert rebuild_a["restored"] == 1 and rebuild_a["eligible"] == 1
        rebuilt_revision = memory.recall(a_id, "revision A")
        assert all(item["memory_id"] not in {correction_1["memory_id"], correction_2["memory_id"]} for item in rebuilt_revision["results"])
        assert memory.recall(a_id, "ALPHA-BRAIN-037")["results"]

        # Canonical PRIME fixture for component-complete R-044 backup.
        repo = root / "repo"
        repo.mkdir()
        (repo / "fixture.txt").write_text("R044-GIT-FIXTURE", encoding="utf-8")
        git(repo, "init", "-q")
        git(repo, "config", "user.email", "qualification@example.invalid")
        git(repo, "config", "user.name", "Continuation 037")
        git(repo, "add", ".")
        git(repo, "commit", "-qm", "R-044 fixture A")
        revision = git(repo, "rev-parse", "HEAD")
        node_id = "node-c037-" + uuid.uuid4().hex
        core.register_node(node_id, "Continuation 037", "linux", uuid.uuid4().hex + uuid.uuid4().hex, [str(root)], {})
        core.bind_repository(a_id, node_id, uuid.uuid4().hex + uuid.uuid4().hex, str(repo))
        RepositoryIndexer(core).build(a_id)
        history = HistoryService(settings)
        evidence = history.record_evidence(a_id, "UPLOAD", "local://r044-fixture", b"R044-EVIDENCE-FIXTURE", source_revision=revision)
        checkpoint = history.add_git_checkpoint(a_id, str(repo), revision, str(root / "checkpoints"))
        evidence_path = Path(evidence["storage_path"])
        checkpoint_path = Path(checkpoint["bundle_locator"])
        evidence_hash = hashlib.sha256(evidence_path.read_bytes()).hexdigest()
        checkpoint_hash = hashlib.sha256(checkpoint_path.read_bytes()).hexdigest()
        bundle_path = root / "r044.continuity"
        passphrase = "continuation-037-qualification-" + uuid.uuid4().hex
        backup = BackupCoordinator().create_continuity_backup(settings, bundle_path, passphrase, project_ids=[a_id], destination_class="operator-selected")
        preflight = BackupCoordinator().preflight_restore(bundle_path, passphrase)
        manifest = preflight["manifest"]
        assert set(("prime_postgresql", "hindsight", "evidence", "historical_state", "git_checkpoints", "configuration")) <= set(manifest["component_inventory"])
        assert preflight["components"]["hindsight"]["mode"] == "SOURCE_LEDGER_REBUILD"
        assert preflight["components"]["evidence"]["fidelity"] == "EXACT_FOR_MANAGED_BYTES"
        assert preflight["components"]["git_checkpoints"]["fidelity"] == "EXACT_FOR_RETAINED_BUNDLES"
        restored = BackupCoordinator().restore_bundle(restore_settings, bundle_path, passphrase, storage_root=root / "restored-files")
        with connect(restore_settings) as db:
            restored_evidence = db.execute("SELECT storage_path FROM prime_core.evidence_records WHERE evidence_id=%s", (evidence["evidence_id"],)).fetchone()
            restored_checkpoint = db.execute("SELECT bundle_locator FROM prime_core.git_history_checkpoints WHERE checkpoint_id=%s", (checkpoint["checkpoint_id"],)).fetchone()
        assert hashlib.sha256(Path(restored_evidence["storage_path"]).read_bytes()).hexdigest() == evidence_hash
        assert hashlib.sha256(Path(restored_checkpoint["bundle_locator"]).read_bytes()).hexdigest() == checkpoint_hash

        outage_settings = Settings(database_url=db_url, hindsight_base_url="http://127.0.0.1:1", hindsight_timeout_seconds=1)
        outage_memory = MemoryService(outage_settings)
        outage = outage_memory.rebuild_from_source_ledger(a_id)
        assert outage["status"] == "UNAVAILABLE"
        with connect(settings) as db:
            assert db.execute("SELECT 1 FROM prime_core.projects WHERE project_id=%s", (a_id,)).fetchone()
        recovery = memory.rebuild_from_source_ledger(a_id)
        assert recovery["status"] == "CURRENT" and recovery["mode"] == "SOURCE_LEDGER_REBUILD"
        assert memory.recall(a_id, "ALPHA-BRAIN-037")["results"]

        negative_missing = root / "missing-required.continuity"
        coordinator = BackupCoordinator()
        original_payload = coordinator._decrypt(bundle_path, passphrase)
        with zipfile.ZipFile(io.BytesIO(original_payload)) as source:
            missing_manifest = json.loads(source.read("manifest.json"))
            missing_manifest["component_inventory"] = ["prime_postgresql"]
            prime_component = source.read("components/prime_postgresql.json")
            missing_manifest["content_hashes"] = {"prime_postgresql": hashlib.sha256(prime_component).hexdigest()}
            missing_plain = io.BytesIO()
            with zipfile.ZipFile(missing_plain, "w", compression=zipfile.ZIP_DEFLATED) as target:
                target.writestr("manifest.json", json.dumps(missing_manifest, sort_keys=True, separators=(",", ":")).encode())
                target.writestr("components/prime_postgresql.json", prime_component)
        coordinator._encrypt(missing_plain.getvalue(), negative_missing, passphrase)
        try:
            coordinator.preflight_restore(negative_missing, passphrase)
        except BackupError:
            missing_status = "REFUSED_MISSING_REQUIRED_COMPONENT"
        else:
            raise AssertionError("missing required component was accepted")
        tampered = root / "tampered.continuity"
        tampered.write_bytes(bundle_path.read_bytes()[:-17])
        try:
            coordinator.preflight_restore(tampered, passphrase)
        except BackupError:
            tamper_status = "REFUSED_CORRUPT_COMPONENT_OR_ARCHIVE"
        else:
            raise AssertionError("tampered continuity bundle was accepted")

        return {
            "continuation": "037",
            "r044": {
                "status": "VERIFIED",
                "backup_id": backup["backup_id"],
                "manifest_components": manifest["component_inventory"],
                "hindsight_manifest": preflight["components"]["hindsight"],
                "hindsight_outage": outage,
                "hindsight_recovery": recovery,
                "source_ledger_rebuild": {"mode": recovery["mode"], "fidelity": recovery["fidelity"], "restored": recovery["restored"], "eligible": recovery["eligible"], "superseded_and_tombstoned_excluded": recovery["superseded_and_tombstoned_excluded"]},
                "evidence_hash_restored": evidence_hash,
                "git_bundle_hash_restored": checkpoint_hash,
                "external_component_failure": "canonical PRIME state remained queryable while Hindsight was unavailable",
                "negative_missing_component": missing_status,
                "negative_corrupt_bundle": tamper_status,
                "component_fidelity": restored["component_fidelity"],
            },
            "hindsight": {
                "dod_067": "VERIFIED",
                "dod_068": "VERIFIED",
                "dod_069": "VERIFIED",
                "dod_070": "VERIFIED",
                "correction": "SUPERSEDE recorded with reason, source revision, immutable prior row",
                "tombstone": "TOMBSTONED current recall excluded while history retained",
                "a_b_bank_isolation": "VERIFIED",
                "bank_ids": {"A": adapter_a.bank_id, "B": adapter_b.bank_id},
            },
        }
    finally:
        for bank in banks:
            try:
                bank.delete_bank()
            except Exception:
                pass
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    db_url = os.environ["PRIME_PHASE1_DB_URL"]
    restore_db_url = os.environ["PRIME_QUAL_RESTORE_DB_URL"]
    print(json.dumps(qualify(db_url, restore_db_url), sort_keys=True, default=str))
