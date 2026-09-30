"""LangChain StructuredTool wrappers for App Def Manager CRUD operations."""

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Input schemas
# ---------------------------------------------------------------------------


class AddEntityInput(BaseModel):
    app: str = Field(description="Application name")
    name: str = Field(description="Entity class name (PascalCase, e.g. 'UserProfile')")
    fields: list[dict] = Field(
        default_factory=list,
        description="List of field dicts, each with 'name' and 'type' (e.g. [{'name':'email','type':'String'}])",
    )


class RemoveEntityInput(BaseModel):
    app: str = Field(description="Application name")
    name: str = Field(description="Entity class name to remove")


class AddFieldInput(BaseModel):
    app: str = Field(description="Application name")
    entity: str = Field(description="Entity class name")
    field: dict = Field(description="Field dict with 'name' and 'type', optional 'fieldWidget', 'language'")


class RemoveFieldInput(BaseModel):
    app: str = Field(description="Application name")
    entity: str = Field(description="Entity class name")
    field_name: str = Field(description="Field name to remove")


class ModifyFieldInput(BaseModel):
    app: str = Field(description="Application name")
    entity: str = Field(description="Entity class name")
    field_name: str = Field(description="Field name to modify")
    updates: dict = Field(description="Dict of updates (e.g. {'type':'Integer','isNullable':false})")


class AddEndpointInput(BaseModel):
    app: str = Field(description="Application name")
    entity: str = Field(description="Entity class name")
    endpoint: dict = Field(description="Endpoint definition dict with 'name', 'path', 'method', etc.")


class RemoveEndpointInput(BaseModel):
    app: str = Field(description="Application name")
    entity: str = Field(description="Entity class name")
    endpoint_name: str = Field(description="Custom endpoint name to remove")


class AddQueryInput(BaseModel):
    app: str = Field(description="Application name")
    entity: str = Field(description="Entity class name")
    query: dict = Field(description="Query definition dict with 'name', 'query', 'returnType', etc.")


class RemoveQueryInput(BaseModel):
    app: str = Field(description="Application name")
    entity: str = Field(description="Entity class name")
    query_name: str = Field(description="Custom query name to remove")


class AddRelationshipInput(BaseModel):
    app: str = Field(description="Application name")
    relationship: dict = Field(
        description="Relationship dict with 'sourceEntity', 'targetEntity', 'type' (e.g. MANY_TO_ONE)",
    )


class RemoveRelationshipInput(BaseModel):
    app: str = Field(description="Application name")
    source: str = Field(description="Source entity class name")
    target: str = Field(description="Target entity class name")


class AppStatusInput(BaseModel):
    app: str = Field(description="Application name")


class ListAppsInput(BaseModel):
    pass


class ListEntitiesInput(BaseModel):
    app: str = Field(description="Application name")


class BulkUpdateInput(BaseModel):
    app: str = Field(description="Application name")
    entities: list[str] = Field(
        default_factory=lambda: ["ALL"],
        description="Entity names to update, or ['ALL'] for all entities",
    )
    updates: dict = Field(description="Key-value pairs to set (e.g. {'hasAuthorization': true, 'roles': 'USER'})")


class DescribeAppInput(BaseModel):
    app: str = Field(description="Application name")
    format: str = Field(default="table", description="Output format: 'table' or 'markdown'")


# ---------------------------------------------------------------------------
# Tool functions — delegate to tool_handler wrappers
# ---------------------------------------------------------------------------


def _run_add_entity(app: str, name: str, fields: list[dict] | None = None) -> str:
    from workspace_web_app.engine.handlers.tool_handler import _add_entity
    return str(_add_entity({"app": app, "name": name, "fields": fields or []}))


def _run_remove_entity(app: str, name: str) -> str:
    from workspace_web_app.engine.handlers.tool_handler import _remove_entity
    return str(_remove_entity({"app": app, "name": name}))


def _run_add_field(app: str, entity: str, field: dict) -> str:
    from workspace_web_app.engine.handlers.tool_handler import _add_field
    return str(_add_field({"app": app, "entity": entity, "field": field}))


def _run_remove_field(app: str, entity: str, field_name: str) -> str:
    from workspace_web_app.engine.handlers.tool_handler import _remove_field
    return str(_remove_field({"app": app, "entity": entity, "field_name": field_name}))


def _run_modify_field(app: str, entity: str, field_name: str, updates: dict) -> str:
    from workspace_web_app.engine.handlers.tool_handler import _modify_field
    return str(_modify_field({"app": app, "entity": entity, "field_name": field_name, "updates": updates}))


def _run_add_endpoint(app: str, entity: str, endpoint: dict) -> str:
    from workspace_web_app.engine.handlers.tool_handler import _add_endpoint
    return str(_add_endpoint({"app": app, "entity": entity, "endpoint": endpoint}))


def _run_remove_endpoint(app: str, entity: str, endpoint_name: str) -> str:
    from workspace_web_app.engine.handlers.tool_handler import _remove_endpoint
    return str(_remove_endpoint({"app": app, "entity": entity, "endpoint_name": endpoint_name}))


def _run_add_query(app: str, entity: str, query: dict) -> str:
    from workspace_web_app.engine.handlers.tool_handler import _add_query
    return str(_add_query({"app": app, "entity": entity, "query": query}))


def _run_remove_query(app: str, entity: str, query_name: str) -> str:
    from workspace_web_app.engine.handlers.tool_handler import _remove_query
    return str(_remove_query({"app": app, "entity": entity, "query_name": query_name}))


