# REAW — React Application Writer — Complete Reference

## 1. Overview

REAW (React Application Writer) is a Python code generator that produces complete, production-ready React applications from swfaw application definitions. It reads the same `application_definitions/` folder that swfaw writes and generates a full React frontend alongside the Java backend.

### Two-Phase Architecture

| Phase | Input | Output |
|-------|-------|--------|
| Phase 1 | swfaw `webflux_*.json` definitions → `AppDefinition` | 12 `react_*.json` definition files + manifest |
| Phase 2 | `react_*.json` definitions → `ReactAppDefinition` | Complete React application source code |

The intermediate `react_*.json` files are user-editable between phases, allowing manual customization of routes, layouts, themes, and component mappings before code generation.

### Tech Stack (Generated Application)

| Concern | Library |
|---------|---------|
| UI Framework | React (JSX) |
| Build Tool | Vite |
| Component Library | PrimeReact |
| State Management | Redux Toolkit |
| HTTP Client | Axios |
| Routing | React Router |
| Forms | react-hook-form |
| Charts | Chart.js (via PrimeReact) |

### Integration with swfaw

REAW reads the same `application_definitions/` folder that swfaw produces. The typical workflow:

1. swfaw generates `webflux_*.json` definitions (Phase 1) + Java code (Phase 2)
2. REAW reads those definitions → generates `react_*.json` (Phase 1) + React code (Phase 2)
3. Both outputs live side-by-side: `webflux_app/` + `react_app/`

> **Important:** swfaw and REAW have conflicting module names — always invoke REAW via subprocess, never import directly.

---

## 2. Entry Points & Scripts

### 2.1 `generate_react_app.py` — Unified Phase 1 + Phase 2

Runs both phases sequentially. This is the primary entry point.

```bash
py reaw/generate_react_app.py --input <application_definitions_path> --output <target_directory>
```

| Argument | Required | Description |
|----------|----------|-------------|
| `--input` | Yes | Path to swfaw `application_definitions/` directory |
| `--output` | No | Target output directory. Default: `../generated_application/<db_name>_<timestamp>` |

**Behavior:**
1. Parses swfaw definitions via `DefinitionParser.parse()`
2. Runs Phase 1 via `ReactDefinitionGenerator.generate()` → writes `react_*.json` to `<output>/application_definitions/`
3. Parses React definitions via `ReactDefinitionParser.parse()`
4. Extracts filter/query data from swfaw definitions via `extract_filter_and_query()`
5. Loads AI layer (`webflux_ai_layer.json`) if present
6. Runs Phase 2 via `ReactCodeGenerator.generate()` → writes React app to `<output>/react_app/`

**AI Layer Loading:**
The unified script checks for `webflux_ai_layer.json` in the input directory. If found, it's loaded as a raw dict and passed to Phase 2's `ReactCodeGenerator.generate()` as the `ai_layer` parameter. Invalid JSON is silently skipped with a warning.

### 2.2 `phase1_generate_react_definition.py` — Phase 1 Only

Generates React definition JSON files from swfaw definitions.

```bash
py reaw/phase1_generate_react_definition.py --input <application_definitions_path> [--output <target_directory>]
```

| Argument | Required | Description |
|----------|----------|-------------|
| `--input` | Yes | Path to swfaw `application_definitions/` directory |
| `--output` | No | Target output directory. Default: same as `--input` (writes `react_*.json` alongside `webflux_*.json`) |

### 2.3 `phase2_generate_react_code.py` — Phase 2 Only

Generates React source code from React definition JSON files.

```bash
py reaw/phase2_generate_react_code.py --input <application_definitions_path> [--output <target_directory>]
```

| Argument | Required | Description |
|----------|----------|-------------|
| `--input` | Yes | Path to directory containing `react_*.json` files |
| `--output` | No | Target output directory. Default: `<parent_of_input>/react_app/` |

**Note:** Phase 2 also reads `webflux_filter_layer.json` and `webflux_query_layer.json` from the same directory for filter/query component generation.

---

## 3. Generation Pipeline

### 3.1 Phase 1: swfaw Definitions → React Definitions

```
application_definitions/
  webflux_manifest.json
  webflux_entities.json
  webflux_relationships.json
  webflux_entity_layer.json
  webflux_dto_layer.json
  webflux_controller_layer.json
  webflux_service_layer.json
  webflux_repository_layer.json
  webflux_query_layer.json
  webflux_filter_layer.json
  webflux_security_layer.json
  webflux_config_layer.json
  webflux_exception_layer.json
  webflux_authorization_layer.json
  webflux_audit_logging_layer.json
  webflux_group_definition_layer.json
  [webflux_custom_queries_layer.json]
  [webflux_ai_layer.json]
        │
        ▼  DefinitionParser.parse()
  AppDefinition (Pydantic model)
        │
        ▼  ReactDefinitionGenerator.generate()
  react_manifest.json
  react_routes.json
  react_form_groupings.json
  react_component_mappings.json
  react_page_definitions.json
  react_layout.json
  react_auth_config.json
  react_api_services.json
  react_redux_store.json
  react_theme.json
  react_charts.json
  react_env.json
```

**Generator execution order (dependency-aware):**
1. `RouteGenerator` (independent)
2. `FormGroupingGenerator` (independent, but output needed by step 4)
3. `ComponentMappingGenerator` (independent)
4. `PageDefinitionGenerator` (depends on form groupings from step 2)
5. `LayoutGenerator` (independent)
6. `AuthConfigGenerator` (independent)
7. `ApiServicesGenerator` (independent, but output needed by step 8)
8. `ReduxStoreGenerator` (depends on API services from step 7)
9. `ThemeGenerator` (independent, no app_def input)
10. `ChartsGenerator` (independent, no app_def input)
11. `EnvGenerator` (independent)
12. `ManifestGenerator` (last — indexes all generated files)

### 3.2 Phase 2: React Definitions → React Source Code

