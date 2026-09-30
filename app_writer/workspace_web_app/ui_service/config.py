"""UI Service configuration — ports, Kafka config, CORS origins."""

import os

# Kafka
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

CONSUME_TOPICS = ["results.tools", "results.agent", "events.jobs", "events.status"]
PRODUCE_TOPICS = ["commands.tools", "commands.agent", "commands.jobs"]

KAFKA_GROUP_ID = "ui-service"

# UI Service
UI_SERVICE_HOST = "0.0.0.0"
UI_SERVICE_PORT = 8001

# CORS — allow React dev server and common local origins
CORS_ORIGINS = [
    "http://localhost:5174",
    "http://127.0.0.1:5174",
]

# Request-reply timeout (seconds)
DEFAULT_REQUEST_TIMEOUT = 30
