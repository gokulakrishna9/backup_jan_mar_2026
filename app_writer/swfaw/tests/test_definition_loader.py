"""Unit tests for swfaw/utils/definition_loader.py."""

import json
import sys
import tempfile
from pathlib import Path

import pytest

# Ensure swfaw/ is on sys.path so `from version import ...` works
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.definition_loader import (
    DefinitionBundle,
    load_all_definitions,
    reconstruct_database_definition,
    _load_json_file,
    _validate_entity_layer,
)


# ---------------------------------------------------------------------------
# Helpers — build minimal valid definition files
# ---------------------------------------------------------------------------

def _minimal_entity_layer():
    return {
        "entities": [
            {
                "tableName": "users",
                "className": "User",
                "fields": [
                    {"columnName": "user_id", "fieldName": "userId", "javaType": "Long",
                     "isPrimaryKey": True, "isNullable": False, "columnDefinition": "BIGINT UNSIGNED"},
                    {"columnName": "email", "fieldName": "email", "javaType": "String",
                     "isPrimaryKey": False, "isNullable": False, "columnDefinition": "VARCHAR(255)"},
                ],
            }
        ]
    }


def _minimal_manifest(extra_files=None):
    files = {
        "project_metadata": "webflux_project_metadata.json",
        "entities": "webflux_entities.json",
        "relationships": "webflux_relationships.json",
        "entity_layer": "webflux_entity_layer.json",
        "repository_layer": "webflux_repository_layer.json",
        "service_layer": "webflux_service_layer.json",
        "controller_layer": "webflux_controller_layer.json",
        "dto_layer": "webflux_dto_layer.json",
    }
    if extra_files:
        files.update(extra_files)
    return {"version": "2.5", "format": "split", "files": files}


def _write_json(directory: Path, filename: str, data: dict):
    with open(directory / filename, "w", encoding="utf-8") as f:
        json.dump(data, f)


def _setup_valid_app(tmp: Path):
    """Write a minimal but valid set of definition files."""
    app_dir = tmp / "my_app"
    app_dir.mkdir(parents=True)

    _write_json(app_dir, "webflux_manifest.json", _minimal_manifest())
    _write_json(app_dir, "webflux_project_metadata.json", {"projectMetadata": {"database": {"name": "my_db"}}})
    _write_json(app_dir, "webflux_entity_layer.json", _minimal_entity_layer())
    _write_json(app_dir, "webflux_entities.json", {"entities": [{"name": "users", "columns": []}]})
    _write_json(app_dir, "webflux_relationships.json", {"relationships": []})
    _write_json(app_dir, "webflux_repository_layer.json", {"repositories": []})
    _write_json(app_dir, "webflux_service_layer.json", {"services": []})
    _write_json(app_dir, "webflux_controller_layer.json", {"controllers": []})
    _write_json(app_dir, "webflux_dto_layer.json", {"dtos": []})
    return app_dir


# ---------------------------------------------------------------------------
# Tests — happy path
# ---------------------------------------------------------------------------

class TestLoadAllDefinitionsHappyPath:

    def test_loads_valid_definitions(self, tmp_path):
        app_dir = _setup_valid_app(tmp_path)
        bundle = load_all_definitions(app_dir)

        assert isinstance(bundle, DefinitionBundle)
        assert bundle.app_name == "my_app"
        assert bundle.definitions_dir == app_dir
        assert bundle.manifest["version"] == "2.5"
        assert bundle.entity_layer["entities"][0]["className"] == "User"

    def test_app_name_from_folder(self, tmp_path):
        app_dir = _setup_valid_app(tmp_path)
        bundle = load_all_definitions(app_dir)
        assert bundle.app_name == "my_app"

    def test_optional_layers_none_when_absent(self, tmp_path):
        app_dir = _setup_valid_app(tmp_path)
        bundle = load_all_definitions(app_dir)

        assert bundle.query_layer is None
        assert bundle.filter_layer is None
        assert bundle.security_layer is None
        assert bundle.config_layer is None
        assert bundle.custom_queries_layer is None
        assert bundle.group_definition_layer is None
        assert bundle.authorization_layer is None
        assert bundle.audit_logging_layer is None
        assert bundle.exception_layer is None

    def test_optional_layer_loaded_when_present(self, tmp_path):
        app_dir = _setup_valid_app(tmp_path)
        # Add an optional layer
        manifest = _minimal_manifest({"query_layer": "webflux_query_layer.json"})
        _write_json(app_dir, "webflux_manifest.json", manifest)
        _write_json(app_dir, "webflux_query_layer.json", {"queries": [{"name": "findByEmail"}]})

        bundle = load_all_definitions(app_dir)
        assert bundle.query_layer is not None
        assert bundle.query_layer["queries"][0]["name"] == "findByEmail"

    def test_accepts_all_supported_versions(self, tmp_path):
        for ver in ["2.2", "2.3", "2.4", "2.5"]:
            app_dir = _setup_valid_app(tmp_path / ver)
            manifest = _minimal_manifest()
            manifest["version"] = ver
            _write_json(app_dir, "webflux_manifest.json", manifest)
            bundle = load_all_definitions(app_dir)
            assert bundle.manifest["version"] == ver


