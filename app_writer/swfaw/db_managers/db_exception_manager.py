"""Database exception manager — CRUD on exception tables (Tier 4b).

Covers: swfaw_exception_config, swfaw_exception_definition, swfaw_exception_message
"""

from typing import Optional, Dict, Any, List
from .db_connection import DbConnection


class DbExceptionManager:
    """CRUD operations on exception configuration tables.
    
    Usage:
        em = DbExceptionManager(db, app_id=1)
        
        # Config (singleton)
        em.create_config(handle_validation_errors=1, log_level="ERROR")
        em.update_config(resp_include_stack_trace=1)
        
        # Custom exception definitions
        em.add_exception("ResourceNotFoundException", 404, "Resource not found")
        
        # Per-entity exception messages
        em.add_message("ResourceNotFoundException", "users", "User not found")
    """

    def __init__(self, db: DbConnection, app_id: int):
        self.db = db
        self.app_id = app_id

    # ------------------------------------------------------------------
    # Exception Config (singleton)
    # ------------------------------------------------------------------

    def get_config(self) -> Optional[Dict[str, Any]]:
        return self.db.fetch_one(
            "SELECT * FROM swfaw_exception_config WHERE app_definition_id = %s",
            (self.app_id,),
        )

    def create_config(self, **kwargs) -> int:
        kwargs.setdefault("app_definition_id", self.app_id)
        columns = ", ".join(kwargs.keys())
        placeholders = ", ".join(["%s"] * len(kwargs))
        return self.db.insert(
            f"INSERT INTO swfaw_exception_config ({columns}) VALUES ({placeholders})",
            tuple(kwargs.values()),
        )

    def update_config(self, **kwargs) -> int:
        if not kwargs:
            return 0
        set_clause = ", ".join(f"{col} = %s" for col in kwargs)
        return self.db.execute(
            f"UPDATE swfaw_exception_config SET {set_clause} WHERE app_definition_id = %s",
            tuple(kwargs.values()) + (self.app_id,),
        )

    # ------------------------------------------------------------------
    # Exception Definitions
    # ------------------------------------------------------------------

    def list_exceptions(self) -> List[Dict[str, Any]]:
        return self.db.fetch_all(
            "SELECT * FROM swfaw_exception_definition WHERE app_definition_id = %s ORDER BY class_name",
            (self.app_id,),
        )

    def add_exception(
        self,
        class_name: str,
        http_status: int,
        default_message: str,
        package_name: str = "com.example.exception",
        include_timestamp: bool = True,
        include_stack_trace: bool = False,
        include_field_errors: bool = False,
    ) -> int:
        sql = (
            "INSERT INTO swfaw_exception_definition "
            "(app_definition_id, class_name, package_name, http_status, default_message, "
            "include_timestamp, include_stack_trace, include_field_errors) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        )
        return self.db.insert(sql, (
            self.app_id, class_name, package_name, http_status, default_message,
            int(include_timestamp), int(include_stack_trace), int(include_field_errors),
        ))

    def remove_exception(self, class_name: str) -> int:
        return self.db.execute(
            "DELETE FROM swfaw_exception_definition "
            "WHERE app_definition_id = %s AND class_name = %s",
            (self.app_id, class_name),
        )

    # ------------------------------------------------------------------
    # Exception Messages (per-entity)
    # ------------------------------------------------------------------

    def list_messages(self, exception_class: Optional[str] = None) -> List[Dict[str, Any]]:
        if exception_class:
            return self.db.fetch_all(
                "SELECT * FROM swfaw_exception_message "
                "WHERE app_definition_id = %s AND exception_class = %s ORDER BY target_name",
                (self.app_id, exception_class),
            )
        return self.db.fetch_all(
            "SELECT * FROM swfaw_exception_message "
            "WHERE app_definition_id = %s ORDER BY exception_class, target_name",
            (self.app_id,),
        )

    def add_message(self, exception_class: str, target_name: str, message: str) -> int:
        sql = (
            "INSERT INTO swfaw_exception_message "
            "(app_definition_id, exception_class, target_name, message) "
            "VALUES (%s, %s, %s, %s)"
        )
        return self.db.insert(sql, (self.app_id, exception_class, target_name, message))

    def update_message(self, exception_class: str, target_name: str, message: str) -> int:
        return self.db.execute(
            "UPDATE swfaw_exception_message SET message = %s "
            "WHERE app_definition_id = %s AND exception_class = %s AND target_name = %s",
            (message, self.app_id, exception_class, target_name),
        )

    def remove_message(self, exception_class: str, target_name: str) -> int:
        return self.db.execute(
            "DELETE FROM swfaw_exception_message "
            "WHERE app_definition_id = %s AND exception_class = %s AND target_name = %s",
            (self.app_id, exception_class, target_name),
        )
