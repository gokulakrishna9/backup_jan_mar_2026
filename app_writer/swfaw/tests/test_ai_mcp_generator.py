"""Unit tests for the AI McpGenerator.

Verifies that the McpGenerator produces correct Java source files
for McpClientService per enabled MCP server with stdio/SSE transport,
tool discovery, proxy methods, connection lifecycle, and role-based
access control.

Requirements: 13.32–13.42
"""

import sys
from pathlib import Path

import pytest

# Ensure swfaw package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import jinja2

from swfaw.generators.ai_mcp_generator import McpGenerator, _pascal


@pytest.fixture
def jinja_env():
    """Create a Jinja2 environment pointing at the swfaw/templates directory."""
    templates_dir = Path(__file__).resolve().parent.parent / "templates"
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(templates_dir)),
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )


@pytest.fixture
def generator(jinja_env):
    return McpGenerator(jinja_env)


@pytest.fixture
def minimal_orchestrator():
    return {"providerName": "mainGpt"}


@pytest.fixture
def output_dirs():
    return {
        "mcp": Path("ai/mcp"),
    }


@pytest.fixture
def stdio_server():
    return {
        "name": "filesystem",
        "transportType": "stdio",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/data"],
        "requiredRoles": ["ADMIN", "EDITOR"],
        "enabled": True,
    }


@pytest.fixture
def sse_server():
    return {
        "name": "weather_api",
        "transportType": "sse",
        "url": "https://mcp.weather.example.com/sse",
        "headers": {"X-Api-Version": "2"},
        "auth": {
            "type": "bearer_token",
            "valueEnvVar": "WEATHER_API_TOKEN",
            "headerName": "Authorization",
        },
        "requiredRoles": [],
        "enabled": True,
    }


@pytest.fixture
def disabled_server():
    return {
        "name": "disabled_tool",
        "transportType": "stdio",
        "command": "some-cmd",
        "requiredRoles": [],
        "enabled": False,
    }


@pytest.fixture
def server_with_exposed_tools():
    return {
        "name": "limited_tools",
        "transportType": "stdio",
        "command": "tool-server",
        "args": [],
        "exposedTools": ["read_file", "write_file"],
        "requiredRoles": ["USER"],
        "enabled": True,
    }


@pytest.fixture
def server_with_env_vars():
    return {
        "name": "env_server",
        "transportType": "sse",
        "url": "https://mcp.env.example.com/sse",
        "envVars": {"API_KEY": "MCP_ENV_API_KEY", "SECRET": "MCP_ENV_SECRET"},
        "requiredRoles": [],
        "enabled": True,
    }


# ======================================================================
# Skip logic tests
# ======================================================================


class TestMcpGeneratorSkipLogic:
    """Verify that generation is skipped when appropriate."""

    def test_no_files_when_orchestrator_is_none(self, generator, output_dirs):
        """Req 13.9: No MCP files when orchestrator is absent."""
        result = generator.generate(
            mcp_servers=[{"name": "x", "enabled": True, "transportType": "stdio", "command": "x"}],
            orchestrator=None,
            base_package="com.example",
            output_dirs=output_dirs,
        )
        assert result == []

    def test_no_files_when_orchestrator_is_empty(self, generator, output_dirs):
        result = generator.generate(
            mcp_servers=[{"name": "x", "enabled": True, "transportType": "stdio", "command": "x"}],
            orchestrator={},
            base_package="com.example",
            output_dirs=output_dirs,
        )
        assert result == []

    def test_no_files_when_mcp_servers_is_none(
        self, generator, minimal_orchestrator, output_dirs
    ):
        result = generator.generate(
            mcp_servers=None,
            orchestrator=minimal_orchestrator,
            base_package="com.example",
            output_dirs=output_dirs,
        )
        assert result == []

    def test_no_files_when_mcp_servers_is_empty(
        self, generator, minimal_orchestrator, output_dirs
    ):
        result = generator.generate(
            mcp_servers=[],
            orchestrator=minimal_orchestrator,
            base_package="com.example",
            output_dirs=output_dirs,
        )
        assert result == []

    def test_no_files_when_all_servers_disabled(
        self, generator, minimal_orchestrator, disabled_server, output_dirs
    ):
        """Req 13.33: Skip disabled servers."""
        result = generator.generate(
            mcp_servers=[disabled_server],
            orchestrator=minimal_orchestrator,
            base_package="com.example",
            output_dirs=output_dirs,
        )
        assert result == []

    def test_only_enabled_servers_generate_files(
        self, generator, minimal_orchestrator, stdio_server, disabled_server, output_dirs
    ):
        """Req 13.33: Only enabled servers produce files."""
        result = generator.generate(
            mcp_servers=[stdio_server, disabled_server],
            orchestrator=minimal_orchestrator,
            base_package="com.example",
            output_dirs=output_dirs,
        )
        assert len(result) == 1