```
react_*.json files
        │
        ▼  ReactDefinitionParser.parse()
  ReactAppDefinition (Pydantic model)
        │
        ▼  ReactCodeGenerator.generate()
  react_app/
    ├── package.json, vite.config.js, .env, index.html
    ├── src/
    │   ├── main.jsx, App.jsx
    │   ├── styles/          (theme CSS)
    │   ├── services/        (apiClient + per-entity services)
    │   ├── store/           (Redux store + per-entity slices)
    │   ├── components/
    │   │   ├── wrappers/    (PrimeReact wrappers)
    │   │   ├── entities/    (per-entity Form, DataTable, FilterPanel, QuerySection)
    │   │   ├── widgets/     (QuillEditor, MonacoEditor, etc.)
    │   │   ├── charts/      (BaseChart + type wrappers)
    │   │   └── ai/          (AI components, if enabled)
    │   ├── pages/           (per-entity pages + filter/query pages)
    │   ├── auth/            (LoginPage, RegisterPage, AuthContext, ProtectedRoute)
    │   ├── hooks/           (usePermissions)
    │   ├── layout/          (AppLayout.jsx + AppLayout.css)
    │   ├── utils/           (logger, chartMappingEngine)
    │   └── config/          (aiNavEntries, if AI enabled)
    └── ...
```

**Phase 2 generator execution order (17 generators):**

| # | Generator | Output |
|---|-----------|--------|
| 1 | `Phase2ThemeGenerator` | `src/styles/theme-variables.css`, `primereact-theme-overrides.css` |
| 2 | `ScaffoldGenerator` | `package.json`, `vite.config.js`, `.env`, `index.html`, `src/main.jsx`, `src/App.jsx`, `src/utils/logger.js`, `DashboardPage.jsx` |
| 3 | `ApiServiceGenerator` | `src/services/apiClient.js` + per-entity `<entity>Service.js` |
| 4 | `ReduxGenerator` | `src/store/store.js`, `src/store/index.js` + per-entity `<entity>Slice.js` |
| 5 | `ComponentWrapperGenerator` | 10 PrimeReact wrapper files in `src/components/wrappers/` |
| 6 | `AuthGenerator` | `src/auth/LoginPage.jsx`, `RegisterPage.jsx`, `AuthContext.jsx`, `ProtectedRoute.jsx` |
| 7 | `PermissionGenerator` | `src/hooks/usePermissions.js` |
| 8 | `ChartGenerator` | `src/components/charts/BaseChart.jsx`, per-type wrappers, `chartRegistry.js`, `src/utils/chartMappingEngine.js` |
| 8.5 | `WidgetGenerator` | `src/components/widgets/` (only for used widget types) |
| 9 | `EntityComponentGenerator` | Per-entity `<Entity>Form.jsx` + `<Entity>DataTable.jsx` |
| 10 | `FilterComponentGenerator` | Per-entity `<Entity>FilterPanel.jsx` |
| 11 | `QueryComponentGenerator` | Per-entity `<Entity>QuerySection.jsx` |
| 12 | `GroupedFormGenerator` | Per-parent `<Entity>GroupedForm.jsx` |
| 13 | `EntityPageGenerator` | Per-entity `<Entity>Page.jsx` |
| 14 | `FilterPageGenerator` | Per-entity `<Entity>FilterPage.jsx` |
| 15 | `QueryPageGenerator` | Per-entity `<Entity>QueryPage.jsx` |
| 16 | `GridLayoutGenerator` | `src/layout/AppLayout.jsx` + `AppLayout.css` |
| 17 | `AiReactGenerator` | AI components (conditional — only when `react_ai_config` + `ai_layer` present) |

### 3.3 Filter/Query Data Extraction

The `extract_filter_and_query()` utility (`reaw/utils/filter_query_extractor.py`) reads swfaw definitions directly:

- **Filter data:** Reads `webflux_filter_layer.json` → extracts `filters` dict → returns `Dict[entityName, List[filterFieldDict]]`
- **Query data:** Reads `webflux_query_layer.json` → extracts `queries` dict → returns `Dict[entityName, List[queryDict]]`

This data is passed to Phase 2's `FilterComponentGenerator` and `QueryComponentGenerator` to produce per-entity filter panels and query sections.

### 3.4 AI React Component Generation

When `webflux_ai_layer.json` exists in the input directory AND `react_ai_config.json` is present in the React definitions:

1. The unified script loads `webflux_ai_layer.json` as a raw dict
2. `ReactDefinitionParser` loads `react_ai_config.json` (concern: `"ai_config"`) as a raw dict on `ReactAppDefinition.react_ai_config`
3. Phase 2's `ReactCodeGenerator` passes both to `AiReactGenerator.generate()`
4. AI components are generated using Python `string.Template` (not Jinja2) to avoid `{{ }}` conflicts with JSX

---

## 4. Data Models

### 4.1 Input Models (`reaw/models/definition_models.py`)

These Pydantic models mirror the JSON structure of swfaw's 18 application definition files. They are read-only input for REAW Phase 1.

#### `AppDefinition` — Root Container

```python
class AppDefinition(BaseModel):
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
```

#### Layer Definition Models

