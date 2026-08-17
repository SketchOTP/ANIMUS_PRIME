from __future__ import annotations

import hashlib
import json
import mimetypes
import re
from pathlib import Path
from pathlib import PurePosixPath
from typing import Any

from .service import _id, now

SEARCH_STOPWORDS = {
    "about", "after", "again", "also", "and", "are", "does", "for", "from", "how", "into",
    "is", "its", "more", "no", "not", "of", "on", "or", "our", "please", "result", "say",
    "some", "that", "the", "their", "there", "these", "this", "to", "was", "what", "when", "where",
    "which", "who", "why", "with", "would", "you",
}


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
            branch = self._branch(root)
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
                    "INSERT INTO prime_core.repository_files(repository_file_id,project_id,repository_id,relative_path,content_hash,size_bytes,file_kind,content_text,source_revision,observation_basis,canonical_revision,worktree_branch,worktree_path,freshness_state,observed_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,'COMMITTED_CANONICAL',%s,%s,%s,'CURRENT',%s) ON CONFLICT (repository_id,relative_path,source_revision) DO UPDATE SET content_hash=EXCLUDED.content_hash,size_bytes=EXCLUDED.size_bytes,file_kind=EXCLUDED.file_kind,content_text=EXCLUDED.content_text,observation_basis='COMMITTED_CANONICAL',canonical_revision=EXCLUDED.canonical_revision,worktree_branch=EXCLUDED.worktree_branch,worktree_path=EXCLUDED.worktree_path,freshness_state='CURRENT',observed_at=EXCLUDED.observed_at",
                    (_id("file"), project_id, binding["repository_id"], relative, hashlib.sha256(data).hexdigest(), len(data), kind, self._search_text(data, kind), source_revision, source_revision, branch, str(root), observed),
                )
                count += 1
            db.execute(
                "INSERT INTO prime_core.source_snapshots(source_snapshot_id,project_id,source_class,source_revision,source_hash,freshness_state,observed_at,metadata) VALUES (%s,%s,'REPOSITORY',%s,%s,'CURRENT',%s,%s) ON CONFLICT (project_id,source_class,source_revision) DO UPDATE SET freshness_state='CURRENT',observed_at=EXCLUDED.observed_at",
                (_id("snapshot"), project_id, source_revision, source_revision, observed, json.dumps({"mode": "FULL", "observation_basis": "COMMITTED_CANONICAL", "canonical_revision": source_revision, "worktree_branch": branch, "worktree_path": str(root)})),
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
            actual_head = self._revision(root)
            if source_revision != actual_head:
                raise ValueError("OBSERVATION_REVISION_MISMATCH")
            normalized = self._normalize_changed_paths(root, changed_paths)
            relation = self._revision_relation(root, binding["canonical_revision"], source_revision)
            dirty_by_path = {relative: self._worktree_status(root, relative) for relative, _candidate in normalized}
            dirty_paths = [relative for relative, status in dirty_by_path.items() if status]
            if relation == "SAME" and not dirty_paths:
                return {"status": "NOOP", "project_id": project_id, "source_revision": source_revision, "changed_paths": []}
            if relation == "NEWER" and dirty_paths:
                raise ValueError("DIRTY_WORKTREE_REQUIRES_CANONICAL_CLEAN")
            observation_basis = "WORKTREE_DIRTY" if dirty_paths else "COMMITTED_CANONICAL"
            observed = now()
            branch = self._branch(root)
            observations: list[tuple[str, Path, bytes | None, str, str]] = []
            for relative, candidate in normalized:
                status = dirty_by_path[relative]
                if not candidate.exists():
                    observations.append((relative, candidate, None, hashlib.sha256(b"<MISSING>").hexdigest(), status))
                    continue
                if not candidate.is_file():
                    raise ValueError(f"changed path is not a regular file: {relative}")
                data = candidate.read_bytes()
                observations.append((relative, candidate, data, hashlib.sha256(data).hexdigest(), status))
            if observation_basis == "WORKTREE_DIRTY":
                snapshot_key = hashlib.sha256(json.dumps([(relative, digest, status) for relative, _candidate, _data, digest, status in observations], sort_keys=True).encode("utf-8")).hexdigest()
                observation_revision = f"WORKTREE:{actual_head}:{snapshot_key}"
            else:
                snapshot_key = source_revision
                observation_revision = source_revision
            indexed = 0
            retracted = 0
            for relative, candidate, data, content_hash, _status in observations:
                db.execute(
                    "UPDATE prime_core.repository_files SET freshness_state='STALE' WHERE project_id=%s AND repository_id=%s AND relative_path=%s AND freshness_state='CURRENT'",
                    (project_id, binding["repository_id"], relative),
                )
                if data is None:
                    retracted += 1
                    continue
                kind = mimetypes.guess_type(candidate.name)[0] or ("binary" if b"\x00" in data[:8192] else "text")
                db.execute(
                    "INSERT INTO prime_core.repository_files(repository_file_id,project_id,repository_id,relative_path,content_hash,size_bytes,file_kind,content_text,source_revision,observation_basis,canonical_revision,worktree_branch,worktree_path,freshness_state,observed_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'CURRENT',%s) ON CONFLICT (repository_id,relative_path,source_revision) DO UPDATE SET content_hash=EXCLUDED.content_hash,size_bytes=EXCLUDED.size_bytes,file_kind=EXCLUDED.file_kind,content_text=EXCLUDED.content_text,observation_basis=EXCLUDED.observation_basis,canonical_revision=EXCLUDED.canonical_revision,worktree_branch=EXCLUDED.worktree_branch,worktree_path=EXCLUDED.worktree_path,freshness_state='CURRENT',observed_at=EXCLUDED.observed_at",
                    (_id("file"), project_id, binding["repository_id"], relative, content_hash, len(data), kind, self._search_text(data, kind), observation_revision, observation_basis, actual_head, branch, str(root), observed),
                )
                indexed += 1
            paths = [item[0] for item in normalized]
            db.execute(
                "INSERT INTO prime_core.source_snapshots(source_snapshot_id,project_id,source_class,source_revision,source_hash,freshness_state,observed_at,metadata) VALUES (%s,%s,'REPOSITORY',%s,%s,'CURRENT',%s,%s) ON CONFLICT (project_id,source_class,source_revision) DO UPDATE SET freshness_state='CURRENT',observed_at=EXCLUDED.observed_at,metadata=EXCLUDED.metadata",
                (_id("snapshot"), project_id, observation_revision, snapshot_key, observed, json.dumps({"mode": "INCREMENTAL", "observation_basis": observation_basis, "changed_paths": paths, "canonical_revision": actual_head, "worktree_branch": branch, "worktree_path": str(root), "dirty_paths": dirty_paths})),
            )
            if observation_basis == "COMMITTED_CANONICAL":
                db.execute(
                    "UPDATE prime_core.source_snapshots SET freshness_state='STALE' WHERE project_id=%s AND source_class='REPOSITORY' AND source_revision<>%s AND source_revision NOT LIKE 'WORKTREE:%%' AND freshness_state='CURRENT'",
                    (project_id, observation_revision),
                )
                db.execute(
                    "UPDATE prime_core.project_bindings SET canonical_revision=%s,updated_at=%s WHERE project_id=%s",
                    (actual_head, observed, project_id),
                )
                db.execute(
                    "UPDATE prime_core.progress_assessments SET freshness_state='STALE' WHERE project_id=%s AND repository_revision<>%s AND freshness_state='CURRENT'",
                    (project_id, actual_head),
                )
                db.execute(
                    "UPDATE prime_core.projects SET connectivity_state='ONLINE',freshness_state='CURRENT',updated_at=%s WHERE project_id=%s",
                    (observed, project_id),
                )
            else:
                db.execute(
                    "UPDATE prime_core.source_snapshots SET freshness_state='STALE' WHERE project_id=%s AND source_class='REPOSITORY' AND source_revision LIKE 'WORKTREE:%%' AND source_revision<>%s AND freshness_state='CURRENT'",
                    (project_id, observation_revision),
                )
                db.execute(
                    "UPDATE prime_core.projects SET connectivity_state='ONLINE',freshness_state='STALE',updated_at=%s WHERE project_id=%s",
                    (observed, project_id),
                )
        event = self.service.emit_coalesced_event(
            "REPOSITORY_CHANGED",
            {"mode": "INCREMENTAL", "observation_basis": observation_basis, "source_revision": source_revision, "canonical_revision": actual_head, "worktree_branch": branch, "changed_paths": paths, "dirty_paths": dirty_paths, "observation_revision": observation_revision},
            project_id,
            observation_revision,
        )
        if observation_basis == "COMMITTED_CANONICAL" and any(path in {".agent/DIRECTIVES.md", ".agent/OUTCOMES.md", ".agent/LEARNINGS.md", ".agent/RECORD.md"} for path in paths):
            from .authority_memory_admission import AuthorityMemoryAdmission
            memory_admission = AuthorityMemoryAdmission(self.service.settings, self.service).admit(project_id, root, actual_head)
        else:
            memory_admission = {"status": "NOT_RUN", "reason": "WORKTREE_DIRTY" if observation_basis == "WORKTREE_DIRTY" else "NO_AUTHORITY_LEDGER_PATH", "records": []}
        return {"status": "OBSERVED_INCREMENTALLY", "project_id": project_id, "source_revision": source_revision, "observation_revision": observation_revision, "observation_basis": observation_basis, "canonical_revision": actual_head, "worktree_branch": branch, "changed_paths": paths, "dirty_paths": dirty_paths, "files_indexed": indexed, "files_retracted": retracted, "event_id": event["event_id"], "memory_admission": memory_admission}

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
        if not query or not query.strip():
            return []
        # Natural-language questions should retrieve content when any
        # meaningful term matches.  websearch_to_tsquery alone treats the
        # question as an AND query, which makes ordinary questions such as
        # "What does AGENTS.md say about code exploration?" miss the file
        # even though its content is indexed.  Build a sanitized OR query
        # for retrieval while retaining the original query for path matches.
        tokens = [token for token in re.findall(r"[A-Za-z0-9_]{3,}", query.lower()) if token not in SEARCH_STOPWORDS]
        fts_query = " | ".join(f"{token}:*" for token in dict.fromkeys(tokens)) or "__prime_no_match__:*"
        normalized_query = query.lower()
        path_query = f"%{query}%"
        if "agents" in normalized_query:
            path_query = "%AGENTS.md%"
        elif "project" in normalized_query and "goal" in normalized_query:
            path_query = "%PROJECT_GOAL.md%"
        with connect(self.service.settings) as db:
            rows = db.execute(
                "SELECT relative_path, content_hash, size_bytes, file_kind, content_text, source_revision, freshness_state, "
                "CASE WHEN relative_path ILIKE %s THEN 1.0 ELSE GREATEST(ts_rank(to_tsvector('simple', COALESCE(content_text,'')), to_tsquery('simple', %s)), ts_rank(to_tsvector('simple', COALESCE(content_text,'')), websearch_to_tsquery('simple', %s))) END AS relevance, "
                "CASE WHEN content_text IS NULL OR content_text='' THEN '' ELSE ts_headline('simple', content_text, to_tsquery('simple', %s), 'MaxFragments=3,MaxWords=45,MinWords=8') END AS excerpt "
                "FROM prime_core.repository_files WHERE project_id=%s AND freshness_state='CURRENT' AND (relative_path ILIKE %s OR to_tsvector('simple', COALESCE(content_text,'')) @@ to_tsquery('simple', %s) OR to_tsvector('simple', COALESCE(content_text,'')) @@ websearch_to_tsquery('simple', %s)) "
                "ORDER BY relevance DESC, relative_path LIMIT %s",
                (path_query, fts_query, query, fts_query, project_id, path_query, fts_query, query, min(max(limit, 1), 100)),
            ).fetchall()
            result = []
            for row in rows:
                item = dict(row)
                item["text"] = item.get("content_text") or ""
                item.pop("content_text", None)
                result.append(item)
            return result

    @staticmethod
    def _search_text(data: bytes, kind: str, max_bytes: int = 200_000) -> str:
        if kind == "binary" or b"\x00" in data[:8192] or len(data) > max_bytes:
            return ""
        return data.decode("utf-8", errors="replace")

    @staticmethod
    def _revision(root: Path) -> str:
        import subprocess
        try:
            return subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], check=True, capture_output=True, text=True, timeout=5).stdout.strip() or "UNBORN"
        except subprocess.CalledProcessError:
            return "UNBORN"

    @staticmethod
    def _worktree_status(root: Path, relative: str) -> str:
        import subprocess
        try:
            return subprocess.run(
                ["git", "-C", str(root), "status", "--porcelain=v1", "--untracked-files=all", "--", relative],
                check=True, capture_output=True, text=True, timeout=5,
            ).stdout.strip()
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
            raise ValueError("unable to determine working-tree status") from exc

    @staticmethod
    def _branch(root: Path) -> str:
        import subprocess
        try:
            return subprocess.run(
                ["git", "-C", str(root), "branch", "--show-current"],
                check=True, capture_output=True, text=True, timeout=5,
            ).stdout.strip() or "DETACHED"
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
            raise ValueError("unable to determine repository branch") from exc
