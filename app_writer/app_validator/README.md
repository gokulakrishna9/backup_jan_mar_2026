# App Validator

Standalone smoke-test tool for validating generated applications (WebFlux backend + React frontend).

## Requirements

```bash
py -m pip install playwright requests
py -m playwright install chromium
```

## Commands

### `backend` — HTTP smoke tests for WebFlux
```bash
py app_validator/validate.py backend --url http://localhost:8081
```
Tests health endpoints, Swagger/OpenAPI, sampled API endpoints, and auth flow via HTTP.

### `frontend` — Page load checks for React
```bash
py app_validator/validate.py frontend --url http://localhost:5173 --definitions <app_definitions_path>
```
Loads routes from `react_routes.json` definition file, navigates each in Chromium, checks for console errors, blank pages, and expected PrimeReact components. Runs headed with video recording by default.

Options: `--headless`, `--no-video`, `--video-dir <path>`, `--max-routes N`

### `simulate` — Interactive E2E (definition-driven)
```bash
py app_validator/validate.py simulate \
    --url http://localhost:5173 \
    --definitions <application_definitions_path> \
    --headed
```
Reads the React definition JSON files to build an interaction plan, then executes it in a real browser:
- Auth: register → login (with API fallback for CORS)
- Navigation: clicks sidebar links from layout.navGroups
- Entity pages: fills forms using field definitions from component_mappings
- DataTable: verifies tables render
- Filter pages: interacts with dropdowns and filter controls
- Query pages: expands accordions, finds execute buttons
- Video: records the entire test session as a .webm file (default on)

Options: `--max-entities N`, `--no-video`, `--video-dir <path>`, `--headed`

### `all` — Backend + Frontend combined
```bash
py app_validator/validate.py all \
    --backend-url http://localhost:8081 \
    --frontend-url http://localhost:5173 \
    --app-dir <react_app_path>
```

### `api-coverage` — Definition-only API coverage check + optional live CRUD
```bash
# Phase 1: definition cross-check only (no servers needed)
py app_validator/validate.py api-coverage \
    --definitions <application_definitions_path>

# Phase 1 + Phase 2: live CRUD lifecycle + DB verification
py app_validator/validate.py api-coverage \
    --definitions <application_definitions_path> \
    --backend-url http://localhost:8081 \
    --username admin --password pass \
    --max-entities 5
```
Phase 1 cross-checks backend API operations (from `webflux_controller_layer.json`) against React UI components (routes, pages, forms, fields, DataTable, Redux thunks, API services). No running servers needed — reads only definition files.

Phase 2 (when `--backend-url` + credentials provided) authenticates against the running backend, then runs create → getById → getAll → update → delete per sampled entity. Verifies DB records after create/delete using connection info from `webflux_project_metadata.json`. Login endpoint is resolved from `webflux_security_layer.json`.

## Common Options
- `--headed` — Show browser window (frontend/simulate)
- `--timeout N` — Timeout in ms (default: 15000)
- `--json` — Output results as JSON
- `--max-routes N` — Max routes per page type (frontend, default: 5)
- `--max-endpoints N` — Max API endpoints per HTTP method (backend, default: 5)
- `--max-entities N` — Max entities per page type (simulate, default: 3)

## Detailed Documentation

See [DOCUMENTATION.md](DOCUMENTATION.md) for comprehensive reference including architecture, API details, data classes, classification logic, known limitations, and troubleshooting.
