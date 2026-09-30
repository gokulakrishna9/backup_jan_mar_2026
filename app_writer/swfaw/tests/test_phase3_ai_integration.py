"""Integration tests for AI layer integration in the Phase 3 pipeline.

Tests that phase3_definition_first.py correctly invokes (or skips) AI generation
in both full and incremental modes based on bundle.ai_layer presence and dirty files.
"""

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app_def_manager.scaffolder import Scaffolder
from app_def_manager.status_tracker import StatusTracker
from utils.definition_loader import load_all_definitions

# Import the pipeline functions under test
from phase3_definition_first import _full_generation, _incremental_generation


TEST_ENTITIES = [
    {"name": "Task", "fields": [{"name": "title", "type": "String"}]},
]

MINIMAL_AI_LAYER = {
    "schemaVersion": "1.0",
    "providers": [
        {
            "name": "test-provider",
            "type": "openai",
            "model": "gpt-4",
            "apiKeyEnvVar": "OPENAI_API_KEY",
        }
    ],
    "entityCapabilities": [],
    "standaloneOperations": [],
    "promptTemplates": [],
    "assistants": [],
    "ragSources": [],
    "evaluators": [],
    "mcpServers": [],
}


@pytest.fixture()
def work_dir():
    """Create a temp directory, chdir into it, and restore cwd on teardown."""
    original_cwd = os.getcwd()
    tmp = tempfile.mkdtemp()
    os.chdir(tmp)
    yield Path(tmp)
    os.chdir(original_cwd)


def _scaffold_app(work_dir, with_ai_layer=False):
    """Scaffold a test app and optionally add an AI layer definition."""
    scaffolder = Scaffolder()
    app_dir = scaffolder.scaffold_application("test_app", TEST_ENTITIES)

    if with_ai_layer:
        ai_path = app_dir / "webflux_ai_layer.json"
        ai_path.write_text(json.dumps(MINIMAL_AI_LAYER), encoding="utf-8")

        # Update manifest to include ai_layer
        manifest_path = app_dir / "webflux_manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["files"]["ai_layer"] = "webflux_ai_layer.json"
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    return app_dir


def _make_args(skip_sql=True, skip_java=False, sql_file="schema.sql"):
    """Build a minimal argparse.Namespace for pipeline functions."""
    return argparse.Namespace(
        app="test_app",
        output="generated_application/test_app",
        full=False,
        skip_sql=skip_sql,
        skip_java=skip_java,
        sql_file=sql_file,
    )


class TestAiLayerFullGeneration:
    """Full generation: AI generator invoked when ai_layer is present, skipped when None."""

    def test_full_gen_skips_ai_when_ai_layer_is_none(self, work_dir):
        """When ai_layer is None, AI generation block is not entered."""
        app_dir = _scaffold_app(work_dir, with_ai_layer=False)
        bundle = load_all_definitions(app_dir)
        assert bundle.ai_layer is None

        output_dir = Path("generated_application") / "test_app"
        output_dir.mkdir(parents=True, exist_ok=True)
        tracker = StatusTracker(app_dir)
        args = _make_args(skip_sql=True, skip_java=False)

        # Patch generate_application to avoid full Java gen overhead
        with patch("phase3_definition_first.generate_application"), \
             patch("phase3_definition_first.reconstruct_database_definition", return_value={}):
            regenerated = _full_generation(bundle, output_dir, tracker, args)

        # No AI files should appear — ai_layer is None so the block is never entered
        regen_strs = [str(p) for p in regenerated]
        assert not any("ai" in s.lower() for s in regen_strs if "ai" in s.lower()), \
            "No AI-related files should be generated when ai_layer is None"

    def test_full_gen_invokes_ai_generator_when_ai_layer_present(self, work_dir):
        """When ai_layer is not None, AiGenerator.generate() is called."""
        app_dir = _scaffold_app(work_dir, with_ai_layer=True)
        bundle = load_all_definitions(app_dir)
        assert bundle.ai_layer is not None

        output_dir = Path("generated_application") / "test_app"
        output_dir.mkdir(parents=True, exist_ok=True)
        tracker = StatusTracker(app_dir)
        args = _make_args(skip_sql=True, skip_java=False)

        # Create a mock AiGenerator
        mock_ai_gen_instance = MagicMock()
        mock_ai_gen_instance.generate.return_value = [Path("ai_service.java")]
        mock_ai_gen_class = MagicMock(return_value=mock_ai_gen_instance)

        # Patch the import inside _full_generation
        import types
        fake_module = types.ModuleType("generators.ai_generator")
        fake_module.AiGenerator = mock_ai_gen_class

        with patch("phase3_definition_first.generate_application"), \
             patch("phase3_definition_first.reconstruct_database_definition", return_value={}), \
             patch.dict("sys.modules", {"generators.ai_generator": fake_module}):
            regenerated = _full_generation(bundle, output_dir, tracker, args)

        mock_ai_gen_instance.generate.assert_called_once_with(bundle, output_dir)
        assert Path("ai_service.java") in regenerated

    def test_full_gen_handles_import_error_gracefully(self, work_dir):
        """When AiGenerator module doesn't exist, pipeline continues without error."""
        app_dir = _scaffold_app(work_dir, with_ai_layer=True)
        bundle = load_all_definitions(app_dir)
        assert bundle.ai_layer is not None

        output_dir = Path("generated_application") / "test_app"
        output_dir.mkdir(parents=True, exist_ok=True)
        tracker = StatusTracker(app_dir)
        args = _make_args(skip_sql=True, skip_java=False)

        # Ensure generators.ai_generator is NOT importable
        with patch("phase3_definition_first.generate_application"), \
             patch("phase3_definition_first.reconstruct_database_definition", return_value={}), \
             patch.dict("sys.modules", {"generators.ai_generator": None}):
            # Should not raise — ImportError is caught
            regenerated = _full_generation(bundle, output_dir, tracker, args)

        # Pipeline completes, just no AI files
        assert isinstance(regenerated, list)

    def test_full_gen_skips_ai_when_skip_java(self, work_dir):
        """When --skip-java is set, AI generation is skipped entirely."""
        app_dir = _scaffold_app(work_dir, with_ai_layer=True)
        bundle = load_all_definitions(app_dir)
        output_dir = Path("generated_application") / "test_app"
        output_dir.mkdir(parents=True, exist_ok=True)
        tracker = StatusTracker(app_dir)
        args = _make_args(skip_sql=True, skip_java=True)

        regenerated = _full_generation(bundle, output_dir, tracker, args)
        # With skip_java=True, no Java code is generated at all
        assert not any("ai" in str(p).lower() for p in regenerated)


