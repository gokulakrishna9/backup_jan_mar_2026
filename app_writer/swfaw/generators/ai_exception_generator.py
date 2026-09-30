"""Exception handler sub-generator for the AI Layer.

Generates AiExceptionHandler (@ControllerAdvice scoped to ai package),
AiErrorResponseDTO, and additional exception classes
(PromptSecurityViolationException, ModerationException,
TokenBudgetExceededException).

Requirements: 14.9–14.26
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import jinja2

# Complete exception-to-HTTP-status mapping used by the handler.
# Each entry: (exception_class, http_status, error_code)
EXCEPTION_MAPPINGS: list[tuple[str, int, str]] = [
    ("UnsupportedRoleException", 400, "UNSUPPORTED_ROLE"),
    ("UnsupportedParameterException", 400, "UNSUPPORTED_PARAMETER"),
    ("TypedResponseDeserializationException", 502, "LLM_RESPONSE_PARSE_ERROR"),
    ("ProviderCircuitOpenException", 503, "PROVIDER_CIRCUIT_OPEN"),
    ("PromptSecurityViolationException", 422, "PROMPT_SECURITY_VIOLATION"),
    ("ModerationException", 422, "CONTENT_MODERATION_BLOCKED"),
    ("TokenBudgetExceededException", 429, "TOKEN_BUDGET_EXCEEDED"),
    ("RateLimitExceededException", 429, "RATE_LIMIT_EXCEEDED"),
]

# Additional mappings handled via broader exception types
BROAD_EXCEPTION_MAPPINGS: list[tuple[str, int, str]] = [
    ("AccessDeniedException", 403, "AI_ACCESS_DENIED"),
    ("InvalidDocumentTypeException", 400, "INVALID_DOCUMENT_TYPE"),
    ("DocumentTooLargeException", 413, "DOCUMENT_TOO_LARGE"),
    ("McpServerException", 502, "MCP_SERVER_ERROR"),
]

# Catch-all for unhandled exceptions
CATCH_ALL_STATUS = 500
CATCH_ALL_ERROR_CODE = "AI_INTERNAL_ERROR"

# LLM provider error mapping
LLM_PROVIDER_STATUS = 502
LLM_PROVIDER_ERROR_CODE = "LLM_PROVIDER_ERROR"


class ExceptionGenerator:
    """Generates AiExceptionHandler, AiErrorResponseDTO, and exception classes.

    Follows the same sub-generator pattern as other AI generators:
    receives parsed definition data, loads and renders Jinja2 templates,
    and returns a list of ``(filepath, content)`` tuples.
    """

    def __init__(self, jinja_env: "jinja2.Environment"):
        self.jinja_env = jinja_env

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(
        self,
        ai_layer: dict,
        base_package: str,
        output_dirs: dict[str, Path],
    ) -> list[tuple[str, str]]:
        """Generate exception handler and error DTO Java files.

        The exception handler is always generated when any AI feature is
        configured — it is a shared component.

        Returns a list of ``(filepath, content)`` tuples where *filepath*
        is relative to the project source root.
        """
        results: list[tuple[str, str]] = []

        controller_dir = output_dirs.get("controller", Path("ai/controller"))
        dto_dir = output_dirs.get("dto", Path("ai/dto"))
        provider_dir = output_dirs.get("provider", Path("ai/provider"))

        # Build context for templates
        ctx = self._build_context(ai_layer, base_package)

        # 1. AiExceptionHandler (Req 14.9, 14.11–14.23)
        results.append((
            str(controller_dir / "AiExceptionHandler.java"),
            self._render("controller/ai_exception_handler.java.j2", ctx),
        ))

        # 2. AiErrorResponseDTO (Req 14.10)
        results.append((
            str(dto_dir / "AiErrorResponseDTO.java"),
            self._render("dto/error_dtos.java.j2", {
                "base_package": base_package,
            }),
        ))

        # 3. Additional exception classes (Req 14.24)
        results.extend(
            self._generate_exception_classes(base_package, provider_dir)
        )

        return results

    # ------------------------------------------------------------------
    # Context builder
    # ------------------------------------------------------------------

    def _build_context(self, ai_layer: dict, base_package: str) -> dict:
        """Build Jinja2 context for the exception handler template."""
        # Determine which features are active to conditionally import
        # the relevant exception classes.
        has_orchestrator = ai_layer.get("orchestrator") is not None
        has_moderation = (
            has_orchestrator
            and ai_layer.get("orchestrator", {})
            .get("moderation", {})
            .get("enabled", False)
        )
        has_prompt_security = (
            has_orchestrator
            and ai_layer.get("orchestrator", {}).get("promptSecurity") is not None
        )
        has_document_ingestion = (
            ai_layer.get("documentIngestion") is not None
            and ai_layer.get("documentIngestion", {}).get("enabled", False)
        )
        has_document_processing = (
            ai_layer.get("documentProcessing") is not None
            and ai_layer.get("documentProcessing", {}).get("enabled", False)
        )
        has_mcp = bool(ai_layer.get("mcpServers"))
        has_token_budget = (
            ai_layer.get("tokenBudget") is not None
            and ai_layer.get("tokenBudget", {}).get("enabled", False)
        )
        has_rate_limiting = ai_layer.get("rateLimiting") is not None

        return {
            "base_package": base_package,
            "exception_mappings": EXCEPTION_MAPPINGS,
            "broad_exception_mappings": BROAD_EXCEPTION_MAPPINGS,
            "catch_all_status": CATCH_ALL_STATUS,
            "catch_all_error_code": CATCH_ALL_ERROR_CODE,
            "llm_provider_status": LLM_PROVIDER_STATUS,
            "llm_provider_error_code": LLM_PROVIDER_ERROR_CODE,
            "has_orchestrator": has_orchestrator,
            "has_moderation": has_moderation,
            "has_prompt_security": has_prompt_security,
            "has_document_ingestion": has_document_ingestion,
            "has_document_processing": has_document_processing,
            "has_mcp": has_mcp,
            "has_token_budget": has_token_budget,
            "has_rate_limiting": has_rate_limiting,
        }

    # ------------------------------------------------------------------
    # Exception class generation
    # ------------------------------------------------------------------

    def _generate_exception_classes(
        self,
        base_package: str,
        provider_dir: Path,
    ) -> list[tuple[str, str]]:
        """Generate additional exception classes not already produced by
        the provider generator.

        The provider generator already creates:
        - UnsupportedRoleException
        - UnsupportedParameterException
        - TypedResponseDeserializationException
        - ProviderCircuitOpenException

        This generator adds:
        - PromptSecurityViolationException (Req 14.14, 14.24)
        - ModerationException (Req 14.15, 14.24)
        - TokenBudgetExceededException (Req 14.22, 15.27)
        - RateLimitExceededException (Req 14.16)
        - InvalidDocumentTypeException (Req 14.19)
        - DocumentTooLargeException (Req 14.19)
        - McpServerException (Req 14.20)
        """
        results: list[tuple[str, str]] = []
        ctx = {"base_package": base_package}

        exception_defs = [
            ("PromptSecurityViolationException", self._prompt_security_violation_body),
            ("ModerationException", self._moderation_exception_body),
            ("TokenBudgetExceededException", self._token_budget_exceeded_body),
            ("RateLimitExceededException", self._rate_limit_exceeded_body),
            ("InvalidDocumentTypeException", self._invalid_document_type_body),
            ("DocumentTooLargeException", self._document_too_large_body),
            ("McpServerException", self._mcp_server_exception_body),
        ]

        for class_name, body_fn in exception_defs:
            content = body_fn(base_package)
            results.append((
                str(provider_dir / f"{class_name}.java"),
                content,
            ))

        return results

    # ------------------------------------------------------------------
    # Exception class bodies
    # ------------------------------------------------------------------

    @staticmethod
    def _prompt_security_violation_body(base_package: str) -> str:
        return f"""package {base_package}.ai.provider;

