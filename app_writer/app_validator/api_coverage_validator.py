"""API Coverage Validator — definition-driven cross-check + live API testing.

Phase 1 (definitions only):
  Reads React + WebFlux definition JSON files and verifies that for every
  API operation the backend exposes, the React frontend has the necessary
  UI components (routes, pages, form fields, DataTable, Redux thunks).

Phase 2 (live backend, optional — requires --backend-url):
  Authenticates against the running backend, then for each sampled entity
  runs the full CRUD lifecycle (create → getById → getAll → update → delete)
  using definition-derived basePaths and fake field data.

No generated source code is read — only application_definitions/ files.

Usage (via validate.py):
    py app_validator/validate.py api-coverage --definitions <path>
    py app_validator/validate.py api-coverage --definitions <path> --backend-url http://localhost:8081 --username admin --password pass
"""

import json
import os
import random
import string
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

try:
    import requests as _requests
except ImportError:
    _requests = None


# ─── Data classes ───────────────────────────────────────────────────────────

@dataclass
class CoverageIssue:
    entity: str
    operation: str       # create, getById, getAll, update, delete, filter, query
    category: str        # route, page, form, field, datatable, redux, api_service, api_live
    severity: str        # error, warning, info
    message: str


@dataclass
class ApiTestResult:
    """Result of a single live API call."""
    entity: str
    operation: str       # create, getById, getAll, update, delete
    method: str          # GET, POST, PUT, DELETE
    path: str            # Full URL path used
    status_code: int     # HTTP status code (0 = connection error)
    status: str          # pass, fail, warn
    response_time_ms: int = 0
    error_detail: Optional[str] = None
    created_id: Optional[Any] = None  # ID returned from create (used by subsequent ops)


@dataclass
class EntityCoverage:
    entity_name: str
    api_operations: List[str] = field(default_factory=list)
    has_route: bool = False
    has_page: bool = False
    has_form: bool = False
    has_datatable: bool = False
    has_redux_thunks: Dict[str, bool] = field(default_factory=dict)
    has_api_service: bool = False
    api_service_endpoints: Dict[str, bool] = field(default_factory=dict)
    form_field_count: int = 0
    form_fields: List[str] = field(default_factory=list)
    issues: List[CoverageIssue] = field(default_factory=list)
    # Filter / query coverage
    has_filter_route: bool = False
    has_filter_page: bool = False
    has_filter_definition: bool = False
    filter_field_count: int = 0
    has_query_route: bool = False
    has_query_page: bool = False
    has_query_definition: bool = False
    query_count: int = 0
    # Live API test results
    api_test_results: List[ApiTestResult] = field(default_factory=list)


@dataclass
class CoverageReport:
    definitions_path: str
    total_entities: int = 0
    total_issues: int = 0
    errors: int = 0
    warnings: int = 0
    infos: int = 0
    entities: List[EntityCoverage] = field(default_factory=list)
    global_issues: List[CoverageIssue] = field(default_factory=list)
    # Phase 2 stats
    live_tested: int = 0
    live_passed: int = 0
    live_failed: int = 0
    live_warned: int = 0


# ─── Definition loader ──────────────────────────────────────────────────────


def _load_json(base_path: str, filename: str, default: Any = None) -> Any:
    """Load a JSON file from the definitions directory."""
    filepath = os.path.join(base_path, filename)
    if not os.path.isfile(filepath):
        return default
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def _find_react_defs_path(definitions_path: str) -> Optional[str]:
    """Find the react application_definitions path.

    React defs may live in the same folder as webflux defs, or in a
    sibling react_app/application_definitions/ folder.
    """
    # Check if react files are in the same folder
    if os.path.isfile(os.path.join(definitions_path, "react_routes.json")):
        return definitions_path

    # Check sibling react_app/application_definitions/
    parent = os.path.dirname(definitions_path)
    react_defs = os.path.join(parent, "react_app", "application_definitions")
    if os.path.isfile(os.path.join(react_defs, "react_routes.json")):
        return react_defs

    return None


