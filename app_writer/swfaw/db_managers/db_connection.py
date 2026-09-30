"""Database connection management for swfaw_definition_store."""

import json
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple

try:
    import mysql.connector
    from mysql.connector import pooling
except ImportError:
    raise ImportError(
        "mysql-connector-python is required. Install with: pip install mysql-connector-python"
    )


class DbConnection:
    """Manages MySQL connections to the swfaw_definition_store database.
    
    Supports connection pooling and config file loading from ~/.swfaw/db_config.json.
    
    Usage:
        # Direct connection
        db = DbConnection(host="localhost", database="swfaw_definition_store")
        
        # From config file
        db = DbConnection.from_config()
        
        # Execute queries
        rows = db.fetch_all("SELECT * FROM swfaw_app_definition WHERE is_active = 1")
        row = db.fetch_one("SELECT * FROM swfaw_app_definition WHERE id = %s", (1,))
        db.execute("UPDATE swfaw_app_definition SET project_name = %s WHERE id = %s", ("MyApp", 1))
        new_id = db.insert("INSERT INTO swfaw_app_definition (project_name) VALUES (%s)", ("MyApp",))
    """

    DEFAULT_CONFIG_PATH = Path.home() / ".swfaw" / "db_config.json"
    DEFAULT_CONFIG = {
        "host": "localhost",
        "port": 3306,
        "database": "swfaw_definition_store",
        "user": "root",
        "password": "password",
        "pool_name": "swfaw_pool",
        "pool_size": 5,
    }

    def __init__(
        self,
        host: str = "localhost",
        port: int = 3306,
        database: str = "swfaw_definition_store",
        user: str = "root",
        password: str = "password",
        pool_size: int = 5,
    ):
        self.config = {
            "host": host,
            "port": port,
            "database": database,
            "user": user,
            "password": password,
        }
        self.pool_size = pool_size
        self._pool: Optional[pooling.MySQLConnectionPool] = None

    @classmethod
    def from_config(cls, config_path: Optional[str] = None) -> "DbConnection":
        """Create a DbConnection from a config file.
        
        Args:
            config_path: Path to config JSON file. Defaults to ~/.swfaw/db_config.json
            
        Returns:
            DbConnection instance
        """
        path = Path(config_path) if config_path else cls.DEFAULT_CONFIG_PATH
        
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
        else:
            cfg = cls.DEFAULT_CONFIG.copy()

        return cls(
            host=cfg.get("host", "localhost"),
            port=cfg.get("port", 3306),
            database=cfg.get("database", "swfaw_definition_store"),
            user=cfg.get("user", cfg.get("username", "root")),
            password=cfg.get("password", "password"),
            pool_size=cfg.get("pool_size", 5),
        )

    # ------------------------------------------------------------------
    # Connection management
    # ------------------------------------------------------------------

    def _get_pool(self) -> pooling.MySQLConnectionPool:
        """Get or create the connection pool."""
        if self._pool is None:
            self._pool = pooling.MySQLConnectionPool(
                pool_name="swfaw_pool",
                pool_size=self.pool_size,
                pool_reset_session=True,
                **self.config,
            )
        return self._pool

    def get_connection(self) -> mysql.connector.MySQLConnection:
        """Get a connection from the pool."""
        return self._get_pool().get_connection()

    def close(self) -> None:
        """Close the connection pool."""
        self._pool = None

    # ------------------------------------------------------------------
    # Query helpers
    # ------------------------------------------------------------------

    def fetch_all(self, sql: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """Execute a SELECT and return all rows as dicts.
        
        Args:
            sql: SQL query string
            params: Query parameters
            
        Returns:
            List of row dicts
        """
        conn = self.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, params or ())
            rows = cursor.fetchall()
            cursor.close()
            return rows
        finally:
            conn.close()

    def fetch_one(self, sql: str, params: Optional[tuple] = None) -> Optional[Dict[str, Any]]:
        """Execute a SELECT and return one row as a dict.
        
        Args:
            sql: SQL query string
            params: Query parameters
            
        Returns:
            Row dict or None
        """
        conn = self.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, params or ())
            row = cursor.fetchone()
            cursor.close()
            return row
        finally:
            conn.close()

    def execute(self, sql: str, params: Optional[tuple] = None) -> int:
        """Execute an INSERT/UPDATE/DELETE and return affected row count.
        
        Args:
            sql: SQL statement
            params: Query parameters
            
        Returns:
            Number of affected rows
        """
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, params or ())
            conn.commit()
            affected = cursor.rowcount
            cursor.close()
            return affected
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def insert(self, sql: str, params: Optional[tuple] = None) -> int:
        """Execute an INSERT and return the last inserted ID.
        
        Args:
            sql: INSERT statement
            params: Query parameters
            
        Returns:
            Last inserted auto-increment ID
        """
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, params or ())
            conn.commit()
            last_id = cursor.lastrowid
            cursor.close()
            return last_id
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def execute_many(self, sql: str, params_list: List[tuple]) -> int:
        """Execute a statement for multiple parameter sets.
        
        Args:
            sql: SQL statement with placeholders
            params_list: List of parameter tuples
            
        Returns:
            Number of affected rows
        """
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.executemany(sql, params_list)
            conn.commit()
            affected = cursor.rowcount
            cursor.close()
            return affected
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def execute_transaction(self, operations: List[Tuple[str, Optional[tuple]]]) -> List[int]:
        """Execute multiple statements in a single transaction.
        
        Args:
            operations: List of (sql, params) tuples
            
        Returns:
            List of lastrowid for each operation
        """
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            results = []
            for sql, params in operations:
                cursor.execute(sql, params or ())
                results.append(cursor.lastrowid)
            conn.commit()
            cursor.close()
            return results
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def table_exists(self, table_name: str) -> bool:
        """Check if a table exists in the database.
        
        Args:
            table_name: Name of the table
            
        Returns:
            True if table exists
        """
        row = self.fetch_one(
            "SELECT COUNT(*) as cnt FROM information_schema.tables "
            "WHERE table_schema = %s AND table_name = %s",
            (self.config["database"], table_name),
        )
        return row is not None and row["cnt"] > 0
