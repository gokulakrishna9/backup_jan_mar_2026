"""Parser for swfaw application definition files (Phase 1 input).

Reads the application_definitions/ folder produced by swfaw_v2 Phase 1
and produces an AppDefinition model containing all parsed layer data.
"""

import json
import os
from typing import Any, Dict

from models.definition_models import (
    AppDefinition,
    AuditLayerDef,
    AuthorizationLayerDef,
    ConfigLayerDef,
    ControllerLayerDef,
    CustomQueriesLayerDef,
    DtoLayerDef,
    EntitiesDef,
    EntityLayerDef,
    ExceptionLayerDef,
    FilterLayerDef,
    GroupDefinitionLayerDef,
    ManifestDef,
    ProjectMetadataDef,
    QueryLayerDef,
    RelationshipsDef,
    RepositoryLayerDef,
    SecurityLayerDef,
    ServiceLayerDef,
)


class DefinitionParseError(Exception):
    """Raised when parsing an application definition file fails."""

    def __init__(self, message: str, file_name: str = "", location: str = ""):
        self.file_name = file_name
        self.location = location
        super().__init__(message)


# Mapping from manifest key → (Pydantic model class, is_required)
_LAYER_MAP = {
    "project_metadata": (ProjectMetadataDef, True),
    "entities": (EntitiesDef, True),
    "relationships": (RelationshipsDef, True),
    "entity_layer": (EntityLayerDef, True),
    "repository_layer": (RepositoryLayerDef, True),
    "service_layer": (ServiceLayerDef, True),
    "controller_layer": (ControllerLayerDef, True),
    "dto_layer": (DtoLayerDef, True),
    "query_layer": (QueryLayerDef, True),
    "filter_layer": (FilterLayerDef, True),
    "group_definition_layer": (GroupDefinitionLayerDef, True),
}

# Files that exist on disk but may not be listed in manifest.files
_EXTRA_LAYERS = {
    "security_layer": (SecurityLayerDef, "webflux_security_layer.json"),
    "config_layer": (ConfigLayerDef, "webflux_config_layer.json"),
    "exception_layer": (ExceptionLayerDef, "webflux_exception_layer.json"),
    "authorization_layer": (AuthorizationLayerDef, "webflux_authorization_layer.json"),
    "audit_layer": (AuditLayerDef, "webflux_audit_logging_layer.json"),
    "custom_queries_layer": (CustomQueriesLayerDef, "webflux_custom_queries_layer.json"),
}


class DefinitionParser:
    """Reads and parses swfaw application definition files."""

    @staticmethod
    def parse(app_def_path: str) -> AppDefinition:
        """Parse all swfaw application definition files into an AppDefinition.

        Args:
            app_def_path: Path to the application_definitions/ folder.

        Returns:
            Populated AppDefinition model.

        Raises:
            DefinitionParseError: On missing files, malformed JSON, or validation errors.
        """
        app_def_path = os.path.abspath(app_def_path)

        if not os.path.isdir(app_def_path):
            raise DefinitionParseError(
                f"Application definitions folder not found: {app_def_path}",
                file_name=app_def_path,
            )

        # 1. Read webflux_manifest.json
        manifest_path = os.path.join(app_def_path, "webflux_manifest.json")
        manifest_data = DefinitionParser._read_json(manifest_path, "webflux_manifest.json")
        manifest = ManifestDef(**manifest_data)

        # 2. Parse all files listed in manifest
        parsed: Dict[str, Any] = {"manifest": manifest}

        for layer_key, (model_cls, required) in _LAYER_MAP.items():
            file_name = manifest.files.get(layer_key)
            if not file_name:
                if required:
                    raise DefinitionParseError(
                        f"Required layer '{layer_key}' not found in webflux_manifest.json",
                        file_name="webflux_manifest.json",
                    )
                continue
            file_path = os.path.join(app_def_path, file_name)
            data = DefinitionParser._read_json(file_path, file_name)
            parsed[layer_key] = model_cls(**data)

        # 3. Parse extra layers (not always in manifest but exist on disk)
        for attr_name, (model_cls, default_file) in _EXTRA_LAYERS.items():
            if attr_name in parsed:
                continue
            # Check if listed in manifest under a different key
            file_name = manifest.files.get(attr_name, default_file)
            file_path = os.path.join(app_def_path, file_name)
            if os.path.isfile(file_path):
                data = DefinitionParser._read_json(file_path, file_name)
                parsed[attr_name] = model_cls(**data)
            else:
                # Use empty defaults
                parsed[attr_name] = model_cls()

        return AppDefinition(**parsed)

    @staticmethod
    def serialize(app_def: AppDefinition, output_dir: str) -> None:
        """Serialize an AppDefinition back to JSON files with 2-space indentation.

        Args:
            app_def: The AppDefinition to serialize.
            output_dir: Directory to write the JSON files to.
        """
        os.makedirs(output_dir, exist_ok=True)

        def _write(filename: str, data):
            path = os.path.join(output_dir, filename)
            if hasattr(data, "model_dump"):
                obj = data.model_dump(by_alias=True, exclude_none=False)
            else:
                obj = data
            with open(path, "w", encoding="utf-8") as f:
                json.dump(obj, f, indent=2, ensure_ascii=False)
                f.write("\n")

        _write("webflux_manifest.json", app_def.manifest)
        _write("webflux_project_metadata.json", app_def.project_metadata)
        _write("webflux_entities.json", app_def.entities)
        _write("webflux_relationships.json", app_def.relationships)
        _write("webflux_entity_layer.json", app_def.entity_layer)
        _write("webflux_repository_layer.json", app_def.repository_layer)
        _write("webflux_service_layer.json", app_def.service_layer)
        _write("webflux_controller_layer.json", app_def.controller_layer)
        _write("webflux_dto_layer.json", app_def.dto_layer)
        _write("webflux_query_layer.json", app_def.query_layer)
        _write("webflux_filter_layer.json", app_def.filter_layer)
        _write("webflux_security_layer.json", app_def.security_layer)
        _write("webflux_config_layer.json", app_def.config_layer)
        _write("webflux_exception_layer.json", app_def.exception_layer)
        _write("webflux_authorization_layer.json", app_def.authorization_layer)
        _write("webflux_audit_logging_layer.json", app_def.audit_layer)
        _write("webflux_group_definition_layer.json", app_def.group_definition_layer)
        if app_def.custom_queries_layer:
            _write("webflux_custom_queries_layer.json", app_def.custom_queries_layer)

    @staticmethod
    def _read_json(file_path: str, file_name: str) -> dict:
        """Read and parse a JSON file.

        Raises:
            DefinitionParseError: If file is missing or contains malformed JSON.
        """
        if not os.path.isfile(file_path):
            raise DefinitionParseError(
                f"Required file not found: {file_name}",
                file_name=file_name,
            )
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise DefinitionParseError(
                f"Malformed JSON in {file_name}: {e.msg} at line {e.lineno}, column {e.colno}",
                file_name=file_name,
                location=f"line {e.lineno}, column {e.colno}",
            ) from e
