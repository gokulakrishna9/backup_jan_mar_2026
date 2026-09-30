
---

## 11. Generated React Application Structure

```
react_app/
├── package.json
├── vite.config.js
├── .env
├── index.html
├── src/
│   ├── main.jsx                          # React entry point
│   ├── App.jsx                           # Root component with Router + Redux Provider
│   │
│   ├── styles/
│   │   ├── theme-variables.css           # CSS custom properties from react_theme.json
│   │   └── primereact-theme-overrides.css # PrimeReact component overrides
│   │
│   ├── auth/
│   │   ├── LoginPage.jsx                 # JWT login form
│   │   ├── RegisterPage.jsx              # User registration form
│   │   ├── AuthContext.jsx               # Auth context provider (token management)
│   │   └── ProtectedRoute.jsx            # Route guard component
│   │
│   ├── hooks/
│   │   └── usePermissions.js             # Permission checking hook
│   │
│   ├── layout/
│   │   ├── AppLayout.jsx                 # CSS Grid app shell (header, sidebar, content, footer)
│   │   └── AppLayout.css                 # Grid layout styles
│   │
│   ├── services/
│   │   ├── apiClient.js                  # Axios instance with interceptors + token refresh
│   │   ├── userService.js                # Per-entity API service (one per entity)
│   │   ├── roleService.js
│   │   ├── ...
│   │   └── aiApiService.js               # AI API service (when AI layer present)
│   │
│   ├── store/
│   │   ├── store.js                      # Redux configureStore
│   │   ├── index.js                      # Store exports
│   │   └── slices/
│   │       ├── userSlice.js              # Per-entity Redux slice (one per entity)
│   │       ├── roleSlice.js
│   │       └── ...
│   │
│   ├── components/
│   │   ├── wrappers/                     # 10 PrimeReact wrapper components
│   │   │   ├── DataTableWrapper.jsx
│   │   │   ├── InputTextWrapper.jsx
│   │   │   ├── InputNumberWrapper.jsx
│   │   │   ├── CalendarWrapper.jsx
│   │   │   ├── DropdownWrapper.jsx
│   │   │   ├── CheckboxWrapper.jsx
│   │   │   ├── InputTextareaWrapper.jsx
│   │   │   ├── ButtonWrapper.jsx
│   │   │   ├── DialogWrapper.jsx
│   │   │   └── ToastWrapper.jsx
│   │   │
│   │   ├── widgets/                      # Shared widget components (only if used)
│   │   │   ├── QuillEditorWidget.jsx
│   │   │   ├── MonacoEditorWidget.jsx
│   │   │   ├── MarkdownEditorWidget.jsx
│   │   │   └── FileUploadWidget.jsx
│   │   │
│   │   ├── charts/
│   │   │   ├── BaseChart.jsx             # Base chart component
│   │   │   ├── BarChart.jsx              # Per-type chart wrappers
│   │   │   ├── LineChart.jsx
│   │   │   ├── PieChart.jsx
│   │   │   └── chartRegistry.js          # Chart type registry
│   │   │
│   │   ├── entities/
│   │   │   ├── user/
│   │   │   │   ├── UserForm.jsx          # Entity form with validation
│   │   │   │   ├── UserDataTable.jsx     # Entity data table with pagination/sorting
│   │   │   │   ├── UserFilterPanel.jsx   # Filter panel (if entity has filters)
│   │   │   │   ├── UserQuerySection.jsx  # Query section (if entity has queries)
│   │   │   │   └── UserGroupedForm.jsx   # Grouped tabbed form (if parent entity)
│   │   │   ├── role/
│   │   │   │   ├── RoleForm.jsx
│   │   │   │   └── RoleDataTable.jsx
│   │   │   └── ...
│   │   │
│   │   └── ai/                           # AI components (when AI layer present)
│   │       ├── AiChatPanel.jsx
│   │       ├── {Entity}SmartSearchBar.jsx
│   │       ├── {Entity}{Field}GenerationButton.jsx
│   │       ├── {Entity}{Field}SuggestionWidget.jsx
│   │       ├── EvaluationScoreBadge.jsx
│   │       ├── DocumentUploadPanel.jsx
│   │       ├── DocumentListPanel.jsx
│   │       ├── DocumentTaskPanel.jsx
│   │       └── DocumentTaskChainBuilder.jsx
│   │
│   ├── pages/
│   │   ├── entitys/                      # Entity pages (folder name from route.pageFolder)
│   │   │   ├── UserPage.jsx              # CSS Grid page with form + table
│   │   │   ├── RolePage.jsx
│   │   │   ├── DashboardPage.jsx         # Dashboard (if dashboard route exists)
│   │   │   └── ...
│   │   │
│   │   ├── filters/
│   │   │   ├── UserFilterPage.jsx
│   │   │   └── ...
│   │   │
│   │   ├── queries/
│   │   │   ├── UserQueryPage.jsx
│   │   │   └── ...
│   │   │
│   │   └── ai/                           # AI pages (when AI layer present)
│   │       ├── {Operation}Page.jsx       # Standalone AI pages
│   │       ├── RagAdminPage.jsx
│   │       ├── EvaluationDashboardPage.jsx
│   │       └── DocumentIngestionPage.jsx
│   │
│   ├── utils/
│   │   ├── logger.js                     # Logging utility
│   │   └── chartMappingEngine.js         # Chart data mapping engine
│   │
│   └── config/
│       └── aiNavEntries.js               # AI navigation entries (when AI layer present)
```

