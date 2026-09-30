"""Unit tests for the AI EvaluatorGenerator.

Verifies that the EvaluatorGenerator produces correct Java source files
for EvaluationPipelineService, EvaluationResultDTO, AiResponseWithEvaluationDTO,
EvaluationStatsDTO, EvaluatorBreakdownDTO, AiEvaluationResult entity,
AiEvaluationResultRepository, and EvaluationController.

Requirements: 10.1–10.12
"""

import sys
from pathlib import Path

import pytest

# Ensure swfaw package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import jinja2

from swfaw.generators.ai_evaluator_generator import (
    EvaluatorGenerator,
    _pascal_case,
    _camel_case,
    VALID_EVALUATOR_TYPES,
    VALID_SCORING_MECHANISMS,
    VALID_FAILURE_ACTIONS,
    VALID_MODES,
)


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
    return EvaluatorGenerator(jinja_env)


@pytest.fixture
def numeric_evaluator():
    """A numeric scoring evaluator (sync, retry)."""
    return {
        "name": "relevancyCheck",
        "type": "relevancy",
        "providerName": "mainGpt",
        "evaluationPrompt": "Rate relevancy of output to input. Score 0.0-1.0. Input: {{input}} Output: {{output}}",
        "scoringMechanism": "numeric",
        "threshold": 0.7,
        "failureAction": "retry",
        "maxRetries": 2,
        "mode": "sync",
    }


@pytest.fixture
def pass_fail_evaluator():
    """A pass/fail scoring evaluator (async, warn)."""
    return {
        "name": "safetyFilter",
        "type": "safety",
        "providerName": "safetyGpt",
        "evaluationPrompt": "Is this output safe? Reply PASS or FAIL. Input: {{input}} Output: {{output}}",
        "scoringMechanism": "pass_fail",
        "failureAction": "warn",
        "mode": "async",
    }


@pytest.fixture
def categorical_evaluator():
    """A categorical scoring evaluator (async, none)."""
    return {
        "name": "topicClassifier",
        "type": "custom",
        "providerName": "mainGpt",
        "evaluationPrompt": "Classify the topic. Input: {{input}} Output: {{output}}",
        "scoringMechanism": "categorical",
        "categories": ["technical", "business", "general"],
        "failureAction": "none",
        "mode": "async",
    }


@pytest.fixture
def all_evaluators(numeric_evaluator, pass_fail_evaluator, categorical_evaluator):
    return [numeric_evaluator, pass_fail_evaluator, categorical_evaluator]


@pytest.fixture
def output_dirs():
    return {
        "evaluator": Path("com/example/app/ai/evaluator"),
        "controller": Path("com/example/app/ai/controller"),
        "dto": Path("com/example/app/ai/dto"),
        "entity": Path("com/example/app/ai/entity"),
        "repository": Path("com/example/app/ai/repository"),
    }


BASE_PACKAGE = "com.example.app"


# ======================================================================
# Test: Helper functions
# ======================================================================

class TestHelperFunctions:
    def test_pascal_case_camel(self):
        assert _pascal_case("relevancyCheck") == "RelevancyCheck"

    def test_pascal_case_snake(self):
        assert _pascal_case("relevancy_check") == "RelevancyCheck"

    def test_pascal_case_single(self):
        assert _pascal_case("safety") == "Safety"

    def test_pascal_case_empty(self):
        assert _pascal_case("") == ""

    def test_camel_case(self):
        assert _camel_case("RelevancyCheck") == "relevancyCheck"

    def test_camel_case_snake(self):
        assert _camel_case("relevancy_check") == "relevancyCheck"

    def test_valid_evaluator_types(self):
        assert VALID_EVALUATOR_TYPES == {"relevancy", "correctness", "safety", "custom"}

    def test_valid_scoring_mechanisms(self):
        assert VALID_SCORING_MECHANISMS == {"numeric", "pass_fail", "categorical"}

    def test_valid_failure_actions(self):
        assert VALID_FAILURE_ACTIONS == {"none", "retry", "warn"}

    def test_valid_modes(self):
        assert VALID_MODES == {"sync", "async"}


