"""GitHub Crawler REST endpoints — thin Kafka gateway.

Every endpoint is a one-liner delegating to publish_and_await.
No tool logic lives here; the Engine Service handles execution.
"""

from fastapi import APIRouter, Depends, Query

from workspace_web_app.ui_service.main import get_correlation_store, get_producer
from workspace_web_app.ui_service.utils.kafka_rpc import publish_and_await

router = APIRouter(tags=["github"])

TOPIC = "commands.tools"


@router.get("/github/{user}/repos")
async def github_list_repos(
    user: str,
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    """List public repositories for a GitHub user."""
    return await publish_and_await(
        TOPIC, "github_list_repos", {"user": user}, store, producer,
    )


@router.get("/github/{owner}/{repo}")
async def github_repo_info(
    owner: str,
    repo: str,
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    """Get detailed metadata for a GitHub repository."""
    return await publish_and_await(
        TOPIC, "github_repo_info", {"owner": owner, "repo": repo},
        store, producer,
    )


@router.get("/github/{owner}/{repo}/tree")
async def github_tree(
    owner: str,
    repo: str,
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    """Browse the file tree of a GitHub repository."""
    return await publish_and_await(
        TOPIC, "github_tree", {"owner": owner, "repo": repo},
        store, producer,
    )


@router.get("/github/{owner}/{repo}/file")
async def github_read_file(
    owner: str,
    repo: str,
    path: str = Query(..., description="File path within the repository"),
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    """Read a file from a GitHub repository."""
    return await publish_and_await(
        TOPIC, "github_read_file",
        {"owner": owner, "repo": repo, "path": path},
        store, producer,
    )


@router.get("/github/{user}/summary")
async def github_summarize(
    user: str,
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    """Generate a summary of a GitHub user's repositories."""
    return await publish_and_await(
        TOPIC, "github_summarize", {"user": user}, store, producer,
    )
