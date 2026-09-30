"""Smoke test for Scaffolder."""

import json
import shutil
from pathlib import Path

import pytest

from app_def_manager.scaffolder import Scaffolder, _to_snake_case, _to_camel_case


TEST_APP = "test_smoke_scaffolder"
TEST_DIR = Path("application_definitions") / TEST_APP


@pytest.fixture(autouse=True)
def cleanup():
    """Clean up test directory before and after each test."""
    if TEST_DIR.exists():
        shutil.rmtree(TEST_DIR)
    yield
    if TEST_DIR.exists():
        shutil.rmtree(TEST_DIR)


ENTITY_DESCRIPTIONS = [
    {"name": "Task", "fields": [{"name": "title", "type": "String"}, {"name": "due_date", "type": "LocalDate"}]},
    {"name": "Category", "fields": [{"name": "name", "type": "String"}]},
]


def test_snake_case():
    assert _to_snake_case("UserProfile") == "user_profile"
    assert _to_snake_case("firstName") == "first_name"
    assert _to_snake_case("Task") == "task"
    assert _to_snake_case("HTMLParser") == "html_parser"


def test_camel_case():
    assert _to_camel_case("first_name") == "firstName"
    assert _to_camel_case("title") == "title"


def test_scaffold_creates_all_files():
    scaffolder = Scaffolder()
    result = scaffolder.scaffold_application(TEST_APP, ENTITY_DESCRIPTIONS)

    expected = [
        "webflux_manifest.json", "webflux_project_metadata.json",
        "webflux_entity_layer.json", "webflux_entities.json",
        "webflux_relationships.json", "webflux_repository_layer.json",
        "webflux_service_layer.json", "webflux_controller_layer.json",
        "webflux_dto_layer.json", "_generation_status.json",
    ]
    for f in expected:
        assert (result / f).exists(), f"Missing: {f}"


def test_entity_layer_auto_fields():
    scaffolder = Scaffolder()
    result = scaffolder.scaffold_application(TEST_APP, ENTITY_DESCRIPTIONS)

    with open(result / "webflux_entity_layer.json") as f:
        el = json.load(f)

    task_entity = el["entities"][0]
    col_names = [fld["columnName"] for fld in task_entity["fields"]]
    assert "task_id" in col_names
    assert "title" in col_names
    assert "due_date" in col_names
    assert "created_at" in col_names
    assert "updated_at" in col_names

    # Verify PK
    pk_field = next(f for f in task_entity["fields"] if f["columnName"] == "task_id")
    assert pk_field["isPrimaryKey"] is True
    assert pk_field["isNullable"] is False
    assert pk_field["columnDefinition"] == "BIGINT UNSIGNED"


def test_entities_json():
    scaffolder = Scaffolder()
    result = scaffolder.scaffold_application(TEST_APP, ENTITY_DESCRIPTIONS)

    with open(result / "webflux_entities.json") as f:
        ent = json.load(f)

    assert len(ent["entities"]) == 2
    assert ent["entities"][0]["name"] == "task"
    assert ent["entities"][1]["name"] == "category"


def test_dto_layer():
    scaffolder = Scaffolder()
    result = scaffolder.scaffold_application(TEST_APP, ENTITY_DESCRIPTIONS)

    with open(result / "webflux_dto_layer.json") as f:
        dto = json.load(f)

    # 3 DTOs per entity (Input, Output, Filter) x 2 entities = 6
    assert len(dto["dtos"]) == 6
    types = [(d["entityName"], d["dtoType"]) for d in dto["dtos"]]
    assert ("Task", "Input") in types
    assert ("Task", "Output") in types
    assert ("Task", "Filter") in types
    assert ("Category", "Input") in types
    assert ("Category", "Output") in types
    assert ("Category", "Filter") in types


def test_status_all_dirty():
    scaffolder = Scaffolder()
    result = scaffolder.scaffold_application(TEST_APP, ENTITY_DESCRIPTIONS)

    with open(result / "_generation_status.json") as f:
        status = json.load(f)

    for fname, info in status["files"].items():
        assert info["status"] == "dirty"


def test_file_exists_error():
    scaffolder = Scaffolder()
    scaffolder.scaffold_application(TEST_APP, ENTITY_DESCRIPTIONS)

    with pytest.raises(FileExistsError):
        scaffolder.scaffold_application(TEST_APP, ENTITY_DESCRIPTIONS)


def test_force_flag():
    scaffolder = Scaffolder()
    scaffolder.scaffold_application(TEST_APP, ENTITY_DESCRIPTIONS)
    # Should not raise
    scaffolder.scaffold_application(TEST_APP, ENTITY_DESCRIPTIONS, force=True)


def test_controller_crud_endpoints():
    scaffolder = Scaffolder()
    result = scaffolder.scaffold_application(TEST_APP, ENTITY_DESCRIPTIONS)

    with open(result / "webflux_controller_layer.json") as f:
        ctrl = json.load(f)

    task_ctrl = ctrl["controllers"][0]
    eps = task_ctrl["endpoints"]
    assert eps["create"]["method"] == "POST"
    assert eps["getById"]["method"] == "GET"
    assert eps["getById"]["path"] == "/{id}"
    assert eps["getAll"]["method"] == "GET"
    assert eps["update"]["method"] == "PUT"
    assert eps["update"]["path"] == "/{id}"
    assert eps["delete"]["method"] == "DELETE"
    assert eps["delete"]["path"] == "/{id}"


def test_relationships_empty():
    scaffolder = Scaffolder()
    result = scaffolder.scaffold_application(TEST_APP, ENTITY_DESCRIPTIONS)

    with open(result / "webflux_relationships.json") as f:
        rels = json.load(f)

    assert rels == {"relationships": []}


def test_manifest_version():
    scaffolder = Scaffolder()
    result = scaffolder.scaffold_application(TEST_APP, ENTITY_DESCRIPTIONS)

    with open(result / "webflux_manifest.json") as f:
        manifest = json.load(f)

    assert manifest["version"] == "2.5"
    assert manifest["format"] == "split"
    assert manifest["statistics"]["total_entities"] == 2