# ======================================================================
# Test: generate() — skip logic and file counts
# ======================================================================

class TestEvaluatorGeneratorGenerate:
    """Tests for the generate() method's file output and skip logic."""

    def test_no_files_when_no_evaluators(self, generator, output_dirs):
        """Req 10.3: No evaluator files when evaluators is None."""
        results = generator.generate(None, BASE_PACKAGE, output_dirs)
        assert results == []

    def test_no_files_when_empty_evaluators(self, generator, output_dirs):
        results = generator.generate([], BASE_PACKAGE, output_dirs)
        assert results == []

    def test_single_evaluator_generates_8_files(
        self, generator, numeric_evaluator, output_dirs
    ):
        """Single evaluator: 4 DTOs + entity + repository + service + controller = 8."""
        results = generator.generate([numeric_evaluator], BASE_PACKAGE, output_dirs)
        assert len(results) == 8

    def test_multiple_evaluators_still_8_files(
        self, generator, all_evaluators, output_dirs
    ):
        """Multiple evaluators still produce 8 files (service handles all)."""
        results = generator.generate(all_evaluators, BASE_PACKAGE, output_dirs)
        assert len(results) == 8

    def test_all_content_is_nonempty(
        self, generator, all_evaluators, output_dirs
    ):
        results = generator.generate(all_evaluators, BASE_PACKAGE, output_dirs)
        for filepath, content in results:
            assert content.strip(), f"Empty content for {filepath}"

    def test_output_dirs_used_in_paths(
        self, generator, numeric_evaluator, output_dirs
    ):
        results = generator.generate([numeric_evaluator], BASE_PACKAGE, output_dirs)
        for filepath, _ in results:
            assert filepath.startswith("com/example/app/ai/")

    def test_correct_filenames(self, generator, numeric_evaluator, output_dirs):
        results = generator.generate([numeric_evaluator], BASE_PACKAGE, output_dirs)
        filenames = {Path(fp).name for fp, _ in results}
        expected = {
            "EvaluationResultDTO.java",
            "AiResponseWithEvaluationDTO.java",
            "EvaluationStatsDTO.java",
            "EvaluatorBreakdownDTO.java",
            "AiEvaluationResult.java",
            "AiEvaluationResultRepository.java",
            "EvaluationPipelineService.java",
            "EvaluationController.java",
        }
        assert filenames == expected


# ======================================================================
# Test: EvaluationResultDTO template
# ======================================================================

class TestEvaluationResultDTO:
    """Tests for the generated EvaluationResultDTO record."""

    def _get_dto(self, generator, evaluators, output_dirs):
        results = generator.generate(evaluators, BASE_PACKAGE, output_dirs)
        return next(c for fp, c in results if Path(fp).name == "EvaluationResultDTO.java")

    def test_is_record(self, generator, numeric_evaluator, output_dirs):
        content = self._get_dto(generator, [numeric_evaluator], output_dirs)
        assert "public record EvaluationResultDTO(" in content

    def test_package_declaration(self, generator, numeric_evaluator, output_dirs):
        content = self._get_dto(generator, [numeric_evaluator], output_dirs)
        assert f"package {BASE_PACKAGE}.ai.dto;" in content

    def test_has_evaluator_name(self, generator, numeric_evaluator, output_dirs):
        content = self._get_dto(generator, [numeric_evaluator], output_dirs)
        assert "String evaluatorName" in content

    def test_has_type(self, generator, numeric_evaluator, output_dirs):
        content = self._get_dto(generator, [numeric_evaluator], output_dirs)
        assert "String type" in content

    def test_has_score(self, generator, numeric_evaluator, output_dirs):
        content = self._get_dto(generator, [numeric_evaluator], output_dirs)
        assert "double score" in content

    def test_has_category(self, generator, numeric_evaluator, output_dirs):
        content = self._get_dto(generator, [numeric_evaluator], output_dirs)
        assert "String category" in content

    def test_has_status(self, generator, numeric_evaluator, output_dirs):
        content = self._get_dto(generator, [numeric_evaluator], output_dirs)
        assert "String status" in content

    def test_has_input(self, generator, numeric_evaluator, output_dirs):
        content = self._get_dto(generator, [numeric_evaluator], output_dirs)
        assert "String input" in content

    def test_has_output(self, generator, numeric_evaluator, output_dirs):
        content = self._get_dto(generator, [numeric_evaluator], output_dirs)
        assert "String output" in content


