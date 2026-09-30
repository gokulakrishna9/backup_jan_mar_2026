"""Async Kafka consumer for the Engine Service.

Subscribes to commands.tools, commands.agent, and commands.jobs topics.
Routes messages to the appropriate handler based on topic.
"""

import json
import logging

from aiokafka import AIOKafkaConsumer

from workspace_web_app.engine.config import (
    CONSUME_TOPICS,
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_GROUP_ID,
)

logger = logging.getLogger(__name__)


async def create_consumer() -> AIOKafkaConsumer:
    """Create and return an aiokafka consumer subscribed to command topics."""
    consumer = AIOKafkaConsumer(
        *CONSUME_TOPICS,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=KAFKA_GROUP_ID,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset="latest",
    )
    return consumer


async def consume_loop(consumer: AIOKafkaConsumer, handlers: dict) -> None:
    """Run the consumer loop, dispatching messages to handlers by topic.

    Args:
        consumer: Started AIOKafkaConsumer instance.
        handlers: Mapping of topic name → async handler function.
            Each handler receives (message_value, producer).
    """
    async for msg in consumer:
        topic = msg.topic
        try:
            handler = handlers.get(topic)
            if handler:
                await handler(msg.value)
            else:
                logger.warning("No handler for topic: %s", topic)
        except Exception:
            logger.exception("Error processing message on %s", topic)
