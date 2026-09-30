"""LangChain StructuredTool wrappers for the DB Manager (direct import)."""

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Input schemas
# ---------------------------------------------------------------------------


class DBCreateInput(BaseModel):
    name: str = Field(description="Database name to create")
    host: str | None = Field(default=None, description="MySQL host (default: localhost)")
    port: int | None = Field(default=None, description="MySQL port (default: 3306)")
    user: str | None = Field(default=None, description="MySQL user (default: root)")
    password: str | None = Field(default=None, description="MySQL password")


class DBDropInput(BaseModel):
    name: str = Field(description="Database name to drop")
    host: str | None = Field(default=None, description="MySQL host")
    port: int | None = Field(default=None, description="MySQL port")
    user: str | None = Field(default=None, description="MySQL user")
    password: str | None = Field(default=None, description="MySQL password")


class DBListInput(BaseModel):
    host: str | None = Field(default=None, description="MySQL host")
    port: int | None = Field(default=None, description="MySQL port")
    user: str | None = Field(default=None, description="MySQL user")
    password: str | None = Field(default=None, description="MySQL password")


class DBSetupInput(BaseModel):
    name: str = Field(description="Database name to set up (run schema + seed)")
    host: str | None = Field(default=None, description="MySQL host")
    port: int | None = Field(default=None, description="MySQL port")
    user: str | None = Field(default=None, description="MySQL user")
    password: str | None = Field(default=None, description="MySQL password")


class DBQueryInput(BaseModel):
    name: str = Field(description="Database name to query")
    query: dict = Field(description="Query specification dict (table, conditions, limit, etc.)")
    host: str | None = Field(default=None, description="MySQL host")
    port: int | None = Field(default=None, description="MySQL port")
    user: str | None = Field(default=None, description="MySQL user")
    password: str | None = Field(default=None, description="MySQL password")


# ---------------------------------------------------------------------------
# Tool functions — delegate to tool_handler wrappers
# ---------------------------------------------------------------------------


def _build_payload(name: str | None = None, query: dict | None = None, **kwargs) -> dict:
    payload: dict = {}
    if name is not None:
        payload["name"] = name
    if query is not None:
        payload["query"] = query
    for k in ("host", "port", "user", "password"):
        if kwargs.get(k) is not None:
            payload[k] = kwargs[k]
    return payload


def _run_db_create(name: str, host: str | None = None, port: int | None = None, user: str | None = None, password: str | None = None) -> str:
    from workspace_web_app.engine.handlers.tool_handler import _db_create
    return str(_db_create(_build_payload(name=name, host=host, port=port, user=user, password=password)))


def _run_db_drop(name: str, host: str | None = None, port: int | None = None, user: str | None = None, password: str | None = None) -> str:
    from workspace_web_app.engine.handlers.tool_handler import _db_drop
    return str(_db_drop(_build_payload(name=name, host=host, port=port, user=user, password=password)))


def _run_db_list(host: str | None = None, port: int | None = None, user: str | None = None, password: str | None = None) -> str:
    from workspace_web_app.engine.handlers.tool_handler import _db_list
    return str(_db_list(_build_payload(host=host, port=port, user=user, password=password)))


def _run_db_setup(name: str, host: str | None = None, port: int | None = None, user: str | None = None, password: str | None = None) -> str:
    from workspace_web_app.engine.handlers.tool_handler import _db_setup
    return str(_db_setup(_build_payload(name=name, host=host, port=port, user=user, password=password)))


def _run_db_query(name: str, query: dict, host: str | None = None, port: int | None = None, user: str | None = None, password: str | None = None) -> str:
    from workspace_web_app.engine.handlers.tool_handler import _db_query
    return str(_db_query(_build_payload(name=name, query=query, host=host, port=port, user=user, password=password)))


# ---------------------------------------------------------------------------
# StructuredTool instances
# ---------------------------------------------------------------------------

db_create_tool = StructuredTool.from_function(
    func=_run_db_create, name="db_create",
    description="Create a new MySQL database. Use when setting up a new application's database.",
    args_schema=DBCreateInput,
)

db_drop_tool = StructuredTool.from_function(
    func=_run_db_drop, name="db_drop",
    description="Drop a MySQL database. Destructive — requires confirmation.",
    args_schema=DBDropInput,
)

db_list_tool = StructuredTool.from_function(
    func=_run_db_list, name="db_list",
    description="List all MySQL databases on the server.",
    args_schema=DBListInput,
)

db_setup_tool = StructuredTool.from_function(
    func=_run_db_setup, name="db_setup",
    description="Run the full database setup workflow (create schema, apply migrations, seed data).",
    args_schema=DBSetupInput,
)

db_query_tool = StructuredTool.from_function(
    func=_run_db_query, name="db_query",
    description="Execute a structured query against a database. Use instead of raw SQL.",
    args_schema=DBQueryInput,
)


def get_tools() -> list[StructuredTool]:
    return [db_create_tool, db_drop_tool, db_list_tool, db_setup_tool, db_query_tool]
