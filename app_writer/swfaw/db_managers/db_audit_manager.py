"""Database audit manager — CRUD on audit tables (Tier 4c).

Covers: swfaw_audit_config, swfaw_audit_event, swfaw_audit_alert
"""

import json
from typing import Optional, Dict, Any, List
from .db_connection import DbConnection


class DbAuditManager:
    """CRUD operations on audit configuration tables.
    
    Usage:
        am = DbAuditManager(db, app_id=1)
        am.create_config(audit_enabled=1)
        am.add_event("AUTH", "LOGIN_SUCCESS", "INFO", "User {username} logged in")
        am.add_alert("LOGIN_FAILED", threshold=5, time_window_minutes=15)
    """

    def __init__(self, db: DbConnection, app_id: int):
        self.db = db
        self.app_id = app_id

    def _get_config_id(self) -> Optional[int]:
        row = self.db.fetch_one(
            "SELECT id FROM swfaw_audit_config WHERE app_definition_id = %s",
            (self.app_id,),
        )
        return row["id"] if row else None

    # ------------------------------------------------------------------
    # Audit Config (singleton)
    # ------------------------------------------------------------------

    def get_config(self) -> Optional[Dict[str, Any]]:
        row = self.db.fetch_one(
            "SELECT * FROM swfaw_audit_config WHERE app_definition_id = %s",
            (self.app_id,),
        )
        if row:
            for key in list(row.keys()):
                if key.endswith("_json") and isinstance(row[key], str):
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
            f"INSERT INTO swfaw_audit_config ({columns}) VALUES ({placeholders})",
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
            f"UPDATE swfaw_audit_config SET {set_clause} WHERE app_definition_id = %s",
            tuple(kwargs.values()) + (self.app_id,),
        )

    # ------------------------------------------------------------------
    # Audit Events
    # ------------------------------------------------------------------

    def list_events(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        config_id = self._get_config_id()
        if config_id is None:
            return []
        if category:
            return self.db.fetch_all(
                "SELECT * FROM swfaw_audit_event "
                "WHERE audit_config_id = %s AND category = %s ORDER BY event_type",
                (config_id, category),
            )
        return self.db.fetch_all(
            "SELECT * FROM swfaw_audit_event WHERE audit_config_id = %s ORDER BY category, event_type",
            (config_id,),
        )

    def add_event(
        self,
        category: str,
        event_type: str,
        log_level: str,
        message_template: str,
        include_user_agent: bool = False,
        include_location: bool = False,
        include_entity_data: bool = False,
        include_changes: bool = False,
        include_reason: bool = False,
        entities_json: Optional[List[str]] = None,
    ) -> int:
        config_id = self._get_config_id()
        if config_id is None:
            raise ValueError("Audit config not found. Create it first.")
        ent_json = json.dumps(entities_json) if entities_json else None
        sql = (
            "INSERT INTO swfaw_audit_event "
            "(audit_config_id, category, event_type, log_level, message_template, "
            "include_user_agent, include_location, include_entity_data, "
            "include_changes, include_reason, entities_json) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        return self.db.insert(sql, (
            config_id, category, event_type, log_level, message_template,
            int(include_user_agent), int(include_location), int(include_entity_data),
            int(include_changes), int(include_reason), ent_json,
        ))

    def remove_event(self, category: str, event_type: str) -> int:
        config_id = self._get_config_id()
        if config_id is None:
            return 0
        return self.db.execute(
            "DELETE FROM swfaw_audit_event "
            "WHERE audit_config_id = %s AND category = %s AND event_type = %s",
            (config_id, category, event_type),
        )

    # ------------------------------------------------------------------
    # Audit Alerts
    # ------------------------------------------------------------------

    def list_alerts(self) -> List[Dict[str, Any]]:
        config_id = self._get_config_id()
        if config_id is None:
            return []
        rows = self.db.fetch_all(
            "SELECT * FROM swfaw_audit_alert WHERE audit_config_id = %s ORDER BY event_type",
            (config_id,),
        )
        for r in rows:
            if isinstance(r.get("recipients_json"), str):
                r["recipients_json"] = json.loads(r["recipients_json"])
        return rows

    def add_alert(
        self,
        event_type: str,
        threshold: int,
        time_window_minutes: int,
        action: str = "SEND_EMAIL",
        recipients: Optional[List[str]] = None,
    ) -> int:
        config_id = self._get_config_id()
        if config_id is None:
            raise ValueError("Audit config not found. Create it first.")
        recipients_json = json.dumps(recipients or [])
        sql = (
            "INSERT INTO swfaw_audit_alert "
            "(audit_config_id, event_type, threshold, time_window_minutes, action, recipients_json) "
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )
        return self.db.insert(sql, (
            config_id, event_type, threshold, time_window_minutes, action, recipients_json,
        ))

    def remove_alert(self, event_type: str) -> int:
        config_id = self._get_config_id()
        if config_id is None:
            return 0
        return self.db.execute(
            "DELETE FROM swfaw_audit_alert WHERE audit_config_id = %s AND event_type = %s",
            (config_id, event_type),
        )
