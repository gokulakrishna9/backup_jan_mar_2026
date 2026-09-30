"""CorrelationStore — routes Kafka results to the correct browser mechanism.

Three delivery mechanisms:
  - Future:    request-reply (REST endpoints await a single result)
  - WebSocket: streaming jobs (generation progress pushed to connected client)
  - Queue:     SSE agent chat (agent response events queued for SSE stream)
"""

import asyncio
import logging
from typing import Any

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class CorrelationStore:
    """Maps correlationId to the appropriate delivery mechanism."""

    def __init__(self) -> None:
        self._pending: dict[str, asyncio.Future] = {}
        self._websockets: dict[str, WebSocket] = {}
        self._sse_queues: dict[str, asyncio.Queue] = {}

    # ── Registration ────────────────────────────────────────────

    def register_request(self, correlation_id: str) -> asyncio.Future:
        """Register a Future for request-reply. Returns the Future to await."""
        loop = asyncio.get_running_loop()
        future = loop.create_future()
        self._pending[correlation_id] = future
        logger.debug("Registered request future: %s", correlation_id)
        return future

    def register_websocket(self, correlation_id: str, ws: WebSocket) -> None:
        """Register a WebSocket for streaming job events."""
        self._websockets[correlation_id] = ws
        logger.debug("Registered WebSocket: %s", correlation_id)

    def register_sse(self, correlation_id: str) -> asyncio.Queue:
        """Register an asyncio.Queue for SSE agent chat. Returns the Queue."""
        queue: asyncio.Queue = asyncio.Queue()
        self._sse_queues[correlation_id] = queue
        logger.debug("Registered SSE queue: %s", correlation_id)
        return queue

    # ── Resolution ──────────────────────────────────────────────

    async def resolve(self, correlation_id: str, result: Any) -> None:
        """Route an incoming result to the correct mechanism.

        Checks Future first, then WebSocket, then SSE queue.
        Logs a warning if no registration is found (message arrived
        after timeout or for an unknown correlation).
        """
        # 1. Request-reply Future
        future = self._pending.pop(correlation_id, None)
        if future is not None and not future.done():
            future.set_result(result)
            logger.debug("Resolved future: %s", correlation_id)
            return

        # 2. WebSocket streaming
        ws = self._websockets.get(correlation_id)
        if ws is not None:
            try:
                await ws.send_json(result)
                logger.debug("Sent to WebSocket: %s", correlation_id)
            except Exception:
                logger.warning("WebSocket send failed: %s", correlation_id)
                self._websockets.pop(correlation_id, None)
            return

        # 3. SSE queue
        queue = self._sse_queues.get(correlation_id)
        if queue is not None:
            await queue.put(result)
            logger.debug("Enqueued for SSE: %s", correlation_id)
            return

        logger.warning("No registration for correlationId: %s", correlation_id)

    # ── Cleanup ─────────────────────────────────────────────────

    def unregister_request(self, correlation_id: str) -> None:
        """Remove a pending request Future (e.g. on timeout)."""
        self._pending.pop(correlation_id, None)

    def unregister_websocket(self, correlation_id: str) -> None:
        """Remove a WebSocket registration."""
        self._websockets.pop(correlation_id, None)

    def unregister_sse(self, correlation_id: str) -> None:
        """Remove an SSE queue registration."""
        self._sse_queues.pop(correlation_id, None)
