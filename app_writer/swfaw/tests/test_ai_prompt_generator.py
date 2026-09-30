"""Unit tests for the AI PromptGenerator.

Verifies that the PromptGenerator produces a correct PromptTemplateEngine
Java source file with placeholder interpolation, single-pass replacement,
nested brace handling, and null/empty template handling.
"""

import sys
from pathlib import Path

import pytest

# Ensure swfaw package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import jinja2

from swfaw.generators.ai_prompt_generator import PromptGenerator


@pytest.fixture
def jinja_env():
    """Create a Jinja2 environment pointing at the swfaw/templates directory."""
    templates_dir = Path(__file__).resolve().parent.parent / "templates"
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(templates_dir)),
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )


@pytest.fixture
def generator(jinja_env):
    return PromptGenerator(jinja_env)


@pytest.fixture
def output_dirs():
    return {
        "service": Path("com/example/app/ai/service"),
    }


BASE_PACKAGE = "com.example.app"


class TestPromptGeneratorGenerate:
    """Tests for the generate() method output structure."""

    def test_generates_one_file(self, generator, output_dirs):
        results = generator.generate(BASE_PACKAGE, output_dirs)
        assert len(results) == 1

    def test_filepath_is_correct(self, generator, output_dirs):
        results = generator.generate(BASE_PACKAGE, output_dirs)
        filepath, _ = results[0]
        assert filepath == "com/example/app/ai/service/PromptTemplateEngine.java"

    def test_content_is_nonempty(self, generator, output_dirs):
        results = generator.generate(BASE_PACKAGE, output_dirs)
        _, content = results[0]
        assert len(content) > 0

    def test_default_output_dir(self, generator):
        results = generator.generate(BASE_PACKAGE, {})
        filepath, _ = results[0]
        assert filepath == "ai/service/PromptTemplateEngine.java"


class TestPromptTemplateEngineContent:
    """Tests for the rendered Java source content."""

    def _render(self, generator):
        return generator._render_prompt_template_engine(BASE_PACKAGE)

    def test_package_declaration(self, generator):
        content = self._render(generator)
        assert "package com.example.app.ai.service;" in content

    def test_class_declaration(self, generator):
        content = self._render(generator)
        assert "public class PromptTemplateEngine" in content

    def test_component_annotation(self, generator):
        content = self._render(generator)
        assert "@Component" in content

    def test_slf4j_annotation(self, generator):
        content = self._render(generator)
        assert "@Slf4j" in content

    def test_interpolate_method_exists(self, generator):
        content = self._render(generator)
        assert "public String interpolate(" in content

    def test_accepts_template_and_map(self, generator):
        content = self._render(generator)
        assert "String template" in content
        assert "Map<String, Object> values" in content

    def test_placeholder_pattern_regex(self, generator):
        """Req 3.13: Regex matches {{placeholder}} patterns."""
        content = self._render(generator)
        assert "PLACEHOLDER_PATTERN" in content
        # The regex should use Pattern.compile with a pattern matching {{...}}
        assert "Pattern.compile(" in content
        assert "[^{}]" in content

    def test_null_template_handling(self, generator):
        """Req 3.22: Null templates return empty string."""
        content = self._render(generator)
        assert "template == null" in content

    def test_empty_template_handling(self, generator):
        """Req 3.22: Empty templates return empty string."""
        content = self._render(generator)
        assert "template.isEmpty()" in content

    def test_empty_values_returns_template(self, generator):
        """Req 3.15/3.20: Empty map returns template unchanged (identity)."""
        content = self._render(generator)
        assert "values == null || values.isEmpty()" in content

    def test_single_pass_replacement(self, generator):
        """Req 3.19: Uses Matcher appendReplacement for single-pass."""
        content = self._render(generator)
        assert "appendReplacement" in content
        assert "appendTail" in content

    def test_quote_replacement_for_safety(self, generator):
        """Values with $ or \\ should not cause regex issues."""
        content = self._render(generator)
        assert "Matcher.quoteReplacement" in content

    def test_unresolved_placeholder_warning(self, generator):
        """Req 3.15: Unresolved placeholders log a warning."""
        content = self._render(generator)
        assert "log.warn" in content

    def test_string_valueof_conversion(self, generator):
        """Req 3.14: Non-string values converted via String.valueOf()."""
        content = self._render(generator)
        assert "String.valueOf" in content

    def test_contains_key_check(self, generator):
        """Req 3.14/3.15: Check if key exists before replacing."""
        content = self._render(generator)
        assert "values.containsKey(key)" in content
