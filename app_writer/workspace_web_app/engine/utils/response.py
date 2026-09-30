"""Standardized result builders for tool execution responses.

All tool results use these builders so the format is consistent
across every handler.
"""


def success_response(data: object) -> dict:
    """Build a success result payload.

    Args:
        data: The result data from tool execution.

    Returns:
        {"success": True, "data": data, "error": None}
    """
    return {"success": True, "data": data, "error": None}


def error_response(error: str) -> dict:
    """Build an error result payload.

    Args:
        error: Human-readable error description.

    Returns:
        {"success": False, "data": None, "error": error}
    """
    return {"success": False, "data": None, "error": error}