class DefinitionSet:
    """Loads all definition files needed for coverage analysis."""

    def __init__(self, definitions_path: str):
        self.path = definitions_path
        self.react_path = _find_react_defs_path(definitions_path)

        # WebFlux definitions
        ctrl_data = _load_json(definitions_path, "webflux_controller_layer.json", {})
        self.controllers: List[Dict] = ctrl_data.get("controllers", []) if isinstance(ctrl_data, dict) else []

        filter_data = _load_json(definitions_path, "webflux_filter_layer.json", {})
        self.filters: Dict[str, Any] = filter_data.get("filters", {}) if isinstance(filter_data, dict) else {}

        query_data = _load_json(definitions_path, "webflux_custom_queries_layer.json", {})
        self.queries: List[Dict] = query_data.get("queries", []) if isinstance(query_data, dict) else []

        # DTO layer (for fake data generation in Phase 2)
        dto_data = _load_json(definitions_path, "webflux_dto_layer.json", {})
        self.dtos: List[Dict] = dto_data.get("dtos", []) if isinstance(dto_data, dict) else []

        # Entity layer (for table names + PK columns in DB verification)
        entity_data = _load_json(definitions_path, "webflux_entity_layer.json", {})
        self.entity_defs: List[Dict] = entity_data.get("entities", []) if isinstance(entity_data, dict) else []

        # Project metadata (for database connection info)
        meta_data = _load_json(definitions_path, "webflux_project_metadata.json", {})
        self.project_metadata: Dict = meta_data.get("projectMetadata", {}) if isinstance(meta_data, dict) else {}

        # Security layer (for auth endpoint paths)
        sec_data = _load_json(definitions_path, "webflux_security_layer.json", {})
        self.security_layer: Dict = sec_data if isinstance(sec_data, dict) else {}

        # React definitions (from react_path)
        rp = self.react_path or definitions_path
        self.routes: List[Dict] = _load_json(rp, "react_routes.json", [])
        self.api_services: List[Dict] = _load_json(rp, "react_api_services.json", [])
        self.component_mappings: List[Dict] = _load_json(rp, "react_component_mappings.json", [])
        self.page_definitions: List[Dict] = _load_json(rp, "react_page_definitions.json", [])
        self.redux_store: List[Dict] = _load_json(rp, "react_redux_store.json", [])
        self.layout: Dict = _load_json(rp, "react_layout.json", {})
        self.auth_config: Dict = _load_json(rp, "react_auth_config.json", {})

        # Build indexes
        self._ctrl_by_entity = {c["entityName"]: c for c in self.controllers}
        self._routes_by_entity: Dict[str, List[Dict]] = {}
        for r in self.routes:
            self._routes_by_entity.setdefault(r["entityName"], []).append(r)
        self._api_svc_by_entity = {s["entityName"]: s for s in self.api_services}
        self._fields_by_entity: Dict[str, List[Dict]] = {}
        self._sensitive_by_entity: Dict[str, set] = {}
        for m in self.component_mappings:
            entity = m["entityName"]
            self._sensitive_by_entity[entity] = set(m.get("excludeSensitiveFields", []))
            self._fields_by_entity[entity] = m.get("fields", [])
        self._pages_by_key: Dict[str, Dict] = {}
        for p in self.page_definitions:
            key = f"{p['entityName']}_{p['pageType']}"
            self._pages_by_key[key] = p
        self._redux_by_entity = {r["entityName"]: r for r in self.redux_store}
        # Queries indexed by entity (derived from table name → entity mapping)
        self._queries_by_table: Dict[str, List[Dict]] = {}
        for q in self.queries:
            self._queries_by_table.setdefault(q.get("table", ""), []).append(q)
        # DTO indexes: Input DTOs by entity
        self._input_dto_by_entity: Dict[str, Dict] = {}
        for d in self.dtos:
            if d.get("dtoType") == "Input":
                self._input_dto_by_entity[d["entityName"]] = d
        # Entity layer indexes: className → entity def (table name, PK, fields)
        self._entity_def_by_name: Dict[str, Dict] = {}
        for e in self.entity_defs:
            self._entity_def_by_name[e["className"]] = e

    def get_all_entity_names(self) -> List[str]:
        """Return all entity names from controllers (the source of truth)."""
        return [c["entityName"] for c in self.controllers]


# ─── Coverage analysis ──────────────────────────────────────────────────────

CRUD_OPS = ["create", "getById", "getAll", "update", "delete"]

# Maps API operation → required UI components
OP_REQUIREMENTS = {
    "create": {
        "needs_form": True,
        "needs_fields": True,
        "needs_redux": "create",
        "needs_api_svc": "create",
        "description": "Create (POST) — needs form with input fields",
    },
    "getById": {
        "needs_form": True,
        "needs_fields": False,  # view mode, fields render but read-only
        "needs_redux": "fetchById",
        "needs_api_svc": "getById",
        "description": "Get by ID (GET /{id}) — needs form in view mode",
    },
    "getAll": {
        "needs_datatable": True,
        "needs_redux": "fetchAll",
        "needs_api_svc": "getAll",
        "description": "List all (GET) — needs DataTable",
    },
    "update": {
        "needs_form": True,
        "needs_fields": True,
        "needs_redux": "update",
        "needs_api_svc": "update",
        "description": "Update (PUT /{id}) — needs form with editable fields",
    },
    "delete": {
        "needs_datatable": True,  # delete button is on the DataTable
        "needs_redux": "delete",
        "needs_api_svc": "delete",
        "description": "Delete (DELETE /{id}) — needs DataTable with delete action",
    },
}


