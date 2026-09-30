"""Database definition models for input JSON."""

from typing import List, Optional
from pydantic import BaseModel


class DatabaseConfig(BaseModel):
    """Database configuration."""
    type: str = "mysql"
    host: str = "localhost"
    port: int = 3306
    name: str
    url: Optional[str] = None  # Full JDBC URL (optional, can be constructed from host/port/name)
    username: str = "root"
    password: str = "password"


class ProjectMetadata(BaseModel):
    """Project metadata."""
    name: str
    applicationName: str  # Display name for the application
    groupId: str = "com.example"
    artifactId: str
    version: str = "1.0.0"
    port: int = 8081
    sqlFileName: Optional[str] = None  # Original SQL file name if generated from SQL
    dateCreated: Optional[str] = None  # ISO format date string (YYYY-MM-DD)
    database: DatabaseConfig


class Column(BaseModel):
    """Database column definition."""
    name: str
    type: str
    primaryKey: bool = False
    nullable: bool = True
    foreignKey: Optional[dict] = None
    unique: bool = False
    defaultValue: Optional[str] = None


class Relationship(BaseModel):
    """Entity relationship definition."""
    type: str  # OneToMany, ManyToOne, ManyToMany
    targetTable: str
    foreignKey: Optional[str] = None
    joinTable: Optional[str] = None


class Table(BaseModel):
    """Database table definition."""
    name: str
    columns: List[Column]
    relationships: List[Relationship] = []


class DatabaseDefinition(BaseModel):
    """Complete database definition."""
    projectMetadata: ProjectMetadata
    tables: List[Table]
