"""Database filter manager — CRUD on filter tables (Tier 3).

Covers: swfaw_filter, swfaw_filter_field
"""

import json
from typing import Optional, Dict, Any, List
from .db_connection import DbConnection


class DbFilterManager:
    """CRUD operations on filter definition tables.
    
    Usage:
        fm = DbFilterManager(db, app_id=1)
        filter_id = fm.add_filter("users")
        fm.add_field(filter_id, "email", "String", operators=["eq", "contains"])
        fm.add_field(filter_id, "created_at", "LocalDateTime", operators=["gte", "lte"])
    """

    def __init__(self, db: DbConnection, app_id: int):
        self.db = db
        self.app_id = app_id

    # ------------------------------------------------------------------
    # Filters
    # ------------------------------------------------------------------

    def list_filters(self) -> List[Dict[str, Any]]:
        return self.db.fetch_all(
            "SELECT * FROM swfaw_filter WHERE app_definition_id = %s ORDER BY entity_name",
            (self.app_id,),
        )

    def get_filter(self, entity_name: str) -> Optional[Dict[str, Any]]:
        return self.db.fetch_one(
            "SELECT * FROM swfaw_filter "
            "WHERE app_definition_id = %s AND entity_name = %s",
            (self.app_id, entity_name),
        )

    def get_filter_id(self, entity_name: str) -> Optional[int]:
        row = self.get_filter(entity_name)
        return row["id"] if row else None

    def add_filter(self, entity_name: str) -> int:
        return self.db.insert(
            "INSERT INTO swfaw_filter (app_definition_id, entity_name) VALUES (%s, %s)",
            (self.app_id, entity_name),
        )

    def remove_filter(self, entity_name: str) -> int:
        return self.db.execute(
            "DELETE FROM swfaw_filter "
            "WHERE app_definition_id = %s AND entity_name = %s",
            (self.app_id, entity_name),
        )

    # ------------------------------------------------------------------
    # Filter Fields
    # ------------------------------------------------------------------

    def list_fields(self, entity_name: str) -> List[Dict[str, Any]]:
        filter_id = self.get_filter_id(entity_name)
        if filter_id is None:
            return []
        rows = self.db.fetch_all(
            "SELECT * FROM swfaw_filter_field WHERE filter_id = %s ORDER BY sort_order",
            (filter_id,),
        )
        for r in rows:
            if isinstance(r.get("operators_json"), str):
                try:
                    r["operators_json"] = json.loads(r["operators_json"])
                except (json.JSONDecodeError, TypeError):
                    pass
        return rows

    def add_field(
        self,
        filter_id: int,
        field_name: str,
        field_type: str,
        operators: Optional[List[str]] = None,
        sort_order: int = 0,
    ) -> int:
        if operators is None:
            operators = ["eq", "neq"]
        sql = (
            "INSERT INTO swfaw_filter_field "
            "(filter_id, field_name, field_type, operators_json, sort_order) "
            "VALUES (%s, %s, %s, %s, %s)"
        )
        return self.db.insert(sql, (
            filter_id, field_name, field_type, json.dumps(operators), sort_order,
        ))

    def update_field(self, field_id: int, **kwargs) -> int:
        if not kwargs:
            return 0
        if "operators_json" in kwargs and not isinstance(kwargs["operators_json"], str):
            kwargs["operators_json"] = json.dumps(kwargs["operators_json"])
        if "operators" in kwargs:
            kwargs["operators_json"] = json.dumps(kwargs.pop("operators"))
        set_clause = ", ".join(f"{col} = %s" for col in kwargs)
        return self.db.execute(
            f"UPDATE swfaw_filter_field SET {set_clause} WHERE id = %s",
            tuple(kwargs.values()) + (field_id,),
        )

    def remove_field(self, field_id: int) -> int:
        return self.db.execute(
            "DELETE FROM swfaw_filter_field WHERE id = %s", (field_id,)
        )

    # ------------------------------------------------------------------
    # Full filter with fields
    # ------------------------------------------------------------------

    def get_full_filter(self, entity_name: str) -> Optional[Dict[str, Any]]:
        """Get a filter with all its fields included."""
        f = self.get_filter(entity_name)
        if f is None:
            return None
        f["fields"] = self.list_fields(entity_name)
        return f
