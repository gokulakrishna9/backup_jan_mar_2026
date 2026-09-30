"""Phase 2 entry point — generates React source code from React Application Definition.

Usage:
    py phase2_generate_react_code.py --input <application_definitions_path> [--output <target_directory>]

Default output: <app_dir>/react_app (sibling to webflux_app/
within the same output directory).
"""

import argparse
import json
import os
import sys

# Ensure reaw package is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parsers.react_definition_parser import ReactDefinitionParser, ReactDefinitionParseError
from generators.phase2.react_code_generator import ReactCodeGenerator
from utils.filter_query_extractor import extract_filter_and_query


def _resolve_db_name_from_layout(react_def_path: str) -> str:
    """Try to extract db/app name from layout.json in the react definition."""
    layout_path = os.path.join(react_def_path, "react_layout.json")
    if os.path.isfile(layout_path):
        with open(layout_path, "r", encoding="utf-8") as f:
            layout = json.load(f)
        name = layout.get("applicationName", "")
        if name:
            return name.lower().replace(" ", "_").replace("-", "_")
    return "app"


def main():
    parser = argparse.ArgumentParser(
        description="REAW Phase 2: Generate React source code from React Application Definition."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to application_definitions/ directory containing react_*.json files",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Target output directory (default: ../generated_application/<db_name>_react)",
    )
    args = parser.parse_args()

    input_path = os.path.abspath(args.input)

    # Validate input path exists
    if not os.path.isdir(input_path):
        print(f"Error: Input path does not exist or is not a directory: {input_path}", file=sys.stderr)
        sys.exit(1)

    # Default output: react_app/ alongside webflux_app/
    if args.output is None:
        # Walk up from application_definitions/ → <app_dir>/
        app_dir = os.path.dirname(input_path)
        args.output = os.path.join(app_dir, "react_app")

    output_path = os.path.abspath(args.output)

    # Validate input path exists
    if not os.path.isdir(input_path):
        print(f"Error: Input path does not exist or is not a directory: {input_path}", file=sys.stderr)
        sys.exit(1)

    # Parse React Application Definition
    try:
        print(f"Parsing React Application Definition from: {input_path}")
        react_def = ReactDefinitionParser.parse(input_path)
    except ReactDefinitionParseError as e:
        print(f"Error parsing React definition: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error during parsing: {e}", file=sys.stderr)
        sys.exit(1)

    # Generate React source code
    try:
        # Extract filter/query data from swfaw definitions in the same folder
        filter_entities, query_entities = extract_filter_and_query(input_path)
        print(f"Generating React application to: {output_path}")
        print(f"  Filter entities: {len(filter_entities)}, Query entities: {len(query_entities)}")
        files = ReactCodeGenerator.generate(react_def, output_path, filter_entities, query_entities)
        print(f"Phase 2 complete. Generated {len(files)} files:")
        for f in files:
            print(f"  {f}")
    except Exception as e:
        print(f"Error during React code generation: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
