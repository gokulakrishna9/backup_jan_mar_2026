"""Smoke tests for CRUDManager."""

import shutil
from pathlib import Path

import pytest

from app_def_manager.scaffolder import Scaffolder
from app_def_manager.crud import CRUDManager


@pytest.fixture
def crud_app(tmp_path, monkeypatch):
    """Scaffold a test app and return a CRUDManager for it."""
    monkeypatch.chdir(tmp_path)
    s = Scaffolder()
    s.scaffold_application("test_app", [
        {"name": "User", "fields": [
            {"name": "email", "type": "String"},
            {"name": "age", "type": "Integer"},
        ]},
    ], force=True)
    return CRUDManager("test_app")


class TestAddEntity:
    def test_add_entity_returns_6_dirty_files(self, crud_app):
        dirty = crud_app.add_entity("Product", [
            {"name": "title", "type": "String"},
            {"name": "price", "type": "BigDecimal"},
        ])
        assert len(dirty) == 6

    def test_add_entity_appears_in_entity_layer(self, crud_app):
        crud_app.add_entity("Product", [{"name": "title", "type": "String"}])
        el = crud_app.editor.get("webflux_entity_layer.json", "entities")
        names = [e["className"] for e in el]
        assert "Product" in names
        assert "User" in names

    def test_add_entity_appears_in_entities(self, crud_app):
        crud_app.add_entity("Product", [{"name": "title", "type": "String"}])
        ents = crud_app.editor.get("webflux_entities.json", "entities")
        tnames = [e["name"] for e in ents]
        assert "product" in tnames

    def test_add_entity_creates_3_dtos(self, crud_app):
        crud_app.add_entity("Product", [{"name": "title", "type": "String"}])
        dtos = crud_app.editor.get("webflux_dto_layer.json", "dtos")
        product_dtos = [d for d in dtos if d["entityName"] == "Product"]
        assert len(product_dtos) == 3
        dto_types = {d["dtoType"] for d in product_dtos}
        assert dto_types == {"Input", "Output", "Filter"}

    def test_add_entity_creates_repo_service_controller(self, crud_app):
        crud_app.add_entity("Product", [{"name": "title", "type": "String"}])
        repos = crud_app.editor.get("webflux_repository_layer.json", "repositories")
        assert any(r["entityName"] == "Product" for r in repos)
        services = crud_app.editor.get("webflux_service_layer.json", "services")
        assert any(s["entityName"] == "Product" for s in services)
        controllers = crud_app.editor.get("webflux_controller_layer.json", "controllers")
        assert any(c["entityName"] == "Product" for c in controllers)

    def test_duplicate_entity_raises_value_error(self, crud_app):
        with pytest.raises(ValueError, match="already exists"):
            crud_app.add_entity("User", [{"name": "x", "type": "String"}])


class TestRemoveEntity:
    def test_remove_entity_returns_6_dirty_files(self, crud_app):
        dirty = crud_app.remove_entity("User")
        assert len(dirty) == 6

    def test_remove_entity_gone_from_all_layers(self, crud_app):
        crud_app.remove_entity("User")
        el = crud_app.editor.get("webflux_entity_layer.json", "entities")
        assert all(e["className"] != "User" for e in el)
        ents = crud_app.editor.get("webflux_entities.json", "entities")
        assert all(e["name"] != "user" for e in ents)
        dtos = crud_app.editor.get("webflux_dto_layer.json", "dtos")
        assert all(d["entityName"] != "User" for d in dtos)
        repos = crud_app.editor.get("webflux_repository_layer.json", "repositories")
        assert all(r["entityName"] != "User" for r in repos)


class TestFieldOperations:
    def test_add_field(self, crud_app):
        dirty = crud_app.add_field("User", {"name": "nickname", "type": "String"})
        assert len(dirty) == 3
        entity = crud_app.editor.find("webflux_entity_layer.json", "entities", {"className": "User"})
        col_names = [f["columnName"] for f in entity["fields"]]
        assert "nickname" in col_names

    def test_add_field_before_audit_fields(self, crud_app):
        crud_app.add_field("User", {"name": "nickname", "type": "String"})
        entity = crud_app.editor.find("webflux_entity_layer.json", "entities", {"className": "User"})
        col_names = [f["columnName"] for f in entity["fields"]]
        # nickname should come before created_at
        assert col_names.index("nickname") < col_names.index("created_at")

    def test_remove_field(self, crud_app):
        dirty = crud_app.remove_field("User", "email")
        assert len(dirty) == 3
        entity = crud_app.editor.find("webflux_entity_layer.json", "entities", {"className": "User"})
        col_names = [f["columnName"] for f in entity["fields"]]
        assert "email" not in col_names

    def test_modify_field(self, crud_app):
        dirty = crud_app.modify_field("User", "age", {"type": "Long", "isNullable": False})
        assert len(dirty) == 3
        entity = crud_app.editor.find("webflux_entity_layer.json", "entities", {"className": "User"})
        age_field = [f for f in entity["fields"] if f["columnName"] == "age"][0]
        assert age_field["javaType"] == "Long"
        assert age_field["isNullable"] is False


class TestEndpointOperations:
    def test_add_endpoint(self, crud_app):
        dirty = crud_app.add_endpoint("User", {"name": "search", "path": "/search", "method": "GET"})
        assert dirty == ["webflux_controller_layer.json"]

    def test_remove_endpoint(self, crud_app):
        crud_app.add_endpoint("User", {"name": "search", "path": "/search", "method": "GET"})
        dirty = crud_app.remove_endpoint("User", "search")
        assert dirty == ["webflux_controller_layer.json"]


class TestQueryOperations:
    def test_add_query(self, crud_app):
        dirty = crud_app.add_query("User", {"name": "findByEmail", "query": "SELECT ..."})
        assert dirty == ["webflux_repository_layer.json"]

    def test_remove_query(self, crud_app):
        crud_app.add_query("User", {"name": "findByEmail", "query": "SELECT ..."})
        dirty = crud_app.remove_query("User", "findByEmail")
        assert dirty == ["webflux_repository_layer.json"]


class TestRelationshipOperations:
    def test_add_relationship(self, crud_app):
        crud_app.add_entity("Product", [{"name": "title", "type": "String"}])
        dirty = crud_app.add_relationship({"sourceEntity": "Product", "targetEntity": "User", "type": "ManyToOne"})
        assert dirty == ["webflux_relationships.json"]

    def test_remove_relationship(self, crud_app):
        crud_app.add_entity("Product", [{"name": "title", "type": "String"}])
        crud_app.add_relationship({"sourceEntity": "Product", "targetEntity": "User", "type": "ManyToOne"})
        dirty = crud_app.remove_relationship("Product", "User")
        assert dirty == ["webflux_relationships.json"]
        rels = crud_app.editor.get("webflux_relationships.json", "relationships")
        assert len(rels) == 0