| Model | Key Fields |
|-------|------------|
| `ManifestDef` | `version`, `format`, `description`, `files: Dict[str, str]`, `statistics: ManifestStatistics` |
| `ManifestStatistics` | `total_entities`, `total_relationships`, `total_columns` |
| `ProjectMetadataDef` | `projectMetadata: ProjectMetadataInner` |
| `ProjectMetadataInner` | `name`, `applicationName`, `groupId`, `artifactId`, `version`, `port`, `sqlFileName`, `dateCreated`, `database: DatabaseConfig` |
| `DatabaseConfig` | `type`, `host`, `port`, `name`, `url`, `username`, `password` |
| `EntitiesDef` | `entities: List[EntityDef]` |
| `EntityDef` | `name`, `columns: List[ColumnDef]` |
| `ColumnDef` | `name`, `type`, `primaryKey`, `nullable`, `foreignKey`, `unique`, `defaultValue` |
| `RelationshipsDef` | `relationships: List[RelationshipDef]` |
| `RelationshipDef` | `type` (OneToMany/ManyToOne/ManyToMany), `sourceTable`, `targetTable`, `foreignKey`, `joinTable` |
| `EntityLayerDef` | `layerType`, `description`, `entities: List[EntityLayerEntry]` |
| `EntityLayerEntry` | `tableName`, `className`, `packageName`, `fields: List[EntityFieldDef]`, `isRootEntity`, `parentEntity`, `hasPublicFlag`, `hasAuditFields`, `hasSoftDelete` |
| `EntityFieldDef` | `columnName`, `fieldName`, `javaType`, `isPrimaryKey`, `isNullable`, `columnDefinition` |
| `RepositoryLayerDef` | `layerType`, `description`, `note`, `repositories: List[RepositoryLayerEntry]` |
| `RepositoryLayerEntry` | `entityName`, `className`, `packageName`, `idType`, `hasCustomQueries`, `customQueries`, `hasSoftDelete`, `hasAuthorization`, `enableCaching`, `cacheNames` |
| `ServiceLayerDef` | `layerType`, `description`, `services: List[ServiceLayerEntry]` |
| `ServiceLayerEntry` | `entityName`, `className`, `packageName`, `repositoryName`, `isRootEntity`, `hasAuthorization`, `authorizationConfig`, `transactionManagement`, `customMethods`, `validationRules` |
| `ControllerLayerDef` | `layerType`, `description`, `controllers: List[ControllerLayerEntry]` |
| `ControllerLayerEntry` | `entityName`, `className`, `packageName`, `serviceName`, `basePath`, `isRootEntity`, `endpoints: Dict[str, EndpointDef]`, `customEndpoints`, `corsConfig` |
| `EndpointDef` | `enabled`, `path`, `method`, `requiresAuth`, `roles`, `rateLimitPerMinute`, `supportsPagination`, `supportsFiltering`, `supportsSorting` |
| `DtoLayerDef` | `layerType`, `description`, `dtos: List[DtoLayerEntry]` |
| `DtoLayerEntry` | `entityName`, `dtoType` (Input/Output/Filter), `className`, `packageName`, `fields: List[DtoFieldDef]`, `excludeSensitiveFields`, `includeRelationships`, `customValidators` |
| `DtoFieldDef` | `fieldName`, `javaType`, `includeInDTO`, `validation: ValidationDef`, `filterType`, `format`, `fieldWidget`, `language` |
| `ValidationDef` | `required`, `requiredMessage`, `maxLength`, `maxLengthMessage`, `email`, `emailMessage`, `minLength`, `minLengthMessage`, `pattern`, `patternMessage` |
| `QueryLayerDef` | `layerType`, `description`, `version`, `queries: Dict[str, List[CustomQueryDef]]` |
| `CustomQueryDef` | `name`, `description`, `returnType`, `select`, `from_` (alias: "from"), `joins: List[QueryJoinDef]`, `where`, `groupBy`, `having`, `orderBy`, `pagination`, `parameters: List[QueryParameterDef]`, `authorization` |
| `QueryParameterDef` | `name`, `type`, `required`, `defaultValue` |
| `QueryJoinDef` | `type` (INNER/LEFT/RIGHT/FULL), `table`, `alias`, `on` |
| `FilterLayerDef` | `layerType`, `description`, `version`, `filters: Dict[str, FilterEntityDef]` |
| `FilterEntityDef` | `fields: List[FilterFieldDef]` |
| `FilterFieldDef` | `name`, `type`, `operators: List[str]` |
| `SecurityLayerDef` | `layerType`, `description`, `jwt: JwtConfig`, `oauth2: OAuth2Config`, `passwordPolicy`, `sessionManagement`, `cors`, `publicEndpoints` |
| `JwtConfig` | `enabled`, `secret`, `expiration`, `expirationUnit`, `issuer`, `audience`, `algorithm`, `refreshToken: RefreshTokenConfig` |
| `RefreshTokenConfig` | `enabled`, `expiration`, `expirationUnit` |
| `OAuth2Config` | `enabled`, `providers: List[OAuth2ProviderDef]` |
| `OAuth2ProviderDef` | `name`, `clientId`, `clientSecret`, `redirectUri`, `scope` |
| `ConfigLayerDef` | `layerType`, `description`, `project`, `server`, `database`, `logging`, `features` |
| `ExceptionLayerDef` | `layerType`, `description`, `customExceptions: List[CustomExceptionDef]`, `globalExceptionHandler` |
| `CustomExceptionDef` | `className`, `packageName`, `httpStatus`, `defaultMessage`, `includeTimestamp`, `includeStackTrace`, `includeFieldErrors` |
| `AuthorizationLayerDef` | `layerType`, `description`, `enabled`, `accessControlModel`, `accessControls: List[AccessControlDef]`, `documentGroupTypes` |
| `AccessControlDef` | `name`, `description`, `enabled` |
| `AuditLayerDef` | `layerType`, `description`, `enabled`, `auditEvents`, `retentionPolicy` |
| `GroupDefinitionLayerDef` | `layerType`, `description`, `version`, `groupManagement`, `ownerEnrollmentDefaults`, `systemGroups: List[SystemGroupDef]`, `tableAccessGroups` |
| `SystemGroupDef` | `groupName`, `description`, `isSuperGroup`, `isDefaultGroup`, `autoAssignToNewUsers` |
| `CustomQueriesLayerDef` | `layerType`, `description`, `queries: List[Dict]` |


### 4.2 React Definition Models (`reaw/models/react_definition_models.py`)

These Pydantic models represent the intermediate JSON artifact produced by Phase 1 and consumed by Phase 2. They are user-editable between phases.

#### `ReactAppDefinition` — Root Container

```python
class ReactAppDefinition(BaseModel):
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
```

#### Manifest Models

| Model | Fields |
|-------|--------|
| `ReactManifest` | `version: str = "1.0.0"`, `files: List[ManifestEntry]` |
| `ManifestEntry` | `path: str`, `concern: str` |

#### `RouteDefinition`

| Field | Type | Description |
|-------|------|-------------|
| `path` | `str` | URL path (e.g., `/users`) |
| `pageComponent` | `str` | Component name (e.g., `UserPage`) |
| `pageType` | `str` | `entity`, `filter`, or `query` |
| `pageFolder` | `str` | Folder name (e.g., `entitys`, `filters`, `queries`) |
| `entityName` | `str` | Associated entity name |
| `navLabel` | `str` | Navigation menu label |
| `navGroup` | `str` | Navigation group name |
| `requiresAuth` | `bool` | Whether route requires authentication (default: `True`) |

#### `FormGrouping`

| Field | Type | Description |
|-------|------|-------------|
| `groupName` | `str` | Group identifier |
| `parentEntity` | `str` | Parent entity name |
| `tabs` | `List[FormGroupTab]` | Tab definitions |

#### `FormGroupTab`

