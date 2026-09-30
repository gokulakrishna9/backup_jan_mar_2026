"""AI Settings REST endpoints — thin Kafka gateway.

Every endpoint delegates to publish_and_await on commands.tools.
No tool logic lives here; the Engine Service handles execution via
LLMProviderManager.

Requirements: 14.7
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Any, Optional

from workspace_web_app.ui_service.main import get_correlation_store, get_producer
from workspace_web_app.ui_service.utils.kafka_rpc import publish_and_await

router = APIRouter(tags=["ai-settings"])

TOPIC = "commands.tools"


class AIConfigUpdateRequest(BaseModel):
    """Request body for updating AI configuration."""

    active_model: Optional[str] = None
    model_params: Optional[dict[str, Any]] = None
    custom_endpoint: Optional[dict[str, Any]] = None
    save: bool = False


@router.get("/ai/config")
async def get_ai_config(
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    """Fetch model registry, active model, params, and provider status."""
    return await publish_and_await(
        TOPIC, "ai_config_get", {}, store, producer,
    )


@router.put("/ai/config")
async def update_ai_config(
    body: AIConfigUpdateRequest,
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    """Update active model, params, or custom endpoints."""
    return await publish_and_await(
        TOPIC, "ai_config_update", body.model_dump(exclude_none=True),
        store, producer,
    )


@router.post("/ai/health-check/{provider}")
async def health_check(
    provider: str,
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    """Trigger a provider connectivity test."""
    return await publish_and_await(
        TOPIC, "ai_health_check", {"provider": provider},
        store, producer, timeout=15,
    )
