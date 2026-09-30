"""Shared tool execution pipeline: validate → execute → publish result.

All tool executions flow through execute_and_respond so there is
exactly ONE place that handles try/except/publish — no duplication.
"""

import asyncio
import json
import logging
from typing import Any, Callable

from workspace_web_app.engine.utils.envelope import build_envelope
from workspace_web_app.engine.utils.response import error_response, success_response

logger = logging.getLogger(__name__)

RESULTS_TOOLS_TOPIC = "results.tools"


async def execute_and_respond(
    tool_fn: Callable[..., Any],
    payload: dict,
    producer,
    correlation_id: str,
    cmd_type: str,
    session_id: str = "",
    app_name: str = "",
) -> None:
    """Execute a tool function and publish the result to Kafka.

    Args:
        tool_fn: The tool function to call with payload.
        payload: Arguments passed to the tool function.
        producer: Kafka producer instance for publishing results.
        correlation_id: Links this result to the originating command.
        cmd_type: The command type string (for logging/envelope).
        session_id: Browser session identifier.
        app_name: Target application name.
    """
    try:
        logger.info("Executing tool: %s (cid=%s)", cmd_type, correlation_id)

        # Run tool — use thread executor for sync functions
        if asyncio.iscoroutinefunction(tool_fn):
            result_data = await tool_fn(payload)
        else:
            loop = asyncio.get_running_loop()
            result_data = await loop.run_in_executor(None, tool_fn, payload)

        result_payload = success_response(result_data)
        logger.info("Tool %s succeeded (cid=%s)", cmd_type, correlation_id)

    except Exception as exc:
        result_payload = error_response(str(exc))
        logger.error("Tool %s failed (cid=%s): %s", cmd_type, correlation_id, exc)

    envelope = build_envelope(
        type=cmd_type,
        payload=result_payload,
        correlation_id=correlation_id,
        session_id=session_id,
        app_name=app_name,
    )

    await producer.send_and_wait(
        RESULTS_TOOLS_TOPIC,
        json.dumps(envelope).encode("utf-8"),
    )
