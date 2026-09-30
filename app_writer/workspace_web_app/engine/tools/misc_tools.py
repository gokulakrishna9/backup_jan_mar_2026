"""LangChain StructuredTool wrappers for Theme Scraper and Dummy Data Generator (subprocess)."""

import asyncio

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from workspace_web_app.engine.utils.subprocess_run import run_tool_subprocess


# ---------------------------------------------------------------------------
# Input schemas
# ---------------------------------------------------------------------------


class ThemeScrapeInput(BaseModel):
    url: str = Field(description="Website URL to scrape theme/colors from")
    output: str | None = Field(default=None, description="Output path for scraped theme JSON")


class DummyDataInput(BaseModel):
    app: str | None = Field(default=None, description="Application name (uses generated_application/<app>/schema.sql)")
    leaf_records: int | None = Field(default=None, description="Number of leaf records to generate per entity")


# ---------------------------------------------------------------------------
# Tool functions — delegate to tool_handler subprocess wrappers
# ---------------------------------------------------------------------------


def _run_theme_scrape(url: str, output: str | None = None) -> str:
    from workspace_web_app.engine.handlers.tool_handler import _theme_scrape

    payload: dict = {"url": url}
    if output:
        payload["output"] = output
    result = asyncio.get_event_loop().run_until_complete(_theme_scrape(payload))
    if result["returncode"] != 0:
        return f"Error: {result['stderr']}"
    return result["stdout"] or "Theme scraped successfully."


def _run_dummy_data(app: str | None = None, leaf_records: int | None = None) -> str:
    from workspace_web_app.engine.handlers.tool_handler import _dummy_data

    payload: dict = {}
    if app:
        payload["app"] = app
    if leaf_records is not None:
        payload["leaf_records"] = leaf_records
    result = asyncio.get_event_loop().run_until_complete(_dummy_data(payload))
    if result["returncode"] != 0:
        return f"Error: {result['stderr']}"
    return result["stdout"] or "Dummy data generated successfully."


# ---------------------------------------------------------------------------
# StructuredTool instances
# ---------------------------------------------------------------------------

theme_scrape_tool = StructuredTool.from_function(
    func=_run_theme_scrape, name="theme_scrape",
    description="Scrape a website's theme (colors, typography, spacing) and save as a theme JSON file for React generation.",
    args_schema=ThemeScrapeInput,
)

dummy_data_tool = StructuredTool.from_function(
    func=_run_dummy_data, name="dummy_data",
    description="Generate dummy/seed data for an application's database from its schema.sql.",
    args_schema=DummyDataInput,
)


def get_tools() -> list[StructuredTool]:
    return [theme_scrape_tool, dummy_data_tool]
