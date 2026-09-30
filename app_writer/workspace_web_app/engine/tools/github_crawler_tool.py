"""LangChain StructuredTool wrappers for the GitHub Crawler (subprocess)."""

import asyncio

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from workspace_web_app.engine.utils.subprocess_run import run_tool_subprocess


# ---------------------------------------------------------------------------
# Input schemas
# ---------------------------------------------------------------------------


class GitHubListReposInput(BaseModel):
    user: str = Field(description="GitHub username or organization name")


class GitHubRepoInfoInput(BaseModel):
    owner: str = Field(description="Repository owner (username or org)")
    repo: str = Field(description="Repository name")


class GitHubTreeInput(BaseModel):
    owner: str = Field(description="Repository owner")
    repo: str = Field(description="Repository name")
    branch: str | None = Field(default=None, description="Branch name (default: main/master)")


class GitHubReadFileInput(BaseModel):
    owner: str = Field(description="Repository owner")
    repo: str = Field(description="Repository name")
    path: str = Field(description="File path within the repository")


class GitHubSummarizeInput(BaseModel):
    user: str = Field(description="GitHub username to generate a repository summary for")


# ---------------------------------------------------------------------------
# Tool functions — delegate to tool_handler subprocess wrappers
# ---------------------------------------------------------------------------


def _run_github_list_repos(user: str) -> str:
    from workspace_web_app.engine.handlers.tool_handler import _github_list_repos
    result = asyncio.get_event_loop().run_until_complete(_github_list_repos({"user": user}))
    if result["returncode"] != 0:
        return f"Error: {result['stderr']}"
    return result["stdout"] or "No repositories found."


def _run_github_repo_info(owner: str, repo: str) -> str:
    from workspace_web_app.engine.handlers.tool_handler import _github_repo_info
    result = asyncio.get_event_loop().run_until_complete(_github_repo_info({"owner": owner, "repo": repo}))
    if result["returncode"] != 0:
        return f"Error: {result['stderr']}"
    return result["stdout"] or "No info available."


def _run_github_tree(owner: str, repo: str, branch: str | None = None) -> str:
    from workspace_web_app.engine.handlers.tool_handler import _github_tree
    payload: dict = {"owner": owner, "repo": repo}
    if branch:
        payload["branch"] = branch
    result = asyncio.get_event_loop().run_until_complete(_github_tree(payload))
    if result["returncode"] != 0:
        return f"Error: {result['stderr']}"
    return result["stdout"] or "Empty tree."


def _run_github_read_file(owner: str, repo: str, path: str) -> str:
    from workspace_web_app.engine.handlers.tool_handler import _github_read_file
    result = asyncio.get_event_loop().run_until_complete(
        _github_read_file({"owner": owner, "repo": repo, "path": path})
    )
    if result["returncode"] != 0:
        return f"Error: {result['stderr']}"
    return result["stdout"] or "File is empty."


def _run_github_summarize(user: str) -> str:
    from workspace_web_app.engine.handlers.tool_handler import _github_summarize
    result = asyncio.get_event_loop().run_until_complete(_github_summarize({"user": user}))
    if result["returncode"] != 0:
        return f"Error: {result['stderr']}"
    return result["stdout"] or "No summary available."


# ---------------------------------------------------------------------------
# StructuredTool instances
# ---------------------------------------------------------------------------

github_list_repos_tool = StructuredTool.from_function(
    func=_run_github_list_repos, name="github_list_repos",
    description="List all public GitHub repositories for a user or organization.",
    args_schema=GitHubListReposInput,
)

github_repo_info_tool = StructuredTool.from_function(
    func=_run_github_repo_info, name="github_repo_info",
    description="Get detailed metadata for a GitHub repository (description, stars, language, etc.).",
    args_schema=GitHubRepoInfoInput,
)

github_tree_tool = StructuredTool.from_function(
    func=_run_github_tree, name="github_tree",
    description="Browse a GitHub repository's file tree. Optionally specify a branch.",
    args_schema=GitHubTreeInput,
)

github_read_file_tool = StructuredTool.from_function(
    func=_run_github_read_file, name="github_read_file",
    description="Read the contents of a file from a GitHub repository.",
    args_schema=GitHubReadFileInput,
)

github_summarize_tool = StructuredTool.from_function(
    func=_run_github_summarize, name="github_summarize",
    description="Generate a markdown summary of a GitHub user's repositories with README excerpts.",
    args_schema=GitHubSummarizeInput,
)


def get_tools() -> list[StructuredTool]:
    return [
        github_list_repos_tool, github_repo_info_tool, github_tree_tool,
        github_read_file_tool, github_summarize_tool,
    ]
