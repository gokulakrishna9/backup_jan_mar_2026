"""Scaffolder - creates a complete set of definition JSON files for a new application."""

import json
import re
from datetime import date
from pathlib import Path

from app_def_manager.status_tracker import StatusTracker


# Java type → SQL type fallback (mirrors DDLGenerator.JAVA_TO_SQL_FALLBACK)
JAVA_TO_SQL_FALLBACK: dict[str, str] = {
    "Long": "BIGINT UNSIGNED",
    "Integer": "INT",
    "Short": "SMALLINT",
    "Byte": "TINYINT",
    "String": "VARCHAR(255)",
    "Boolean": "BOOLEAN",
    "LocalDate": "DATE",
    "LocalDateTime": "TIMESTAMP",
    "LocalTime": "TIME",
    "BigDecimal": "DECIMAL(19,4)",
    "Float": "FLOAT",
    "Double": "DOUBLE",
    "byte[]": "BLOB",
    "UUID": "VARCHAR(36)",
}

MANIFEST_VERSION = "2.5"

# The 9 definition files the scaffolder writes (excluding _generation_status.json)
DEFINITION_FILES = [
    "webflux_manifest.json",
    "webflux_project_metadata.json",
    "webflux_entity_layer.json",
    "webflux_entities.json",
    "webflux_relationships.json",
    "webflux_repository_layer.json",
    "webflux_service_layer.json",
    "webflux_controller_layer.json",
    "webflux_dto_layer.json",
    "webflux_document_storage_layer.json",
    "webflux_ai_layer.json",
    "react_ai_config.json",
]


def _to_snake_case(name: str) -> str:
    """Convert PascalCase or camelCase to snake_case.

    Examples:
        "UserProfile" → "user_profile"
        "firstName" → "first_name"
        "HTMLParser" → "html_parser"
    """
    # Insert underscore before uppercase letters that follow lowercase/digit,
    # or before a single uppercase followed by lowercase.
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", s)
    return s.lower()


def _to_camel_case(name: str) -> str:
    """Convert snake_case or plain name to camelCase.

    Examples:
        "first_name" → "firstName"
        "title" → "title"
    """
    parts = name.split("_")
    return parts[0].lower() + "".join(p.capitalize() for p in parts[1:])


def _infer_column_definition(java_type: str) -> str:
    """Infer SQL columnDefinition from a Java type using the fallback mapping."""
    return JAVA_TO_SQL_FALLBACK.get(java_type, "VARCHAR(255)")


