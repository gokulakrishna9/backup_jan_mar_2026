"""Phase 1: Generate Application Definition from SQL or JSON.

This phase creates a comprehensive application definition that includes:
- Database schema (tables, columns, relationships)
- Project metadata
- All configuration needed for Phase 2 code generation

The definition is saved to the application output folder.
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

from models.database_definition import DatabaseDefinition
from parsers.sql_parser import SQLParser
from utils.definition_splitter import split_definition
from version import __version__, MANIFEST_VERSION


def load_or_parse_definition(input_file: str) -> DatabaseDefinition:
    """Load database definition from JSON or parse from SQL."""
    input_path = Path(input_file)
    
    if not input_path.exists():
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    
    # Check file extension
    if input_path.suffix.lower() == '.sql':
        print(f">> Parsing SQL file: {input_file}")
        try:
            parser = SQLParser()
            db_def = parser.parse_file(input_file)
            print(f">> Successfully parsed SQL schema")
            return db_def
        except Exception as e:
            print(f"Error: Failed to parse SQL file: {e}")
            sys.exit(1)
    
    elif input_path.suffix.lower() == '.json':
        print(f">> Loading JSON definition: {input_file}")
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            db_def = DatabaseDefinition(**data)
            print(f">> Successfully loaded JSON definition")
            return db_def
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in input file: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Error: Failed to parse database definition: {e}")
            sys.exit(1)
    
    else:
        print(f"Error: Unsupported file type. Use .sql or .json files.")
        sys.exit(1)


def save_application_definition(db_def: DatabaseDefinition, output_dir: str,
                                storage: str = "json", db_config: str = None) -> str:
    """Save application definition using the specified storage backend(s).
    
    Args:
        db_def: Database definition to save
        output_dir: Output directory
        storage: 'json', 'db', or 'both'
        db_config: Path to DB config file (for db/both)
    
    Returns the identifier (manifest path for json, app_id for db, manifest for both).
    """
    from storage import JsonStore, DbStore

    result = None

    if storage in ('json', 'both'):
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        json_store = JsonStore()
        result = json_store.save(db_def, output_dir)
        print(f"\n>> Application definition saved to JSON files")
        print(f"   Location: {output_path / 'application_definitions'}")
        print(f"\n>> You can now modify these files before running Phase 2")

    if storage in ('db', 'both'):
        from db_managers import DbConnection
        db = DbConnection.from_config(db_config)
        db_store = DbStore(db)
        app_id = db_store.save(db_def, output_dir)
        print(f"\n>> Application definition saved to database (app_id: {app_id})")
        if storage == 'db':
            result = app_id

    return result


def print_summary(db_def: DatabaseDefinition):
    """Print summary of the application definition."""
    print(f"\n{'='*60}")
    print(f"APPLICATION DEFINITION SUMMARY")
    print(f"{'='*60}")
    print(f"Project: {db_def.projectMetadata.applicationName}")
    print(f"Group ID: {db_def.projectMetadata.groupId}")
    print(f"Artifact ID: {db_def.projectMetadata.artifactId}")
    print(f"Version: {db_def.projectMetadata.version}")
    print(f"Port: {db_def.projectMetadata.port}")
    print(f"\nDatabase:")
    print(f"  Type: {db_def.projectMetadata.database.type}")
    print(f"  Host: {db_def.projectMetadata.database.host}")
    print(f"  Port: {db_def.projectMetadata.database.port}")
    print(f"  Name: {db_def.projectMetadata.database.name}")
    print(f"\nTables: {len(db_def.tables)}")
    
    total_columns = sum(len(table.columns) for table in db_def.tables)
    print(f"Total Columns: {total_columns}")
    
    tables_with_relationships = sum(1 for table in db_def.tables if table.relationships)
    print(f"Tables with Relationships: {tables_with_relationships}")
    
    print(f"{'='*60}\n")


def main():
    """Main entry point for Phase 1."""
    print(f"\n{'='*60}")
    print(f"swfaw_v2 - Phase 1: Generate Application Definition")
    print(f"Version: {__version__} (Manifest: {MANIFEST_VERSION})")
    print(f"{'='*60}\n")
    parser = argparse.ArgumentParser(
        description='Phase 1: Generate application definition from SQL or JSON'
    )
    parser.add_argument(
        '--input',
        '-i',
        required=True,
        help='Input SQL or JSON file'
    )
    parser.add_argument(
        '--output',
        '-o',
        default=None,
        help='Output directory for application (default: ../generated_application/<db_name>_<timestamp>)'
    )
    parser.add_argument(
        '--storage',
        '-s',
        choices=['json', 'db', 'both'],
        default='json',
        help='Storage backend: json (default), db (MySQL), both'
    )
    parser.add_argument(
        '--db-config',
        default=None,
        help='Path to DB config file (default: ~/.swfaw/db_config.json)'
    )
    
    args = parser.parse_args()
    
    # Load or parse database definition
    db_def = load_or_parse_definition(args.input)
    
    # Generate default output path with timestamp if not provided
    if args.output is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        db_name = db_def.projectMetadata.database.name
        args.output = f'../generated_application/{db_name}_{timestamp}'
    
    # Save application definition to output directory
    definition_file = save_application_definition(
        db_def, args.output,
        storage=args.storage, db_config=args.db_config,
    )
    
    # Print summary
    print_summary(db_def)
    
    print(f">> Next step: Generate application code")
    print(f"   python phase2_generate_code.py --output {args.output}\n")


if __name__ == '__main__':
    main()
