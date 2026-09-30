"""MCP client sub-generator for the AI Layer.

Generates McpClientService per enabled MCP server with stdio or SSE
transport, tool discovery, proxy methods, connection lifecycle, and
role-based access control.

Requirements: 13.32–13.42
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import jinja2


def _pascal(name: str) -> str:
    """Convert a snake_case or camelCase name to PascalCase."""
    if "_" in name:
        return "".join(part.capitalize() for part in name.split("_"))
    if name:
        return name[0].upper() + name[1:]
    return name


class McpGenerator:
    """Generates MCP client service Java files from the AI_Layer definition.

    Follows the same sub-generator pattern as OrchestratorGenerator:
    receives parsed definition data, checks whether the feature is
    enabled, loads and renders Jinja2 templates, and returns a list
    of ``(filepath, content)`` tuples.

    Req 13.34: Generates McpClientService per enabled MCP server.
    Req 13.42: All MCP client classes generated using SWFAW Jinja2 templates.
    """

    def __init__(self, jinja_env: "jinja2.Environment"):
        self.jinja_env = jinja_env

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(
        self,
        mcp_servers: list[dict] | None,
        orchestrator: dict | None,
        base_package: str,
        output_dirs: dict[str, Path],
    ) -> list[tuple[str, str]]:
        """Generate MCP client service Java files.

        Returns a list of ``(filepath, content)`` tuples where *filepath*
        is relative to the project source root.

        Req 13.9: When the orchestrator is absent, no MCP files are
        generated (MCP servers require orchestrator).

        Req 13.33: When ``enabled`` is ``false``, skip that server.
        When no enabled servers exist, return empty list.
        """
        if not orchestrator:
            return []

        if not mcp_servers:
            return []

        enabled_servers = [
            s for s in mcp_servers if s.get("enabled", False)
        ]
        if not enabled_servers:
            return []

        results: list[tuple[str, str]] = []
        mcp_dir = output_dirs.get("mcp", Path("ai/mcp"))

        for server in enabled_servers:
            ctx = self._build_context(server, base_package)
            class_name = ctx["class_name"]
            results.append((
                str(mcp_dir / f"{class_name}.java"),
                self._render("mcp/mcp_client_service.java.j2", ctx),
            ))

        return results

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _build_context(self, server: dict, base_package: str) -> dict:
        """Build Jinja2 context for an MCP server template."""
        name = server.get("name", "")
        transport_type = server.get("transportType", "stdio")
        required_roles = server.get("requiredRoles", [])
        exposed_tools = server.get("exposedTools")
        env_vars = server.get("envVars")
        auth = server.get("auth")

        class_name = f"{_pascal(name)}McpClientService"

        ctx: dict = {
            "base_package": base_package,
            "server_name": name,
            "class_name": class_name,
            "transport_type": transport_type,
            "required_roles": required_roles,
            "exposed_tools": exposed_tools,
            "env_vars": env_vars,
            "auth": auth,
        }

        # Transport-specific fields (Req 13.32)
        if transport_type == "stdio":
            ctx["command"] = server.get("command", "")
            ctx["args"] = server.get("args", [])
        elif transport_type == "sse":
            ctx["url"] = server.get("url", "")
            ctx["headers"] = server.get("headers", {})

        return ctx

    def _render(self, template_name: str, ctx: dict) -> str:
        """Render a Jinja2 template under the ai/ prefix."""
        template = self.jinja_env.get_template(f"ai/{template_name}")
        return template.render(**ctx)
