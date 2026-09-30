"""React Definition Parser — reads react_*.json files and produces ReactAppDefinition.

Used by Phase 2 to load the (possibly user-edited) React Application Definition.
The react definition files live alongside swfaw definition files in the same
application_definitions/ directory, prefixed with ``react_``.
"""

import json
import logging
import os
from typing import Any, Dict, List, Set

from models.react_definition_models import (
    ApiServiceDefinition,
    AuthConfig,
    ChartsDefinition,
    ComponentMapping,
    EnvDefinition,
    FormGrouping,
    LayoutDefinition,
    PageDefinition,
    ReactAppDefinition,
    ReactManifest,
    ReduxStoreDefinition,
    RouteDefinition,
    ThemeDefinition,
)

logger = logging.getLogger(__name__)


class ReactDefinitionParseError(Exception):
    """Raised when parsing the React Application Definition fails."""

    def __init__(self, message: str, file_name: str = "", error_location: str = "", invalid_reference: str = ""):
        self.file_name = file_name
        self.error_location = error_location
        self.invalid_reference = invalid_reference
        super().__init__(message)


# Concern name → (model class, field name on ReactAppDefinition, is_list)
_CONCERN_MAP: Dict[str, tuple] = {
    "routing": (RouteDefinition, "routes", True),
    "form_groupings": (FormGrouping, "form_groupings", True),
    "component_mappings": (ComponentMapping, "component_mappings", True),
    "page_definitions": (PageDefinition, "page_definitions", True),
    "layout": (LayoutDefinition, "layout", False),
    "authentication": (AuthConfig, "auth_config", False),
    "api_services": (ApiServiceDefinition, "api_services", True),
    "redux_store": (ReduxStoreDefinition, "redux_store", True),
    "theme": (ThemeDefinition, "theme", False),
    "charts": (ChartsDefinition, "charts", False),
    "env_config": (EnvDefinition, "env_config", False),
}


