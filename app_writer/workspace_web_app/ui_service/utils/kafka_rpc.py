"""Shared Kafka RPC pipeline — publish_and_await.

This is the SINGLE utility for all REST → Kafka → response flows.
Every router endpoint calls this instead of duplicating the
publish → register → await → timeout → return pattern.
"""

import asyncio
import logging
import uuid

from fastapi import HTTPException

from workspace_web_app.engine.utils.envelope import build_envelope
from workspace_web_app.ui_service.config import DEFAULT_REQUEST_TIMEOUT
from workspace_web_app.ui_service.correlation_store import CorrelationStore

logger = logging.getLogger(__name__)


async def publish_and_await(
    topic: str,
    message_type: str,
    payload: dict,
    store: CorrelationStore,
    producer,
    timeout: float = DEFAULT_REQUEST_TIMEOUT,
    session_id: str = "",
    app_name: str = "",
) -> dict:
    """Publish a command to Kafka and await the correlated result.

    1. Generate a correlationId.
    2. Register a Future in CorrelationStore.
    3. Build envelope and publish to the given topic.
    4. Await the Future with timeout.
    5. Return the result payload, or raise HTTP 504 on timeout.

    Args:
        topic: Kafka topic to publish to (e.g. "commands.tools").
        message_type: Command type string (e.g. "add_entity").
        payload: Command-specific data.
        store: CorrelationStore instance for request-reply registration.
        producer: Kafka producer instance.
        timeout: Seconds to wait before returning 504. Default 30s.
        session_id: Browser session identifier.
        app_name: Target application name.

    Returns:
        The result dict from the Engine Service.

    Raises:
        HTTPException: 504 if the Engine does not respond within timeout.
    """
    correlation_id = str(uuid.uuid4())
    future = store.register_request(correlation_id)

    envelope = build_envelope(
        type=message_type,
        payload=payload,
        correlation_id=correlation_id,
        session_id=session_id,
        app_name=app_name,
    )

    logger.info(
        "Publishing %s to %s (cid=%s)", message_type, topic, correlation_id
    )
    await producer.send_and_wait(topic, envelope)

    try:
        result = await asyncio.wait_for(future, timeout=timeout)
        logger.info("Received result for %s (cid=%s)", message_type, correlation_id)
        return result
    except asyncio.TimeoutError:
        store.unregister_request(correlation_id)
        logger.warning(
            "Timeout waiting for %s (cid=%s, timeout=%ss)",
            message_type,
            correlation_id,
            timeout,
        )
        raise HTTPException(
            status_code=504,
            detail=f"Engine did not respond within {timeout}s for {message_type}",
        )
