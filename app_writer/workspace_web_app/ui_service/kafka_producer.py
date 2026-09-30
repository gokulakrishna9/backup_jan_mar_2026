"""Async Kafka producer for the UI Service.

Publishes commands to commands.tools, commands.agent, and commands.jobs topics.
"""

import json
import logging

from aiokafka import AIOKafkaProducer

from workspace_web_app.ui_service.config import KAFKA_BOOTSTRAP_SERVERS

logger = logging.getLogger(__name__)


async def create_producer() -> AIOKafkaProducer:
    """Create and return an aiokafka producer."""
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
        if isinstance(v, dict)
        else v,
    )
    return producer
