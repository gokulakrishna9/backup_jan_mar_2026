"""AI React Generator — produces React components from react_ai_config.json.

Reads the React_AI_Config definition and generates React components for
AI chat, smart search, content generation, suggestion widgets, standalone
AI feature pages, RAG admin, evaluation display, and document management.

Uses Python string.Template ($variable substitution) for component templates
to avoid conflicts between Jinja2 {{ }} delimiters and JavaScript object
literals.  AI_NAV_ENTRIES uses Jinja2 for its loop construct.
"""

import json
import os
from pathlib import Path
from string import Template as StringTemplate
from typing import List

from jinja2 import Template as Jinja2Template

# Resolve templates relative to this file so imports work regardless of cwd.
import sys as _sys

_REAW_ROOT = str(Path(__file__).resolve().parent.parent)
if _REAW_ROOT not in _sys.path:
    _sys.path.insert(0, _REAW_ROOT)

from templates.ai_templates import (
    AI_CHAT_PANEL,
    SMART_SEARCH_BAR,
    CONTENT_GENERATION_BUTTON,
    AI_SUGGESTION_WIDGET,
    STANDALONE_CHAT_PAGE,
    STANDALONE_GENERATOR_PAGE,
    STANDALONE_DASHBOARD_PAGE,
    RAG_ADMIN_PAGE,
    EVALUATION_SCORE_BADGE,
    EVALUATION_DASHBOARD_PAGE,
    DOCUMENT_UPLOAD_PANEL,
    DOCUMENT_LIST_PANEL,
    DOCUMENT_INGESTION_PAGE,
    DOCUMENT_TASK_PANEL,
    DOCUMENT_TASK_CHAIN_BUILDER,
    AI_API_SERVICE,
    AI_NAV_ENTRIES,
)


