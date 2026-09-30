"""LangChain StructuredTool wrappers for the Definition Editor (direct import)."""

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Input schemas
# ---------------------------------------------------------------------------


class DefinitionGetInput(BaseModel):
    app: str = Field(description="Application name")
    file: str = Field(description="Definition file name (e.g. 'webflux_entity_layer.json')")
    path: str | None = Field(default=None, description="Optional JSON path to retrieve a nested value")


class DefinitionSetInput(BaseModel):
    app: str = Field(description="Application name")
    file: str = Field(description="Definition file name")
    path: str = Field(description="JSON path to set (e.g. 'entities[0].className')")
    value: object = Field(description="Value to set at the path")


class DefinitionListInput(BaseModel):
    app: str = Field(description="Application name")
    prefix: str | None = Field(default=None, description="Optional prefix filter (e.g. 'webflux_' or 'react_')")


# ---------------------------------------------------------------------------
# Tool functions — delegate to tool_handler wrappers
# ---------------------------------------------------------------------------


def _run_definition_get(app: str, file: str, path: str | None = None) -> str:
    from workspace_web_app.engine.handlers.tool_handler import _definition_get

    payload = {"app": app, "file": file}
    if path:
        payload["path"] = path
    return str(_definition_get(payload))


def _run_definition_set(app: str, file: str, path: str, value: object) -> str:
    from workspace_web_app.engine.handlers.tool_handler import _definition_set

    return str(_definition_set({"app": app, "file": file, "path": path, "value": value}))


def _run_definition_list(app: str, prefix: str | None = None) -> str:
    from workspace_web_app.engine.handlers.tool_handler import _definition_list

    payload = {"app": app}
    if prefix:
        payload["prefix"] = prefix
    return str(_definition_list(payload))


# ---------------------------------------------------------------------------
# StructuredTool instances
# ---------------------------------------------------------------------------

definition_get_tool = StructuredTool.from_function(
    func=_run_definition_get, name="definition_get",
    description="Read a definition file or a specific JSON path within it. Use to inspect current application configuration.",
    args_schema=DefinitionGetInput,
)

definition_set_tool = StructuredTool.from_function(
    func=_run_definition_set, name="definition_set",
    description="Set a value at a specific JSON path in a definition file. Use for fine-grained definition edits.",
    args_schema=DefinitionSetInput,
)

definition_list_tool = StructuredTool.from_function(
    func=_run_definition_list, name="definition_list",
    description="List all definition files for an application. Optionally filter by prefix (e.g. 'webflux_' or 'react_').",
    args_schema=DefinitionListInput,
)


def get_tools() -> list[StructuredTool]:
    return [definition_get_tool, definition_set_tool, definition_list_tool]
