"""Incremental code generator for definition-first pipeline.

Regenerates only the affected generated files for specific entities,
rather than the entire project. Mirrors the logic in
generate_from_layer_definitions() from main.py but processes only
entities and file types identified by DependencyMapper.
"""

from __future__ import annotations

from pathlib import Path

from generators.entity_generator import EntityGenerator
from generators.dto_generator import DTOGenerator
from generators.repository_generator import RepositoryGenerator
from generators.service_generator import ServiceGenerator
from generators.controller_generator import ControllerGenerator
from models.layer_objects import (
    EntityLayerObject, Field, DTOLayerObject,
    RepositoryLayerObject, ServiceLayerObject, ControllerLayerObject,
)
from utils.file_writer import create_directory_structure, write_file
from utils.dependency_mapper import AffectedOutputs
from utils.definition_loader import DefinitionBundle


class IncrementalGenerator:
    """Regenerates only affected files based on dirty definition changes."""

    def regenerate_affected(
        self,
        bundle: DefinitionBundle,
        affected: AffectedOutputs,
        output_dir: Path,
    ) -> list[Path]:
        """Regenerate only the files identified by AffectedOutputs.

        Args:
            bundle: The loaded DefinitionBundle with all definition data.
            affected: AffectedOutputs describing which entities/file types
                need regeneration.
            output_dir: Root output directory (e.g. generated_application/<app>).

        Returns:
            List of all regenerated file paths.
        """
        output_dir = Path(output_dir)
        code_dir = output_dir / "webflux_app"
        package_name = bundle.project_metadata["projectMetadata"]["groupId"]

        # Reconstruct dirs dict (mkdir exist_ok=True is safe on existing dirs)
        dirs = create_directory_structure(str(code_dir), package_name)

        # Build lookup dicts from bundle layers
        entity_defs = bundle.entity_layer["entities"]
        repo_defs = bundle.repository_layer["repositories"]
        service_defs = bundle.service_layer["services"]
        controller_defs = bundle.controller_layer["controllers"]
        dto_defs = bundle.dto_layer["dtos"]

        entity_lookup = {e["className"]: e for e in entity_defs}
        repo_lookup = {r["entityName"]: r for r in repo_defs}
        service_lookup = {s["entityName"]: s for s in service_defs}
        controller_lookup = {c["entityName"]: c for c in controller_defs}

        # Group DTOs by entity name
        dto_lookup: dict[str, dict[str, dict]] = {}
        for dto_def in dto_defs:
            entity_name = dto_def["entityName"]
            if entity_name not in dto_lookup:
                dto_lookup[entity_name] = {}
            dto_lookup[entity_name][dto_def["dtoType"]] = dto_def

        regenerated: list[Path] = []

        for entity_name in affected.affected_entities:
            entity_def = entity_lookup.get(entity_name)
            if entity_def is None:
                continue

            file_types = affected.affected_file_types.get(entity_name, set())

            if "entity" in file_types:
                path = self._regenerate_entity(entity_def, dirs)
                regenerated.append(path)

            dto_types_needed = file_types & {"dto_input", "dto_output", "dto_filter"}
            if dto_types_needed and entity_name in dto_lookup:
                paths = self._regenerate_dtos(
                    entity_name, dto_lookup[entity_name],
                    entity_def, dirs, dto_types_needed,
                )
                regenerated.extend(paths)

            if "repository" in file_types and entity_name in repo_lookup:
                path = self._regenerate_repository(repo_lookup[entity_name], entity_def, dirs)
                regenerated.append(path)

            if "service" in file_types and entity_name in service_lookup:
                path = self._regenerate_service(
                    service_lookup[entity_name], entity_def, dirs,
                )
                regenerated.append(path)

            if "controller" in file_types and entity_name in controller_lookup:
                path = self._regenerate_controller(
                    controller_lookup[entity_name],
                    service_lookup.get(entity_name, {}),
                    dirs,
                )
                regenerated.append(path)

        # Check for document storage file types (global, not per-entity)
        all_affected_types = set()
        for types in affected.affected_file_types.values():
            all_affected_types.update(types)

        if "file_storage" in all_affected_types:
            regenerated.extend(self._regenerate_file_storage(bundle, dirs, package_name))

        if "json_converter" in all_affected_types or "document_collection" in all_affected_types:
            regenerated.extend(self._regenerate_json_columns(bundle, dirs, package_name))

        return regenerated

    # ------------------------------------------------------------------
    # Per-type regeneration helpers (mirror main.py patterns exactly)
    # ------------------------------------------------------------------

    def _regenerate_entity(self, entity_def: dict, dirs: dict) -> Path:
        """Regenerate a single Entity.java file."""
        fields = [Field(**f) for f in entity_def["fields"]]
        entity = EntityLayerObject(
            tableName=entity_def["tableName"],
            className=entity_def["className"],
            packageName=entity_def["packageName"],
            fields=fields,
            isRootEntity=entity_def.get("isRootEntity", False),
            parentEntity=entity_def.get("parentEntity"),
            hasPublicFlag=entity_def.get("hasPublicFlag", False),
            hasAuditFields=entity_def.get("hasAuditFields", True),
            hasSoftDelete=entity_def.get("hasSoftDelete", True),
            relationships=entity_def.get("relationships", []),
        )
        code = EntityGenerator.generate(entity)
        path = dirs["entity"] / f"{entity.className}.java"
        write_file(path, code)
        return path

    def _regenerate_dtos(
        self,
        entity_name: str,
        dto_defs: dict[str, dict],
        entity_def: dict,
        dirs: dict,
        file_types: set[str],
    ) -> list[Path]:
        """Regenerate DTO files for a single entity.

        Only regenerates the DTO types whose file_type key is in
        *file_types* (e.g. ``{"dto_input", "dto_output"}``).
        """
        _TYPE_MAP = {
            "dto_input": "Input",
            "dto_output": "Output",
            "dto_filter": "Filter",
        }
        paths: list[Path] = []

        for file_type_key, dto_type in _TYPE_MAP.items():
            if file_type_key not in file_types:
                continue
            if dto_type not in dto_defs:
                continue

            dto_def = dto_defs[dto_type]

            # Add columnName to DTO fields (same as fieldName for DTOs)
            dto_fields = []
            for field_def in dto_def["fields"]:
                fd = dict(field_def)  # shallow copy to avoid mutating bundle
                if "columnName" not in fd:
                    fd["columnName"] = fd["fieldName"]
                dto_fields.append(Field(**fd))

            dto = DTOLayerObject(
                entityName=dto_def["entityName"],
                className=dto_def["className"],
                packageName=dto_def["packageName"],
                fields=dto_fields,
                dtoType=dto_def["dtoType"],
                isRootEntity=entity_def.get("isRootEntity", False),
                fieldConfigs=dto_def.get("fields", []),
                customValidators=dto_def.get("customValidators", []),
                excludeSensitiveFields=dto_def.get("excludeSensitiveFields", []),
                includeRelationships=dto_def.get("includeRelationships", False),
            )
            code = DTOGenerator.generate(dto)
            path = dirs["dto"] / f"{dto.className}.java"
            write_file(path, code)
            paths.append(path)

        return paths

    def _regenerate_repository(self, repo_def: dict, entity_def: dict, dirs: dict) -> Path:
        """Regenerate a single Repository.java file."""
        repository = RepositoryLayerObject(
            entityName=repo_def["entityName"],
            className=repo_def["className"],
            packageName=repo_def["packageName"],
            idType=repo_def["idType"],
            hasCustomQueries=repo_def.get("hasCustomQueries", False),
            customQueries=repo_def.get("customQueries", []),
            hasSoftDelete=repo_def.get("hasSoftDelete", False),
            hasAuthorization=repo_def.get("hasAuthorization", False),
            singleRecordPerUser=repo_def.get("singleRecordPerUser", False),
            tableName=entity_def.get("tableName"),
            idColumn=next((f["columnName"] for f in entity_def.get("fields", []) if f.get("isPrimaryKey")), None),
        )
        code = RepositoryGenerator.generate(repository)
        path = dirs["repository"] / f"{repository.className}.java"
        write_file(path, code)
        return path

    def _regenerate_service(
        self, service_def: dict, entity_def: dict, dirs: dict,
    ) -> Path:
        """Regenerate a single Service.java file."""
        # Reconstruct entity object (ServiceGenerator.generate needs it)
        fields = [Field(**f) for f in entity_def["fields"]]
        entity = EntityLayerObject(
            tableName=entity_def["tableName"],
            className=entity_def["className"],
            packageName=entity_def["packageName"],
            fields=fields,
            isRootEntity=entity_def.get("isRootEntity", False),
            parentEntity=entity_def.get("parentEntity"),
            hasPublicFlag=entity_def.get("hasPublicFlag", False),
            hasAuditFields=entity_def.get("hasAuditFields", True),
            hasSoftDelete=entity_def.get("hasSoftDelete", True),
            relationships=entity_def.get("relationships", []),
        )

        service = ServiceLayerObject(
            entityName=service_def["entityName"],
            className=service_def["className"],
            packageName=service_def["packageName"],
            repositoryName=service_def["repositoryName"],
            isRootEntity=service_def["isRootEntity"],
            hasAuthorization=service_def.get("hasAuthorization", False),
            singleRecordPerUser=service_def.get("singleRecordPerUser", False),
        )
        code = ServiceGenerator.generate(service, entity)
        path = dirs["service"] / f"{service.className}.java"
        write_file(path, code)
        return path

    def _regenerate_controller(
        self, controller_def: dict, service_def: dict, dirs: dict,
    ) -> Path:
        """Regenerate a single Controller.java file."""
        controller = ControllerLayerObject(
            entityName=controller_def["entityName"],
            className=controller_def["className"],
            packageName=controller_def["packageName"],
            serviceName=controller_def["serviceName"],
            basePath=controller_def["basePath"],
            isRootEntity=controller_def["isRootEntity"],
            endpoints=controller_def.get("endpoints", {}),
            customEndpoints=controller_def.get("customEndpoints", []),
            corsConfig=controller_def.get("corsConfig", {}),
            singleRecordPerUser=controller_def.get("singleRecordPerUser", False),
        )
        code = ControllerGenerator.generate(
            controller,
            has_authorization=service_def.get("hasAuthorization", False),
        )
        path = dirs["controller"] / f"{controller.className}.java"
        write_file(path, code)
        return path


    def _regenerate_file_storage(
        self, bundle: DefinitionBundle, dirs: dict, package_name: str,
    ) -> list[Path]:
        """Regenerate file storage Java files."""
        if bundle.document_storage_layer is None:
            return []
        from generators.file_storage_generator import FileStorageGenerator
        return FileStorageGenerator.generate(
            bundle.document_storage_layer, bundle.entity_layer, package_name, dirs
        )

    def _regenerate_json_columns(
        self, bundle: DefinitionBundle, dirs: dict, package_name: str,
    ) -> list[Path]:
        """Regenerate JSON column converter and document collection files."""
        if bundle.document_storage_layer is None:
            return []
        from generators.json_column_generator import JsonColumnGenerator
        return JsonColumnGenerator.generate(
            bundle.document_storage_layer, bundle.entity_layer, package_name, dirs
        )

