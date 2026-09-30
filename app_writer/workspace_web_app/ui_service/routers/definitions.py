"""Definition Editor REST endpoints — thin Kafka gateway.

Every endpoint is a one-liner delegating to publish_and_await.
No tool logic lives here; the Engine Service handles execution.
"""

from fastapi import APIRouter, Depends, Query

from workspace_web_app.ui_service.main import get_correlation_store, get_producer
from workspace_web_app.ui_service.models.requests import DefinitionSetRequest
from workspace_web_app.ui_service.utils.kafka_rpc import publish_and_await

router = APIRouter(tags=["definitions"])

TOPIC = "commands.tools"


@router.get("/definitions/{app}")
async def definition_list(
    app: str,
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    """List all definition files for an application."""
    return await publish_and_await(
        TOPIC, "definition_list", {"app": app}, store, producer, app_name=app,
    )


@router.get("/definitions/{app}/{file}")
async def definition_get(
    app: str,
    file: str,
    path: str = Query(default="", description="JSON path within the definition file"),
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    """Get a definition file (optionally at a specific JSON path)."""
    return await publish_and_await(
        TOPIC, "definition_get", {"app": app, "file": file, "path": path},
        store, producer, app_name=app,
    )


@router.put("/definitions/{app}/{file}")
async def definition_set(
    app: str,
    file: str,
    body: DefinitionSetRequest,
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    """Set a value in a definition file at a specific JSON path."""
    return await publish_and_await(
        TOPIC, "definition_set",
        {"app": app, "file": file, **body.model_dump()},
        store, producer, app_name=app,
    )
