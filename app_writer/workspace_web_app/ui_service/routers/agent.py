"""Agent chat REST + SSE endpoints — thin Kafka gateway.

POST /chat publishes to commands.agent and returns an SSE stream
from results.agent via CorrelationStore's SSE queue mechanism.

GET/DELETE /history/{app_name} use publish_and_await for request-reply.
"""

import asyncio
import json
import logging
import uuid

from fastapi import APIRouter, Depends
from sse_starlette.sse import EventSourceResponse

from workspace_web_app.ui_service.main import get_correlation_store, get_producer
from workspace_web_app.ui_service.models.requests import AgentChatRequest
from workspace_web_app.ui_service.utils.kafka_rpc import publish_and_await
from workspace_web_app.engine.utils.envelope import build_envelope

logger = logging.getLogger(__name__)

router = APIRouter(tags=["agent"])

AGENT_TOPIC = "commands.agent"

# Agent chat timeout — longer than default for LLM reasoning + tool calls
AGENT_CHAT_TIMEOUT = 120


# ── POST /agent/chat — SSE streaming ───────────────────────────


@router.post("/agent/chat")
async def agent_chat(
    body: AgentChatRequest,
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    """Send a chat message to the agent and stream the response via SSE.

    1. Generate a correlationId.
    2. Register an SSE queue in CorrelationStore.
    3. Publish to commands.agent with type "agent_chat".
    4. Return an SSE EventSourceResponse that reads from the queue.
    5. Each SSE event is a JSON object with type and data.
    6. When a "message" type event arrives, it's the final event — close the stream.
    """
    correlation_id = str(uuid.uuid4())
    queue = store.register_sse(correlation_id)

    envelope = build_envelope(
        type="agent_chat",
        payload={"message": body.message},
        correlation_id=correlation_id,
        session_id=body.session_id,
        app_name=body.app_name,
    )

    logger.info(
        "Publishing agent_chat to %s (cid=%s, app=%s)",
        AGENT_TOPIC, correlation_id, body.app_name,
    )
    await producer.send_and_wait(AGENT_TOPIC, envelope)

    async def event_generator():
        """Yield SSE events from the CorrelationStore queue."""
        try:
            while True:
                try:
                    event = await asyncio.wait_for(
                        queue.get(), timeout=AGENT_CHAT_TIMEOUT
                    )
                except asyncio.TimeoutError:
                    # Send a timeout error event and close
                    yield {
                        "event": "error",
                        "data": json.dumps({
                            "type": "error",
                            "data": f"Agent did not respond within {AGENT_CHAT_TIMEOUT}s",
                        }),
                    }
                    return

                event_type = event.get("type", "message")
                yield {
                    "event": event_type,
                    "data": json.dumps(event),
                }

                # "message" type is the final event — close the stream
                if event_type == "message":
                    return
        finally:
            store.unregister_sse(correlation_id)

    return EventSourceResponse(event_generator())


# ── GET /agent/history/{app_name} — fetch conversation history ─


@router.get("/agent/history/{app_name}")
async def get_history(
    app_name: str,
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    """Fetch conversation history for a specific application."""
    return await publish_and_await(
        AGENT_TOPIC, "agent_get_history",
        {"app_name": app_name},
        store, producer, app_name=app_name,
    )


# ── DELETE /agent/history/{app_name} — clear conversation history


@router.delete("/agent/history/{app_name}")
async def clear_history(
    app_name: str,
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    """Clear conversation history for a specific application."""
    return await publish_and_await(
        AGENT_TOPIC, "agent_clear_history",
        {"app_name": app_name},
        store, producer, app_name=app_name,
    )
