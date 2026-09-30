"""Pydantic models for parsed swfaw application definition files (Phase 1 input).

These models mirror the JSON structure of the 18 application definition files
produced by swfaw_v2 Phase 1. They are read-only input models for REAW Phase 1.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# ─── Manifest ───────────────────────────────────────────────────────────────

class ManifestStatistics(BaseModel):
    total_entities: int = 0
    total_relationships: int = 0
    total_columns: int = 0


class ManifestDef(BaseModel):
    version: str = ""
    format: str = "split"
    description: str = ""
    files: Dict[str, str] = {}
    statistics: Optional[ManifestStatistics] = None


# ─── Project Metadata ───────────────────────────────────────────────────────

class DatabaseConfig(BaseModel):
    type: str = "mysql"
    host: str = "localhost"
    port: int = 3306
    name: str = ""
    url: Optional[str] = None
    username: str = "root"
    password: str = "password"


class ProjectMetadataInner(BaseModel):
    name: str = ""
    applicationName: str = ""
    groupId: str = "com.example"
    artifactId: str = ""
    version: str = "1.0.0"
    port: int = 8080
    sqlFileName: str = ""
    dateCreated: str = ""
    database: Optional[DatabaseConfig] = None


class ProjectMetadataDef(BaseModel):
    projectMetadata: ProjectMetadataInner


# ─── Entities ───────────────────────────────────────────────────────────────

class ColumnDef(BaseModel):
    name: str
    type: str
    primaryKey: bool = False
    nullable: bool = True
    foreignKey: Optional[Any] = None
    unique: bool = False
    defaultValue: Optional[Any] = None


class EntityDef(BaseModel):
    name: str
    columns: List[ColumnDef] = []


class EntitiesDef(BaseModel):
    entities: List[EntityDef] = []


# ─── Relationships ──────────────────────────────────────────────────────────

class RelationshipDef(BaseModel):
    type: str = ""  # OneToMany, ManyToOne, ManyToMany
    sourceTable: str = ""
    targetTable: str = ""
    foreignKey: Optional[str] = None
    joinTable: Optional[str] = None


class RelationshipsDef(BaseModel):
    relationships: List[RelationshipDef] = []


# ─── Entity Layer ───────────────────────────────────────────────────────────

class EntityFieldDef(BaseModel):
    columnName: str = ""
    fieldName: str = ""
    javaType: str = ""
    isPrimaryKey: bool = False
    isNullable: bool = True
    columnDefinition: str = ""


class EntityLayerEntry(BaseModel):
    tableName: str = ""
    className: str = ""
    packageName: str = ""
    fields: List[EntityFieldDef] = []
    isRootEntity: bool = False
    parentEntity: Optional[str] = None
    hasPublicFlag: bool = False
    hasAuditFields: bool = True
    hasSoftDelete: bool = True


class EntityLayerDef(BaseModel):
    layerType: str = "entity"
    description: str = ""
    entities: List[EntityLayerEntry] = []


# ─── Repository Layer ───────────────────────────────────────────────────────

class RepositoryLayerEntry(BaseModel):
    entityName: str = ""
    className: str = ""
    packageName: str = ""
    idType: str = "Long"
    hasCustomQueries: bool = False
    customQueries: List[Any] = []
    hasSoftDelete: bool = False
    hasAuthorization: bool = False
    enableCaching: bool = False
    cacheNames: List[str] = []


class RepositoryLayerDef(BaseModel):
    layerType: str = "repository"
    description: str = ""
    note: str = ""
    repositories: List[RepositoryLayerEntry] = []


# ─── Service Layer ──────────────────────────────────────────────────────────

class ServiceLayerEntry(BaseModel):
    entityName: str = ""
    className: str = ""
    packageName: str = ""
    repositoryName: str = ""
    isRootEntity: bool = False
    hasAuthorization: bool = False
    authorizationConfig: Optional[Dict[str, Any]] = None
    transactionManagement: Optional[Dict[str, Any]] = None
    customMethods: List[Any] = []
    validationRules: Optional[Dict[str, Any]] = None


class ServiceLayerDef(BaseModel):
    layerType: str = "service"
    description: str = ""
    services: List[ServiceLayerEntry] = []


# ─── Controller Layer ───────────────────────────────────────────────────────

class EndpointDef(BaseModel):
    enabled: bool = True
    path: str = ""
    method: str = "GET"
    requiresAuth: bool = True
    roles: List[str] = []
    rateLimitPerMinute: int = 60
    supportsPagination: bool = False
    supportsFiltering: bool = False
    supportsSorting: bool = False


class ControllerLayerEntry(BaseModel):
    entityName: str = ""
    className: str = ""
    packageName: str = ""
    serviceName: str = ""
    basePath: str = ""
    isRootEntity: bool = False
    endpoints: Dict[str, EndpointDef] = {}
    customEndpoints: List[Any] = []
    corsConfig: Optional[Dict[str, Any]] = None


class ControllerLayerDef(BaseModel):
    layerType: str = "controller"
    description: str = ""
    controllers: List[ControllerLayerEntry] = []


# ─── DTO Layer ──────────────────────────────────────────────────────────────

class ValidationDef(BaseModel):
    required: bool = False
    requiredMessage: Optional[str] = None
    maxLength: Optional[int] = None
    maxLengthMessage: Optional[str] = None
    email: bool = False
    emailMessage: Optional[str] = None
    minLength: Optional[int] = None
    minLengthMessage: Optional[str] = None
    pattern: Optional[str] = None
    patternMessage: Optional[str] = None


class DtoFieldDef(BaseModel):
    fieldName: str = ""
    javaType: str = ""
    includeInDTO: bool = True
    validation: Optional[ValidationDef] = None
    filterType: Optional[str] = None
    format: Optional[str] = None
    fieldWidget: Optional[str] = None
    language: Optional[str] = None


class DtoLayerEntry(BaseModel):
    entityName: str = ""
    dtoType: str = ""  # Input, Output, Filter
    className: str = ""
    packageName: str = ""
    fields: List[DtoFieldDef] = []
    excludeSensitiveFields: List[str] = []
    includeRelationships: bool = False
    customValidators: List[Any] = []


class DtoLayerDef(BaseModel):
    layerType: str = "dto"
    description: str = ""
    dtos: List[DtoLayerEntry] = []


# ─── Query Layer ────────────────────────────────────────────────────────────

class QueryParameterDef(BaseModel):
    name: str = ""
    type: str = ""
    required: bool = True
    defaultValue: Optional[str] = None


class QueryJoinDef(BaseModel):
    type: str = ""  # INNER, LEFT, RIGHT, FULL
    table: str = ""
    alias: Optional[str] = None
    on: str = ""


class CustomQueryDef(BaseModel):
    name: str = ""
    description: str = ""
    returnType: str = ""
    select: List[str] = []
    from_: str = Field("", alias="from")
    joins: List[QueryJoinDef] = []
    where: List[str] = []
    groupBy: List[str] = []
    having: List[str] = []
    orderBy: List[str] = []
    pagination: bool = True
    parameters: List[QueryParameterDef] = []
    authorization: Optional[Dict[str, Any]] = None

    model_config = {"populate_by_name": True}


class QueryLayerDef(BaseModel):
    layerType: str = "query"
    description: str = ""
    version: str = ""
    queries: Dict[str, List[CustomQueryDef]] = {}


# ─── Filter Layer ───────────────────────────────────────────────────────────

class FilterFieldDef(BaseModel):
    name: str = ""
    type: str = ""
    operators: List[str] = []


class FilterEntityDef(BaseModel):
    fields: List[FilterFieldDef] = []


class FilterLayerDef(BaseModel):
    layerType: str = "filter"
    description: str = ""
    version: str = ""
    filters: Dict[str, FilterEntityDef] = {}


# ─── Security Layer ─────────────────────────────────────────────────────────

class RefreshTokenConfig(BaseModel):
    enabled: bool = False
    expiration: int = 604800000
    expirationUnit: str = "milliseconds"


class JwtConfig(BaseModel):
    enabled: bool = True
    secret: str = ""
    expiration: int = 86400000
    expirationUnit: str = "milliseconds"
    issuer: str = ""
    audience: str = ""
    algorithm: str = "HS256"
    refreshToken: Optional[RefreshTokenConfig] = None


class OAuth2ProviderDef(BaseModel):
    name: str = ""
    clientId: str = ""
    clientSecret: str = ""
    redirectUri: str = ""
    scope: List[str] = []


class OAuth2Config(BaseModel):
    enabled: bool = False
    providers: List[OAuth2ProviderDef] = []


class SecurityLayerDef(BaseModel):
    layerType: str = "security"
    description: str = ""
    jwt: Optional[JwtConfig] = None
    oauth2: Optional[OAuth2Config] = None
    passwordPolicy: Optional[Dict[str, Any]] = None
    sessionManagement: Optional[Dict[str, Any]] = None
    cors: Optional[Dict[str, Any]] = None
    publicEndpoints: List[str] = []


# ─── Config Layer ───────────────────────────────────────────────────────────

class ConfigLayerDef(BaseModel):
    layerType: str = "config"
    description: str = ""
    project: Optional[Dict[str, Any]] = None
    server: Optional[Dict[str, Any]] = None
    database: Optional[Dict[str, Any]] = None
    logging: Optional[Dict[str, Any]] = None
    features: Optional[Dict[str, Any]] = None


# ─── Exception Layer ────────────────────────────────────────────────────────

class CustomExceptionDef(BaseModel):
    className: str = ""
    packageName: str = ""
    httpStatus: int = 500
    defaultMessage: str = ""
    includeTimestamp: bool = True
    includeStackTrace: bool = False
    includeFieldErrors: bool = False


class ExceptionLayerDef(BaseModel):
    layerType: str = "exception"
    description: str = ""
    customExceptions: List[CustomExceptionDef] = []
    globalExceptionHandler: Optional[Dict[str, Any]] = None


# ─── Authorization Layer ────────────────────────────────────────────────────

class AccessControlDef(BaseModel):
    name: str = ""
    description: str = ""
    enabled: bool = True


class AuthorizationLayerDef(BaseModel):
    layerType: str = "authorization"
    description: str = ""
    enabled: bool = False
    accessControlModel: str = "document-based"
    accessControls: List[AccessControlDef] = []
    documentGroupTypes: List[Dict[str, Any]] = []


# ─── Audit Logging Layer ───────────────────────────────────────────────────

class AuditLayerDef(BaseModel):
    layerType: str = "auditLogging"
    description: str = ""
    enabled: bool = True
    auditEvents: Optional[Dict[str, Any]] = None
    retentionPolicy: Optional[Dict[str, Any]] = None


# ─── Group Definition Layer ─────────────────────────────────────────────────

class SystemGroupDef(BaseModel):
    groupName: str = ""
    description: str = ""
    isSuperGroup: bool = False
    isDefaultGroup: bool = False
    autoAssignToNewUsers: bool = False


class GroupDefinitionLayerDef(BaseModel):
    layerType: str = "group_definition"
    description: str = ""
    version: str = ""
    groupManagement: Optional[Dict[str, Any]] = None
    ownerEnrollmentDefaults: Optional[Dict[str, Any]] = None
    systemGroups: List[SystemGroupDef] = []
    tableAccessGroups: List[Dict[str, Any]] = []


# ─── Custom Queries Layer ──────────────────────────────────────────────────

class CustomQueriesLayerDef(BaseModel):
    layerType: str = "custom_queries"
    description: str = ""
    queries: List[Dict[str, Any]] = []


# ─── Root Container ────────────────────────────────────────────────────────

class AppDefinition(BaseModel):
    """Root container for all parsed swfaw application definition files."""
    manifest: ManifestDef
    project_metadata: ProjectMetadataDef
    entities: EntitiesDef
    relationships: RelationshipsDef
    entity_layer: EntityLayerDef
    repository_layer: RepositoryLayerDef
    service_layer: ServiceLayerDef
    controller_layer: ControllerLayerDef
    dto_layer: DtoLayerDef
    query_layer: QueryLayerDef
    filter_layer: FilterLayerDef
    security_layer: SecurityLayerDef
    config_layer: ConfigLayerDef
    exception_layer: ExceptionLayerDef
    authorization_layer: AuthorizationLayerDef
    audit_layer: AuditLayerDef
    group_definition_layer: GroupDefinitionLayerDef
    custom_queries_layer: Optional[CustomQueriesLayerDef] = None