### File Counts (Typical Application)

For an application with N entities:
- Fixed files: ~25 (scaffold, auth, layout, theme, store config, chart base, wrappers)
- Per-entity files: ~5-7 per entity (Form, DataTable, Service, Slice, Page, optional FilterPanel, QuerySection, GroupedForm)
- AI files: ~15-20 (when AI layer is present)
- Total: ~25 + (N * 6) + optional AI files

---

## 12. Component Type Mapping

### Java Type to PrimeReact Component

The `TypeMapper` class (`reaw/utils/type_mapping.py`) maps Java/SQL types to PrimeReact components:

| Java Type | PrimeReact Component | Mode | Import |
|-----------|---------------------|------|--------|
| String | InputText | — | primereact/inputtext |
| VARCHAR | InputText | — | primereact/inputtext |
| Long | InputNumber | decimal | primereact/inputnumber |
| Integer | InputNumber | decimal | primereact/inputnumber |
| int | InputNumber | decimal | primereact/inputnumber |
| BigDecimal | InputNumber | decimal | primereact/inputnumber |
| DECIMAL | InputNumber | decimal | primereact/inputnumber |
| INT | InputNumber | decimal | primereact/inputnumber |
| BIGINT | InputNumber | decimal | primereact/inputnumber |
| Float | InputNumber | decimal | primereact/inputnumber |
| Double | InputNumber | decimal | primereact/inputnumber |
| LocalDate | Calendar | date | primereact/calendar |
| DATE | Calendar | date | primereact/calendar |
| LocalDateTime | Calendar | datetime | primereact/calendar |
| TIMESTAMP | Calendar | datetime | primereact/calendar |
| Boolean | Checkbox | — | primereact/checkbox |
| boolean | Checkbox | — | primereact/checkbox |
| TINYINT(1) | Checkbox | — | primereact/checkbox |
| Byte | Checkbox | — | primereact/checkbox |
| TEXT | InputTextarea | — | primereact/inputtextarea |

### Special Mappings

| Condition | Component | Mode |
|-----------|-----------|------|
| ENUM in column definition | Dropdown | enum |
| ManyToOne / OneToMany FK | AutoComplete | single |
| ManyToMany / link entity FK | AutoComplete | multiple |
| Default fallback | InputText | — |

### fieldWidget Overrides

When a DTO field has `fieldWidget` set, the widget component overrides the standard type mapping:

| fieldWidget Value | Component Type | Extra Props |
|-------------------|---------------|-------------|
| richText | QuillEditor | `{ fieldWidget: "richText" }` |
| codeEditor | MonacoEditor | `{ fieldWidget: "codeEditor", language: "javascript" }` |
| json | MonacoEditor | `{ fieldWidget: "json", language: "json" }` |
| markdown | MarkdownEditor | `{ fieldWidget: "markdown", language: "markdown" }` |

Widget components are only generated if at least one entity uses them (conditional generation in WidgetGenerator).