# ======================================================================
# Test: AiResponseWithEvaluationDTO template
# ======================================================================

class TestAiResponseWithEvaluationDTO:
    """Tests for the generated AiResponseWithEvaluationDTO record."""

    def _get_dto(self, generator, evaluators, output_dirs):
        results = generator.generate(evaluators, BASE_PACKAGE, output_dirs)
        return next(c for fp, c in results if Path(fp).name == "AiResponseWithEvaluationDTO.java")

    def test_is_record(self, generator, numeric_evaluator, output_dirs):
        """Req 10.8: AiResponseWithEvaluationDTO with response, evaluations, warnings."""
        content = self._get_dto(generator, [numeric_evaluator], output_dirs)
        assert "public record AiResponseWithEvaluationDTO(" in content

    def test_has_response(self, generator, numeric_evaluator, output_dirs):
        content = self._get_dto(generator, [numeric_evaluator], output_dirs)
        assert "String response" in content

    def test_has_evaluations(self, generator, numeric_evaluator, output_dirs):
        content = self._get_dto(generator, [numeric_evaluator], output_dirs)
        assert "List<EvaluationResultDTO> evaluations" in content

    def test_has_warnings(self, generator, numeric_evaluator, output_dirs):
        content = self._get_dto(generator, [numeric_evaluator], output_dirs)
        assert "List<String> warnings" in content


# ======================================================================
# Test: EvaluationStatsDTO template
# ======================================================================

class TestEvaluationStatsDTO:
    """Tests for the generated EvaluationStatsDTO record."""

    def _get_dto(self, generator, evaluators, output_dirs):
        results = generator.generate(evaluators, BASE_PACKAGE, output_dirs)
        return next(c for fp, c in results if Path(fp).name == "EvaluationStatsDTO.java")

    def test_is_record(self, generator, numeric_evaluator, output_dirs):
        content = self._get_dto(generator, [numeric_evaluator], output_dirs)
        assert "public record EvaluationStatsDTO(" in content

    def test_has_total(self, generator, numeric_evaluator, output_dirs):
        content = self._get_dto(generator, [numeric_evaluator], output_dirs)
        assert "long totalEvaluations" in content

    def test_has_pass_count(self, generator, numeric_evaluator, output_dirs):
        content = self._get_dto(generator, [numeric_evaluator], output_dirs)
        assert "long passCount" in content

    def test_has_breakdown(self, generator, numeric_evaluator, output_dirs):
        content = self._get_dto(generator, [numeric_evaluator], output_dirs)
        assert "List<EvaluatorBreakdownDTO> breakdown" in content


# ======================================================================
# Test: AiEvaluationResult entity template
# ======================================================================