/**
 * Thrown when a prompt security violation is detected
 * (SafeGuard sensitive word match or CanaryWord leakage).
 * HTTP 422 (PROMPT_SECURITY_VIOLATION) via AiExceptionHandler.
 *
 * Generated by SWFAW AI Layer generator.
 */
public class PromptSecurityViolationException extends RuntimeException {{

    private final String violationType;

    public PromptSecurityViolationException(String violationType, String message) {{
        super(message);
        this.violationType = violationType;
    }}

    public String getViolationType() {{ return violationType; }}
}}
"""

    @staticmethod
    def _moderation_exception_body(base_package: str) -> str:
        return f"""package {base_package}.ai.provider;

import java.util.List;

/**
 * Thrown when content moderation blocks a request or response.
 * HTTP 422 (CONTENT_MODERATION_BLOCKED) via AiExceptionHandler.
 *
 * Generated by SWFAW AI Layer generator.
 */
public class ModerationException extends RuntimeException {{

    private final List<String> flaggedCategories;
    private final String action;

    public ModerationException(String message, List<String> flaggedCategories, String action) {{
        super(message);
        this.flaggedCategories = flaggedCategories;
        this.action = action;
    }}

    public List<String> getFlaggedCategories() {{ return flaggedCategories; }}
    public String getAction() {{ return action; }}
}}
"""

    @staticmethod
    def _token_budget_exceeded_body(base_package: str) -> str:
        return f"""package {base_package}.ai.provider;