### Validation Mapping

DTO validation rules map directly to form field validation:

| DTO Validation | React Validation | Behavior |
|---------------|-----------------|----------|
| `required: true` | Required field indicator + message | Form prevents submit |
| `maxLength: N` | Character limit + message | Input constrained |
| `minLength: N` | Minimum length + message | Validation on blur |
| `email: true` | Email format validation + message | Pattern check |
| `pattern: "regex"` | Regex pattern validation + message | Custom pattern |

### Relationship Field Resolution

For AutoComplete fields (FK relationships):
1. `relatedEntityName` identifies the target entity
2. `autocompleteDisplayField` is resolved by finding the first non-ID String field from the related entity's Output DTO
3. Falls back to `"name"` if no suitable field found
4. `isMultiSelect` is true for ManyToMany relationships

---

## 13. Theme System

### Default Color Palette

The default theme uses a soft, muted, pastel-like palette:

| Token | Default Value | Purpose |
|-------|--------------|---------|
| background-primary | #f8f9fa | Main background |
| background-secondary | #ffffff | Card/panel background |
| surface | #f1f3f5 | Surface elements |
| border | #dee2e6 | Border color |
| text-primary | #495057 | Primary text |
| text-secondary | #868e96 | Secondary/muted text |
| accent | #748ffc | Primary accent (buttons, links) |
| accent-hover | #5c7cfa | Accent hover state |
| success | #69db7c | Success indicators |
| warning | #ffd43b | Warning indicators |
| error | #ff8787 | Error indicators |
| info | #74c0fc | Info indicators |

### Typography

| Token | Default | Description |
|-------|---------|-------------|
| fontFamily | Inter, system-ui, sans-serif | Body text font |
| fontSize | 16px | Base font size |
| fontSizeSmall | 14px | Small text |
| fontSizeLarge | 20px | Large text |
| headingFontFamily | null (falls back to fontFamily) | Heading font |
| headingFontWeight | 600 | Heading weight |
| lineHeight | 1.5 | Line height |

### Spacing

| Token | Default | Description |
|-------|---------|-------------|
| unit | 8px | Base spacing unit |
| small | 4px | Small spacing |
| medium | 8px | Medium spacing |
| large | 16px | Large spacing |
| xlarge | 24px | Extra large spacing |

### Borders

| Token | Default | Description |
|-------|---------|-------------|
| radius | 6px | Default border radius |
| radiusLarge | 12px | Large border radius |
| width | 1px | Border width |
| color | #dee2e6 | Border color |

### Shadows

| Token | Default | Description |
|-------|---------|-------------|
| small | 0 1px 2px rgba(0,0,0,0.05) | Subtle shadow |
| medium | 0 4px 6px rgba(0,0,0,0.1) | Card shadow |
| large | 0 10px 15px rgba(0,0,0,0.1) | Modal/overlay shadow |

### Animation Styles

Animations are enabled by default with these settings:

| Property | Default | Description |
|----------|---------|-------------|
| transitionDuration | 200ms | Transition speed |
| easingFunction | ease-out | Easing curve |

| Event | Effect Type | Intensity |
|-------|------------|-----------|
| hover | background-shift | subtle |
| focus | outline | mild |
| click | scale | subtle |
| selection | fade | mild |

Available effect types: `fade`, `outline`, `scale`, `background-shift`
Available intensities: `subtle`, `mild`, `moderate`

### Component Tokens

Per-component style overrides (typically populated by Theme Scraper):

```json
{
  "button": { "borderRadius": "8px", "fontWeight": "600" },
  "input": { "borderColor": "#ced4da", "focusBorderColor": "#748ffc" },
  "card": { "borderRadius": "12px", "shadow": "0 2px 8px rgba(0,0,0,0.08)" },
  "table": { "headerBackground": "#f8f9fa", "stripedBackground": "#fafbfc" },
  "sidebar": { "background": "#1a1a2e", "textColor": "#e0e0e0" }
}
```

### Theme Scraper Integration

The default theme can be replaced with a scraped theme from any website:

```bash
# Scrape a theme and overwrite the default
py theme_scraper/scrape.py --url https://target-site.com --output <app_definitions_dir>

# Regenerate React code with the new theme
py reaw/phase2_generate_react_code.py --input <app_definitions_dir> --output <output_dir>
```

