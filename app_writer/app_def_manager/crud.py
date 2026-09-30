"""CRUDManager - granular CRUD operations on definition components with cross-layer consistency."""

from pathlib import Path

from definition_editor.editor import DefinitionEditor
from app_def_manager.status_tracker import StatusTracker
from app_def_manager.scaffolder import _to_snake_case, _to_camel_case, _infer_column_definition


# The 6 layer files that entity-level operations touch
ENTITY_LAYER_FILES = [
    "webflux_entity_layer.json",
    "webflux_entities.json",
    "webflux_repository_layer.json",
    "webflux_service_layer.json",
    "webflux_controller_layer.json",
    "webflux_dto_layer.json",
]

# The 3 files that field-level operations touch
FIELD_LAYER_FILES = [
    "webflux_entity_layer.json",
    "webflux_entities.json",
    "webflux_dto_layer.json",
]

# Document storage layer file
DSL_FILE = "webflux_document_storage_layer.json"

# Valid fieldWidget values for DTO fields
VALID_FIELD_WIDGETS = {"text", "richText", "codeEditor", "markdown", "json"}


class CRUDManager:
    """CRUD operations on definition components with cross-layer consistency."""

    def __init__(self, app_name: str):
        self.app_dir = Path("application_definitions") / app_name
        self.editor = DefinitionEditor(str(self.app_dir))
        self.status = StatusTracker(self.app_dir)

    # ── Entity operations ───────────────────────────────────────────────

    def add_entity(self, name: str, fields: list[dict]) -> list[str]:
        """Add entity across all 6 layers. Returns list of dirty filenames.

        Args:
            name: PascalCase entity class name (e.g. "Product").
            fields: List of {"name": str, "type": str} field descriptions.

        Raises:
            ValueError: If an entity with the same className already exists.
        """
        # Check for duplicate
        existing = self.editor.find("webflux_entity_layer.json", "entities", {"className": name})
        if existing is not None:
            raise ValueError(f"Entity '{name}' already exists in entity_layer")

        table_name = _to_snake_case(name)
        base_package = self._get_base_package()

        # Build entity_layer entry
        entity_fields = self._build_entity_fields(table_name, fields)
        entity_def = {
            "tableName": table_name,
            "className": name,
            "packageName": f"{base_package}.entity",
            "fields": entity_fields,
            "hasAuditFields": True,
            "hasSoftDelete": False,
        }
        self.editor.append("webflux_entity_layer.json", "entities", entity_def)

        # Build entities entry (column-level view)
        columns = self._build_entity_columns(table_name, fields)
        entities_entry = {"name": table_name, "columns": columns}
        self.editor.append("webflux_entities.json", "entities", entities_entry)

        # Build repository_layer entry
        repo_def = {
            "entityName": name,
            "className": f"{name}Repository",
            "packageName": f"{base_package}.repository",
            "idType": "Long",
            "hasCustomQueries": False,
            "customQueries": [],
            "hasSoftDelete": False,
            "hasAuthorization": False,
            "singleRecordPerUser": False,
            "enableCaching": False,
            "cacheNames": [],
        }
        self.editor.append("webflux_repository_layer.json", "repositories", repo_def)

        # Build service_layer entry
        service_def = {
            "entityName": name,
            "className": f"{name}Service",
            "packageName": f"{base_package}.service",
            "repositoryName": f"{name}Repository",
            "isRootEntity": False,
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
            "validationRules": {"onCreate": [], "onUpdate": [], "onDelete": []},
        }
        self.editor.append("webflux_service_layer.json", "services", service_def)

        # Build controller_layer entry
        base_path = f"/api/{table_name}s"
        controller_def = {
            "entityName": name,
            "className": f"{name}Controller",
            "packageName": f"{base_package}.controller",
            "serviceName": f"{name}Service",
            "basePath": base_path,
            "isRootEntity": False,
            "singleRecordPerUser": False,
            "endpoints": {
                "create": {
                    "enabled": True, "path": "", "method": "POST",
                    "requiresAuth": False, "roles": [], "rateLimitPerMinute": 10,
                },
                "getById": {
                    "enabled": True, "path": "/{id}", "method": "GET",
                    "requiresAuth": False, "roles": [], "rateLimitPerMinute": 60,
                },
                "getAll": {
                    "enabled": True, "path": "", "method": "GET",
                    "requiresAuth": False, "roles": [], "rateLimitPerMinute": 30,
                    "defaultPageSize": 20, "supportsPagination": True,
                    "supportsFiltering": True, "supportsSorting": True,
                },
                "update": {
                    "enabled": True, "path": "/{id}", "method": "PUT",
                    "requiresAuth": False, "roles": [], "rateLimitPerMinute": 10,
                },
                "delete": {
                    "enabled": True, "path": "/{id}", "method": "DELETE",
                    "requiresAuth": False, "roles": [], "rateLimitPerMinute": 5,
                },
            },
            "customEndpoints": [],
            "corsConfig": {
                "enabled": True,
                "allowedOrigins": ["*"],
                "allowedMethods": ["GET", "POST", "PUT", "DELETE"],
                "allowedHeaders": ["*"],
            },
        }
        self.editor.append("webflux_controller_layer.json", "controllers", controller_def)

        # Build dto_layer entries (Input, Output, Filter)
        self._append_dtos_for_entity(name, table_name, fields, base_package)

        # Mark all 6 files dirty
        dirty = list(ENTITY_LAYER_FILES)
        self.status.mark_dirty(dirty)
        return dirty

    def remove_entity(self, name: str) -> list[str]:
        """Remove entity from all 6 layers. Returns list of dirty filenames."""
        table_name = _to_snake_case(name)

        # entity_layer: filter out entity by className
        entities = self.editor.get("webflux_entity_layer.json", "entities")
        filtered = [e for e in entities if e.get("className") != name]
        self.editor.set("webflux_entity_layer.json", "entities", filtered)

        # entities: filter out by table name
        ent_list = self.editor.get("webflux_entities.json", "entities")
        filtered = [e for e in ent_list if e.get("name") != table_name]
        self.editor.set("webflux_entities.json", "entities", filtered)

        # repository_layer
        repos = self.editor.get("webflux_repository_layer.json", "repositories")
        filtered = [r for r in repos if r.get("entityName") != name]
        self.editor.set("webflux_repository_layer.json", "repositories", filtered)

        # service_layer
        services = self.editor.get("webflux_service_layer.json", "services")
        filtered = [s for s in services if s.get("entityName") != name]
        self.editor.set("webflux_service_layer.json", "services", filtered)

        # controller_layer
        controllers = self.editor.get("webflux_controller_layer.json", "controllers")
        filtered = [c for c in controllers if c.get("entityName") != name]
        self.editor.set("webflux_controller_layer.json", "controllers", filtered)

        # dto_layer: remove all DTOs for this entity
        dtos = self.editor.get("webflux_dto_layer.json", "dtos")
        filtered = [d for d in dtos if d.get("entityName") != name]
        self.editor.set("webflux_dto_layer.json", "dtos", filtered)

        dirty = list(ENTITY_LAYER_FILES)
        self.status.mark_dirty(dirty)
        return dirty

    # ── Field operations ────────────────────────────────────────────────

    def add_field(self, entity_name: str, field: dict) -> list[str]:
        """Add field to entity_layer, entities, and dto_layer. Returns dirty files.

        Args:
            entity_name: PascalCase entity class name.
            field: {"name": str, "type": str} field description.
        """
        table_name = _to_snake_case(entity_name)
        field_name = field["name"]
        java_type = field.get("type", "String")
        col_name = _to_snake_case(field_name)
        camel_name = _to_camel_case(field_name)

        # Validate fieldWidget if present
        field_widget = field.get("fieldWidget")
        if field_widget and field_widget not in VALID_FIELD_WIDGETS:
            raise ValueError(
                f"Invalid fieldWidget '{field_widget}'. "
                f"Allowed values: {sorted(VALID_FIELD_WIDGETS)}"
            )

        # entity_layer: find entity, append field before audit fields
        el_entities = self.editor.get("webflux_entity_layer.json", "entities")
        for entity in el_entities:
            if entity.get("className") == entity_name:
                new_field = {
                    "columnName": col_name,
                    "fieldName": camel_name,
                    "javaType": java_type,
                    "isPrimaryKey": False,
                    "isNullable": True,
                    "columnDefinition": _infer_column_definition(java_type),
                }
                # Insert before audit fields (created_at is typically 2nd-to-last group)
                insert_idx = self._find_audit_insert_index(entity["fields"])
                entity["fields"].insert(insert_idx, new_field)
                break
        self.editor.set("webflux_entity_layer.json", "entities", el_entities)

        # entities: find entity by table_name, append column before audit columns
        ent_list = self.editor.get("webflux_entities.json", "entities")
        for entity in ent_list:
            if entity.get("name") == table_name:
                new_col = {
                    "name": col_name,
                    "type": _infer_column_definition(java_type),
                    "primaryKey": False,
                    "nullable": True,
                    "foreignKey": None,
                    "unique": False,
                    "defaultValue": None,
                }
                insert_idx = self._find_audit_column_insert_index(entity["columns"])
                entity["columns"].insert(insert_idx, new_col)
                break
        self.editor.set("webflux_entities.json", "entities", ent_list)

        # dto_layer: add field to Input, Output, and Filter DTOs
        dto_field = {"fieldName": camel_name, "javaType": java_type, "includeInDTO": True}
        field_widget = field.get("fieldWidget")
        if field_widget:
            dto_field["fieldWidget"] = field_widget
            if field_widget == "codeEditor" and "language" in field:
                dto_field["language"] = field["language"]
        dtos = self.editor.get("webflux_dto_layer.json", "dtos")
        for dto in dtos:
            if dto.get("entityName") == entity_name:
                if dto.get("dtoType") in ("Input", "Filter"):
                    dto["fields"].append(dto_field.copy())
                elif dto.get("dtoType") == "Output":
                    # Insert before audit fields in Output DTO
                    idx = self._find_dto_audit_insert_index(dto["fields"])
                    dto["fields"].insert(idx, dto_field.copy())
        self.editor.set("webflux_dto_layer.json", "dtos", dtos)

        dirty = list(FIELD_LAYER_FILES)
        self.status.mark_dirty(dirty)
        return dirty

    def remove_field(self, entity_name: str, field_name: str) -> list[str]:
        """Remove field from entity_layer, entities, and dto_layer. Returns dirty files."""
        table_name = _to_snake_case(entity_name)
        col_name = _to_snake_case(field_name)
        camel_name = _to_camel_case(field_name)

        # entity_layer
        el_entities = self.editor.get("webflux_entity_layer.json", "entities")
        for entity in el_entities:
            if entity.get("className") == entity_name:
                entity["fields"] = [
                    f for f in entity["fields"] if f.get("columnName") != col_name
                ]
                break
        self.editor.set("webflux_entity_layer.json", "entities", el_entities)

        # entities
        ent_list = self.editor.get("webflux_entities.json", "entities")
        for entity in ent_list:
            if entity.get("name") == table_name:
                entity["columns"] = [
                    c for c in entity["columns"] if c.get("name") != col_name
                ]
                break
        self.editor.set("webflux_entities.json", "entities", ent_list)

        # dto_layer
        dtos = self.editor.get("webflux_dto_layer.json", "dtos")
        for dto in dtos:
            if dto.get("entityName") == entity_name:
                dto["fields"] = [
                    f for f in dto["fields"] if f.get("fieldName") != camel_name
                ]
        self.editor.set("webflux_dto_layer.json", "dtos", dtos)

        dirty = list(FIELD_LAYER_FILES)
        self.status.mark_dirty(dirty)
        return dirty

    def modify_field(self, entity_name: str, field_name: str, updates: dict) -> list[str]:
        """Modify field properties in entity_layer, entities, and dto_layer. Returns dirty files.

        Args:
            entity_name: PascalCase entity class name.
            field_name: snake_case or camelCase field name to modify.
            updates: Dict of property updates (e.g. {"type": "Integer", "isNullable": False}).
        """
        table_name = _to_snake_case(entity_name)
        col_name = _to_snake_case(field_name)
        camel_name = _to_camel_case(field_name)

        # Validate fieldWidget if present in updates
        update_widget = updates.get("fieldWidget")
        if update_widget and update_widget not in VALID_FIELD_WIDGETS:
            raise ValueError(
                f"Invalid fieldWidget '{update_widget}'. "
                f"Allowed values: {sorted(VALID_FIELD_WIDGETS)}"
            )

        new_java_type = updates.get("type")
        new_col_def = _infer_column_definition(new_java_type) if new_java_type else None

        # entity_layer
        el_entities = self.editor.get("webflux_entity_layer.json", "entities")
        for entity in el_entities:
            if entity.get("className") == entity_name:
                for f in entity["fields"]:
                    if f.get("columnName") == col_name:
                        if new_java_type:
                            f["javaType"] = new_java_type
                            f["columnDefinition"] = new_col_def
                        if "isNullable" in updates:
                            f["isNullable"] = updates["isNullable"]
                        break
                break
        self.editor.set("webflux_entity_layer.json", "entities", el_entities)

        # entities
        ent_list = self.editor.get("webflux_entities.json", "entities")
        for entity in ent_list:
            if entity.get("name") == table_name:
                for c in entity["columns"]:
                    if c.get("name") == col_name:
                        if new_col_def:
                            c["type"] = new_col_def
                        if "isNullable" in updates:
                            c["nullable"] = updates["isNullable"]
                        break
                break
        self.editor.set("webflux_entities.json", "entities", ent_list)

        # dto_layer
        dtos = self.editor.get("webflux_dto_layer.json", "dtos")
        for dto in dtos:
            if dto.get("entityName") == entity_name:
                for f in dto["fields"]:
                    if f.get("fieldName") == camel_name:
                        if new_java_type:
                            f["javaType"] = new_java_type
                        if "fieldWidget" in updates:
                            f["fieldWidget"] = updates["fieldWidget"]
                            if updates["fieldWidget"] == "codeEditor" and "language" in updates:
                                f["language"] = updates["language"]
                            elif "language" in f and updates["fieldWidget"] != "codeEditor":
                                del f["language"]
                        break
        self.editor.set("webflux_dto_layer.json", "dtos", dtos)

        dirty = list(FIELD_LAYER_FILES)
        self.status.mark_dirty(dirty)
        return dirty

    # ── Endpoint operations ─────────────────────────────────────────────

    def add_endpoint(self, entity_name: str, endpoint: dict) -> list[str]:
        """Add custom endpoint to controller_layer. Returns dirty files."""
        controllers = self.editor.get("webflux_controller_layer.json", "controllers")
        for ctrl in controllers:
            if ctrl.get("entityName") == entity_name:
                ctrl["customEndpoints"].append(endpoint)
                break
        self.editor.set("webflux_controller_layer.json", "controllers", controllers)

        dirty = ["webflux_controller_layer.json"]
        self.status.mark_dirty(dirty)
        return dirty

    def remove_endpoint(self, entity_name: str, endpoint_name: str) -> list[str]:
        """Remove custom endpoint from controller_layer. Returns dirty files."""
        controllers = self.editor.get("webflux_controller_layer.json", "controllers")
        for ctrl in controllers:
            if ctrl.get("entityName") == entity_name:
                ctrl["customEndpoints"] = [
                    e for e in ctrl.get("customEndpoints", [])
                    if e.get("name") != endpoint_name
                ]
                break
        self.editor.set("webflux_controller_layer.json", "controllers", controllers)

        dirty = ["webflux_controller_layer.json"]
        self.status.mark_dirty(dirty)
        return dirty

    # ── Query operations ────────────────────────────────────────────────

    def add_query(self, entity_name: str, query: dict) -> list[str]:
        """Add custom query to repository_layer. Returns dirty files."""
        repos = self.editor.get("webflux_repository_layer.json", "repositories")
        for repo in repos:
            if repo.get("entityName") == entity_name:
                repo["customQueries"].append(query)
                repo["hasCustomQueries"] = True
                break
        self.editor.set("webflux_repository_layer.json", "repositories", repos)

        dirty = ["webflux_repository_layer.json"]
        self.status.mark_dirty(dirty)
        return dirty

    def remove_query(self, entity_name: str, query_name: str) -> list[str]:
        """Remove custom query from repository_layer. Returns dirty files."""
        repos = self.editor.get("webflux_repository_layer.json", "repositories")
        for repo in repos:
            if repo.get("entityName") == entity_name:
                repo["customQueries"] = [
                    q for q in repo.get("customQueries", [])
                    if q.get("name") != query_name
                ]
                repo["hasCustomQueries"] = len(repo["customQueries"]) > 0
                break
        self.editor.set("webflux_repository_layer.json", "repositories", repos)

        dirty = ["webflux_repository_layer.json"]
        self.status.mark_dirty(dirty)
        return dirty

    # ── Relationship operations ─────────────────────────────────────────

    def add_relationship(self, relationship: dict) -> list[str]:
        """Add relationship to relationships file. Returns dirty files."""
        self.editor.append("webflux_relationships.json", "relationships", relationship)

        dirty = ["webflux_relationships.json"]
        self.status.mark_dirty(dirty)
        return dirty

    def remove_relationship(self, source: str, target: str) -> list[str]:
        """Remove relationship by source and target entity names. Returns dirty files."""
        rels = self.editor.get("webflux_relationships.json", "relationships")
        filtered = [
            r for r in rels
            if not (r.get("sourceEntity") == source and r.get("targetEntity") == target)
        ]
        self.editor.set("webflux_relationships.json", "relationships", filtered)

        dirty = ["webflux_relationships.json"]
        self.status.mark_dirty(dirty)
        return dirty

    # ── Document storage layer operations ───────────────────────────────

    def add_json_column(self, entity_name: str, column_name: str, field_name: str) -> list[str]:
        """Add a JSON column mapping. Returns list of dirty filenames."""
        json_columns = self.editor.get(DSL_FILE, "jsonColumns")
        entry = {"entityName": entity_name, "columnName": column_name, "fieldName": field_name}
        json_columns.append(entry)
        self.editor.set(DSL_FILE, "jsonColumns", json_columns)
        self.status.mark_dirty([DSL_FILE])
        return [DSL_FILE]

    def remove_json_column(self, entity_name: str, field_name: str) -> list[str]:
        """Remove a JSON column mapping by entity name and field name. Returns list of dirty filenames."""
        json_columns = self.editor.get(DSL_FILE, "jsonColumns")
        json_columns = [
            jc for jc in json_columns
            if not (jc["entityName"] == entity_name and jc["fieldName"] == field_name)
        ]
        self.editor.set(DSL_FILE, "jsonColumns", json_columns)
        self.status.mark_dirty([DSL_FILE])
        return [DSL_FILE]

    def add_document_collection(self, name: str, table_name: str, description: str = "") -> list[str]:
        """Add a document collection. Returns list of dirty filenames."""
        collections = self.editor.get(DSL_FILE, "documentCollections")
        entry = {"name": name, "tableName": table_name, "description": description}
        collections.append(entry)
        self.editor.set(DSL_FILE, "documentCollections", collections)
        self.status.mark_dirty([DSL_FILE])
        return [DSL_FILE]

    def remove_document_collection(self, name: str) -> list[str]:
        """Remove a document collection by name. Returns list of dirty filenames."""
        collections = self.editor.get(DSL_FILE, "documentCollections")
        collections = [dc for dc in collections if dc["name"] != name]
        self.editor.set(DSL_FILE, "documentCollections", collections)
        self.status.mark_dirty([DSL_FILE])
        return [DSL_FILE]

    # ── Private helpers ─────────────────────────────────────────────────

    def _get_base_package(self) -> str:
        """Extract base package from project_metadata, defaulting to com.example."""
        try:
            meta = self.editor.get("webflux_project_metadata.json", "projectMetadata")
            return meta.get("groupId", "com.example")
        except (FileNotFoundError, KeyError):
            return "com.example"

    def _build_entity_fields(self, table_name: str, fields: list[dict]) -> list[dict]:
        """Build the full fields list for entity_layer (id + user + audit + soft-delete)."""
        result = []

        # Primary key
        result.append({
            "columnName": f"{table_name}_id",
            "fieldName": f"{_to_camel_case(table_name)}Id",
            "javaType": "Long",
            "isPrimaryKey": True,
            "isNullable": False,
            "columnDefinition": "BIGINT UNSIGNED",
        })

        # User fields
        for field_desc in fields:
            fname = field_desc["name"]
            java_type = field_desc.get("type", "String")
            result.append({
                "columnName": _to_snake_case(fname),
                "fieldName": _to_camel_case(fname),
                "javaType": java_type,
                "isPrimaryKey": False,
                "isNullable": True,
                "columnDefinition": _infer_column_definition(java_type),
            })

        # Audit fields
        result.append({
            "columnName": "created_at", "fieldName": "createdAt",
            "javaType": "LocalDateTime", "isPrimaryKey": False,
            "isNullable": False, "columnDefinition": "TIMESTAMP",
        })
        result.append({
            "columnName": "updated_at", "fieldName": "updatedAt",
            "javaType": "LocalDateTime", "isPrimaryKey": False,
            "isNullable": False, "columnDefinition": "TIMESTAMP",
        })

        return result

    def _build_entity_columns(self, table_name: str, fields: list[dict]) -> list[dict]:
        """Build the columns list for entities (column-level view)."""
        columns = []

        # Primary key
        columns.append({
            "name": f"{table_name}_id", "type": "BIGINT UNSIGNED",
            "primaryKey": True, "nullable": False,
            "foreignKey": None, "unique": False, "defaultValue": None,
        })

        # User columns
        for field_desc in fields:
            fname = field_desc["name"]
            java_type = field_desc.get("type", "String")
            columns.append({
                "name": _to_snake_case(fname),
                "type": _infer_column_definition(java_type),
                "primaryKey": False, "nullable": True,
                "foreignKey": None, "unique": False, "defaultValue": None,
            })

        # Audit columns
        columns.append({
            "name": "created_at", "type": "TIMESTAMP",
            "primaryKey": False, "nullable": False,
            "foreignKey": None, "unique": False, "defaultValue": None,
        })
        columns.append({
            "name": "updated_at", "type": "TIMESTAMP",
            "primaryKey": False, "nullable": False,
            "foreignKey": None, "unique": False, "defaultValue": None,
        })

        return columns

    def _append_dtos_for_entity(self, name: str, table_name: str,
                                 fields: list[dict], base_package: str) -> None:
        """Append Input, Output, and Filter DTOs for an entity to dto_layer."""
        # Input DTO: user fields only
        input_fields = []
        for fd in fields:
            input_fields.append({
                "fieldName": _to_camel_case(fd["name"]),
                "javaType": fd.get("type", "String"),
                "includeInDTO": True,
            })
        self.editor.append("webflux_dto_layer.json", "dtos", {
            "entityName": name, "dtoType": "Input",
            "className": f"{name}InputDTO",
            "packageName": f"{base_package}.dto",
            "fields": input_fields,
        })

        # Output DTO: id + user + audit + soft-delete
        output_fields = [
            {"fieldName": f"{_to_camel_case(table_name)}Id", "javaType": "Long", "includeInDTO": True},
        ]
        for fd in fields:
            output_fields.append({
                "fieldName": _to_camel_case(fd["name"]),
                "javaType": fd.get("type", "String"),
                "includeInDTO": True,
            })
        output_fields.append({"fieldName": "createdAt", "javaType": "LocalDateTime", "includeInDTO": True})
        output_fields.append({"fieldName": "updatedAt", "javaType": "LocalDateTime", "includeInDTO": True})
        self.editor.append("webflux_dto_layer.json", "dtos", {
            "entityName": name, "dtoType": "Output",
            "className": f"{name}OutputDTO",
            "packageName": f"{base_package}.dto",
            "fields": output_fields,
        })

        # Filter DTO: user fields only
        filter_fields = []
        for fd in fields:
            filter_fields.append({
                "fieldName": _to_camel_case(fd["name"]),
                "javaType": fd.get("type", "String"),
                "includeInDTO": True,
            })
        self.editor.append("webflux_dto_layer.json", "dtos", {
            "entityName": name, "dtoType": "Filter",
            "className": f"{name}FilterDTO",
            "packageName": f"{base_package}.dto",
            "fields": filter_fields,
        })

    def _find_audit_insert_index(self, fields: list[dict]) -> int:
        """Find the index where user fields end and audit fields begin in entity_layer."""
        for i, f in enumerate(fields):
            if f.get("columnName") in ("created_at", "updated_at"):
                return i
        return len(fields)

    def _find_audit_column_insert_index(self, columns: list[dict]) -> int:
        """Find the index where user columns end and audit columns begin in entities."""
        for i, c in enumerate(columns):
            if c.get("name") in ("created_at", "updated_at"):
                return i
        return len(columns)

    def _find_dto_audit_insert_index(self, fields: list[dict]) -> int:
        """Find the index where user fields end and audit fields begin in Output DTO."""
        for i, f in enumerate(fields):
            if f.get("fieldName") in ("createdAt", "updatedAt"):
                return i
        return len(fields)
