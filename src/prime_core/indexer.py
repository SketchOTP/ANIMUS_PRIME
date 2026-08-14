from __future__ import annotations

import hashlib
import mimetypes
from pathlib import Path
from pathlib import PurePosixPath
from typing import Any

from .service import _id, now


class RepositoryIndexer:
    def __init__(self, service: Any, max_files: int = 100_000):
        self.service = service
        self.max_files = max_files

    def build(self, project_id: str) -> dict[str, Any]:
        from .db import transaction
        with transaction(self.service.settings) as db:
            binding = db.execute(
                "SELECT b.repository_id, r.canonical_path FROM prime_core.project_bindings b JOIN prime_core.repositories r ON r.repository_id=b.repository_id WHERE b.project_id=%s",
                (project_id,),
            ).fetchone()
            if not binding:
                raise KeyError("project has no repository binding")
            root = Path(binding["canonical_path"]).resolve(strict=True)
            if not (root / ".git").exists():
                raise ValueError("bound path is not a working repository")
            source_revision = self._revision(root)
            observed = now()
            previous_revision = db.execute("SELECT canonical_revision FROM prime_core.project_bindings WHERE project_id=%s", (project_id,)).fetchone()["canonical_revision"]
            db.execute(
                "UPDATE prime_core.repository_files SET freshness_state='STALE' "
                "WHERE project_id=%s AND repository_id=%s AND freshness_state='CURRENT'",
                (project_id, binding["repository_id"]),
            )
            count = 0
            for path in sorted(root.rglob("*")):
                if ".git" in path.relative_to(root).parts or not path.is_file():
                    continue
                if count >= self.max_files:
                    raise ValueError("repository exceeds index file limit")
                relative = path.relative_to(root).as_posix()
                data = path.read_bytes()
                kind = mimetypes.guess_type(path.name)[0] or ("binary" if b"\x00" in data[:8192] else "text")
                db.execute(
                    "INSERT INTO prime_core.repository_files(repository_file_id,project_id,repository_id,relative_path,content_hash,size_bytes,file_kind,source_revision,freshness_state,observed_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,'CURRENT',%s) ON CONFLICT (repository_id,relative_path,source_revision) DO UPDATE SET content_hash=EXCLUDED.content_hash,size_bytes=EXCLUDED.size_bytes,file_kind=EXCLUDED.file_kind,freshness_state='CURRENT',observed_at=EXCLUDED.observed_at",
                    (_id("file"), project_id, binding["repository_id"], relative, hashlib.sha256(data).hexdigest(), len(data), kind, source_revision, observed),
                )
                count += 1
            db.execute(
                "INSERT INTO prime_core.source_snapshots(source_snapshot_id,project_id,source_class,source_revision,source_hash,freshness_state,observed_at,metadata) VALUES (%s,%s,'REPOSITORY',%s,%s,'CURRENT',%s,%s) ON CONFLICT (project_id,source_class,source_revision) DO UPDATE SET freshness_state='CURRENT',observed_at=EXCLUDED.observed_at",
                (_id("snapshot"), project_id, source_revision, source_revision, observed, "{}"),
            )
            db.execute(
                "UPDATE prime_core.source_snapshots SET freshness_state='STALE' WHERE project_id=%s AND source_class='REPOSITORY' AND source_revision<>%s AND freshness_state='CURRENT'",
                (project_id, source_revision),
            )
            db.execute(
                "UPDATE prime_core.project_bindings SET canonical_revision=%s,updated_at=%s WHERE project_id=%s",
                (source_revision, observed, project_id),
            )
            if previous_revision and previous_revision != source_revision:
                db.execute("UPDATE prime_core.progress_assessments SET freshness_state='STALE' WHERE project_id=%s AND repository_revision<>%s AND freshness_state='CURRENT'", (project_id, source_revision))
            db.execute(
                "UPDATE prime_core.projects SET lifecycle_state='ACTIVE', connectivity_state='ONLINE', freshness_state='CURRENT', onboarding_step='BASELINE', onboarding_state='AWAITING_BASELINE', updated_at=%s WHERE project_id=%s",
                (observed, project_id),
            )
            result = {"project_id": project_id, "source_revision": source_revision, "files_indexed": count, "freshness_state": "CURRENT"}
        from .authority_memory_admission import AuthorityMemoryAdmission
        result["memory_admission"] = AuthorityMemoryAdmission(self.service.settings, self.service).admit(project_id, root, source_revision)
        return result

    def observe_incremental(self, project_id: str, changed_paths: list[str], source_revision: str) -> dict[str, Any]:
        """Apply a bounded repository change event without a full recursive rescan."""
        if not source_revision or not isinstance(changed_paths, list):
            raise ValueError("incremental observation requires a source revision and changed path list")
        from .db import transaction
        with transaction(self.service.settings) as db:
            binding = db.execute(
                "SELECT b.repository_id,b.canonical_revision,r.canonical_path FROM prime_core.project_bindings b JOIN prime_core.repositories r ON r.repository_id=b.repository_id WHERE b.project_id=%s",
                (project_id,),
            ).fetchone()
            if not binding:
                raise KeyError("project has no repository binding")
            root = Path(binding["canonical_path"]).resolve(strict=True)
            if not (root / ".git").exists():
                raise ValueError("bound path is not a working repository")
            relation = self._revision_relation(root, binding["canonical_revision"], source_revision)
            if relation == "SAME":
                return {"status": "NOOP", "project_id": project_id, "source_revision": source_revision, "changed_paths": []}
            normalized = self._normalize_changed_paths(root, changed_paths)
            observed = now()
            indexed = 0
            retracted = 0
            for relative, candidate in normalized:
                db.execute(
                    "UPDATE prime_core.repository_files SET freshness_state='STALE' WHERE project_id=%s AND repository_id=%s AND relative_path=%s AND freshness_state='CURRENT'",
                    (project_id, binding["repository_id"], relative),
                )
                if not candidate.exists():
                    retracted += 1
                    continue
                if not candidate.is_file():
                    raise ValueError(f"changed path is not a regular file: {relative}")
                data = candidate.read_bytes()
                kind = mimetypes.guess_type(candidate.name)[0] or ("binary" if b"\x00" in data[:8192] else "text")
                db.execute(
                    "INSERT INTO prime_core.repository_files(repository_file_id,project_id,repository_id,relative_path,content_hash,size_bytes,file_kind,source_revision,freshness_state,observed_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,'CURRENT',%s) ON CONFLICT (repository_id,relative_path,source_revision) DO UPDATE SET content_hash=EXCLUDED.content_hash,size_bytes=EXCLUDED.size_bytes,file_kind=EXCLUDED.file_kind,freshness_state='CURRENT',observed_at=EXCLUDED.observed_at",
                    (_id("file"), project_id, binding["repository_id"], relative, hashlib.sha256(data).hexdigest(), len(data), kind, source_revision, observed),
                )
                indexed += 1
            paths = [item[0] for item in normalized]
            db.execute(
                "INSERT INTO prime_core.source_snapshots(source_snapshot_id,project_id,source_class,source_revision,source_hash,freshness_state,observed_at,metadata) VALUES (%s,%s,'REPOSITORY',%s,%s,'CURRENT',%s,%s,%s) ON CONFLICT (project_id,source_class,source_revision) DO UPDATE SET freshness_state='CURRENT',observed_at=EXCLUDED.observed_at,metadata=EXCLUDED.metadata",
                (_id("snapshot"), project_id, source_revision, source_revision, observed, json.dumps({"mode": "INCREMENTAL", "changed_paths": paths})),
            )
            db.execute(
                "UPDATE prime_core.source_snapshots SET freshness_state='STALE' WHERE project_id=%s AND source_class='REPOSITORY' AND source_revision<>%s AND freshness_state='CURRENT'",
                (project_id, source_revision),
            )
            db.execute(
                "UPDATE prime_core.project_bindings SET canonical_revision=%s,updated_at=%s WHERE project_id=%s",
                (source_revision, observed, project_id),
            )
            db.execute(
                "UPDATE prime_core.projects SET connectivity_state='ONLINE',freshness_state='CURRENT',updated_at=%s WHERE project_id=%s",
                (observed, project_id),
            )
        event = self.service.emit_coalesced_event(
            "REPOSITORY_CHANGED",
            {"mode": "INCREMENTAL", "source_revision": source_revision, "changed_paths": paths},
            project_id,
            source_revision,
        )
        return {"status": "OBSERVED_INCREMENTALLY", "project_id": project_id, "source_revision": source_revision, "changed_paths": paths, "files_indexed": indexed, "files_retracted": retracted, "event_id": event["event_id"]}

    @staticmethod
    def _normalize_changed_paths(root: Path, changed_paths: list[str]) -> list[tuple[str, Path]]:
        normalized: dict[str, Path] = {}
        for raw in changed_paths:
            if not isinstance(raw, str) or not raw.strip():
                raise ValueError("changed paths must be non-empty strings")
            portable = PurePosixPath(raw.replace("\\", "/"))
            if portable.is_absolute() or ".." in portable.parts or ".git" in portable.parts:
                raise ValueError("changed path escapes the repository boundary")
            relative = portable.as_posix()
            candidate = (root / Path(*portable.parts)).resolve(strict=False)
            if candidate != root and root not in candidate.parents:
                raise ValueError("changed path escapes the repository boundary")
            normalized[relative] = candidate
        return sorted(normalized.items())

    @staticmethod
    def _revision_relation(root: Path, canonical_revision: str | None, source_revision: str) -> str:
        if not canonical_revision or canonical_revision == source_revision:
            return "SAME" if canonical_revision == source_revision else "NEWER"
        if source_revision == "UNBORN" or canonical_revision == "UNBORN":
            return "NEWER"
        import subprocess
        for revision in (canonical_revision, source_revision):
            try:
                subprocess.run(["git", "-C", str(root), "cat-file", "-e", f"{revision}^{{commit}}"], check=True, capture_output=True, text=True, timeout=5)
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
                raise ValueError("incremental observation revision is not a valid Git commit") from exc
        source_is_ancestor = subprocess.run(["git", "-C", str(root), "merge-base", "--is-ancestor", source_revision, canonical_revision], check=False, capture_output=True, text=True, timeout=5).returncode == 0
        if source_is_ancestor:
            raise ValueError("STALE_OBSERVATION_REJECTED")
        canonical_is_ancestor = subprocess.run(["git", "-C", str(root), "merge-base", "--is-ancestor", canonical_revision, source_revision], check=False, capture_output=True, text=True, timeout=5).returncode == 0
        if not canonical_is_ancestor:
            raise ValueError("CONFLICTING_OBSERVATION_REJECTED")
        return "NEWER"

    def search(self, project_id: str, query: str, limit: int = 50) -> list[dict[str, Any]]:
        from .db import connect
        with connect(self.service.settings) as db:
            rows = db.execute(
                "SELECT relative_path, content_hash, size_bytes, file_kind, source_revision, freshness_state FROM prime_core.repository_files WHERE project_id=%s AND freshness_state='CURRENT' AND relative_path ILIKE %s ORDER BY relative_path LIMIT %s",
                (project_id, f"%{query}%", min(max(limit, 1), 100)),
            ).fetchall()
            return [dict(row) for row in rows]

    @staticmethod
    def _revision(root: Path) -> str:
        import subprocess
        try:
            return subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], check=True, capture_output=True, text=True, timeout=5).stdout.strip() or "UNBORN"
        except subprocess.CalledProcessError:
            return "UNBORN"
