"""Entity AI sub-generator for the AI Layer.

Generates per-entity AI_Service and AI_Controller classes for entities
listed in ``entityCapabilities``.  Each service conditionally includes
methods based on ``enabledOperations`` (search, generate, summarize,
classify, chat/chatStream) and injects the entity's existing service
plus a ``ChatClient`` bean via ``@Qualifier("<providerName>")``.

Requirements: 5.1–5.9
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import jinja2


class EntityAiGenerator:
    """Generates per-entity AI_Service and AI_Controller classes."""

    def __init__(self, jinja_env: "jinja2.Environment"):
        self.jinja_env = jinja_env

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(
        self,
        entity_capabilities: list[dict],
        base_package: str,
        output_dirs: dict[str, Path],
        bundle_controller_layer: dict | None = None,
    ) -> list[tuple[str, str]]:
        """Generate AI service and controller Java files for each entity.

        Returns a list of ``(filepath, content)`` tuples where *filepath* is
        relative to the project source root.

        Req 5.8: When an entity is NOT in ``entityCapabilities``, no AI code
        is generated for that entity.
        """
        if not entity_capabilities:
            return []

        results: list[tuple[str, str]] = []

        service_dir = output_dirs.get("service", Path("ai/service"))
        controller_dir = output_dirs.get("controller", Path("ai/controller"))

        # Build a lookup from entity name → controller basePath
        base_path_map = self._build_base_path_map(bundle_controller_layer)

        for cap in entity_capabilities:
            entity_name: str = cap.get("entityName", "")
            if not entity_name:
                continue

            # Derive naming variants
            pascal_name = self._to_pascal_case(entity_name)
            camel_name = pascal_name[0].lower() + pascal_name[1:] if pascal_name else ""

            # Resolve the entity's REST base path (e.g. "/api/courses")
            entity_base_path = base_path_map.get(entity_name, f"/api/{entity_name.lower()}s")

            # Build the template context shared by service and controller
            ctx = self._build_template_context(
                cap, base_package, pascal_name, camel_name, entity_base_path,
            )

            # 1. AI_Service (Req 5.1, 5.2–5.6, 5.7)
            content = self._render_service(ctx)
            results.append(
                (str(service_dir / f"{pascal_name}AiService.java"), content)
            )

            # 2. AI_Controller (Req 5.1, 5.2–5.6, 5.9)
            content = self._render_controller(ctx)
            results.append(
                (str(controller_dir / f"{pascal_name}AiController.java"), content)
            )

        return results

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _build_template_context(
        self,
        cap: dict,
        base_package: str,
        pascal_name: str,
        camel_name: str,
        entity_base_path: str,
    ) -> dict:
        """Build the Jinja2 template context for a single entity capability."""
        enabled_ops: list[str] = cap.get("enabledOperations", [])
        provider_name: str = cap.get("providerName", "")
        searchable_fields: list[str] = cap.get("searchableFields", [])
        evaluator_names: list[str] = cap.get("evaluatorNames", [])
        chat_options: dict | None = cap.get("chatOptions")
        role_prompt_sequence: list[dict] | None = cap.get("rolePromptSequence")
        response_type: dict | None = cap.get("responseType")
        rag_source_names: list[str] = cap.get("ragSourceNames", [])

        return {
            "base_package": base_package,
            "entity_name": pascal_name,
            "entity_name_camel": camel_name,
            "provider_name": provider_name,
            "entity_base_path": entity_base_path,
            "enabled_operations": enabled_ops,
            "has_search": "search" in enabled_ops,
            "has_generate": "generate" in enabled_ops,
            "has_summarize": "summarize" in enabled_ops,
            "has_classify": "classify" in enabled_ops,
            "has_chat": "chat" in enabled_ops,
            "has_chat_stream": "chatStream" in enabled_ops,
            "searchable_fields": searchable_fields,
            "evaluator_names": evaluator_names,
            "chat_options": chat_options,
            "role_prompt_sequence": role_prompt_sequence,
            "response_type": response_type,
            "rag_source_names": rag_source_names,
        }

    def _render_service(self, ctx: dict) -> str:
        """Render the entity AI service template.

        Req 5.1: Named ``<EntityName>AiService`` in ``<basePackage>.ai.service``.
        Req 5.2: ``aiSearch`` when search enabled.
        Req 5.3: ``generateContent`` when generate enabled.
        Req 5.4: ``summarize`` when summarize enabled.
        Req 5.5: ``classify`` when classify enabled.
        Req 5.6: ``chat`` / ``chatStream`` when chat enabled.
        Req 5.7: Injects entity service + ``ChatClient`` via ``@Qualifier``.
        """
        template = self.jinja_env.get_template(
            "ai/service/entity_ai_service.java.j2"
        )
        return template.render(**ctx)

    def _render_controller(self, ctx: dict) -> str:
        """Render the entity AI controller template.

        Req 5.1: Named ``<EntityName>AiController`` in ``<basePackage>.ai.controller``
                 with base path ``/api/<entityBasePath>/ai``.
        Req 5.9: JWT authentication and rate limiting.
        """
        template = self.jinja_env.get_template(
            "ai/controller/entity_ai_controller.java.j2"
        )
        return template.render(**ctx)

    @staticmethod
    def _build_base_path_map(controller_layer: dict | None) -> dict[str, str]:
        """Build a mapping from entity name → REST base path.

        Reads the ``controller_layer`` definition (from the DefinitionBundle)
        to resolve each entity's configured ``basePath``.
        """
        if not controller_layer:
            return {}
        controllers = controller_layer.get("controllers", [])
        return {
            ctrl["entityName"]: ctrl.get("basePath", f"/api/{ctrl['entityName'].lower()}s")
            for ctrl in controllers
            if "entityName" in ctrl
        }

    @staticmethod
    def _to_pascal_case(name: str) -> str:
        """Convert an entity name to PascalCase.

        Handles names that are already PascalCase (e.g. ``"Course"``) as well
        as snake_case names (e.g. ``"user_profile"`` → ``"UserProfile"``).
        """
        if "_" in name:
            return "".join(word.capitalize() for word in name.split("_"))
        # Already PascalCase or single word — ensure first letter is upper
        return name[0].upper() + name[1:] if name else ""
