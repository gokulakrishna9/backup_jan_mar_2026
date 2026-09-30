"""Unit tests for the AI OrchestratorGenerator.

Verifies that the OrchestratorGenerator produces correct Java source files
for AiOrchestratorService, AiOrchestratorController, and
OrchestratorResponseDTO.

Requirements: 13.4–13.9, 13.15–13.16, 13.29–13.31
"""

import sys
from pathlib import Path

import pytest

# Ensure swfaw package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import jinja2

from swfaw.generators.ai_orchestrator_generator import (
    OrchestratorGenerator,
    DEFAULT_ACCESS_DENIED_MESSAGE,
)


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
    return OrchestratorGenerator(jinja_env)


@pytest.fixture
def minimal_orchestrator():
    """Minimal orchestrator config with only required providerName."""
    return {"providerName": "mainGpt"}


@pytest.fixture
def full_orchestrator():
    """Full orchestrator config with all optional fields."""
    return {
        "providerName": "orchestratorGpt",
        "systemPrompt": "You are a helpful AI assistant.",
        "chatOptions": {
            "temperature": 0.3,
            "maxTokens": 4096,
            "topP": 0.9,
        },
        "accessDeniedMessage": "Sorry, you are not authorized.",
    }


@pytest.fixture
def output_dirs():
    return {
        "orchestrator": Path("com/example/app/ai/orchestrator"),
        "controller": Path("com/example/app/ai/controller"),
        "dto": Path("com/example/app/ai/dto"),
    }


BASE_PACKAGE = "com.example.app"


# ======================================================================
# Test: generate() — skip logic and file counts
# ======================================================================

class TestOrchestratorGeneratorGenerate:
    """Tests for the generate() method's file output and skip logic."""

    def test_no_files_when_orchestrator_is_none(self, generator, output_dirs):
        """Req 13.9: No orchestrator files when orchestrator is None."""
        results = generator.generate(None, BASE_PACKAGE, output_dirs)
        assert results == []

    def test_no_files_when_orchestrator_is_empty_dict(self, generator, output_dirs):
        """Req 13.9: Empty dict is falsy — no files generated."""
        results = generator.generate({}, BASE_PACKAGE, output_dirs)
        assert results == []

    def test_minimal_orchestrator_generates_3_files(
        self, generator, minimal_orchestrator, output_dirs
    ):
        """Minimal config: DTO + service + controller = 3 files."""
        results = generator.generate(minimal_orchestrator, BASE_PACKAGE, output_dirs)
        assert len(results) == 3

    def test_full_orchestrator_generates_3_files(
        self, generator, full_orchestrator, output_dirs
    ):
        """Full config still produces 3 files."""
        results = generator.generate(full_orchestrator, BASE_PACKAGE, output_dirs)
        assert len(results) == 3

    def test_all_content_is_nonempty(
        self, generator, full_orchestrator, output_dirs
    ):
        results = generator.generate(full_orchestrator, BASE_PACKAGE, output_dirs)
        for filepath, content in results:
            assert content.strip(), f"Empty content for {filepath}"

    def test_output_dirs_used_in_paths(
        self, generator, minimal_orchestrator, output_dirs
    ):
        results = generator.generate(minimal_orchestrator, BASE_PACKAGE, output_dirs)
        for filepath, _ in results:
            assert filepath.startswith("com/example/app/ai/")

    def test_correct_filenames(self, generator, minimal_orchestrator, output_dirs):
        results = generator.generate(minimal_orchestrator, BASE_PACKAGE, output_dirs)
        filenames = {Path(fp).name for fp, _ in results}
        expected = {
            "OrchestratorResponseDTO.java",
            "AiOrchestratorService.java",
            "AiOrchestratorController.java",
        }
        assert filenames == expected


# ======================================================================
# Test: OrchestratorResponseDTO template
# ======================================================================

