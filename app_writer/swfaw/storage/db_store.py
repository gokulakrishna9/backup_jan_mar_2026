"""MySQL database storage backend — uses db_managers for all operations."""

import re
import json
from typing import Optional, Dict, Any, List

from .base import DefinitionStore
from models.database_definition import DatabaseDefinition
from db_managers import (
    DbConnection,
    DbStoreManager,
    DbEntityManager,
    DbRelationshipManager,
    DbLayerManager,
    DbSecurityManager,
    DbConfigManager,
    DbExceptionManager,
    DbAuditManager,
    DbAuthorizationManager,
    DbGroupManager,
    DbQueryManager,
    DbFilterManager,
    DbDtoManager,
)


class DbStore(DefinitionStore):
    """Storage backend that reads/writes to the swfaw_definition_store MySQL database.

    Uses the db_managers module for all CRUD operations. Produces the same
    DatabaseDefinition and layer_definitions dict that the JSON backend does.
    """

    def __init__(self, db: DbConnection):
        self.db = db

    # ------------------------------------------------------------------
    # SAVE
    # ------------------------------------------------------------------

    def save(self, db_def: DatabaseDefinition, output_dir: str) -> str:
        """Save a complete application definition to the database.

        Inserts into all relevant tables using the db_managers API.
        Also generates layer definitions from the DatabaseDefinition
        (same logic as the JSON pipeline) and stores them in DB tables.

        Returns:
            str(app_id) — the new app definition row ID
        """
        meta = db_def.projectMetadata
        store = DbStoreManager(self.db)

        # 1. Create root app definition
        app_id = store.create_app(
            project_name=meta.name,
            application_name=meta.applicationName,
            artifact_id=meta.artifactId,
            db_name=meta.database.name,
            group_id=meta.groupId,
            project_version=meta.version,
            port=meta.port,
            db_type=meta.database.type,
            db_host=meta.database.host,
            db_port=meta.database.port,
            db_username=meta.database.username,
            db_password=meta.database.password,
            sql_file_name=meta.sqlFileName,
        )

        # 2. Insert entities
        em = DbEntityManager(self.db, app_id)
        for idx, table in enumerate(db_def.tables):
            columns = [col.model_dump() for col in table.columns]
            pk_col = None
            for col in table.columns:
                if col.primaryKey:
                    pk_col = col.name
                    break
            em.add_entity(
                table_name=table.name,
                columns=columns,
                primary_key_column=pk_col,
                sort_order=idx,
            )

        # 3. Insert relationships
        rm = DbRelationshipManager(self.db, app_id)
        for table in db_def.tables:
            for rel in table.relationships:
                rm.add_relationship(
                    source_table=table.name,
                    target_table=rel.targetTable,
                    relationship_type=rel.type,
                    foreign_key_column=rel.foreignKey,
                    join_table=rel.joinTable,
                )

        # 4. Generate and store layer definitions
        self._save_layer_definitions(db_def, app_id)

        # 5. Update statistics
        store.refresh_statistics(app_id)

        return str(app_id)

    # ------------------------------------------------------------------
    # CAMEL-CASE → SNAKE-CASE MAPPING HELPERS
    # ------------------------------------------------------------------

    @staticmethod
    def _camel_to_snake(name: str) -> str:
        """Convert camelCase to snake_case."""
        s1 = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', name)
        return re.sub(r'([a-z\d])([A-Z])', r'\1_\2', s1).lower()

    @classmethod
    def _map_entity_layer(cls, ent: Dict[str, Any]) -> Dict[str, Any]:
        """Map entity layer generator output to DB column names."""
        return {cls._camel_to_snake(k): v for k, v in ent.items() if k != "fields"}

    @classmethod
    def _map_entity_layer_field(cls, field: Dict[str, Any]) -> Dict[str, Any]:
        """Map entity layer field generator output to DB column names."""
        return {cls._camel_to_snake(k): v for k, v in field.items()}

    @classmethod
    def _map_repo_layer(cls, repo: Dict[str, Any]) -> Dict[str, Any]:
        """Map repository layer generator output to DB column names.
        
        Handles list/dict values → _json suffix columns.
        """
        mapped = {}
        for k, v in repo.items():
            snake = cls._camel_to_snake(k)
            # Lists/dicts go into _json columns
            if isinstance(v, (list, dict)) and not snake.endswith("_json"):
                snake = snake + "_json"
            mapped[snake] = v
        return mapped

    @classmethod
    def _map_service_layer(cls, svc: Dict[str, Any]) -> Dict[str, Any]:
        """Map service layer generator output to DB column names.
        
        Flattens nested authorizationConfig, transactionManagement,
        customMethods, and validationRules into flat DB columns.
        """
        mapped = {}
        for k, v in svc.items():
            if k == "authorizationConfig" and isinstance(v, dict):
                mapped["auth_check_on_create"] = int(v.get("checkOnCreate", True))
                mapped["auth_check_on_read"] = int(v.get("checkOnRead", True))
                mapped["auth_check_on_update"] = int(v.get("checkOnUpdate", True))
                mapped["auth_check_on_delete"] = int(v.get("checkOnDelete", True))
                mapped["auth_allow_public_read"] = int(v.get("allowPublicRead", False))
                mapped["auth_require_ownership"] = int(v.get("requireOwnership", True))
            elif k == "transactionManagement" and isinstance(v, dict):
                mapped["tx_enabled"] = int(v.get("enabled", True))
                mapped["tx_propagation"] = v.get("propagation", "REQUIRED")
                mapped["tx_isolation"] = v.get("isolation", "DEFAULT")
                mapped["tx_timeout"] = v.get("timeout", 30)
            elif k == "customMethods" and isinstance(v, list):
                mapped["custom_methods_json"] = v
            elif k == "validationRules" and isinstance(v, dict):
                mapped["validation_rules_json"] = v
            else:
                snake = cls._camel_to_snake(k)
                mapped[snake] = v
        return mapped

    @classmethod
    def _map_controller_layer(cls, ctrl: Dict[str, Any]) -> Dict[str, Any]:
        """Map controller layer generator output to DB column names.
        
        Flattens endpoints dict into endpoint_*_json columns and
        corsConfig into cors_* columns.
        """
        mapped = {}
        for k, v in ctrl.items():
            if k == "endpoints" and isinstance(v, dict):
                mapped["endpoint_create_json"] = v.get("create")
                mapped["endpoint_get_by_id_json"] = v.get("getById")
                mapped["endpoint_get_all_json"] = v.get("getAll")
                mapped["endpoint_update_json"] = v.get("update")
                mapped["endpoint_delete_json"] = v.get("delete")
            elif k == "corsConfig" and isinstance(v, dict):
                mapped["cors_enabled"] = int(v.get("enabled", True))
                origins = v.get("allowedOrigins", ["*"])
                methods = v.get("allowedMethods", ["GET", "POST", "PUT", "DELETE"])
                headers = v.get("allowedHeaders", ["*"])
                # These are JSON columns — serialize lists to JSON strings
                mapped["cors_allowed_origins"] = json.dumps(origins if isinstance(origins, list) else [origins])
                mapped["cors_allowed_methods"] = json.dumps(methods if isinstance(methods, list) else [methods])
                mapped["cors_allowed_headers"] = json.dumps(headers if isinstance(headers, list) else [headers])
                mapped["cors_max_age"] = v.get("maxAge", 3600)
            elif k == "customEndpoints" and isinstance(v, list):
                mapped["custom_endpoints_json"] = v
            else:
                snake = cls._camel_to_snake(k)
                mapped[snake] = v
        return mapped

    def _save_layer_definitions(self, db_def: DatabaseDefinition, app_id: int):
        """Generate layer definitions and store them in DB tables."""
        from utils.layer_definition_generator import (
            generate_entity_layer_definition,
            generate_repository_layer_definition,
            generate_service_layer_definition,
            generate_controller_layer_definition,
            generate_dto_layer_definition,
            generate_security_layer_definition,
            generate_config_layer_definition,
            generate_exception_layer_definition,
            generate_audit_logging_layer_definition,
            generate_authorization_layer_definition,
            generate_group_definition_layer,
            generate_query_layer_definition,
            generate_filter_layer_definition,
        )

        lm = DbLayerManager(self.db, app_id)

        # --- Per-entity layers ---
        entity_layer = generate_entity_layer_definition(db_def)
        for ent in entity_layer.get("entities", []):
            data = self._map_entity_layer(ent)
            data["app_definition_id"] = app_id
            ent_row_id = lm.insert("entity_layer", data)
            for field in ent.get("fields", []):
                mapped_field = self._map_entity_layer_field(field)
                mapped_field["entity_layer_id"] = ent_row_id
                lm.insert("entity_layer_field", mapped_field)

        repo_layer = generate_repository_layer_definition(db_def)
        for repo in repo_layer.get("repositories", []):
            data = self._map_repo_layer(repo)
            data["app_definition_id"] = app_id
            lm.insert("repository_layer", data)

        svc_layer = generate_service_layer_definition(db_def)
        for svc in svc_layer.get("services", []):
            data = self._map_service_layer(svc)
            data["app_definition_id"] = app_id
            lm.insert("service_layer", data)

        ctrl_layer = generate_controller_layer_definition(db_def)
        for ctrl in ctrl_layer.get("controllers", []):
            data = self._map_controller_layer(ctrl)
            data["app_definition_id"] = app_id
            lm.insert("controller_layer", data)

        dto_layer = generate_dto_layer_definition(db_def)
        dm = DbDtoManager(self.db, app_id)
        for dto in dto_layer.get("dtos", []):
            dm.add_dto(
                entity_name=dto.get("entityName", dto.get("tableName", "")),
                dto_type=dto.get("dtoType", "Input"),
                class_name=dto.get("className", ""),
                field_configs=dto.get("fields", []),
                package_name=dto.get("packageName", "com.example.dto"),
            )

        # --- Application-wide config layers ---
        sec_layer = generate_security_layer_definition(db_def)
        sm = DbSecurityManager(self.db, app_id)
        jwt = sec_layer.get("jwt", {})
        sm.create_config(
            jwt_enabled=int(jwt.get("enabled", True)),
            jwt_secret=jwt.get("secret", ""),
            jwt_expiration=jwt.get("expiration", 86400000),
            jwt_issuer=jwt.get("issuer", ""),
            jwt_algorithm=jwt.get("algorithm", "HS256"),
        )
        cors = sec_layer.get("cors", {})
        if cors:
            sm.set_cors(
                cors_enabled=int(cors.get("enabled", True)),
                allowed_origins_json=cors.get("allowedOrigins", ["*"]),
                allowed_methods_json=cors.get("allowedMethods", []),
                allowed_headers_json=cors.get("allowedHeaders", []),
            )
        for ep in sec_layer.get("publicEndpoints", []):
            pattern = ep if isinstance(ep, str) else ep.get("pattern", "")
            if pattern:
                sm.add_public_endpoint(pattern)

        cfg_layer = generate_config_layer_definition(db_def)
        cm = DbConfigManager(self.db, app_id)
        app_cfg = cfg_layer.get("application", {})
        cm.create_config(
            server_port=app_cfg.get("port", 8081),
            java_version=str(app_cfg.get("javaVersion", "21")),
            spring_boot_version=app_cfg.get("springBootVersion", "3.3.0"),
        )

        exc_layer = generate_exception_layer_definition(db_def)
        exm = DbExceptionManager(self.db, app_id)
        exc_cfg = exc_layer.get("globalConfig", exc_layer.get("config", {}))
        exm.create_config(
            handle_validation_errors=int(exc_cfg.get("handleValidationErrors", True)),
            log_level=exc_cfg.get("logLevel", "ERROR"),
        )
        for exc_def in exc_layer.get("exceptions", []):
            exm.add_exception(
                class_name=exc_def.get("className", ""),
                http_status=exc_def.get("httpStatus", 500),
                default_message=exc_def.get("defaultMessage", ""),
            )
        for msg in exc_layer.get("entityMessages", []):
            exm.add_message(
                exception_class=msg.get("exceptionClass", ""),
                target_name=msg.get("entityName", msg.get("targetName", "")),
                message=msg.get("message", ""),
            )

        audit_layer = generate_audit_logging_layer_definition(db_def)
        am = DbAuditManager(self.db, app_id)
        audit_cfg = audit_layer.get("config", {})
        am.create_config(
            audit_enabled=int(audit_cfg.get("enabled", True)),
        )
        for evt in audit_layer.get("events", []):
            am.add_event(
                category=evt.get("category", ""),
                event_type=evt.get("eventType", ""),
                log_level=evt.get("logLevel", "INFO"),
                message_template=evt.get("messageTemplate", ""),
            )
        for alert in audit_layer.get("alerts", []):
            am.add_alert(
                event_type=alert.get("eventType", ""),
                threshold=alert.get("threshold", 5),
                time_window_minutes=alert.get("timeWindowMinutes", 15),
            )

        authz_layer = generate_authorization_layer_definition(db_def)
        azm = DbAuthorizationManager(self.db, app_id)
        azm.create_config(
            access_controls_json=[],
            document_group_types_json=[],
        )
        for ac in authz_layer.get("entityAccessControls", []):
            azm.add_entity_access(
                entity_name=ac.get("entityName", ""),
                table_name=ac.get("tableName", ""),
                enable_access_control=int(ac.get("enableAccessControl", True)),
            )

        group_layer = generate_group_definition_layer(db_def)
        gm = DbGroupManager(self.db, app_id)
        gm.create_config()
        for grp in group_layer.get("groups", []):
            gm.add_group(
                group_name=grp.get("groupName", ""),
                group_category=grp.get("groupCategory", "SYSTEM"),
                table_name=grp.get("tableName"),
                group_type=grp.get("groupType"),
                access_level=grp.get("accessLevel"),
                is_super_group=int(grp.get("isSuperGroup", False)),
                sort_order=grp.get("sortOrder", 0),
            )

        query_layer = generate_query_layer_definition(db_def)
        qm = DbQueryManager(self.db, app_id)
        queries_data = query_layer.get("queries", {})
        # queries_data is a dict: {entityName: [query_dict, ...]}
        if isinstance(queries_data, dict):
            for entity_name, query_list in queries_data.items():
                for q in (query_list if isinstance(query_list, list) else []):
                    query_id = qm.add_query(
                        entity_name=entity_name,
                        query_name=q.get("name", q.get("queryName", "")),
                        return_type=q.get("returnType", ""),
                        select_fields=q.get("select", q.get("selectFields", [])),
                        from_clause=q.get("from", q.get("fromClause", "")),
                        description=q.get("description"),
                        pagination=q.get("pagination", True),
                    )
                    for j in q.get("joins", []):
                        qm.add_join(
                            query_id,
                            j.get("type", j.get("joinType", "")),
                            j.get("table", j.get("joinTable", "")),
                            j.get("on", j.get("joinCondition", "")),
                        )
                    for p in q.get("parameters", []):
                        qm.add_parameter(
                            query_id,
                            p.get("name", p.get("paramName", "")),
                            p.get("type", p.get("paramType", "")),
                        )
        else:
            # Fallback: flat list with entityName in each dict
            for q in queries_data:
                query_id = qm.add_query(
                    entity_name=q.get("entityName", ""),
                    query_name=q.get("queryName", q.get("name", "")),
                    return_type=q.get("returnType", ""),
                    select_fields=q.get("selectFields", q.get("select", [])),
                    from_clause=q.get("fromClause", q.get("from", "")),
                    description=q.get("description"),
                    pagination=q.get("pagination", True),
                )
                for j in q.get("joins", []):
                    qm.add_join(query_id, j.get("joinType", j.get("type", "")), j.get("joinTable", j.get("table", "")), j.get("joinCondition", j.get("on", "")))
                for p in q.get("parameters", []):
                    qm.add_parameter(query_id, p.get("paramName", p.get("name", "")), p.get("paramType", p.get("type", "")))

        filter_layer = generate_filter_layer_definition(db_def)
        fm = DbFilterManager(self.db, app_id)
        filters_data = filter_layer.get("filters", {})
        # filters_data is a dict: {entityName: {fields: [...]}}
        if isinstance(filters_data, dict):
            for entity_name, filter_def in filters_data.items():
                if isinstance(filter_def, dict):
                    filter_id = fm.add_filter(entity_name)
                    for field in filter_def.get("fields", []):
                        fm.add_field(
                            filter_id,
                            field.get("name", field.get("fieldName", "")),
                            field.get("type", field.get("fieldType", "")),
                            operators=field.get("operators"),
                        )
        else:
            # Fallback: flat list with entityName in each dict
            for f in filters_data:
                filter_id = fm.add_filter(f.get("entityName", ""))
                for field in f.get("fields", []):
                    fm.add_field(
                        filter_id,
                        field.get("fieldName", field.get("name", "")),
                        field.get("fieldType", field.get("type", "")),
                        operators=field.get("operators"),
                    )

    # ------------------------------------------------------------------
    # LOAD
    # ------------------------------------------------------------------

    def load(self, identifier: str) -> DatabaseDefinition:
        """Load a DatabaseDefinition from the database.

        Args:
            identifier: str(app_id)
        """
        app_id = int(identifier)
        store = DbStoreManager(self.db)
        app = store.get_app(app_id)
        if app is None:
            raise ValueError(f"App definition {app_id} not found")

        # Reconstruct ProjectMetadata
        project_metadata = {
            "name": app["project_name"],
            "applicationName": app["application_name"],
            "groupId": app["group_id"],
            "artifactId": app["artifact_id"],
            "version": app["project_version"],
            "port": app["port"],
            "sqlFileName": app.get("sql_file_name"),
            "database": {
                "type": app["db_type"],
                "host": app["db_host"],
                "port": app["db_port"],
                "name": app["db_name"],
                "url": app.get("db_url"),
                "username": app["db_username"],
                "password": app["db_password"],
            },
        }

        # Reconstruct tables with relationships
        em = DbEntityManager(self.db, app_id)
        rm = DbRelationshipManager(self.db, app_id)
        entities = em.list_entities()
        all_rels = rm.list_relationships()

        tables = []
        for entity in entities:
            entity_rels = [r for r in all_rels if r["source_table"] == entity["table_name"]]
            tables.append({
                "name": entity["table_name"],
                "columns": entity.get("columns", []),
                "relationships": [
                    {
                        "type": r["relationship_type"],
                        "targetTable": r["target_table"],
                        "foreignKey": r.get("foreign_key_column"),
                        "joinTable": r.get("join_table"),
                    }
                    for r in entity_rels
                ],
            })

        return DatabaseDefinition(**{
            "projectMetadata": project_metadata,
            "tables": tables,
        })

    def load_layer_definitions(self, identifier: str) -> Optional[Dict[str, Any]]:
        """Load layer definitions from DB tables.

        Produces the same dict structure that load_layer_definitions_if_exist()
        returns from JSON files, so generators work identically.
        """
        app_id = int(identifier)
        lm = DbLayerManager(self.db, app_id)

        # Entity layer: rows → dict with "entities" list
        entity_rows = lm.get("entity_layer")
        if not entity_rows:
            return None  # No layer definitions stored

        # Attach fields to each entity layer row
        for row in entity_rows:
            fields = lm.get("entity_layer_field", {"entity_layer_id": row["id"]})
            row["fields"] = fields if isinstance(fields, list) else []

        entity_layer = {"entities": entity_rows}

        # Repository layer
        repo_rows = lm.get("repository_layer")
        repository_layer = {"repositories": repo_rows or []}

        # Service layer
        svc_rows = lm.get("service_layer")
        service_layer = {"services": svc_rows or []}

        # Controller layer
        ctrl_rows = lm.get("controller_layer")
        controller_layer = {"controllers": ctrl_rows or []}

        # DTO layer
        dm = DbDtoManager(self.db, app_id)
        dto_rows = dm.list_dtos()
        dto_layer = {"dtos": dto_rows or []}

        return {
            "entity_layer": entity_layer,
            "repository_layer": repository_layer,
            "service_layer": service_layer,
            "controller_layer": controller_layer,
            "dto_layer": dto_layer,
        }

    # ------------------------------------------------------------------
    # LIST / DELETE
    # ------------------------------------------------------------------

    def list_apps(self) -> List[Dict[str, Any]]:
        """List all active application definitions in the database."""
        store = DbStoreManager(self.db)
        apps = store.list_apps(active_only=True)
        return [
            {
                "identifier": str(a["id"]),
                "name": a["project_name"],
                "application_name": a["application_name"],
                "artifact_id": a["artifact_id"],
                "version": a["project_version"],
                "total_entities": a["total_entities"],
                "total_relationships": a["total_relationships"],
                "date_modified": str(a.get("date_modified", "")),
            }
            for a in apps
        ]

    def delete(self, identifier: str) -> bool:
        """Hard-delete an application definition and all child rows."""
        app_id = int(identifier)
        store = DbStoreManager(self.db)
        affected = store.delete_app(app_id)
        return affected > 0
