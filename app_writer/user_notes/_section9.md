
---

## 9. Templates

### Template Organization

All templates live in `reaw/templates/` as Python modules containing multi-line string constants. Phase 2 generators import these constants and render them with Jinja2 or Python string.Template.

| Template Module | Templates | Used By |
|----------------|-----------|---------|
| `scaffold_templates.py` | PACKAGE_JSON, VITE_CONFIG, ENV_FILE, INDEX_HTML, MAIN_JSX, APP_JSX, LOGGER_UTIL, DASHBOARD_PAGE | ScaffoldGenerator |
| `api_service_templates.py` | API_CLIENT, ENTITY_SERVICE | ApiServiceGenerator |
| `redux_templates.py` | STORE_JS, STORE_INDEX, ENTITY_SLICE | ReduxGenerator |
| `component_wrapper_templates.py` | COMPONENT_WRAPPER | ComponentWrapperGenerator |
| `auth_templates.py` | LOGIN_PAGE, REGISTER_PAGE, AUTH_CONTEXT, PROTECTED_ROUTE | AuthGenerator |
| `permission_templates.py` | USE_PERMISSIONS | PermissionGenerator |
| `chart_templates.py` | BASE_CHART, CHART_TYPE_WRAPPER, CHART_REGISTRY, CHART_MAPPING_ENGINE | ChartGenerator |
| `widget_templates.py` | QUILL_EDITOR_WIDGET, MONACO_EDITOR_WIDGET, MARKDOWN_EDITOR_WIDGET, FILE_UPLOAD_WIDGET | WidgetGenerator |
| `entity_component_templates.py` | ENTITY_FORM, ENTITY_DATATABLE | EntityComponentGenerator |
| `filter_component_templates.py` | FILTER_PANEL | FilterComponentGenerator |
| `query_component_templates.py` | QUERY_SECTION | QueryComponentGenerator |
| `grouped_form_templates.py` | GROUPED_FORM | GroupedFormGenerator |
| `entity_page_templates.py` | ENTITY_PAGE | EntityPageGenerator |
| `filter_page_templates.py` | FILTER_PAGE | FilterPageGenerator |
| `query_page_templates.py` | QUERY_PAGE | QueryPageGenerator |
| `grid_layout_templates.py` | APP_LAYOUT_JSX, APP_LAYOUT_CSS | GridLayoutGenerator |
| `theme_templates.py` | THEME_VARIABLES, PRIMEREACT_OVERRIDES | Phase2ThemeGenerator |
| `ai_templates.py` | AI_CHAT_PANEL, SMART_SEARCH_BAR, CONTENT_GENERATION_BUTTON, AI_SUGGESTION_WIDGET, STANDALONE_CHAT_PAGE, STANDALONE_GENERATOR_PAGE, STANDALONE_DASHBOARD_PAGE, RAG_ADMIN_PAGE, EVALUATION_SCORE_BADGE, EVALUATION_DASHBOARD_PAGE, DOCUMENT_UPLOAD_PANEL, DOCUMENT_LIST_PANEL, DOCUMENT_INGESTION_PAGE, DOCUMENT_TASK_PANEL, DOCUMENT_TASK_CHAIN_BUILDER, AI_API_SERVICE, AI_NAV_ENTRIES | AiReactGenerator |

### Template Rendering Patterns

Most templates use Jinja2:
```python
from jinja2 import Template
content = Template(TEMPLATE_STRING).render(**context_dict)
```

Redux templates use Jinja2 Environment with custom filters:
```python
from jinja2 import Environment
env = Environment()
env.filters["camelCase"] = to_camel_case
content = env.from_string(TEMPLATE_STRING).render(**context)
```

AI templates use Python string.Template to avoid JSX/Jinja2 delimiter conflicts:
```python
from string import Template as StringTemplate
content = StringTemplate(TEMPLATE_STRING).safe_substitute(key=value, ...)
```

---

## 10. React Definition File Schemas

### react_manifest.json

Index of all React definition files.

```json
{
  "version": "1.0.0",
  "files": [
    { "path": "react_routes.json", "concern": "routing" },
    { "path": "react_form_groupings.json", "concern": "form_groupings" },
    { "path": "react_component_mappings.json", "concern": "component_mappings" },
    { "path": "react_page_definitions.json", "concern": "page_definitions" },
    { "path": "react_layout.json", "concern": "layout" },
    { "path": "react_auth_config.json", "concern": "authentication" },
    { "path": "react_api_services.json", "concern": "api_services" },
    { "path": "react_redux_store.json", "concern": "redux_store" },
    { "path": "react_theme.json", "concern": "theme" },
    { "path": "react_charts.json", "concern": "charts" },
    { "path": "react_env.json", "concern": "env_config" }
  ]
}
```

### react_routes.json

Array of route definitions. Each route maps a URL path to a page component.