def _analyze_entity(defs: DefinitionSet, entity_name: str) -> EntityCoverage:
    """Analyze coverage for a single entity."""
    ec = EntityCoverage(entity_name=entity_name)

    ctrl = defs._ctrl_by_entity.get(entity_name, {})
    ctrl_endpoints = ctrl.get("endpoints", {})

    # 1. Determine which API operations the backend exposes
    for op in CRUD_OPS:
        ep = ctrl_endpoints.get(op, {})
        if ep.get("enabled", False):
            ec.api_operations.append(op)

    # 2. Check route existence
    entity_routes = defs._routes_by_entity.get(entity_name, [])
    route_types = {r["pageType"] for r in entity_routes}
    ec.has_route = "entity" in route_types
    ec.has_filter_route = "filter" in route_types
    ec.has_query_route = "query" in route_types

    if not ec.has_route and ec.api_operations:
        ec.issues.append(CoverageIssue(
            entity=entity_name, operation="*", category="route",
            severity="error",
            message=f"No entity route defined — backend exposes {', '.join(ec.api_operations)} but no React route exists",
        ))

    # 3. Check page definition
    page_def = defs._pages_by_key.get(f"{entity_name}_entity")
    if page_def:
        ec.has_page = True
        placements = page_def.get("componentPlacements", [])
        placement_types = {p["componentType"] for p in placements}
        ec.has_form = "form" in placement_types
        ec.has_datatable = "dataTable" in placement_types
    else:
        if ec.has_route:
            ec.issues.append(CoverageIssue(
                entity=entity_name, operation="*", category="page",
                severity="error",
                message="Entity route exists but no page definition found",
            ))

    # 4. Check form fields from component_mappings
    fields = defs._fields_by_entity.get(entity_name, [])
    sensitive = defs._sensitive_by_entity.get(entity_name, set())
    usable_fields = [f for f in fields if f["fieldName"] not in sensitive]
    ec.form_field_count = len(usable_fields)
    ec.form_fields = [f["fieldName"] for f in usable_fields]

    # 5. Check Redux thunks
    redux_def = defs._redux_by_entity.get(entity_name)
    if redux_def:
        thunks = redux_def.get("thunks", {})
        ec.has_redux_thunks = {
            "create": thunks.get("create", False),
            "fetchById": thunks.get("fetchById", False),
            "fetchAll": thunks.get("fetchAll", False),
            "update": thunks.get("update", False),
            "delete": thunks.get("delete", False),
        }
    else:
        if ec.api_operations:
            ec.issues.append(CoverageIssue(
                entity=entity_name, operation="*", category="redux",
                severity="error",
                message="Backend exposes API operations but no Redux store definition exists",
            ))

    # 6. Check API service definition
    api_svc = defs._api_svc_by_entity.get(entity_name)
    if api_svc:
        ec.has_api_service = True
        svc_endpoints = api_svc.get("endpoints", {})
        ec.api_service_endpoints = {
            op: svc_endpoints.get(op, {}).get("enabled", False)
            for op in CRUD_OPS
        }
    else:
        if ec.api_operations:
            ec.issues.append(CoverageIssue(
                entity=entity_name, operation="*", category="api_service",
                severity="error",
                message="Backend exposes API operations but no React API service definition exists",
            ))

    # 7. Check filter coverage
    ec.has_filter_definition = entity_name in defs.filters
    if ec.has_filter_definition:
        ec.filter_field_count = len(defs.filters[entity_name].get("fields", []))
    filter_page = defs._pages_by_key.get(f"{entity_name}_filter")
    ec.has_filter_page = filter_page is not None

    if ec.has_filter_route and not ec.has_filter_definition:
        ec.issues.append(CoverageIssue(
            entity=entity_name, operation="filter", category="filter",
            severity="warning",
            message="Filter route exists but no filter definition in webflux_filter_layer.json",
        ))
    if ec.has_filter_definition and not ec.has_filter_route:
        ec.issues.append(CoverageIssue(
            entity=entity_name, operation="filter", category="route",
            severity="info",
            message="Filter definition exists but no filter route in React — filter not exposed in UI",
        ))

    # 8. Check query coverage
    # Queries are table-based; we can't perfectly map table→entity without more info,
    # so we just check if query routes/pages exist
    ec.has_query_page = defs._pages_by_key.get(f"{entity_name}_query") is not None

    # 9. Per-operation checks — does the React UI have everything needed?
    for op in ec.api_operations:
        reqs = OP_REQUIREMENTS.get(op, {})

        # Form needed?
        if reqs.get("needs_form") and not ec.has_form:
            ec.issues.append(CoverageIssue(
                entity=entity_name, operation=op, category="form",
                severity="error",
                message=f"Operation '{op}' requires a form component but page has no form placement",
            ))

        # Fields needed for create/update?
        if reqs.get("needs_fields") and ec.form_field_count == 0:
            ec.issues.append(CoverageIssue(
                entity=entity_name, operation=op, category="field",
                severity="error",
                message=f"Operation '{op}' requires form fields but component_mappings has 0 usable fields",
            ))

        # DataTable needed?
        if reqs.get("needs_datatable") and not ec.has_datatable:
            ec.issues.append(CoverageIssue(
                entity=entity_name, operation=op, category="datatable",
                severity="error",
                message=f"Operation '{op}' requires a DataTable but page has no dataTable placement",
            ))

        # Redux thunk needed?
        redux_thunk = reqs.get("needs_redux")
        if redux_thunk and not ec.has_redux_thunks.get(redux_thunk, False):
            ec.issues.append(CoverageIssue(
                entity=entity_name, operation=op, category="redux",
                severity="error",
                message=f"Operation '{op}' requires Redux thunk '{redux_thunk}' but it is missing or disabled",
            ))

        # API service endpoint needed?
        api_ep = reqs.get("needs_api_svc")
        if api_ep and not ec.api_service_endpoints.get(api_ep, False):
            ec.issues.append(CoverageIssue(
                entity=entity_name, operation=op, category="api_service",
                severity="error",
                message=f"Operation '{op}' requires API service endpoint '{api_ep}' but it is missing or disabled",
            ))

    return ec


