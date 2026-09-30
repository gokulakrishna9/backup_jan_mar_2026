"""Phase 2: Generate Spring WebFlux Application Code from Application Definition.

This phase takes the application definition from the output folder (JSON)
or from the database (MySQL) and generates all code files.
"""

import argparse
import json
import sys
from pathlib import Path

from models.database_definition import DatabaseDefinition
from utils.definition_splitter import load_split_definition
from version import __version__


def load_application_definition(output_dir: str) -> DatabaseDefinition:
    """Load application definition from split files in output directory.
    
    Expects application_definitions/ folder with webflux_manifest.json and related files.
    """
    output_path = Path(output_dir)
    definitions_dir = output_path / 'application_definitions'
    
    if not definitions_dir.exists():
        print(f"Error: Application definitions directory not found: {definitions_dir}")
        print(f"Run Phase 1 first to generate the definition.")
        sys.exit(1)
    
    manifest_file = definitions_dir / 'webflux_manifest.json'
    if not manifest_file.exists():
        print(f"Error: Manifest file not found: {manifest_file}")
        print(f"Run Phase 1 first to generate the definition.")
        sys.exit(1)
    
    print(f">> Loading application definition from: {definitions_dir}")
    try:
        return load_split_definition(output_dir)
    except Exception as e:
        print(f"Error: Failed to load application definition: {e}")
        sys.exit(1)


def load_from_db(app_id: int, db_config: str = None):
    """Load application definition and layer definitions from the database.

    Returns:
        (DatabaseDefinition, layer_definitions_dict)
    """
    from storage import DbStore
    from db_managers import DbConnection

    db = DbConnection.from_config(db_config)
    db_store = DbStore(db)
    identifier = str(app_id)

    print(f">> Loading application definition from database (app_id: {app_id})")
    db_def = db_store.load(identifier)
    layer_defs = db_store.load_layer_definitions(identifier)
    return db_def, layer_defs


def main():
    """Main entry point for Phase 2."""
    print(f"\n{'='*60}")
    print(f"swfaw_v2 - Phase 2: Generate Application Code")
    print(f"Version: {__version__}")
    print(f"{'='*60}\n")
    
    parser = argparse.ArgumentParser(
        description='Phase 2: Generate Spring WebFlux application code from definition'
    )
    parser.add_argument(
        '--output',
        '-o',
        required=True,
        help='Output directory for generated application code'
    )
    parser.add_argument(
        '--storage',
        '-s',
        choices=['json', 'db'],
        default='json',
        help='Storage backend to load from: json (default), db (MySQL)'
    )
    parser.add_argument(
        '--app-id',
        type=int,
        default=None,
        help='App definition ID (required when --storage db)'
    )
    parser.add_argument(
        '--db-config',
        default=None,
        help='Path to DB config file (default: ~/.swfaw/db_config.json)'
    )
    
    args = parser.parse_args()

    if args.storage == 'db':
        if args.app_id is None:
            print("Error: --app-id is required when --storage db")
            sys.exit(1)
        db_def, layer_defs = load_from_db(args.app_id, args.db_config)
    else:
        db_def = load_application_definition(args.output)
        layer_defs = None  # main.py will load from JSON files itself
    
    # Import and use the existing generate_application function
    from main import generate_application
    
    # Generate application in the same directory
    generate_application(db_def, args.output)


if __name__ == '__main__':
    main()
