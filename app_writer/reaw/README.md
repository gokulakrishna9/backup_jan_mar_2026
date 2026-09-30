# React Application Writer (REAW)

Generates complete React applications from swfaw application definitions. Reads `webflux_*.json` definitions to understand the backend API, then produces a full React frontend with routing, Redux state management, API services, forms, tables, and theming.

## Quick Start

```bash
# Generate React app from existing application definitions
py reaw/generate_react_app.py --input <path_to_application_definitions> --output <output_dir>
```

## Usage

### Unified (Phase 1 + Phase 2)

```bash
py reaw/generate_react_app.py \
    --input generated_application/my_app/application_definitions \
    --output generated_application/my_app
```

### Phase 1 Only (Generate React Definitions)

```bash
py reaw/phase1_generate_react_definition.py \
    --input generated_application/my_app/application_definitions \
    --output generated_application/my_app
```

### Phase 2 Only (Generate React Code from Definitions)

```bash
py reaw/phase2_generate_react_code.py \
    --output generated_application/my_app
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--input` | Yes | Path to `application_definitions/` directory containing `webflux_*.json` files |
| `--output` | No | Output directory (default: `../generated_application/<db_name>_<timestamp>`) |

## Two-Phase Architecture

### Phase 1: Generate React Definitions

Reads swfaw `webflux_*.json` definitions and produces `react_*.json` definition files:

| Output File | Purpose |
|-------------|---------|
| `react_manifest.json` | Index of all React definition files |
| `react_routes.json` | Route definitions per entity (list/detail/create/edit pages) |
| `react_page_definitions.json` | Page layouts, columns, form fields per entity |
| `react_api_services.json` | API service definitions (endpoints, methods, DTOs) |
| `react_redux_store.json` | Redux slices, actions, selectors per entity |
| `react_component_mappings.json` | Component type mappings (field type → React component) |
| `react_auth_config.json` | Authentication configuration (JWT, login/logout routes) |
| `react_layout.json` | App layout (sidebar, header, navigation structure) |
| `react_theme.json` | Design tokens (colors, typography, spacing, shadows) |
| `react_charts.json` | Dashboard chart definitions |
| `react_form_groupings.json` | Form field groupings for complex entities |
| `react_env.json` | Environment configuration (API base URL, ports) |

### Phase 2: Generate React Code

Reads `react_*.json` definitions and generates the full React application:

- Pages (list, detail, create, edit per entity)
- Components (forms, tables, filters, charts)
- API services (Axios-based, auto-generated from endpoint definitions)
- Redux store (slices, thunks, selectors)
- Routing (React Router with auth guards)
- Layout (sidebar navigation, header, breadcrumbs)
- Theming (CSS variables from react_theme.json)
- Authentication (JWT login/logout, token refresh)

## Output Structure

```
<output_dir>/
├── application_definitions/     # React definition JSONs (Phase 1 output)
│   ├── react_manifest.json
│   ├── react_routes.json
│   ├── react_page_definitions.json
│   ├── react_api_services.json
│   ├── react_redux_store.json
│   ├── react_component_mappings.json
│   ├── react_auth_config.json
│   ├── react_layout.json
│   ├── react_theme.json
│   ├── react_charts.json
│   ├── react_form_groupings.json
│   └── react_env.json
└── react_app/                   # Generated React application (Phase 2 output)
    ├── public/
    ├── src/
    │   ├── components/
    │   ├── pages/
    │   ├── services/
    │   ├── store/
    │   ├── routes/
    │   ├── layout/
    │   ├── theme/
    │   └── App.jsx
    ├── package.json
    └── vite.config.js
```

## Theming

The default `react_theme.json` can be replaced with a scraped theme from any website using the Theme Scraper:

```bash
# Scrape a theme and overwrite the default
py theme_scraper/scrape.py --url https://target-site.com --output <app_definitions_dir>

# Regenerate React code with the new theme
py reaw/phase2_generate_react_code.py --output <output_dir>
```

## Integration with swfaw

REAW reads the same `application_definitions/` folder that swfaw writes. The typical workflow:

1. swfaw generates `webflux_*.json` definitions (Phase 1) + Java code (Phase 2)
2. REAW reads those definitions → generates `react_*.json` (Phase 1) + React code (Phase 2)
3. Both outputs live side-by-side: `webflux_app/` + `react_app/`

With the definition-first pipeline (Phase 3), definitions live at `application_definitions/<app_name>/` and REAW reads from there directly.

## Important Notes

- REAW has conflicting module names with swfaw — always invoke via subprocess, never import directly
- React dev server runs on port 5173 (Vite)
- Backend API expected on port 8081 (Spring WebFlux)

## Dependencies

```bash
pip install -r reaw/requirements.txt
```

## Running the Generated App

```bash
cd generated_application/my_app/react_app
npm install
npm run dev
# Opens at http://localhost:5173
```