def _run_add_relationship(app: str, relationship: dict) -> str:
    from workspace_web_app.engine.handlers.tool_handler import _add_relationship
    return str(_add_relationship({"app": app, "relationship": relationship}))


def _run_remove_relationship(app: str, source: str, target: str) -> str:
    from workspace_web_app.engine.handlers.tool_handler import _remove_relationship
    return str(_remove_relationship({"app": app, "source": source, "target": target}))


def _run_app_status(app: str) -> str:
    from workspace_web_app.engine.handlers.tool_handler import _app_status
    return str(_app_status({"app": app}))


def _run_list_apps() -> str:
    from workspace_web_app.engine.handlers.tool_handler import _list_apps
    return str(_list_apps({}))


def _run_list_entities(app: str) -> str:
    from workspace_web_app.engine.handlers.tool_handler import _list_entities
    return str(_list_entities({"app": app}))


def _run_bulk_update(app: str, entities: list[str] | None = None, updates: dict | None = None) -> str:
    from workspace_web_app.engine.handlers.tool_handler import _bulk_update
    return str(_bulk_update({"app": app, "entities": entities or ["ALL"], "updates": updates or {}}))


def _run_describe_app(app: str, format: str = "table") -> str:
    from workspace_web_app.engine.handlers.tool_handler import _describe_app
    return str(_describe_app({"app": app, "format": format}))


# ---------------------------------------------------------------------------
# StructuredTool instances
# ---------------------------------------------------------------------------

add_entity_tool = StructuredTool.from_function(
    func=_run_add_entity, name="add_entity",
    description="Add a new entity to an application. Creates entries in all 6 definition layers.",
    args_schema=AddEntityInput,
)

remove_entity_tool = StructuredTool.from_function(
    func=_run_remove_entity, name="remove_entity",
    description="Remove an entity from an application across all definition layers.",
    args_schema=RemoveEntityInput,
)

add_field_tool = StructuredTool.from_function(
    func=_run_add_field, name="add_field",
    description="Add a field to an entity. Updates entity layer, entities, and DTO definitions.",
    args_schema=AddFieldInput,
)

remove_field_tool = StructuredTool.from_function(
    func=_run_remove_field, name="remove_field",
    description="Remove a field from an entity across entity layer, entities, and DTO definitions.",
    args_schema=RemoveFieldInput,
)

modify_field_tool = StructuredTool.from_function(
    func=_run_modify_field, name="modify_field",
    description="Modify a field's type, nullability, or widget on an entity.",
    args_schema=ModifyFieldInput,
)

add_endpoint_tool = StructuredTool.from_function(
    func=_run_add_endpoint, name="add_endpoint",
    description="Add a custom REST endpoint to an entity's controller definition.",
    args_schema=AddEndpointInput,
)

remove_endpoint_tool = StructuredTool.from_function(
    func=_run_remove_endpoint, name="remove_endpoint",
    description="Remove a custom endpoint from an entity's controller definition.",
    args_schema=RemoveEndpointInput,
)

add_query_tool = StructuredTool.from_function(
    func=_run_add_query, name="add_query",
    description="Add a custom repository query to an entity.",
    args_schema=AddQueryInput,
)

remove_query_tool = StructuredTool.from_function(
    func=_run_remove_query, name="remove_query",
    description="Remove a custom repository query from an entity.",
    args_schema=RemoveQueryInput,
)

add_relationship_tool = StructuredTool.from_function(
    func=_run_add_relationship, name="add_relationship",
    description="Add a relationship between two entities (e.g. MANY_TO_ONE, ONE_TO_MANY).",
    args_schema=AddRelationshipInput,
)

remove_relationship_tool = StructuredTool.from_function(
    func=_run_remove_relationship, name="remove_relationship",
    description="Remove a relationship between two entities.",
    args_schema=RemoveRelationshipInput,
)

app_status_tool = StructuredTool.from_function(
    func=_run_app_status, name="app_status",
    description="Get dirty/clean file status for an application. Shows which definition files have changed since last generation.",
    args_schema=AppStatusInput,
)

list_apps_tool = StructuredTool.from_function(
    func=_run_list_apps, name="list_apps",
    description="List all application definitions in the workspace.",
    args_schema=ListAppsInput,
)

list_entities_tool = StructuredTool.from_function(
    func=_run_list_entities, name="list_entities",
    description="List all entities in an application with class name, table name, and field count.",
    args_schema=ListEntitiesInput,
)

bulk_update_tool = StructuredTool.from_function(
    func=_run_bulk_update, name="bulk_update",
    description="Bulk-update entity-level flags (hasAuthorization, singleRecordPerUser, roles, etc.) across service/repository/controller layers.",
    args_schema=BulkUpdateInput,
)

describe_app_tool = StructuredTool.from_function(
    func=_run_describe_app, name="describe_app",
    description="Get a rich formatted description of an application's entities, fields, relationships, and configuration.",
    args_schema=DescribeAppInput,
)


def get_tools() -> list[StructuredTool]:
    return [
        add_entity_tool, remove_entity_tool,
        add_field_tool, remove_field_tool, modify_field_tool,
        add_endpoint_tool, remove_endpoint_tool,
        add_query_tool, remove_query_tool,
        add_relationship_tool, remove_relationship_tool,
        app_status_tool, list_apps_tool, list_entities_tool,
        bulk_update_tool, describe_app_tool,
    ]
