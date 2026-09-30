"""Pydantic response models for UI Service endpoints."""

from typing import Any

from pydantic import BaseModel, Field


class ToolResponse(BaseModel):
    """Standard response wrapper for tool execution results."""

    success: bool = Field(..., description="Whether the operation succeeded")
    data: Any = Field(default=None, description="Result data")
    error: str | None = Field(default=None, description="Error message if failed")


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = Field(..., description="Service status")
    service: str = Field(..., description="Service name")


class AppListResponse(BaseModel):
    """Response for listing applications."""

    apps: list[dict] = Field(default_factory=list, description="Application list")


class EntityListResponse(BaseModel):
    """Response for listing entities."""

    entities: list[dict] = Field(default_factory=list, description="Entity list")


class JobStatusResponse(BaseModel):
    """Response for job status queries."""

    job_id: str = Field(..., description="Job identifier")
    status: str = Field(..., description="Job status")
    output_lines: list[str] = Field(
        default_factory=list, description="Output lines so far"
    )
