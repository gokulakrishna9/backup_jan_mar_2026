"""LLM Provider Manager — multi-provider LLM abstraction via LiteLLM.

Singleton service that manages AI configuration, model registry, active model
selection, parameter tuning, completion with auto-fallback, health checks,
and custom endpoint management.

Reads configuration from ``ai_config.yaml`` (path defined in ``config.py``).
Environment variables override YAML values for API keys.

Requirements: 13.2, 13.3, 13.5, 13.6, 13.7, 13.8, 13.9, 13.10
"""

from __future__ import annotations

import asyncio
import copy
import logging
import os
from pathlib import Path
from typing import Any, Optional

import yaml

from workspace_web_app.engine.config import AI_CONFIG_PATH

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Provider → environment variable mapping for API keys
# ---------------------------------------------------------------------------

_PROVIDER_ENV_MAP: dict[str, str] = {
    "openai": "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "google": "GEMINI_API_KEY",
    "ollama": "OLLAMA_API_BASE",
    "together ai": "TOGETHERAI_API_KEY",
    "groq": "GROQ_API_KEY",
    "aws bedrock": "AWS_ACCESS_KEY_ID",
}


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------


def _validate_model_params(params: dict[str, Any]) -> dict[str, Any]:
    """Validate and clamp model parameters to acceptable ranges.

    Raises:
        ValueError: If a parameter value is invalid and cannot be clamped.
    """
    validated: dict[str, Any] = {}

    if "temperature" in params:
        temp = float(params["temperature"])
        if temp < 0.0 or temp > 2.0:
            raise ValueError(
                f"temperature must be between 0.0 and 2.0, got {temp}"
            )
        validated["temperature"] = temp

    if "max_tokens" in params:
        max_tok = int(params["max_tokens"])
        if max_tok <= 0:
            raise ValueError(f"max_tokens must be > 0, got {max_tok}")
        validated["max_tokens"] = max_tok

    if "top_p" in params:
        top_p = float(params["top_p"])
        if top_p < 0.0 or top_p > 1.0:
            raise ValueError(f"top_p must be between 0.0 and 1.0, got {top_p}")
        validated["top_p"] = top_p

    if "frequency_penalty" in params:
        fp = float(params["frequency_penalty"])
        if fp < -2.0 or fp > 2.0:
            raise ValueError(
                f"frequency_penalty must be between -2.0 and 2.0, got {fp}"
            )
        validated["frequency_penalty"] = fp

    return validated


# ---------------------------------------------------------------------------
# LLMProviderManager — Singleton
# ---------------------------------------------------------------------------