class Scaffolder:
    """Scaffolds a complete application definition from entity descriptions."""

    def scaffold_application(
        self,
        app_name: str,
        entity_descriptions: list[dict],
        db_name: str | None = None,
        base_package: str = "com.example",
        force: bool = False,
    ) -> Path:
        """Create all definition files for a new application.

        Args:
            app_name: Application name (used as folder name).
            entity_descriptions: List of {"name": str, "fields": [{"name": str, "type": str}]}.
            db_name: Database name (defaults to app_name as snake_case).
            base_package: Java base package name.
            force: If True, overwrite existing directory.

        Returns:
            Path to created application_definitions/<app_name>/ directory.

        Raises:
            FileExistsError: If target directory exists and force is False.
        """
        app_dir = Path("application_definitions") / app_name

        if app_dir.exists() and not force:
            raise FileExistsError(
                f"Directory '{app_dir}' already exists. Use force=True to overwrite."
            )

        app_dir.mkdir(parents=True, exist_ok=True)

        if db_name is None:
            db_name = _to_snake_case(app_name)

        # Generate all definition dicts
        manifest = self._generate_manifest(entity_descriptions)
        project_metadata = self._generate_project_metadata(app_name, db_name, base_package)
        entity_layer = self._generate_entity_layer(entity_descriptions, base_package)
        entities = self._generate_entities(entity_descriptions)
        relationships = self._generate_relationships()
        repository_layer = self._generate_repository_layer(entity_descriptions, base_package)
        service_layer = self._generate_service_layer(entity_descriptions, base_package)
        controller_layer = self._generate_controller_layer(entity_descriptions, base_package)
        dto_layer = self._generate_dto_layer(entity_descriptions, base_package)
        document_storage_layer = {
            "fileStorage": {"enabled": False},
            "jsonColumns": [],
            "documentCollections": [],
            "entityAttachments": [],
        }

        ai_layer = self._generate_ai_layer_default()
        react_ai_config = self._generate_react_ai_config_default()

        # Write all files
        file_data = {
            "webflux_manifest.json": manifest,
            "webflux_project_metadata.json": project_metadata,
            "webflux_entity_layer.json": entity_layer,
            "webflux_entities.json": entities,
            "webflux_relationships.json": relationships,
            "webflux_repository_layer.json": repository_layer,
            "webflux_service_layer.json": service_layer,
            "webflux_controller_layer.json": controller_layer,
            "webflux_dto_layer.json": dto_layer,
            "webflux_document_storage_layer.json": document_storage_layer,
            "webflux_ai_layer.json": ai_layer,
            "react_ai_config.json": react_ai_config,
        }

        for filename, data in file_data.items():
            filepath = app_dir / filename
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

        # Create _generation_status.json with all files marked dirty
        tracker = StatusTracker(app_dir)
        tracker.create_initial_status(list(file_data.keys()))

        return app_dir

    def _generate_manifest(self, entities: list[dict]) -> dict:
        """Generate webflux_manifest.json content."""
        total_entities = len(entities)
        # Count columns: user fields + 3 auto fields per entity
        # (id, created_at, updated_at)
        total_columns = sum(len(e.get("fields", [])) + 3 for e in entities)

        return {
            "version": MANIFEST_VERSION,
            "format": "split",
            "description": "Application definition split into multiple files by layer",
            "files": {
                "project_metadata": "webflux_project_metadata.json",
                "entities": "webflux_entities.json",
                "relationships": "webflux_relationships.json",
                "entity_layer": "webflux_entity_layer.json",
                "repository_layer": "webflux_repository_layer.json",
                "service_layer": "webflux_service_layer.json",
                "controller_layer": "webflux_controller_layer.json",
                "dto_layer": "webflux_dto_layer.json",
                "document_storage_layer": "webflux_document_storage_layer.json",
                "ai_layer": "webflux_ai_layer.json",
            },
            "statistics": {
                "total_entities": total_entities,
                "total_relationships": 0,
                "total_columns": total_columns,
            },
        }

    def _generate_project_metadata(self, app_name: str, db_name: str,
                                    base_package: str) -> dict:
        """Generate webflux_project_metadata.json content."""
        # Derive artifact-style name: snake_case → kebab-case
        kebab_name = app_name.replace("_", "-")
        # Title-case application name
        title_name = " ".join(w.capitalize() for w in app_name.split("_"))

        return {
            "projectMetadata": {
                "name": kebab_name,
                "applicationName": title_name,
                "groupId": base_package,
                "artifactId": kebab_name,
                "version": "1.0.0",
                "port": 8081,
                "sqlFileName": f"{db_name}.sql",
                "dateCreated": date.today().isoformat(),
                "database": {
                    "type": "mysql",
                    "host": "localhost",
                    "port": 3306,
                    "name": db_name,
                    "url": None,
                    "username": "root",
                    "password": "password",
                },
            }
        }

    def _generate_entity_layer(self, entity_descriptions: list[dict],
                                base_package: str) -> dict:
        """Generate webflux_entity_layer.json from entity descriptions."""
        entities = []
        for desc in entity_descriptions:
            entity_name = desc["name"]
            table_name = _to_snake_case(entity_name)

            # Build fields: auto id + user fields + audit + soft-delete
            fields = []

            # Auto-add primary key: {table_name}_id
            fields.append({
                "columnName": f"{table_name}_id",
                "fieldName": f"{_to_camel_case(table_name)}Id",
                "javaType": "Long",
                "isPrimaryKey": True,
                "isNullable": False,
                "columnDefinition": "BIGINT UNSIGNED",
            })

            # User-specified fields
            for field_desc in desc.get("fields", []):
                field_name = field_desc["name"]
                java_type = field_desc.get("type", "String")
                col_name = _to_snake_case(field_name)
                camel_name = _to_camel_case(field_name)

                fields.append({
                    "columnName": col_name,
                    "fieldName": camel_name,
                    "javaType": java_type,
                    "isPrimaryKey": False,
                    "isNullable": True,
                    "columnDefinition": _infer_column_definition(java_type),
                })

            # Auto-add audit fields
            fields.append({
                "columnName": "created_at",
                "fieldName": "createdAt",
                "javaType": "LocalDateTime",
                "isPrimaryKey": False,
                "isNullable": False,
                "columnDefinition": "TIMESTAMP",
            })
            fields.append({
                "columnName": "updated_at",
                "fieldName": "updatedAt",
                "javaType": "LocalDateTime",
                "isPrimaryKey": False,
                "isNullable": False,
                "columnDefinition": "TIMESTAMP",
            })

            entities.append({
                "tableName": table_name,
                "className": entity_name,
                "packageName": f"{base_package}.entity",
                "fields": fields,
                "hasAuditFields": True,
                "hasSoftDelete": False,
            })

        return {
            "layerType": "entity",
            "description": "Entity layer configuration - controls JPA entity generation with R2DBC support",
            "entities": entities,
        }

    def _generate_entities(self, entity_descriptions: list[dict]) -> dict:
        """Generate webflux_entities.json (column-level view)."""
        entities = []
        for desc in entity_descriptions:
            entity_name = desc["name"]
            table_name = _to_snake_case(entity_name)

            columns = []

            # Primary key column
            columns.append({
                "name": f"{table_name}_id",
                "type": "BIGINT UNSIGNED",
                "primaryKey": True,
                "nullable": False,
                "foreignKey": None,
                "unique": False,
                "defaultValue": None,
            })

            # User-specified columns
            for field_desc in desc.get("fields", []):
                field_name = field_desc["name"]
                java_type = field_desc.get("type", "String")
                col_name = _to_snake_case(field_name)

                columns.append({
                    "name": col_name,
                    "type": _infer_column_definition(java_type),
                    "primaryKey": False,
                    "nullable": True,
                    "foreignKey": None,
                    "unique": False,
                    "defaultValue": None,
                })

            # Audit columns
            columns.append({
                "name": "created_at",
                "type": "TIMESTAMP",
                "primaryKey": False,
                "nullable": False,
                "foreignKey": None,
                "unique": False,
                "defaultValue": None,
            })
            columns.append({
                "name": "updated_at",
                "type": "TIMESTAMP",
                "primaryKey": False,
                "nullable": False,
                "foreignKey": None,
                "unique": False,
                "defaultValue": None,
            })

            entities.append({
                "name": table_name,
                "columns": columns,
            })

        return {"entities": entities}

    def _generate_repository_layer(self, entity_descriptions: list[dict],
                                    base_package: str) -> dict:
        """Generate webflux_repository_layer.json with standard CRUD repos."""
        repositories = []
        for desc in entity_descriptions:
            entity_name = desc["name"]
            repositories.append({
                "entityName": entity_name,
                "className": f"{entity_name}Repository",
                "packageName": f"{base_package}.repository",
                "idType": "Long",
                "hasCustomQueries": False,
                "customQueries": [],
                "hasSoftDelete": False,
                "hasAuthorization": False,
                "singleRecordPerUser": False,
                "enableCaching": False,
                "cacheNames": [],
            })

        return {
            "layerType": "repository",
            "description": "Repository layer configuration - controls R2DBC repository generation",
            "repositories": repositories,
        }

    def _generate_service_layer(self, entity_descriptions: list[dict],
                                 base_package: str) -> dict:
        """Generate webflux_service_layer.json with standard CRUD services."""
        services = []
        for i, desc in enumerate(entity_descriptions):
            entity_name = desc["name"]
            services.append({
                "entityName": entity_name,
                "className": f"{entity_name}Service",
                "packageName": f"{base_package}.service",
                "repositoryName": f"{entity_name}Repository",
                "isRootEntity": i == 0,
                "hasAuthorization": False,
                "singleRecordPerUser": False,
                "authorizationConfig": {
                    "checkOnCreate": False,
                    "checkOnRead": False,
                    "checkOnUpdate": False,
                    "checkOnDelete": False,
                    "allowPublicRead": False,
                    "requireOwnership": False,
                },
                "transactionManagement": {
                    "enabled": True,
                    "propagation": "REQUIRED",
                    "isolation": "DEFAULT",
                    "timeout": 30,
                },
                "customMethods": [],
                "validationRules": {
                    "onCreate": [],
                    "onUpdate": [],
                    "onDelete": [],
                },
            })

        return {
            "layerType": "service",
            "description": "Service layer configuration - controls business logic and authorization",
            "services": services,
        }

    def _generate_controller_layer(self, entity_descriptions: list[dict],
                                    base_package: str) -> dict:
        """Generate webflux_controller_layer.json with standard REST endpoints."""
        controllers = []
        for i, desc in enumerate(entity_descriptions):
            entity_name = desc["name"]
            table_name = _to_snake_case(entity_name)
            # basePath: /api/{plural table name}
            base_path = f"/api/{table_name}s"

            controllers.append({
                "entityName": entity_name,
                "className": f"{entity_name}Controller",
                "packageName": f"{base_package}.controller",
                "serviceName": f"{entity_name}Service",
                "basePath": base_path,
                "isRootEntity": i == 0,
                "singleRecordPerUser": False,
                "endpoints": {
                    "create": {
                        "enabled": True,
                        "path": "",
                        "method": "POST",
                        "requiresAuth": False,
                        "roles": [],
                        "rateLimitPerMinute": 10,
                    },
                    "getById": {
                        "enabled": True,
                        "path": "/{id}",
                        "method": "GET",
                        "requiresAuth": False,
                        "roles": [],
                        "rateLimitPerMinute": 60,
                    },
                    "getAll": {
                        "enabled": True,
                        "path": "",
                        "method": "GET",
                        "requiresAuth": False,
                        "roles": [],
                        "rateLimitPerMinute": 30,
                        "defaultPageSize": 20,
                        "supportsPagination": True,
                        "supportsFiltering": True,
                        "supportsSorting": True,
                    },
                    "update": {
                        "enabled": True,
                        "path": "/{id}",
                        "method": "PUT",
                        "requiresAuth": False,
                        "roles": [],
                        "rateLimitPerMinute": 10,
                    },
                    "delete": {
                        "enabled": True,
                        "path": "/{id}",
                        "method": "DELETE",
                        "requiresAuth": False,
                        "roles": [],
                        "rateLimitPerMinute": 5,
                    },
                },
                "customEndpoints": [],
                "corsConfig": {
                    "enabled": True,
                    "allowedOrigins": ["*"],
                    "allowedMethods": ["GET", "POST", "PUT", "DELETE"],
                    "allowedHeaders": ["*"],
                },
            })

        return {
            "layerType": "controller",
            "description": "Controller layer configuration - controls REST endpoint generation",
            "controllers": controllers,
        }

    def _generate_dto_layer(self, entity_descriptions: list[dict],
                             base_package: str) -> dict:
        """Generate webflux_dto_layer.json with Input/Output/Filter DTOs per entity."""
        dtos = []
        for desc in entity_descriptions:
            entity_name = desc["name"]
            user_fields = desc.get("fields", [])

            # Input DTO: user-specified fields only (excludes id, audit, soft-delete)
            input_fields = []
            for field_desc in user_fields:
                field_name = field_desc["name"]
                java_type = field_desc.get("type", "String")
                camel_name = _to_camel_case(field_name)
                input_fields.append({
                    "fieldName": camel_name,
                    "javaType": java_type,
                    "includeInDTO": True,
                })

            dtos.append({
                "entityName": entity_name,
                "dtoType": "Input",
                "className": f"{entity_name}InputDTO",
                "packageName": f"{base_package}.dto",
                "fields": input_fields,
            })

            # Output DTO: all fields (id + user + audit + soft-delete)
            table_name = _to_snake_case(entity_name)
            output_fields = []

            # id field
            output_fields.append({
                "fieldName": f"{_to_camel_case(table_name)}Id",
                "javaType": "Long",
                "includeInDTO": True,
            })

            # user fields
            for field_desc in user_fields:
                field_name = field_desc["name"]
                java_type = field_desc.get("type", "String")
                camel_name = _to_camel_case(field_name)
                output_fields.append({
                    "fieldName": camel_name,
                    "javaType": java_type,
                    "includeInDTO": True,
                })

            # audit + soft-delete
            output_fields.append({"fieldName": "createdAt", "javaType": "LocalDateTime", "includeInDTO": True})
            output_fields.append({"fieldName": "updatedAt", "javaType": "LocalDateTime", "includeInDTO": True})

            dtos.append({
                "entityName": entity_name,
                "dtoType": "Output",
                "className": f"{entity_name}OutputDTO",
                "packageName": f"{base_package}.dto",
                "fields": output_fields,
            })

            # Filter DTO: filterable user fields (typically all user fields)
            filter_fields = []
            for field_desc in user_fields:
                field_name = field_desc["name"]
                java_type = field_desc.get("type", "String")
                camel_name = _to_camel_case(field_name)
                filter_fields.append({
                    "fieldName": camel_name,
                    "javaType": java_type,
                    "includeInDTO": True,
                })

            dtos.append({
                "entityName": entity_name,
                "dtoType": "Filter",
                "className": f"{entity_name}FilterDTO",
                "packageName": f"{base_package}.dto",
                "fields": filter_fields,
            })

        return {
            "layerType": "dto",
            "description": "DTO layer configuration - controls Data Transfer Object generation with validation",
            "dtos": dtos,
        }

    def _generate_relationships(self) -> dict:
        """Generate empty webflux_relationships.json."""
        return {"relationships": []}

    def _generate_ai_layer_default(self) -> dict:
        """Generate default webflux_ai_layer.json with empty structure."""
        return {
            "schemaVersion": "1.0",
            "providers": [],
            "entityCapabilities": [],
            "standaloneOperations": [],
            "promptTemplates": [],
            "assistants": [],
            "ragSources": [],
            "evaluators": [],
            "vectorStore": None,
            "documentIngestion": None,
            "documentProcessing": None,
            "orchestrator": None,
            "mcpServers": [],
            "observability": None,
            "rateLimiting": None,
            "tokenBudget": None,
            "chatSessionCleanup": None,
            "auditLog": None,
        }

    def _generate_react_ai_config_default(self) -> dict:
        """Generate default react_ai_config.json with all features disabled."""
        return {
            "schemaVersion": "1.0",
            "chatPanel": {
                "enabled": False,
                "position": "sidebar",
                "defaultAssistant": "",
                "showOnPages": [],
                "streamingEnabled": True,
            },
            "entityFeatures": [],
            "standaloneFeatures": [],
            "theme": {
                "accentColor": "#6366f1",
                "chatBubbleStyle": "rounded",
                "loadingAnimation": "dots",
            },
            "evaluationDisplay": None,
            "ragFeatures": None,
        }
