import json, os

APP_DIR = "application_definitions/online_shopping"
entities = json.load(open(os.path.join(APP_DIR, "webflux_entity_layer.json")))["entities"]

# === Query Layer ===
queries = {}
for ent in entities:
    cn = ent["className"]
    tn = ent["tableName"]
    fields = ent["fields"]
    select = ["e." + f["columnName"] for f in fields]
    queries[cn] = [{
        "name": "list" + cn,
        "description": "List all " + cn + " records",
        "returnType": cn + "OutputDTO",
        "select": select,
        "from": tn + " e",
        "joins": [],
        "where": [],
        "groupBy": [],
        "having": [],
        "orderBy": ["e." + fields[0]["columnName"] + " ASC"],
        "parameters": []
    }]

query_layer = {
    "layerType": "query",
    "description": "Custom query definitions",
    "version": "2.4.0",
    "queries": queries
}
with open(os.path.join(APP_DIR, "webflux_query_layer.json"), "w") as f:
    json.dump(query_layer, f, indent=2)
print("query_layer written")

# === Filter Layer ===
type_ops = {
    "Long": ["equals", "greaterThan", "lessThan", "between", "in"],
    "String": ["equals", "contains", "startsWith", "endsWith", "in"],
    "Integer": ["equals", "greaterThan", "lessThan", "between", "in"],
    "BigDecimal": ["equals", "greaterThan", "lessThan", "between"],
    "Boolean": ["equals"],
    "LocalDateTime": ["equals", "greaterThan", "lessThan", "between"],
}
filters = {}
for ent in entities:
    cn = ent["className"]
    flds = []
    for f in ent["fields"]:
        if f.get("isPrimaryKey"):
            continue
        ops = type_ops.get(f["javaType"], ["equals"])
        flds.append({"name": f["fieldName"], "type": f["javaType"], "operators": ops})
    filters[cn] = {"fields": flds}

filter_layer = {
    "layerType": "filter",
    "description": "Filter definitions",
    "version": "2.4.0",
    "filters": filters
}
with open(os.path.join(APP_DIR, "webflux_filter_layer.json"), "w") as f:
    json.dump(filter_layer, f, indent=2)
print("filter_layer written")

# === Group Definition Layer ===
group_layer = {
    "layerType": "group_definition",
    "description": "Access group definitions",
    "version": "1.0",
    "groupManagement": {
        "allowRuntimeCreation": False,
        "allowRuntimeDeletion": False,
        "adminCanGrantMembership": True,
        "adminCanRevokeMembership": True,
        "adminGroupName": "Administrators"
    },
    "ownerEnrollmentDefaults": {
        "ownershipCheck": "CREATOR_RECORDS",
        "maxRecordsPerUser": None,
        "allowEnroll": False,
        "allowUnenroll": False
    },
    "systemGroups": [
        {
            "groupName": "Super Administrators",
            "description": "Full system access",
            "isSuperGroup": True,
            "isDefaultGroup": False,
            "autoAssignToNewUsers": False
        },
        {
            "groupName": "Administrators",
            "description": "Can manage users and groups",
            "isSuperGroup": False,
            "isDefaultGroup": False,
            "autoAssignToNewUsers": False
        },
        {
            "groupName": "Users",
            "description": "Default user group",
            "isSuperGroup": False,
            "isDefaultGroup": True,
            "autoAssignToNewUsers": True
        }
    ],
    "entityAccess": {}
}
with open(os.path.join(APP_DIR, "webflux_group_definition_layer.json"), "w") as f:
    json.dump(group_layer, f, indent=2)
print("group_definition_layer written")
