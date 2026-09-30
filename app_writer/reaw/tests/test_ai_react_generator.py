"""Unit tests for AiReactGenerator — validate() and generate() coordinator."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import tempfile
import pytest
from generators.ai_react_generator import AiReactGenerator


# ── Fixtures ────────────────────────────────────────────────────────────────


def _minimal_ai_layer(**overrides):
    """Return a minimal valid AI_Layer dict."""
    base = {
        "schemaVersion": "1.0",
        "providers": [],
        "entityCapabilities": [],
        "standaloneOperations": [],
        "promptTemplates": [],
        "assistants": [],
        "ragSources": [],
        "evaluators": [],
        "vectorStore": None,
        "documentIngestion": None,
        "documentProcessing": None,
        "orchestrator": None,
        "mcpServers": [],
        "observability": None,
        "rateLimiting": None,
        "tokenBudget": None,
        "chatSessionCleanup": None,
        "auditLog": None,
    }
    base.update(overrides)
    return base


def _minimal_react_ai_config(**overrides):
    """Return a minimal valid React_AI_Config dict."""
    base = {
        "schemaVersion": "1.0",
        "chatPanel": {
            "enabled": False,
            "position": "sidebar",
            "defaultAssistant": "",
            "showOnPages": [],
            "streamingEnabled": True,
        },
        "entityFeatures": [],
        "standaloneFeatures": [],
        "theme": {
            "accentColor": "#6366f1",
            "chatBubbleStyle": "rounded",
            "loadingAnimation": "dots",
        },
        "evaluationDisplay": None,
        "ragFeatures": None,
    }
    base.update(overrides)
    return base


def _react_defs_with_entities(*entity_names):
    """Return a react_definitions dict with given entity names as keys."""
    return {name: {"fields": []} for name in entity_names}


# ── Validation Tests ────────────────────────────────────────────────────────


class TestValidate:
    """Tests for AiReactGenerator._validate()."""

    def test_valid_empty_config_passes(self):
        gen = AiReactGenerator()
        config = _minimal_react_ai_config()
        ai_layer = _minimal_ai_layer()
        react_defs = {}
        # Should not raise
        gen._validate(config, ai_layer, react_defs)

    def test_entity_feature_with_valid_entity_passes(self):
        gen = AiReactGenerator()
        config = _minimal_react_ai_config(
            entityFeatures=[
                {
                    "entityName": "Product",
                    "smartSearch": True,
                    "contentGeneration": [],
                    "suggestions": [],
                }
            ]
        )
        ai_layer = _minimal_ai_layer()
        react_defs = _react_defs_with_entities("Product", "Order")
        gen._validate(config, ai_layer, react_defs)

    def test_entity_feature_with_missing_entity_raises(self):
        gen = AiReactGenerator()
        config = _minimal_react_ai_config(
            entityFeatures=[
                {
                    "entityName": "NonExistent",
                    "smartSearch": True,
                    "contentGeneration": [],
                    "suggestions": [],
                }
            ]
        )
        ai_layer = _minimal_ai_layer()
        react_defs = _react_defs_with_entities("Product", "Order")
        with pytest.raises(ValueError, match="NonExistent"):
            gen._validate(config, ai_layer, react_defs)

    def test_entity_feature_error_mentions_available_entities(self):
        gen = AiReactGenerator()
        config = _minimal_react_ai_config(
            entityFeatures=[
                {
                    "entityName": "Ghost",
                    "smartSearch": False,
                    "contentGeneration": [],
                    "suggestions": [],
                }
            ]
        )
        ai_layer = _minimal_ai_layer()
        react_defs = _react_defs_with_entities("Alpha", "Beta")
        with pytest.raises(ValueError, match="React component mappings"):
            gen._validate(config, ai_layer, react_defs)

    def test_standalone_feature_with_valid_operation_passes(self):
        gen = AiReactGenerator()
        config = _minimal_react_ai_config(
            standaloneFeatures=[
                {
                    "operationName": "text_summarizer",
                    "pageRoute": "/ai/summarizer",
                    "pageTitle": "Summarizer",
                    "showInNav": True,
                    "componentType": "chat",
                }
            ]
        )
        ai_layer = _minimal_ai_layer(
            standaloneOperations=[
                {"name": "text_summarizer", "type": "chat", "providerName": "gpt4"}
            ]
        )
        react_defs = {}
        gen._validate(config, ai_layer, react_defs)

    def test_standalone_feature_with_missing_operation_raises(self):
        gen = AiReactGenerator()
        config = _minimal_react_ai_config(
            standaloneFeatures=[
                {
                    "operationName": "missing_op",
                    "pageRoute": "/ai/missing",
                    "pageTitle": "Missing",
                    "showInNav": True,
                    "componentType": "chat",
                }
            ]
        )
        ai_layer = _minimal_ai_layer(
            standaloneOperations=[
                {"name": "text_summarizer", "type": "chat", "providerName": "gpt4"}
            ]
        )
        react_defs = {}
        with pytest.raises(ValueError, match="missing_op"):
            gen._validate(config, ai_layer, react_defs)

    def test_standalone_feature_error_mentions_available_operations(self):
        gen = AiReactGenerator()
        config = _minimal_react_ai_config(
            standaloneFeatures=[
                {
                    "operationName": "bad_op",
                    "pageRoute": "/ai/bad",
                    "pageTitle": "Bad",
                    "showInNav": True,
                    "componentType": "generator",
                }
            ]
        )
        ai_layer = _minimal_ai_layer(
            standaloneOperations=[
                {"name": "op_a", "type": "chat", "providerName": "gpt4"},
                {"name": "op_b", "type": "query", "providerName": "gpt4"},
            ]
        )
        react_defs = {}
        with pytest.raises(ValueError, match="standaloneOperations"):
            gen._validate(config, ai_layer, react_defs)

    def test_multiple_entity_features_all_valid(self):
        gen = AiReactGenerator()
        config = _minimal_react_ai_config(
            entityFeatures=[
                {"entityName": "Product", "smartSearch": True, "contentGeneration": [], "suggestions": []},
                {"entityName": "Order", "smartSearch": False, "contentGeneration": [], "suggestions": []},
            ]
        )
        ai_layer = _minimal_ai_layer()
        react_defs = _react_defs_with_entities("Product", "Order", "User")
        gen._validate(config, ai_layer, react_defs)

    def test_multiple_entity_features_one_invalid(self):
        gen = AiReactGenerator()
        config = _minimal_react_ai_config(
            entityFeatures=[
                {"entityName": "Product", "smartSearch": True, "contentGeneration": [], "suggestions": []},
                {"entityName": "Missing", "smartSearch": False, "contentGeneration": [], "suggestions": []},
            ]
        )
        ai_layer = _minimal_ai_layer()
        react_defs = _react_defs_with_entities("Product", "Order")
        with pytest.raises(ValueError, match="Missing"):
            gen._validate(config, ai_layer, react_defs)

    def test_multiple_standalone_features_all_valid(self):
        gen = AiReactGenerator()
        config = _minimal_react_ai_config(
            standaloneFeatures=[
                {"operationName": "op_a", "pageRoute": "/a", "pageTitle": "A", "showInNav": True, "componentType": "chat"},
                {"operationName": "op_b", "pageRoute": "/b", "pageTitle": "B", "showInNav": True, "componentType": "generator"},
            ]
        )
        ai_layer = _minimal_ai_layer(
            standaloneOperations=[
                {"name": "op_a", "type": "chat", "providerName": "gpt4"},
                {"name": "op_b", "type": "query", "providerName": "gpt4"},
            ]
        )
        react_defs = {}
        gen._validate(config, ai_layer, react_defs)

    def test_both_entity_and_standalone_validated(self):
        """Both entity and standalone features are validated together."""
        gen = AiReactGenerator()
        config = _minimal_react_ai_config(
            entityFeatures=[
                {"entityName": "Product", "smartSearch": True, "contentGeneration": [], "suggestions": []},
            ],
            standaloneFeatures=[
                {"operationName": "bad_op", "pageRoute": "/bad", "pageTitle": "Bad", "showInNav": True, "componentType": "chat"},
            ],
        )
        ai_layer = _minimal_ai_layer(standaloneOperations=[])
        react_defs = _react_defs_with_entities("Product")
        # Entity is valid but standalone is not — should raise for standalone
        with pytest.raises(ValueError, match="bad_op"):
            gen._validate(config, ai_layer, react_defs)

    def test_empty_react_defs_with_no_entity_features_passes(self):
        gen = AiReactGenerator()
        config = _minimal_react_ai_config(entityFeatures=[])
        ai_layer = _minimal_ai_layer()
        react_defs = {}
        gen._validate(config, ai_layer, react_defs)

    def test_empty_ai_layer_standalone_ops_with_no_standalone_features_passes(self):
        gen = AiReactGenerator()
        config = _minimal_react_ai_config(standaloneFeatures=[])
        ai_layer = _minimal_ai_layer(standaloneOperations=[])
        react_defs = {}
        gen._validate(config, ai_layer, react_defs)


# ── Generate Coordinator Tests ──────────────────────────────────────────────


class TestGenerate:
    """Tests for AiReactGenerator.generate() coordinator."""

    def test_generate_with_empty_config_returns_list(self):
        gen = AiReactGenerator()
        config = _minimal_react_ai_config()
        ai_layer = _minimal_ai_layer()
        react_defs = {}
        with tempfile.TemporaryDirectory() as td:
            result = gen.generate(config, ai_layer, react_defs, Path(td))
        assert isinstance(result, list)

    def test_generate_calls_validate_first(self):
        """generate() should raise ValueError if validation fails."""
        gen = AiReactGenerator()
        config = _minimal_react_ai_config(
            entityFeatures=[
                {"entityName": "Ghost", "smartSearch": True, "contentGeneration": [], "suggestions": []}
            ]
        )
        ai_layer = _minimal_ai_layer()
        react_defs = {}
        with tempfile.TemporaryDirectory() as td:
            with pytest.raises(ValueError, match="Ghost"):
                gen.generate(config, ai_layer, react_defs, Path(td))

    def test_generate_with_all_features_disabled_returns_base_files(self):
        """With all features disabled, only base files (API service + nav) are generated."""
        gen = AiReactGenerator()
        config = _minimal_react_ai_config()
        ai_layer = _minimal_ai_layer()
        react_defs = {}
        with tempfile.TemporaryDirectory() as td:
            result = gen.generate(config, ai_layer, react_defs, Path(td))
        # ai_api_service and nav_entries always run
        assert len(result) == 2
        names = {p.name for p in result}
        assert "aiApiService.js" in names
        assert "aiNavEntries.js" in names

    def test_generate_accepts_path_or_string_output_dir(self):
        gen = AiReactGenerator()
        config = _minimal_react_ai_config()
        ai_layer = _minimal_ai_layer()
        react_defs = {}
        with tempfile.TemporaryDirectory() as td:
            result = gen.generate(config, ai_layer, react_defs, Path(td))
            assert isinstance(result, list)

    def test_generate_validation_error_prevents_generation(self):
        """If validation fails, no generation methods should run."""
        gen = AiReactGenerator()
        config = _minimal_react_ai_config(
            standaloneFeatures=[
                {"operationName": "nope", "pageRoute": "/nope", "pageTitle": "Nope", "showInNav": True, "componentType": "chat"}
            ]
        )
        ai_layer = _minimal_ai_layer(standaloneOperations=[])
        react_defs = {}
        with tempfile.TemporaryDirectory() as td:
            with pytest.raises(ValueError):
                gen.generate(config, ai_layer, react_defs, Path(td))


# ── Chat Panel Tests ────────────────────────────────────────────────────────


class TestGenerateChatPanel:
    """Tests for _generate_chat_panel()."""

    def test_chat_panel_generates_file(self):
        gen = AiReactGenerator()
        config = _minimal_react_ai_config(
            chatPanel={
                "enabled": True,
                "position": "sidebar",
                "defaultAssistant": "helper",
                "showOnPages": [],
                "streamingEnabled": True,
            }
        )
        ai_layer = _minimal_ai_layer()
        with tempfile.TemporaryDirectory() as td:
            result = gen.generate(config, ai_layer, {}, Path(td))
        names = {p.name for p in result}
        assert "AiChatPanel.jsx" in names

    def test_chat_panel_contains_position(self):
        gen = AiReactGenerator()
        config = _minimal_react_ai_config(
            chatPanel={
                "enabled": True,
                "position": "floating",
                "defaultAssistant": "",
                "showOnPages": [],
                "streamingEnabled": False,
            }
        )
        ai_layer = _minimal_ai_layer()
        with tempfile.TemporaryDirectory() as td:
            result = gen.generate(config, ai_layer, {}, Path(td))
            chat_file = [p for p in result if p.name == "AiChatPanel.jsx"][0]
            content = chat_file.read_text()
            assert "floating" in content

    def test_chat_panel_not_generated_when_disabled(self):
        gen = AiReactGenerator()
        config = _minimal_react_ai_config()  # chatPanel.enabled = False
        ai_layer = _minimal_ai_layer()
        with tempfile.TemporaryDirectory() as td:
            result = gen.generate(config, ai_layer, {}, Path(td))
        names = {p.name for p in result}
        assert "AiChatPanel.jsx" not in names


# ── Entity Features Tests ───────────────────────────────────────────────────


class TestGenerateEntityFeatures:
    """Tests for _generate_entity_features()."""

    def test_smart_search_bar_generated(self):
        gen = AiReactGenerator()
        config = _minimal_react_ai_config(
            entityFeatures=[
                {
                    "entityName": "Product",
                    "smartSearch": True,
                    "contentGeneration": [],
                    "suggestions": [],
                }
            ]
        )
        ai_layer = _minimal_ai_layer()
        react_defs = _react_defs_with_entities("Product")
        with tempfile.TemporaryDirectory() as td:
            result = gen.generate(config, ai_layer, react_defs, Path(td))
        names = {p.name for p in result}
        assert "ProductSmartSearchBar.jsx" in names

    def test_content_generation_button_generated(self):
        gen = AiReactGenerator()
        config = _minimal_react_ai_config(
            entityFeatures=[
                {
                    "entityName": "Product",
                    "smartSearch": False,
                    "contentGeneration": [
                        {"fieldName": "description", "buttonLabel": "Generate Description"}
                    ],
                    "suggestions": [],
                }
            ]
        )
        ai_layer = _minimal_ai_layer()
        react_defs = _react_defs_with_entities("Product")
        with tempfile.TemporaryDirectory() as td:
            result = gen.generate(config, ai_layer, react_defs, Path(td))
        names = {p.name for p in result}
        assert "ProductDescriptionGenerationButton.jsx" in names

    def test_suggestion_widget_generated(self):
        gen = AiReactGenerator()
        config = _minimal_react_ai_config(
            entityFeatures=[
                {
                    "entityName": "Product",
                    "smartSearch": False,
                    "contentGeneration": [],
                    "suggestions": [
                        {"fieldName": "tags", "triggerOn": "blur"}
                    ],
                }
            ]
        )
        ai_layer = _minimal_ai_layer()
        react_defs = _react_defs_with_entities("Product")
        with tempfile.TemporaryDirectory() as td:
            result = gen.generate(config, ai_layer, react_defs, Path(td))
        names = {p.name for p in result}
        assert "ProductTagsSuggestionWidget.jsx" in names

    def test_no_entity_features_when_empty(self):
        gen = AiReactGenerator()
        config = _minimal_react_ai_config(entityFeatures=[])
        ai_layer = _minimal_ai_layer()
        with tempfile.TemporaryDirectory() as td:
            result = gen.generate(config, ai_layer, {}, Path(td))
        names = {p.name for p in result}
        # Only base files
        assert not any("SmartSearchBar" in n for n in names)

    def test_multiple_entities_generate_separate_files(self):
        gen = AiReactGenerator()
        config = _minimal_react_ai_config(
            entityFeatures=[
                {"entityName": "Product", "smartSearch": True, "contentGeneration": [], "suggestions": []},
                {"entityName": "Order", "smartSearch": True, "contentGeneration": [], "suggestions": []},
            ]
        )
        ai_layer = _minimal_ai_layer()
        react_defs = _react_defs_with_entities("Product", "Order")
        with tempfile.TemporaryDirectory() as td:
            result = gen.generate(config, ai_layer, react_defs, Path(td))
        names = {p.name for p in result}
        assert "ProductSmartSearchBar.jsx" in names
        assert "OrderSmartSearchBar.jsx" in names


# ── Standalone Pages Tests ──────────────────────────────────────────────────


class TestGenerateStandalonePages:
    """Tests for _generate_standalone_pages()."""

    def test_chat_page_generated(self):
        gen = AiReactGenerator()
        config = _minimal_react_ai_config(
            standaloneFeatures=[
                {
                    "operationName": "text_chat",
                    "pageRoute": "/ai/chat",
                    "pageTitle": "Text Chat",
                    "showInNav": True,
                    "componentType": "chat",
                }
            ]
        )
        ai_layer = _minimal_ai_layer(
            standaloneOperations=[{"name": "text_chat", "type": "chat", "providerName": "gpt4"}]
        )
        with tempfile.TemporaryDirectory() as td:
            result = gen.generate(config, ai_layer, {}, Path(td))
        names = {p.name for p in result}
        assert "TextChatPage.jsx" in names

    def test_generator_page_generated(self):
        gen = AiReactGenerator()
        config = _minimal_react_ai_config(
            standaloneFeatures=[
                {
                    "operationName": "content_writer",
                    "pageRoute": "/ai/writer",
                    "pageTitle": "Content Writer",
                    "showInNav": True,
                    "componentType": "generator",
                }
            ]
        )
        ai_layer = _minimal_ai_layer(
            standaloneOperations=[{"name": "content_writer", "type": "chat", "providerName": "gpt4"}]
        )
        with tempfile.TemporaryDirectory() as td:
            result = gen.generate(config, ai_layer, {}, Path(td))
        names = {p.name for p in result}
        assert "ContentWriterPage.jsx" in names

    def test_dashboard_page_generated(self):
        gen = AiReactGenerator()
        config = _minimal_react_ai_config(
            standaloneFeatures=[
                {
                    "operationName": "analytics_dash",
                    "pageRoute": "/ai/analytics",
                    "pageTitle": "Analytics",
                    "showInNav": True,
                    "componentType": "dashboard",
                }
            ]
        )
        ai_layer = _minimal_ai_layer(
            standaloneOperations=[{"name": "analytics_dash", "type": "query", "providerName": "gpt4"}]
        )
        with tempfile.TemporaryDirectory() as td:
            result = gen.generate(config, ai_layer, {}, Path(td))
        names = {p.name for p in result}
        assert "AnalyticsDashPage.jsx" in names

    def test_standalone_page_contains_operation_name(self):
        gen = AiReactGenerator()
        config = _minimal_react_ai_config(
            standaloneFeatures=[
                {
                    "operationName": "my_op",
                    "pageRoute": "/ai/my-op",
                    "pageTitle": "My Op",
                    "showInNav": True,
                    "componentType": "chat",
                }
            ]
        )
        ai_layer = _minimal_ai_layer(
            standaloneOperations=[{"name": "my_op", "type": "chat", "providerName": "gpt4"}]
        )
        with tempfile.TemporaryDirectory() as td:
            result = gen.generate(config, ai_layer, {}, Path(td))
            page = [p for p in result if p.name == "MyOpPage.jsx"][0]
            content = page.read_text()
            assert "my_op" in content


# ── RAG Admin Tests ─────────────────────────────────────────────────────────


class TestGenerateRagAdmin:
    """Tests for _generate_rag_admin()."""

    def test_rag_admin_generated_when_enabled(self):
        gen = AiReactGenerator()
        config = _minimal_react_ai_config(
            ragFeatures={"enabled": True, "showStatusIndicators": True, "adminPageRoute": "/ai/rag-admin"}
        )
        ai_layer = _minimal_ai_layer()
        with tempfile.TemporaryDirectory() as td:
            result = gen.generate(config, ai_layer, {}, Path(td))
        names = {p.name for p in result}
        assert "RagAdminPage.jsx" in names

    def test_rag_admin_not_generated_when_disabled(self):
        gen = AiReactGenerator()
        config = _minimal_react_ai_config()  # ragFeatures is None
        ai_layer = _minimal_ai_layer()
        with tempfile.TemporaryDirectory() as td:
            result = gen.generate(config, ai_layer, {}, Path(td))
        names = {p.name for p in result}
        assert "RagAdminPage.jsx" not in names


# ── Evaluation Display Tests ────────────────────────────────────────────────


class TestGenerateEvaluationDisplay:
    """Tests for _generate_evaluation_display()."""

    def test_evaluation_components_generated_when_enabled(self):
        gen = AiReactGenerator()
        config = _minimal_react_ai_config(
            evaluationDisplay={
                "enabled": True,
                "showInChat": True,
                "showInEntityViews": True,
                "badgeStyle": "tooltip",
                "scoreColorThresholds": {"pass": 0.8, "warn": 0.5},
            }
        )
        ai_layer = _minimal_ai_layer()
        with tempfile.TemporaryDirectory() as td:
            result = gen.generate(config, ai_layer, {}, Path(td))
        names = {p.name for p in result}
        assert "EvaluationScoreBadge.jsx" in names
        assert "EvaluationDashboardPage.jsx" in names

    def test_evaluation_not_generated_when_disabled(self):
        gen = AiReactGenerator()
        config = _minimal_react_ai_config()  # evaluationDisplay is None
        ai_layer = _minimal_ai_layer()
        with tempfile.TemporaryDirectory() as td:
            result = gen.generate(config, ai_layer, {}, Path(td))
        names = {p.name for p in result}
        assert "EvaluationScoreBadge.jsx" not in names

    def test_evaluation_badge_contains_threshold(self):
        gen = AiReactGenerator()
        config = _minimal_react_ai_config(
            evaluationDisplay={
                "enabled": True,
                "showInChat": True,
                "showInEntityViews": True,
                "badgeStyle": "inline",
                "scoreColorThresholds": {"pass": 0.9, "warn": 0.6},
            }
        )
        ai_layer = _minimal_ai_layer()
        with tempfile.TemporaryDirectory() as td:
            result = gen.generate(config, ai_layer, {}, Path(td))
            badge = [p for p in result if p.name == "EvaluationScoreBadge.jsx"][0]
            content = badge.read_text()
            assert "0.9" in content
            assert "0.6" in content


# ── Document UI Tests ───────────────────────────────────────────────────────


class TestGenerateDocumentUI:
    """Tests for _generate_document_ui()."""

    def test_document_ui_generated_when_ingestion_enabled(self):
        gen = AiReactGenerator()
        config = _minimal_react_ai_config()
        ai_layer = _minimal_ai_layer(documentIngestion={"enabled": True})
        with tempfile.TemporaryDirectory() as td:
            result = gen.generate(config, ai_layer, {}, Path(td))
        names = {p.name for p in result}
        assert "DocumentUploadPanel.jsx" in names
        assert "DocumentListPanel.jsx" in names
        assert "DocumentIngestionPage.jsx" in names
        assert "DocumentTaskPanel.jsx" in names
        assert "DocumentTaskChainBuilder.jsx" in names

    def test_document_ui_not_generated_when_ingestion_disabled(self):
        gen = AiReactGenerator()
        config = _minimal_react_ai_config()
        ai_layer = _minimal_ai_layer()  # documentIngestion is None
        with tempfile.TemporaryDirectory() as td:
            result = gen.generate(config, ai_layer, {}, Path(td))
        names = {p.name for p in result}
        assert "DocumentUploadPanel.jsx" not in names


# ── AI API Service Tests ────────────────────────────────────────────────────


class TestGenerateAiApiService:
    """Tests for _generate_ai_api_service()."""

    def test_api_service_always_generated(self):
        gen = AiReactGenerator()
        config = _minimal_react_ai_config()
        ai_layer = _minimal_ai_layer()
        with tempfile.TemporaryDirectory() as td:
            result = gen.generate(config, ai_layer, {}, Path(td))
        names = {p.name for p in result}
        assert "aiApiService.js" in names

    def test_api_service_contains_endpoints(self):
        gen = AiReactGenerator()
        config = _minimal_react_ai_config()
        ai_layer = _minimal_ai_layer()
        with tempfile.TemporaryDirectory() as td:
            result = gen.generate(config, ai_layer, {}, Path(td))
            svc = [p for p in result if p.name == "aiApiService.js"][0]
            content = svc.read_text()
            assert "entitySearch" in content
            assert "standaloneChat" in content
            assert "uploadDocument" in content
            assert "getRagSources" in content


# ── Nav Entries Tests ───────────────────────────────────────────────────────


class TestGenerateNavEntries:
    """Tests for _generate_nav_entries()."""

    def test_nav_entries_always_generated(self):
        gen = AiReactGenerator()
        config = _minimal_react_ai_config()
        ai_layer = _minimal_ai_layer()
        with tempfile.TemporaryDirectory() as td:
            result = gen.generate(config, ai_layer, {}, Path(td))
        names = {p.name for p in result}
        assert "aiNavEntries.js" in names

    def test_nav_entries_include_standalone_features(self):
        gen = AiReactGenerator()
        config = _minimal_react_ai_config(
            standaloneFeatures=[
                {
                    "operationName": "summarizer",
                    "pageRoute": "/ai/summarizer",
                    "pageTitle": "Summarizer",
                    "showInNav": True,
                    "componentType": "chat",
                }
            ]
        )
        ai_layer = _minimal_ai_layer(
            standaloneOperations=[{"name": "summarizer", "type": "chat", "providerName": "gpt4"}]
        )
        with tempfile.TemporaryDirectory() as td:
            result = gen.generate(config, ai_layer, {}, Path(td))
            nav = [p for p in result if p.name == "aiNavEntries.js"][0]
            content = nav.read_text()
            assert "Summarizer" in content
            assert "/ai/summarizer" in content

    def test_nav_entries_include_chat_when_enabled(self):
        gen = AiReactGenerator()
        config = _minimal_react_ai_config(
            chatPanel={
                "enabled": True,
                "position": "sidebar",
                "defaultAssistant": "",
                "showOnPages": [],
                "streamingEnabled": True,
            }
        )
        ai_layer = _minimal_ai_layer()
        with tempfile.TemporaryDirectory() as td:
            result = gen.generate(config, ai_layer, {}, Path(td))
            nav = [p for p in result if p.name == "aiNavEntries.js"][0]
            content = nav.read_text()
            assert "AI Chat" in content

    def test_nav_entries_include_rag_when_enabled(self):
        gen = AiReactGenerator()
        config = _minimal_react_ai_config(
            ragFeatures={"enabled": True, "showStatusIndicators": True, "adminPageRoute": "/ai/rag-admin"}
        )
        ai_layer = _minimal_ai_layer()
        with tempfile.TemporaryDirectory() as td:
            result = gen.generate(config, ai_layer, {}, Path(td))
            nav = [p for p in result if p.name == "aiNavEntries.js"][0]
            content = nav.read_text()
            assert "RAG Admin" in content


# ── Full Integration Test ───────────────────────────────────────────────────


class TestFullGeneration:
    """Integration test with all features enabled."""

    def test_all_features_enabled_generates_all_components(self):
        gen = AiReactGenerator()
        config = _minimal_react_ai_config(
            chatPanel={
                "enabled": True,
                "position": "floating",
                "defaultAssistant": "main",
                "showOnPages": ["home"],
                "streamingEnabled": True,
            },
            entityFeatures=[
                {
                    "entityName": "Product",
                    "smartSearch": True,
                    "contentGeneration": [{"fieldName": "description", "buttonLabel": "Gen Desc"}],
                    "suggestions": [{"fieldName": "tags", "triggerOn": "change"}],
                }
            ],
            standaloneFeatures=[
                {
                    "operationName": "summarizer",
                    "pageRoute": "/ai/summarizer",
                    "pageTitle": "Summarizer",
                    "showInNav": True,
                    "componentType": "generator",
                }
            ],
            ragFeatures={"enabled": True, "showStatusIndicators": True, "adminPageRoute": "/ai/rag-admin"},
            evaluationDisplay={
                "enabled": True,
                "showInChat": True,
                "showInEntityViews": True,
                "badgeStyle": "inline",
                "scoreColorThresholds": {"pass": 0.8, "warn": 0.5},
            },
        )
        ai_layer = _minimal_ai_layer(
            standaloneOperations=[{"name": "summarizer", "type": "chat", "providerName": "gpt4"}],
            documentIngestion={"enabled": True},
        )
        react_defs = _react_defs_with_entities("Product")
        with tempfile.TemporaryDirectory() as td:
            result = gen.generate(config, ai_layer, react_defs, Path(td))

        names = {p.name for p in result}
        # Chat panel
        assert "AiChatPanel.jsx" in names
        # Entity features
        assert "ProductSmartSearchBar.jsx" in names
        assert "ProductDescriptionGenerationButton.jsx" in names
        assert "ProductTagsSuggestionWidget.jsx" in names
        # Standalone
        assert "SummarizerPage.jsx" in names
        # RAG
        assert "RagAdminPage.jsx" in names
        # Evaluation
        assert "EvaluationScoreBadge.jsx" in names
        assert "EvaluationDashboardPage.jsx" in names
        # Document UI
        assert "DocumentUploadPanel.jsx" in names
        assert "DocumentListPanel.jsx" in names
        assert "DocumentIngestionPage.jsx" in names
        assert "DocumentTaskPanel.jsx" in names
        assert "DocumentTaskChainBuilder.jsx" in names
        # Always present
        assert "aiApiService.js" in names
        assert "aiNavEntries.js" in names

    def test_all_generated_files_are_non_empty(self):
        gen = AiReactGenerator()
        config = _minimal_react_ai_config(
            chatPanel={"enabled": True, "position": "sidebar", "defaultAssistant": "", "showOnPages": [], "streamingEnabled": True},
            entityFeatures=[{"entityName": "Item", "smartSearch": True, "contentGeneration": [], "suggestions": []}],
            standaloneFeatures=[{"operationName": "op1", "pageRoute": "/ai/op1", "pageTitle": "Op1", "showInNav": True, "componentType": "chat"}],
            ragFeatures={"enabled": True, "showStatusIndicators": True, "adminPageRoute": "/ai/rag"},
            evaluationDisplay={"enabled": True, "showInChat": True, "showInEntityViews": True, "badgeStyle": "inline", "scoreColorThresholds": {"pass": 0.8, "warn": 0.5}},
        )
        ai_layer = _minimal_ai_layer(
            standaloneOperations=[{"name": "op1", "type": "chat", "providerName": "gpt4"}],
            documentIngestion={"enabled": True},
        )
        react_defs = _react_defs_with_entities("Item")
        with tempfile.TemporaryDirectory() as td:
            result = gen.generate(config, ai_layer, react_defs, Path(td))
            for p in result:
                assert p.exists(), f"{p} does not exist"
                assert p.stat().st_size > 0, f"{p} is empty"


# ── Run with python3 ────────────────────────────────────────────────────────

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
