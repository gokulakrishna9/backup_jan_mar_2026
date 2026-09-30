"""Unified entry point — runs Phase 1 then Phase 2 sequentially.

Usage:
    py generate_react_app.py --input <application_definitions_path> --output <target_directory>

Default output mirrors the swfaw convention:
    ../generated_application/<db_name>_<timestamp>

Phase 1 writes react definition JSONs into:
    <output>/application_definitions/

Phase 2 writes the generated React app into:
    <output>/react_app
"""

import argparse
import json
import os
import sys
from datetime import datetime

# Ensure reaw package is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parsers.definition_parser import DefinitionParser, DefinitionParseError
from generators.phase1.react_definition_generator import ReactDefinitionGenerator
from parsers.react_definition_parser import ReactDefinitionParser, ReactDefinitionParseError
from generators.phase2.react_code_generator import ReactCodeGenerator
from utils.filter_query_extractor import extract_filter_and_query


def _resolve_db_name(input_path: str) -> str:
    """Try to extract the database name from the application definitions."""
    manifest_path = os.path.join(input_path, "webflux_manifest.json")
    if os.path.isfile(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        # manifest.files is a dict of concern → filename (strings, not dicts)
        files = manifest.get("files", {})
        pm_file = files.get("project_metadata")
        if pm_file:
            pm_path = os.path.join(input_path, pm_file)
            if os.path.isfile(pm_path):
                with open(pm_path, "r", encoding="utf-8") as f:
                    pm = json.load(f)
                db_name = pm.get("database", {}).get("name", "")
                if db_name:
                    return db_name
    return "app"


def main():
    parser = argparse.ArgumentParser(
        description="REAW: Generate a complete React application from swfaw application definitions."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to swfaw application_definitions/ directory",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Target output directory (default: ../generated_application/<db_name>_<timestamp>)",
    )
    args = parser.parse_args()

    input_path = os.path.abspath(args.input)

    # Validate input path exists
    if not os.path.isdir(input_path):
        print(f"Error: Input path does not exist or is not a directory: {input_path}", file=sys.stderr)
        sys.exit(1)

    # Resolve db_name for default paths
    db_name = _resolve_db_name(input_path)

    # Default output: same convention as swfaw
    if args.output is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output = os.path.join("..", "generated_application", f"{db_name}_{timestamp}")

    output_path = os.path.abspath(args.output)

    # React definitions go into application_definitions/react_application_definition/
    react_def_output = os.path.join(output_path, "application_definitions")

    # React app goes alongside webflux_app/
    react_app_path = os.path.join(output_path, "react_app")

    # ── Phase 1: Generate React Application Definition ──
    try:
        print(f"[Phase 1] Parsing application definitions from: {input_path}")
        app_def = DefinitionParser.parse(input_path)
    except DefinitionParseError as e:
        print(f"[Phase 1] Error parsing application definitions: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[Phase 1] Unexpected error during parsing: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        print(f"[Phase 1] Generating React Application Definition to: {react_def_output}")
        phase1_files = ReactDefinitionGenerator.generate(app_def, react_def_output)
        print(f"[Phase 1] Complete. Generated {len(phase1_files)} definition files.")
    except Exception as e:
        print(f"[Phase 1] Error during React definition generation: {e}", file=sys.stderr)
        sys.exit(1)

    # ── Phase 2: Generate React Source Code ──
    try:
        print(f"[Phase 2] Parsing React Application Definition from: {react_def_output}")
        react_def = ReactDefinitionParser.parse(react_def_output)
    except ReactDefinitionParseError as e:
        print(f"[Phase 2] Error parsing React definition: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[Phase 2] Unexpected error during parsing: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        # Extract filter/query data from swfaw definitions
        filter_entities, query_entities = extract_filter_and_query(input_path)

        # Load AI layer definition if present (for AI React component generation)
        ai_layer = None
        ai_layer_file = os.path.join(input_path, "webflux_ai_layer.json")
        if os.path.isfile(ai_layer_file):
            try:
                with open(ai_layer_file, "r", encoding="utf-8") as f:
                    ai_layer = json.load(f)
            except (json.JSONDecodeError, UnicodeDecodeError):
                print("[Phase 2] Warning: invalid webflux_ai_layer.json, skipping AI generation")

        print(f"[Phase 2] Generating React application to: {react_app_path}")
        print(f"[Phase 2] Filter entities: {len(filter_entities)}, Query entities: {len(query_entities)}")
        phase2_files = ReactCodeGenerator.generate(react_def, react_app_path, filter_entities, query_entities, ai_layer=ai_layer)
        print(f"[Phase 2] Complete. Generated {len(phase2_files)} source files.")
        print(f"\nTotal: {len(phase1_files) + len(phase2_files)} files generated.")
        print(f"React definitions: {react_def_output}/")
        print(f"React application: {react_app_path}/")
    except Exception as e:
        print(f"[Phase 2] Error during React code generation: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
