"""Pydantic request models for UI Service endpoints."""

from pydantic import BaseModel, Field


class ScaffoldAppRequest(BaseModel):
    """Request body for scaffolding a new application."""

    name: str = Field(..., description="Application name")
    entities: list[dict] = Field(
        default_factory=list, description="Initial entities to create"
    )


class AddEntityRequest(BaseModel):
    """Request body for adding an entity."""

    name: str = Field(..., description="Entity name")
    fields: list[dict] = Field(
        default_factory=list, description="Entity fields"
    )


class AddFieldRequest(BaseModel):
    """Request body for adding a field to an entity."""

    name: str = Field(..., description="Field name")
    type: str = Field(..., description="Field type")
    nullable: bool = Field(default=True, description="Whether the field is nullable")
    unique: bool = Field(default=False, description="Whether the field is unique")


class ModifyFieldRequest(BaseModel):
    """Request body for modifying a field."""

    updates: dict = Field(..., description="Field properties to update")


class AddRelationshipRequest(BaseModel):
    """Request body for adding a relationship."""

    target_entity: str = Field(..., description="Target entity name")
    type: str = Field(..., description="Relationship type (OneToMany, ManyToOne, etc.)")
    field_name: str = Field(default="", description="Relationship field name")


class AddEndpointRequest(BaseModel):
    """Request body for adding a custom endpoint."""

    name: str = Field(..., description="Endpoint name")
    method: str = Field(default="GET", description="HTTP method")
    path: str = Field(default="", description="Endpoint path")
    description: str = Field(default="", description="Endpoint description")


class AddQueryRequest(BaseModel):
    """Request body for adding a custom query."""

    name: str = Field(..., description="Query name")
    query: str = Field(default="", description="Query string")
    description: str = Field(default="", description="Query description")


class BulkUpdateRequest(BaseModel):
    """Request body for bulk entity updates."""

    entities: list[str] = Field(..., description="Entity names (or ['ALL'])")
    updates: dict = Field(..., description="Key-value pairs to set")


class DefinitionSetRequest(BaseModel):
    """Request body for setting a definition value."""

    path: str = Field(..., description="JSON path within the definition file")
    value: object = Field(..., description="Value to set")


class DatabaseCreateRequest(BaseModel):
    """Request body for creating a database."""

    name: str = Field(..., description="Database name")


class DatabaseQueryRequest(BaseModel):
    """Request body for executing a database query."""

    sql: str = Field(..., description="SQL query to execute")


class AgentChatRequest(BaseModel):
    """Request body for agent chat messages."""

    message: str = Field(..., description="User message")
    app_name: str = Field(default="", description="Target application name")
    session_id: str = Field(default="", description="Browser session ID")


class ToolRequest(BaseModel):
    """Generic request body for miscellaneous tool operations."""

    params: dict = Field(default_factory=dict, description="Tool-specific parameters")


class DiscussionLogRequest(BaseModel):
    """Request body for logging a discussion."""

    content: str = Field(..., description="Discussion content")
    tags: list[str] = Field(default_factory=list, description="Tags")


class DiscussionTaskRequest(BaseModel):
    """Request body for creating a task."""

    title: str = Field(..., description="Task title")
    description: str = Field(default="", description="Task description")


class DiscussionDecisionRequest(BaseModel):
    """Request body for recording a decision."""

    title: str = Field(..., description="Decision title")
    rationale: str = Field(default="", description="Decision rationale")
