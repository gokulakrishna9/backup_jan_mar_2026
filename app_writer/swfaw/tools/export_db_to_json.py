"""Export a database-stored application definition back to JSON files.

Usage:
    cd emotisense-ai/swfaw
    python tools/export_db_to_json.py --app-id 1 --output ../generated_application/my_app_export
    python tools/export_db_to_json.py --app-id 1 --output ../generated_application/my_app_export --db-config ~/.swfaw/db_config.json
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path so we can import swfaw modules
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from storage import JsonStore, DbStore
from db_managers import DbConnection


def main():
    parser = argparse.ArgumentParser(
        description='Export database application definition to JSON files'
    )
    parser.add_argument(
        '--app-id', type=int, required=True,
        help='App definition ID in the database'
    )
    parser.add_argument(
        '--output', '-o', required=True,
        help='Output directory for JSON files'
    )
    parser.add_argument(
        '--db-config', default=None,
        help='Path to DB config file (default: ~/.swfaw/db_config.json)'
    )

    args = parser.parse_args()

    # Load from DB
    print(f">> Loading definition from database (app_id: {args.app_id})")
    db = DbConnection.from_config(args.db_config)
    db_store = DbStore(db)
    db_def = db_store.load(str(args.app_id))

    print(f"   Project: {db_def.projectMetadata.applicationName}")
    print(f"   Tables: {len(db_def.tables)}")

    # Save to JSON
    print(f"\n>> Exporting to JSON: {args.output}")
    json_store = JsonStore()
    manifest = json_store.save(db_def, args.output)

    print(f"\n>> Export complete. Manifest: {manifest}")
    print(f"   To generate code from JSON:")
    print(f"   python phase2_generate_code.py --output {args.output}")


if __name__ == '__main__':
    main()
