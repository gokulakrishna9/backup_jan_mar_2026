"""Template-ready property objects for Phase 2 Jinja2 templates.

Each property object contains exactly the data a template needs to render
one or more output files. Produced by Phase 2 transformers.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel

from models.react_definition_models import (
    AnimationStyleDef,
    ApiEndpointDef,
    BordersDef,
    ChartMappingRule,
    ComponentPlacement,
    ComponentTokensDef,
    FormButton,
    FormGroupTab,
    FormLayout,
    GridTemplate,
    LayoutRegion,
    NavGroup,
    RouteDefinition,
    ShadowsDef,
    SpacingDef,
    TypographyDef,
    ValidationConfig,
)


# ─── Scaffold ───────────────────────────────────────────────────────────────

class ScaffoldProperties(BaseModel):
    applicationName: str
    apiPort: int
    routes: List[RouteDefinition]
    hasAuth: bool
    widgetDependencies: Dict[str, str] = {}


# ─── Env ────────────────────────────────────────────────────────────────────

class EnvVariableProperties(BaseModel):
    key: str
    value: str
    comment: str = ""


class EnvProperties(BaseModel):
    variables: List[EnvVariableProperties] = []


# ─── API Services ───────────────────────────────────────────────────────────

class ApiServiceProperties(BaseModel):
    entityName: str
    entityNameCamel: str
    basePath: str
    endpoints: Dict[str, ApiEndpointDef]


class ApiClientProperties(BaseModel):
    baseUrl: str
    refreshTokenEnabled: bool = True


# ─── Redux ──────────────────────────────────────────────────────────────────

class ReduxSliceProperties(BaseModel):
    entityName: str
    entityNameCamel: str
    entityNamePascal: str
    pkField: str = "id"
    thunks: Dict[str, bool]
    hasPagination: bool
    pageSize: int = 20


class ReduxStoreProperties(BaseModel):
    entities: List[str]


# ─── Component Wrappers ────────────────────────────────────────────────────

class ComponentWrapperProperties(BaseModel):
    componentName: str
    primeReactComponent: str
    primeReactImport: str


# ─── Entity Components ─────────────────────────────────────────────────────

class FormFieldProperties(BaseModel):
    fieldName: str
    fieldLabel: str
    componentType: str
    javaType: str
    columnDefinition: str = ""
    props: Dict[str, Any] = {}
    validation: Optional[ValidationConfig] = None
    isRelationshipField: bool = False
    relatedEntityName: Optional[str] = None
    isMultiSelect: bool = False
    autocompleteDisplayField: Optional[str] = None


class EntityFormProperties(BaseModel):
    entityName: str
    entityNamePascal: str
    entityNameCamel: str
    basePath: str = ""
    pkField: str = "id"
    fields: List[FormFieldProperties]
    isRootEntity: bool
    hasCreateEndpoint: bool
    hasUpdateEndpoint: bool
    hasDeleteEndpoint: bool
    parentForeignKey: Optional[str] = None
    formLayout: Optional[FormLayout] = None
    formButtons: Optional[List[FormButton]] = None
    singleRecordPerUser: bool = False


class DataTableColumnProperties(BaseModel):
    fieldName: str
    header: str
    sortable: bool
    javaType: str
    fieldWidget: Optional[str] = None


class EntityDataTableProperties(BaseModel):
    entityName: str
    entityNamePascal: str
    entityNameCamel: str
    basePath: str = ""
    pkField: str = "id"
    columns: List[DataTableColumnProperties]
    hasPagination: bool
    hasSorting: bool
    hasViewAction: bool
    hasUpdateAction: bool
    hasDeleteAction: bool


# ─── Entity Pages ──────────────────────────────────────────────────────────

class EntityPageProperties(BaseModel):
    entityName: str
    entityNamePascal: str
    entityNameCamel: str = ""
    pageTitle: str = ""
    pageType: str
    gridTemplate: GridTemplate
    componentPlacements: List[ComponentPlacement]
    isGroupedForm: bool = False
    groupTabs: Optional[List[FormGroupTab]] = None


# ─── Filter ─────────────────────────────────────────────────────────────────

class FilterFieldProperties(BaseModel):
    fieldName: str
    fieldLabel: str
    javaType: str
    operators: List[str]
    componentType: str


class FilterPanelProperties(BaseModel):
    entityName: str
    entityNamePascal: str
    entityNameCamel: str
    filterFields: List[FilterFieldProperties]


# ─── Query ──────────────────────────────────────────────────────────────────

class QueryParameterProperties(BaseModel):
    name: str
    type: str
    required: bool
    componentType: str


class QueryProperties(BaseModel):
    queryName: str
    queryNameCamel: str
    description: str
    parameters: List[QueryParameterProperties]
    hasPagination: bool


class QuerySectionProperties(BaseModel):
    entityName: str
    entityNamePascal: str
    entityNameCamel: str
    queries: List[QueryProperties]


# ─── Grid Layout ────────────────────────────────────────────────────────────

class GridLayoutProperties(BaseModel):
    applicationName: str
    header: LayoutRegion
    footer: LayoutRegion
    leftNav: LayoutRegion
    navGroups: List[NavGroup]


# ─── Auth ───────────────────────────────────────────────────────────────────

class AuthProperties(BaseModel):
    jwtEnabled: bool
    oauth2Enabled: bool
    oauth2Providers: List[str]
    refreshTokenEnabled: bool
    permissionsEndpoint: str
    loginEndpoint: str = "/api/auth/login"
    registerEndpoint: str = "/api/auth/register"
    registerEnabled: bool
    userEntityInputFields: List[FormFieldProperties] = []


# ─── Theme ──────────────────────────────────────────────────────────────────

class ThemeProperties(BaseModel):
    colorPalette: Dict[str, str]
    typography: TypographyDef = TypographyDef()
    spacing: SpacingDef = SpacingDef()
    borders: BordersDef = BordersDef()
    shadows: ShadowsDef = ShadowsDef()
    components: ComponentTokensDef = ComponentTokensDef()
    animationsEnabled: bool
    animationStyle: Optional[AnimationStyleDef] = None


# ─── Charts ─────────────────────────────────────────────────────────────────

class ChartComponentProperties(BaseModel):
    typeId: str
    componentName: str
    defaultOption: Dict[str, Any]


class ChartRegistryProperties(BaseModel):
    chartTypes: List[ChartComponentProperties]


class ChartMappingEngineProperties(BaseModel):
    mappingRules: List[ChartMappingRule]