# ======================================================================
# File count and naming tests
# ======================================================================


class TestMcpGeneratorFileCounts:
    """Verify correct number and naming of generated files."""

    def test_one_file_per_enabled_server(
        self, generator, minimal_orchestrator, stdio_server, sse_server, output_dirs
    ):
        result = generator.generate(
            mcp_servers=[stdio_server, sse_server],
            orchestrator=minimal_orchestrator,
            base_package="com.example",
            output_dirs=output_dirs,
        )
        assert len(result) == 2

    def test_file_path_contains_class_name(
        self, generator, minimal_orchestrator, stdio_server, output_dirs
    ):
        """Req 13.34: McpClientService in ai.mcp package."""
        result = generator.generate(
            mcp_servers=[stdio_server],
            orchestrator=minimal_orchestrator,
            base_package="com.example",
            output_dirs=output_dirs,
        )
        filepath, _ = result[0]
        assert "FilesystemMcpClientService.java" in filepath
        assert "ai/mcp" in filepath

    def test_sse_server_class_name(
        self, generator, minimal_orchestrator, sse_server, output_dirs
    ):
        result = generator.generate(
            mcp_servers=[sse_server],
            orchestrator=minimal_orchestrator,
            base_package="com.example",
            output_dirs=output_dirs,
        )
        filepath, _ = result[0]
        assert "WeatherApiMcpClientService.java" in filepath

    def test_all_content_is_nonempty(
        self, generator, minimal_orchestrator, stdio_server, sse_server, output_dirs
    ):
        result = generator.generate(
            mcp_servers=[stdio_server, sse_server],
            orchestrator=minimal_orchestrator,
            base_package="com.example",
            output_dirs=output_dirs,
        )
        for filepath, content in result:
            assert content.strip(), f"Empty content for {filepath}"


# ======================================================================
# Stdio transport tests
# ======================================================================


