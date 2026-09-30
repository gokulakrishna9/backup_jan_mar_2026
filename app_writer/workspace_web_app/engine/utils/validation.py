"""Payload schema validation helpers.

Lightweight validation for incoming Kafka message payloads.
Raises ValueError with a descriptive message on failure.
"""


def validate_payload(payload: dict, required_keys: list[str]) -> None:
    """Validate that payload contains all required keys.

    Args:
        payload: The message payload dict to validate.
        required_keys: List of keys that must be present.

    Raises:
        ValueError: If any required key is missing.
    """
    if not isinstance(payload, dict):
        raise ValueError(f"Payload must be a dict, got {type(payload).__name__}")

    missing = [k for k in required_keys if k not in payload]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")
