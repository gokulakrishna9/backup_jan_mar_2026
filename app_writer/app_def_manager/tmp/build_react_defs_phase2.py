"""Build remaining React definition files: component_mappings, api_services, redux_store, page_definitions."""
import json
from pathlib import Path

app_dir = Path("application_definitions/job_portal")

# Load entity and controller layers
entity_layer = json.loads((app_dir / "webflux_entity_layer.json").read_text(encoding="utf-8"))
controller_layer = json.loads((app_dir / "webflux_controller_layer.json").read_text(encoding="utf-8"))
service_layer = json.loads((app_dir / "webflux_service_layer.json").read_text(encoding="utf-8"))
dto_layer = json.loads((app_dir / "webflux_dto_layer.json").read_text(encoding="utf-8"))

ctrl_map = {c["entityName"]: c for c in controller_layer["controllers"]}
svc_map = {s["entityName"]: s for s in service_layer["services"]}

# ── Java type → PrimeReact component mapping ────────────────────────────────
TYPE_TO_COMPONENT = {
    "String": "InputText",
    "Integer": "InputNumber",
    "Long": "InputNumber",
    "Short": "InputNumber",
    "Float": "InputNumber",
    "Double": "InputNumber",
    "BigDecimal": "InputNumber",
    "Boolean": "Checkbox",
    "LocalDate": "Calendar",
    "LocalDateTime": "Calendar",
    "LocalTime": "Calendar",
}

# Fields with special widget overrides (from DTO fieldWidget annotations)
dto_widgets = {}  # {entityName: {fieldName: fieldWidget}}
for dto in dto_layer.get("dtos", []):
    ename = dto["entityName"]
    if ename not in dto_widgets:
        dto_widgets[ename] = {}
    for f in dto.get("fields", []):
        w = f.get("fieldWidget")
        if w:
            dto_widgets[ename][f["fieldName"]] = w

WIDGET_TO_COMPONENT = {
    "richText": "QuillEditor",
    "codeEditor": "MonacoEditor",
    "markdown": "MarkdownEditor",
}

# Auto fields to skip in component mappings
AUTO_COLS = {"created_at", "updated_at", "is_deleted"}

# singleRecordPerUser entities
single_record_entities = set()
for s in service_layer.get("services", []):
    if s.get("singleRecordPerUser"):
        single_record_entities.add(s["entityName"])

def to_camel(s):
    parts = s.split("_")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])

def to_label(field_name):
    import re
    words = re.sub(r'([a-z])([A-Z])', r'\1 \2', field_name)
    return words[0].upper() + words[1:]

# ── Component Mappings ──────────────────────────────────────────────────────
component_mappings = []
for ent in entity_layer["entities"]:
    name = ent["className"]
    fields = []
    for f in ent["fields"]:
        if f.get("isPrimaryKey"):
            continue
        if f["columnName"] in AUTO_COLS:
            continue
        
        field_name = f["fieldName"]
        java_type = f["javaType"]
        
        # Check for widget override
        widget = dto_widgets.get(name, {}).get(field_name)
        if widget and widget in WIDGET_TO_COMPONENT:
            comp_type = WIDGET_TO_COMPONENT[widget]
        else:
            comp_type = TYPE_TO_COMPONENT.get(java_type, "InputText")
        
        field_entry = {
            "fieldName": field_name,
            "fieldLabel": to_label(field_name),
            "componentType": comp_type,
            "javaType": java_type,
            "columnDefinition": f.get("columnDefinition", ""),
            "props": {},
            "includeInDTO": True,
        }
        
        # Add datetime mode for LocalDateTime
        if java_type == "LocalDateTime":
            field_entry["props"]["mode"] = "datetime"
        
        # Add fieldWidget prop if present
        if widget:
            field_entry["props"]["fieldWidget"] = widget
        
        fields.append(field_entry)
    
    mapping = {
        "entityName": name,
        "fields": fields,
        "excludeSensitiveFields": [],
    }
    if name in single_record_entities:
        mapping["singleRecordPerUser"] = True
    
    component_mappings.append(mapping)

(app_dir / "react_component_mappings.json").write_text(
    json.dumps(component_mappings, indent=2), encoding="utf-8")
print(f"  ✅ react_component_mappings.json ({len(component_mappings)} entities)")

# ── API Services ────────────────────────────────────────────────────────────
api_services = []
for ent in entity_layer["entities"]:
    name = ent["className"]
    ctrl = ctrl_map.get(name, {})
    base_path = ctrl.get("basePath", f"/api/{name.lower()}s")
    endpoints = ctrl.get("endpoints", {})
    
    svc_endpoints = {}
    for ep_name, ep in endpoints.items():
        if isinstance(ep, dict) and ep.get("enabled"):
            svc_ep = {
                "enabled": True,
                "method": ep.get("method", "GET"),
            }
            if ep_name == "getAll":
                svc_ep["supportsPagination"] = ep.get("supportsPagination", True)
                svc_ep["supportsFiltering"] = ep.get("supportsFiltering", True)
                svc_ep["supportsSorting"] = ep.get("supportsSorting", True)
            svc_endpoints[ep_name] = svc_ep
    
    api_services.append({
        "entityName": name,
        "basePath": base_path,
        "endpoints": svc_endpoints,
    })

