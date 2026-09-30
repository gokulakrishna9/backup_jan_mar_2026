"""Utility to extract filter and query data from swfaw application definitions.

Reads webflux_filter_layer.json and webflux_query_layer.json from the
application_definitions/ folder and converts them to the dict format
expected by Phase 2 generators (FilterComponentGenerator, QueryComponentGenerator).
"""

import json
import os
from typing import Dict, List, Tuple


def extract_filter_entities(app_def_path: str) -> Dict[str, List[Dict]]:
    """Extract filter field dicts from webflux_filter_layer.json.

    Returns:
        Dict of entityName → list of filter field dicts, e.g.:
        {"User": [{"name": "firstName", "type": "String", "operators": ["equals", "contains"]}]}
    """
    filter_path = os.path.join(app_def_path, "webflux_filter_layer.json")
    if not os.path.isfile(filter_path):
        return {}

    with open(filter_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    result: Dict[str, List[Dict]] = {}
    for entity_name, entity_def in data.get("filters", {}).items():
        fields = entity_def if isinstance(entity_def, list) else entity_def.get("fields", [])
        if fields:
            result[entity_name] = fields

    return result


def extract_query_entities(app_def_path: str) -> Dict[str, List[Dict]]:
    """Extract query dicts from webflux_query_layer.json.

    Returns:
        Dict of entityName → list of query dicts, e.g.:
        {"User": [{"name": "listUser", "description": "...", "parameters": [...]}]}
    """
    query_path = os.path.join(app_def_path, "webflux_query_layer.json")
    if not os.path.isfile(query_path):
        return {}

    with open(query_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    result: Dict[str, List[Dict]] = {}
    for entity_name, queries in data.get("queries", {}).items():
        if queries:
            result[entity_name] = queries

    return result


def extract_filter_and_query(app_def_path: str) -> Tuple[Dict[str, List[Dict]], Dict[str, List[Dict]]]:
    """Convenience: extract both filter and query data in one call."""
    return extract_filter_entities(app_def_path), extract_query_entities(app_def_path)