# ─── Phase 2: Live API testing + DB verification ───────────────────────────

def _rand_str(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=length))


def _generate_fake_body(defs: DefinitionSet, entity_name: str) -> Dict[str, Any]:
    """Build a fake JSON body from the Input DTO fields."""
    dto = defs._input_dto_by_entity.get(entity_name)
    if not dto:
        return {}
    body: Dict[str, Any] = {}
    for f in dto.get("fields", []):
        if not f.get("includeInDTO", True):
            continue
        name = f["fieldName"]
        jtype = f.get("javaType", "String")
        validation = f.get("validation", {}) or {}
        max_len = validation.get("maxLength")

        if jtype == "String":
            if validation.get("email"):
                val = f"test_{_rand_str(5)}@example.com"
            elif "phone" in name.lower():
                val = "555-0100"
            elif "url" in name.lower() or "website" in name.lower():
                val = "https://example.com"
            elif "password" in name.lower() or "encrypted" in name.lower():
                val = f"Pass_{_rand_str(8)}1!"
            else:
                val = f"Test {_rand_str(6)}"
            if max_len and len(val) > max_len:
                val = val[:max_len]
            body[name] = val
        elif jtype in ("Long", "Integer", "int", "long"):
            body[name] = random.randint(1, 100)
        elif jtype in ("Double", "Float", "BigDecimal", "double", "float"):
            body[name] = round(random.uniform(1.0, 100.0), 2)
        elif jtype == "Boolean":
            body[name] = True
        elif jtype == "Byte":
            body[name] = 1
        elif jtype == "LocalDate":
            body[name] = "2026-03-15"
        elif jtype == "LocalDateTime":
            body[name] = "2026-03-15T10:00:00"
        else:
            body[name] = f"test_{_rand_str(5)}"
    return body


def _update_body(original: Dict[str, Any], defs: DefinitionSet, entity_name: str) -> Dict[str, Any]:
    """Modify a few string fields in the body for the update operation."""
    updated = dict(original)
    dto = defs._input_dto_by_entity.get(entity_name)
    if not dto:
        return updated
    changed = 0
    for f in dto.get("fields", []):
        if changed >= 2:
            break
        name = f["fieldName"]
        jtype = f.get("javaType", "String")
        if jtype == "String" and name in updated and "password" not in name.lower() and "email" not in name.lower():
            validation = f.get("validation", {}) or {}
            max_len = validation.get("maxLength")
            val = f"Upd {_rand_str(6)}"
            if max_len and len(val) > max_len:
                val = val[:max_len]
            updated[name] = val
            changed += 1
    return updated


