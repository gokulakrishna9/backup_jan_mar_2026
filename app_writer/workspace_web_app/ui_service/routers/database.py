"""DB Manager REST endpoints — thin Kafka gateway.

Every endpoint is a one-liner delegating to publish_and_await.
No tool logic lives here; the Engine Service handles execution.
Destructive operations require ``confirm=true`` query parameter (Req 12.2).
"""

from fastapi import APIRouter, Depends, HTTPException, Query

from workspace_web_app.ui_service.main import get_correlation_store, get_producer
from workspace_web_app.ui_service.models.requests import (
    DatabaseCreateRequest,
    DatabaseQueryRequest,
)
from workspace_web_app.ui_service.utils.kafka_rpc import publish_and_await

router = APIRouter(tags=["databases"])

TOPIC = "commands.tools"


@router.get("/databases")
async def db_list(
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    """List all databases."""
    return await publish_and_await(TOPIC, "db_list", {}, store, producer)


@router.post("/databases")
async def db_create(
    body: DatabaseCreateRequest,
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    """Create a new database."""
    return await publish_and_await(
        TOPIC, "db_create", body.model_dump(), store, producer,
    )


@router.delete("/databases/{name}")
async def db_drop(
    name: str,
    confirm: bool = Query(False, description="Must be true to confirm destructive operation"),
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    """Drop a database. Requires confirm=true."""
    if not confirm:
        raise HTTPException(status_code=400, detail="Destructive operation requires confirm=true")
    return await publish_and_await(
        TOPIC, "db_drop", {"name": name}, store, producer,
    )


@router.post("/databases/{name}/setup")
async def db_setup(
    name: str,
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    """Set up a database (run schema migrations)."""
    return await publish_and_await(
        TOPIC, "db_setup", {"name": name}, store, producer,
    )


@router.post("/databases/{name}/query")
async def db_query(
    name: str,
    body: DatabaseQueryRequest,
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    """Execute a query against a database."""
    return await publish_and_await(
        TOPIC, "db_query", {"name": name, **body.model_dump()}, store, producer,
    )
