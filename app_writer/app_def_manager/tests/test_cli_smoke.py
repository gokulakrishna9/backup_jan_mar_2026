"""Smoke tests for app_def_manager CLI."""

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

APP_DEFS = Path("application_definitions")
TEST_APP = "test_cli_smoke_app"


@pytest.fixture(autouse=True)
def cleanup():
    """Remove test app before and after each test."""
    app_dir = APP_DEFS / TEST_APP
    if app_dir.exists():
        shutil.rmtree(app_dir)
    yield
    if app_dir.exists():
        shutil.rmtree(app_dir)


def _run(*args):
    """Run CLI command and return CompletedProcess."""
    return subprocess.run(
        [sys.executable, "app_def_manager/cli.py", *args],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )


def test_list_apps_empty():
    r = _run("list-apps")
    assert r.returncode == 0


def test_scaffold_and_list():
    entities = json.dumps([
        {"name": "User", "fields": [{"name": "email", "type": "String"}]},
    ])
    r = _run("scaffold", "--name", TEST_APP, "--entities", entities)
    assert r.returncode == 0
    assert "Scaffolded" in r.stdout
    assert "1 entity" in r.stdout

    # list-apps should show it
    r = _run("list-apps")
    assert r.returncode == 0
    assert TEST_APP in r.stdout


def test_list_entities():
    entities = json.dumps([
        {"name": "User", "fields": [{"name": "email", "type": "String"}]},
        {"name": "Product", "fields": [{"name": "title", "type": "String"}]},
    ])
    _run("scaffold", "--name", TEST_APP, "--entities", entities)

    r = _run("list-entities", "--app", TEST_APP)
    assert r.returncode == 0
    assert "User" in r.stdout
    assert "Product" in r.stdout
    assert "2 entities" in r.stdout


def test_status():
    entities = json.dumps([
        {"name": "User", "fields": [{"name": "email", "type": "String"}]},
    ])
    _run("scaffold", "--name", TEST_APP, "--entities", entities)

    r = _run("status", "--app", TEST_APP)
    assert r.returncode == 0
    assert "dirty" in r.stdout


def test_add_and_remove_entity():
    entities = json.dumps([
        {"name": "User", "fields": [{"name": "email", "type": "String"}]},
    ])
    _run("scaffold", "--name", TEST_APP, "--entities", entities)

    fields = json.dumps([{"name": "title", "type": "String"}])
    r = _run("add-entity", "--app", TEST_APP, "--name", "Product", "--fields", fields)
    assert r.returncode == 0
    assert "Product" in r.stdout

    r = _run("list-entities", "--app", TEST_APP)
    assert "Product" in r.stdout

    r = _run("remove-entity", "--app", TEST_APP, "--name", "Product")
    assert r.returncode == 0
    assert "removed" in r.stdout


def test_add_and_remove_field():
    entities = json.dumps([
        {"name": "User", "fields": [{"name": "email", "type": "String"}]},
    ])
    _run("scaffold", "--name", TEST_APP, "--entities", entities)

    field = json.dumps({"name": "age", "type": "Integer"})
    r = _run("add-field", "--app", TEST_APP, "--entity", "User", "--field", field)
    assert r.returncode == 0
    assert "Field added" in r.stdout

    r = _run("remove-field", "--app", TEST_APP, "--entity", "User", "--field", "age")
    assert r.returncode == 0
    assert "removed" in r.stdout


def test_modify_field():
    entities = json.dumps([
        {"name": "User", "fields": [{"name": "email", "type": "String"}]},
    ])
    _run("scaffold", "--name", TEST_APP, "--entities", entities)

    updates = json.dumps({"type": "Integer"})
    r = _run("modify-field", "--app", TEST_APP, "--entity", "User",
             "--field", "email", "--updates", updates)
    assert r.returncode == 0
    assert "modified" in r.stdout


def test_mark_clean_and_dirty():
    entities = json.dumps([
        {"name": "User", "fields": [{"name": "email", "type": "String"}]},
    ])
    _run("scaffold", "--name", TEST_APP, "--entities", entities)

    r = _run("mark-clean", "--app", TEST_APP)
    assert r.returncode == 0
    assert "clean" in r.stdout

    r = _run("mark-dirty", "--app", TEST_APP, "--file", "webflux_entity_layer.json")
    assert r.returncode == 0
    assert "dirty" in r.stdout