(app_dir / "react_api_services.json").write_text(
    json.dumps(api_services, indent=2), encoding="utf-8")
print(f"  ✅ react_api_services.json ({len(api_services)} services)")

# ── Redux Store ─────────────────────────────────────────────────────────────
redux_stores = []
for ent in entity_layer["entities"]:
    name = ent["className"]
    # Find PK field name
    pk_field = "id"
    for f in ent["fields"]:
        if f.get("isPrimaryKey"):
            pk_field = f["fieldName"]
            break
    
    ctrl = ctrl_map.get(name, {})
    endpoints = ctrl.get("endpoints", {})
    
    thunks = {}
    if endpoints.get("getAll", {}).get("enabled"):
        thunks["fetchAll"] = True
    if endpoints.get("getById", {}).get("enabled"):
        thunks["fetchById"] = True
    if endpoints.get("create", {}).get("enabled"):
        thunks["create"] = True
    if endpoints.get("update", {}).get("enabled"):
        thunks["update"] = True
    if endpoints.get("delete", {}).get("enabled"):
        thunks["delete"] = True
    
    has_pagination = endpoints.get("getAll", {}).get("supportsPagination", True)
    
    redux_stores.append({
        "entityName": name,
        "pkField": pk_field,
        "thunks": thunks,
        "stateShape": {"listState": True, "singleItemState": True, "mutationState": True},
        "pagination": {"currentPage": 0, "pageSize": 20, "totalCount": 0} if has_pagination else None,
    })

(app_dir / "react_redux_store.json").write_text(
    json.dumps(redux_stores, indent=2), encoding="utf-8")
print(f"  ✅ react_redux_store.json ({len(redux_stores)} stores)")

# ── Page Definitions ────────────────────────────────────────────────────────
# Standard entity page: form on top, datatable on bottom
def make_entity_page(entity_name, page_type="entity"):
    return {
        "pageId": f"{entity_name}Page",
        "pageType": page_type,
        "entityName": entity_name,
        "gridTemplate": {
            "gridTemplateRows": "auto 1fr",
            "gridTemplateColumns": "1fr",
            "gridTemplateAreas": ["form", "table"],
        },
        "componentPlacements": [
            {"componentType": "form", "entityName": entity_name, "gridArea": "form",
             "formLayout": {"columnsLg": 3, "columnsMd": 2, "columnsSm": 1,
                           "fullWidthComponentTypes": ["InputTextarea", "QuillEditor", "MonacoEditor", "MarkdownEditor", "FileUpload"]}},
            {"componentType": "dataTable", "entityName": entity_name, "gridArea": "table"},
        ],
    }

# Grouped form page (tabbed): just the form, no datatable at page level
def make_grouped_page(entity_name):
    return {
        "pageId": f"{entity_name}Page",
        "pageType": "entity",
        "entityName": entity_name,
        "gridTemplate": {
            "gridTemplateRows": "1fr",
            "gridTemplateColumns": "1fr",
            "gridTemplateAreas": ["content"],
        },
        "componentPlacements": [
            {"componentType": "groupedForm", "entityName": entity_name, "gridArea": "content"},
        ],
    }

page_definitions = []

# Grouped pages (parent entities in form groupings)
grouped_parents = {"UserProfile", "UserEducation", "TrainingProgram", "TrainingExam", "CourseQuestion"}
for name in grouped_parents:
    page_definitions.append(make_grouped_page(name))

# Standard entity pages (everything else that has a route)
routed_entities = set()
routes = json.loads((app_dir / "react_routes.json").read_text(encoding="utf-8"))
for r in routes:
    routed_entities.add(r["entityName"])

for name in routed_entities:
    if name in grouped_parents or name == "Dashboard":
        continue
    page_definitions.append(make_entity_page(name))

(app_dir / "react_page_definitions.json").write_text(
    json.dumps(page_definitions, indent=2), encoding="utf-8")
print(f"  ✅ react_page_definitions.json ({len(page_definitions)} pages)")

# ── Env config ──────────────────────────────────────────────────────────────
env_config = {
    "variables": [
        {"key": "VITE_API_BASE_URL", "value": "http://localhost:8081", "comment": "Backend API base URL"},
        {"key": "VITE_APP_NAME", "value": "Job Portal", "comment": "Application display name"},
    ]
}
(app_dir / "react_env_config.json").write_text(
    json.dumps(env_config, indent=2), encoding="utf-8")
print("  ✅ react_env_config.json")

print(f"\n✅ All React Phase 2 definition files created!")