class TestStdioTransport:
    """Verify stdio transport-specific generation."""

    def _get_content(self, generator, minimal_orchestrator, stdio_server, output_dirs):
        result = generator.generate(
            mcp_servers=[stdio_server],
            orchestrator=minimal_orchestrator,
            base_package="com.example",
            output_dirs=output_dirs,
        )
        return result[0][1]

    def test_package_declaration(self, generator, minimal_orchestrator, stdio_server, output_dirs):
        content = self._get_content(generator, minimal_orchestrator, stdio_server, output_dirs)
        assert "package com.example.ai.mcp;" in content

    def test_component_annotation(self, generator, minimal_orchestrator, stdio_server, output_dirs):
        """Req 13.34: Spring @Component."""
        content = self._get_content(generator, minimal_orchestrator, stdio_server, output_dirs)
        assert "@Component" in content

    def test_post_construct(self, generator, minimal_orchestrator, stdio_server, output_dirs):
        content = self._get_content(generator, minimal_orchestrator, stdio_server, output_dirs)
        assert "@PostConstruct" in content

    def test_pre_destroy(self, generator, minimal_orchestrator, stdio_server, output_dirs):
        content = self._get_content(generator, minimal_orchestrator, stdio_server, output_dirs)
        assert "@PreDestroy" in content

    def test_command_constant(self, generator, minimal_orchestrator, stdio_server, output_dirs):
        """Req 13.32: stdio transport with command/args."""
        content = self._get_content(generator, minimal_orchestrator, stdio_server, output_dirs)
        assert 'COMMAND = "npx"' in content

    def test_args_constant(self, generator, minimal_orchestrator, stdio_server, output_dirs):
        content = self._get_content(generator, minimal_orchestrator, stdio_server, output_dirs)
        assert "@modelcontextprotocol/server-filesystem" in content
        assert "/data" in content

    def test_no_url_for_stdio(self, generator, minimal_orchestrator, stdio_server, output_dirs):
        content = self._get_content(generator, minimal_orchestrator, stdio_server, output_dirs)
        assert "private static final String URL" not in content

    def test_required_roles_as_constants(self, generator, minimal_orchestrator, stdio_server, output_dirs):
        """Req 13.41: requiredRoles as compile-time constants."""
        content = self._get_content(generator, minimal_orchestrator, stdio_server, output_dirs)
        assert '"ADMIN"' in content
        assert '"EDITOR"' in content
        assert "REQUIRED_ROLES = Set.of(" in content

    def test_class_name(self, generator, minimal_orchestrator, stdio_server, output_dirs):
        content = self._get_content(generator, minimal_orchestrator, stdio_server, output_dirs)
        assert "class FilesystemMcpClientService" in content

    def test_server_name_constant(self, generator, minimal_orchestrator, stdio_server, output_dirs):
        content = self._get_content(generator, minimal_orchestrator, stdio_server, output_dirs)
        assert 'SERVER_NAME = "filesystem"' in content

    def test_reconnect_logic(self, generator, minimal_orchestrator, stdio_server, output_dirs):
        """Req 13.36: reconnect with 3 attempts/exponential backoff."""
        content = self._get_content(generator, minimal_orchestrator, stdio_server, output_dirs)
        assert "MAX_RECONNECT_ATTEMPTS = 3" in content
        assert "INITIAL_BACKOFF_MS = 1000L" in content
        assert "reconnect()" in content

    def test_tool_security_context_import(self, generator, minimal_orchestrator, stdio_server, output_dirs):
        """Req 13.38: Uses ToolSecurityContextHolder for role checks."""
        content = self._get_content(generator, minimal_orchestrator, stdio_server, output_dirs)
        assert "ToolSecurityContextHolder" in content

    def test_invoke_tool_method(self, generator, minimal_orchestrator, stdio_server, output_dirs):
        """Req 13.36: invokeTool delegates via tools/call."""
        content = self._get_content(generator, minimal_orchestrator, stdio_server, output_dirs)
        assert "public String invokeTool(String toolName, String arguments)" in content

    def test_discover_tools_method(self, generator, minimal_orchestrator, stdio_server, output_dirs):
        """Req 13.35: Discovers tools at startup."""
        content = self._get_content(generator, minimal_orchestrator, stdio_server, output_dirs)
        assert "discoverTools()" in content

    def test_stdio_connect_log(self, generator, minimal_orchestrator, stdio_server, output_dirs):
        content = self._get_content(generator, minimal_orchestrator, stdio_server, output_dirs)
        assert "via stdio" in content


# ======================================================================
# SSE transport tests
# ======================================================================