class TestAiEvaluationResultEntity:
    """Tests for the generated AiEvaluationResult entity."""

    def _get_entity(self, generator, evaluators, output_dirs):
        results = generator.generate(evaluators, BASE_PACKAGE, output_dirs)
        return next(c for fp, c in results if Path(fp).name == "AiEvaluationResult.java")

    def test_package_declaration(self, generator, numeric_evaluator, output_dirs):
        content = self._get_entity(generator, [numeric_evaluator], output_dirs)
        assert f"package {BASE_PACKAGE}.ai.entity;" in content

    def test_table_annotation(self, generator, numeric_evaluator, output_dirs):
        """Req 10.9: @Table("ai_evaluation_result")."""
        content = self._get_entity(generator, [numeric_evaluator], output_dirs)
        assert '@Table("ai_evaluation_result")' in content

    def test_has_id(self, generator, numeric_evaluator, output_dirs):
        content = self._get_entity(generator, [numeric_evaluator], output_dirs)
        assert "@Id" in content
        assert "Long id" in content

    def test_has_user_id(self, generator, numeric_evaluator, output_dirs):
        content = self._get_entity(generator, [numeric_evaluator], output_dirs)
        assert "Long userId" in content

    def test_has_operation_name(self, generator, numeric_evaluator, output_dirs):
        content = self._get_entity(generator, [numeric_evaluator], output_dirs)
        assert "String operationName" in content

    def test_has_evaluator_name(self, generator, numeric_evaluator, output_dirs):
        content = self._get_entity(generator, [numeric_evaluator], output_dirs)
        assert "String evaluatorName" in content

    def test_has_evaluator_type(self, generator, numeric_evaluator, output_dirs):
        content = self._get_entity(generator, [numeric_evaluator], output_dirs)
        assert "String evaluatorType" in content

    def test_has_scoring_mechanism(self, generator, numeric_evaluator, output_dirs):
        content = self._get_entity(generator, [numeric_evaluator], output_dirs)
        assert "String scoringMechanism" in content

    def test_has_score(self, generator, numeric_evaluator, output_dirs):
        content = self._get_entity(generator, [numeric_evaluator], output_dirs)
        assert "Double score" in content

    def test_has_category(self, generator, numeric_evaluator, output_dirs):
        content = self._get_entity(generator, [numeric_evaluator], output_dirs)
        assert "String category" in content

    def test_has_status(self, generator, numeric_evaluator, output_dirs):
        content = self._get_entity(generator, [numeric_evaluator], output_dirs)
        assert "String status" in content

    def test_has_input_text(self, generator, numeric_evaluator, output_dirs):
        content = self._get_entity(generator, [numeric_evaluator], output_dirs)
        assert "String inputText" in content

    def test_has_output_text(self, generator, numeric_evaluator, output_dirs):
        content = self._get_entity(generator, [numeric_evaluator], output_dirs)
        assert "String outputText" in content

    def test_has_evaluation_response(self, generator, numeric_evaluator, output_dirs):
        content = self._get_entity(generator, [numeric_evaluator], output_dirs)
        assert "String evaluationResponse" in content

    def test_has_created_at(self, generator, numeric_evaluator, output_dirs):
        content = self._get_entity(generator, [numeric_evaluator], output_dirs)
        assert "LocalDateTime createdAt" in content

    def test_lombok_annotations(self, generator, numeric_evaluator, output_dirs):
        content = self._get_entity(generator, [numeric_evaluator], output_dirs)
        assert "@Data" in content
        assert "@Builder" in content
        assert "@NoArgsConstructor" in content
        assert "@AllArgsConstructor" in content


# ======================================================================
# Test: AiEvaluationResultRepository template
# ======================================================================

