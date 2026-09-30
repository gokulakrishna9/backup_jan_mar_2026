"""Layer object definitions for all generators."""

from typing import List, Optional
from pydantic import BaseModel


class Field(BaseModel):
    """Field definition."""
    columnName: str
    fieldName: str
    javaType: str
    isPrimaryKey: bool = False
    isNullable: bool = True
    columnDefinition: str = ""


class EntityLayerObject(BaseModel):
    """Entity layer object for R2DBC entities.
    
    Note: R2DBC does not support JPA relationship annotations (@OneToMany, @ManyToOne, etc.).
    Relationships are tracked separately in relationships.json and handled at the service layer.
    """
    tableName: str
    className: str
    packageName: str
    fields: List[Field]
    isRootEntity: bool
    parentEntity: Optional[str] = None
    hasPublicFlag: bool
    hasAuditFields: bool = True
    hasSoftDelete: bool = True


class DTOLayerObject(BaseModel):
    """DTO layer object with validation configuration."""
    entityName: str
    className: str
    packageName: str
    fields: List[Field]
    dtoType: str  # Input, Output, Filter
    isRootEntity: bool
    fieldConfigs: List[dict] = []  # Field-level configurations (includeInDTO, validation, filterType, format)
    customValidators: List[dict] = []  # Custom validator classes
    excludeSensitiveFields: List[str] = []  # Fields to exclude from Output DTOs
    includeRelationships: bool = False  # Include related entities in Output DTOs


class RepositoryLayerObject(BaseModel):
    """Repository layer object."""
    entityName: str
    className: str
    packageName: str
    idType: str
    hasCustomQueries: bool = False
    customQueries: List[dict] = []
    hasSoftDelete: bool = False
    hasAuthorization: bool = False
    singleRecordPerUser: bool = False
    tableName: Optional[str] = None
    idColumn: Optional[str] = None


class ServiceLayerObject(BaseModel):
    """Service layer object."""
    entityName: str
    className: str
    packageName: str
    repositoryName: str
    isRootEntity: bool
    hasAuthorization: bool
    singleRecordPerUser: bool = False


class ControllerLayerObject(BaseModel):
    """Controller layer object with endpoint configuration."""
    entityName: str
    className: str
    packageName: str
    serviceName: str
    basePath: str
    isRootEntity: bool
    endpoints: dict = {}  # Endpoint configurations (create, getById, getAll, update, delete)
    customEndpoints: List[dict] = []  # Custom endpoint definitions
    corsConfig: dict = {}  # CORS configuration
    singleRecordPerUser: bool = False


class AuthorizationServiceLayerObject(BaseModel):
    """Authorization service layer object."""
    packageName: str
    rootEntities: List[str]


class SecurityConfigLayerObject(BaseModel):
    """Security config layer object."""
    packageName: str
    jwtSecret: str = "your-secret-key-change-in-production"
    jwtExpiration: int = 86400000  # 24 hours


class JWTAuthenticationLayerObject(BaseModel):
    """JWT authentication layer object."""
    packageName: str
    jwtSecret: str = "your-secret-key-change-in-production"
    jwtExpiration: int = 86400000
    refreshExpiration: int = 604800000  # 7 days


class ApplicationConfigLayerObject(BaseModel):
    """Application config layer object."""
    projectName: str
    groupId: str
    artifactId: str
    packageName: str
    port: int
    databaseType: str
    databaseHost: str
    databasePort: int
    databaseName: str


class POMLayerObject(BaseModel):
    """POM layer object."""
    groupId: str
    artifactId: str
    version: str
    projectName: str
    javaVersion: str = "17"
    springBootVersion: str = "3.2.0"


class TestLayerObject(BaseModel):
    """Test layer object."""
    entityName: str
    className: str
    packageName: str
    serviceName: str
    isRootEntity: bool


class QueryParameter(BaseModel):
    """Query parameter definition."""
    name: str
    type: str  # Java type (String, Integer, Boolean, LocalDateTime, etc.)
    required: bool = True
    defaultValue: Optional[str] = None


class QueryJoin(BaseModel):
    """Query join definition."""
    type: str  # INNER, LEFT, RIGHT, FULL
    table: str
    alias: Optional[str] = None
    on: str  # Join condition (e.g., "u.id = ur.user_id")


class CustomQuery(BaseModel):
    """Custom query definition."""
    name: str
    description: str
    returnType: str  # DTO class name for results
    select: List[str]  # SELECT fields
    from_: str  # FROM clause with alias (e.g., "users u")
    joins: List[QueryJoin] = []
    where: List[str] = []  # WHERE conditions
    groupBy: List[str] = []
    having: List[str] = []
    orderBy: List[str] = []
    pagination: bool = True
    parameters: List[QueryParameter] = []
    authorization: dict = {}  # {enabled: bool, documentField: str}
    
    class Config:
        fields = {'from_': 'from'}


class QueryLayerObject(BaseModel):
    """Query layer object for custom queries per entity."""
    entityName: str
    queries: List[CustomQuery] = []
    packageName: str


class FilterField(BaseModel):
    """Filter field definition."""
    name: str
    type: str  # Java type
    operators: List[str] = []  # equals, contains, startsWith, endsWith, greaterThan, lessThan, between, in


class FilterLayerObject(BaseModel):
    """Filter layer object for entity-specific filters."""
    entityName: str
    fields: List[FilterField] = []
    packageName: str
