"""Shared async subprocess execution for CLI tool invocations.

Used by tool handlers that need to shell out to workspace CLI tools
(REAW, Discussion Tracker, GitHub Crawler, etc.).
"""

import asyncio
import shlex

from workspace_web_app.engine.config import WORKSPACE_ROOT


async def run_tool_subprocess(
    command: str,
    cwd: str | None = None,
) -> dict:
    """Run a CLI command asynchronously and capture output.

    Args:
        command: Shell command string to execute.
        cwd: Working directory. Defaults to WORKSPACE_ROOT.

    Returns:
        {"returncode": int, "stdout": str, "stderr": str}
    """
    work_dir = cwd or WORKSPACE_ROOT
    args = shlex.split(command)

    proc = await asyncio.create_subprocess_exec(
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=work_dir,
    )
    stdout, stderr = await proc.communicate()

    return {
        "returncode": proc.returncode,
        "stdout": stdout.decode("utf-8", errors="replace"),
        "stderr": stderr.decode("utf-8", errors="replace"),
    }