| Field | Type | Description |
|-------|------|-------------|
| `entityName` | `str` | Entity for this tab |
| `tabLabel` | `str` | Display label |
| `tabOrder` | `int` | Sort order |
| `included` | `bool` | Whether tab is included (default: `True`) |

#### `ComponentMapping`

| Field | Type | Description |
|-------|------|-------------|
| `entityName` | `str` | Entity name |
| `fields` | `List[FieldMapping]` | Field-to-component mappings |
| `excludeSensitiveFields` | `List[str]` | Fields to exclude from display |
| `singleRecordPerUser` | `bool` | Whether entity has one record per user |

#### `FieldMapping`

| Field | Type | Description |
|-------|------|-------------|
| `fieldName` | `str` | Field identifier |
| `fieldLabel` | `str` | Display label |
| `componentType` | `str` | PrimeReact component (e.g., `InputText`, `Calendar`, `AutoComplete`) |
| `javaType` | `str` | Java type from entity layer |
| `columnDefinition` | `str` | SQL column definition |
| `props` | `Dict[str, Any]` | Additional component props |
| `validation` | `Optional[ValidationConfig]` | Validation rules |
| `isRelationshipField` | `bool` | Whether this is a FK field |
| `relatedEntityName` | `Optional[str]` | Related entity for FK fields |
| `isMultiSelect` | `bool` | Whether FK allows multiple selection |
| `autocompleteDisplayField` | `Optional[str]` | Display field for AutoComplete |
| `includeInDTO` | `bool` | Whether field is in DTO |

#### `ValidationConfig`

| Field | Type | Description |
|-------|------|-------------|
| `required` | `bool` | Field is required |
| `requiredMessage` | `Optional[str]` | Custom required message |
| `maxLength` | `Optional[int]` | Maximum length |
| `maxLengthMessage` | `Optional[str]` | Custom max length message |
| `email` | `bool` | Email validation |
| `emailMessage` | `Optional[str]` | Custom email message |
| `minLength` | `Optional[int]` | Minimum length |
| `minLengthMessage` | `Optional[str]` | Custom min length message |
| `pattern` | `Optional[str]` | Regex pattern |
| `patternMessage` | `Optional[str]` | Custom pattern message |

#### Page Definition Models

| Model | Fields |
|-------|--------|
| `PageDefinition` | `pageId`, `pageType` (entity/filter/query), `entityName`, `gridTemplate: GridTemplate`, `componentPlacements: List[ComponentPlacement]` |
| `GridTemplate` | `gridTemplateRows: str`, `gridTemplateColumns: str`, `gridTemplateAreas: List[str]` |
| `ComponentPlacement` | `componentType` (form/dataTable/filterPanel/querySection/chart/componentWrapper/groupedForm), `entityName`, `gridArea`, `chartType`, `formLayout: FormLayout`, `formButtons: List[FormButton]` |
| `FormLayout` | `columnsLg: int = 3`, `columnsMd: int = 2`, `columnsSm: int = 1`, `fullWidthComponentTypes: List[str]` |
| `FormButton` | `label`, `icon`, `action` (submit/cancel/edit/grantAccess/custom), `className`, `visibleWhen` (always/editMode/viewMode) |

#### `LayoutDefinition`

| Field | Type | Description |
|-------|------|-------------|
| `applicationName` | `str` | App display name |
| `apiPort` | `int` | Backend API port (default: 8080) |
| `header` | `LayoutRegion` | Header config |
| `footer` | `LayoutRegion` | Footer config |
| `leftNav` | `LayoutRegion` | Left navigation config |
| `content` | `LayoutRegion` | Content area config |
| `navGroups` | `List[NavGroup]` | Navigation groups |

| Model | Fields |
|-------|--------|
| `LayoutRegion` | `visible: bool`, `collapsible: bool`, `defaultCollapsed: bool` |
| `NavGroup` | `groupName: str`, `entities: List[NavItem]` |
| `NavItem` | `label: str`, `path: str` |

#### `AuthConfig`

| Field | Type | Default |
|-------|------|---------|
| `jwtEnabled` | `bool` | `True` |
| `oauth2Enabled` | `bool` | `False` |
| `oauth2Providers` | `List[str]` | `[]` |
| `refreshTokenEnabled` | `bool` | `False` |
| `protectedRoutes` | `List[str]` | `[]` |
| `permissionsEndpoint` | `str` | `/api/auth/permissions` |
| `loginEndpoint` | `str` | `/api/auth/login` |
| `registerEndpoint` | `str` | `/api/auth/register` |
| `registerEnabled` | `bool` | `True` |

#### `ApiServiceDefinition`

| Field | Type | Description |
|-------|------|-------------|
| `entityName` | `str` | Entity name |
| `basePath` | `str` | API base path (e.g., `/api/users`) |
| `endpoints` | `Dict[str, ApiEndpointDef]` | Endpoint definitions keyed by operation name |

| Model | Fields |
|-------|--------|
| `ApiEndpointDef` | `enabled: bool`, `method: str`, `supportsPagination: bool`, `supportsFiltering: bool`, `supportsSorting: bool` |

#### `ReduxStoreDefinition`

| Field | Type | Description |
|-------|------|-------------|
| `entityName` | `str` | Entity name |
| `pkField` | `str` | Primary key field (default: `"id"`) |
| `thunks` | `Dict[str, bool]` | Thunk operations (e.g., `{"fetchAll": true, "create": true}`) |
| `stateShape` | `StateShapeDef` | State shape config |
| `pagination` | `Optional[PaginationStateDef]` | Pagination config |

| Model | Fields |
|-------|--------|
| `StateShapeDef` | `listState: bool`, `singleItemState: bool`, `mutationState: bool` |
| `PaginationStateDef` | `currentPage: int = 0`, `pageSize: int = 20`, `totalCount: int = 0` |

#### `ThemeDefinition`

| Field | Type | Description |
|-------|------|-------------|
| `colorPalette` | `Dict[str, str]` | Color name → hex value |
| `typography` | `TypographyDef` | Font settings |
| `spacing` | `SpacingDef` | Spacing tokens |
| `borders` | `BordersDef` | Border tokens |
| `shadows` | `ShadowsDef` | Shadow tokens |
| `components` | `ComponentTokensDef` | Per-component overrides |
| `animationsEnabled` | `bool` | Enable animations (default: `True`) |
| `animationStyle` | `AnimationStyleDef` | Animation configuration |
| `source` | `ThemeSourceDef` | Provenance metadata (scraped URL, timestamp) |