def _write(path: str, content: str) -> Path:
    """Write content to *path*, creating parent dirs as needed. Returns Path."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return p


class AiReactGenerator:
    """Generates React components from react_ai_config.json."""

    def generate(
        self,
        react_ai_config: dict,
        ai_layer: dict,
        react_definitions: dict,
        output_dir: Path,
    ) -> List[Path]:
        """Full generation of all AI React components.

        Args:
            react_ai_config: Parsed react_ai_config.json dict.
            ai_layer: Parsed webflux_ai_layer.json dict (for cross-ref validation).
            react_definitions: React component mappings dict with entity names
                as keys (from the parsed React definition).
            output_dir: Root output directory for generated files.

        Returns:
            List of Paths for all generated files.

        Raises:
            ValueError: If validation fails (missing cross-references).
        """
        self._validate(react_ai_config, ai_layer, react_definitions)

        output = Path(output_dir)
        generated: List[Path] = []

        # Chat panel
        chat_panel = react_ai_config.get("chatPanel", {})
        if chat_panel.get("enabled", False):
            generated.extend(self._generate_chat_panel(react_ai_config, output))

        # Entity features (smart search, content generation, suggestions)
        entity_features = react_ai_config.get("entityFeatures", [])
        if entity_features:
            generated.extend(self._generate_entity_features(entity_features, output))

        # Standalone feature pages
        standalone_features = react_ai_config.get("standaloneFeatures", [])
        if standalone_features:
            generated.extend(
                self._generate_standalone_pages(standalone_features, output)
            )

        # RAG admin page
        rag_features = react_ai_config.get("ragFeatures") or {}
        if rag_features.get("enabled", False):
            generated.extend(self._generate_rag_admin(react_ai_config, output))

        # Evaluation display
        eval_display = react_ai_config.get("evaluationDisplay") or {}
        if eval_display.get("enabled", False):
            generated.extend(
                self._generate_evaluation_display(react_ai_config, output)
            )

        # Document UI (requires AI_Layer documentIngestion to be enabled)
        doc_ingestion = ai_layer.get("documentIngestion") or {}
        if doc_ingestion.get("enabled", False):
            generated.extend(self._generate_document_ui(react_ai_config, output))

        # Centralized AI API service
        generated.extend(self._generate_ai_api_service(react_ai_config, output))

        # Navigation entries for AI sections
        generated.extend(self._generate_nav_entries(react_ai_config, output))

        return generated

    def _validate(
        self, config: dict, ai_layer: dict, react_defs: dict
    ) -> None:
        """Validate cross-references between React AI config and other definitions.

        Checks:
        - entityFeatures entity names exist in React component mappings
        - standaloneFeatures operation names exist in AI_Layer standaloneOperations

        Args:
            config: Parsed react_ai_config.json dict.
            ai_layer: Parsed webflux_ai_layer.json dict.
            react_defs: React component mappings dict — keys are entity names.

        Raises:
            ValueError: For missing cross-references.
        """
        # Validate entityFeatures entity names against React component mappings
        react_entity_names = set(react_defs.keys())
        for feature in config.get("entityFeatures", []):
            entity_name = feature.get("entityName", "")
            if entity_name not in react_entity_names:
                raise ValueError(
                    f"entityFeatures references entity '{entity_name}' "
                    f"which does not exist in React component mappings. "
                    f"Available entities: {sorted(react_entity_names)}"
                )

        # Validate standaloneFeatures operation names against AI_Layer
        standalone_ops = ai_layer.get("standaloneOperations", [])
        ai_layer_op_names = {op.get("name", "") for op in standalone_ops}
        for feature in config.get("standaloneFeatures", []):
            op_name = feature.get("operationName", "")
            if op_name not in ai_layer_op_names:
                raise ValueError(
                    f"standaloneFeatures references operation '{op_name}' "
                    f"which does not exist in AI_Layer standaloneOperations. "
                    f"Available operations: {sorted(ai_layer_op_names)}"
                )

    # ── Generation methods ──────────────────────────────────────────────

    def _generate_chat_panel(
        self, config: dict, output_dir: Path
    ) -> List[Path]:
        """Generate AiChatPanel component with position variants and streaming."""
        chat_cfg = config.get("chatPanel", {})
        theme = config.get("theme", {})

        content = StringTemplate(AI_CHAT_PANEL).safe_substitute(
            position=chat_cfg.get("position", "sidebar"),
            accentColor=theme.get("accentColor", "#6366f1"),
            bubbleStyle=theme.get("chatBubbleStyle", "rounded"),
            loadingAnimation=theme.get("loadingAnimation", "dots"),
            streamingEnabled="true" if chat_cfg.get("streamingEnabled", True) else "false",
            defaultAssistant=chat_cfg.get("defaultAssistant", ""),
        )

        dest = output_dir / "src" / "components" / "ai" / "AiChatPanel.jsx"
        return [_write(str(dest), content)]

    def _generate_entity_features(
        self, features: list, output_dir: Path
    ) -> List[Path]:
        """Generate SmartSearchBar, ContentGenerationButton, AiSuggestionWidget per entity."""
        generated: List[Path] = []
        ai_dir = output_dir / "src" / "components" / "ai"

        for feat in features:
            entity = feat.get("entityName", "")
            entity_lower = entity[0].lower() + entity[1:] if entity else ""

            # SmartSearchBar
            if feat.get("smartSearch", False):
                comp_name = f"{entity}SmartSearchBar"
                searchable = json.dumps(feat.get("searchableFields", []))
                content = StringTemplate(SMART_SEARCH_BAR).safe_substitute(
                    componentName=comp_name,
                    entityName=entity,
                    entityNameLower=entity_lower,
                    searchableFields=searchable,
                )
                generated.append(_write(str(ai_dir / f"{comp_name}.jsx"), content))

            # ContentGenerationButton (one per field)
            for cg in feat.get("contentGeneration", []):
                field = cg.get("fieldName", "")
                label = cg.get("buttonLabel", f"Generate {field}")
                comp_name = f"{entity}{_pascal(field)}GenerationButton"
                content = StringTemplate(CONTENT_GENERATION_BUTTON).safe_substitute(
                    componentName=comp_name,
                    entityName=entity,
                    entityNameLower=entity_lower,
                    fieldName=field,
                    buttonLabel=label,
                )
                generated.append(_write(str(ai_dir / f"{comp_name}.jsx"), content))

            # AiSuggestionWidget (one per field)
            for sg in feat.get("suggestions", []):
                field = sg.get("fieldName", "")
                trigger = sg.get("triggerOn", "change")
                comp_name = f"{entity}{_pascal(field)}SuggestionWidget"
                content = StringTemplate(AI_SUGGESTION_WIDGET).safe_substitute(
                    componentName=comp_name,
                    entityName=entity,
                    entityNameLower=entity_lower,
                    fieldName=field,
                    triggerOn=trigger,
                )
                generated.append(_write(str(ai_dir / f"{comp_name}.jsx"), content))

        return generated

    def _generate_standalone_pages(
        self, features: list, output_dir: Path
    ) -> List[Path]:
        """Generate standalone AI feature pages (chat/generator/dashboard)."""
        generated: List[Path] = []
        pages_dir = output_dir / "src" / "pages" / "ai"

        template_map = {
            "chat": STANDALONE_CHAT_PAGE,
            "generator": STANDALONE_GENERATOR_PAGE,
            "dashboard": STANDALONE_DASHBOARD_PAGE,
        }

        for feat in features:
            op_name = feat.get("operationName", "")
            comp_type = feat.get("componentType", "chat")
            page_title = feat.get("pageTitle", op_name)
            comp_name = f"{_pascal(op_name)}Page"

            tmpl = template_map.get(comp_type, STANDALONE_CHAT_PAGE)
            content = StringTemplate(tmpl).safe_substitute(
                componentName=comp_name,
                operationName=op_name,
                pageTitle=page_title,
            )
            generated.append(_write(str(pages_dir / f"{comp_name}.jsx"), content))

        return generated

    def _generate_rag_admin(
        self, config: dict, output_dir: Path
    ) -> List[Path]:
        """Generate RagAdminPage with source listing, reindex buttons, status badges."""
        dest = output_dir / "src" / "pages" / "ai" / "RagAdminPage.jsx"
        return [_write(str(dest), RAG_ADMIN_PAGE)]

    def _generate_evaluation_display(
        self, config: dict, output_dir: Path
    ) -> List[Path]:
        """Generate EvaluationScoreBadge and EvaluationDashboardPage."""
        generated: List[Path] = []
        eval_cfg = config.get("evaluationDisplay") or {}
        thresholds = eval_cfg.get("scoreColorThresholds", {})

        # EvaluationScoreBadge
        content = StringTemplate(EVALUATION_SCORE_BADGE).safe_substitute(
            badgeStyle=eval_cfg.get("badgeStyle", "inline"),
            passThreshold=thresholds.get("pass", 0.8),
            warnThreshold=thresholds.get("warn", 0.5),
        )
        dest = output_dir / "src" / "components" / "ai" / "EvaluationScoreBadge.jsx"
        generated.append(_write(str(dest), content))

        # EvaluationDashboardPage
        dest = output_dir / "src" / "pages" / "ai" / "EvaluationDashboardPage.jsx"
        generated.append(_write(str(dest), EVALUATION_DASHBOARD_PAGE))

        return generated

    def _generate_document_ui(
        self, config: dict, output_dir: Path
    ) -> List[Path]:
        """Generate DocumentUploadPanel, DocumentListPanel, DocumentIngestionPage,
        DocumentTaskPanel, DocumentTaskChainBuilder."""
        generated: List[Path] = []
        ai_comp = output_dir / "src" / "components" / "ai"
        ai_pages = output_dir / "src" / "pages" / "ai"

        generated.append(_write(str(ai_comp / "DocumentUploadPanel.jsx"), DOCUMENT_UPLOAD_PANEL))
        generated.append(_write(str(ai_comp / "DocumentListPanel.jsx"), DOCUMENT_LIST_PANEL))
        generated.append(_write(str(ai_pages / "DocumentIngestionPage.jsx"), DOCUMENT_INGESTION_PAGE))
        generated.append(_write(str(ai_comp / "DocumentTaskPanel.jsx"), DOCUMENT_TASK_PANEL))
        generated.append(_write(str(ai_comp / "DocumentTaskChainBuilder.jsx"), DOCUMENT_TASK_CHAIN_BUILDER))

        return generated

    def _generate_ai_api_service(
        self, config: dict, output_dir: Path
    ) -> List[Path]:
        """Generate centralized AI API service for AI endpoints."""
        dest = output_dir / "src" / "services" / "aiApiService.js"
        return [_write(str(dest), AI_API_SERVICE)]

    def _generate_nav_entries(
        self, config: dict, output_dir: Path
    ) -> List[Path]:
        """Generate AI section navigation entries."""
        entries = []

        # Chat panel entry
        chat_cfg = config.get("chatPanel", {})
        if chat_cfg.get("enabled", False):
            entries.append({"label": "AI Chat", "icon": "pi pi-comments", "to": "/ai/chat"})

        # Standalone feature entries
        for feat in config.get("standaloneFeatures", []):
            if feat.get("showInNav", True):
                entries.append({
                    "label": feat.get("pageTitle", feat.get("operationName", "")),
                    "icon": "pi pi-bolt",
                    "to": feat.get("pageRoute", f"/ai/{feat.get('operationName', '')}"),
                })

        # RAG admin entry
        rag = config.get("ragFeatures") or {}
        if rag.get("enabled", False):
            entries.append({
                "label": "RAG Admin",
                "icon": "pi pi-database",
                "to": rag.get("adminPageRoute", "/ai/rag-admin"),
            })

        # Evaluation dashboard entry
        eval_cfg = config.get("evaluationDisplay") or {}
        if eval_cfg.get("enabled", False):
            entries.append({"label": "Evaluations", "icon": "pi pi-chart-bar", "to": "/ai/evaluations"})

        # Document ingestion entry (always add if we got this far — caller checks)
        entries.append({"label": "Documents", "icon": "pi pi-file", "to": "/ai/documents"})

        if not entries:
            return []

        content = Jinja2Template(AI_NAV_ENTRIES).render(entries=entries)
        dest = output_dir / "src" / "config" / "aiNavEntries.js"
        return [_write(str(dest), content)]


def _pascal(name: str) -> str:
    """Convert snake_case or plain string to PascalCase."""
    return "".join(part.capitalize() for part in name.replace("-", "_").split("_"))
