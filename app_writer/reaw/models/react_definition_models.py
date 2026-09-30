"""Pydantic models for the React Application Definition JSON files.

These models represent the intermediate JSON artifact produced by REAW Phase 1
and consumed by REAW Phase 2. They are user-editable between phases.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel


# ─── Manifest ───────────────────────────────────────────────────────────────

class ManifestEntry(BaseModel):
    path: str
    concern: str


class ReactManifest(BaseModel):
    version: str = "1.0.0"
    files: List[ManifestEntry] = []


# ─── Routes ─────────────────────────────────────────────────────────────────

class RouteDefinition(BaseModel):
    path: str
    pageComponent: str
    pageType: str  # entity, filter, query
    pageFolder: str = ""  # entitys, filters, queries — actual folder name
    entityName: str
    navLabel: str
    navGroup: str
    requiresAuth: bool = True


# ─── Form Groupings ────────────────────────────────────────────────────────

class FormGroupTab(BaseModel):
    entityName: str
    tabLabel: str
    tabOrder: int
    included: bool = True


class FormGrouping(BaseModel):
    groupName: str
    parentEntity: str
    tabs: List[FormGroupTab] = []


# ─── Component Mappings ─────────────────────────────────────────────────────

class ValidationConfig(BaseModel):
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


class FieldMapping(BaseModel):
    fieldName: str
    fieldLabel: str = ""
    componentType: str  # InputText, InputNumber, Calendar, Checkbox, etc.
    javaType: str
    columnDefinition: str = ""
    props: Dict[str, Any] = {}
    validation: Optional[ValidationConfig] = None
    isRelationshipField: bool = False
    relatedEntityName: Optional[str] = None
    isMultiSelect: bool = False
    autocompleteDisplayField: Optional[str] = None
    includeInDTO: bool = True


class ComponentMapping(BaseModel):
    entityName: str
    fields: List[FieldMapping] = []
    excludeSensitiveFields: List[str] = []
    singleRecordPerUser: bool = False


# ─── Page Definitions ───────────────────────────────────────────────────────

class GridTemplate(BaseModel):
    gridTemplateRows: str
    gridTemplateColumns: str
    gridTemplateAreas: List[str]


class ComponentPlacement(BaseModel):
    componentType: str  # form, dataTable, filterPanel, querySection, chart, componentWrapper, groupedForm
    entityName: str
    gridArea: str
    chartType: Optional[str] = None
    formLayout: Optional["FormLayout"] = None
    formButtons: Optional[List["FormButton"]] = None


class FormLayout(BaseModel):
    """Responsive grid layout for form fields."""
    columnsLg: int = 3   # columns on large screens (≥992px)
    columnsMd: int = 2   # columns on medium screens (≥768px)
    columnsSm: int = 1   # columns on small screens (<768px)
    fullWidthComponentTypes: List[str] = ["InputTextarea"]  # components that span all columns


class FormButton(BaseModel):
    """Button definition for form actions."""
    label: str
    icon: str = ""
    action: str  # submit, cancel, edit, grantAccess, custom
    className: str = ""
    visibleWhen: str = "always"  # always, editMode, viewMode


class PageDefinition(BaseModel):
    pageId: str
    pageType: str  # entity, filter, query
    entityName: str
    gridTemplate: GridTemplate
    componentPlacements: List[ComponentPlacement] = []


# ─── Layout ─────────────────────────────────────────────────────────────────

class LayoutRegion(BaseModel):
    visible: bool = True
    collapsible: bool = True
    defaultCollapsed: bool = False


class NavItem(BaseModel):
    label: str
    path: str


class NavGroup(BaseModel):
    groupName: str
    entities: List[NavItem] = []


class LayoutDefinition(BaseModel):
    applicationName: str = ""
    apiPort: int = 8080
    header: LayoutRegion = LayoutRegion()
    footer: LayoutRegion = LayoutRegion()
    leftNav: LayoutRegion = LayoutRegion()
    content: LayoutRegion = LayoutRegion(collapsible=False)
    navGroups: List[NavGroup] = []


# ─── Auth Config ────────────────────────────────────────────────────────────

class AuthConfig(BaseModel):
    jwtEnabled: bool = True
    oauth2Enabled: bool = False
    oauth2Providers: List[str] = []
    refreshTokenEnabled: bool = False
    protectedRoutes: List[str] = []
    permissionsEndpoint: str = "/api/auth/permissions"
    loginEndpoint: str = "/api/auth/login"
    registerEndpoint: str = "/api/auth/register"
    registerEnabled: bool = True


# ─── API Services ───────────────────────────────────────────────────────────

class ApiEndpointDef(BaseModel):
    enabled: bool = True
    method: str = "GET"
    supportsPagination: bool = False
    supportsFiltering: bool = False
    supportsSorting: bool = False


class ApiServiceDefinition(BaseModel):
    entityName: str
    basePath: str
    endpoints: Dict[str, ApiEndpointDef] = {}


# ─── Redux Store ────────────────────────────────────────────────────────────

class StateShapeDef(BaseModel):
    listState: bool = True
    singleItemState: bool = True
    mutationState: bool = True


class PaginationStateDef(BaseModel):
    currentPage: int = 0
    pageSize: int = 20
    totalCount: int = 0


class ReduxStoreDefinition(BaseModel):
    entityName: str
    pkField: str = "id"
    thunks: Dict[str, bool] = {}
    stateShape: StateShapeDef = StateShapeDef()
    pagination: Optional[PaginationStateDef] = None


# ─── Theme ──────────────────────────────────────────────────────────────────

class AnimationEffectDef(BaseModel):
    type: str = "fade"  # fade, outline, scale, background-shift
    intensity: str = "subtle"  # subtle, mild, moderate


class AnimationStyleDef(BaseModel):
    transitionDuration: str = "200ms"
    easingFunction: str = "ease-out"
    hover: AnimationEffectDef = AnimationEffectDef(type="background-shift", intensity="subtle")
    focus: AnimationEffectDef = AnimationEffectDef(type="outline", intensity="mild")
    click: AnimationEffectDef = AnimationEffectDef(type="scale", intensity="subtle")
    selection: AnimationEffectDef = AnimationEffectDef(type="fade", intensity="mild")


class TypographyDef(BaseModel):
    fontFamily: str = "Inter, system-ui, sans-serif"
    fontSize: str = "16px"
    fontSizeSmall: str = "14px"
    fontSizeLarge: str = "20px"
    headingFontFamily: Optional[str] = None  # falls back to fontFamily
    headingFontWeight: str = "600"
    lineHeight: str = "1.5"


class SpacingDef(BaseModel):
    unit: str = "8px"
    small: str = "4px"
    medium: str = "8px"
    large: str = "16px"
    xlarge: str = "24px"


class BordersDef(BaseModel):
    radius: str = "6px"
    radiusLarge: str = "12px"
    width: str = "1px"
    color: str = "#dee2e6"


class ShadowsDef(BaseModel):
    small: str = "0 1px 2px rgba(0,0,0,0.05)"
    medium: str = "0 4px 6px rgba(0,0,0,0.1)"
    large: str = "0 10px 15px rgba(0,0,0,0.1)"


class ComponentTokensDef(BaseModel):
    """Per-component overrides scraped from a target site."""
    button: Dict[str, str] = {}
    input: Dict[str, str] = {}
    card: Dict[str, str] = {}
    table: Dict[str, str] = {}
    sidebar: Dict[str, str] = {}


class ThemeSourceDef(BaseModel):
    """Provenance metadata when theme was scraped from a website."""
    url: str = ""
    scrapedAt: str = ""


class ThemeDefinition(BaseModel):
    colorPalette: Dict[str, str] = {}
    typography: TypographyDef = TypographyDef()
    spacing: SpacingDef = SpacingDef()
    borders: BordersDef = BordersDef()
    shadows: ShadowsDef = ShadowsDef()
    components: ComponentTokensDef = ComponentTokensDef()
    animationsEnabled: bool = True
    animationStyle: AnimationStyleDef = AnimationStyleDef()
    source: ThemeSourceDef = ThemeSourceDef()


# ─── Charts ─────────────────────────────────────────────────────────────────

class ChartTypeDef(BaseModel):
    typeId: str
    enabled: bool = True
    defaultOption: Dict[str, Any] = {}


class ChartMappingRule(BaseModel):
    ruleId: str
    chartType: str
    conditions: Dict[str, Any] = {}
    priority: int = 50


class ChartsDefinition(BaseModel):
    chartTypes: List[ChartTypeDef] = []
    mappingRules: List[ChartMappingRule] = []


# ─── Env Config ─────────────────────────────────────────────────────────────

class EnvVariable(BaseModel):
    key: str
    value: str
    comment: str = ""


class EnvDefinition(BaseModel):
    variables: List[EnvVariable] = []


# ─── Root Container ────────────────────────────────────────────────────────

class ReactAppDefinition(BaseModel):
    """Container for all parsed React Application Definition files."""
    manifest: ReactManifest = ReactManifest()
    routes: List[RouteDefinition] = []
    form_groupings: List[FormGrouping] = []
    component_mappings: List[ComponentMapping] = []
    page_definitions: List[PageDefinition] = []
    layout: LayoutDefinition = LayoutDefinition()
    auth_config: AuthConfig = AuthConfig()
    api_services: List[ApiServiceDefinition] = []
    redux_store: List[ReduxStoreDefinition] = []
    theme: ThemeDefinition = ThemeDefinition()
    charts: ChartsDefinition = ChartsDefinition()
    env_config: EnvDefinition = EnvDefinition()
    react_ai_config: Optional[Dict[str, Any]] = None
