"""App Validator REST endpoints — thin Kafka gateway.

Every endpoint is a one-liner delegating to publish_and_await.
No tool logic lives here; the Engine Service handles execution.
"""

from fastapi import APIRouter, Depends

from workspace_web_app.ui_service.main import get_correlation_store, get_producer
from workspace_web_app.ui_service.utils.kafka_rpc import publish_and_await

router = APIRouter(tags=["validation"])

TOPIC = "commands.tools"

# Validation can be slow — use a longer timeout
VALIDATION_TIMEOUT = 90


@router.post("/validate/{app}/backend")
async def validate_backend(
    app: str,
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    """Validate backend definitions for an application."""
    return await publish_and_await(
        TOPIC, "validate_backend", {"app": app}, store, producer,
        timeout=VALIDATION_TIMEOUT, app_name=app,
    )


@router.post("/validate/{app}/frontend")
async def validate_frontend(
    app: str,
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    """Validate frontend definitions for an application."""
    return await publish_and_await(
        TOPIC, "validate_frontend", {"app": app}, store, producer,
        timeout=VALIDATION_TIMEOUT, app_name=app,
    )


@router.post("/validate/{app}/api-coverage")
async def validate_api_coverage(
    app: str,
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    """Run API coverage validation for an application."""
    return await publish_and_await(
        TOPIC, "validate_api_coverage", {"app": app}, store, producer,
        timeout=VALIDATION_TIMEOUT, app_name=app,
    )
