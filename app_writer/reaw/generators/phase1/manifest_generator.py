"""Manifest generator — produces react_manifest.json."""

import os
from typing import List

from models.react_definition_models import ManifestEntry, ReactManifest
from utils.file_writer import FileWriter


# Concern name for each definition file
_FILE_CONCERNS = {
    "react_routes.json": "routing",
    "react_form_groupings.json": "form_groupings",
    "react_component_mappings.json": "component_mappings",
    "react_page_definitions.json": "page_definitions",
    "react_layout.json": "layout",
    "react_auth_config.json": "authentication",
    "react_api_services.json": "api_services",
    "react_redux_store.json": "redux_store",
    "react_theme.json": "theme",
    "react_charts.json": "charts",
    "react_env.json": "env_config",
}


class ManifestGenerator:
    @staticmethod
    def generate(generated_files: List[str], output_dir: str) -> str:
        """Produce react_manifest.json listing all generated definition files.

        Args:
            generated_files: List of absolute paths to generated JSON files.
            output_dir: Base output directory (application_definitions/).

        Returns:
            Path to the generated manifest file.
        """
        entries: List[ManifestEntry] = []

        for file_path in generated_files:
            filename = os.path.basename(file_path)
            concern = _FILE_CONCERNS.get(filename, filename.replace(".json", ""))
            entries.append(ManifestEntry(path=filename, concern=concern))

        manifest = ReactManifest(version="1.0.0", files=entries)
        path = os.path.join(output_dir, "react_manifest.json")
        FileWriter.write_json(path, manifest.model_dump())
        return path