When a theme is scraped, the `source` field records provenance:
```json
{
  "source": {
    "url": "https://target-site.com",
    "scrapedAt": "2025-01-15T10:30:00Z"
  }
}
```

### Generated CSS

Phase 2 produces two CSS files:

1. **theme-variables.css** — CSS custom properties derived from all theme tokens
2. **primereact-theme-overrides.css** — PrimeReact component-specific overrides using the custom properties

---

## Appendix A: Transformers

Each generator has a corresponding transformer that converts definition models into property objects.

### Phase 1 Transformers (`reaw/transformers/phase1/`)

| Transformer | Input | Output |
|------------|-------|--------|
| RouteTransformer | controller_layer, filter_layer, query_layer | List[RouteDefinition] |
| FormGroupingTransformer | relationships, entity_layer | List[FormGrouping] |
| ComponentMappingTransformer | dto_layer, relationships, entity_layer | List[ComponentMapping] |
| PageDefinitionTransformer | entity_layer, filter_layer, query_layer, form_groupings | List[PageDefinition] |
| LayoutTransformer | entity_layer, controller_layer, project_metadata | LayoutDefinition |
| AuthConfigTransformer | security_layer, authorization_layer, controller_layer | AuthConfig |
| ApiServicesTransformer | controller_layer | List[ApiServiceDefinition] |
| ReduxStoreTransformer | api_services, entity_layer | List[ReduxStoreDefinition] |
| ThemeTransformer | (none) | ThemeDefinition |
| ChartsTransformer | (none) | ChartsDefinition |
| EnvTransformer | app_def | EnvDefinition |

### Phase 2 Transformers (`reaw/transformers/phase2/`)

| Transformer | Input | Output |
|------------|-------|--------|
| ScaffoldTransformer | ReactAppDefinition | (ScaffoldProperties, EnvProperties) |
| ApiServiceTransformer | api_services, layout, auth_config | (ApiClientProperties, List[ApiServiceProperties]) |
| ReduxSliceTransformer | redux_store | (ReduxStoreProperties, List[ReduxSliceProperties]) |
| ComponentWrapperTransformer | (none) | List[ComponentWrapperProperties] |
| AuthTransformer | auth_config, component_mappings | AuthProperties |
| PermissionTransformer | auth_config | dict |
| ChartTransformer | charts | (List[ChartComponentProperties], ChartRegistryProperties, ChartMappingEngineProperties) |
| Phase2ThemeTransformer | theme | ThemeProperties |
| EntityComponentTransformer | component_mappings, api_services, form_groupings, redux_store, page_definitions | List[(EntityFormProperties, EntityDataTableProperties)] |
| FilterComponentTransformer | component_mappings, filter_entities | List[FilterPanelProperties] |
| QueryComponentTransformer | query_entities | List[QuerySectionProperties] |
| EntityPageTransformer | page_definitions, form_groupings | List[EntityPageProperties] |
| FilterPageTransformer | page_definitions | List[EntityPageProperties] (pageType=filter) |
| QueryPageTransformer | page_definitions | List[EntityPageProperties] (pageType=query) |
| GridLayoutTransformer | layout | GridLayoutProperties |

---

## Appendix B: Utilities

### String Utilities (`reaw/utils/string_utils.py`)

| Function | Input Example | Output |
|----------|--------------|--------|
| to_camel_case | "user_roles" / "UserRoles" | "userRoles" |
| to_pascal_case | "user_roles" / "userRoles" | "UserRoles" |
| to_snake_case | "UserRoles" / "userRoles" | "user_roles" |
| to_kebab_case | "UserRoles" / "user_roles" | "user-roles" |
| to_display_label | "firstName" / "user_roles" | "First Name" / "User Roles" |

### File Writer (`reaw/utils/file_writer.py`)

Utility for writing files with automatic directory creation.

### Filter/Query Extractor (`reaw/utils/filter_query_extractor.py`)

Reads `webflux_filter_layer.json` and `webflux_query_layer.json` from the application_definitions/ folder and converts them to dict format for Phase 2 generators.