| Model | Fields |
|-------|--------|
| `TypographyDef` | `fontFamily`, `fontSize`, `fontSizeSmall`, `fontSizeLarge`, `headingFontFamily`, `headingFontWeight`, `lineHeight` |
| `SpacingDef` | `unit`, `small`, `medium`, `large`, `xlarge` |
| `BordersDef` | `radius`, `radiusLarge`, `width`, `color` |
| `ShadowsDef` | `small`, `medium`, `large` |
| `ComponentTokensDef` | `button: Dict`, `input: Dict`, `card: Dict`, `table: Dict`, `sidebar: Dict` |
| `AnimationStyleDef` | `transitionDuration`, `easingFunction`, `hover: AnimationEffectDef`, `focus: AnimationEffectDef`, `click: AnimationEffectDef`, `selection: AnimationEffectDef` |
| `AnimationEffectDef` | `type` (fade/outline/scale/background-shift), `intensity` (subtle/mild/moderate) |
| `ThemeSourceDef` | `url: str`, `scrapedAt: str` |

#### `ChartsDefinition`

| Field | Type | Description |
|-------|------|-------------|
| `chartTypes` | `List[ChartTypeDef]` | Available chart types |
| `mappingRules` | `List[ChartMappingRule]` | Auto-mapping rules |

| Model | Fields |
|-------|--------|
| `ChartTypeDef` | `typeId`, `enabled`, `defaultOption: Dict` |
| `ChartMappingRule` | `ruleId`, `chartType`, `conditions: Dict`, `priority: int` |

#### `EnvDefinition`

| Field | Type | Description |
|-------|------|-------------|
| `variables` | `List[EnvVariable]` | Environment variables |

| Model | Fields |
|-------|--------|
| `EnvVariable` | `key: str`, `value: str`, `comment: str` |

test


---

## 5. Parsers

### 5.1 DefinitionParser (`reaw/parsers/definition_parser.py`)

Reads swfaw `webflux_*.json` files from the `application_definitions/` directory and produces an `AppDefinition` Pydantic model.

**Layer mapping (`_LAYER_MAP`)** — maps manifest keys to `(PydanticModelClass, is_required)`:

| Manifest Key | Model Class | Required |
|-------------|-------------|----------|
| `project_metadata` | `ProjectMetadataDef` | Yes |
| `entities` | `EntitiesDef` | Yes |
| `relationships` | `RelationshipsDef` | Yes |
| `entity_layer` | `EntityLayerDef` | Yes |
| `repository_layer` | `RepositoryLayerDef` | Yes |
| `service_layer` | `ServiceLayerDef` | Yes |
| `controller_layer` | `ControllerLayerDef` | Yes |
| `dto_layer` | `DtoLayerDef` | Yes |
| `query_layer` | `QueryLayerDef` | Yes |
| `filter_layer` | `FilterLayerDef` | Yes |
| `group_definition_layer` | `GroupDefinitionLayerDef` | Yes |

**Extra layers (`_EXTRA_LAYERS`)** — loaded from disk even if not listed in manifest:

| Attribute | Model Class | Default Filename |
|-----------|-------------|-----------------|
| `security_layer` | `SecurityLayerDef` | `webflux_security_layer.json` |
| `config_layer` | `ConfigLayerDef` | `webflux_config_layer.json` |
| `exception_layer` | `ExceptionLayerDef` | `webflux_exception_layer.json` |
| `authorization_layer` | `AuthorizationLayerDef` | `webflux_authorization_layer.json` |
| `audit_layer` | `AuditLayerDef` | `webflux_audit_logging_layer.json` |
| `custom_queries_layer` | `CustomQueriesLayerDef` | `webflux_custom_queries_layer.json` |

**Parse flow:**
1. Read `webflux_manifest.json`
2. Parse all files listed in manifest via `_LAYER_MAP` (raise `DefinitionParseError` if required layer missing)
3. Parse extra layers from disk (use empty defaults if file not found)
4. Return populated `AppDefinition`

**Error handling:** `DefinitionParseError` with `file_name` and `location` attributes. Raised on missing files, malformed JSON, or validation errors.

### 5.2 ReactDefinitionParser (`reaw/parsers/react_definition_parser.py`)

Reads `react_*.json` files from the `application_definitions/` directory and produces a `ReactAppDefinition` Pydantic model.

**Concern mapping (`_CONCERN_MAP`)** — maps manifest concern names to `(ModelClass, field_name, is_list)`:

| Concern | Model Class | Field on ReactAppDefinition | Is List |
|---------|-------------|----------------------------|---------|
| `routing` | `RouteDefinition` | `routes` | Yes |
| `form_groupings` | `FormGrouping` | `form_groupings` | Yes |
| `component_mappings` | `ComponentMapping` | `component_mappings` | Yes |
| `page_definitions` | `PageDefinition` | `page_definitions` | Yes |
| `layout` | `LayoutDefinition` | `layout` | No |
| `authentication` | `AuthConfig` | `auth_config` | No |
| `api_services` | `ApiServiceDefinition` | `api_services` | Yes |
| `redux_store` | `ReduxStoreDefinition` | `redux_store` | Yes |
| `theme` | `ThemeDefinition` | `theme` | No |
| `charts` | `ChartsDefinition` | `charts` | No |
| `env_config` | `EnvDefinition` | `env_config` | No |

**AI config** is loaded separately (concern: `"ai_config"`) as a raw dict (not a Pydantic model) onto `ReactAppDefinition.react_ai_config`. Schema version validation requires `schemaVersion: "1.0"` — raises `ValueError` if missing or unsupported.

**Parse flow:**
1. Read `react_manifest.json` → `ReactManifest`
2. Track listed files; parse each referenced file by concern
3. For `ai_config` concern: load as raw dict, validate schemaVersion
4. For all other concerns: validate via `_CONCERN_MAP` Pydantic models; list concerns merge with existing (supports split files)
5. Per-entity page file support: scan `pages/` subdirectory for additional `PageDefinition` JSON files
6. Warn about unlisted files in directory
7. Build `ReactAppDefinition`
8. Validate cross-references

**Cross-reference validation (`_validate_cross_references`):**
- Grid area names: every `componentPlacement.gridArea` must exist in the page's `gridTemplateAreas`
- Entity references: every `page.entityName` must be referenced in at least one other definition file (routes, component mappings, API services, or redux store)
- Form grouping entity references: every `tab.entityName` in form groupings must exist in known entities