def _api_request(base_url: str, path: str, method: str, token: str,
                 body: Any = None, timeout_s: float = 10) -> Tuple[int, Any, int]:
    """Make an HTTP request. Returns (status_code, response_json_or_None, elapsed_ms)."""
    url = f"{base_url}{path}"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    start = time.time()
    try:
        if method == "GET":
            resp = _requests.get(url, headers=headers, timeout=timeout_s)
        elif method == "POST":
            resp = _requests.post(url, headers=headers, json=body, timeout=timeout_s)
        elif method == "PUT":
            resp = _requests.put(url, headers=headers, json=body, timeout=timeout_s)
        elif method == "DELETE":
            resp = _requests.delete(url, headers=headers, timeout=timeout_s)
        else:
            resp = _requests.get(url, headers=headers, timeout=timeout_s)
        elapsed = int((time.time() - start) * 1000)
        try:
            data = resp.json()
        except Exception:
            data = None
        return resp.status_code, data, elapsed
    except _requests.exceptions.ConnectionError:
        return 0, None, 0
    except Exception:
        return 0, None, 0


def _db_count(db_config: Dict, table_name: str, pk_column: str, pk_value: Any) -> Optional[int]:
    """Query the database to check if a record exists. Returns count or None on error."""
    try:
        import mysql.connector
        conn = mysql.connector.connect(
            host=db_config.get("host", "localhost"),
            port=db_config.get("port", 3306),
            user=db_config.get("username", "root"),
            password=db_config.get("password", "password"),
            database=db_config.get("name"),
        )
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM `{table_name}` WHERE `{pk_column}` = %s", (pk_value,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row[0] if row else 0
    except Exception:
        return None


def _resolve_login_path(defs: DefinitionSet) -> str:
    """Extract the login endpoint path from webflux_security_layer.json publicEndpoints.

    Looks for an endpoint containing 'login'. Falls back to /api/auth/login.
    """
    public_eps = defs.security_layer.get("publicEndpoints", [])
    for ep in public_eps:
        path = ep if isinstance(ep, str) else ep.get("path", "")
        if "login" in path.lower():
            # Strip trailing /** wildcard if present
            return path.rstrip("*").rstrip("/") if path.endswith("/**") else path
    # Also check nested securityConfig.publicEndpoints
    sec_cfg = defs.security_layer.get("securityConfig", {})
    for ep in sec_cfg.get("publicEndpoints", []):
        path = ep if isinstance(ep, str) else ep.get("path", "")
        if "login" in path.lower():
            return path.rstrip("*").rstrip("/") if path.endswith("/**") else path
    return "/api/auth/login"


def _authenticate(base_url: str, username: str, password: str,
                  login_path: str = "/api/auth/login",
                  timeout_s: float = 10) -> Optional[str]:
    """Login and return JWT token, or None on failure."""
    code, data, _ = _api_request(base_url, login_path, "POST", "",
                                  body={"username": username, "password": password},
                                  timeout_s=timeout_s)
    if code == 200 and data and "token" in data:
        return data["token"]
    return None