# ---------------------------------------------------------------------------
# Tests — error cases
# ---------------------------------------------------------------------------

class TestLoadAllDefinitionsErrors:

    def test_missing_directory(self, tmp_path):
        with pytest.raises(FileNotFoundError, match="Definitions directory not found"):
            load_all_definitions(tmp_path / "nonexistent")

    def test_missing_manifest(self, tmp_path):
        app_dir = tmp_path / "app"
        app_dir.mkdir()
        with pytest.raises(FileNotFoundError, match="webflux_manifest.json"):
            load_all_definitions(app_dir)

    def test_invalid_manifest_json(self, tmp_path):
        app_dir = tmp_path / "app"
        app_dir.mkdir()
        (app_dir / "webflux_manifest.json").write_text("{bad json", encoding="utf-8")
        with pytest.raises(ValueError, match="Invalid JSON"):
            load_all_definitions(app_dir)

    def test_unsupported_manifest_version(self, tmp_path):
        app_dir = _setup_valid_app(tmp_path)
        manifest = _minimal_manifest()
        manifest["version"] = "1.0"
        _write_json(app_dir, "webflux_manifest.json", manifest)

        with pytest.raises(ValueError, match="Unsupported manifest version"):
            load_all_definitions(app_dir)

    def test_missing_required_file(self, tmp_path):
        app_dir = _setup_valid_app(tmp_path)
        (app_dir / "webflux_entities.json").unlink()

        with pytest.raises(FileNotFoundError, match="webflux_entities.json"):
            load_all_definitions(app_dir)

    def test_invalid_json_in_required_file(self, tmp_path):
        app_dir = _setup_valid_app(tmp_path)
        (app_dir / "webflux_entities.json").write_text("not json!", encoding="utf-8")

        with pytest.raises(ValueError, match="Invalid JSON"):
            load_all_definitions(app_dir)

    def test_manifest_missing_required_key(self, tmp_path):
        app_dir = _setup_valid_app(tmp_path)
        manifest = _minimal_manifest()
        del manifest["files"]["entities"]
        _write_json(app_dir, "webflux_manifest.json", manifest)

        with pytest.raises(ValueError, match="missing required file entry 'entities'"):
            load_all_definitions(app_dir)


# ---------------------------------------------------------------------------
# Tests — entity_layer validation
# ---------------------------------------------------------------------------

class TestEntityLayerValidation:

    def test_empty_entities_list(self, tmp_path):
        app_dir = _setup_valid_app(tmp_path)
        _write_json(app_dir, "webflux_entity_layer.json", {"entities": []})

        with pytest.raises(ValueError, match="non-empty 'entities' list"):
            load_all_definitions(app_dir)

    def test_entity_missing_tableName(self, tmp_path):
        app_dir = _setup_valid_app(tmp_path)
        bad_layer = {"entities": [{"className": "User", "fields": [
            {"columnName": "id", "fieldName": "id", "javaType": "Long"}
        ]}]}
        _write_json(app_dir, "webflux_entity_layer.json", bad_layer)

        with pytest.raises(ValueError, match="tableName"):
            load_all_definitions(app_dir)

    def test_entity_missing_className(self, tmp_path):
        app_dir = _setup_valid_app(tmp_path)
        bad_layer = {"entities": [{"tableName": "users", "fields": [
            {"columnName": "id", "fieldName": "id", "javaType": "Long"}
        ]}]}
        _write_json(app_dir, "webflux_entity_layer.json", bad_layer)

        with pytest.raises(ValueError, match="className"):
            load_all_definitions(app_dir)

    def test_entity_empty_fields(self, tmp_path):
        app_dir = _setup_valid_app(tmp_path)
        bad_layer = {"entities": [{"tableName": "users", "className": "User", "fields": []}]}
        _write_json(app_dir, "webflux_entity_layer.json", bad_layer)

        with pytest.raises(ValueError, match="non-empty 'fields' list"):
            load_all_definitions(app_dir)

    def test_field_missing_columnName(self, tmp_path):
        app_dir = _setup_valid_app(tmp_path)
        bad_layer = {"entities": [{"tableName": "users", "className": "User", "fields": [
            {"fieldName": "id", "javaType": "Long"}
        ]}]}
        _write_json(app_dir, "webflux_entity_layer.json", bad_layer)

        with pytest.raises(ValueError, match="columnName"):
            load_all_definitions(app_dir)

    def test_field_missing_javaType(self, tmp_path):
        app_dir = _setup_valid_app(tmp_path)
        bad_layer = {"entities": [{"tableName": "users", "className": "User", "fields": [
            {"columnName": "id", "fieldName": "id"}
        ]}]}
        _write_json(app_dir, "webflux_entity_layer.json", bad_layer)

        with pytest.raises(ValueError, match="javaType"):
            load_all_definitions(app_dir)


