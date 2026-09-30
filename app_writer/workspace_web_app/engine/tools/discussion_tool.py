"""LangChain StructuredTool wrappers for the Discussion Tracker (subprocess)."""

import asyncio

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from workspace_web_app.engine.utils.subprocess_run import run_tool_subprocess


# ---------------------------------------------------------------------------
# Input schemas
# ---------------------------------------------------------------------------


class DiscussionLogInput(BaseModel):
    message: str = Field(description="Discussion message to log")


class DiscussionTaskInput(BaseModel):
    title: str = Field(description="Task title")
    description: str | None = Field(default=None, description="Task description")


class DiscussionDecisionInput(BaseModel):
    title: str = Field(description="Decision title")
    rationale: str | None = Field(default=None, description="Rationale for the decision")


class DiscussionCompleteInput(BaseModel):
    id: str = Field(description="Task ID to mark as completed")


class DiscussionStartInput(BaseModel):
    id: str = Field(description="Task ID to mark as in-progress")
    notes: str | None = Field(default=None, description="Optional notes for starting the task")


class DiscussionListInput(BaseModel):
    type: str | None = Field(default=None, description="Filter by type: 'task', 'decision', 'discussion'")


class DiscussionSearchInput(BaseModel):
    query: str = Field(description="Search keyword to find discussions, tasks, or decisions")


class DiscussionSummaryInput(BaseModel):
    pass


# ---------------------------------------------------------------------------
# Tool functions — delegate to tool_handler subprocess wrappers
# ---------------------------------------------------------------------------


def _run_discussion_log(message: str) -> str:
    from workspace_web_app.engine.handlers.tool_handler import _discussion_log
    result = asyncio.get_event_loop().run_until_complete(_discussion_log({"message": message}))
    if result["returncode"] != 0:
        return f"Error: {result['stderr']}"
    return result["stdout"] or "Discussion logged."


def _run_discussion_task(title: str, description: str | None = None) -> str:
    from workspace_web_app.engine.handlers.tool_handler import _discussion_task
    payload: dict = {"title": title}
    if description:
        payload["description"] = description
    result = asyncio.get_event_loop().run_until_complete(_discussion_task(payload))
    if result["returncode"] != 0:
        return f"Error: {result['stderr']}"
    return result["stdout"] or "Task created."


def _run_discussion_decision(title: str, rationale: str | None = None) -> str:
    from workspace_web_app.engine.handlers.tool_handler import _discussion_decision
    payload: dict = {"title": title}
    if rationale:
        payload["rationale"] = rationale
    result = asyncio.get_event_loop().run_until_complete(_discussion_decision(payload))
    if result["returncode"] != 0:
        return f"Error: {result['stderr']}"
    return result["stdout"] or "Decision recorded."


def _run_discussion_complete(id: str) -> str:
    from workspace_web_app.engine.handlers.tool_handler import _discussion_complete
    result = asyncio.get_event_loop().run_until_complete(_discussion_complete({"id": id}))
    if result["returncode"] != 0:
        return f"Error: {result['stderr']}"
    return result["stdout"] or "Task completed."


def _run_discussion_start(id: str, notes: str | None = None) -> str:
    from workspace_web_app.engine.handlers.tool_handler import _discussion_start
    payload: dict = {"id": id}
    if notes:
        payload["notes"] = notes
    result = asyncio.get_event_loop().run_until_complete(_discussion_start(payload))
    if result["returncode"] != 0:
        return f"Error: {result['stderr']}"
    return result["stdout"] or "Task started."


def _run_discussion_list(type: str | None = None) -> str:
    from workspace_web_app.engine.handlers.tool_handler import _discussion_list
    payload: dict = {}
    if type:
        payload["type"] = type
    result = asyncio.get_event_loop().run_until_complete(_discussion_list(payload))
    if result["returncode"] != 0:
        return f"Error: {result['stderr']}"
    return result["stdout"] or "No discussions found."


def _run_discussion_search(query: str) -> str:
    from workspace_web_app.engine.handlers.tool_handler import _discussion_search
    result = asyncio.get_event_loop().run_until_complete(_discussion_search({"query": query}))
    if result["returncode"] != 0:
        return f"Error: {result['stderr']}"
    return result["stdout"] or "No results found."


def _run_discussion_summary() -> str:
    from workspace_web_app.engine.handlers.tool_handler import _discussion_summary
    result = asyncio.get_event_loop().run_until_complete(_discussion_summary({}))
    if result["returncode"] != 0:
        return f"Error: {result['stderr']}"
    return result["stdout"] or "No summary available."


# ---------------------------------------------------------------------------
# StructuredTool instances
# ---------------------------------------------------------------------------

discussion_log_tool = StructuredTool.from_function(
    func=_run_discussion_log, name="discussion_log",
    description="Log a discussion entry. Use to record conversations, notes, or context.",
    args_schema=DiscussionLogInput,
)

discussion_task_tool = StructuredTool.from_function(
    func=_run_discussion_task, name="discussion_task",
    description="Create a new task in the Discussion Tracker. Always create a task before implementing changes.",
    args_schema=DiscussionTaskInput,
)

discussion_decision_tool = StructuredTool.from_function(
    func=_run_discussion_decision, name="discussion_decision",
    description="Record a decision with rationale in the Discussion Tracker.",
    args_schema=DiscussionDecisionInput,
)

discussion_complete_tool = StructuredTool.from_function(
    func=_run_discussion_complete, name="discussion_complete",
    description="Mark a task as completed in the Discussion Tracker.",
    args_schema=DiscussionCompleteInput,
)

discussion_start_tool = StructuredTool.from_function(
    func=_run_discussion_start, name="discussion_start",
    description="Mark a task as in-progress in the Discussion Tracker.",
    args_schema=DiscussionStartInput,
)

discussion_list_tool = StructuredTool.from_function(
    func=_run_discussion_list, name="discussion_list",
    description="List discussions, tasks, or decisions. Optionally filter by type.",
    args_schema=DiscussionListInput,
)

discussion_search_tool = StructuredTool.from_function(
    func=_run_discussion_search, name="discussion_search",
    description="Search discussions, tasks, and decisions by keyword.",
    args_schema=DiscussionSearchInput,
)

discussion_summary_tool = StructuredTool.from_function(
    func=_run_discussion_summary, name="discussion_summary",
    description="Get a summary of open tasks, in-progress tasks, recent decisions, and earmarked items.",
    args_schema=DiscussionSummaryInput,
)


def get_tools() -> list[StructuredTool]:
    return [
        discussion_log_tool, discussion_task_tool, discussion_decision_tool,
        discussion_complete_tool, discussion_start_tool, discussion_list_tool,
        discussion_search_tool, discussion_summary_tool,
    ]
