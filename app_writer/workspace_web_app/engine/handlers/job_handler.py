"""Job command router — handles cancel and status requests from ``commands.jobs``.

Delegates to :class:`~workspace_web_app.engine.services.job_manager.JobManager`
and publishes results to ``results.tools`` using the standard envelope and
response helpers.
"""

import json
import logging

from workspace_web_app.engine.utils.envelope import build_envelope
from workspace_web_app.engine.utils.response import error_response, success_response

logger = logging.getLogger(__name__)

RESULTS_TOOLS_TOPIC = "results.tools"


class JobHandler:
    """Routes ``commands.jobs`` messages to :class:`JobManager` methods.

    Supported command types:

    * ``job_cancel``  → :meth:`JobManager.cancel_job`
    * ``job_status``  → :meth:`JobManager.get_job_status`

    Usage::

        handler = JobHandler(job_manager, producer)
        await handler.handle(message)
    """

    def __init__(self, job_manager, producer) -> None:
        self.job_manager = job_manager
        self.producer = producer

    async def handle(self, message: dict) -> None:
        """Dispatch a job command message.

        Extracts ``type`` from the message, delegates to the appropriate
        :class:`JobManager` method, and publishes the result envelope to
        ``results.tools``.
        """
        cmd_type = message.get("type", "")
        correlation_id = message.get("correlationId", "")
        session_id = message.get("sessionId", "")
        app_name = message.get("appName", "")
        payload = message.get("payload", {})

        if cmd_type == "job_cancel":
            await self._handle_cancel(payload, correlation_id, session_id, app_name)
        elif cmd_type == "job_status":
            await self._handle_status(payload, correlation_id, session_id, app_name)
        else:
            logger.warning("Unknown job command type: %s (cid=%s)", cmd_type, correlation_id)
            await self._publish(
                cmd_type,
                error_response(f"Unknown job command type: {cmd_type}"),
                correlation_id,
                session_id,
                app_name,
            )

    # ------------------------------------------------------------------
    # Command handlers
    # ------------------------------------------------------------------

    async def _handle_cancel(
        self,
        payload: dict,
        correlation_id: str,
        session_id: str,
        app_name: str,
    ) -> None:
        """Handle a ``job_cancel`` command."""
        job_id = payload.get("job_id", "")
        if not job_id:
            await self._publish(
                "job_cancel",
                error_response("Missing required field: job_id"),
                correlation_id,
                session_id,
                app_name,
            )
            return

        try:
            cancelled = self.job_manager.cancel_job(job_id)
            if cancelled:
                result = success_response({"job_id": job_id, "cancelled": True})
            else:
                result = error_response(
                    f"Job '{job_id}' not found or not in a cancellable state"
                )
            await self._publish("job_cancel", result, correlation_id, session_id, app_name)
        except Exception as exc:
            logger.error("job_cancel failed (cid=%s): %s", correlation_id, exc)
            await self._publish(
                "job_cancel",
                error_response(str(exc)),
                correlation_id,
                session_id,
                app_name,
            )

    async def _handle_status(
        self,
        payload: dict,
        correlation_id: str,
        session_id: str,
        app_name: str,
    ) -> None:
        """Handle a ``job_status`` command."""
        job_id = payload.get("job_id", "")
        if not job_id:
            await self._publish(
                "job_status",
                error_response("Missing required field: job_id"),
                correlation_id,
                session_id,
                app_name,
            )
            return

        try:
            status = self.job_manager.get_job_status(job_id)
            await self._publish(
                "job_status",
                success_response(status),
                correlation_id,
                session_id,
                app_name,
            )
        except KeyError:
            await self._publish(
                "job_status",
                error_response(f"Unknown job_id: {job_id}"),
                correlation_id,
                session_id,
                app_name,
            )
        except Exception as exc:
            logger.error("job_status failed (cid=%s): %s", correlation_id, exc)
            await self._publish(
                "job_status",
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
        """Build an envelope and publish to ``results.tools``."""
        envelope = build_envelope(
            type=msg_type,
            payload=result_payload,
            correlation_id=correlation_id,
            session_id=session_id,
            app_name=app_name,
        )
        await self.producer.send_and_wait(
            RESULTS_TOOLS_TOPIC,
            json.dumps(envelope).encode("utf-8"),
        )