```json
[
  {
    "path": "/users",
    "pageComponent": "UserPage",
    "pageType": "entity",
    "pageFolder": "entitys",
    "entityName": "User",
    "navLabel": "Users",
    "navGroup": "Entities",
    "requiresAuth": true
  },
  {
    "path": "/users/filter",
    "pageComponent": "UserFilterPage",
    "pageType": "filter",
    "pageFolder": "filters",
    "entityName": "User",
    "navLabel": "User Filters",
    "navGroup": "Filters",
    "requiresAuth": true
  },
  {
    "path": "/users/query",
    "pageComponent": "UserQueryPage",
    "pageType": "query",
    "pageFolder": "queries",
    "entityName": "User",
    "navLabel": "User Queries",
    "navGroup": "Queries",
    "requiresAuth": true
  }
]
```

Maps to: React Router route entries in App.jsx, navigation items in AppLayout.jsx.

### react_form_groupings.json

Array of form groupings for parent-child entity relationships (tabbed forms).

```json
[
  {
    "groupName": "CourseGroup",
    "parentEntity": "Course",
    "tabs": [
      { "entityName": "Course", "tabLabel": "Course", "tabOrder": 0, "included": true },
      { "entityName": "Module", "tabLabel": "Modules", "tabOrder": 1, "included": true },
      { "entityName": "Lesson", "tabLabel": "Lessons", "tabOrder": 2, "included": true }
    ]
  }
]
```

Maps to: GroupedForm.jsx components with PrimeReact TabView.

### react_component_mappings.json

Array of per-entity field-to-component mappings.

```json
[
  {
    "entityName": "User",
    "fields": [
      {
        "fieldName": "firstName",
        "fieldLabel": "First Name",
        "componentType": "InputText",
        "javaType": "String",
        "columnDefinition": "",
        "props": {},
        "validation": {
          "required": true,
          "requiredMessage": "First name is required",
          "maxLength": 100,
          "maxLengthMessage": "Max 100 characters"
        },
        "isRelationshipField": false,
        "relatedEntityName": null,
        "isMultiSelect": false,
        "autocompleteDisplayField": null,
        "includeInDTO": true
      },
      {
        "fieldName": "roleId",
        "fieldLabel": "Role",
        "componentType": "AutoComplete",
        "javaType": "Long",
        "props": { "mode": "single", "relatedEntity": "Role", "displayField": "name" },
        "validation": { "required": true },
        "isRelationshipField": true,
        "relatedEntityName": "Role",
        "isMultiSelect": false,
        "autocompleteDisplayField": "name",
        "includeInDTO": true
      },
      {
        "fieldName": "bio",
        "fieldLabel": "Bio",
        "componentType": "QuillEditor",
        "javaType": "String",
        "props": { "fieldWidget": "richText" },
        "validation": null,
        "isRelationshipField": false,
        "includeInDTO": true
      }
    ],
    "excludeSensitiveFields": ["passwordHash"],
    "singleRecordPerUser": false
  }
]
```

Maps to: Form.jsx field rendering, DataTable.jsx column definitions.

### react_page_definitions.json

Array of page layouts using CSS Grid.

```json
[
  {
    "pageId": "user-page",
    "pageType": "entity",
    "entityName": "User",
    "gridTemplate": {
      "gridTemplateRows": "auto 1fr",
      "gridTemplateColumns": "1fr",
      "gridTemplateAreas": ["\"form\"", "\"table\""]
    },
    "componentPlacements": [
      {
        "componentType": "form",
        "entityName": "User",
        "gridArea": "form",
        "formLayout": { "columnsLg": 3, "columnsMd": 2, "columnsSm": 1, "fullWidthComponentTypes": ["InputTextarea"] },
        "formButtons": [
          { "label": "Save", "icon": "pi pi-check", "action": "submit", "className": "p-button-success", "visibleWhen": "editMode" },
          { "label": "Cancel", "icon": "pi pi-times", "action": "cancel", "visibleWhen": "editMode" }
        ]
      },
      {
        "componentType": "dataTable",
        "entityName": "User",
        "gridArea": "table"
      }
    ]
  }
]
```

Maps to: EntityPage.jsx CSS Grid layout, component placement within grid areas.

### react_layout.json

Application-level layout configuration.

```json
{
  "applicationName": "My Application",
  "apiPort": 8081,
  "header": { "visible": true, "collapsible": true, "defaultCollapsed": false },
  "footer": { "visible": true, "collapsible": true, "defaultCollapsed": false },
  "leftNav": { "visible": true, "collapsible": true, "defaultCollapsed": false },
  "content": { "visible": true, "collapsible": false, "defaultCollapsed": false },
  "navGroups": [
    {
      "groupName": "Entities",
      "entities": [
        { "label": "Users", "path": "/users" },
        { "label": "Roles", "path": "/roles" }
      ]
    },
    {
      "groupName": "Filters",
      "entities": [
        { "label": "User Filters", "path": "/users/filter" }
      ]
    }
  ]
}
```

