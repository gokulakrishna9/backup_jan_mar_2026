"""Single source of truth for Kafka message envelope format.

Every Kafka message in the system uses this envelope. Never construct
message dicts inline — always call build_envelope.
"""

import uuid
from datetime import datetime, timezone


def build_envelope(
    type: str,
    payload: dict,
    correlation_id: str | None = None,
    session_id: str = "",
    app_name: str = "",
) -> dict:
    """Build a Kafka message envelope.

    Args:
        type: Message type (e.g. 'add_entity', 'generate_full').
        payload: Message-specific data.
        correlation_id: Links command to its result. Auto-generated if None.
        session_id: Browser session identifier.
        app_name: Target application name.

    Returns:
        Complete envelope dict ready for JSON serialization.
    """
    return {
        "messageId": str(uuid.uuid4()),
        "correlationId": correlation_id or str(uuid.uuid4()),
        "sessionId": session_id,
        "appName": app_name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "type": type,
        "payload": payload,
    }
