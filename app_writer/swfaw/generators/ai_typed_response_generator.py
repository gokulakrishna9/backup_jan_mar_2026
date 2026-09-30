"""Typed Response sub-generator for the AI Layer.

Generates ``TypedResponseResult<T>`` generic wrapper, ``TypedResponseDeserializer``
utility with fallback logic, and per-responseType ``ParameterizedTypeReference<T>``
constants.  These are shared utilities used by both entity AI services and
standalone AI services when ``responseType`` is configured.

Requirements: 7.1–7.18
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import jinja2

# Wrapper type → Java generic wrapper mapping
_WRAPPER_MAP: dict[str, str] = {
    "list": "List",
    "map": "Map<String, Object>",
    "none": "",
}


class TypedResponseGenerator:
    """Generates typed response handling utilities for AI services."""

    def __init__(self, jinja_env: "jinja2.Environment"):
        self.jinja_env = jinja_env

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(
        self,
        entity_capabilities: list[dict],
        standalone_operations: list[dict],
        base_package: str,
        output_dirs: dict[str, Path],
    ) -> list[tuple[str, str]]:
        """Generate typed response Java files.

        Returns a list of ``(filepath, content)`` tuples where *filepath* is
        relative to the project source root.

        Req 7.14: Generates TypedResponseDeserializationException,
                  TypedResponseResult<T>, and all ParameterizedTypeReference<T>
                  constants as part of standard generation.
        Req 7.17: When no responseType is configured anywhere, no typed
                  response files are generated.
        """
        # Collect all unique responseType configs
        response_types = self._collect_response_types(
            entity_capabilities, standalone_operations,
        )

        if not response_types:
            return []

        results: list[tuple[str, str]] = []

        dto_dir = output_dirs.get("dto", Path("ai/dto"))
        service_dir = output_dirs.get("service", Path("ai/service"))
        provider_dir = output_dirs.get("provider", Path("ai/provider"))

        # 1. TypedResponseResult<T> DTO (Req 7.9, 7.10, 7.14)
        content = self._render_typed_response_result(base_package)
        results.append(
            (str(dto_dir / "TypedResponseResult.java"), content)
        )

        # 2. TypedResponseDeserializer utility (Req 7.8, 7.9, 7.10, 7.11, 7.12, 7.13)
        content = self._render_typed_response_deserializer(
            base_package, response_types,
        )
        results.append(
            (str(service_dir / "TypedResponseDeserializer.java"), content)
        )

        # 3. TypedResponseDeserializationException (Req 7.8, 7.14)
        content = self._render_deserialization_exception(base_package)
        results.append(
            (str(provider_dir / "TypedResponseDeserializationException.java"), content)
        )

        # 4. ParameterizedTypeReference constants class (Req 7.3, 7.4, 7.5, 7.6)
        content = self._render_type_reference_constants(
            base_package, response_types,
        )
        results.append(
            (str(service_dir / "AiTypeReferences.java"), content)
        )

        return results

    # ------------------------------------------------------------------
    # Collection helpers
    # ------------------------------------------------------------------

    def _collect_response_types(
        self,
        entity_capabilities: list[dict],
        standalone_operations: list[dict],
    ) -> list[dict]:
        """Collect all unique responseType configurations.

        Each returned dict has: ``className``, ``wrapper``, ``fallbackBehavior``,
        and ``source`` (for traceability).

        Req 7.1: entityCapabilities responseType with className (defaults to
                 entity DTO), wrapper, fallbackBehavior.
        Req 7.2: standaloneOperations responseType with required className.
        """
        seen: set[str] = set()
        result: list[dict] = []

        for cap in (entity_capabilities or []):
            rt = cap.get("responseType")
            if not rt:
                continue
            entity_name = cap.get("entityName", "")
            class_name = rt.get("className") or f"{self._to_pascal_case(entity_name)}OutputDTO"
            wrapper = rt.get("wrapper", "none")
            fallback = rt.get("fallbackBehavior", "throw")
            key = f"{class_name}:{wrapper}"
            if key not in seen:
                seen.add(key)
                result.append({
                    "className": class_name,
                    "wrapper": wrapper,
                    "fallbackBehavior": fallback,
                    "source": f"entity:{entity_name}",
                })

        for op in (standalone_operations or []):
            rt = op.get("responseType")
            if not rt:
                continue
            op_name = op.get("name", "")
            class_name = rt.get("className", "")
            if not class_name:
                continue  # className is required for standalone (Req 7.2)
            wrapper = rt.get("wrapper", "none")
            fallback = rt.get("fallbackBehavior", "throw")
            key = f"{class_name}:{wrapper}"
            if key not in seen:
                seen.add(key)
                result.append({
                    "className": class_name,
                    "wrapper": wrapper,
                    "fallbackBehavior": fallback,
                    "source": f"standalone:{op_name}",
                })

        return result

    # ------------------------------------------------------------------
    # Rendering helpers
    # ------------------------------------------------------------------

    def _render_typed_response_result(self, base_package: str) -> str:
        """Render the TypedResponseResult<T> DTO template.

        Req 7.9:  success=false, rawResponse when fallback is raw_string.
        Req 7.10: default-constructed instance when fallback is default_object.
        Req 7.14: Generated as part of standard generation.
        """
        template = self.jinja_env.get_template(
            "ai/dto/typed_response_result.java.j2"
        )
        return template.render(base_package=base_package)

    def _render_typed_response_deserializer(
        self, base_package: str, response_types: list[dict],
    ) -> str:
        """Render the TypedResponseDeserializer utility template.

        Req 7.8:  throw fallback → Mono.error with TypedResponseDeserializationException.
        Req 7.9:  raw_string fallback → TypedResponseResult with raw response.
        Req 7.10: default_object fallback → TypedResponseResult with default instance.
        Req 7.11: Retry on deserialization failure with correction prompt.
        Req 7.12: Validate response starts with { or [ before deserializing.
        Req 7.13: Ignore unknown properties, Jackson defaults for missing fields.
        """
        template = self.jinja_env.get_template(
            "ai/service/typed_response_deserializer.java.j2"
        )
        return template.render(
            base_package=base_package,
            response_types=response_types,
        )

    def _render_deserialization_exception(self, base_package: str) -> str:
        """Render the TypedResponseDeserializationException class.

        Req 7.8:  Used when fallbackBehavior is "throw".
        Req 7.14: Generated as part of standard generation.
        """
        template = self.jinja_env.get_template(
            "ai/provider/typed_response_deserialization_exception.java.j2"
        )
        return template.render(base_package=base_package)

    def _render_type_reference_constants(
        self, base_package: str, response_types: list[dict],
    ) -> str:
        """Render the ParameterizedTypeReference constants class.

        Req 7.3: Generate a ParameterizedTypeReference<T> constant per responseType.
        Req 7.4: Used by search operations with List<EntityDTO>.
        Req 7.5: Used by classify operations with ClassificationResultDTO.
        Req 7.6: Used by standalone query operations.
        """
        # Build constant entries with Java generic type strings
        constants = []
        for rt in response_types:
            class_name = rt["className"]
            wrapper = rt.get("wrapper", "none")
            java_type = self._build_java_type(class_name, wrapper)
            constant_name = self._build_constant_name(class_name, wrapper)
            constants.append({
                "constant_name": constant_name,
                "java_type": java_type,
                "class_name": class_name,
                "wrapper": wrapper,
            })

        template = self.jinja_env.get_template(
            "ai/service/ai_type_references.java.j2"
        )
        return template.render(
            base_package=base_package,
            constants=constants,
        )

    # ------------------------------------------------------------------
    # Static helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _build_java_type(class_name: str, wrapper: str) -> str:
        """Build the full Java generic type string.

        Examples:
            ("CourseOutputDTO", "none")  → "CourseOutputDTO"
            ("CourseOutputDTO", "list")  → "List<CourseOutputDTO>"
            ("CourseOutputDTO", "map")   → "Map<String, CourseOutputDTO>"
        """
        if wrapper == "list":
            return f"List<{class_name}>"
        if wrapper == "map":
            return f"Map<String, {class_name}>"
        return class_name

    @staticmethod
    def _build_constant_name(class_name: str, wrapper: str) -> str:
        """Build the constant name for a ParameterizedTypeReference.

        Examples:
            ("CourseOutputDTO", "none") → "COURSE_OUTPUT_DTO_TYPE"
            ("CourseOutputDTO", "list") → "COURSE_OUTPUT_DTO_LIST_TYPE"
            ("CourseOutputDTO", "map")  → "COURSE_OUTPUT_DTO_MAP_TYPE"
        """
        # Convert PascalCase/camelCase to UPPER_SNAKE_CASE
        snake = ""
        for i, ch in enumerate(class_name):
            if ch.isupper() and i > 0:
                snake += "_"
            snake += ch.upper()

        suffix = ""
        if wrapper == "list":
            suffix = "_LIST"
        elif wrapper == "map":
            suffix = "_MAP"

        return f"{snake}{suffix}_TYPE"

    @staticmethod
    def _to_pascal_case(name: str) -> str:
        """Convert an entity name to PascalCase."""
        if "_" in name:
            return "".join(word.capitalize() for word in name.split("_"))
        return name[0].upper() + name[1:] if name else ""