def _run_entity_lifecycle(
    defs: DefinitionSet,
    ec: EntityCoverage,
    base_url: str,
    token: str,
    db_config: Optional[Dict],
    timeout_s: float,
) -> None:
    """Run create → getById → getAll → update → delete for one entity, with DB checks."""
    entity_name = ec.entity_name
    ctrl = defs._ctrl_by_entity.get(entity_name, {})
    base_path = ctrl.get("basePath", "")
    if not base_path:
        return

    # Get entity def for table/PK info
    entity_def = defs._entity_def_by_name.get(entity_name, {})
    table_name = entity_def.get("tableName", "")
    pk_column = ""
    pk_field = ""
    for f in entity_def.get("fields", []):
        if f.get("isPrimaryKey"):
            pk_column = f.get("columnName", "")
            pk_field = f.get("fieldName", "")
            break

    # Get redux PK field as fallback
    redux_def = defs._redux_by_entity.get(entity_name, {})
    if not pk_field:
        pk_field = redux_def.get("pkField", "id")

    created_id = None
    create_body = None

    # ── CREATE ──
    if "create" in ec.api_operations:
        create_body = _generate_fake_body(defs, entity_name)
        code, data, elapsed = _api_request(base_url, base_path, "POST", token,
                                            body=create_body, timeout_s=timeout_s)
        result = ApiTestResult(entity=entity_name, operation="create", method="POST",
                               path=base_path, status_code=code, status="pass",
                               response_time_ms=elapsed)
        if code in (200, 201):
            if data and pk_field in data:
                created_id = data[pk_field]
                result.created_id = created_id
            elif data and isinstance(data, dict):
                # Try to find any ID-like field
                for k, v in data.items():
                    if k.lower().endswith("id") and isinstance(v, (int, str)):
                        created_id = v
                        result.created_id = created_id
                        break
            # DB verify: record should exist
            if db_config and table_name and pk_column and created_id is not None:
                cnt = _db_count(db_config, table_name, pk_column, created_id)
                if cnt == 1:
                    result.error_detail = f"DB verified: record {pk_column}={created_id} exists"
                elif cnt == 0:
                    result.status = "fail"
                    result.error_detail = f"API returned 2xx but DB has no record with {pk_column}={created_id}"
                elif cnt is None:
                    result.error_detail = f"Created id={created_id}, DB check skipped (connection error)"
        elif code == 400:
            result.status = "warn"
            result.error_detail = f"400 Bad Request — validation error (fake data may not satisfy constraints)"
        elif code == 401 or code == 403:
            result.status = "warn"
            result.error_detail = f"{code} — auth/permission issue"
        else:
            result.status = "fail"
            result.error_detail = f"Unexpected HTTP {code}"
        ec.api_test_results.append(result)

    # ── GET BY ID ──
    if "getById" in ec.api_operations and created_id is not None:
        path = f"{base_path}/{created_id}"
        code, data, elapsed = _api_request(base_url, path, "GET", token, timeout_s=timeout_s)
        result = ApiTestResult(entity=entity_name, operation="getById", method="GET",
                               path=path, status_code=code, status="pass",
                               response_time_ms=elapsed)
        if code == 200:
            if data and pk_field in data and str(data[pk_field]) == str(created_id):
                result.error_detail = f"Returned correct record {pk_field}={created_id}"
            elif data:
                result.error_detail = "Returned data (PK field check inconclusive)"
            else:
                result.status = "warn"
                result.error_detail = "200 but empty response body"
        elif code == 404:
            result.status = "fail"
            result.error_detail = f"Record {created_id} not found — create may have failed silently"
        else:
            result.status = "fail"
            result.error_detail = f"Unexpected HTTP {code}"
        ec.api_test_results.append(result)

    # ── GET ALL ──
    if "getAll" in ec.api_operations:
        code, data, elapsed = _api_request(base_url, base_path, "GET", token, timeout_s=timeout_s)
        result = ApiTestResult(entity=entity_name, operation="getAll", method="GET",
                               path=base_path, status_code=code, status="pass",
                               response_time_ms=elapsed)
        if code == 200:
            # Response may be a list or a paginated object with "content"
            if isinstance(data, list):
                result.error_detail = f"Returned {len(data)} records"
            elif isinstance(data, dict) and "content" in data:
                result.error_detail = f"Returned page with {len(data['content'])} records, total={data.get('totalElements', '?')}"
            elif isinstance(data, dict):
                result.error_detail = "Returned data object"
            else:
                result.status = "warn"
                result.error_detail = "200 but unexpected response format"
        elif code == 401 or code == 403:
            result.status = "warn"
            result.error_detail = f"{code} — auth/permission issue"
        else:
            result.status = "fail"
            result.error_detail = f"Unexpected HTTP {code}"
        ec.api_test_results.append(result)

    # ── UPDATE ──
    if "update" in ec.api_operations and created_id is not None and create_body:
        path = f"{base_path}/{created_id}"
        update_data = _update_body(create_body, defs, entity_name)
        code, data, elapsed = _api_request(base_url, path, "PUT", token,
                                            body=update_data, timeout_s=timeout_s)
        result = ApiTestResult(entity=entity_name, operation="update", method="PUT",
                               path=path, status_code=code, status="pass",
                               response_time_ms=elapsed)
        if code == 200:
            # DB verify: check a changed field
            result.error_detail = f"Updated record {created_id}"
        elif code == 400:
            result.status = "warn"
            result.error_detail = "400 Bad Request — validation error on update data"
        elif code == 404:
            result.status = "fail"
            result.error_detail = f"Record {created_id} not found for update"
        else:
            result.status = "fail"
            result.error_detail = f"Unexpected HTTP {code}"
        ec.api_test_results.append(result)

    # ── DELETE ──
    if "delete" in ec.api_operations and created_id is not None:
        path = f"{base_path}/{created_id}"
        code, data, elapsed = _api_request(base_url, path, "DELETE", token, timeout_s=timeout_s)
        result = ApiTestResult(entity=entity_name, operation="delete", method="DELETE",
                               path=path, status_code=code, status="pass",
                               response_time_ms=elapsed)
        if code in (200, 204):
            # DB verify: record should be gone
            if db_config and table_name and pk_column and created_id is not None:
                cnt = _db_count(db_config, table_name, pk_column, created_id)
                if cnt == 0:
                    result.error_detail = f"DB verified: record {pk_column}={created_id} deleted"
                elif cnt and cnt > 0:
                    result.status = "fail"
                    result.error_detail = f"API returned {code} but DB still has record {pk_column}={created_id}"
                elif cnt is None:
                    result.error_detail = f"Deleted id={created_id}, DB check skipped (connection error)"
        elif code == 404:
            result.status = "warn"
            result.error_detail = f"Record {created_id} already gone (may have been cascade-deleted)"
        else:
            result.status = "fail"
            result.error_detail = f"Unexpected HTTP {code}"
        ec.api_test_results.append(result)