class TestAiLayerIncrementalGeneration:
    """Incremental generation: AI regeneration when webflux_ai_layer.json is dirty."""

    def test_incremental_invokes_ai_regenerate_when_ai_layer_dirty(self, work_dir):
        """When webflux_ai_layer.json is dirty and ai_layer is not None, regenerate() is called."""
        app_dir = _scaffold_app(work_dir, with_ai_layer=True)
        bundle = load_all_definitions(app_dir)
        assert bundle.ai_layer is not None

        output_dir = Path("generated_application") / "test_app"
        output_dir.mkdir(parents=True, exist_ok=True)
        tracker = StatusTracker(app_dir)
        args = _make_args(skip_sql=True, skip_java=False)

        dirty_files = ["webflux_ai_layer.json"]

        mock_ai_gen_instance = MagicMock()
        mock_ai_gen_instance.regenerate.return_value = [Path("ai_regen.java")]
        mock_ai_gen_class = MagicMock(return_value=mock_ai_gen_instance)

        import types
        fake_module = types.ModuleType("generators.ai_generator")
        fake_module.AiGenerator = mock_ai_gen_class

        with patch.dict("sys.modules", {"generators.ai_generator": fake_module}):
            regenerated = _incremental_generation(
                bundle, dirty_files, output_dir, tracker, args,
            )

        mock_ai_gen_instance.regenerate.assert_called_once_with(bundle, output_dir)
        assert Path("ai_regen.java") in regenerated

    def test_incremental_skips_ai_when_ai_layer_not_dirty(self, work_dir):
        """When webflux_ai_layer.json is NOT in dirty files, AI regeneration is skipped."""
        app_dir = _scaffold_app(work_dir, with_ai_layer=True)
        bundle = load_all_definitions(app_dir)

        output_dir = Path("generated_application") / "test_app"
        output_dir.mkdir(parents=True, exist_ok=True)
        tracker = StatusTracker(app_dir)
        args = _make_args(skip_sql=True, skip_java=False)

        # Only entity_layer is dirty, not ai_layer
        dirty_files = ["webflux_entity_layer.json"]

        mock_ai_gen_instance = MagicMock()
        mock_ai_gen_class = MagicMock(return_value=mock_ai_gen_instance)

        import types
        fake_module = types.ModuleType("generators.ai_generator")
        fake_module.AiGenerator = mock_ai_gen_class

        with patch.dict("sys.modules", {"generators.ai_generator": fake_module}):
            _incremental_generation(bundle, dirty_files, output_dir, tracker, args)

        # AiGenerator should NOT have been instantiated
        mock_ai_gen_class.assert_not_called()

    def test_incremental_skips_ai_when_ai_layer_is_none(self, work_dir):
        """When ai_layer is None (file absent), AI regeneration is skipped even if dirty."""
        app_dir = _scaffold_app(work_dir, with_ai_layer=False)
        bundle = load_all_definitions(app_dir)
        assert bundle.ai_layer is None

        output_dir = Path("generated_application") / "test_app"
        output_dir.mkdir(parents=True, exist_ok=True)
        tracker = StatusTracker(app_dir)
        args = _make_args(skip_sql=True, skip_java=False)

        # Even if dirty_files contains ai_layer, bundle.ai_layer is None → skip
        dirty_files = ["webflux_ai_layer.json"]

        mock_ai_gen_class = MagicMock()

        import types
        fake_module = types.ModuleType("generators.ai_generator")
        fake_module.AiGenerator = mock_ai_gen_class

        with patch.dict("sys.modules", {"generators.ai_generator": fake_module}):
            _incremental_generation(bundle, dirty_files, output_dir, tracker, args)

        mock_ai_gen_class.assert_not_called()

    def test_incremental_handles_import_error_gracefully(self, work_dir):
        """When AiGenerator module doesn't exist, incremental pipeline continues."""
        app_dir = _scaffold_app(work_dir, with_ai_layer=True)
        bundle = load_all_definitions(app_dir)

        output_dir = Path("generated_application") / "test_app"
        output_dir.mkdir(parents=True, exist_ok=True)
        tracker = StatusTracker(app_dir)
        args = _make_args(skip_sql=True, skip_java=False)

        dirty_files = ["webflux_ai_layer.json"]

        with patch.dict("sys.modules", {"generators.ai_generator": None}):
            regenerated = _incremental_generation(
                bundle, dirty_files, output_dir, tracker, args,
            )

        assert isinstance(regenerated, list)