def _read_json(file_path: str) -> Any:
    """Read and parse a JSON file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ReactDefinitionParseError(
            f"Malformed JSON in {os.path.basename(file_path)}: {e}",
            file_name=os.path.basename(file_path),
            error_location=f"line {e.lineno}, column {e.colno}",
        )


def _validate_ai_config_schema(data: dict, file_name: str) -> None:
    """Validate react_ai_config schemaVersion.

    Raises:
        ValueError: If schemaVersion is missing or unsupported.
    """
    version = data.get("schemaVersion")
    if version != "1.0":
        raise ValueError(
            f"Unsupported schemaVersion '{version}' in {file_name}. "
            f"Expected '1.0'. Migration hint: update schemaVersion to '1.0'."
        )


class ReactDefinitionParser:
    """Parses react_*.json files from the application_definitions/ directory into a ReactAppDefinition."""

    @staticmethod
    def parse(react_def_path: str) -> ReactAppDefinition:
        """Parse all React Application Definition files.

        Args:
            react_def_path: Path to the directory containing react_*.json files.

        Returns:
            Populated ReactAppDefinition.

        Raises:
            ReactDefinitionParseError on any validation or parse failure.
        """
        react_def_path = os.path.abspath(react_def_path)

        # 1. Read react_manifest.json
        manifest_path = os.path.join(react_def_path, "react_manifest.json")
        if not os.path.isfile(manifest_path):
            raise ReactDefinitionParseError(
                f"react_manifest.json not found at: {manifest_path}",
                file_name="react_manifest.json",
            )

        manifest_data = _read_json(manifest_path)
        manifest = ReactManifest.model_validate(manifest_data)

        # 2. Track which files are listed in manifest
        listed_files: Set[str] = {"react_manifest.json"}
        result_data: Dict[str, Any] = {"manifest": manifest}

        # 3. Parse each referenced file
        for entry in manifest.files:
            listed_files.add(entry.path)
            file_path = os.path.join(react_def_path, entry.path)

            if not os.path.isfile(file_path):
                raise ReactDefinitionParseError(
                    f"Referenced file not found: {entry.path}",
                    file_name=entry.path,
                )

            # Handle ai_config concern separately (raw dict, not a Pydantic model)
            if entry.concern == "ai_config":
                raw = _read_json(file_path)
                _validate_ai_config_schema(raw, entry.path)
                result_data["react_ai_config"] = raw
                continue

            concern_info = _CONCERN_MAP.get(entry.concern)
            if concern_info is None:
                logger.warning("Unknown concern '%s' for file '%s', skipping.", entry.concern, entry.path)
                continue

            model_cls, field_name, is_list = concern_info
            raw = _read_json(file_path)

            try:
                if is_list:
                    if isinstance(raw, list):
                        parsed = [model_cls.model_validate(item) for item in raw]
                    else:
                        parsed = [model_cls.model_validate(raw)]
                    # Merge with existing (for split page files)
                    existing = result_data.get(field_name, [])
                    result_data[field_name] = existing + parsed
                else:
                    result_data[field_name] = model_cls.model_validate(raw)
            except Exception as e:
                raise ReactDefinitionParseError(
                    f"Error parsing {entry.path} as {entry.concern}: {e}",
                    file_name=entry.path,
                )

        # 4. Support per-entity page files under pages/ subdirectory
        pages_dir = os.path.join(react_def_path, "pages")
        if os.path.isdir(pages_dir):
            for page_file in sorted(os.listdir(pages_dir)):
                if not page_file.endswith(".json"):
                    continue
                listed_files.add(f"pages/{page_file}")
                page_path = os.path.join(pages_dir, page_file)
                raw = _read_json(page_path)
                try:
                    if isinstance(raw, list):
                        pages = [PageDefinition.model_validate(item) for item in raw]
                    else:
                        pages = [PageDefinition.model_validate(raw)]
                    existing = result_data.get("page_definitions", [])
                    result_data["page_definitions"] = existing + pages
                except Exception as e:
                    raise ReactDefinitionParseError(
                        f"Error parsing page file pages/{page_file}: {e}",
                        file_name=f"pages/{page_file}",
                    )

        # 5. Warn about unlisted files in directory
        if os.path.isdir(react_def_path):
            for item in os.listdir(react_def_path):
                if item not in listed_files and item != "pages" and not item.startswith("."):
                    logger.warning("File '%s' exists in directory but is not listed in manifest, ignoring.", item)

        # 6. Build ReactAppDefinition
        react_def = ReactAppDefinition.model_validate(result_data)

        # 7. Validate cross-references
        ReactDefinitionParser._validate_cross_references(react_def)

        return react_def

    @staticmethod
    def _validate_cross_references(react_def: ReactAppDefinition) -> None:
        """Validate cross-references between definition files."""
        # Collect all known entity names from various sources
        known_entities: Set[str] = set()
        for route in react_def.routes:
            known_entities.add(route.entityName)
        for mapping in react_def.component_mappings:
            known_entities.add(mapping.entityName)
        for svc in react_def.api_services:
            known_entities.add(svc.entityName)
        for store in react_def.redux_store:
            known_entities.add(store.entityName)

        # Validate grid area names in page definitions
        for page in react_def.page_definitions:
            # Extract all area names from gridTemplateAreas
            defined_areas: Set[str] = set()
            for row in page.gridTemplate.gridTemplateAreas:
                for area in row.replace('"', "").replace("'", "").split():
                    if area != ".":
                        defined_areas.add(area)

            # Check that each componentPlacement references a defined area
            for placement in page.componentPlacements:
                if placement.gridArea not in defined_areas:
                    raise ReactDefinitionParseError(
                        f"Grid area '{placement.gridArea}' in page '{page.pageId}' "
                        f"is not defined in gridTemplateAreas: {sorted(defined_areas)}",
                        file_name="page_definitions.json",
                        invalid_reference=placement.gridArea,
                    )

        # Validate entity references in page definitions
        if known_entities:
            for page in react_def.page_definitions:
                if page.entityName not in known_entities:
                    raise ReactDefinitionParseError(
                        f"Entity '{page.entityName}' in page '{page.pageId}' "
                        f"is not referenced in any other definition file.",
                        file_name="page_definitions.json",
                        invalid_reference=page.entityName,
                    )

            # Validate entity references in form groupings
            for grouping in react_def.form_groupings:
                for tab in grouping.tabs:
                    if tab.entityName not in known_entities:
                        raise ReactDefinitionParseError(
                            f"Entity '{tab.entityName}' in form grouping '{grouping.groupName}' "
                            f"is not referenced in any other definition file.",
                            file_name="form_groupings.json",
                            invalid_reference=tab.entityName,
                        )