# ---------------------------------------------------------------------------
# Tests — reconstruct_database_definition
# ---------------------------------------------------------------------------

class TestReconstructDatabaseDefinition:

    def _make_bundle(self, entities, relationships=None, project_metadata=None):
        """Build a minimal DefinitionBundle for testing reconstruction."""
        if relationships is None:
            relationships = []
        if project_metadata is None:
            project_metadata = {
                "name": "test_app",
                "applicationName": "Test App",
                "groupId": "com.example",
                "artifactId": "test-app",
                "version": "1.0.0",
                "port": 8081,
                "database": {
                    "type": "mysql",
                    "host": "localhost",
                    "port": 3306,
                    "name": "test_db",
                    "username": "root",
                    "password": "password",
                },
            }
        return DefinitionBundle(
            app_name="test_app",
            definitions_dir=Path("/tmp/test_app"),
            manifest={"version": "2.5", "files": {}},
            project_metadata={"projectMetadata": project_metadata},
            entity_layer={"entities": []},
            entities={"entities": entities},
            relationships={"relationships": relationships},
            repository_layer={"repositories": []},
            service_layer={"services": []},
            controller_layer={"controllers": []},
            dto_layer={"dtos": []},
        )

    def test_basic_reconstruction(self):
        entities = [
            {
                "name": "users",
                "columns": [
                    {"name": "id", "type": "BIGINT UNSIGNED", "primaryKey": True, "nullable": False},
                    {"name": "email", "type": "VARCHAR(255)", "primaryKey": False, "nullable": False},
                ],
            }
        ]
        bundle = self._make_bundle(entities)
        db_def = reconstruct_database_definition(bundle)

        assert len(db_def.tables) == 1
        assert db_def.tables[0].name == "users"
        assert len(db_def.tables[0].columns) == 2
        assert db_def.projectMetadata.database.name == "test_db"

    def test_table_count_matches_entity_count(self):
        entities = [
            {"name": "users", "columns": [{"name": "id", "type": "BIGINT"}]},
            {"name": "orders", "columns": [{"name": "id", "type": "BIGINT"}]},
            {"name": "products", "columns": [{"name": "id", "type": "BIGINT"}]},
        ]
        bundle = self._make_bundle(entities)
        db_def = reconstruct_database_definition(bundle)

        assert len(db_def.tables) == len(entities)

    def test_relationships_attached_to_correct_table(self):
        entities = [
            {"name": "users", "columns": [{"name": "id", "type": "BIGINT"}]},
            {"name": "orders", "columns": [{"name": "id", "type": "BIGINT"}]},
        ]
        relationships = [
            {
                "sourceTable": "orders",
                "type": "ManyToOne",
                "targetTable": "users",
                "foreignKey": "user_id",
                "joinTable": None,
            }
        ]
        bundle = self._make_bundle(entities, relationships)
        db_def = reconstruct_database_definition(bundle)

        users_table = next(t for t in db_def.tables if t.name == "users")
        orders_table = next(t for t in db_def.tables if t.name == "orders")

        assert len(users_table.relationships) == 0
        assert len(orders_table.relationships) == 1
        assert orders_table.relationships[0].targetTable == "users"

    def test_passes_pydantic_validation(self):
        entities = [
            {"name": "users", "columns": [{"name": "id", "type": "BIGINT"}]},
        ]
        bundle = self._make_bundle(entities)
        db_def = reconstruct_database_definition(bundle)

        # Pydantic validation happens in the constructor; if we get here it passed
        assert db_def.projectMetadata.name == "test_app"
        assert db_def.projectMetadata.artifactId == "test-app"

    def test_empty_relationships(self):
        entities = [
            {"name": "users", "columns": [{"name": "id", "type": "BIGINT"}]},
        ]
        bundle = self._make_bundle(entities, relationships=[])
        db_def = reconstruct_database_definition(bundle)

        assert db_def.tables[0].relationships == []
