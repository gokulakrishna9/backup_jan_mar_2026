"""Tracks dirty/clean status per definition file via _generation_status.json."""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


class StatusTracker:
    """Tracks dirty/clean status per definition file via _generation_status.json.

    A file is "dirty" when its definition has changed since the last code generation,
    and "clean" when the generated code is up to date.
    """

    STATUS_FILE = "_generation_status.json"

    def __init__(self, app_dir: Path):
        self.app_dir = Path(app_dir)
        self.status_path = self.app_dir / self.STATUS_FILE

    def load(self) -> dict:
        """Load _generation_status.json. Returns {} if not found (treat as all-dirty)."""
        if not self.status_path.exists():
            return {}
        try:
            with open(self.status_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}

    def save(self, status: dict) -> None:
        """Write _generation_status.json."""
        self.app_dir.mkdir(parents=True, exist_ok=True)
        with open(self.status_path, "w", encoding="utf-8") as f:
            json.dump(status, f, indent=2)

    def _compute_hash(self, filename: str) -> str:
        """Compute SHA-256 hash of a definition file's contents."""
        file_path = self.app_dir / filename
        if not file_path.exists():
            return ""
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        return f"sha256:{sha256.hexdigest()}"

    def _now_iso(self) -> str:
        """Return current UTC timestamp in ISO 8601 format."""
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def _check_external_edits(self, status: dict) -> dict:
        """Detect external edits on clean files by comparing SHA-256 hashes.

        If a clean file's current hash doesn't match the stored content_hash,
        auto-mark it dirty and print a warning.
        """
        files = status.get("files", {})
        for filename, info in files.items():
            if info.get("status") == "clean":
                stored_hash = info.get("content_hash", "")
                current_hash = self._compute_hash(filename)
                if current_hash and stored_hash and current_hash != stored_hash:
                    info["status"] = "dirty"
                    info["last_modified"] = self._now_iso()
                    info["content_hash"] = current_hash
                    print(
                        f"WARNING: External edit detected on '{filename}' — "
                        f"hash mismatch (stored: {stored_hash}, current: {current_hash}). "
                        f"Auto-marking as dirty."
                    )
        return status

    def get_dirty_files(self) -> list[str]:
        """Return list of filenames with status 'dirty'.

        Also checks for external edits on clean files before returning.
        """
        status = self.load()
        if not status:
            return []
        status = self._check_external_edits(status)
        self.save(status)
        files = status.get("files", {})
        return [fname for fname, info in files.items() if info.get("status") == "dirty"]

    def get_clean_files(self) -> list[str]:
        """Return list of filenames with status 'clean'."""
        status = self.load()
        if not status:
            return []
        status = self._check_external_edits(status)
        self.save(status)
        files = status.get("files", {})
        return [fname for fname, info in files.items() if info.get("status") == "clean"]

    def mark_dirty(self, filenames: list[str]) -> None:
        """Mark specific files as dirty. Updates last_modified timestamp and content_hash."""
        status = self.load()
        if "files" not in status:
            status["files"] = {}
        now = self._now_iso()
        for fname in filenames:
            if fname not in status["files"]:
                status["files"][fname] = {}
            status["files"][fname]["status"] = "dirty"
            status["files"][fname]["last_modified"] = now
            status["files"][fname]["content_hash"] = self._compute_hash(fname)
        self.save(status)

    def mark_clean(self, filenames: list[str]) -> None:
        """Mark specific files as clean. Updates last_generated timestamp."""
        status = self.load()
        if "files" not in status:
            status["files"] = {}
        now = self._now_iso()
        for fname in filenames:
            if fname not in status["files"]:
                status["files"][fname] = {}
            status["files"][fname]["status"] = "clean"
            status["files"][fname]["last_generated"] = now
            # Update content_hash to current so external edit detection works
            status["files"][fname]["content_hash"] = self._compute_hash(fname)
        self.save(status)

    def mark_all_dirty(self) -> None:
        """Mark all tracked files as dirty."""
        status = self.load()
        if not status:
            return
        now = self._now_iso()
        for fname, info in status.get("files", {}).items():
            info["status"] = "dirty"
            info["last_modified"] = now
            info["content_hash"] = self._compute_hash(fname)
        self.save(status)

    def mark_all_clean(self) -> None:
        """Mark all tracked files as clean with updated last_generated timestamps."""
        status = self.load()
        if not status:
            return
        now = self._now_iso()
        for fname, info in status.get("files", {}).items():
            info["status"] = "clean"
            info["last_generated"] = now
            info["content_hash"] = self._compute_hash(fname)
        self.save(status)

    def is_dirty(self, filename: str) -> bool:
        """Check if a specific file is dirty.

        Returns True if the file is marked dirty, not tracked, or the status file is missing.
        """
        status = self.load()
        if not status:
            return True
        files = status.get("files", {})
        if filename not in files:
            return True
        # Check for external edit on this specific file
        info = files[filename]
        if info.get("status") == "clean":
            stored_hash = info.get("content_hash", "")
            current_hash = self._compute_hash(filename)
            if current_hash and stored_hash and current_hash != stored_hash:
                info["status"] = "dirty"
                info["last_modified"] = self._now_iso()
                info["content_hash"] = current_hash
                self.save(status)
                print(
                    f"WARNING: External edit detected on '{filename}' — "
                    f"hash mismatch. Auto-marking as dirty."
                )
                return True
        return info.get("status") == "dirty"

    def create_initial_status(self, filenames: list[str]) -> None:
        """Create _generation_status.json with all files marked dirty."""
        now = self._now_iso()
        app_name = self.app_dir.name
        files = {}
        for fname in filenames:
            files[fname] = {
                "status": "dirty",
                "last_modified": now,
                "last_generated": None,
                "content_hash": self._compute_hash(fname),
            }
        status = {
            "app_name": app_name,
            "schema_version": "1.0",
            "files": files,
            "last_full_generation": None,
        }
        self.save(status)