class TestSseTransport:
    """Verify SSE transport-specific generation."""

    def _get_content(self, generator, minimal_orchestrator, sse_server, output_dirs):
        result = generator.generate(
            mcp_servers=[sse_server],
            orchestrator=minimal_orchestrator,
            base_package="com.example",
            output_dirs=output_dirs,
        )
        return result[0][1]

    def test_url_constant(self, generator, minimal_orchestrator, sse_server, output_dirs):
        """Req 13.32: SSE transport with url."""
        content = self._get_content(generator, minimal_orchestrator, sse_server, output_dirs)
        assert 'URL = "https://mcp.weather.example.com/sse"' in content

    def test_no_command_for_sse(self, generator, minimal_orchestrator, sse_server, output_dirs):
        content = self._get_content(generator, minimal_orchestrator, sse_server, output_dirs)
        assert "private static final String COMMAND" not in content

    def test_headers(self, generator, minimal_orchestrator, sse_server, output_dirs):
        content = self._get_content(generator, minimal_orchestrator, sse_server, output_dirs)
        assert "HEADER_X_API_VERSION" in content

    def test_auth_config(self, generator, minimal_orchestrator, sse_server, output_dirs):
        """Req 13.32: optional auth with type and valueEnvVar."""
        content = self._get_content(generator, minimal_orchestrator, sse_server, output_dirs)
        assert 'AUTH_TYPE = "bearer_token"' in content
        assert 'System.getenv("WEATHER_API_TOKEN")' in content
        assert 'AUTH_HEADER = "Authorization"' in content

    def test_empty_required_roles(self, generator, minimal_orchestrator, sse_server, output_dirs):
        """Req 13.39: Empty requiredRoles allows all authenticated users."""
        content = self._get_content(generator, minimal_orchestrator, sse_server, output_dirs)
        assert "REQUIRED_ROLES = Set.of();" in content

    def test_sse_connect_log(self, generator, minimal_orchestrator, sse_server, output_dirs):
        content = self._get_content(generator, minimal_orchestrator, sse_server, output_dirs)
        assert "via SSE" in content


# ======================================================================
# Exposed tools filter tests
# ======================================================================


class TestExposedToolsFilter:
    """Verify exposedTools filtering in generated code."""

    def _get_content(self, generator, minimal_orchestrator, server_with_exposed_tools, output_dirs):
        result = generator.generate(
            mcp_servers=[server_with_exposed_tools],
            orchestrator=minimal_orchestrator,
            base_package="com.example",
            output_dirs=output_dirs,
        )
        return result[0][1]

    def test_exposed_tools_set(self, generator, minimal_orchestrator, server_with_exposed_tools, output_dirs):
        """Req 13.35: filtered by exposedTools if configured."""
        content = self._get_content(generator, minimal_orchestrator, server_with_exposed_tools, output_dirs)
        assert "EXPOSED_TOOLS = Set.of(" in content
        assert '"read_file"' in content
        assert '"write_file"' in content

    def test_is_exposed_tool_method(self, generator, minimal_orchestrator, server_with_exposed_tools, output_dirs):
        content = self._get_content(generator, minimal_orchestrator, server_with_exposed_tools, output_dirs)
        assert "isExposedTool(toolName)" in content

    def test_no_exposed_tools_when_not_configured(
        self, generator, minimal_orchestrator, stdio_server, output_dirs
    ):
        """When exposedTools is absent, no filter is generated."""
        result = generator.generate(
            mcp_servers=[stdio_server],
            orchestrator=minimal_orchestrator,
            base_package="com.example",
            output_dirs=output_dirs,
        )
        content = result[0][1]
        assert "EXPOSED_TOOLS" not in content


# ======================================================================
# Environment variables tests
# ======================================================================


class TestEnvVars:
    """Verify environment variable generation."""

    def _get_content(self, generator, minimal_orchestrator, server_with_env_vars, output_dirs):
        result = generator.generate(
            mcp_servers=[server_with_env_vars],
            orchestrator=minimal_orchestrator,
            base_package="com.example",
            output_dirs=output_dirs,
        )
        return result[0][1]

    def test_env_var_constants(self, generator, minimal_orchestrator, server_with_env_vars, output_dirs):
        content = self._get_content(generator, minimal_orchestrator, server_with_env_vars, output_dirs)
        assert 'System.getenv("MCP_ENV_API_KEY")' in content
        assert 'System.getenv("MCP_ENV_SECRET")' in content


# ======================================================================
# Role-based access control tests
# ======================================================================