```python
filter_entities, query_entities = extract_filter_and_query(app_def_path)
# filter_entities: Dict[entityName, List[filter_field_dicts]]
# query_entities: Dict[entityName, List[query_dicts]]
```

---

## Appendix C: Running the Generated App

```bash
cd generated_application/my_app/react_app
npm install
npm run dev
# Opens at http://localhost:5173
```

- React dev server: port 5173 (Vite)
- Backend API expected: port 8081 (Spring WebFlux)
- API base URL configured via VITE_API_URL in .env

---

## Appendix D: Module Structure Summary

```
reaw/
├── generate_react_app.py              # Unified entry point (Phase 1 + 2)
├── phase1_generate_react_definition.py # Phase 1 entry point
├── phase2_generate_react_code.py       # Phase 2 entry point
├── requirements.txt                    # pydantic, jinja2
├── version.py
│
├── models/
│   ├── definition_models.py            # swfaw input models (18 layers)
│   ├── react_definition_models.py      # React definition models (12 concerns)
│   └── property_objects.py             # Phase 2 template-ready property objects
│
├── parsers/
│   ├── definition_parser.py            # swfaw JSON → AppDefinition
│   └── react_definition_parser.py      # react JSON → ReactAppDefinition
│
├── generators/
│   ├── phase1/
│   │   ├── react_definition_generator.py  # Phase 1 coordinator
│   │   ├── route_generator.py
│   │   ├── form_grouping_generator.py
│   │   ├── component_mapping_generator.py
│   │   ├── page_definition_generator.py
│   │   ├── layout_generator.py
│   │   ├── auth_config_generator.py
│   │   ├── api_services_generator.py
│   │   ├── redux_store_generator.py
│   │   ├── theme_generator.py
│   │   ├── charts_generator.py
│   │   ├── env_generator.py
│   │   └── manifest_generator.py
│   │
│   ├── phase2/
│   │   ├── react_code_generator.py        # Phase 2 coordinator
│   │   ├── theme_generator.py
│   │   ├── scaffold_generator.py
│   │   ├── api_service_generator.py
│   │   ├── redux_generator.py
│   │   ├── component_wrapper_generator.py
│   │   ├── auth_generator.py
│   │   ├── permission_generator.py
│   │   ├── chart_generator.py
│   │   ├── widget_generator.py
│   │   ├── entity_component_generator.py
│   │   ├── filter_component_generator.py
│   │   ├── query_component_generator.py
│   │   ├── grouped_form_generator.py
│   │   ├── entity_page_generator.py
│   │   ├── filter_page_generator.py
│   │   ├── query_page_generator.py
│   │   └── grid_layout_generator.py
│   │
│   └── ai_react_generator.py             # AI component generator
│
├── transformers/
│   ├── phase1/                            # 11 Phase 1 transformers
│   └── phase2/                            # 16 Phase 2 transformers
│
├── templates/                             # 19 template modules
│   ├── scaffold_templates.py
│   ├── api_service_templates.py
│   ├── redux_templates.py
│   ├── component_wrapper_templates.py
│   ├── auth_templates.py
│   ├── permission_templates.py
│   ├── chart_templates.py
│   ├── widget_templates.py
│   ├── entity_component_templates.py
│   ├── filter_component_templates.py
│   ├── query_component_templates.py
│   ├── grouped_form_templates.py
│   ├── entity_page_templates.py
│   ├── filter_page_templates.py
│   ├── query_page_templates.py
│   ├── grid_layout_templates.py
│   ├── theme_templates.py
│   └── ai_templates.py
│
├── utils/
│   ├── file_writer.py
│   ├── filter_query_extractor.py
│   ├── string_utils.py
│   └── type_mapping.py
│
├── tools/
│   └── validate_react_app.py
│
└── tests/                                 # Property-based and smoke tests
    ├── test_ai_react_generator.py
    ├── test_reaw_ai_integration.py
    ├── test_component_mapping_properties.py
    ├── test_component_mapping_widget_properties.py
    ├── test_entity_component_widget_properties.py
    ├── test_form_template_widget_properties.py
    ├── test_scaffold_widget_deps_properties.py
    ├── test_widget_generator_properties.py
    ├── test_widget_generator_smoke.py
    ├── test_widget_integration.py
    └── test_widget_templates_smoke.py
```
