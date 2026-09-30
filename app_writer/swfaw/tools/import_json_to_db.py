"""Import an existing JSON application definition into the MySQL database.

Usage:
    cd emotisense-ai/swfaw
    python tools/import_json_to_db.py --input ../generated_application/my_app
    python tools/import_json_to_db.py --input ../generated_application/my_app --db-config ~/.swfaw/db_config.json
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
        description='Import JSON application definition into MySQL database'
    )
    parser.add_argument(
        '--input', '-i', required=True,
        help='Path to the generated application directory (contains application_definitions/)'
    )
    parser.add_argument(
        '--db-config', default=None,
        help='Path to DB config file (default: ~/.swfaw/db_config.json)'
    )

    args = parser.parse_args()
    input_dir = Path(args.input)

    if not (input_dir / "application_definitions" / "webflux_manifest.json").exists():
        print(f"Error: No application_definitions/webflux_manifest.json found in {input_dir}")
        sys.exit(1)

    # Load from JSON
    print(f">> Loading definition from JSON: {input_dir}")
    json_store = JsonStore()
    db_def = json_store.load(str(input_dir))

    print(f"   Project: {db_def.projectMetadata.applicationName}")
    print(f"   Tables: {len(db_def.tables)}")

    # Save to DB
    print(f"\n>> Saving to database...")
    db = DbConnection.from_config(args.db_config)
    db_store = DbStore(db)
    app_id = db_store.save(db_def, str(input_dir))

    print(f"\n>> Import complete. app_id: {app_id}")
    print(f"   To generate code from DB:")
    print(f"   python phase2_generate_code.py --output {input_dir} --storage db --app-id {app_id}")


if __name__ == '__main__':
    main()
