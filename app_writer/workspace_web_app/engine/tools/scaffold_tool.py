"""LangChain StructuredTool wrapper for the App Def Manager scaffold command."""

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field


class ScaffoldAppInput(BaseModel):
    """Input schema for scaffolding a new application definition set."""

    app: str = Field(description="Application name (kebab-case, e.g. 'job-portal')")
    entities: list[dict] = Field(
        default_factory=list,
        description="List of entity descriptions, each with 'name' (PascalCase) and optional 'fields' list",
    )
    db_name: str | None = Field(
        default=None,
        description="Database name. Defaults to snake_case of app name",
    )


def _run_scaffold_app(app: str, entities: list[dict] | None = None, db_name: str | None = None) -> str:
    from workspace_web_app.engine.handlers.tool_handler import _scaffold_app

    payload = {"app": app, "entities": entities or []}
    if db_name:
        payload["db_name"] = db_name
    result = _scaffold_app(payload)
    return str(result)


scaffold_app_tool = StructuredTool.from_function(
    func=_run_scaffold_app,
    name="scaffold_app",
    description=(
        "Scaffold a new application definition set. Creates all 12+ definition files "
        "(webflux layers, react config, generation status) for a new app. "
        "Use this when the user wants to create a brand new application."
    ),
    args_schema=ScaffoldAppInput,
)


def get_tools() -> list[StructuredTool]:
    return [scaffold_app_tool]
