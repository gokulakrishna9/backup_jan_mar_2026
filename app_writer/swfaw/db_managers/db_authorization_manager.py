"""Database authorization manager — CRUD on authorization tables (Tier 4d).

Covers: swfaw_authorization_config, swfaw_entity_access_control
"""

import json
from typing import Optional, Dict, Any, List
from .db_connection import DbConnection


class DbAuthorizationManager:
    """CRUD operations on authorization configuration tables.
    
    Usage:
        am = DbAuthorizationManager(db, app_id=1)
        am.create_config()
        am.add_entity_access("users", "users", enable_access_control=1)
        am.update_entity_access("users", check_on_delete=0)
    """

    def __init__(self, db: DbConnection, app_id: int):
        self.db = db
        self.app_id = app_id

    def _get_config_id(self) -> Optional[int]:
        row = self.db.fetch_one(
            "SELECT id FROM swfaw_authorization_config WHERE app_definition_id = %s",
            (self.app_id,),
        )
        return row["id"] if row else None

    # ------------------------------------------------------------------
    # Authorization Config (singleton)
    # ------------------------------------------------------------------

    def get_config(self) -> Optional[Dict[str, Any]]:
        row = self.db.fetch_one(
            "SELECT * FROM swfaw_authorization_config WHERE app_definition_id = %s",
            (self.app_id,),
        )
        if row:
            for key in ("access_controls_json", "document_group_types_json"):
                if isinstance(row.get(key), str):
                    try:
                        row[key] = json.loads(row[key])
                    except (json.JSONDecodeError, TypeError):
                        pass
        return row

    def create_config(self, **kwargs) -> int:
        kwargs.setdefault("app_definition_id", self.app_id)
        for col in list(kwargs.keys()):
            if col.endswith("_json") and not isinstance(kwargs[col], str) and kwargs[col] is not None:
                kwargs[col] = json.dumps(kwargs[col])
        columns = ", ".join(kwargs.keys())
        placeholders = ", ".join(["%s"] * len(kwargs))
        return self.db.insert(
            f"INSERT INTO swfaw_authorization_config ({columns}) VALUES ({placeholders})",
            tuple(kwargs.values()),
        )

    def update_config(self, **kwargs) -> int:
        if not kwargs:
            return 0
        for col in list(kwargs.keys()):
            if col.endswith("_json") and not isinstance(kwargs[col], str) and kwargs[col] is not None:
                kwargs[col] = json.dumps(kwargs[col])
        set_clause = ", ".join(f"{col} = %s" for col in kwargs)
        return self.db.execute(
            f"UPDATE swfaw_authorization_config SET {set_clause} WHERE app_definition_id = %s",
            tuple(kwargs.values()) + (self.app_id,),
        )

    # ------------------------------------------------------------------
    # Entity Access Control
    # ------------------------------------------------------------------

    def list_entity_access(self) -> List[Dict[str, Any]]:
        config_id = self._get_config_id()
        if config_id is None:
            return []
        rows = self.db.fetch_all(
            "SELECT * FROM swfaw_entity_access_control "
            "WHERE authorization_config_id = %s ORDER BY entity_name",
            (config_id,),
        )
        for r in rows:
            if isinstance(r.get("custom_rules_json"), str):
                try:
                    r["custom_rules_json"] = json.loads(r["custom_rules_json"])
                except (json.JSONDecodeError, TypeError):
                    pass
        return rows

    def get_entity_access(self, entity_name: str) -> Optional[Dict[str, Any]]:
        config_id = self._get_config_id()
        if config_id is None:
            return None
        return self.db.fetch_one(
            "SELECT * FROM swfaw_entity_access_control "
            "WHERE authorization_config_id = %s AND entity_name = %s",
            (config_id, entity_name),
        )

    def add_entity_access(self, entity_name: str, table_name: str, **kwargs) -> int:
        config_id = self._get_config_id()
        if config_id is None:
            raise ValueError("Authorization config not found. Create it first.")
        data = {"authorization_config_id": config_id, "entity_name": entity_name, "table_name": table_name}
        data.update(kwargs)
        if "custom_rules_json" in data and not isinstance(data["custom_rules_json"], str) and data["custom_rules_json"] is not None:
            data["custom_rules_json"] = json.dumps(data["custom_rules_json"])
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        return self.db.insert(
            f"INSERT INTO swfaw_entity_access_control ({columns}) VALUES ({placeholders})",
            tuple(data.values()),
        )

    def update_entity_access(self, entity_name: str, **kwargs) -> int:
        config_id = self._get_config_id()
        if config_id is None:
            return 0
        if not kwargs:
            return 0
        if "custom_rules_json" in kwargs and not isinstance(kwargs["custom_rules_json"], str) and kwargs["custom_rules_json"] is not None:
            kwargs["custom_rules_json"] = json.dumps(kwargs["custom_rules_json"])
        set_clause = ", ".join(f"{col} = %s" for col in kwargs)
        return self.db.execute(
            f"UPDATE swfaw_entity_access_control SET {set_clause} "
            "WHERE authorization_config_id = %s AND entity_name = %s",
            tuple(kwargs.values()) + (config_id, entity_name),
        )

    def remove_entity_access(self, entity_name: str) -> int:
        config_id = self._get_config_id()
        if config_id is None:
            return 0
        return self.db.execute(
            "DELETE FROM swfaw_entity_access_control "
            "WHERE authorization_config_id = %s AND entity_name = %s",
            (config_id, entity_name),
        )