**Error handling:** `ReactDefinitionParseError` with `file_name`, `error_location`, and `invalid_reference` attributes.

---

## 6. Phase 1 Generators

`ReactDefinitionGenerator` (`reaw/generators/phase1/react_definition_generator.py`) orchestrates 12 generators in dependency order. Each generator reads from the parsed `AppDefinition` and writes a `react_*.json` file.

**Execution order:**

| # | Generator | Output File | Input Dependencies |
|---|-----------|------------|-------------------|
| 1 | `RouteGenerator` | `react_routes.json` | `controller_layer`, `filter_layer`, `query_layer` |
| 2 | `FormGroupingGenerator` | `react_form_groupings.json` | `relationships`, `entity_layer` |
| 3 | `ComponentMappingGenerator` | `react_component_mappings.json` | `dto_layer`, `relationships`, `entity_layer` |
| 4 | `PageDefinitionGenerator` | `react_page_definitions.json` | `entity_layer`, `filter_layer`, `query_layer`, form groupings (from step 2) |
| 5 | `LayoutGenerator` | `react_layout.json` | `project_metadata`, `controller_layer` |
| 6 | `AuthConfigGenerator` | `react_auth_config.json` | `security_layer` |
| 7 | `ApiServicesGenerator` | `react_api_services.json` | `controller_layer` |
| 8 | `ReduxStoreGenerator` | `react_redux_store.json` | API services (from step 7), `entity_layer` |
| 9 | `ThemeGenerator` | `react_theme.json` | None (default theme tokens) |
| 10 | `ChartsGenerator` | `react_charts.json` | None (default chart config) |
| 11 | `EnvGenerator` | `react_env.json` | `project_metadata` |
| 12 | `ManifestGenerator` | `react_manifest.json` | All generated file paths (indexes all files) |

**Dependency chain:** Steps 1–3 are independent. Step 4 depends on step 2 (form groupings). Steps 5–6 are independent. Step 8 depends on step 7 (API services). Steps 9–11 are independent. Step 12 must run last.

The `FormGroupingTransformer` is called between steps 2 and 4 to transform relationship + entity layer data into form grouping structures needed by `PageDefinitionGenerator`.

---

## 7. Phase 2 Generators

`ReactCodeGenerator` (`reaw/generators/phase2/react_code_generator.py`) orchestrates 17 generators that produce the complete React application source code from a parsed `ReactAppDefinition`.

**Execution order:**

| # | Generator | Output |
|---|-----------|--------|
| 1 | `Phase2ThemeGenerator` | CSS variables from theme definition (`src/styles/theme-variables.css`, `primereact-theme-overrides.css`) |
| 2 | `ScaffoldGenerator` | `package.json`, `vite.config.js`, `.env`, `index.html`, `src/main.jsx`, `src/App.jsx`, `src/utils/logger.js`, `DashboardPage.jsx` |
| 3 | `ApiServiceGenerator` | `src/services/apiClient.js` + per-entity `<entity>Service.js` with CRUD methods |
| 4 | `ReduxGenerator` | `src/store/store.js`, `src/store/index.js` + per-entity `<entity>Slice.js` with async thunks |
| 5 | `ComponentWrapperGenerator` | 10 PrimeReact wrapper components in `src/components/wrappers/` |
| 6 | `AuthGenerator` | `src/auth/LoginPage.jsx`, `RegisterPage.jsx`, `AuthContext.jsx`, `ProtectedRoute.jsx` |
| 7 | `PermissionGenerator` | `src/hooks/usePermissions.js` |
| 8 | `ChartGenerator` | `src/components/charts/BaseChart.jsx` + type wrappers + `chartRegistry.js` + `src/utils/chartMappingEngine.js` |
| 8.5 | `WidgetGenerator` | `src/components/widgets/` — only generates files for widget types actually used (scans `component_mappings` for `QuillEditor`, `MonacoEditor`, `MarkdownEditor`, `FileUpload`) |
| 9 | `EntityComponentGenerator` | Per-entity `<Entity>Form.jsx` + `<Entity>DataTable.jsx` in `src/components/entities/<entity>/` |
| 10 | `FilterComponentGenerator` | Per-entity `<Entity>FilterPanel.jsx` |
| 11 | `QueryComponentGenerator` | Per-entity `<Entity>QuerySection.jsx` |
| 12 | `GroupedFormGenerator` | Per-parent `<Entity>GroupedForm.jsx` with tabs |
| 13 | `EntityPageGenerator` | Per-entity `<Entity>Page.jsx` with CSS Grid layout |
| 14 | `FilterPageGenerator` | Per-entity `<Entity>FilterPage.jsx` |
| 15 | `QueryPageGenerator` | Per-entity `<Entity>QueryPage.jsx` |
| 16 | `GridLayoutGenerator` | `src/layout/AppLayout.jsx` + `AppLayout.css` (sidebar nav, header, content area) |
| 17 | `AiReactGenerator` | AI components (conditional — only when `react_ai_config` + `ai_layer` both present) |

**Method signature:**
```python
ReactCodeGenerator.generate(
    react_def: ReactAppDefinition,
    output_dir: str,
    filter_entities: Dict[str, List[Dict]] = None,   # from extract_filter_and_query()
    query_entities: Dict[str, List[Dict]] = None,     # from extract_filter_and_query()
    ai_layer: Dict[str, Any] | None = None,           # raw webflux_ai_layer.json dict
) -> List[str]
```

**AI generation trigger:** Step 17 only runs when `react_def.react_ai_config is not None` AND `ai_layer is not None`. It builds a `react_definitions` dict mapping entity names to their `ComponentMapping` objects, then delegates to `AiReactGenerator.generate()`.

---

## 8. AI React Generator

`AiReactGenerator` (`reaw/generators/ai_react_generator.py`) generates React components from `react_ai_config.json` and `webflux_ai_layer.json`.

### 8.1 Validation (`_validate`)

Two cross-reference checks:

1. **entityFeatures entity names** must exist in React component mappings (`react_definitions` keys). Raises `ValueError` listing available entities if not found.
2. **standaloneFeatures operation names** must exist in `AI_Layer.standaloneOperations` (matched by `name` field). Raises `ValueError` listing available operations if not found.