class TestAiEvaluationResultRepository:
    """Tests for the generated AiEvaluationResultRepository."""

    def _get_repo(self, generator, evaluators, output_dirs):
        results = generator.generate(evaluators, BASE_PACKAGE, output_dirs)
        return next(c for fp, c in results if Path(fp).name == "AiEvaluationResultRepository.java")

    def test_package_declaration(self, generator, numeric_evaluator, output_dirs):
        content = self._get_repo(generator, [numeric_evaluator], output_dirs)
        assert f"package {BASE_PACKAGE}.ai.repository;" in content

    def test_repository_annotation(self, generator, numeric_evaluator, output_dirs):
        content = self._get_repo(generator, [numeric_evaluator], output_dirs)
        assert "@Repository" in content

    def test_extends_reactive_crud(self, generator, numeric_evaluator, output_dirs):
        content = self._get_repo(generator, [numeric_evaluator], output_dirs)
        assert "extends ReactiveCrudRepository<AiEvaluationResult, Long>" in content

    def test_find_by_operation_name(self, generator, numeric_evaluator, output_dirs):
        content = self._get_repo(generator, [numeric_evaluator], output_dirs)
        assert "findByOperationNameOrderByCreatedAtDesc" in content

    def test_find_by_evaluator_name(self, generator, numeric_evaluator, output_dirs):
        content = self._get_repo(generator, [numeric_evaluator], output_dirs)
        assert "findByEvaluatorNameOrderByCreatedAtDesc" in content

    def test_find_by_user_id(self, generator, numeric_evaluator, output_dirs):
        content = self._get_repo(generator, [numeric_evaluator], output_dirs)
        assert "findByUserIdOrderByCreatedAtDesc" in content

    def test_find_by_status(self, generator, numeric_evaluator, output_dirs):
        content = self._get_repo(generator, [numeric_evaluator], output_dirs)
        assert "findByStatusOrderByCreatedAtDesc" in content

    def test_find_all(self, generator, numeric_evaluator, output_dirs):
        content = self._get_repo(generator, [numeric_evaluator], output_dirs)
        assert "findAllByOrderByCreatedAtDesc" in content


# ======================================================================
# Test: EvaluationPipelineService template
# ======================================================================

class TestEvaluationPipelineService:
    """Tests for the generated EvaluationPipelineService."""

    def _get_service(self, generator, evaluators, output_dirs):
        results = generator.generate(evaluators, BASE_PACKAGE, output_dirs)
        return next(c for fp, c in results if Path(fp).name == "EvaluationPipelineService.java")

    def test_package_declaration(self, generator, numeric_evaluator, output_dirs):
        content = self._get_service(generator, [numeric_evaluator], output_dirs)
        assert f"package {BASE_PACKAGE}.ai.evaluator;" in content

    def test_service_annotation(self, generator, numeric_evaluator, output_dirs):
        content = self._get_service(generator, [numeric_evaluator], output_dirs)
        assert "@Service" in content

    def test_class_name(self, generator, numeric_evaluator, output_dirs):
        """Req 10.3: EvaluationPipelineService."""
        content = self._get_service(generator, [numeric_evaluator], output_dirs)
        assert "public class EvaluationPipelineService" in content

    def test_evaluate_method(self, generator, numeric_evaluator, output_dirs):
        """Req 10.3: evaluate(...) method returning Flux<EvaluationResultDTO>."""
        content = self._get_service(generator, [numeric_evaluator], output_dirs)
        assert "Flux<EvaluationResultDTO> evaluate(" in content

    def test_evaluate_sync_method(self, generator, numeric_evaluator, output_dirs):
        """Req 10.4: evaluateSync returning AiResponseWithEvaluationDTO."""
        content = self._get_service(generator, [numeric_evaluator], output_dirs)
        assert "Mono<AiResponseWithEvaluationDTO> evaluateSync(" in content

    def test_evaluate_async_method(self, generator, numeric_evaluator, output_dirs):
        """Req 10.4: evaluateAsync running on Schedulers.boundedElastic()."""
        content = self._get_service(generator, [numeric_evaluator], output_dirs)
        assert "Mono<Void> evaluateAsync(" in content
        assert "Schedulers.boundedElastic()" in content

    def test_chat_client_qualifier(self, generator, numeric_evaluator, output_dirs):
        """Evaluator uses its own provider's ChatClient via @Qualifier."""
        content = self._get_service(generator, [numeric_evaluator], output_dirs)
        assert '@Qualifier("mainGpt")' in content

    def test_multiple_evaluator_qualifiers(self, generator, all_evaluators, output_dirs):
        """Multiple evaluators each get their own ChatClient."""
        content = self._get_service(generator, all_evaluators, output_dirs)
        assert '@Qualifier("mainGpt")' in content
        assert '@Qualifier("safetyGpt")' in content

    def test_numeric_scoring(self, generator, numeric_evaluator, output_dirs):
        """Req 10.1: Numeric scoring with threshold."""
        content = self._get_service(generator, [numeric_evaluator], output_dirs)
        assert "parseNumericScore" in content
        assert "0.7" in content  # threshold

    def test_pass_fail_scoring(self, generator, pass_fail_evaluator, output_dirs):
        """Req 10.1: Pass/fail scoring."""
        content = self._get_service(generator, [pass_fail_evaluator], output_dirs)
        assert 'response.toLowerCase().contains("pass")' in content

    def test_categorical_scoring(self, generator, categorical_evaluator, output_dirs):
        """Req 10.1: Categorical scoring."""
        content = self._get_service(generator, [categorical_evaluator], output_dirs)
        assert "response.trim()" in content
        assert '"evaluated"' in content

    def test_retry_logic(self, generator, numeric_evaluator, output_dirs):
        """Req 10.5: Retry when failureAction is 'retry'."""
        content = self._get_service(generator, [numeric_evaluator], output_dirs)
        assert "retryEvaluation" in content
        assert "maxRetries" in content or "2" in content

    def test_warn_logic(self, generator, pass_fail_evaluator, output_dirs):
        """Req 10.5: Warn flag when failureAction is 'warn'."""
        content = self._get_service(generator, [pass_fail_evaluator], output_dirs)
        assert '"warn"' in content
        assert "flagged" in content

    def test_concurrent_execution(self, generator, all_evaluators, output_dirs):
        """Req 10.6: Multiple evaluators execute concurrently via Flux.merge."""
        content = self._get_service(generator, all_evaluators, output_dirs)
        assert "Flux.merge(evaluations)" in content

    def test_evaluation_prompt_placeholders(self, generator, numeric_evaluator, output_dirs):
        """Req 10.2: evaluationPrompt with {{input}}/{{output}} placeholders."""
        content = self._get_service(generator, [numeric_evaluator], output_dirs)
        assert '.replace("{{input}}", inputText)' in content
        assert '.replace("{{output}}", outputText)' in content

    def test_stores_result_in_repository(self, generator, numeric_evaluator, output_dirs):
        """Req 10.3: Stores results in ai_evaluation_result."""
        content = self._get_service(generator, [numeric_evaluator], output_dirs)
        assert "evaluationResultRepository.save(" in content

    def test_error_handling(self, generator, numeric_evaluator, output_dirs):
        """Error handling returns error status DTO."""
        content = self._get_service(generator, [numeric_evaluator], output_dirs)
        assert "onErrorResume" in content
        assert '"error"' in content