Maps to: AppLayout.jsx (sidebar, header, footer), navigation menu structure.

### react_auth_config.json

Authentication and authorization configuration.

```json
{
  "jwtEnabled": true,
  "oauth2Enabled": false,
  "oauth2Providers": [],
  "refreshTokenEnabled": true,
  "protectedRoutes": ["/users", "/roles"],
  "permissionsEndpoint": "/api/auth/permissions",
  "loginEndpoint": "/api/auth/login",
  "registerEndpoint": "/api/auth/register",
  "registerEnabled": true
}
```

Maps to: AuthContext.jsx (token management), LoginPage.jsx, RegisterPage.jsx, ProtectedRoute.jsx, usePermissions.js hook.

### react_api_services.json

Array of per-entity API service definitions.

```json
[
  {
    "entityName": "User",
    "basePath": "/api/users",
    "endpoints": {
      "getAll": { "enabled": true, "method": "GET", "supportsPagination": true, "supportsFiltering": true, "supportsSorting": true },
      "getById": { "enabled": true, "method": "GET" },
      "create": { "enabled": true, "method": "POST" },
      "update": { "enabled": true, "method": "PUT" },
      "delete": { "enabled": true, "method": "DELETE" }
    }
  }
]
```

Maps to: apiClient.js (Axios instance with interceptors), per-entity service files (userService.js, etc.).

### react_redux_store.json

Array of per-entity Redux store definitions.

```json
[
  {
    "entityName": "User",
    "pkField": "id",
    "thunks": {
      "fetchAll": true,
      "fetchById": true,
      "create": true,
      "update": true,
      "delete": true
    },
    "stateShape": {
      "listState": true,
      "singleItemState": true,
      "mutationState": true
    },
    "pagination": {
      "currentPage": 0,
      "pageSize": 20,
      "totalCount": 0
    }
  }
]
```

Maps to: store.js (configureStore), per-entity slice files with async thunks, selectors, and reducers.

### react_theme.json

Design tokens for the entire application.

```json
{
  "colorPalette": {
    "background-primary": "#f8f9fa",
    "background-secondary": "#ffffff",
    "surface": "#f1f3f5",
    "border": "#dee2e6",
    "text-primary": "#495057",
    "text-secondary": "#868e96",
    "accent": "#748ffc",
    "accent-hover": "#5c7cfa",
    "success": "#69db7c",
    "warning": "#ffd43b",
    "error": "#ff8787",
    "info": "#74c0fc"
  },
  "typography": {
    "fontFamily": "Inter, system-ui, sans-serif",
    "fontSize": "16px",
    "fontSizeSmall": "14px",
    "fontSizeLarge": "20px",
    "headingFontFamily": null,
    "headingFontWeight": "600",
    "lineHeight": "1.5"
  },
  "spacing": {
    "unit": "8px",
    "small": "4px",
    "medium": "8px",
    "large": "16px",
    "xlarge": "24px"
  },
  "borders": {
    "radius": "6px",
    "radiusLarge": "12px",
    "width": "1px",
    "color": "#dee2e6"
  },
  "shadows": {
    "small": "0 1px 2px rgba(0,0,0,0.05)",
    "medium": "0 4px 6px rgba(0,0,0,0.1)",
    "large": "0 10px 15px rgba(0,0,0,0.1)"
  },
  "components": {
    "button": {},
    "input": {},
    "card": {},
    "table": {},
    "sidebar": {}
  },
  "animationsEnabled": true,
  "animationStyle": {
    "transitionDuration": "200ms",
    "easingFunction": "ease-out",
    "hover": { "type": "background-shift", "intensity": "subtle" },
    "focus": { "type": "outline", "intensity": "mild" },
    "click": { "type": "scale", "intensity": "subtle" },
    "selection": { "type": "fade", "intensity": "mild" }
  },
  "source": { "url": "", "scrapedAt": "" }
}
```

Maps to: theme-variables.css (CSS custom properties), primereact-theme-overrides.css.

### react_charts.json

Chart type definitions and mapping rules.

```json
{
  "chartTypes": [
    { "typeId": "bar", "enabled": true, "defaultOption": {} },
    { "typeId": "line", "enabled": true, "defaultOption": {} },
    { "typeId": "pie", "enabled": true, "defaultOption": {} }
  ],
  "mappingRules": [
    { "ruleId": "numeric-bar", "chartType": "bar", "conditions": {}, "priority": 50 }
  ]
}
```

Maps to: BaseChart.jsx, per-type chart wrappers, chartRegistry.js, chartMappingEngine.js.

### react_env.json

Environment variable definitions.

```json
{
  "variables": [
    { "key": "VITE_API_URL", "value": "http://localhost:8081", "comment": "Backend API base URL" },
    { "key": "VITE_APP_NAME", "value": "My Application", "comment": "Application display name" }
  ]
}
```

Maps to: .env file in the React app root.