class TestOrchestratorResponseDTO:
    """Tests for the generated OrchestratorResponseDTO record."""

    def _get_dto(self, generator, orchestrator, output_dirs):
        results = generator.generate(orchestrator, BASE_PACKAGE, output_dirs)
        return next(c for fp, c in results if Path(fp).name == "OrchestratorResponseDTO.java")

    def test_is_record(self, generator, minimal_orchestrator, output_dirs):
        content = self._get_dto(generator, minimal_orchestrator, output_dirs)
        assert "public record OrchestratorResponseDTO(" in content

    def test_package_declaration(self, generator, minimal_orchestrator, output_dirs):
        content = self._get_dto(generator, minimal_orchestrator, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.dto;" in content

    def test_has_response_field(self, generator, minimal_orchestrator, output_dirs):
        """Req 13.5: OrchestratorResponseDTO has response field."""
        content = self._get_dto(generator, minimal_orchestrator, output_dirs)
        assert "String response" in content

    def test_has_tools_invoked_field(self, generator, minimal_orchestrator, output_dirs):
        """Req 13.5: OrchestratorResponseDTO has toolsInvoked field."""
        content = self._get_dto(generator, minimal_orchestrator, output_dirs)
        assert "List<String> toolsInvoked" in content

    def test_has_success_field(self, generator, minimal_orchestrator, output_dirs):
        """Req 13.5: OrchestratorResponseDTO has success field."""
        content = self._get_dto(generator, minimal_orchestrator, output_dirs)
        assert "boolean success" in content

    def test_has_error_field(self, generator, minimal_orchestrator, output_dirs):
        """Req 13.5: OrchestratorResponseDTO has error field."""
        content = self._get_dto(generator, minimal_orchestrator, output_dirs)
        assert "String error" in content

    def test_has_list_import(self, generator, minimal_orchestrator, output_dirs):
        content = self._get_dto(generator, minimal_orchestrator, output_dirs)
        assert "import java.util.List;" in content


# ======================================================================
# Test: AiOrchestratorService template
# ======================================================================

class TestAiOrchestratorService:
    """Tests for the generated AiOrchestratorService."""

    def _get_service(self, generator, orchestrator, output_dirs):
        results = generator.generate(orchestrator, BASE_PACKAGE, output_dirs)
        return next(c for fp, c in results if Path(fp).name == "AiOrchestratorService.java")

    def test_package_declaration(self, generator, minimal_orchestrator, output_dirs):
        content = self._get_service(generator, minimal_orchestrator, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.orchestrator;" in content

    def test_service_annotation(self, generator, minimal_orchestrator, output_dirs):
        content = self._get_service(generator, minimal_orchestrator, output_dirs)
        assert "@Service" in content

    def test_class_name(self, generator, minimal_orchestrator, output_dirs):
        """Req 13.4: AiOrchestratorService."""
        content = self._get_service(generator, minimal_orchestrator, output_dirs)
        assert "public class AiOrchestratorService" in content

    def test_chat_client_qualifier(self, generator, minimal_orchestrator, output_dirs):
        """Req 13.4: ChatClient injected via @Qualifier for orchestrator provider."""
        content = self._get_service(generator, minimal_orchestrator, output_dirs)
        assert '@Qualifier("mainGpt")' in content

    def test_full_provider_qualifier(self, generator, full_orchestrator, output_dirs):
        content = self._get_service(generator, full_orchestrator, output_dirs)
        assert '@Qualifier("orchestratorGpt")' in content

    def test_route_method(self, generator, minimal_orchestrator, output_dirs):
        """Req 13.5: route() returning Mono<OrchestratorResponseDTO>."""
        content = self._get_service(generator, minimal_orchestrator, output_dirs)
        assert "Mono<OrchestratorResponseDTO> route(" in content

    def test_route_stream_method(self, generator, minimal_orchestrator, output_dirs):
        """Req 13.5: routeStream() returning Flux<String>."""
        content = self._get_service(generator, minimal_orchestrator, output_dirs)
        assert "Flux<String> routeStream(" in content

    def test_system_prompt_present(self, generator, full_orchestrator, output_dirs):
        """Req 13.6: Uses orchestrator systemPrompt."""
        content = self._get_service(generator, full_orchestrator, output_dirs)
        assert "SYSTEM_PROMPT" in content
        assert "You are a helpful AI assistant." in content

    def test_no_system_prompt_when_absent(self, generator, minimal_orchestrator, output_dirs):
        """When systemPrompt is absent, no SYSTEM_PROMPT constant."""
        content = self._get_service(generator, minimal_orchestrator, output_dirs)
        assert 'private static final String SYSTEM_PROMPT' not in content

    def test_access_denied_message_custom(self, generator, full_orchestrator, output_dirs):
        """Req 13.16: Custom accessDeniedMessage."""
        content = self._get_service(generator, full_orchestrator, output_dirs)
        assert "Sorry, you are not authorized." in content

    def test_access_denied_message_default(self, generator, minimal_orchestrator, output_dirs):
        """Req 13.16: Default accessDeniedMessage when not configured."""
        content = self._get_service(generator, minimal_orchestrator, output_dirs)
        assert DEFAULT_ACCESS_DENIED_MESSAGE in content

    def test_get_access_denied_message_method(self, generator, minimal_orchestrator, output_dirs):
        """Req 13.16: getAccessDeniedMessage() method exists."""
        content = self._get_service(generator, minimal_orchestrator, output_dirs)
        assert "getAccessDeniedMessage()" in content

    def test_error_handling_in_route(self, generator, minimal_orchestrator, output_dirs):
        """Req 13.7: Tool failure captured with success=false."""
        content = self._get_service(generator, minimal_orchestrator, output_dirs)
        assert "onErrorResume" in content
        assert "false" in content

    def test_streaming_api_used(self, generator, minimal_orchestrator, output_dirs):
        """Req 13.29: routeStream uses ChatClient streaming API."""
        content = self._get_service(generator, minimal_orchestrator, output_dirs)
        assert ".stream()" in content

    def test_stream_error_handling(self, generator, minimal_orchestrator, output_dirs):
        """Req 13.31: Error mid-stream emits error event."""
        content = self._get_service(generator, minimal_orchestrator, output_dirs)
        assert "[ERROR]" in content

    def test_chat_options_temperature(self, generator, full_orchestrator, output_dirs):
        """Req 13.6: Merged chatOptions applied."""
        content = self._get_service(generator, full_orchestrator, output_dirs)
        assert "0.3" in content

    def test_chat_options_max_tokens(self, generator, full_orchestrator, output_dirs):
        content = self._get_service(generator, full_orchestrator, output_dirs)
        assert "4096" in content

    def test_logging_in_route(self, generator, minimal_orchestrator, output_dirs):
        """Req 13.6: Logs each request with user ID."""
        content = self._get_service(generator, minimal_orchestrator, output_dirs)
        assert "log.info" in content
        assert "userId" in content

    def test_imports_orchestrator_response_dto(self, generator, minimal_orchestrator, output_dirs):
        content = self._get_service(generator, minimal_orchestrator, output_dirs)
        assert f"import {BASE_PACKAGE}.ai.dto.OrchestratorResponseDTO;" in content

    def test_imports_mono_and_flux(self, generator, minimal_orchestrator, output_dirs):
        content = self._get_service(generator, minimal_orchestrator, output_dirs)
        assert "import reactor.core.publisher.Mono;" in content
        assert "import reactor.core.publisher.Flux;" in content


# ======================================================================
# Test: AiOrchestratorController template
# ======================================================================

class TestAiOrchestratorController:
    """Tests for the generated AiOrchestratorController."""

    def _get_controller(self, generator, orchestrator, output_dirs):
        results = generator.generate(orchestrator, BASE_PACKAGE, output_dirs)
        return next(c for fp, c in results if Path(fp).name == "AiOrchestratorController.java")

    def test_package_declaration(self, generator, minimal_orchestrator, output_dirs):
        content = self._get_controller(generator, minimal_orchestrator, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.controller;" in content

    def test_rest_controller_annotation(self, generator, minimal_orchestrator, output_dirs):
        content = self._get_controller(generator, minimal_orchestrator, output_dirs)
        assert "@RestController" in content

    def test_base_path(self, generator, minimal_orchestrator, output_dirs):
        """Req 13.8: Base path /api/ai/orchestrator."""
        content = self._get_controller(generator, minimal_orchestrator, output_dirs)
        assert '@RequestMapping("/api/ai/orchestrator")' in content

    def test_post_request_endpoint(self, generator, minimal_orchestrator, output_dirs):
        """Req 13.8: POST /request endpoint."""
        content = self._get_controller(generator, minimal_orchestrator, output_dirs)
        assert '@PostMapping("/request")' in content
        assert "Mono<OrchestratorResponseDTO> request(" in content

    def test_get_stream_endpoint(self, generator, minimal_orchestrator, output_dirs):
        """Req 13.8: GET /request/stream (SSE) endpoint."""
        content = self._get_controller(generator, minimal_orchestrator, output_dirs)
        assert "/request/stream" in content
        assert "Flux<String> requestStream(" in content

    def test_sse_media_type(self, generator, minimal_orchestrator, output_dirs):
        """Req 13.8: SSE uses text/event-stream media type."""
        content = self._get_controller(generator, minimal_orchestrator, output_dirs)
        assert "MediaType.TEXT_EVENT_STREAM_VALUE" in content

    def test_service_injection(self, generator, minimal_orchestrator, output_dirs):
        content = self._get_controller(generator, minimal_orchestrator, output_dirs)
        assert "AiOrchestratorService" in content

    def test_request_body_annotation(self, generator, minimal_orchestrator, output_dirs):
        content = self._get_controller(generator, minimal_orchestrator, output_dirs)
        assert "@RequestBody" in content

    def test_request_param_annotation(self, generator, minimal_orchestrator, output_dirs):
        content = self._get_controller(generator, minimal_orchestrator, output_dirs)
        assert "@RequestParam" in content

    def test_imports_media_type(self, generator, minimal_orchestrator, output_dirs):
        content = self._get_controller(generator, minimal_orchestrator, output_dirs)
        assert "import org.springframework.http.MediaType;" in content


# ======================================================================
# Test: Context building
# ======================================================================

class TestBuildContext:
    """Tests for the _build_context method."""

    def test_provider_name(self, generator, minimal_orchestrator):
        ctx = generator._build_context(minimal_orchestrator, BASE_PACKAGE)
        assert ctx["provider_name"] == "mainGpt"

    def test_default_access_denied_message(self, generator, minimal_orchestrator):
        ctx = generator._build_context(minimal_orchestrator, BASE_PACKAGE)
        assert ctx["access_denied_message"] == DEFAULT_ACCESS_DENIED_MESSAGE

    def test_custom_access_denied_message(self, generator, full_orchestrator):
        ctx = generator._build_context(full_orchestrator, BASE_PACKAGE)
        assert ctx["access_denied_message"] == "Sorry, you are not authorized."

    def test_system_prompt_present(self, generator, full_orchestrator):
        ctx = generator._build_context(full_orchestrator, BASE_PACKAGE)
        assert ctx["system_prompt"] == "You are a helpful AI assistant."

    def test_system_prompt_absent(self, generator, minimal_orchestrator):
        ctx = generator._build_context(minimal_orchestrator, BASE_PACKAGE)
        assert ctx["system_prompt"] == ""

    def test_chat_options_present(self, generator, full_orchestrator):
        ctx = generator._build_context(full_orchestrator, BASE_PACKAGE)
        assert ctx["chat_options"]["temperature"] == 0.3
        assert ctx["chat_options"]["maxTokens"] == 4096
        assert ctx["chat_options"]["topP"] == 0.9

    def test_chat_options_absent(self, generator, minimal_orchestrator):
        ctx = generator._build_context(minimal_orchestrator, BASE_PACKAGE)
        assert ctx["chat_options"] is None

    def test_base_package(self, generator, minimal_orchestrator):
        ctx = generator._build_context(minimal_orchestrator, BASE_PACKAGE)
        assert ctx["base_package"] == BASE_PACKAGE