# ======================================================================
# Test: EvaluationController template
# ======================================================================

class TestEvaluationController:
    """Tests for the generated EvaluationController."""

    def _get_controller(self, generator, evaluators, output_dirs):
        results = generator.generate(evaluators, BASE_PACKAGE, output_dirs)
        return next(c for fp, c in results if Path(fp).name == "EvaluationController.java")

    def test_package_declaration(self, generator, numeric_evaluator, output_dirs):
        content = self._get_controller(generator, [numeric_evaluator], output_dirs)
        assert f"package {BASE_PACKAGE}.ai.controller;" in content

    def test_rest_controller_annotation(self, generator, numeric_evaluator, output_dirs):
        content = self._get_controller(generator, [numeric_evaluator], output_dirs)
        assert "@RestController" in content

    def test_base_path(self, generator, numeric_evaluator, output_dirs):
        """Req 10.10: Base path /api/ai/evaluations."""
        content = self._get_controller(generator, [numeric_evaluator], output_dirs)
        assert '@RequestMapping("/api/ai/evaluations")' in content

    def test_list_results_endpoint(self, generator, numeric_evaluator, output_dirs):
        """Req 10.10: GET / (list results with filters)."""
        content = self._get_controller(generator, [numeric_evaluator], output_dirs)
        assert "@GetMapping" in content
        assert "listResults(" in content

    def test_stats_endpoint(self, generator, numeric_evaluator, output_dirs):
        """Req 10.10: GET /stats (aggregate statistics)."""
        content = self._get_controller(generator, [numeric_evaluator], output_dirs)
        assert '@GetMapping("/stats")' in content
        assert "getStats()" in content

    def test_by_operation_endpoint(self, generator, numeric_evaluator, output_dirs):
        """Req 10.10: GET /by-operation/{operationName}."""
        content = self._get_controller(generator, [numeric_evaluator], output_dirs)
        assert '/by-operation/{operationName}' in content
        assert "getByOperation(" in content

    def test_filter_by_evaluator_name(self, generator, numeric_evaluator, output_dirs):
        """Supports filtering by evaluatorName."""
        content = self._get_controller(generator, [numeric_evaluator], output_dirs)
        assert "evaluatorName" in content
        assert "@RequestParam" in content

    def test_filter_by_status(self, generator, numeric_evaluator, output_dirs):
        """Supports filtering by status."""
        content = self._get_controller(generator, [numeric_evaluator], output_dirs)
        assert "status" in content

    def test_stats_returns_breakdown(self, generator, numeric_evaluator, output_dirs):
        """Req 10.9: Stats include EvaluatorBreakdownDTO."""
        content = self._get_controller(generator, [numeric_evaluator], output_dirs)
        assert "EvaluationStatsDTO" in content
        assert "EvaluatorBreakdownDTO" in content

    def test_repository_injection(self, generator, numeric_evaluator, output_dirs):
        content = self._get_controller(generator, [numeric_evaluator], output_dirs)
        assert "AiEvaluationResultRepository" in content


