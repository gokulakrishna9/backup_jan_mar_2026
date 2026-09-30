"""Provider sub-generator for the AI Layer.

Generates ChatClientConfig, ChatOptionsResolver, RoleValidationAdvisor,
ProviderResilienceConfig, and exception classes from the AI_Layer providers
definition.

Requirements: 2.1–2.8, 2.20–2.34
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import jinja2

# Marker used inside the exceptions template to split into multiple files.
_FILESPLIT_MARKER = "###FILESPLIT:"


class ProviderGenerator:
    """Generates ChatClientConfig, ChatOptionsResolver, RoleValidationAdvisor,
    ProviderResilienceConfig, and exception classes."""

    def __init__(self, jinja_env: "jinja2.Environment"):
        self.jinja_env = jinja_env

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(
        self,
        providers: list[dict],
        base_package: str,
        output_dirs: dict[str, Path],
    ) -> list[tuple[str, str]]:
        """Generate all provider-related Java files.

        Returns a list of ``(filepath, content)`` tuples where *filepath* is
        relative to the project source root.
        """
        if not providers:
            return []

        results: list[tuple[str, str]] = []

        config_dir = output_dirs.get("config", Path("ai/config"))
        provider_dir = output_dirs.get("provider", Path("ai/provider"))

        # 1. ChatClientConfig (Req 2.1–2.3, 2.6–2.7)
        content = self._render_chat_client_config(providers, base_package)
        results.append((str(config_dir / "ChatClientConfig.java"), content))

        # 2. ChatOptionsResolver (Req 2.9–2.13, 2.15–2.16)
        content = self._render_chat_options_resolver(providers, base_package)
        results.append((str(provider_dir / "ChatOptionsResolver.java"), content))

        # 3. RoleValidationAdvisor (Req 2.17–2.19)
        content = self._render_role_validation_advisor(providers, base_package)
        results.append((str(provider_dir / "RoleValidationAdvisor.java"), content))

        # 4. ProviderResilienceConfig (Req 2.21–2.33)
        content = self._render_resilience_config(providers, base_package)
        results.append((str(provider_dir / "ProviderResilienceConfig.java"), content))

        # 5. Exception classes (Req 2.20, 2.28)
        for filename, exc_content in self._render_exception_classes(base_package):
            results.append((str(provider_dir / filename), exc_content))

        return results

    # ------------------------------------------------------------------
    # Private render helpers
    # ------------------------------------------------------------------

    def _render_chat_client_config(
        self, providers: list[dict], base_package: str
    ) -> str:
        """Render the ChatClientConfig @Configuration class.

        Req 2.1: OpenAI → OpenAiChatModel + OpenAiEmbeddingModel
        Req 2.2: Ollama → OllamaChatModel + OllamaEmbeddingModel
        Req 2.3: @Configuration class
        Req 2.6: Single provider → also @Primary (default beans)
        Req 2.7: Inject supportedRoles, roleFallbacks, chatOptions, etc.
        """
        template = self.jinja_env.get_template(
            "ai/config/chat_client_config.java.j2"
        )
        # De-duplicate import types
        has_openai = any(p["type"] == "openai" for p in providers)
        has_ollama = any(p["type"] == "ollama" for p in providers)
        return template.render(
            base_package=base_package,
            providers=providers,
            has_openai=has_openai,
            has_ollama=has_ollama,
        )

    def _render_chat_options_resolver(
        self, providers: list[dict], base_package: str
    ) -> str:
        """Render the ChatOptionsResolver utility class.

        Req 2.9–2.13: Parameter validation and mapping per provider type.
        Req 2.15: Empty supportedParameters → skip all with warning.
        Req 2.16: Parameter compliance invariant.
        """
        template = self.jinja_env.get_template(
            "ai/provider/chat_options_resolver.java.j2"
        )
        return template.render(
            base_package=base_package,
            providers=providers,
        )

    def _render_role_validation_advisor(
        self, providers: list[dict], base_package: str
    ) -> str:
        """Render the RoleValidationAdvisor utility class.

        Req 2.17: Validate roles, apply fallbacks (prepend_to_user, skip,
                  merge_to_system, error).
        Req 2.18: Operates on defensive copy before ChatClient call.
        Req 2.19: Role compliance invariant.
        """
        template = self.jinja_env.get_template(
            "ai/provider/role_validation_advisor.java.j2"
        )
        return template.render(
            base_package=base_package,
            providers=providers,
        )

    def _render_resilience_config(
        self, providers: list[dict], base_package: str
    ) -> str:
        """Render the ProviderResilienceConfig @Configuration class.

        Req 2.21–2.27: Retry with exponential backoff, circuit breaker.
        Req 2.24: Default resilience when absent.
        Req 2.25: Retry logging at WARN.
        Req 2.26: Circuit breaker OPEN logging at ERROR.
        Req 2.29: application.properties entries.
        Req 2.31: Resilience4j Reactor integration.
        """
        template = self.jinja_env.get_template(
            "ai/provider/provider_resilience_config.java.j2"
        )
        return template.render(
            base_package=base_package,
            providers=providers,
        )

    def _render_exception_classes(
        self, base_package: str
    ) -> list[tuple[str, str]]:
        """Render all provider exception classes.

        Req 2.20: UnsupportedRoleException, UnsupportedParameterException,
                  TypedResponseDeserializationException.
        Req 2.28: ProviderCircuitOpenException.

        Returns a list of ``(filename, content)`` tuples.
        """
        template = self.jinja_env.get_template(
            "ai/provider/exceptions.java.j2"
        )
        raw = template.render(base_package=base_package)

        # Split the rendered output by the FILESPLIT markers.
        results: list[tuple[str, str]] = []
        parts = raw.split(_FILESPLIT_MARKER)
        for part in parts:
            part = part.strip()
            if not part:
                continue
            # Each part starts with "ClassName.java###\n<content>"
            if "###" in part:
                filename, content = part.split("###", 1)
                filename = filename.strip()
                content = content.strip()
                if filename and content:
                    results.append((filename, content))
        return results