def run_live_api_tests(
    defs: DefinitionSet,
    report: CoverageReport,
    base_url: str,
    username: str,
    password: str,
    max_entities: int = 5,
    timeout_ms: int = 15000,
) -> None:
    """Phase 2: authenticate, run CRUD lifecycle per sampled entity, verify DB."""
    if _requests is None:
        report.global_issues.append(CoverageIssue(
            entity="*", operation="*", category="api_live",
            severity="error", message="requests library not installed — cannot run live API tests",
        ))
        return

    timeout_s = timeout_ms / 1000

    print(f"\n{'='*70}")
    print(f"  Phase 2: Live API CRUD + DB Verification")
    print(f"  Backend: {base_url}")
    print(f"  Auth: {username}")
    print(f"{'='*70}\n")

    # Resolve login endpoint from security layer definitions
    login_path = _resolve_login_path(defs)
    print(f"  Login endpoint: {login_path}")

    # Authenticate
    token = _authenticate(base_url, username, password, login_path, timeout_s)
    if not token:
        report.global_issues.append(CoverageIssue(
            entity="*", operation="auth", category="api_live",
            severity="error", message=f"Login failed for user '{username}' at {login_path} — cannot run live tests",
        ))
        print(f"  ❌ Login failed for '{username}' at {login_path} — skipping live tests\n")
        return
    print(f"  ✅ Authenticated as '{username}'\n")

    # DB config from project metadata
    db_config = defs.project_metadata.get("database")

    # Sample entities: pick non-User root entities first, then others
    # Skip User entity (auth-related, special handling)
    candidates = [ec for ec in report.entities
                  if ec.api_operations and ec.entity_name != "User"]
    sampled = candidates[:max_entities]

    print(f"  Testing {len(sampled)} entities (max {max_entities}):\n")

    for ec in sampled:
        print(f"  [{ec.entity_name}]")
        _run_entity_lifecycle(defs, ec, base_url, token, db_config, timeout_s)

        for r in ec.api_test_results:
            icon = {"pass": "✅", "fail": "❌", "warn": "⚠️"}.get(r.status, "?")
            print(f"    {icon} {r.method:6s} {r.operation:<10s} HTTP {r.status_code:3d} ({r.response_time_ms}ms)")
            if r.error_detail:
                print(f"       └─ {r.error_detail}")

        report.live_tested += 1

    # Tally live results
    for ec in report.entities:
        for r in ec.api_test_results:
            if r.status == "pass":
                report.live_passed += 1
            elif r.status == "fail":
                report.live_failed += 1
            else:
                report.live_warned += 1


# ─── Main entry point ──────────────────────────────────────────────────────

def run_api_coverage_validation(
    definitions_path: str,
    backend_url: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    max_live_entities: int = 5,
    timeout_ms: int = 15000,
) -> CoverageReport:
    """Run the full API coverage validation (Phase 1 + optional Phase 2)."""
    defs = DefinitionSet(definitions_path)
    report = CoverageReport(definitions_path=definitions_path)

    entity_names = defs.get_all_entity_names()
    report.total_entities = len(entity_names)

    # Check for missing react definitions path
    if not defs.react_path:
        report.global_issues.append(CoverageIssue(
            entity="*", operation="*", category="setup",
            severity="error",
            message="Could not find React definition files (react_routes.json etc.)",
        ))

    # Check auth config
    if defs.auth_config:
        if defs.auth_config.get("jwtEnabled") and not defs.auth_config.get("loginRoute"):
            report.global_issues.append(CoverageIssue(
                entity="*", operation="auth", category="auth",
                severity="warning",
                message="JWT is enabled but no loginRoute defined in react_auth_config.json",
            ))

    # Analyze each entity
    for entity_name in entity_names:
        ec = _analyze_entity(defs, entity_name)
        report.entities.append(ec)

    # Check for React entities that have no backend controller
    react_entities = {s["entityName"] for s in defs.api_services}
    backend_entities = set(entity_names)
    orphan_react = react_entities - backend_entities
    for orphan in orphan_react:
        report.global_issues.append(CoverageIssue(
            entity=orphan, operation="*", category="api_service",
            severity="warning",
            message=f"React API service defined for '{orphan}' but no backend controller exists",
        ))

    # Phase 2: Live API tests (if backend URL provided)
    if backend_url and username and password:
        run_live_api_tests(defs, report, backend_url, username, password,
                           max_live_entities, timeout_ms)

    # Tally
    all_issues = list(report.global_issues)
    for ec in report.entities:
        all_issues.extend(ec.issues)
    report.total_issues = len(all_issues)
    report.errors = sum(1 for i in all_issues if i.severity == "error")
    report.warnings = sum(1 for i in all_issues if i.severity == "warning")
    report.infos = sum(1 for i in all_issues if i.severity == "info")

    return report


