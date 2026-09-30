"""Engine Service — FastAPI application with Kafka consumer lifecycle.

Owns all workspace tools and the LangChain agent. Consumes commands
from Kafka, executes tools, and produces results back to Kafka.
"""

import asyncio
import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from workspace_web_app.engine.config import ENGINE_HOST, ENGINE_PORT
from workspace_web_app.engine.kafka_consumer import consume_loop, create_consumer
from workspace_web_app.engine.kafka_producer import create_producer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)

# Global references set during lifespan
_producer = None
_consumer = None
_consumer_task: asyncio.Task | None = None


def _build_topic_handlers(producer):
    """Build the topic → handler mapping.

    Handlers are imported here to avoid circular imports and to allow
    the producer to be injected at startup time.
    """
    from workspace_web_app.engine.handlers.agent_handler import AgentHandler
    from workspace_web_app.engine.handlers.job_handler import JobHandler
    from workspace_web_app.engine.handlers.tool_handler import ToolHandler
    from workspace_web_app.engine.services.agent_service import AgentService
    from workspace_web_app.engine.services.job_manager import JobManager

    job_manager = JobManager()
    agent_service = AgentService()

    tool_handler = ToolHandler(producer, job_manager=job_manager)
    job_handler = JobHandler(job_manager, producer)
    agent_handler = AgentHandler(agent_service, producer)

    async def handle_tools(message: dict):
        """Route tool commands via ToolHandler."""
        await tool_handler.handle(message)

    async def handle_agent(message: dict):
        """Route agent commands via AgentHandler."""
        await agent_handler.handle(message)

    async def handle_jobs(message: dict):
        """Route job commands via JobHandler."""
        await job_handler.handle(message)

    return {
        "commands.tools": handle_tools,
        "commands.agent": handle_agent,
        "commands.jobs": handle_jobs,
    }


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Start Kafka producer and consumer on startup, stop on shutdown."""
    global _producer, _consumer, _consumer_task

    logger.info("Starting Engine Service — initializing Kafka connections")

    _producer = await create_producer()
    await _producer.start()
    logger.info("Kafka producer started")

    _consumer = await create_consumer()
    await _consumer.start()
    logger.info("Kafka consumer started")

    handlers = _build_topic_handlers(_producer)
    _consumer_task = asyncio.create_task(consume_loop(_consumer, handlers))

    yield

    logger.info("Shutting down Engine Service")
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
    logger.info("Engine Service stopped")


app = FastAPI(
    title="Workspace Engine Service",
    description="Owns all workspace tools and the LangChain agent.",
    version="0.1.0",
    lifespan=lifespan,
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


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok", "service": "engine"}