def test_scaffold_duplicate_fails():
    entities = json.dumps([
        {"name": "User", "fields": [{"name": "email", "type": "String"}]},
    ])
    _run("scaffold", "--name", TEST_APP, "--entities", entities)

    r = _run("scaffold", "--name", TEST_APP, "--entities", entities)
    assert r.returncode == 1
    assert "already exists" in r.stderr


def test_add_endpoint_and_remove():
    entities = json.dumps([
        {"name": "User", "fields": [{"name": "email", "type": "String"}]},
    ])
    _run("scaffold", "--name", TEST_APP, "--entities", entities)

    endpoint = json.dumps({"name": "search", "path": "/search", "method": "GET"})
    r = _run("add-endpoint", "--app", TEST_APP, "--entity", "User", "--endpoint", endpoint)
    assert r.returncode == 0
    assert "Endpoint added" in r.stdout

    r = _run("remove-endpoint", "--app", TEST_APP, "--entity", "User", "--endpoint", "search")
    assert r.returncode == 0


def test_add_query_and_remove():
    entities = json.dumps([
        {"name": "User", "fields": [{"name": "email", "type": "String"}]},
    ])
    _run("scaffold", "--name", TEST_APP, "--entities", entities)

    query = json.dumps({"name": "findByEmail", "query": "SELECT * FROM user WHERE email = ?"})
    r = _run("add-query", "--app", TEST_APP, "--entity", "User", "--query", query)
    assert r.returncode == 0

    r = _run("remove-query", "--app", TEST_APP, "--entity", "User", "--query", "findByEmail")
    assert r.returncode == 0


def test_add_relationship_and_remove():
    entities = json.dumps([
        {"name": "User", "fields": [{"name": "email", "type": "String"}]},
        {"name": "Post", "fields": [{"name": "title", "type": "String"}]},
    ])
    _run("scaffold", "--name", TEST_APP, "--entities", entities)

    rel = json.dumps({"sourceEntity": "Post", "targetEntity": "User", "type": "ManyToOne"})
    r = _run("add-relationship", "--app", TEST_APP, "--relationship", rel)
    assert r.returncode == 0

    r = _run("remove-relationship", "--app", TEST_APP, "--source", "Post", "--target", "User")
    assert r.returncode == 0


def test_invalid_json_exits_1():
    r = _run("scaffold", "--name", TEST_APP, "--entities", "not-json")
    assert r.returncode == 1
    assert "Invalid JSON" in r.stderr


def test_status_missing_app():
    r = _run("status", "--app", "nonexistent_app_xyz")
    assert r.returncode == 1


def test_add_and_remove_json_column():
    entities = json.dumps([
        {"name": "User", "fields": [{"name": "email", "type": "String"}]},
    ])
    _run("scaffold", "--name", TEST_APP, "--entities", entities)

    r = _run("add-json-column", "--app", TEST_APP, "--entity", "User",
             "--column", "metadata", "--field", "metadata")
    assert r.returncode == 0
    assert "JSON column" in r.stdout
    assert "metadata" in r.stdout

    r = _run("remove-json-column", "--app", TEST_APP, "--entity", "User", "--field", "metadata")
    assert r.returncode == 0
    assert "removed" in r.stdout


def test_add_and_remove_document_collection():
    entities = json.dumps([
        {"name": "User", "fields": [{"name": "email", "type": "String"}]},
    ])
    _run("scaffold", "--name", TEST_APP, "--entities", entities)

    r = _run("add-document-collection", "--app", TEST_APP, "--name", "AuditLog",
             "--table", "audit_log_docs", "--description", "Audit log entries")
    assert r.returncode == 0
    assert "Document collection" in r.stdout
    assert "AuditLog" in r.stdout

    r = _run("remove-document-collection", "--app", TEST_APP, "--name", "AuditLog")
    assert r.returncode == 0
    assert "removed" in r.stdout


def test_add_document_collection_no_description():
    entities = json.dumps([
        {"name": "User", "fields": [{"name": "email", "type": "String"}]},
    ])
    _run("scaffold", "--name", TEST_APP, "--entities", entities)

    r = _run("add-document-collection", "--app", TEST_APP, "--name", "Notes",
             "--table", "notes_docs")
    assert r.returncode == 0
    assert "Notes" in r.stdout
