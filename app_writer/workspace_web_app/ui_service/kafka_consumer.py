"""Async Kafka consumer for the UI Service.

Subscribes to results.tools, results.agent, events.jobs, and events.status.
Routes every incoming message to CorrelationStore.resolve() which dispatches
to the correct browser delivery mechanism (Future, WebSocket, or SSE queue).
"""

import json
import logging

from aiokafka import AIOKafkaConsumer

from workspace_web_app.ui_service.config import (
    CONSUME_TOPICS,
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_GROUP_ID,
)
from workspace_web_app.ui_service.correlation_store import CorrelationStore

logger = logging.getLogger(__name__)


async def create_consumer() -> AIOKafkaConsumer:
    """Create and return an aiokafka consumer subscribed to result/event topics."""
    consumer = AIOKafkaConsumer(
        *CONSUME_TOPICS,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=KAFKA_GROUP_ID,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset="latest",
    )
    return consumer


async def consume_loop(consumer: AIOKafkaConsumer, store: CorrelationStore) -> None:
    """Run the consumer loop, routing messages to CorrelationStore.

    Every message is expected to carry a correlationId in the envelope.
    The store dispatches to the correct mechanism (Future, WebSocket, Queue).
    """
    async for msg in consumer:
        try:
            value = msg.value
            correlation_id = value.get("correlationId")
            if not correlation_id:
                logger.warning("Message on %s missing correlationId", msg.topic)
                continue
            await store.resolve(correlation_id, value)
        except Exception:
            logger.exception("Error processing message on %s", msg.topic)
