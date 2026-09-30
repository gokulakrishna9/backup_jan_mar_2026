"""Standalone Definition Editor — generic JSON CRUD for application definitions.

Works with both webflux_*.json and react_*.json files in any application_definitions/ folder.
No dependency on swfaw or reaw modules.

Operations: get, set, update, delete, append, find, filter, exists, list_files, diff, backup, restore
Path syntax: dot notation ("jwt.expiration"), array access ("entities[0].name"), combined ("routes[0].path")
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union


# ─── Aliases ────────────────────────────────────────────────────────────────
# Short names → actual file names for both webflux and react definitions

WEBFLUX_ALIASES = {
    "wf:entity": "webflux_entity_layer.json",
    "wf:repository": "webflux_repository_layer.json",
    "wf:service": "webflux_service_layer.json",
    "wf:controller": "webflux_controller_layer.json",
    "wf:dto": "webflux_dto_layer.json",
    "wf:security": "webflux_security_layer.json",
    "wf:config": "webflux_config_layer.json",
    "wf:exception": "webflux_exception_layer.json",
    "wf:audit": "webflux_audit_logging_layer.json",
    "wf:authorization": "webflux_authorization_layer.json",
    "wf:custom_queries": "webflux_custom_queries_layer.json",
    "wf:group_definition": "webflux_group_definition_layer.json",
    "wf:manifest": "webflux_manifest.json",
    "wf:metadata": "webflux_project_metadata.json",
    "wf:entities": "webflux_entities.json",
    "wf:relationships": "webflux_relationships.json",
}

REACT_ALIASES = {
    "rx:routes": "react_routes.json",
    "rx:auth": "react_auth_config.json",
    "rx:layout": "react_layout.json",
    "rx:components": "react_component_mappings.json",
    "rx:pages": "react_page_definitions.json",
    "rx:api": "react_api_services.json",
    "rx:redux": "react_redux_store.json",
    "rx:theme": "react_theme.json",
    "rx:charts": "react_charts.json",
    "rx:manifest": "react_manifest.json",
    "rx:groupings": "react_form_groupings.json",
}

ALL_ALIASES = {**WEBFLUX_ALIASES, **REACT_ALIASES}


# ─── Path parsing ───────────────────────────────────────────────────────────

def _parse_path(path: str) -> List[Union[str, int]]:
    """Parse dot/bracket notation into path parts."""
    parts = []
    current = ""
    in_bracket = False

    for char in path:
        if char == '[':
            if current:
                parts.append(current)
                current = ""
            in_bracket = True
        elif char == ']':
            if in_bracket and current:
                parts.append(int(current))
                current = ""
            in_bracket = False
        elif char == '.' and not in_bracket:
            if current:
                parts.append(current)
                current = ""
        else:
            current += char

    if current:
        parts.append(int(current) if in_bracket else current)

    return parts


def _get_nested(data: Any, path: str) -> Any:
    """Navigate to a value using dot/bracket path."""
    if not path:
        return data
    current = data
    for part in _parse_path(path):
        if isinstance(part, int):
            current = current[part]
        else:
            current = current[part]
    return current


def _set_nested(data: Any, path: str, value: Any) -> None:
    """Set a value at a dot/bracket path."""
    parts = _parse_path(path)
    current = data
    for part in parts[:-1]:
        current = current[part]
    current[parts[-1]] = value


def _delete_nested(data: Any, path: str) -> None:
    """Delete a value at a dot/bracket path."""
    parts = _parse_path(path)
    current = data
    for part in parts[:-1]:
        current = current[part]
    last = parts[-1]
    if isinstance(last, int) and isinstance(current, list):
        del current[last]
    elif isinstance(current, dict):
        del current[last]
    else:
        raise ValueError(f"Cannot delete at path: {path}")


# ─── Editor class ───────────────────────────────────────────────────────────

class DefinitionEditor:
    """Generic JSON CRUD editor for application_definitions/ folders.

    Works with both webflux_*.json and react_*.json files.
    Supports aliases (wf:security, rx:theme, etc.) or direct file names.
    """

    def __init__(self, definitions_dir: str):
        """Initialize with path to application_definitions/ folder.

        Args:
            definitions_dir: Path to the directory containing definition JSON files.
        """
        self.dir = Path(definitions_dir).resolve()
        if not self.dir.is_dir():
            raise FileNotFoundError(f"Directory not found: {self.dir}")

    def _resolve(self, name: str) -> Path:
        """Resolve alias or filename to full path."""
        filename = ALL_ALIASES.get(name, name)
        if not filename.endswith(".json"):
            filename += ".json"
        return self.dir / filename

    def _read(self, name: str) -> Tuple[Path, Any]:
        """Read and return (path, data) for a file."""
        p = self._resolve(name)
        if not p.is_file():
            raise FileNotFoundError(f"Not found: {p}")
        with open(p, "r", encoding="utf-8") as f:
            return p, json.load(f)

    def _write(self, path: Path, data: Any) -> None:
        """Write data back to a file."""
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # ── CRUD operations ─────────────────────────────────────────────────

    def get(self, name: str, path: Optional[str] = None) -> Any:
        """Read a value. Returns entire file if path is None.

        Examples:
            editor.get("rx:theme")
            editor.get("rx:theme", "colorPalette.accent")
            editor.get("wf:entities", "entities[0].name")
        """
        _, data = self._read(name)
        return _get_nested(data, path) if path else data

    def set(self, name: str, path: str, value: Any) -> None:
        """Set a value at a path.

        Examples:
            editor.set("rx:theme", "colorPalette.accent", "#2563eb")
            editor.set("wf:security", "jwt.expiration", 3600000)
        """
        p, data = self._read(name)
        _set_nested(data, path, value)
        self._write(p, data)

    def update(self, name: str, path: Optional[str], updates: Dict[str, Any]) -> None:
        """Merge updates into an object at path. Use path=None for root.

        Examples:
            editor.update("rx:theme", "typography", {"fontSize": "16px", "lineHeight": "1.6"})
            editor.update("wf:metadata", None, {"applicationName": "My App"})
        """
        p, data = self._read(name)
        target = _get_nested(data, path) if path else data
        if not isinstance(target, dict):
            raise ValueError(f"Target at '{path}' is not a dict")
        target.update(updates)
        self._write(p, data)

    def delete(self, name: str, path: str) -> None:
        """Delete a value at a path.

        Examples:
            editor.delete("rx:theme", "source")
            editor.delete("wf:entities", "entities[2]")
        """
        p, data = self._read(name)
        _delete_nested(data, path)
        self._write(p, data)

    def append(self, name: str, path: str, value: Any) -> None:
        """Append a value to an array at path.

        Examples:
            editor.append("rx:routes", "", {"path": "/new", "pageType": "entity", ...})
            editor.append("wf:entities", "entities", {"name": "new_table", ...})
        """
        p, data = self._read(name)
        target = _get_nested(data, path) if path else data
        if not isinstance(target, list):
            raise ValueError(f"Target at '{path}' is not an array")
        target.append(value)
        self._write(p, data)

    def find(self, name: str, path: str, predicate: Dict[str, Any]) -> Optional[Any]:
        """Find first item in an array matching all predicate key-value pairs.

        Examples:
            editor.find("rx:routes", "", {"entityName": "User"})
            editor.find("wf:entities", "entities", {"name": "ems_users"})
        """
        arr = self.get(name, path) if path else self.get(name)
        if not isinstance(arr, list):
            raise ValueError(f"Target at '{path}' is not an array")
        for item in arr:
            if isinstance(item, dict) and all(item.get(k) == v for k, v in predicate.items()):
                return item
        return None

    def filter(self, name: str, path: str, predicate: Dict[str, Any]) -> List[Any]:
        """Filter items in an array matching all predicate key-value pairs.

        Examples:
            editor.filter("rx:routes", "", {"pageType": "entity"})
            editor.filter("rx:components", "", {"entityName": "User"})
        """
        arr = self.get(name, path) if path else self.get(name)
        if not isinstance(arr, list):
            raise ValueError(f"Target at '{path}' is not an array")
        return [i for i in arr if isinstance(i, dict) and all(i.get(k) == v for k, v in predicate.items())]

    def exists(self, name: str, path: Optional[str] = None) -> bool:
        """Check if a file or path within a file exists.

        Examples:
            editor.exists("rx:theme")
            editor.exists("rx:theme", "colorPalette.accent")
        """
        try:
            p = self._resolve(name)
            if not p.is_file():
                return False
            if path is None:
                return True
            _, data = self._read(name)
            _get_nested(data, path)
            return True
        except (KeyError, IndexError, ValueError, FileNotFoundError):
            return False

    # ── Listing ─────────────────────────────────────────────────────────

    def list_files(self, prefix: Optional[str] = None) -> List[str]:
        """List JSON files. Optional prefix filter: 'webflux', 'react', or None for all.

        Examples:
            editor.list_files()            # all
            editor.list_files("react")     # react_*.json only
            editor.list_files("webflux")   # webflux_*.json only
        """
        files = sorted(f.name for f in self.dir.glob("*.json"))
        if prefix:
            files = [f for f in files if f.startswith(prefix)]
        return files

    def list_aliases(self, prefix: Optional[str] = None) -> Dict[str, str]:
        """List available aliases. Optional prefix filter: 'wf' or 'rx'.

        Examples:
            editor.list_aliases()       # all
            editor.list_aliases("rx")   # react aliases only
        """
        if prefix:
            return {k: v for k, v in ALL_ALIASES.items() if k.startswith(prefix + ":")}
        return dict(ALL_ALIASES)

    # ── Diff ────────────────────────────────────────────────────────────

    def diff(self, name: str, path: Optional[str], other_dir: str) -> Dict[str, Any]:
        """Compare a file/path between this definitions dir and another.

        Returns {"left": value_here, "right": value_there, "equal": bool}.

        Examples:
            editor.diff("rx:theme", "colorPalette", "/other/application_definitions")
        """
        left = self.get(name, path)
        other = DefinitionEditor(other_dir)
        right = other.get(name, path)
        return {"left": left, "right": right, "equal": left == right}

    # ── Backup / Restore ────────────────────────────────────────────────

    def backup(self, name: str) -> str:
        """Create a timestamped backup of a file. Returns backup path.

        Examples:
            editor.backup("rx:theme")  # → react_theme.20260323_120000.bak.json
        """
        p, _ = self._read(name)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        bak = p.with_suffix(f".{ts}.bak.json")
        shutil.copy2(p, bak)
        return str(bak)

    def restore(self, backup_path: str) -> str:
        """Restore a file from a backup. Returns the restored file path.

        Examples:
            editor.restore("react_theme.20260323_120000.bak.json")
        """
        bak = Path(backup_path)
        if not bak.is_absolute():
            bak = self.dir / bak
        if not bak.is_file():
            raise FileNotFoundError(f"Backup not found: {bak}")
        # Extract original name: remove .TIMESTAMP.bak from the name
        original_name = bak.name
        # Pattern: name.YYYYMMDD_HHMMSS.bak.json → name.json
        parts = original_name.split(".")
        if len(parts) >= 4 and parts[-2] == "bak":
            original_name = parts[0] + ".json"
        target = self.dir / original_name
        shutil.copy2(bak, target)
        return str(target)
