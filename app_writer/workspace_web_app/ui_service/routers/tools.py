"""Theme Scraper and Dummy Data REST endpoints — thin Kafka gateway.

Every endpoint is a one-liner delegating to publish_and_await.
No tool logic lives here; the Engine Service handles execution.
"""

from fastapi import APIRouter, Depends

from workspace_web_app.ui_service.main import get_correlation_store, get_producer
from workspace_web_app.ui_service.models.requests import ToolRequest
from workspace_web_app.ui_service.utils.kafka_rpc import publish_and_await

router = APIRouter(tags=["tools"])

TOPIC = "commands.tools"


@router.post("/tools/theme-scrape")
async def theme_scrape(
    body: ToolRequest,
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    """Scrape a website theme."""
    return await publish_and_await(
        TOPIC, "theme_scrape", body.model_dump(), store, producer,
    )


@router.post("/tools/dummy-data")
async def dummy_data(
    body: ToolRequest,
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    """Generate dummy data for an application."""
    return await publish_and_await(
        TOPIC, "dummy_data", body.model_dump(), store, producer,
    )