class LLMProviderManager:
    """Manages LLM providers, model selection, and completion via LiteLLM.

    Implements the singleton pattern — all instantiations return the same
    shared instance so that configuration state is consistent across the
    engine service.

    Key behaviors:
      - Loads and validates ``ai_config.yaml`` at startup.
      - Provides a model registry grouped by provider for the UI.
      - Validates model IDs against the registry (all known models from all
        providers + custom endpoints).
      - On primary model failure, automatically tries the fallback model.
      - Health check sends a lightweight prompt and classifies the result.
      - Environment variables override YAML values for API keys.
    """

    _instance: Optional[LLMProviderManager] = None

    def __new__(cls) -> LLMProviderManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
        self._initialized = True
        self._config: dict[str, Any] = {}
        self._active_model: str = ""
        self._fallback_model: str = ""
        self._model_params: dict[str, Any] = {}
        self._providers: list[dict[str, Any]] = []
        self._custom_endpoints: list[dict[str, Any]] = []
        self._model_registry_cache: Optional[list[dict[str, Any]]] = None
        self._load_config()

    # ------------------------------------------------------------------
    # Config loading and persistence
    # ------------------------------------------------------------------

    def _load_config(self) -> None:
        """Load and validate ai_config.yaml from disk.

        Sets active model, fallback model, model parameters, providers,
        and custom endpoints from the YAML file.
        """
        config_path = Path(AI_CONFIG_PATH)
        if not config_path.exists():
            logger.warning(
                "AI config file not found at %s — using defaults", config_path
            )
            self._config = {}
            self._active_model = "gpt-4"
            self._fallback_model = "ollama/llama3"
            self._model_params = {
                "temperature": 0.7,
                "max_tokens": 4096,
                "top_p": 1.0,
                "frequency_penalty": 0.0,
            }
            self._providers = []
            self._custom_endpoints = []
            self._model_registry_cache = None
            return

        with open(config_path, "r") as f:
            raw = yaml.safe_load(f) or {}

        self._config = raw
        self._active_model = raw.get("default_model", "gpt-4")
        self._fallback_model = raw.get("fallback_model", "ollama/llama3")
        self._model_params = raw.get("model_params", {
            "temperature": 0.7,
            "max_tokens": 4096,
            "top_p": 1.0,
            "frequency_penalty": 0.0,
        })
        self._providers = raw.get("providers", [])
        self._custom_endpoints = raw.get("custom_endpoints", [])
        # Invalidate registry cache on reload
        self._model_registry_cache = None

        logger.info(
            "AI config loaded: active_model=%s, fallback=%s, providers=%d, custom_endpoints=%d",
            self._active_model,
            self._fallback_model,
            len(self._providers),
            len(self._custom_endpoints),
        )

    def reload_config(self) -> None:
        """Reload configuration from disk (runtime hot-reload)."""
        self._load_config()

    def save_config(self) -> None:
        """Persist current configuration state to ai_config.yaml."""
        config_path = Path(AI_CONFIG_PATH)

        data = {
            "default_model": self._active_model,
            "fallback_model": self._fallback_model,
            "model_params": copy.deepcopy(self._model_params),
            "providers": copy.deepcopy(self._providers),
            "custom_endpoints": copy.deepcopy(self._custom_endpoints),
        }

        with open(config_path, "w") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)

        logger.info("AI config saved to %s", config_path)

    # ------------------------------------------------------------------
    # Model registry
    # ------------------------------------------------------------------

    def get_model_registry(self) -> list[dict[str, Any]]:
        """Return models grouped by provider for the UI.

        Returns:
            List of provider dicts, each containing:
              - ``name``: Provider display name
              - ``api_key_env``: Environment variable name for the API key
              - ``api_key_configured``: Whether the env var is set
              - ``models``: List of model dicts with ``id`` and ``display_name``
        """
        if self._model_registry_cache is not None:
            return self._model_registry_cache

        registry: list[dict[str, Any]] = []

        for provider in self._providers:
            env_var = provider.get("api_key_env", "")
            registry.append({
                "name": provider["name"],
                "api_key_env": env_var,
                "api_key_configured": bool(os.environ.get(env_var, "")),
                "models": [
                    {"id": m["id"], "display_name": m["display_name"]}
                    for m in provider.get("models", [])
                ],
            })

        # Add custom endpoints as providers
        for endpoint in self._custom_endpoints:
            registry.append({
                "name": endpoint["name"],
                "api_key_env": "",
                "api_key_configured": True,  # Custom endpoints manage their own keys
                "models": [
                    {"id": m_id, "display_name": m_id}
                    for m_id in endpoint.get("models", [])
                ],
            })

        self._model_registry_cache = registry
        return registry

    def _get_all_known_model_ids(self) -> set[str]:
        """Return all model IDs from all providers and custom endpoints."""
        ids: set[str] = set()
        for provider in self._providers:
            for model in provider.get("models", []):
                ids.add(model["id"])
        for endpoint in self._custom_endpoints:
            for m_id in endpoint.get("models", []):
                ids.add(m_id)
        return ids

    # ------------------------------------------------------------------
    # Active model management
    # ------------------------------------------------------------------

    def get_active_model(self) -> str:
        """Return the currently active model ID."""
        return self._active_model

    def set_active_model(self, model_id: str) -> None:
        """Set the active model, validating against the model registry.

        Args:
            model_id: A LiteLLM-compatible model identifier.

        Raises:
            ValueError: If the model_id is not recognized in the registry.
        """
        known_ids = self._get_all_known_model_ids()
        if model_id not in known_ids:
            raise ValueError(
                f"Model '{model_id}' is not recognized. "
                f"Available models: {sorted(known_ids)}"
            )
        self._active_model = model_id
        logger.info("Active model set to: %s", model_id)

    # ------------------------------------------------------------------
    # Model parameters
    # ------------------------------------------------------------------

    def get_model_params(self) -> dict[str, Any]:
        """Return current model parameters (temperature, max_tokens, etc.)."""
        return copy.deepcopy(self._model_params)

    def update_model_params(self, params: dict[str, Any]) -> None:
        """Update model parameters with validation.

        Only updates keys that are provided. Validates ranges before applying.

        Args:
            params: Dict with any of: temperature, max_tokens, top_p, frequency_penalty.

        Raises:
            ValueError: If any parameter value is out of range.
        """
        validated = _validate_model_params(params)
        self._model_params.update(validated)
        logger.info("Model params updated: %s", validated)

    # ------------------------------------------------------------------
    # Completion (LiteLLM)
    # ------------------------------------------------------------------

    async def completion(self, messages: list[dict[str, str]], **kwargs: Any) -> Any:
        """Call LiteLLM acompletion with the active model.

        On failure, automatically retries with the fallback model. If both
        fail, raises the last exception.

        Args:
            messages: List of message dicts (role + content).
            **kwargs: Additional parameters passed to litellm.acompletion.

        Returns:
            LiteLLM response object (OpenAI-compatible).

        Raises:
            RuntimeError: If no API key is configured for the model's provider.
            Exception: If both primary and fallback models fail.
        """
        import litellm

        # Check API key availability for the active model
        self._check_api_key(self._active_model)

        # Build call parameters
        call_params = {
            "model": self._active_model,
            "messages": messages,
            **self._model_params,
            **kwargs,
        }

        # Attempt primary model
        try:
            response = await litellm.acompletion(**call_params)
            return response
        except Exception as primary_error:
            logger.warning(
                "Primary model '%s' failed: %s. Trying fallback '%s'.",
                self._active_model,
                primary_error,
                self._fallback_model,
            )

        # Attempt fallback model
        if not self._fallback_model:
            raise primary_error  # noqa: F821 — re-raise if no fallback configured

        try:
            self._check_api_key(self._fallback_model)
        except RuntimeError:
            # If fallback also has no key, raise the original error
            raise primary_error  # noqa: F821

        fallback_params = {
            "model": self._fallback_model,
            "messages": messages,
            **self._model_params,
            **kwargs,
        }

        try:
            response = await litellm.acompletion(**fallback_params)
            logger.info("Fallback model '%s' succeeded.", self._fallback_model)
            return response
        except Exception as fallback_error:
            logger.error(
                "Both primary ('%s') and fallback ('%s') models failed. "
                "Primary error: %s | Fallback error: %s",
                self._active_model,
                self._fallback_model,
                primary_error,
                fallback_error,
            )
            raise fallback_error

    def _check_api_key(self, model_id: str) -> None:
        """Verify that the required API key is available for a model.

        Raises:
            RuntimeError: With a descriptive message including the env var name.
        """
        provider = self._find_provider_for_model(model_id)
        if provider is None:
            # Model might be from a custom endpoint or unknown — allow through
            return

        env_var = provider.get("api_key_env", "")
        if not env_var:
            return

        # Ollama uses OLLAMA_API_BASE which is a URL, not a key — optional
        if provider["name"].lower() == "ollama":
            return

        if not os.environ.get(env_var, ""):
            raise RuntimeError(
                f"No API key configured for provider '{provider['name']}'. "
                f"Set the environment variable '{env_var}' to use model '{model_id}'."
            )

    def _find_provider_for_model(self, model_id: str) -> Optional[dict[str, Any]]:
        """Find the provider entry that contains the given model ID."""
        for provider in self._providers:
            for model in provider.get("models", []):
                if model["id"] == model_id:
                    return provider
        return None

    # ------------------------------------------------------------------
    # Health check
    # ------------------------------------------------------------------

    async def health_check(self, provider_name: str) -> dict[str, Any]:
        """Send a lightweight test prompt to a provider and report status.

        Args:
            provider_name: Display name of the provider (e.g., "OpenAI").

        Returns:
            Dict with ``status`` and ``message`` keys.
            Status is one of: "reachable", "auth_error", "timeout", "error".
        """
        import litellm

        # Find the provider and pick the first model for testing
        provider = self._find_provider_by_name(provider_name)
        if provider is None:
            return {
                "status": "error",
                "message": f"Provider '{provider_name}' not found in configuration.",
            }

        models = provider.get("models", [])
        if not models:
            return {
                "status": "error",
                "message": f"No models configured for provider '{provider_name}'.",
            }

        test_model = models[0]["id"]

        # Check API key first
        env_var = provider.get("api_key_env", "")
        if env_var and provider["name"].lower() != "ollama":
            if not os.environ.get(env_var, ""):
                return {
                    "status": "auth_error",
                    "message": (
                        f"API key not configured. "
                        f"Set environment variable '{env_var}'."
                    ),
                }

        # Send lightweight test prompt
        test_messages = [{"role": "user", "content": "Say hello"}]

        try:
            await litellm.acompletion(
                model=test_model,
                messages=test_messages,
                max_tokens=5,
                timeout=10,
            )
            return {
                "status": "reachable",
                "message": f"Provider '{provider_name}' is reachable.",
            }
        except litellm.AuthenticationError:
            return {
                "status": "auth_error",
                "message": (
                    f"Authentication failed for '{provider_name}'. "
                    f"Check your API key in '{env_var}'."
                ),
            }
        except (asyncio.TimeoutError, litellm.Timeout):
            return {
                "status": "timeout",
                "message": f"Provider '{provider_name}' timed out.",
            }
        except Exception as exc:
            return {
                "status": "error",
                "message": f"Provider '{provider_name}' error: {exc}",
            }

    def _find_provider_by_name(self, name: str) -> Optional[dict[str, Any]]:
        """Find a provider entry by display name (case-insensitive)."""
        name_lower = name.lower()
        for provider in self._providers:
            if provider["name"].lower() == name_lower:
                return provider
        # Also check custom endpoints
        for endpoint in self._custom_endpoints:
            if endpoint["name"].lower() == name_lower:
                return endpoint
        return None

    # ------------------------------------------------------------------
    # Custom endpoints
    # ------------------------------------------------------------------

    def add_custom_endpoint(
        self,
        name: str,
        base_url: str,
        api_key: str = "",
        models: Optional[list[str]] = None,
    ) -> None:
        """Add a custom OpenAI-compatible endpoint.

        Custom endpoints use the ``openai/`` prefix for LiteLLM routing.

        Args:
            name: Display name for the endpoint.
            base_url: Base URL of the OpenAI-compatible API.
            api_key: Optional API key for the endpoint.
            models: List of model identifiers available at this endpoint.
        """
        if models is None:
            models = []

        # Prefix model IDs with openai/ for LiteLLM routing if not already
        prefixed_models = []
        for m in models:
            if not m.startswith("openai/"):
                prefixed_models.append(f"openai/{m}")
            else:
                prefixed_models.append(m)

        endpoint = {
            "name": name,
            "base_url": base_url,
            "api_key": api_key,
            "models": prefixed_models,
        }

        # Remove existing endpoint with same name if present
        self._custom_endpoints = [
            ep for ep in self._custom_endpoints if ep["name"] != name
        ]
        self._custom_endpoints.append(endpoint)

        # Set LiteLLM environment for the custom endpoint
        if api_key:
            os.environ[f"OPENAI_API_KEY_{name.upper().replace(' ', '_')}"] = api_key
        if base_url:
            os.environ[f"OPENAI_API_BASE_{name.upper().replace(' ', '_')}"] = base_url

        # Invalidate registry cache
        self._model_registry_cache = None
        logger.info("Custom endpoint added: %s (%s)", name, base_url)

    def remove_custom_endpoint(self, name: str) -> None:
        """Remove a custom endpoint by name.

        Args:
            name: Display name of the endpoint to remove.

        Raises:
            ValueError: If the endpoint is not found.
        """
        original_len = len(self._custom_endpoints)
        self._custom_endpoints = [
            ep for ep in self._custom_endpoints if ep["name"] != name
        ]

        if len(self._custom_endpoints) == original_len:
            raise ValueError(f"Custom endpoint '{name}' not found.")

        # Invalidate registry cache
        self._model_registry_cache = None
        logger.info("Custom endpoint removed: %s", name)
