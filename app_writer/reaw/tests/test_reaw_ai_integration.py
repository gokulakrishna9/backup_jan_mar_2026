"""Tests for REAW AI integration — definition loading and pipeline wiring.

Covers:
- ReactDefinitionParser loading react_ai_config.json via concern: "ai_config"
- SchemaVersion validation
- Invalid JSON rejection (ValueError)
- Absent file handling (react_ai_config is None)
- ReactCodeGenerator conditional AI generation invocation
"""

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from parsers.react_definition_parser import ReactDefinitionParser, ReactDefinitionParseError
from models.react_definition_models import ReactAppDefinition


def _write_json(directory: str, filename: str, data) -> str:
    """Write a JSON file and return its path."""
    path = os.path.join(directory, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    return path


def _minimal_manifest(extra_files=None):
    """Return a minimal react_manifest.json dict."""
    files = []
    if extra_files:
        files.extend(extra_files)
    return {"version": "1.0.0", "files": files}


def _minimal_react_ai_config(**overrides):
    """Return a minimal valid react_ai_config.json dict."""
    base = {
        "schemaVersion": "1.0",
        "chatPanel": {"enabled": False, "position": "sidebar",
                       "defaultAssistant": "", "showOnPages": [],
                       "streamingEnabled": True},
        "entityFeatures": [],
        "standaloneFeatures": [],
        "theme": {"accentColor": "#6366f1", "chatBubbleStyle": "rounded",
                  "loadingAnimation": "dots"},
        "evaluationDisplay": None,
        "ragFeatures": None,
    }
    base.update(overrides)
    return base


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


class TestReactAiConfigLoading(unittest.TestCase):
    """Test ReactDefinitionParser loading of react_ai_config.json."""

    def test_loads_valid_react_ai_config(self):
        """When manifest has concern: ai_config, parser loads the dict."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ai_config = _minimal_react_ai_config()
            _write_json(tmpdir, "react_ai_config.json", ai_config)
            manifest = _minimal_manifest([
                {"path": "react_ai_config.json", "concern": "ai_config"},
            ])
            _write_json(tmpdir, "react_manifest.json", manifest)

            result = ReactDefinitionParser.parse(tmpdir)
            self.assertIsNotNone(result.react_ai_config)
            self.assertEqual(result.react_ai_config["schemaVersion"], "1.0")

    def test_absent_ai_config_sets_none(self):
        """When no ai_config concern in manifest, react_ai_config is None."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest = _minimal_manifest()
            _write_json(tmpdir, "react_manifest.json", manifest)

            result = ReactDefinitionParser.parse(tmpdir)
            self.assertIsNone(result.react_ai_config)

    def test_invalid_json_raises_error(self):
        """When react_ai_config.json contains invalid JSON, raise error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Write invalid JSON
            bad_path = os.path.join(tmpdir, "react_ai_config.json")
            with open(bad_path, "w") as f:
                f.write("{not valid json!!!")
            manifest = _minimal_manifest([
                {"path": "react_ai_config.json", "concern": "ai_config"},
            ])
            _write_json(tmpdir, "react_manifest.json", manifest)

            with self.assertRaises(ReactDefinitionParseError) as ctx:
                ReactDefinitionParser.parse(tmpdir)
            self.assertIn("Malformed JSON", str(ctx.exception))

    def test_missing_schema_version_raises_value_error(self):
        """When schemaVersion is missing, raise ValueError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ai_config = _minimal_react_ai_config()
            del ai_config["schemaVersion"]
            _write_json(tmpdir, "react_ai_config.json", ai_config)
            manifest = _minimal_manifest([
                {"path": "react_ai_config.json", "concern": "ai_config"},
            ])
            _write_json(tmpdir, "react_manifest.json", manifest)

            with self.assertRaises(ValueError) as ctx:
                ReactDefinitionParser.parse(tmpdir)
            self.assertIn("schemaVersion", str(ctx.exception))
            self.assertIn("1.0", str(ctx.exception))

    def test_wrong_schema_version_raises_value_error(self):
        """When schemaVersion is not '1.0', raise ValueError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ai_config = _minimal_react_ai_config(schemaVersion="2.0")
            _write_json(tmpdir, "react_ai_config.json", ai_config)
            manifest = _minimal_manifest([
                {"path": "react_ai_config.json", "concern": "ai_config"},
            ])
            _write_json(tmpdir, "react_manifest.json", manifest)

            with self.assertRaises(ValueError) as ctx:
                ReactDefinitionParser.parse(tmpdir)
            self.assertIn("2.0", str(ctx.exception))
            self.assertIn("1.0", str(ctx.exception))

    def test_referenced_file_not_found_raises_error(self):
        """When manifest references ai_config file that doesn't exist, raise error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest = _minimal_manifest([
                {"path": "react_ai_config.json", "concern": "ai_config"},
            ])
            _write_json(tmpdir, "react_manifest.json", manifest)

            with self.assertRaises(ReactDefinitionParseError) as ctx:
                ReactDefinitionParser.parse(tmpdir)
            self.assertIn("not found", str(ctx.exception))

    def test_ai_config_preserves_all_fields(self):
        """Loaded react_ai_config preserves all fields from the JSON."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ai_config = _minimal_react_ai_config(
                chatPanel={"enabled": True, "position": "floating",
                           "defaultAssistant": "helper", "showOnPages": ["/home"],
                           "streamingEnabled": False},
                entityFeatures=[{"entityName": "Product", "smartSearch": True}],
            )
            _write_json(tmpdir, "react_ai_config.json", ai_config)
            manifest = _minimal_manifest([
                {"path": "react_ai_config.json", "concern": "ai_config"},
            ])
            _write_json(tmpdir, "react_manifest.json", manifest)

            result = ReactDefinitionParser.parse(tmpdir)
            self.assertTrue(result.react_ai_config["chatPanel"]["enabled"])
            self.assertEqual(result.react_ai_config["chatPanel"]["position"], "floating")
            self.assertEqual(len(result.react_ai_config["entityFeatures"]), 1)


class TestReactCodeGeneratorAiWiring(unittest.TestCase):
    """Test ReactCodeGenerator conditional AI generation invocation."""

    @patch("generators.phase2.react_code_generator.AiReactGenerator")
    @patch("generators.phase2.react_code_generator.GridLayoutGenerator")
    @patch("generators.phase2.react_code_generator.QueryPageGenerator")
    @patch("generators.phase2.react_code_generator.FilterPageGenerator")
    @patch("generators.phase2.react_code_generator.EntityPageGenerator")
    @patch("generators.phase2.react_code_generator.GroupedFormGenerator")
    @patch("generators.phase2.react_code_generator.QueryComponentGenerator")
    @patch("generators.phase2.react_code_generator.FilterComponentGenerator")
    @patch("generators.phase2.react_code_generator.EntityComponentGenerator")
    @patch("generators.phase2.react_code_generator.WidgetGenerator")
    @patch("generators.phase2.react_code_generator.ChartGenerator")
    @patch("generators.phase2.react_code_generator.PermissionGenerator")
    @patch("generators.phase2.react_code_generator.AuthGenerator")
    @patch("generators.phase2.react_code_generator.ComponentWrapperGenerator")
    @patch("generators.phase2.react_code_generator.ReduxGenerator")
    @patch("generators.phase2.react_code_generator.ApiServiceGenerator")
    @patch("generators.phase2.react_code_generator.ScaffoldGenerator")
    @patch("generators.phase2.react_code_generator.Phase2ThemeGenerator")
    def test_ai_generator_invoked_when_config_present(self, *mocks):
        """When react_ai_config is present and ai_layer provided, AiReactGenerator is invoked."""
        # All phase2 generators return empty lists
        for m in mocks:
            m.generate.return_value = []

        # The last mock in the positional args is AiReactGenerator (first @patch)
        ai_gen_cls = mocks[0]  # Phase2ThemeGenerator is last positional
        # Actually, mocks are passed in reverse order of @patch decorators
        # First @patch = last positional arg
        # Let me re-check: @patch decorators apply bottom-up, args are passed in order
        # So mocks[0] = Phase2ThemeGenerator, mocks[-1] = AiReactGenerator
        ai_gen_mock = MagicMock()
        ai_gen_mock.generate.return_value = [Path("/tmp/test.jsx")]
        mocks[-1].return_value = ai_gen_mock

        react_def = ReactAppDefinition(
            react_ai_config=_minimal_react_ai_config(),
        )
        ai_layer = _minimal_ai_layer()

        from generators.phase2.react_code_generator import ReactCodeGenerator
        with tempfile.TemporaryDirectory() as tmpdir:
            files = ReactCodeGenerator.generate(react_def, tmpdir, ai_layer=ai_layer)

        ai_gen_mock.generate.assert_called_once()
        # Verify the generated file path is in the result
        self.assertTrue(any("test.jsx" in f for f in files))

    @patch("generators.phase2.react_code_generator.AiReactGenerator")
    @patch("generators.phase2.react_code_generator.GridLayoutGenerator")
    @patch("generators.phase2.react_code_generator.QueryPageGenerator")
    @patch("generators.phase2.react_code_generator.FilterPageGenerator")
    @patch("generators.phase2.react_code_generator.EntityPageGenerator")
    @patch("generators.phase2.react_code_generator.GroupedFormGenerator")
    @patch("generators.phase2.react_code_generator.QueryComponentGenerator")
    @patch("generators.phase2.react_code_generator.FilterComponentGenerator")
    @patch("generators.phase2.react_code_generator.EntityComponentGenerator")
    @patch("generators.phase2.react_code_generator.WidgetGenerator")
    @patch("generators.phase2.react_code_generator.ChartGenerator")
    @patch("generators.phase2.react_code_generator.PermissionGenerator")
    @patch("generators.phase2.react_code_generator.AuthGenerator")
    @patch("generators.phase2.react_code_generator.ComponentWrapperGenerator")
    @patch("generators.phase2.react_code_generator.ReduxGenerator")
    @patch("generators.phase2.react_code_generator.ApiServiceGenerator")
    @patch("generators.phase2.react_code_generator.ScaffoldGenerator")
    @patch("generators.phase2.react_code_generator.Phase2ThemeGenerator")
    def test_ai_generator_skipped_when_config_absent(self, *mocks):
        """When react_ai_config is None, AiReactGenerator is NOT invoked."""
        for m in mocks:
            m.generate.return_value = []

        ai_gen_cls = mocks[-1]  # AiReactGenerator mock

        react_def = ReactAppDefinition(react_ai_config=None)

        from generators.phase2.react_code_generator import ReactCodeGenerator
        with tempfile.TemporaryDirectory() as tmpdir:
            ReactCodeGenerator.generate(react_def, tmpdir, ai_layer=_minimal_ai_layer())

        ai_gen_cls.assert_not_called()
        ai_gen_cls.return_value.generate.assert_not_called()

    @patch("generators.phase2.react_code_generator.AiReactGenerator")
    @patch("generators.phase2.react_code_generator.GridLayoutGenerator")
    @patch("generators.phase2.react_code_generator.QueryPageGenerator")
    @patch("generators.phase2.react_code_generator.FilterPageGenerator")
    @patch("generators.phase2.react_code_generator.EntityPageGenerator")
    @patch("generators.phase2.react_code_generator.GroupedFormGenerator")
    @patch("generators.phase2.react_code_generator.QueryComponentGenerator")
    @patch("generators.phase2.react_code_generator.FilterComponentGenerator")
    @patch("generators.phase2.react_code_generator.EntityComponentGenerator")
    @patch("generators.phase2.react_code_generator.WidgetGenerator")
    @patch("generators.phase2.react_code_generator.ChartGenerator")
    @patch("generators.phase2.react_code_generator.PermissionGenerator")
    @patch("generators.phase2.react_code_generator.AuthGenerator")
    @patch("generators.phase2.react_code_generator.ComponentWrapperGenerator")
    @patch("generators.phase2.react_code_generator.ReduxGenerator")
    @patch("generators.phase2.react_code_generator.ApiServiceGenerator")
    @patch("generators.phase2.react_code_generator.ScaffoldGenerator")
    @patch("generators.phase2.react_code_generator.Phase2ThemeGenerator")
    def test_ai_generator_skipped_when_ai_layer_absent(self, *mocks):
        """When ai_layer is None, AiReactGenerator is NOT invoked even if config present."""
        for m in mocks:
            m.generate.return_value = []

        ai_gen_cls = mocks[-1]

        react_def = ReactAppDefinition(
            react_ai_config=_minimal_react_ai_config(),
        )

        from generators.phase2.react_code_generator import ReactCodeGenerator
        with tempfile.TemporaryDirectory() as tmpdir:
            ReactCodeGenerator.generate(react_def, tmpdir, ai_layer=None)

        ai_gen_cls.assert_not_called()
        ai_gen_cls.return_value.generate.assert_not_called()


if __name__ == "__main__":
    unittest.main()
