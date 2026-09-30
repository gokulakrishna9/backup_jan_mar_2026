"""Generation REST + WebSocket endpoints — thin Kafka gateway.

POST endpoints publish to commands.tools and await results via publish_and_await.
GET/DELETE job endpoints publish to commands.jobs and await results.
WebSocket endpoint registers the job_id in CorrelationStore and receives
events pushed by the Kafka consumer from events.jobs.
"""

import logging

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from workspace_web_app.ui_service.main import get_correlation_store, get_producer
from workspace_web_app.ui_service.utils.kafka_rpc import publish_and_await

logger = logging.getLogger(__name__)

router = APIRouter(tags=["generation"])

TOOLS_TOPIC = "commands.tools"
JOBS_TOPIC = "commands.jobs"

# Generation timeout is longer than default — these are long-running operations
GENERATION_TIMEOUT = 120


# ── POST generation endpoints (commands.tools) ─────────────────


@router.post("/generate/{app}/full")
async def generate_full(
    app: str,
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    """Start a full generation job (SQL + Java + React)."""
    return await publish_and_await(
        TOOLS_TOPIC, "generate_full", {"app": app}, store, producer,
        timeout=GENERATION_TIMEOUT, app_name=app,
    )


@router.post("/generate/{app}/incremental")
async def generate_incremental(
    app: str,
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    """Start an incremental generation job (skip-sql)."""
    return await publish_and_await(
        TOOLS_TOPIC, "generate_incremental", {"app": app}, store, producer,
        timeout=GENERATION_TIMEOUT, app_name=app,
    )


@router.post("/generate/{app}/sql-only")
async def generate_sql_only(
    app: str,
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    """Start a SQL-only generation job (skip-java)."""
    return await publish_and_await(
        TOOLS_TOPIC, "generate_sql_only", {"app": app}, store, producer,
        timeout=GENERATION_TIMEOUT, app_name=app,
    )


@router.post("/generate/{app}/react")
async def generate_react(
    app: str,
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    """Start a React frontend generation job via REAW."""
    return await publish_and_await(
        TOOLS_TOPIC, "generate_react", {"app": app}, store, producer,
        timeout=GENERATION_TIMEOUT, app_name=app,
    )


# ── GET/DELETE job endpoints (commands.jobs) ────────────────────


@router.get("/generate/{app}/jobs/{job_id}")
async def job_status(
    app: str,
    job_id: str,
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    """Query the status of a generation job."""
    return await publish_and_await(
        JOBS_TOPIC, "job_status", {"app": app, "job_id": job_id},
        store, producer, app_name=app,
    )


@router.delete("/generate/{app}/jobs/{job_id}")
async def job_cancel(
    app: str,
    job_id: str,
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    """Cancel a running generation job."""
    return await publish_and_await(
        JOBS_TOPIC, "job_cancel", {"app": app, "job_id": job_id},
        store, producer, app_name=app,
    )


# ── WebSocket streaming endpoint (events.jobs via CorrelationStore) ─


@router.websocket("/generate/{app}/jobs/{job_id}/stream")
async def job_stream(
    app: str,
    job_id: str,
    ws: WebSocket,
):
    """Stream generation job events to the browser via WebSocket.

    The Kafka consumer pushes events.jobs messages into the CorrelationStore,
    which forwards them to this WebSocket. The job_id is used as the
    correlationId for routing.
    """
    from workspace_web_app.ui_service.main import get_correlation_store as _get_store

    store = _get_store()
    await ws.accept()
    store.register_websocket(job_id, ws)
    logger.info("WebSocket connected for job %s (app=%s)", job_id, app)

    try:
        # Keep the connection alive — the Kafka consumer pushes events
        # via CorrelationStore.resolve() → ws.send_json().
        # We just need to keep reading to detect client disconnect.
        while True:
            # Wait for client messages (ping/pong or close frame)
            await ws.receive_text()
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected for job %s", job_id)
    finally:
        store.unregister_websocket(job_id)