### 8.2 Generated Components

**Entity-level components** (per entity, in `src/components/ai/`):
- `<Entity>SmartSearchBar.jsx` — AI-powered search with configurable `searchableFields`, calls `aiApiService.entitySearch()`
- `<Entity><Field>GenerationButton.jsx` — Content generation per field, opens dialog with context input, calls `aiApiService.entityGenerate()`
- `<Entity><Field>SuggestionWidget.jsx` — Auto-suggestions per field, triggers on change or blur, calls `aiApiService.entitySuggest()`

**Chat panel** (`src/components/ai/AiChatPanel.jsx`):
- Position variants: `sidebar`, `floating`, `fullpage` (CSS-based)
- SSE streaming support (configurable via `streamingEnabled`)
- Configurable accent color, bubble style (rounded/square), loading animation (spinner/pulse/dots)
- Session management with `sessionId`

**Standalone pages** (in `src/pages/ai/`):
- Chat page (`STANDALONE_CHAT_PAGE`) — full-page chat with session persistence
- Generator page (`STANDALONE_GENERATOR_PAGE`) — prompt → generated output
- Dashboard page (`STANDALONE_DASHBOARD_PAGE`) — query interface with result history table

**RAG admin page** (`src/pages/ai/RagAdminPage.jsx`):
- Source listing with status badges (Indexed/Pending/Disabled)
- Reindex buttons with confirmation dialog
- Document count display

**Evaluation display:**
- `EvaluationScoreBadge.jsx` — score badge with configurable thresholds (`pass`/`warn`), badge styles (`inline`/`tooltip`/`expandable`)
- `EvaluationDashboardPage.jsx` — paginated table of evaluation results with score badges and status

**Document UI** (generated when `ai_layer.documentIngestion.enabled` is true):
- `DocumentUploadPanel.jsx` — file upload with progress bar and error/success messages
- `DocumentListPanel.jsx` — paginated document table with status badges and selection
- `DocumentIngestionPage.jsx` — tabbed page combining upload + document list
- `DocumentTaskPanel.jsx` — run document tasks (summarization, translation, extraction, etc.)
- `DocumentTaskChainBuilder.jsx` — build ordered chains of document tasks

**AI API service** (`src/services/aiApiService.js`):
- Centralized service for all AI endpoints (chat, entity search/generate/suggest, standalone operations, RAG, evaluations, documents)

**Navigation entries** (`src/config/aiNavEntries.js`):
- Auto-generated nav entries for enabled AI sections (chat, standalone features, RAG admin, evaluations, documents)

### 8.3 Template System

Uses Python `string.Template` (`$variable` substitution) for all JSX component templates to avoid conflicts between Jinja2 `{{ }}` delimiters and JavaScript object literals. The only exception is `AI_NAV_ENTRIES`, which uses Jinja2 for its loop construct.

---

## 9. Component Type Mapping

How Java types from the entity layer map to React component types in `ComponentMappingGenerator`:

### 9.1 Standard Field Mappings

| Java Type | Component Type | PrimeReact Component |
|-----------|---------------|---------------------|
| `String` | `InputText` | `InputText` |
| `String` (textarea — via `fieldWidget`) | `InputTextarea` | `InputTextarea` |
| `Integer`, `Long`, `Short` | `InputNumber` | `InputNumber` |
| `BigDecimal`, `Float`, `Double` | `InputNumber` | `InputNumber` (with decimal mode) |
| `Boolean` | `Checkbox` | `Checkbox` |
| `LocalDate` | `Calendar` | `Calendar` (`dateOnly`) |
| `LocalDateTime` | `Calendar` | `Calendar` (`showTime`) |
| `LocalTime` | `Calendar` | `Calendar` (`timeOnly`) |
| FK field (relationship) | `AutoComplete` | `AutoComplete` (with search callback) |

### 9.2 Widget Component Types

Widget types are specified via the `fieldWidget` attribute on `DtoFieldDef`. The `WidgetGenerator` only generates files for widget types actually used in the application.

| Widget Type | Component | File Generated | Use Case |
|-------------|-----------|---------------|----------|
| `QuillEditor` | `QuillEditorWidget` | `QuillEditorWidget.jsx` | Rich text editing (WYSIWYG) |
| `MonacoEditor` | `MonacoEditorWidget` | `MonacoEditorWidget.jsx` | Code editing with syntax highlighting |
| `MarkdownEditor` | `MarkdownEditorWidget` | `MarkdownEditorWidget.jsx` | Markdown editing with preview |
| `FileUpload` | `FileUploadWidget` | `FileUploadWidget.jsx` | File upload |

---

## 10. Generated React Application Structure

```
react_app/
├── package.json
├── vite.config.js
├── .env
├── index.html
└── src/
    ├── main.jsx
    ├── App.jsx
    ├── styles/
    │   ├── theme-variables.css
    │   └── primereact-theme-overrides.css
    ├── services/
    │   ├── apiClient.js
    │   ├── <entity>Service.js              (per entity)
    │   └── aiApiService.js                 (if AI enabled)
    ├── store/
    │   ├── store.js
    │   ├── index.js
    │   └── slices/
    │       └── <entity>Slice.js            (per entity)
    ├── components/
    │   ├── wrappers/                       (10 PrimeReact wrapper components)
    │   ├── entities/
    │   │   └── <entity>/
    │   │       ├── <Entity>Form.jsx
    │   │       └── <Entity>DataTable.jsx
    │   ├── widgets/                        (only for used widget types)
    │   │   ├── QuillEditorWidget.jsx
    │   │   ├── MonacoEditorWidget.jsx
    │   │   ├── MarkdownEditorWidget.jsx
    │   │   └── FileUploadWidget.jsx
    │   ├── charts/
    │   │   ├── BaseChart.jsx
    │   │   ├── <Type>Chart.jsx             (per chart type)
    │   │   └── chartRegistry.js
    │   └── ai/                             (if AI enabled)
    │       ├── AiChatPanel.jsx
    │       ├── <Entity>SmartSearchBar.jsx
    │       ├── <Entity><Field>GenerationButton.jsx
    │       ├── <Entity><Field>SuggestionWidget.jsx
    │       ├── EvaluationScoreBadge.jsx
    │       ├── DocumentUploadPanel.jsx
    │       ├── DocumentListPanel.jsx
    │       ├── DocumentTaskPanel.jsx
    │       └── DocumentTaskChainBuilder.jsx
    ├── pages/
    │   ├── entitys/
    │   │   └── <Entity>Page.jsx            (per entity)
    │   ├── filters/
    │   │   └── <Entity>FilterPage.jsx      (per entity)
    │   ├── queries/
    │   │   └── <Entity>QueryPage.jsx       (per entity)
    │   └── ai/                             (if AI enabled)
    │       ├── <Operation>Page.jsx         (per standalone feature)
    │       ├── RagAdminPage.jsx
    │       ├── EvaluationDashboardPage.jsx
    │       └── DocumentIngestionPage.jsx
    ├── auth/
    │   ├── LoginPage.jsx
    │   ├── RegisterPage.jsx
    │   ├── AuthContext.jsx
    │   └── ProtectedRoute.jsx
    ├── hooks/
    │   └── usePermissions.js
    ├── layout/
    │   ├── AppLayout.jsx
    │   └── AppLayout.css
    ├── utils/
    │   ├── logger.js
    │   └── chartMappingEngine.js
    └── config/
        └── aiNavEntries.js                 (if AI enabled)
```