# ======================================================================
# Test: Pipeline context building
# ======================================================================

class TestBuildPipelineContext:
    """Tests for the _build_pipeline_context method."""

    def test_has_retry_flag_true(self, generator, numeric_evaluator):
        ctx = generator._build_pipeline_context([numeric_evaluator], BASE_PACKAGE)
        assert ctx["has_retry_evaluators"] is True

    def test_has_retry_flag_false(self, generator, pass_fail_evaluator):
        ctx = generator._build_pipeline_context([pass_fail_evaluator], BASE_PACKAGE)
        assert ctx["has_retry_evaluators"] is False

    def test_evaluator_names_processed(self, generator, all_evaluators):
        ctx = generator._build_pipeline_context(all_evaluators, BASE_PACKAGE)
        names = [e["name"] for e in ctx["evaluators"]]
        assert names == ["relevancyCheck", "safetyFilter", "topicClassifier"]

    def test_pascal_names(self, generator, all_evaluators):
        ctx = generator._build_pipeline_context(all_evaluators, BASE_PACKAGE)
        pascal_names = [e["name_pascal"] for e in ctx["evaluators"]]
        assert pascal_names == ["RelevancyCheck", "SafetyFilter", "TopicClassifier"]

    def test_camel_names(self, generator, all_evaluators):
        ctx = generator._build_pipeline_context(all_evaluators, BASE_PACKAGE)
        camel_names = [e["name_camel"] for e in ctx["evaluators"]]
        assert camel_names == ["relevancyCheck", "safetyFilter", "topicClassifier"]

    def test_default_failure_action(self, generator):
        ev = {"name": "test", "providerName": "gpt"}
        ctx = generator._build_pipeline_context([ev], BASE_PACKAGE)
        assert ctx["evaluators"][0]["failure_action"] == "none"

    def test_default_mode(self, generator):
        ev = {"name": "test", "providerName": "gpt"}
        ctx = generator._build_pipeline_context([ev], BASE_PACKAGE)
        assert ctx["evaluators"][0]["mode"] == "async"

    def test_default_threshold(self, generator):
        ev = {"name": "test", "providerName": "gpt"}
        ctx = generator._build_pipeline_context([ev], BASE_PACKAGE)
        assert ctx["evaluators"][0]["threshold"] == 0.5

    def test_default_max_retries(self, generator):
        ev = {"name": "test", "providerName": "gpt"}
        ctx = generator._build_pipeline_context([ev], BASE_PACKAGE)
        assert ctx["evaluators"][0]["max_retries"] == 1
