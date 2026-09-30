"""Database DTO manager — CRUD on swfaw_dto_layer (Tier 2).

Each entity typically has 3 DTO rows: Input, Output, Filter.
"""

import json
from typing import Optional, Dict, Any, List
from .db_connection import DbConnection


class DbDtoManager:
    """CRUD operations on swfaw_dto_layer (replaces dto_layer.json).
    
    Usage:
        dm = DbDtoManager(db, app_id=1)
        
        dm.add_dto("users", "Input", "UserInputDto", field_configs=[...])
        dm.add_dto("users", "Output", "UserOutputDto", field_configs=[...])
        dm.add_dto("users", "Filter", "UserFilterDto", field_configs=[...])
        
        dtos = dm.list_dtos("users")
        dm.update_dto("users", "Input", field_configs_json=[...])
    """

    TABLE = "swfaw_dto_layer"

    def __init__(self, db: DbConnection, app_id: int):
        self.db = db
        self.app_id = app_id

    def _decode_row(self, row: Dict[str, Any]) -> Dict[str, Any]:
        if row is None:
            return row
        for key in list(row.keys()):
            if key.endswith("_json") and isinstance(row[key], str):
                try:
                    row[key] = json.loads(row[key])
                except (json.JSONDecodeError, TypeError):
                    pass
        return row

    # ------------------------------------------------------------------
    # READ
    # ------------------------------------------------------------------

    def list_dtos(self, entity_name: Optional[str] = None) -> List[Dict[str, Any]]:
        if entity_name:
            rows = self.db.fetch_all(
                f"SELECT * FROM {self.TABLE} "
                "WHERE app_definition_id = %s AND entity_name = %s ORDER BY dto_type",
                (self.app_id, entity_name),
            )
        else:
            rows = self.db.fetch_all(
                f"SELECT * FROM {self.TABLE} "
                "WHERE app_definition_id = %s ORDER BY entity_name, dto_type",
                (self.app_id,),
            )
        return [self._decode_row(r) for r in rows]

    def get_dto(self, entity_name: str, dto_type: str) -> Optional[Dict[str, Any]]:
        row = self.db.fetch_one(
            f"SELECT * FROM {self.TABLE} "
            "WHERE app_definition_id = %s AND entity_name = %s AND dto_type = %s",
            (self.app_id, entity_name, dto_type),
        )
        return self._decode_row(row)

    # ------------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------------

    def add_dto(
        self,
        entity_name: str,
        dto_type: str,
        class_name: str,
        field_configs: List[Dict[str, Any]],
        package_name: str = "com.example.dto",
        is_root_entity: bool = False,
        custom_validators: Optional[List] = None,
        exclude_sensitive_fields: Optional[List[str]] = None,
        include_relationships: bool = False,
    ) -> int:
        sql = (
            f"INSERT INTO {self.TABLE} "
            "(app_definition_id, entity_name, dto_type, class_name, package_name, "
            "is_root_entity, field_configs_json, custom_validators_json, "
            "exclude_sensitive_fields, include_relationships) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        return self.db.insert(sql, (
            self.app_id, entity_name, dto_type, class_name, package_name,
            int(is_root_entity), json.dumps(field_configs),
            json.dumps(custom_validators) if custom_validators else None,
            json.dumps(exclude_sensitive_fields) if exclude_sensitive_fields else None,
            int(include_relationships),
        ))

    # ------------------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------------------

    def update_dto(self, entity_name: str, dto_type: str, **kwargs) -> int:
        if not kwargs:
            return 0
        for col in list(kwargs.keys()):
            if col.endswith("_json") and not isinstance(kwargs[col], str) and kwargs[col] is not None:
                kwargs[col] = json.dumps(kwargs[col])
            # Convenience: accept "field_configs" as a list
            if col == "field_configs" and "field_configs_json" not in kwargs:
                kwargs["field_configs_json"] = json.dumps(kwargs.pop("field_configs"))
        set_clause = ", ".join(f"{col} = %s" for col in kwargs)
        return self.db.execute(
            f"UPDATE {self.TABLE} SET {set_clause} "
            "WHERE app_definition_id = %s AND entity_name = %s AND dto_type = %s",
            tuple(kwargs.values()) + (self.app_id, entity_name, dto_type),
        )

    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------

    def remove_dto(self, entity_name: str, dto_type: str) -> int:
        return self.db.execute(
            f"DELETE FROM {self.TABLE} "
            "WHERE app_definition_id = %s AND entity_name = %s AND dto_type = %s",
            (self.app_id, entity_name, dto_type),
        )

    def remove_all_dtos(self, entity_name: str) -> int:
        """Remove all DTOs (Input, Output, Filter) for an entity."""
        return self.db.execute(
            f"DELETE FROM {self.TABLE} "
            "WHERE app_definition_id = %s AND entity_name = %s",
            (self.app_id, entity_name),
        )
