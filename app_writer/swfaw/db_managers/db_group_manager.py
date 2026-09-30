"""Database group manager — CRUD on group tables (Tier 4d).

Covers: swfaw_group_config, swfaw_group_definition
"""

from typing import Optional, Dict, Any, List
from .db_connection import DbConnection


class DbGroupManager:
    """CRUD operations on group configuration and definition tables.
    
    Usage:
        gm = DbGroupManager(db, app_id=1)
        gm.create_config()
        gm.add_group("Administrators", "SYSTEM", is_super_group=1)
        gm.add_group("users_viewers", "TABLE_ACCESS",
                      table_name="users", group_type="VIEWER", access_level="READ")
    """

    def __init__(self, db: DbConnection, app_id: int):
        self.db = db
        self.app_id = app_id

    # ------------------------------------------------------------------
    # Group Config (singleton)
    # ------------------------------------------------------------------

    def get_config(self) -> Optional[Dict[str, Any]]:
        return self.db.fetch_one(
            "SELECT * FROM swfaw_group_config WHERE app_definition_id = %s",
            (self.app_id,),
        )

    def create_config(self, **kwargs) -> int:
        kwargs.setdefault("app_definition_id", self.app_id)
        columns = ", ".join(kwargs.keys())
        placeholders = ", ".join(["%s"] * len(kwargs))
        return self.db.insert(
            f"INSERT INTO swfaw_group_config ({columns}) VALUES ({placeholders})",
            tuple(kwargs.values()),
        )

    def update_config(self, **kwargs) -> int:
        if not kwargs:
            return 0
        set_clause = ", ".join(f"{col} = %s" for col in kwargs)
        return self.db.execute(
            f"UPDATE swfaw_group_config SET {set_clause} WHERE app_definition_id = %s",
            tuple(kwargs.values()) + (self.app_id,),
        )

    # ------------------------------------------------------------------
    # Group Definitions
    # ------------------------------------------------------------------

    def list_groups(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        if category:
            return self.db.fetch_all(
                "SELECT * FROM swfaw_group_definition "
                "WHERE app_definition_id = %s AND group_category = %s ORDER BY sort_order",
                (self.app_id, category),
            )
        return self.db.fetch_all(
            "SELECT * FROM swfaw_group_definition "
            "WHERE app_definition_id = %s ORDER BY group_category, sort_order",
            (self.app_id,),
        )

    def get_group(self, group_name: str) -> Optional[Dict[str, Any]]:
        return self.db.fetch_one(
            "SELECT * FROM swfaw_group_definition "
            "WHERE app_definition_id = %s AND group_name = %s",
            (self.app_id, group_name),
        )

    def add_group(self, group_name: str, group_category: str, **kwargs) -> int:
        data = {
            "app_definition_id": self.app_id,
            "group_name": group_name,
            "group_category": group_category,
        }
        data.update(kwargs)
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        return self.db.insert(
            f"INSERT INTO swfaw_group_definition ({columns}) VALUES ({placeholders})",
            tuple(data.values()),
        )

    def update_group(self, group_name: str, **kwargs) -> int:
        if not kwargs:
            return 0
        set_clause = ", ".join(f"{col} = %s" for col in kwargs)
        return self.db.execute(
            f"UPDATE swfaw_group_definition SET {set_clause} "
            "WHERE app_definition_id = %s AND group_name = %s",
            tuple(kwargs.values()) + (self.app_id, group_name),
        )

    def remove_group(self, group_name: str) -> int:
        return self.db.execute(
            "DELETE FROM swfaw_group_definition "
            "WHERE app_definition_id = %s AND group_name = %s",
            (self.app_id, group_name),
        )

    def list_system_groups(self) -> List[Dict[str, Any]]:
        return self.list_groups(category="SYSTEM")

    def list_table_access_groups(self, table_name: Optional[str] = None) -> List[Dict[str, Any]]:
        if table_name:
            return self.db.fetch_all(
                "SELECT * FROM swfaw_group_definition "
                "WHERE app_definition_id = %s AND group_category = 'TABLE_ACCESS' "
                "AND table_name = %s ORDER BY sort_order",
                (self.app_id, table_name),
            )
        return self.list_groups(category="TABLE_ACCESS")