/**
 * Thrown when a user's token budget is exceeded and enforcement is "block".
 * HTTP 429 (TOKEN_BUDGET_EXCEEDED) via AiExceptionHandler.
 *
 * Generated by SWFAW AI Layer generator.
 */
public class TokenBudgetExceededException extends RuntimeException {{

    private final String providerName;
    private final long currentUsage;
    private final long limit;
    private final String period;

    public TokenBudgetExceededException(String providerName, long currentUsage, long limit, String period) {{
        super(String.format("Token budget exceeded for provider '%s': %d/%d (%s)",
                providerName, currentUsage, limit, period));
        this.providerName = providerName;
        this.currentUsage = currentUsage;
        this.limit = limit;
        this.period = period;
    }}

    public String getProviderName() {{ return providerName; }}
    public long getCurrentUsage() {{ return currentUsage; }}
    public long getLimit() {{ return limit; }}
    public String getPeriod() {{ return period; }}
}}
"""

    @staticmethod
    def _rate_limit_exceeded_body(base_package: str) -> str:
        return f"""package {base_package}.ai.provider;

/**
 * Thrown when the per-user rate limit is exceeded for an AI endpoint.
 * HTTP 429 (RATE_LIMIT_EXCEEDED) via AiExceptionHandler.
 *
 * Generated by SWFAW AI Layer generator.
 */
public class RateLimitExceededException extends RuntimeException {{

    private final int retryAfterSeconds;

    public RateLimitExceededException(String message, int retryAfterSeconds) {{
        super(message);
        this.retryAfterSeconds = retryAfterSeconds;
    }}

    public int getRetryAfterSeconds() {{ return retryAfterSeconds; }}
}}
"""

    @staticmethod
    def _invalid_document_type_body(base_package: str) -> str:
        return f"""package {base_package}.ai.provider;

/**
 * Thrown when an uploaded document has an unsupported MIME type.
 * HTTP 400 (INVALID_DOCUMENT_TYPE) via AiExceptionHandler.
 *
 * Generated by SWFAW AI Layer generator.
 */
public class InvalidDocumentTypeException extends RuntimeException {{

    private final String mimeType;

    public InvalidDocumentTypeException(String mimeType) {{
        super("Unsupported document MIME type: " + mimeType);
        this.mimeType = mimeType;
    }}

    public String getMimeType() {{ return mimeType; }}
}}
"""

    @staticmethod
    def _document_too_large_body(base_package: str) -> str:
        return f"""package {base_package}.ai.provider;

/**
 * Thrown when an uploaded document exceeds the maximum allowed size.
 * HTTP 413 (DOCUMENT_TOO_LARGE) via AiExceptionHandler.
 *
 * Generated by SWFAW AI Layer generator.
 */
public class DocumentTooLargeException extends RuntimeException {{

    private final long fileSize;
    private final long maxSize;

    public DocumentTooLargeException(long fileSize, long maxSize) {{
        super(String.format("Document size %d bytes exceeds maximum allowed %d bytes", fileSize, maxSize));
        this.fileSize = fileSize;
        this.maxSize = maxSize;
    }}

    public long getFileSize() {{ return fileSize; }}
    public long getMaxSize() {{ return maxSize; }}
}}
"""

    @staticmethod
    def _mcp_server_exception_body(base_package: str) -> str:
        return f"""package {base_package}.ai.provider;

/**
 * Thrown when an MCP server encounters a connection or tool invocation error.
 * HTTP 502 (MCP_SERVER_ERROR) via AiExceptionHandler.
 *
 * Generated by SWFAW AI Layer generator.
 */
public class McpServerException extends RuntimeException {{

    private final String serverName;

    public McpServerException(String serverName, String message) {{
        super(message);
        this.serverName = serverName;
    }}

    public McpServerException(String serverName, String message, Throwable cause) {{
        super(message, cause);
        this.serverName = serverName;
    }}

    public String getServerName() {{ return serverName; }}
}}
"""

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def _render(self, template_name: str, ctx: dict) -> str:
        """Render a Jinja2 template under the ai/ prefix."""
        template = self.jinja_env.get_template(f"ai/{template_name}")
        return template.render(**ctx)