# ─── Printing ───────────────────────────────────────────────────────────────

SEVERITY_ICON = {"error": "❌", "warning": "⚠️", "info": "ℹ️"}

def print_api_coverage_summary(report: CoverageReport):
    """Print the full API coverage report."""
    print(f"\n{'='*70}")
    print(f"  API Coverage Validator")
    print(f"  Definitions: {report.definitions_path}")
    print(f"  Entities analyzed: {report.total_entities}")
    print(f"{'='*70}\n")

    # Per-entity summary table
    print(f"  {'Entity':<35s} {'API Ops':>7s} {'Route':>5s} {'Form':>5s} {'Table':>5s} {'Redux':>5s} {'APISvc':>6s} {'Fields':>6s} {'Issues':>6s}")
    print(f"  {'-'*35} {'-'*7} {'-'*5} {'-'*5} {'-'*5} {'-'*5} {'-'*6} {'-'*6} {'-'*6}")

    for ec in report.entities:
        ops = len(ec.api_operations)
        route = "✓" if ec.has_route else "✗"
        form = "✓" if ec.has_form else "✗"
        table = "✓" if ec.has_datatable else "✗"
        redux = "✓" if ec.has_redux_thunks else "✗"
        api_svc = "✓" if ec.has_api_service else "✗"
        fields = str(ec.form_field_count)
        issues = str(len(ec.issues))
        print(f"  {ec.entity_name:<35s} {ops:>7d} {route:>5s} {form:>5s} {table:>5s} {redux:>5s} {api_svc:>6s} {fields:>6s} {issues:>6s}")

    # Global issues
    if report.global_issues:
        print(f"\n  Global Issues:")
        for issue in report.global_issues:
            icon = SEVERITY_ICON.get(issue.severity, "?")
            print(f"    {icon} [{issue.category}] {issue.message}")

    # Per-entity issues (only show entities with issues)
    entities_with_issues = [ec for ec in report.entities if ec.issues]
    if entities_with_issues:
        print(f"\n  Entity Issues:")
        for ec in entities_with_issues:
            print(f"\n    {ec.entity_name}:")
            for issue in ec.issues:
                icon = SEVERITY_ICON.get(issue.severity, "?")
                print(f"      {icon} [{issue.category}:{issue.operation}] {issue.message}")

    # Live API test failures
    entities_with_live_fails = [ec for ec in report.entities
                                if any(r.status == "fail" for r in ec.api_test_results)]
    if entities_with_live_fails:
        print(f"\n  Live API Failures:")
        for ec in entities_with_live_fails:
            for r in ec.api_test_results:
                if r.status == "fail":
                    print(f"    ❌ {ec.entity_name}.{r.operation} {r.method} {r.path} → HTTP {r.status_code}")
                    if r.error_detail:
                        print(f"       └─ {r.error_detail}")

    # Summary
    print(f"\n{'='*70}")
    print(f"  COVERAGE RESULTS: {report.errors} errors, {report.warnings} warnings, {report.infos} info")
    print(f"  Total entities: {report.total_entities}, Total issues: {report.total_issues}")
    if report.live_tested > 0:
        total_live = report.live_passed + report.live_failed + report.live_warned
        print(f"  Live API tests: {report.live_passed} passed, {report.live_failed} failed, {report.live_warned} warnings ({total_live} total across {report.live_tested} entities)")
    print(f"{'='*70}\n")

    if report.errors == 0 and report.live_failed == 0:
        print("  🎉 Full API coverage — every backend operation has matching React UI components.\n")
    else:
        print("  ⚡ Some API operations lack required React UI components.\n")
