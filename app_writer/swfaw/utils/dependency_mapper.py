"""Dependency mapper for incremental code generation.

Maps dirty definition files to the specific generated output files that
need regeneration, enabling targeted incremental builds instead of full
project regeneration.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from swfaw.utils.definition_loader import DefinitionBundle


@dataclass
class AffectedOutputs:
    """Describes which generated files need regeneration."""

    regenerate_sql: bool = False
    affected_entities: set[str] = field(default_factory=set)  # entity classNames
    affected_file_types: dict[str, set[str]] = field(default_factory=dict)
    # e.g. {"User": {"entity", "dto_input", "repository", "service", "controller"}}


# Definition files that are scoped to individual entities.
# When these are dirty, ALL entities are marked affected for the
# corresponding file types (simplified — no per-entity diffing).
_ENTITY_SCOPED_FILES = {
    "webflux_entity_layer.json",
    "webflux_entities.json",
    "webflux_relationships.json",
    "webflux_repository_layer.json",
    "webflux_service_layer.json",
    "webflux_controller_layer.json",
    "webflux_dto_layer.json",
    "webflux_query_layer.json",
    "webflux_filter_layer.json",
    "webflux_custom_queries_layer.json",
    "webflux_authorization_layer.json",
    "webflux_audit_logging_layer.json",
    "webflux_document_storage_layer.json",
    "webflux_ai_layer.json",
}

# Definition files that are global (not entity-scoped).
# When these are dirty, ALL entities are marked affected.
_GLOBAL_FILES = {
    "webflux_security_layer.json",
    "webflux_config_layer.json",
    "webflux_project_metadata.json",
    "webflux_exception_layer.json",
}


class DependencyMapper:
    """Maps dirty definition files to affected generated output files."""

    # Definition file → which generated file types are affected
    DEPENDENCY_MAP: dict[str, list[str]] = {
        "webflux_entity_layer.json": [
            "entity", "dto_input", "dto_output", "dto_filter",
            "repository", "service", "controller", "sql",
        ],
        "webflux_entities.json": ["entity", "sql"],
        "webflux_relationships.json": ["entity", "repository", "sql"],
        "webflux_repository_layer.json": ["repository"],
        "webflux_service_layer.json": ["service"],
        "webflux_controller_layer.json": ["controller"],
        "webflux_dto_layer.json": ["dto_input", "dto_output", "dto_filter"],
        "webflux_query_layer.json": ["repository", "service", "controller"],
        "webflux_filter_layer.json": ["dto_filter", "controller"],
        "webflux_custom_queries_layer.json": ["repository"],
        "webflux_security_layer.json": ["security_config"],
        "webflux_config_layer.json": ["config"],
        "webflux_authorization_layer.json": ["service", "controller"],
        "webflux_audit_logging_layer.json": ["service"],
        "webflux_exception_layer.json": ["exception"],
        "webflux_project_metadata.json": ["config", "pom", "sql"],
        "webflux_document_storage_layer.json": ["file_storage", "json_converter", "document_collection", "sql"],
        "webflux_ai_layer.json": [
            "ai_service", "ai_controller", "ai_entity", "ai_config",
            "ai_dto", "ai_repository", "ai_provider", "ai_rag",
            "ai_evaluator", "ai_ingestion", "ai_processing",
            "ai_vectorstore", "ai_orchestrator", "ai_tools", "ai_mcp",
            "ai_observability", "ai_budget", "ai_audit", "sql",
        ],
    }

    # Files whose dirtiness triggers SQL regeneration
    _SQL_TRIGGER_FILES = {
        "webflux_entity_layer.json",
        "webflux_entities.json",
        "webflux_relationships.json",
        "webflux_project_metadata.json",
        "webflux_document_storage_layer.json",
        "webflux_ai_layer.json",
    }

    def _get_all_entity_names(self, bundle: DefinitionBundle) -> set[str]:
        """Extract all entity classNames from the bundle's entity_layer."""
        entities = bundle.entity_layer.get("entities", [])
        return {e["className"] for e in entities if "className" in e}

    def resolve_affected_outputs(
        self,
        dirty_files: list[str],
        bundle: DefinitionBundle,
    ) -> AffectedOutputs:
        """Determine which generated files need regeneration.

        For each dirty file, looks up DEPENDENCY_MAP to get affected file
        types.  Sets ``regenerate_sql = True`` when entity_layer, entities,
        relationships, or project_metadata are dirty.

        Simplified approach: when any entity-scoped or global file is dirty,
        ALL entities are marked affected for the corresponding file types
        (no per-entity diffing).

        Args:
            dirty_files: Filenames of dirty definition files.
            bundle: The loaded DefinitionBundle (used to enumerate entities).

        Returns:
            An ``AffectedOutputs`` describing what needs regeneration.
        """
        result = AffectedOutputs()
        all_entities = self._get_all_entity_names(bundle)

        for dirty_file in dirty_files:
            file_types = self.DEPENDENCY_MAP.get(dirty_file, [])
            if not file_types:
                continue

            # Check SQL trigger
            if dirty_file in self._SQL_TRIGGER_FILES:
                result.regenerate_sql = True

            # Filter out "sql" — it's handled via regenerate_sql flag
            code_types = {ft for ft in file_types if ft != "sql"}
            if not code_types:
                continue

            # Both entity-scoped and global files mark ALL entities
            # affected for the resolved file types.
            result.affected_entities.update(all_entities)
            for entity_name in all_entities:
                existing = result.affected_file_types.get(entity_name, set())
                existing.update(code_types)
                result.affected_file_types[entity_name] = existing

        return result

    @staticmethod
    def get_generated_file_paths(
        entity_name: str,
        file_type: str,
        dirs: dict[str, Path],
        package_name: str,
    ) -> list[Path]:
        """Return actual file paths for a given entity + file type.

        Args:
            entity_name: The entity className (e.g. ``"User"``).
            file_type: One of the generated file type keys
                (``"entity"``, ``"dto_input"``, ``"dto_output"``,
                ``"dto_filter"``, ``"repository"``, ``"service"``,
                ``"controller"``).
            dirs: Mapping of directory keys to ``Path`` objects, e.g.
                ``{"entity": Path(...), "dto": Path(...), ...}``.
            package_name: Java package name (currently unused but
                reserved for future package-path resolution).

        Returns:
            A list containing the resolved ``Path`` (single element).
            Empty list if *file_type* is not recognised.
        """
        _FILE_TYPE_MAP: dict[str, tuple[str, str]] = {
            "entity": ("entity", f"{entity_name}.java"),
            "dto_input": ("dto", f"{entity_name}InputDTO.java"),
            "dto_output": ("dto", f"{entity_name}OutputDTO.java"),
            "dto_filter": ("dto", f"{entity_name}FilterDTO.java"),
            "repository": ("repository", f"{entity_name}Repository.java"),
            "service": ("service", f"{entity_name}Service.java"),
            "controller": ("controller", f"{entity_name}Controller.java"),
        }

        mapping = _FILE_TYPE_MAP.get(file_type)
        if mapping is None:
            return []

        dir_key, filename = mapping
        target_dir = dirs.get(dir_key)
        if target_dir is None:
            return []

        return [Path(target_dir) / filename]