class TestRoleBasedAccessControl:
    """Verify role-based access control in generated code."""

    def test_role_check_in_invoke_tool(
        self, generator, minimal_orchestrator, stdio_server, output_dirs
    ):
        """Req 13.38: Check user roles before invoking."""
        result = generator.generate(
            mcp_servers=[stdio_server],
            orchestrator=minimal_orchestrator,
            base_package="com.example",
            output_dirs=output_dirs,
        )
        content = result[0][1]
        assert "checkRoleAccess()" in content

    def test_access_denied_message(
        self, generator, minimal_orchestrator, stdio_server, output_dirs
    ):
        """Req 13.38: Return descriptive error string on unauthorized."""
        result = generator.generate(
            mcp_servers=[stdio_server],
            orchestrator=minimal_orchestrator,
            base_package="com.example",
            output_dirs=output_dirs,
        )
        content = result[0][1]
        assert "Access denied" in content

    def test_empty_roles_allows_all(
        self, generator, minimal_orchestrator, sse_server, output_dirs
    ):
        """Req 13.39: Empty requiredRoles allows all authenticated users."""
        result = generator.generate(
            mcp_servers=[sse_server],
            orchestrator=minimal_orchestrator,
            base_package="com.example",
            output_dirs=output_dirs,
        )
        content = result[0][1]
        # Empty roles → early return null (access granted)
        assert "REQUIRED_ROLES.isEmpty()" in content


# ======================================================================
# Context building tests
# ======================================================================


class TestContextBuilding:
    """Verify internal context building logic."""

    def test_stdio_context(self, generator):
        server = {
            "name": "my_server",
            "transportType": "stdio",
            "command": "cmd",
            "args": ["--flag"],
            "requiredRoles": ["ADMIN"],
            "enabled": True,
        }
        ctx = generator._build_context(server, "com.test")
        assert ctx["server_name"] == "my_server"
        assert ctx["class_name"] == "MyServerMcpClientService"
        assert ctx["transport_type"] == "stdio"
        assert ctx["command"] == "cmd"
        assert ctx["args"] == ["--flag"]
        assert ctx["required_roles"] == ["ADMIN"]
        assert ctx["base_package"] == "com.test"

    def test_sse_context(self, generator):
        server = {
            "name": "api_server",
            "transportType": "sse",
            "url": "https://example.com/sse",
            "headers": {"X-Key": "val"},
            "requiredRoles": [],
            "enabled": True,
        }
        ctx = generator._build_context(server, "com.test")
        assert ctx["transport_type"] == "sse"
        assert ctx["url"] == "https://example.com/sse"
        assert ctx["headers"] == {"X-Key": "val"}
        assert "command" not in ctx

    def test_exposed_tools_in_context(self, generator):
        server = {
            "name": "tools_srv",
            "transportType": "stdio",
            "command": "x",
            "exposedTools": ["a", "b"],
            "requiredRoles": [],
            "enabled": True,
        }
        ctx = generator._build_context(server, "com.test")
        assert ctx["exposed_tools"] == ["a", "b"]

    def test_no_exposed_tools_is_none(self, generator):
        server = {
            "name": "srv",
            "transportType": "stdio",
            "command": "x",
            "requiredRoles": [],
            "enabled": True,
        }
        ctx = generator._build_context(server, "com.test")
        assert ctx["exposed_tools"] is None

    def test_auth_in_context(self, generator):
        server = {
            "name": "auth_srv",
            "transportType": "sse",
            "url": "https://x.com/sse",
            "auth": {"type": "api_key", "valueEnvVar": "KEY", "headerName": "X-Api-Key"},
            "requiredRoles": [],
            "enabled": True,
        }
        ctx = generator._build_context(server, "com.test")
        assert ctx["auth"]["type"] == "api_key"
        assert ctx["auth"]["valueEnvVar"] == "KEY"

    def test_env_vars_in_context(self, generator):
        server = {
            "name": "env_srv",
            "transportType": "stdio",
            "command": "x",
            "envVars": {"TOKEN": "MY_TOKEN"},
            "requiredRoles": [],
            "enabled": True,
        }
        ctx = generator._build_context(server, "com.test")
        assert ctx["env_vars"] == {"TOKEN": "MY_TOKEN"}


# ======================================================================
# Helper function tests
# ======================================================================


class TestPascalHelper:
    """Verify _pascal helper function."""

    def test_snake_case(self):
        assert _pascal("my_server") == "MyServer"

    def test_already_pascal(self):
        assert _pascal("MyServer") == "MyServer"

    def test_camel_case(self):
        assert _pascal("myServer") == "MyServer"

    def test_empty(self):
        assert _pascal("") == ""

    def test_single_word(self):
        assert _pascal("filesystem") == "Filesystem"
