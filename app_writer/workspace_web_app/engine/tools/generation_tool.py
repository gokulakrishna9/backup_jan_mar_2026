"""LangChain StructuredTool wrappers for code generation commands.

Generation tools start background jobs via the JobManager. They use
run_tool_subprocess for REAW (module name conflicts) and Phase 3 for
backend generation.
"""

import asyncio

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from workspace_web_app.engine.config import TOOL_PATHS, WORKSPACE_ROOT
from workspace_web_app.engine.utils.subprocess_run import run_tool_subprocess


# ---------------------------------------------------------------------------
# Input schemas
# ---------------------------------------------------------------------------


class GenerateFullInput(BaseModel):
    app: str = Field(description="Application name to generate full backend code for")


class GenerateIncrementalInput(BaseModel):
    app: str = Field(description="Application name for incremental generation (skip-sql, only dirty files)")


class GenerateSQLOnlyInput(BaseModel):
    app: str = Field(description="Application name to generate SQL schema only")


class GenerateReactInput(BaseModel):
    app: str = Field(description="Application name to generate React frontend for")


# ---------------------------------------------------------------------------
# Tool functions
# ---------------------------------------------------------------------------


def _run_generate_full(app: str) -> str:
    cmd = f"python {TOOL_PATHS['phase3']} --app {app} --output generated_application/{app} --full"
    result = asyncio.get_event_loop().run_until_complete(run_tool_subprocess(cmd, cwd=WORKSPACE_ROOT))
    if result["returncode"] != 0:
        return f"Generation failed: {result['stderr']}"
    return result["stdout"] or "Full generation completed successfully."


def _run_generate_incremental(app: str) -> str:
    cmd = f"python {TOOL_PATHS['phase3']} --app {app} --output generated_application/{app} --skip-sql"
    result = asyncio.get_event_loop().run_until_complete(run_tool_subprocess(cmd, cwd=WORKSPACE_ROOT))
    if result["returncode"] != 0:
        return f"Generation failed: {result['stderr']}"
    return result["stdout"] or "Incremental generation completed successfully."


def _run_generate_sql_only(app: str) -> str:
    cmd = f"python {TOOL_PATHS['phase3']} --app {app} --output generated_application/{app} --skip-java"
    result = asyncio.get_event_loop().run_until_complete(run_tool_subprocess(cmd, cwd=WORKSPACE_ROOT))
    if result["returncode"] != 0:
        return f"Generation failed: {result['stderr']}"
    return result["stdout"] or "SQL-only generation completed successfully."


def _run_generate_react(app: str) -> str:
    from workspace_web_app.engine.config import APPLICATION_DEFINITIONS_DIR

    cmd = (
        f"python {TOOL_PATHS['reaw']}"
        f" --input {APPLICATION_DEFINITIONS_DIR}/{app}"
        f" --output generated_application/{app}/react_app"
    )
    result = asyncio.get_event_loop().run_until_complete(run_tool_subprocess(cmd, cwd=WORKSPACE_ROOT))
    if result["returncode"] != 0:
        return f"React generation failed: {result['stderr']}"
    return result["stdout"] or "React generation completed successfully."


# ---------------------------------------------------------------------------
# StructuredTool instances
# ---------------------------------------------------------------------------

generate_full_tool = StructuredTool.from_function(
    func=_run_generate_full, name="generate_full",
    description="Run full code generation (SQL + Java + config) for an application. Use when all definition files need regeneration.",
    args_schema=GenerateFullInput,
)

generate_incremental_tool = StructuredTool.from_function(
    func=_run_generate_incremental, name="generate_incremental",
    description="Run incremental generation (skip SQL, only regenerate dirty Java files). Use after small definition changes.",
    args_schema=GenerateIncrementalInput,
)

generate_sql_only_tool = StructuredTool.from_function(
    func=_run_generate_sql_only, name="generate_sql_only",
    description="Generate only the SQL schema file. Use when only database schema changes are needed.",
    args_schema=GenerateSQLOnlyInput,
)

generate_react_tool = StructuredTool.from_function(
    func=_run_generate_react, name="generate_react",
    description="Generate the React frontend application from react definition files. Uses REAW via subprocess.",
    args_schema=GenerateReactInput,
)


def get_tools() -> list[StructuredTool]:
    return [generate_full_tool, generate_incremental_tool, generate_sql_only_tool, generate_react_tool]
