"""UI Service — FastAPI application with CORS and Kafka consumer lifecycle.

Browser-facing gateway. Receives HTTP/WebSocket/SSE requests from the
React frontend, publishes commands to Kafka, consumes results from Kafka,
and pushes them to the browser. Contains ZERO tool logic.
"""

import asyncio
import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from workspace_web_app.ui_service.config import (
    CORS_ORIGINS,
    UI_SERVICE_HOST,
    UI_SERVICE_PORT,
)
from workspace_web_app.ui_service.correlation_store import CorrelationStore
from workspace_web_app.ui_service.kafka_consumer import consume_loop, create_consumer
from workspace_web_app.ui_service.kafka_producer import create_producer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)

# Global references set during lifespan
_producer = None
_consumer = None
_consumer_task: asyncio.Task | None = None
_correlation_store = CorrelationStore()


def get_producer():
    """Return the global Kafka producer (available after startup)."""
    return _producer


def get_correlation_store() -> CorrelationStore:
    """Return the global CorrelationStore instance."""
    return _correlation_store


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Start Kafka producer and consumer on startup, stop on shutdown."""
    global _producer, _consumer, _consumer_task

    logger.info("Starting UI Service — initializing Kafka connections")

    _producer = await create_producer()
    await _producer.start()
    logger.info("Kafka producer started")

    _consumer = await create_consumer()
    await _consumer.start()
    logger.info("Kafka consumer started")

    _consumer_task = asyncio.create_task(
        consume_loop(_consumer, _correlation_store)
    )

    yield

    logger.info("Shutting down UI Service")
    if _consumer_task:
        _consumer_task.cancel()
        try:
            await _consumer_task
        except asyncio.CancelledError:
            pass
    if _consumer:
        await _consumer.stop()
    if _producer:
        await _producer.stop()
    logger.info("UI Service stopped")


app = FastAPI(
    title="Workspace UI Service",
    description="Browser-facing Kafka gateway — zero tool logic.",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware — allow React dev server on port 5174
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Global exception handler — consistent JSON error format (Req 12.1)
# ---------------------------------------------------------------------------


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Return a consistent JSON error for any unhandled exception."""
    logger.exception("Unhandled exception on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": str(exc), "data": None},
    )


# ---------------------------------------------------------------------------
# Request logging middleware — logs method, path, status, duration (Req 12.3)
# ---------------------------------------------------------------------------


@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    """Log every request with method, path, status code, and duration."""
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000
    logger.info(
        "%s %s → %d (%.1fms)",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response


from workspace_web_app.ui_service.routers.apps import router as apps_router  # noqa: E402
from workspace_web_app.ui_service.routers.generation import router as generation_router  # noqa: E402
from workspace_web_app.ui_service.routers.agent import router as agent_router  # noqa: E402
from workspace_web_app.ui_service.routers.definitions import router as definitions_router  # noqa: E402
from workspace_web_app.ui_service.routers.database import router as database_router  # noqa: E402
from workspace_web_app.ui_service.routers.validation import router as validation_router  # noqa: E402
from workspace_web_app.ui_service.routers.tools import router as tools_router  # noqa: E402
from workspace_web_app.ui_service.routers.discussions import router as discussions_router  # noqa: E402
from workspace_web_app.ui_service.routers.github import router as github_router  # noqa: E402
from workspace_web_app.ui_service.routers.ai_settings import router as ai_settings_router  # noqa: E402

app.include_router(apps_router, prefix="/api")
app.include_router(generation_router, prefix="/api")
app.include_router(agent_router, prefix="/api")
app.include_router(definitions_router, prefix="/api")
app.include_router(database_router, prefix="/api")
app.include_router(validation_router, prefix="/api")
app.include_router(tools_router, prefix="/api")
app.include_router(discussions_router, prefix="/api")
app.include_router(github_router, prefix="/api")
app.include_router(ai_settings_router, prefix="/api")


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok", "service": "ui-service"}
