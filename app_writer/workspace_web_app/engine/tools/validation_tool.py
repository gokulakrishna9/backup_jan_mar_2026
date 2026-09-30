"""LangChain StructuredTool wrappers for the App Validator (subprocess)."""

import asyncio

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from workspace_web_app.engine.utils.subprocess_run import run_tool_subprocess


# ---------------------------------------------------------------------------
# Input schemas
# ---------------------------------------------------------------------------


class ValidateBackendInput(BaseModel):
    app: str = Field(description="Application name to validate backend definitions for")


class ValidateFrontendInput(BaseModel):
    app: str = Field(description="Application name to validate frontend definitions for")


class ValidateAPICoverageInput(BaseModel):
    app: str = Field(description="Application name to validate API coverage for")
    backend_url: str | None = Field(
        default=None,
        description="Running backend URL for live CRUD testing (e.g. 'http://localhost:8081'). Omit for definition-only analysis.",
    )


# ---------------------------------------------------------------------------
# Tool functions — delegate to tool_handler subprocess wrappers
# ---------------------------------------------------------------------------


def _run_validate_backend(app: str) -> str:
    from workspace_web_app.engine.handlers.tool_handler import _validate_backend
    result = asyncio.get_event_loop().run_until_complete(_validate_backend({"app": app}))
    if result["returncode"] != 0:
        return f"Validation failed: {result['stderr']}"
    return result["stdout"] or "Backend validation passed."


def _run_validate_frontend(app: str) -> str:
    from workspace_web_app.engine.handlers.tool_handler import _validate_frontend
    result = asyncio.get_event_loop().run_until_complete(_validate_frontend({"app": app}))
    if result["returncode"] != 0:
        return f"Validation failed: {result['stderr']}"
    return result["stdout"] or "Frontend validation passed."


def _run_validate_api_coverage(app: str, backend_url: str | None = None) -> str:
    from workspace_web_app.engine.handlers.tool_handler import _validate_api_coverage
    payload: dict = {"app": app}
    if backend_url:
        payload["backend_url"] = backend_url
    result = asyncio.get_event_loop().run_until_complete(_validate_api_coverage(payload))
    if result["returncode"] != 0:
        return f"Validation failed: {result['stderr']}"
    return result["stdout"] or "API coverage validation passed."


# ---------------------------------------------------------------------------
# StructuredTool instances
# ---------------------------------------------------------------------------

validate_backend_tool = StructuredTool.from_function(
    func=_run_validate_backend, name="validate_backend",
    description="Validate backend definition files for consistency and completeness. Reads only application_definitions/ JSON.",
    args_schema=ValidateBackendInput,
)

validate_frontend_tool = StructuredTool.from_function(
    func=_run_validate_frontend, name="validate_frontend",
    description="Validate frontend (React) definition files for consistency and completeness.",
    args_schema=ValidateFrontendInput,
)

validate_api_coverage_tool = StructuredTool.from_function(
    func=_run_validate_api_coverage, name="validate_api_coverage",
    description="Validate API coverage. Without backend_url: definition-only analysis. With backend_url: live CRUD lifecycle testing.",
    args_schema=ValidateAPICoverageInput,
)


def get_tools() -> list[StructuredTool]:
    return [validate_backend_tool, validate_frontend_tool, validate_api_coverage_tool]