**Per-entity file count:** ~5 files per entity (service + slice + Form + DataTable + Page). Filter and query entities add `FilterPanel.jsx`, `FilterPage.jsx`, `QuerySection.jsx`, and `QueryPage.jsx` respectively.

---

## 11. Theme System

The theme is defined in `react_theme.json` (Phase 1 output) and consumed by `Phase2ThemeGenerator` to produce CSS custom properties.

### 11.1 Color Palette

CSS custom properties generated from the `colorPalette` dict. Each key becomes `--color-<name>` with the hex value.

### 11.2 Typography

| Token | Description |
|-------|-------------|
| `fontFamily` | Base font family |
| `fontSize` | Default font size |
| `fontSizeSmall` | Small variant |
| `fontSizeLarge` | Large variant |
| `headingFontFamily` | Heading font family |
| `headingFontWeight` | Heading font weight |
| `lineHeight` | Base line height |

### 11.3 Spacing

Unit-based spacing tokens:

| Token | Description |
|-------|-------------|
| `unit` | Base spacing unit |
| `small` | Small spacing |
| `medium` | Medium spacing |
| `large` | Large spacing |
| `xlarge` | Extra-large spacing |

### 11.4 Borders

| Token | Description |
|-------|-------------|
| `radius` | Default border radius |
| `radiusLarge` | Large border radius |
| `width` | Border width |
| `color` | Border color |

### 11.5 Shadows

| Token | Description |
|-------|-------------|
| `small` | Small shadow (subtle elevation) |
| `medium` | Medium shadow |
| `large` | Large shadow (high elevation) |

### 11.6 Animations

| Token | Description |
|-------|-------------|
| `transitionDuration` | Global transition duration |
| `easingFunction` | Global easing function |

Per-interaction animation effects:

| Interaction | Config Fields | Description |
|-------------|--------------|-------------|
| `hover` | `type`, `intensity` | Hover effect |
| `focus` | `type`, `intensity` | Focus effect |
| `click` | `type`, `intensity` | Click effect |
| `selection` | `type`, `intensity` | Selection effect |

Effect types: `fade`, `outline`, `scale`, `background-shift`
Intensity levels: `subtle`, `mild`, `moderate`

### 11.7 Component Tokens

Per-component CSS overrides stored as dicts:

| Component | Key | Description |
|-----------|-----|-------------|
| `button` | `button` | Button component overrides |
| `input` | `input` | Input component overrides |
| `card` | `card` | Card component overrides |
| `table` | `table` | Table component overrides |
| `sidebar` | `sidebar` | Sidebar component overrides |

### 11.8 Theme Scraper Integration

The default `react_theme.json` can be replaced with a scraped theme from any website:

```bash
# Scrape a theme from a target website
py theme_scraper/scrape.py --url https://target-site.com --output <app_definitions_dir>

# Regenerate React code with the new theme
py reaw/phase2_generate_react_code.py --output <output_dir>
```

The scraper extracts colors, typography, spacing, and other design tokens from the target site and writes them into `react_theme.json`, replacing the default theme. The `ThemeSourceDef` model tracks provenance (`url`, `scrapedAt`).

---

## 12. Integration with swfaw

### 12.1 Shared Application Definitions

REAW reads the same `application_definitions/` folder that swfaw writes. Both tools operate on the same directory:

```
application_definitions/
├── webflux_manifest.json          ← swfaw writes
├── webflux_entities.json          ← swfaw writes
├── webflux_*.json                 ← swfaw writes (all layers)
├── react_manifest.json            ← REAW writes (Phase 1)
├── react_routes.json              ← REAW writes (Phase 1)
├── react_*.json                   ← REAW writes (Phase 1)
└── pages/                         ← REAW writes (optional per-entity pages)
```

### 12.2 Filter/Query Extraction

Phase 2 reads swfaw filter and query definitions directly:
- `webflux_filter_layer.json` → `extract_filter_and_query()` → `Dict[entityName, List[filterFieldDict]]`
- `webflux_query_layer.json` → `extract_filter_and_query()` → `Dict[entityName, List[queryDict]]`

This data is passed to `FilterComponentGenerator` and `QueryComponentGenerator`.

### 12.3 AI Layer Passthrough

`webflux_ai_layer.json` is loaded as a raw dict (not parsed into a Pydantic model) and passed directly to `AiReactGenerator`. The AI layer defines backend AI operations; REAW generates the corresponding frontend components.

### 12.4 Side-by-Side Output

Both tools produce output in the same parent directory:

```
generated_application/<app_name>/
├── application_definitions/       ← shared definitions
├── webflux_app/                   ← swfaw output (Java/Spring WebFlux)
├── react_app/                     ← REAW output (React/Vite)
└── schema.sql                     ← swfaw output (database schema)
```

### 12.5 Module Conflict

swfaw and REAW have conflicting module names (both have `models/`, `generators/`, `templates/`, etc.). Always invoke REAW via subprocess — never import REAW modules directly from swfaw or vice versa.

### 12.6 Development Ports

| Service | Port | Tool |
|---------|------|------|
| React dev server (Vite) | 5173 | REAW |
| Backend API (Spring WebFlux) | 8081 | swfaw |

*End of REAW reference document.*