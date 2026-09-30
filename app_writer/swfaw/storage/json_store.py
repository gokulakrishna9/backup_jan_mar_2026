"""JSON file storage backend — wraps existing split_definition functions."""

import json
import shutil
from pathlib import Path
from typing import Optional, Dict, Any, List

from .base import DefinitionStore
from models.database_definition import DatabaseDefinition
from utils.definition_splitter import (
    split_definition,
    load_split_definition,
    load_layer_definitions_if_exist,
)


class JsonStore(DefinitionStore):
    """Storage backend that reads/writes JSON files in application_definitions/.

    This is a thin wrapper around the existing split_definition utilities.
    No logic is duplicated — all file I/O delegates to definition_splitter.
    """

    def save(self, db_def: DatabaseDefinition, output_dir: str) -> str:
        """Save definition as split JSON files.

        Returns:
            Path to the manifest.json file
        """
        file_paths = split_definition(db_def, output_dir)
        return file_paths['manifest']

    def load(self, identifier: str) -> DatabaseDefinition:
        """Load definition from split JSON files.

        Args:
            identifier: output_dir containing application_definitions/
        """
        return load_split_definition(identifier)

    def load_layer_definitions(self, identifier: str) -> Optional[Dict[str, Any]]:
        """Load layer definitions from JSON files if they exist."""
        return load_layer_definitions_if_exist(identifier)

    def list_apps(self) -> List[Dict[str, Any]]:
        """Scan ../generated_application/ for existing definitions."""
        gen_dir = Path("../generated_application")
        if not gen_dir.exists():
            return []

        apps = []
        for app_dir in sorted(gen_dir.iterdir()):
            manifest = app_dir / "application_definitions" / "webflux_manifest.json"
            if manifest.exists():
                try:
                    with open(manifest, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    apps.append({
                        "identifier": str(app_dir),
                        "name": app_dir.name,
                        "version": data.get("version"),
                        "statistics": data.get("statistics", {}),
                    })
                except (json.JSONDecodeError, IOError):
                    pass
        return apps

    def delete(self, identifier: str) -> bool:
        """Delete an application directory."""
        path = Path(identifier)
        if path.exists() and path.is_dir():
            shutil.rmtree(path)
            return True
        return False
