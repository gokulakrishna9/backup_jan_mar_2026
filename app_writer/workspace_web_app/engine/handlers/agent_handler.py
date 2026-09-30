"""Agent command router — handles chat, history, and clear-history from ``commands.agent``.

Delegates to :class:`~workspace_web_app.engine.services.agent_service.AgentService`
and publishes streaming events to ``results.agent`` using the standard envelope
and response helpers.

Requirements: 3.3
"""

import json
import logging

from workspace_web_app.engine.utils.envelope import build_envelope
from workspace_web_app.engine.utils.response import error_response, success_response

logger = logging.getLogger(__name__)

RESULTS_AGENT_TOPIC = "results.agent"


class AgentHandler:
    """Routes ``commands.agent`` messages to :class:`AgentService` methods.

    Supported command types:

    * ``agent_chat``          → :meth:`AgentService.chat` (async generator, streams events)
    * ``agent_history``       → :meth:`AgentService.get_history`
    * ``agent_clear_history`` → :meth:`AgentService.clear_history`

    Usage::

        handler = AgentHandler(agent_service, producer)
        await handler.handle(message)
    """

    def __init__(self, agent_service, producer) -> None:
        self.agent_service = agent_service
        self.producer = producer

    async def handle(self, message: dict) -> None:
        """Dispatch an agent command message.

        Extracts ``type`` from the message and routes to the appropriate
        handler method.
        """
        cmd_type = message.get("type", "")
        correlation_id = message.get("correlationId", "")
        session_id = message.get("sessionId", "")
        app_name = message.get("appName", "")
        payload = message.get("payload", {})

        if cmd_type == "agent_chat":
            await self._handle_chat(payload, correlation_id, session_id, app_name)
        elif cmd_type == "agent_history":
            await self._handle_history(payload, correlation_id, session_id, app_name)
        elif cmd_type == "agent_clear_history":
            await self._handle_clear_history(payload, correlation_id, session_id, app_name)
        else:
            logger.warning("Unknown agent command type: %s (cid=%s)", cmd_type, correlation_id)
            await self._publish(
                cmd_type,
                error_response(f"Unknown agent command type: {cmd_type}"),
                correlation_id,
                session_id,
                app_name,
            )

    # ------------------------------------------------------------------
    # Command handlers
    # ------------------------------------------------------------------

    async def _handle_chat(
        self,
        payload: dict,
        correlation_id: str,
        session_id: str,
        app_name: str,
    ) -> None:
        """Handle an ``agent_chat`` command.

        Calls ``AgentService.chat()`` which is an async generator.
        Each yielded event is published to ``results.agent`` with the
        same correlationId so the UI Service can route it to the correct
        SSE stream.
        """
        user_message = payload.get("message", "")
        # appName can come from the envelope or the payload
        chat_app_name = payload.get("appName", app_name)

        if not user_message:
            await self._publish(
                "agent_chat",
                error_response("Missing required field: message"),
                correlation_id,
                session_id,
                app_name,
            )
            return

        try:
            async for event in self.agent_service.chat(chat_app_name, user_message):
                await self._publish(
                    f"agent_{event['type']}",
                    success_response(event["data"]),
                    correlation_id,
                    session_id,
                    app_name,
                )
        except Exception as exc:
            logger.error("agent_chat failed (cid=%s): %s", correlation_id, exc)
            await self._publish(
                "agent_chat",
                error_response(str(exc)),
                correlation_id,
                session_id,
                app_name,
            )

    async def _handle_history(
        self,
        payload: dict,
        correlation_id: str,
        session_id: str,
        app_name: str,
    ) -> None:
        """Handle an ``agent_history`` command — return conversation history."""
        history_app_name = payload.get("appName", app_name)

        if not history_app_name:
            await self._publish(
                "agent_history",
                error_response("Missing required field: appName"),
                correlation_id,
                session_id,
                app_name,
            )
            return

        try:
            history = self.agent_service.get_history(history_app_name)
            await self._publish(
                "agent_history",
                success_response({"appName": history_app_name, "history": history}),
                correlation_id,
                session_id,
                app_name,
            )
        except Exception as exc:
            logger.error("agent_history failed (cid=%s): %s", correlation_id, exc)
            await self._publish(
                "agent_history",
                error_response(str(exc)),
                correlation_id,
                session_id,
                app_name,
            )

    async def _handle_clear_history(
        self,
        payload: dict,
        correlation_id: str,
        session_id: str,
        app_name: str,
    ) -> None:
        """Handle an ``agent_clear_history`` command — clear conversation history."""
        clear_app_name = payload.get("appName", app_name)

        if not clear_app_name:
            await self._publish(
                "agent_clear_history",
                error_response("Missing required field: appName"),
                correlation_id,
                session_id,
                app_name,
            )
            return

        try:
            self.agent_service.clear_history(clear_app_name)
            await self._publish(
                "agent_clear_history",
                success_response({"appName": clear_app_name, "cleared": True}),
                correlation_id,
                session_id,
                app_name,
            )
        except Exception as exc:
            logger.error("agent_clear_history failed (cid=%s): %s", correlation_id, exc)
            await self._publish(
                "agent_clear_history",
                error_response(str(exc)),
                correlation_id,
                session_id,
                app_name,
            )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    async def _publish(
        self,
        msg_type: str,
        result_payload: dict,
        correlation_id: str,
        session_id: str,
        app_name: str,
    ) -> None:
        """Build an envelope and publish to ``results.agent``."""
        envelope = build_envelope(
            type=msg_type,
            payload=result_payload,
            correlation_id=correlation_id,
            session_id=session_id,
            app_name=app_name,
        )
        await self.producer.send_and_wait(
            RESULTS_AGENT_TOPIC,
            json.dumps(envelope).encode("utf-8"),
        )
