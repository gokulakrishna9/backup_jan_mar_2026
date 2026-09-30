# App Validator — Comprehensive Documentation

Standalone smoke-test and interactive E2E validation tool for generated applications produced by **swfaw_v2** (Spring WebFlux backend) and **REAW** (React frontend).

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Installation](#installation)
3. [CLI Reference](#cli-reference)
4. [Module Reference](#module-reference)
   - [validate.py — Unified CLI](#validatepy)
   - [backend_validator.py — HTTP Smoke Tests](#backend_validatorpy)
   - [frontend_validator.py — Headless Browser Checks](#frontend_validatorpy)
   - [interaction_validator.py — Definition-Driven E2E](#interaction_validatorpy)
   - [api_coverage_validator.py — API Coverage Check](#api_coverage_validatorpy)
5. [Data Classes](#data-classes)
6. [Definition-Driven Approach](#definition-driven-approach)
7. [Result Classification Logic](#result-classification-logic)
8. [Console Noise Filtering](#console-noise-filtering)
9. [Video Recording](#video-recording)
10. [Exit Codes](#exit-codes)
11. [Known Limitations](#known-limitations)
12. [Troubleshooting](#troubleshooting)

---

## Architecture Overview

```
app_validator/
├── validate.py                 # Unified CLI entry point (5 subcommands)
├── backend_validator.py        # HTTP-based WebFlux smoke tests
├── frontend_validator.py       # Headless Chromium page-load checks (Playwright)
├── interaction_validator.py    # Definition-driven interactive E2E simulation
├── api_coverage_validator.py   # Definition-only API coverage cross-check
├── README.md                   # Quick-start usage guide
├── DOCUMENTATION.md            # This file
└── __init__.py
```

The tool is organized into four independent validators, each callable standalone or combined through the unified CLI:

| Module | Transport | What it tests |
|--------|-----------|---------------|
| `backend_validator` | HTTP (requests) | Server health, Swagger/OpenAPI, API endpoints, auth flow |
| `frontend_validator` | Headless Chromium (Playwright) | Route loading, console errors, PrimeReact DOM elements |
| `interaction_validator` | Headed/headless Chromium (Playwright) | Auth register/login, sidebar nav, form fill, DataTable, filters, queries |
| `api_coverage_validator` | Definition files only (no servers) | Cross-checks backend API operations against React UI components |

---

## Installation

```bash
py -m pip install playwright requests
py -m playwright install chromium
```

Dependencies:
- `requests` — used by `backend_validator` and as API fallback in `interaction_validator`
- `playwright` — used by `frontend_validator` and `interaction_validator`
- Chromium browser — installed via Playwright

---

## CLI Reference

All commands are run from the workspace root:

```bash
py app_validator/validate.py <subcommand> [options]
```

### Subcommand: `backend`

HTTP smoke tests against the running WebFlux application.

```bash
py app_validator/validate.py backend --url http://localhost:8081 [options]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--url` | (required) | Base URL of the running WebFlux app |
| `--max-endpoints` | 5 | Max API endpoints to sample per HTTP method |
| `--timeout` | 15000 | Request timeout in milliseconds |
| `--json` | false | Output results as JSON |

### Subcommand: `frontend`

Headless Chromium page-load validation of the React app.

```bash
py app_validator/validate.py frontend --url http://localhost:5173 --definitions <app_definitions_path> [options]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--url` | None | Base URL of running React dev server (provide this OR `--app-dir`) |
| `--definitions` | None | Path to `application_definitions/` folder (for route discovery from `react_routes.json`) |
| `--app-dir` | None | Path to `react_app/` folder — auto-starts Vite dev server |
| `--max-routes` | 5 | Max routes to sample per page type |
| `--timeout` | 15000 | Page load timeout in milliseconds |
| `--headed` | true | Show browser window (default: on) |
| `--headless` | false | Run headless (no browser window) |
| `--no-video` | false | Disable video recording |
| `--video-dir` | auto | Custom video output directory |
| `--json` | false | Output results as JSON |

One of `--url` or `--app-dir` is required. If `--app-dir` is provided without `--url`, Vite is started automatically and stopped on exit. Routes are loaded from `react_routes.json` in the definitions folder. Video is recorded by default to `<definitions>/../validation_videos/frontend_<timestamp>/`.

### Subcommand: `simulate`

Definition-driven interactive E2E simulation in a real browser.

```bash
py app_validator/validate.py simulate \
    --url http://localhost:5173 \
    --definitions <application_definitions_path> \
    --headed [options]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--url` | None | Base URL of running React dev server (provide this OR `--app-dir`) |
| `--app-dir` | None | Path to `react_app/` folder — auto-starts Vite |
| `--definitions` | (required) | Path to `application_definitions/` folder |
| `--max-entities` | 3 | Max entities to test per page type |
| `--timeout` | 15000 | Timeout in milliseconds |
| `--headed` | false | Show browser window (recommended for simulate) |
| `--no-video` | false | Disable video recording |
| `--video-dir` | auto | Custom video output directory |
| `--json` | false | Output results as JSON |

### Subcommand: `all`

Runs backend + frontend validation sequentially.

```bash
py app_validator/validate.py all \
    --backend-url http://localhost:8081 \
    --frontend-url http://localhost:5173 \
    --app-dir <path> [options]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--backend-url` | (required) | Base URL of WebFlux app |
| `--frontend-url` | None | Base URL of React dev server (provide this OR `--app-dir`) |
| `--app-dir` | None | Path to `react_app/` folder |
| `--max-routes` | 5 | Max routes per page type (frontend) |
| `--max-endpoints` | 5 | Max endpoints per HTTP method (backend) |
| `--timeout` | 15000 | Timeout in milliseconds |
| `--headed` | true | Show browser window (default: on) |
| `--headless` | false | Run headless (no browser window) |
| `--no-video` | false | Disable video recording |
| `--video-dir` | auto | Custom video output directory |
| `--json` | false | Output results as JSON |

### Subcommand: `api-coverage`

Two-phase validation: (1) definition-only cross-check verifying every backend API operation has matching React UI components, and (2) optional live CRUD lifecycle testing with DB verification against a running backend.

```bash
# Phase 1 only (definitions only, no servers needed)
py app_validator/validate.py api-coverage --definitions <application_definitions_path>

# Phase 1 + Phase 2 (live CRUD + DB verification)
py app_validator/validate.py api-coverage --definitions <application_definitions_path> \
    --backend-url http://localhost:8081 \
    --username admin --password pass \
    --max-entities 5
```

| Option | Default | Description |
|--------|---------|-------------|
| `--definitions` | (required) | Path to `application_definitions/` folder |
| `--backend-url` | None | Base URL of running WebFlux app (enables Phase 2 live CRUD tests) |
| `--username` | None | Login username for live tests (required with `--backend-url`) |
| `--password` | None | Login password for live tests (required with `--backend-url`) |
| `--max-entities` | 5 | Max entities to test in live mode |
| `--timeout` | 15000 | Timeout in ms |
| `--json` | false | Output results as JSON |

React definition files (`react_*.json`) are auto-discovered — either in the same folder or in a sibling `react_app/application_definitions/` folder.

Phase 2 login endpoint is resolved from `webflux_security_layer.json` `publicEndpoints` (looks for a path containing "login"). Falls back to `/api/auth/login` if not found.

---

## Module Reference

### validate.py

Unified CLI entry point. Parses arguments via `argparse` and dispatches to the appropriate validator module.

**Functions:**

| Function | Description |
|----------|-------------|
| `cmd_frontend(args)` | Runs frontend validation. Optionally starts/stops Vite. |
| `cmd_backend(args)` | Runs backend validation. |
| `cmd_all(args)` | Runs backend then frontend, prints combined summary. |
| `cmd_simulate(args)` | Runs interactive E2E simulation. Optionally starts/stops Vite. |
| `cmd_api_coverage(args)` | Runs definition-only API coverage cross-check. |
| `main()` | Parses CLI args and dispatches to the correct subcommand. |

Vite lifecycle: When `--app-dir` is provided without a URL, `start_vite()` is called before validation and `stop_vite()` is called in a `finally` block to ensure cleanup.

---

### backend_validator.py

HTTP-based smoke tests for the Spring WebFlux application. No browser required.

**Test sequence (5 phases):**

1. **Health checks** — `GET /setup`, `GET /login`
2. **Swagger/OpenAPI** — `GET /v3/api-docs`, `GET /swagger-ui.html`
3. **API endpoint discovery** — Parses the OpenAPI JSON to extract all paths and methods
4. **API endpoint sampling** — Samples up to N endpoints per HTTP method, sends requests
5. **Auth endpoints** — `POST /api/auth/register`, `POST /api/auth/login`, `GET /api/auth/me`

**Key functions:**

| Function | Signature | Description |
|----------|-----------|-------------|
| `run_backend_validation` | `(base_url, max_api_endpoints=5, timeout_ms=15000) → BackendReport` | Main entry point. Runs all 5 phases. |
| `print_backend_summary` | `(report: BackendReport) → None` | Prints formatted results to stdout. |
| `sample_api_paths` | `(paths, max_per_method=5) → List[Tuple[str,str]]` | Samples endpoints. Prefers parameterless GET paths. |
| `_request` | `(base_url, path, method, timeout_s, body, headers) → EndpointResult` | Makes a single HTTP request. |
| `_extract_api_paths_from_swagger` | `(base_url, timeout_s) → List[Tuple[str,str]]` | Fetches `/v3/api-docs` and extracts path+method pairs. |
| `_classify_result` | `(result, category) → EndpointResult` | Applies pass/fail/warn logic based on category. |

**Predefined endpoint lists:**

| Constant | Endpoints |
|----------|-----------|
| `HEALTH_PATHS` | `/setup` (GET), `/login` (GET) |
| `SWAGGER_PATHS` | `/v3/api-docs`, `/swagger-ui.html` |
| `AUTH_PATHS` | `/api/auth/login` (POST), `/api/auth/register` (POST), `/api/auth/me` (GET) |

---

### frontend_validator.py

Chromium-based page-load validation using Playwright. Loads routes from `react_routes.json` definition file, loads each in the browser, and checks for errors and expected DOM elements. Runs headed with video recording by default.

**Test sequence:**

1. Load routes from `react_routes.json` (path and pageType per route)
2. Sample up to N routes per type
3. For each route: load page, capture console errors, check for error boundaries, verify expected PrimeReact components

**Key functions:**

| Function | Signature | Description |
|----------|-----------|-------------|
| `run_frontend_validation` | `(base_url, definitions_path, app_dir, max_routes, timeout, headed=True, video=True, video_dir=None) → FrontendReport` | Main entry point. Headed + video on by default. |
| `print_frontend_summary` | `(report: FrontendReport) → None` | Prints formatted results. |
| `extract_routes_from_definitions` | `(definitions_path) → List[Tuple[str,str]]` | Loads routes from `react_routes.json`. |
| `validate_route` | `(page, base_url, route_path, page_type, timeout) → RouteResult` | Validates a single route. |
| `sample_routes` | `(routes, max_per_type) → List[Tuple[str,str]]` | Samples routes by page type. |
| `start_vite` | `(app_dir) → Tuple[Popen, str]` | Starts Vite dev server, returns process + URL. |
| `stop_vite` | `(proc) → None` | Gracefully terminates Vite. |
| `is_noise` | `(msg) → bool` | Checks if a console message is ignorable noise. |

**PAGE_EXPECTATIONS — Expected DOM selectors per page type:**

| Page Type | Expected Elements | Selectors |
|-----------|-------------------|-----------|
| `auth` | input field, button | `[data-pc-name='inputtext']`, `[data-pc-name='button']` |
| `entity` | data table, form/input | `[data-pc-name='datatable']`, `[data-pc-name='inputtext']` |
| `filter` | data table, filter dropdown | `[data-pc-name='datatable']`, `[data-pc-name='dropdown']` |
| `query` | accordion, execute button | `[data-pc-name='accordion']`, `[data-pc-name='button']` |

**Route validation checks (in order):**
1. HTTP response status (≥400 → fail)
2. React error boundary text ("Something went wrong")
3. Auth redirect detection (redirected to `/login` → pass with note)
4. Blank page detection (`#root` inner HTML < 10 chars)
5. Expected DOM elements from PAGE_EXPECTATIONS
6. Console errors (filtered for noise)

---

### interaction_validator.py

Definition-driven interactive E2E validator. Reads React definition JSON files to build an interaction plan, then executes it in a real browser. This is the most comprehensive validator — it simulates actual user behavior.

**Test scenarios (executed in order):**

| # | Scenario | What it does |
|---|----------|-------------|
| 1 | `auth` | Register a new user (fills form from User entity fields), then login. Falls back to direct API calls if CORS blocks the UI. |
| 2 | `nav` | Clicks sidebar navigation links derived from `layout.navGroups`. Tries kebab-case, lowercase, and text-match href formats. |
| 3 | `entity_form` | Navigates to entity pages, clicks Edit button (forms start in view mode), fills fields per `componentType`, checks DataTable presence. |
| 4 | `filter` | Navigates to filter pages, interacts with dropdowns and inputs, looks for Apply/Search buttons. |
| 5 | `query` | Navigates to query pages, expands accordion sections, looks for Execute/Run buttons. |

**Key functions:**

| Function | Signature | Description |
|----------|-----------|-------------|
| `run_interaction_validation` | `(base_url, app_def_path, max_entities=3, timeout=15000, headed=False, video=True, video_dir=None) → InteractionReport` | Main entry point. |
| `print_interaction_summary` | `(report: InteractionReport) → None` | Prints formatted results. |
| `generate_fake_value` | `(field_def: Dict) → Any` | Generates fake data based on componentType, javaType, and validation rules. |
| `scenario_auth` | `(page, base_url, app_def, timeout) → Tuple[List[StepResult], Optional[str]]` | Auth flow. Returns results + JWT token. |
| `scenario_nav` | `(page, base_url, app_def, timeout, max_clicks) → List[StepResult]` | Sidebar navigation clicks. |
| `scenario_entity_form` | `(page, base_url, app_def, timeout, entity_routes, step_counter) → Tuple[List[StepResult], int]` | Entity page form fill + DataTable check. |
| `scenario_filter` | `(page, base_url, app_def, timeout, filter_routes, step_counter) → Tuple[List[StepResult], int]` | Filter page interaction. |
| `scenario_query` | `(page, base_url, app_def, timeout, query_routes, step_counter) → Tuple[List[StepResult], int]` | Query page interaction. |

**AppDefinition class:**

Loads and indexes all React definition JSON files. Provides lookup methods used by every scenario.

| Method / Property | Returns | Description |
|-------------------|---------|-------------|
| `get_entity_routes(max_per_type)` | `Dict[str, List[Dict]]` | Routes grouped and sampled by pageType |
| `get_fields(entity_name)` | `List[Dict]` | Field definitions for an entity (excludes sensitive fields) |
| `get_page(entity_name, page_type)` | `Optional[Dict]` | Page definition for entity+type combo |
| `get_api(entity_name)` | `Optional[Dict]` | API service definition for an entity |
| `get_nav_groups()` | `List[Dict]` | Navigation groups from layout |
| `register_enabled` | `bool` | Whether registration is enabled in auth config |
| `jwt_enabled` | `bool` | Whether JWT auth is enabled |
| `app_name` | `str` | Application name from layout |

**Fake data generation (`generate_fake_value`):**

| componentType | Generated Value |
|---------------|----------------|
| `InputText` | `"Test <random>"` (respects maxLength). Special handling for phone, URL, email fields. |
| `InputNumber` | Random int 1-100 or float 1.0-100.0 based on javaType |
| `Calendar` | `"03/15/2026"` |
| `Checkbox` | `True` (clicks the checkbox) |
| `Dropdown` | `None` (skipped — can't determine options without runtime data) |
| `InputTextarea` | `"Test description <random>"` |

**ConsoleCapture context manager:**

Used within each scenario to capture console errors during a test step. Automatically filters noise patterns. Usage:

```python
with ConsoleCapture(page) as cc:
    # ... interact with page ...
    errors = cc.errors  # List[str] of real console errors
```

---

### api_coverage_validator.py

Two-phase API coverage validator. Phase 1 is definition-only: cross-checks every backend API operation against React UI components. Phase 2 (optional, requires `--backend-url`) authenticates against the running backend and runs the full CRUD lifecycle (create → getById → getAll → update → delete) per sampled entity, with DB verification.

No generated source code is read — only `application_definitions/` JSON files.

**Phase 1 — What it checks per entity:**

For each entity in `webflux_controller_layer.json`, it verifies the React app has:

| Backend Operation | Required React Components |
|-------------------|--------------------------|
| `create` (POST) | Route, page with form placement, form fields in component_mappings, Redux `create` thunk, API service `create` endpoint |
| `getById` (GET /{id}) | Route, page with form placement, Redux `fetchById` thunk, API service `getById` endpoint |
| `getAll` (GET) | Route, page with dataTable placement, Redux `fetchAll` thunk, API service `getAll` endpoint |
| `update` (PUT /{id}) | Route, page with form placement, form fields, Redux `update` thunk, API service `update` endpoint |
| `delete` (DELETE /{id}) | Route, page with dataTable placement, Redux `delete` thunk, API service `delete` endpoint |

Additionally checks:
- Filter route ↔ filter definition consistency
- Query route ↔ query page consistency
- Auth config completeness (JWT + loginRoute)
- Orphan React API services (no matching backend controller)

**Key functions:**

| Function | Signature | Description |
|----------|-----------|-------------|
| `run_api_coverage_validation` | `(definitions_path, backend_url=None, username=None, password=None, max_live_entities=5, timeout_ms=15000) → CoverageReport` | Main entry point. Runs Phase 1 + optional Phase 2. |
| `print_api_coverage_summary` | `(report: CoverageReport) → None` | Prints entity table + issues + live test results. |
| `run_live_api_tests` | `(defs, report, base_url, username, password, max_entities, timeout_ms) → None` | Phase 2: authenticates, runs CRUD lifecycle per sampled entity, verifies DB. |
| `_resolve_login_path` | `(defs: DefinitionSet) → str` | Extracts login endpoint from `webflux_security_layer.json` `publicEndpoints`. Falls back to `/api/auth/login`. |
| `_authenticate` | `(base_url, username, password, login_path, timeout_s) → Optional[str]` | Logs in and returns JWT token. |
| `_generate_fake_body` | `(defs, entity_name) → Dict` | Builds fake JSON body from Input DTO fields. |
| `_run_entity_lifecycle` | `(defs, ec, base_url, token, db_config, timeout_s) → None` | Runs create → getById → getAll → update → delete for one entity with DB checks. |
| `_db_count` | `(db_config, table_name, pk_column, pk_value) → Optional[int]` | Queries MySQL to verify record existence. |

**Phase 2 — Live CRUD lifecycle:**

When `--backend-url`, `--username`, and `--password` are provided, Phase 2 runs after Phase 1:

1. **Auth**: Resolves login endpoint from `webflux_security_layer.json` `publicEndpoints`, authenticates via POST, obtains JWT token.
2. **Entity sampling**: Selects up to `--max-entities` entities (skips User entity). Uses entities from Phase 1 that have enabled API operations.
3. **Per-entity CRUD lifecycle**:
   - **Create** (POST to basePath): Generates fake body from Input DTO fields. Verifies DB record exists after creation.
   - **GetById** (GET basePath/{id}): Uses the ID returned from create. Verifies correct record returned.
   - **GetAll** (GET basePath): Checks response format (list or paginated object).
   - **Update** (PUT basePath/{id}): Modifies 2 string fields from the create body. Sends update request.
   - **Delete** (DELETE basePath/{id}): Deletes the created record. Verifies DB record is gone.
4. **DB verification**: After create and delete, queries MySQL directly using connection info from `webflux_project_metadata.json` to confirm the record exists/is gone.

**Fake data generation** (`_generate_fake_body`):

| Java Type | Generated Value |
|-----------|----------------|
| `String` | `"Test <random>"` — special handling for email, phone, URL, password fields. Respects `maxLength`. |
| `Long`, `Integer` | Random int 1–100 |
| `Double`, `Float`, `BigDecimal` | Random float 1.0–100.0 |
| `Boolean` | `True` |
| `LocalDate` | `"2026-03-15"` |
| `LocalDateTime` | `"2026-03-15T10:00:00"` |

**Live test result classification:**

| Status | Meaning |
|--------|---------|
| `pass` | Operation succeeded (2xx) and DB verification passed |
| `warn` | 400 (validation error from fake data) or 401/403 (auth/permission issue) |
| `fail` | Unexpected HTTP status, 404 on getById after create, or DB verification mismatch |

**DefinitionSet class:**

Loads and indexes all definition files from both webflux and react definition paths.

| Attribute | Source File | Description |
|-----------|-------------|-------------|
| `controllers` | `webflux_controller_layer.json` | Backend controller definitions with endpoints |
| `filters` | `webflux_filter_layer.json` | Filter field definitions per entity |
| `queries` | `webflux_custom_queries_layer.json` | Custom query definitions |
| `dtos` | `webflux_dto_layer.json` | DTO definitions (Input DTOs used for fake data in Phase 2) |
| `entity_defs` | `webflux_entity_layer.json` | Entity definitions (table names, PK columns for DB verification) |
| `project_metadata` | `webflux_project_metadata.json` | Project metadata (database connection info for DB verification) |
| `security_layer` | `webflux_security_layer.json` | Security config (publicEndpoints for login path resolution) |
| `routes` | `react_routes.json` | React route definitions |
| `api_services` | `react_api_services.json` | React API service endpoint definitions |
| `component_mappings` | `react_component_mappings.json` | Form field definitions per entity |
| `page_definitions` | `react_page_definitions.json` | Component placements per page |
| `redux_store` | `react_redux_store.json` | Redux thunk definitions per entity |
| `layout` | `react_layout.json` | App layout and nav groups |
| `auth_config` | `react_auth_config.json` | Auth configuration |

**Issue severities:**

| Severity | Meaning |
|----------|---------|
| `error` | A backend API operation cannot be completed from the React UI (missing route, form, fields, Redux thunk, or API service) |
| `warning` | Inconsistency that may not block functionality (e.g., filter definition exists but no filter route) |
| `info` | Informational note (e.g., filter definition exists but not exposed in UI) |

**Data classes:**

```python
@dataclass
class CoverageIssue:
    entity: str          # Entity name or "*" for global
    operation: str       # create, getById, getAll, update, delete, filter, query, *, auth
    category: str        # route, page, form, field, datatable, redux, api_service, auth, setup, api_live
    severity: str        # error, warning, info
    message: str

@dataclass
class ApiTestResult:
    entity: str          # Entity name
    operation: str       # create, getById, getAll, update, delete
    method: str          # GET, POST, PUT, DELETE
    path: str            # Full URL path used
    status_code: int     # HTTP status code (0 = connection error)
    status: str          # pass, fail, warn
    response_time_ms: int
    error_detail: Optional[str]
    created_id: Optional[Any]  # ID returned from create

@dataclass
class EntityCoverage:
    entity_name: str
    api_operations: List[str]           # Enabled CRUD operations from backend
    has_route: bool                     # Entity route exists in react_routes.json
    has_page: bool                      # Page definition exists
    has_form: bool                      # Form placement on page
    has_datatable: bool                 # DataTable placement on page
    has_redux_thunks: Dict[str, bool]   # Which Redux thunks are defined
    has_api_service: bool               # API service definition exists
    api_service_endpoints: Dict[str, bool]  # Which API endpoints are enabled
    form_field_count: int               # Number of usable form fields
    form_fields: List[str]              # Field names
    issues: List[CoverageIssue]         # Issues found for this entity
    # Filter/query coverage
    has_filter_route: bool
    has_filter_page: bool
    has_filter_definition: bool
    filter_field_count: int
    has_query_route: bool
    has_query_page: bool
    has_query_definition: bool
    query_count: int
    # Phase 2 live test results
    api_test_results: List[ApiTestResult]

@dataclass
class CoverageReport:
    definitions_path: str
    total_entities: int
    total_issues: int
    errors: int
    warnings: int
    infos: int
    entities: List[EntityCoverage]
    global_issues: List[CoverageIssue]
    # Phase 2 stats
    live_tested: int
    live_passed: int
    live_failed: int
    live_warned: int
```

---

## Data Classes

### BackendReport / EndpointResult

```python
@dataclass
class EndpointResult:
    path: str               # e.g. "/api/users"
    method: str             # GET, POST, PUT, DELETE
    status_code: int        # HTTP status or 0 if no response
    status: str             # "pass", "fail", "warn"
    response_time_ms: int
    error_detail: Optional[str]
    category: str           # "health", "swagger", "api", "auth"

@dataclass
class BackendReport:
    base_url: str
    total_endpoints: int
    passed: int
    failed: int
    warned: int
    results: List[EndpointResult]
    api_paths_discovered: int
    swagger_available: bool
```

### FrontendReport / RouteResult

```python
@dataclass
class RouteResult:
    path: str               # e.g. "/users"
    page_type: str          # "entity", "filter", "query", "auth", "root"
    status: str             # "pass", "fail", "warn"
    load_time_ms: int
    console_errors: List[str]
    console_warnings: List[str]
    missing_elements: List[str]
    found_elements: List[str]
    error_detail: Optional[str]

@dataclass
class FrontendReport:
    base_url: str
    total_routes: int
    passed: int
    failed: int
    warned: int
    results: List[RouteResult]
    global_errors: List[str]
    video_dir: Optional[str]
```

### InteractionReport / StepResult

```python
@dataclass
class StepResult:
    scenario: str           # "auth", "nav", "entity_form", "datatable", "filter", "query"
    step: str               # Human-readable description
    status: str             # "pass", "fail", "warn"
    duration_ms: int
    error_detail: Optional[str]
    console_errors: List[str]

@dataclass
class InteractionReport:
    base_url: str
    app_def_path: str
    total_steps: int
    passed: int
    failed: int
    warned: int
    results: List[StepResult]
    video_dir: Optional[str]
```

All report classes support `dataclasses.asdict()` for JSON serialization via the `--json` flag.

---

## Definition-Driven Approach

The `simulate` subcommand reads React definition JSON files produced by REAW Phase 1. No selectors are hardcoded for entity-specific content — everything is derived from definitions.

**Definition files consumed:**

| File | Used By | Purpose |
|------|---------|---------|
| `react_routes.json` | `AppDefinition.routes` | Route paths, entityName, pageType for all pages |
| `react_auth_config.json` | `AppDefinition.auth_config` | Whether register/JWT is enabled |
| `react_layout.json` | `AppDefinition.layout` | applicationName, apiPort, navGroups (sidebar links) |
| `react_component_mappings.json` | `AppDefinition.component_mappings` | Field definitions per entity (fieldName, componentType, javaType, validation) |
| `react_page_definitions.json` | `AppDefinition.page_definitions` | Component placements per page (which components appear where) |
| `react_api_services.json` | `AppDefinition.api_services` | API endpoint definitions per entity |

**The `api-coverage` subcommand** also reads WebFlux definition files:

| File | Used By | Purpose |
|------|---------|---------|
| `webflux_controller_layer.json` | `DefinitionSet.controllers` | Backend controller endpoints — the source of truth for what API operations exist |
| `webflux_filter_layer.json` | `DefinitionSet.filters` | Filter field definitions per entity |
| `webflux_custom_queries_layer.json` | `DefinitionSet.queries` | Custom query definitions |
| `webflux_dto_layer.json` | `DefinitionSet.dtos` | Input DTO fields — used to generate fake request bodies in Phase 2 |
| `webflux_entity_layer.json` | `DefinitionSet.entity_defs` | Entity table names and PK columns — used for DB verification in Phase 2 |
| `webflux_project_metadata.json` | `DefinitionSet.project_metadata` | Database connection info — used for DB verification in Phase 2 |
| `webflux_security_layer.json` | `DefinitionSet.security_layer` | Public endpoints — used to resolve the login path in Phase 2 |

**How definitions drive each scenario:**

- **Auth**: User entity fields from `component_mappings` determine which form fields to fill during registration. `auth_config.registerEnabled` controls whether registration is attempted.
- **Nav**: `layout.navGroups[].entities[]` provides the list of sidebar links to click. Entity names are converted to href formats (kebab-case, lowercase).
- **Entity forms**: `component_mappings[].fields[]` drives which fields to fill and how (componentType determines interaction method). `page_definitions[].componentPlacements[]` determines whether a DataTable should be present.
- **Filters**: Routes with `pageType: "filter"` are navigated. Generic filter controls (dropdowns, inputs, apply buttons) are verified.
- **Queries**: Routes with `pageType: "query"` are navigated. Accordion sections and execute buttons are verified.

---

## Result Classification Logic

### Backend (`_classify_result`)

| Category | Pass | Warn | Fail |
|----------|------|------|------|
| `health` | 200, 302, 303, 400 (setup done) | — | Everything else |
| `swagger` | 200 | Non-200 | — |
| `api` | 200, 201, 401, 403, 302/303 | 404, unexpected codes | 5xx |
| `auth` | 200, 201, 400, 401, 403, 409 | 500 on login/register (smoke data) | Other 5xx |

### Frontend (`validate_route`)

| Check | Pass | Warn | Fail |
|-------|------|------|------|
| HTTP status | < 400 | — | ≥ 400 |
| Error boundary | Not present | — | "Something went wrong" in body |
| Auth redirect | Redirected to /login (expected) | — | — |
| Blank page | — | Blank + network error | Blank + no network error |
| DOM elements | All expected found | Some missing | — |
| Console errors | None (after noise filter) | — | Real errors present |

### Interaction (`scenario_*`)

Each scenario function returns `StepResult` with status set contextually:
- **pass**: Action completed successfully
- **warn**: Action partially completed or used fallback (e.g., API fallback for CORS)
- **fail**: Action could not complete (exception, error boundary, no response)

---

## Console Noise Filtering

Both `frontend_validator` and `interaction_validator` filter out known noise from browser console output.

**Frontend noise patterns (`IGNORE_PATTERNS`):**
- React DevTools download prompt
- React Router Future Flag warnings
- HMR / Vite hot-reload messages
- favicon.ico errors

**Interaction noise patterns (`NOISE_PATTERNS`):** All of the above, plus:
- `ERR_INSUFFICIENT_RESOURCES` / `ERR_NETWORK_CHANGED`
- CORS blocked XMLHttpRequest errors (known issue with hardcoded `baseURL` in apiClient)
- `net::ERR_FAILED`
- `Failed to fetch permissions`

---

## Video Recording

Both the `frontend` and `simulate` subcommands record the entire test session as a `.webm` video file using Playwright's built-in video recording. Video is enabled by default for both.

**Default locations:**
- `frontend`: `<definitions>/../validation_videos/frontend_<YYYYMMDD_HHMMSS>/`
- `simulate`: `<definitions>/../validation_videos/<YYYYMMDD_HHMMSS>/`

The video captures everything the browser renders during the test in a single continuous recording.

Disable with `--no-video`. Override directory with `--video-dir <path>`.

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All checks passed (may include warnings) |
| 1 | One or more checks failed |

---

## Known Limitations

1. **CORS with hardcoded apiClient baseURL**: The generated React app's `apiClient.js` has a hardcoded `baseURL` pointing to `http://localhost:8081`. When the React app runs on a different port (e.g., 5173), browser-based API calls are blocked by CORS. The `simulate` command works around this by falling back to direct API calls via `requests` for auth operations.

2. **Nav link format mismatch**: Sidebar link `href` values may not match the route paths exactly. The validator tries multiple formats (kebab-case, lowercase-no-separator, text match) but some links may not be found.

3. **Dropdown fields skipped**: `generate_fake_value` returns `None` for Dropdown fields because the available options are not known from the definition files alone (they come from API data at runtime).

4. **Calendar input**: PrimeReact Calendar wraps an `<input>` inside a container div. The validator tries `el.fill()` first, then falls back to `click() + keyboard.type()`. Some Calendar configurations may not respond to either approach.

5. **No file upload testing**: File upload fields are not tested.

6. **Single-user session**: The simulate command registers and logs in as a single test user. It does not test multi-user or permission-based scenarios.

7. **Frontend validator route source**: Routes are loaded from `react_routes.json` definition file. If this file is missing or incomplete, no routes will be discovered.

---

## Troubleshooting

**"playwright is required"**
```bash
py -m pip install playwright
py -m playwright install chromium
```

**"requests library is required"**
```bash
py -m pip install requests
```

**"Vite did not start within 30 seconds"**
- Ensure `npm install` has been run in the `react_app/` directory
- Check that Node.js and npm are available on PATH
- Try starting Vite manually: `npm run dev` in the react_app folder

**All routes show "auth redirect"**
- The app requires authentication. Use `simulate` instead of `frontend` — it handles login automatically.
- Or manually log in and provide a running session.

**Backend shows "Connection refused"**
- Ensure the WebFlux app is running on the specified port
- Check: `curl http://localhost:8081/setup`

**CORS errors in simulate**
- This is expected when the React app's `apiClient.js` has a hardcoded `baseURL`. The validator automatically falls back to direct API calls for auth operations. CORS console errors are filtered from results.

**"Error boundary" failures**
- A React component crashed. Check the browser console for the actual error.
- Run with `--headed` to see the error visually.
- Common cause: API returning unexpected data format.

**Video not appearing**
- Ensure `--no-video` is not set
- Check the video directory path in the output header
- Default: `<definitions>/../validation_videos/<timestamp>/`
