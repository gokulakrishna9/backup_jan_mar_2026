"""Discussion Tracker REST endpoints — thin Kafka gateway.

Every endpoint is a one-liner delegating to publish_and_await.
No tool logic lives here; the Engine Service handles execution.
"""

from fastapi import APIRouter, Depends, Query

from workspace_web_app.ui_service.main import get_correlation_store, get_producer
from workspace_web_app.ui_service.models.requests import (
    DiscussionDecisionRequest,
    DiscussionLogRequest,
    DiscussionTaskRequest,
    ToolRequest,
)
from workspace_web_app.ui_service.utils.kafka_rpc import publish_and_await

router = APIRouter(tags=["discussions"])

TOPIC = "commands.tools"


@router.post("/discussions/log")
async def discussion_log(
    body: DiscussionLogRequest,
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    """Log a discussion."""
    return await publish_and_await(
        TOPIC, "discussion_log", body.model_dump(), store, producer,
    )


@router.post("/discussions/task")
async def discussion_task(
    body: DiscussionTaskRequest,
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    """Create a task from a discussion."""
    return await publish_and_await(
        TOPIC, "discussion_task", body.model_dump(), store, producer,
    )


@router.post("/discussions/decision")
async def discussion_decision(
    body: DiscussionDecisionRequest,
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    """Record a decision."""
    return await publish_and_await(
        TOPIC, "discussion_decision", body.model_dump(), store, producer,
    )


@router.put("/discussions/{id}/complete")
async def discussion_complete(
    id: str,
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    """Mark a discussion item as complete."""
    return await publish_and_await(
        TOPIC, "discussion_complete", {"id": id}, store, producer,
    )


@router.put("/discussions/{id}/start")
async def discussion_start(
    id: str,
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    """Mark a discussion task as in-progress."""
    return await publish_and_await(
        TOPIC, "discussion_start", {"id": id}, store, producer,
    )


@router.get("/discussions")
async def discussion_list(
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    """List all discussion items."""
    return await publish_and_await(
        TOPIC, "discussion_list", {}, store, producer,
    )


@router.get("/discussions/search")
async def discussion_search(
    q: str = Query(..., description="Search keyword"),
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    """Search discussion items by keyword."""
    return await publish_and_await(
        TOPIC, "discussion_search", {"q": q}, store, producer,
    )


@router.get("/discussions/summary")
async def discussion_summary(
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    """Get a summary of discussions (open tasks, decisions, etc.)."""
    return await publish_and_await(
        TOPIC, "discussion_summary", {}, store, producer,
    )
