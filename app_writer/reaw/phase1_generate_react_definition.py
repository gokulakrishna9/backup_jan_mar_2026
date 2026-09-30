"""Phase 1 entry point — generates React Application Definition from swfaw application definitions.

Usage:
    py phase1_generate_react_definition.py --input <application_definitions_path> [--output <target_directory>]

Default output: writes react_*.json files directly into the same
application_definitions/ folder that was provided as input.
"""

import argparse
import os
import sys

# Ensure reaw package is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parsers.definition_parser import DefinitionParser, DefinitionParseError
from generators.phase1.react_definition_generator import ReactDefinitionGenerator


def main():
    parser = argparse.ArgumentParser(
        description="REAW Phase 1: Generate React Application Definition from swfaw application definitions."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to swfaw application_definitions/ directory",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Target output directory (default: same as --input, so react_*.json files are created alongside swfaw definitions)",
    )
    args = parser.parse_args()

    input_path = os.path.abspath(args.input)

    # Default output: write into the same application_definitions/ folder
    if args.output is None:
        output_path = input_path
    else:
        output_path = os.path.abspath(args.output)

    # Validate input path exists
    if not os.path.isdir(input_path):
        print(f"Error: Input path does not exist or is not a directory: {input_path}", file=sys.stderr)
        sys.exit(1)

    # Parse swfaw application definitions
    try:
        print(f"Parsing application definitions from: {input_path}")
        app_def = DefinitionParser.parse(input_path)
    except DefinitionParseError as e:
        print(f"Error parsing application definitions: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error during parsing: {e}", file=sys.stderr)
        sys.exit(1)

    # Generate React Application Definition
    try:
        print(f"Generating React Application Definition to: {output_path}")
        files = ReactDefinitionGenerator.generate(app_def, output_path)
        print(f"Phase 1 complete. Generated {len(files)} files:")
        for f in files:
            print(f"  {f}")
    except Exception as e:
        print(f"Error during React definition generation: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
