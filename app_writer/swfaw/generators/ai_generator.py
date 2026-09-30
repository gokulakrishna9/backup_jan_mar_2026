"""Main AI Generator coordinator for the AI Layer.

Coordinates all AI code generation from the AI_Layer definition by
delegating to sub-generators in dependency order, collecting their
``(filepath, content)`` tuples, and writing them to disk.

Requirements: All (coordinator)
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import jinja2

if TYPE_CHECKING:
    from swfaw.utils.definition_loader import DefinitionBundle


class AiGenerator:
    """Coordinates all AI code generation from the AI_Layer definition."""

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(self, bundle: "DefinitionBundle", output_dir: Path) -> list[Path]:
        """Full generation: validate, then generate all AI code.

        1. Validates the AI_Layer definition
        2. Sets up Jinja2 environment
        3. Resolves output directories from base_package
        4. Calls each sub-generator in dependency order
        5. Writes all (filepath, content) tuples to disk
        6. Returns list of written Paths
        """
        ai_layer = bundle.ai_layer
        if ai_layer is None:
            return []

        self._validate(ai_layer, bundle)

        base_package = bundle.project_metadata["projectMetadata"]["groupId"]
        code_dir = output_dir / "webflux_app"
        jinja_env = self._create_jinja_env()
        output_dirs = self._resolve_output_dirs(code_dir, base_package)

        all_tuples = self._run_sub_generators(
            ai_layer, bundle, base_package, output_dirs, jinja_env, code_dir,
        )

        return self._write_files(all_tuples, code_dir)

    def regenerate(self, bundle: "DefinitionBundle", output_dir: Path) -> list[Path]:
        """Incremental regeneration: regenerate all AI-related files.

        Same logic as full generation — sub-generators are idempotent.
        """
        return self.generate(bundle, output_dir)

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def _validate(self, ai_layer: dict, bundle: "DefinitionBundle") -> None:
        """Run all validation checks. Raises ValueError on failure."""
        from swfaw.generators.ai_validator import AiValidator

        validator = AiValidator()
        # validate() raises ValueError on errors, returns warnings list
        warnings = validator.validate(ai_layer, bundle)
        for w in warnings:
            print(f"  [AI WARN] {w}")

    # ------------------------------------------------------------------
    # Jinja2 environment
    # ------------------------------------------------------------------

    @staticmethod
    def _create_jinja_env() -> jinja2.Environment:
        """Set up Jinja2 environment for swfaw/templates/ directory."""
        templates_dir = Path(__file__).resolve().parent.parent / "templates"
        return jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(templates_dir)),
            keep_trailing_newline=True,
            trim_blocks=True,
            lstrip_blocks=True,
        )

    # ------------------------------------------------------------------
    # Output directory resolution
    # ------------------------------------------------------------------

    @staticmethod
    def _resolve_output_dirs(code_dir: Path, base_package: str) -> dict[str, Path]:
        """Resolve Java package paths to filesystem directories.

        Maps logical directory names (e.g. ``"service"``, ``"controller"``)
        to absolute filesystem paths under the Maven source tree.
        """
        package_path = base_package.replace(".", "/")
        src_root = code_dir / "src" / "main" / "java" / package_path

        ai_dirs = {
            "config": src_root / "ai" / "config",
            "provider": src_root / "ai" / "provider",
            "service": src_root / "ai" / "service",
            "controller": src_root / "ai" / "controller",
            "dto": src_root / "ai" / "dto",
            "entity": src_root / "ai" / "entity",
            "repository": src_root / "ai" / "repository",
            "rag": src_root / "ai" / "rag",
            "evaluator": src_root / "ai" / "evaluator",
            "ingestion": src_root / "ai" / "ingestion",
            "processing": src_root / "ai" / "processing",
            "vectorstore": src_root / "ai" / "vectorstore",
            "orchestrator": src_root / "ai" / "orchestrator",
            "tools": src_root / "ai" / "tools",
            "mcp": src_root / "ai" / "mcp",
            "observability": src_root / "ai" / "observability",
            "budget": src_root / "ai" / "budget",
            "audit": src_root / "ai" / "audit",
            "scheduler": src_root / "ai" / "scheduler",
        }
        return ai_dirs

    # ------------------------------------------------------------------
    # Sub-generator orchestration
    # ------------------------------------------------------------------

    def _run_sub_generators(
        self,
        ai_layer: dict,
        bundle: "DefinitionBundle",
        base_package: str,
        output_dirs: dict[str, Path],
        jinja_env: jinja2.Environment,
        code_dir: Path,
    ) -> list[tuple[str, str]]:
        """Call each sub-generator in dependency order.

        Returns a flat list of ``(filepath, content)`` tuples where
        *filepath* is relative to ``code_dir``.
        """
        from swfaw.generators.ai_provider_generator import ProviderGenerator
        from swfaw.generators.ai_prompt_generator import PromptGenerator
        from swfaw.generators.ai_conversation_generator import ConversationGenerator
        from swfaw.generators.ai_entity_generator import EntityAiGenerator
        from swfaw.generators.ai_standalone_generator import StandaloneAiGenerator
        from swfaw.generators.ai_typed_response_generator import TypedResponseGenerator
        from swfaw.generators.ai_vectorstore_generator import VectorStoreGenerator
        from swfaw.generators.ai_rag_generator import RagGenerator
        from swfaw.generators.ai_evaluator_generator import EvaluatorGenerator
        from swfaw.generators.ai_document_ingestion_generator import DocumentIngestionGenerator
        from swfaw.generators.ai_document_processing_generator import DocumentProcessingGenerator
        from swfaw.generators.ai_orchestrator_generator import OrchestratorGenerator
        from swfaw.generators.ai_tool_generator import ToolFunctionGenerator
        from swfaw.generators.ai_mcp_generator import McpGenerator
        from swfaw.generators.ai_security_generator import SecurityGenerator
        from swfaw.generators.ai_exception_generator import ExceptionGenerator
        from swfaw.generators.ai_observability_generator import ObservabilityGenerator
        from swfaw.generators.ai_token_budget_generator import TokenBudgetGenerator
        from swfaw.generators.ai_audit_generator import AuditGenerator
        from swfaw.generators.ai_session_cleanup_generator import SessionCleanupGenerator
        from swfaw.generators.ai_ddl_generator import AiDdlGenerator
        from swfaw.generators.ai_dto_generator import AiDtoGenerator
        from swfaw.generators.ai_pom_generator import AiPomGenerator
        from swfaw.generators.ai_app_properties_generator import AiAppPropertiesGenerator

        all_tuples: list[tuple[str, str]] = []

        # Extract definition sections
        providers = ai_layer.get("providers", [])
        entity_capabilities = ai_layer.get("entityCapabilities", [])
        standalone_operations = ai_layer.get("standaloneOperations", [])
        assistants = ai_layer.get("assistants", [])
        rag_sources = ai_layer.get("ragSources", [])
        evaluators = ai_layer.get("evaluators", [])
        vector_store = ai_layer.get("vectorStore")
        document_ingestion = ai_layer.get("documentIngestion")
        document_processing = ai_layer.get("documentProcessing")
        orchestrator = ai_layer.get("orchestrator")
        mcp_servers = ai_layer.get("mcpServers", [])
        observability = ai_layer.get("observability")
        token_budget = ai_layer.get("tokenBudget")
        chat_session_cleanup = ai_layer.get("chatSessionCleanup")
        audit_log = ai_layer.get("auditLog")

        # 1. ProviderGenerator
        gen = ProviderGenerator(jinja_env)
        all_tuples.extend(gen.generate(providers, base_package, output_dirs))

        # 2. PromptGenerator
        gen = PromptGenerator(jinja_env)
        all_tuples.extend(gen.generate(base_package, output_dirs))

        # 3. ConversationGenerator
        gen = ConversationGenerator(jinja_env)
        all_tuples.extend(gen.generate(assistants, base_package, output_dirs))

        # 4. EntityAiGenerator
        gen = EntityAiGenerator(jinja_env)
        all_tuples.extend(
            gen.generate(
                entity_capabilities,
                base_package,
                output_dirs,
                bundle_controller_layer=bundle.controller_layer,
            )
        )

        # 5. StandaloneAiGenerator
        gen = StandaloneAiGenerator(jinja_env)
        all_tuples.extend(
            gen.generate(
                standalone_operations,
                base_package,
                output_dirs,
                assistants=assistants,
            )
        )

        # 6. TypedResponseGenerator
        gen = TypedResponseGenerator(jinja_env)
        all_tuples.extend(
            gen.generate(
                entity_capabilities,
                standalone_operations,
                base_package,
                output_dirs,
            )
        )

        # 7. VectorStoreGenerator
        gen = VectorStoreGenerator(jinja_env)
        all_tuples.extend(
            gen.generate(vector_store, rag_sources, base_package, output_dirs)
        )

        # 8. RagGenerator
        gen = RagGenerator(jinja_env)
        all_tuples.extend(
            gen.generate(rag_sources, vector_store, base_package, output_dirs)
        )

        # 9. EvaluatorGenerator
        gen = EvaluatorGenerator(jinja_env)
        all_tuples.extend(gen.generate(evaluators, base_package, output_dirs))

        # 10. DocumentIngestionGenerator
        gen = DocumentIngestionGenerator(jinja_env)
        all_tuples.extend(
            gen.generate(document_ingestion, base_package, output_dirs)
        )

        # 11. DocumentProcessingGenerator
        gen = DocumentProcessingGenerator(jinja_env)
        all_tuples.extend(
            gen.generate(document_processing, base_package, output_dirs)
        )

        # 12. OrchestratorGenerator
        gen = OrchestratorGenerator(jinja_env)
        all_tuples.extend(
            gen.generate(orchestrator, base_package, output_dirs)
        )

        # 13. ToolFunctionGenerator
        gen = ToolFunctionGenerator(jinja_env)
        all_tuples.extend(
            gen.generate(
                orchestrator,
                entity_capabilities,
                standalone_operations,
                document_processing,
                rag_sources,
                document_ingestion,
                base_package,
                output_dirs,
            )
        )

        # 14. McpGenerator
        gen = McpGenerator(jinja_env)
        all_tuples.extend(
            gen.generate(mcp_servers, orchestrator, base_package, output_dirs)
        )

        # 15. SecurityGenerator
        gen = SecurityGenerator(jinja_env)
        all_tuples.extend(
            gen.generate(orchestrator, base_package, output_dirs)
        )

        # 16. ExceptionGenerator
        gen = ExceptionGenerator(jinja_env)
        all_tuples.extend(
            gen.generate(ai_layer, base_package, output_dirs)
        )

        # 17. ObservabilityGenerator
        gen = ObservabilityGenerator(jinja_env)
        all_tuples.extend(
            gen.generate(observability, base_package, output_dirs)
        )

        # 18. TokenBudgetGenerator
        gen = TokenBudgetGenerator(jinja_env)
        all_tuples.extend(
            gen.generate(token_budget, base_package, output_dirs)
        )

        # 19. AuditGenerator
        gen = AuditGenerator(jinja_env)
        all_tuples.extend(gen.generate(audit_log, base_package, output_dirs))

        # 20. SessionCleanupGenerator
        gen = SessionCleanupGenerator(jinja_env)
        all_tuples.extend(
            gen.generate(chat_session_cleanup, base_package, output_dirs)
        )

        # 21. AiDdlGenerator
        gen = AiDdlGenerator(jinja_env)
        ddl_output_path = str(
            code_dir / "src" / "main" / "resources" / "ai_tables.sql"
        )
        all_tuples.extend(gen.generate(ai_layer, output_path=ddl_output_path))

        # 22. AiDtoGenerator
        gen = AiDtoGenerator(jinja_env)
        all_tuples.extend(gen.generate(ai_layer, base_package, output_dirs))

        # 23. AiPomGenerator
        gen = AiPomGenerator(jinja_env)
        pom_output_path = str(code_dir / "ai_dependencies.xml")
        all_tuples.extend(gen.generate(ai_layer, output_path=pom_output_path))

        # 24. AiAppPropertiesGenerator
        gen = AiAppPropertiesGenerator(jinja_env)
        props_output_path = str(
            code_dir / "src" / "main" / "resources" / "ai_application.properties"
        )
        all_tuples.extend(
            gen.generate(ai_layer, output_path=props_output_path)
        )

        return all_tuples

    # ------------------------------------------------------------------
    # File writing
    # ------------------------------------------------------------------

    @staticmethod
    def _write_files(
        tuples: list[tuple[str, str]], code_dir: Path
    ) -> list[Path]:
        """Write all (filepath, content) tuples to disk.

        Each filepath may be absolute or relative to ``code_dir``.
        Returns the list of written absolute Paths.
        """
        written: list[Path] = []
        for filepath_str, content in tuples:
            filepath = Path(filepath_str)
            # If the path is already absolute, use it directly;
            # otherwise treat it as relative to code_dir.
            if not filepath.is_absolute():
                filepath = code_dir / filepath
            filepath.parent.mkdir(parents=True, exist_ok=True)
            filepath.write_text(content, encoding="utf-8")
            written.append(filepath)
        return written
