"""Unified workflow script for two-phase application generation.

This script combines Phase 1 and Phase 2 into a single command.
Supports both JSON file and MySQL database storage backends.
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

from phase1_generate_definition import load_or_parse_definition, save_application_definition, print_summary
from phase2_generate_code import load_application_definition, load_from_db
from main import generate_application


def main():
    """Main entry point for unified two-phase workflow."""
    parser = argparse.ArgumentParser(
        description='Generate Spring WebFlux application (two-phase workflow)'
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
        help='Output directory for generated application (default: ../generated_application/<db_name>_<timestamp>)'
    )
    parser.add_argument(
        '--phase',
        '-p',
        choices=['1', '2', 'both'],
        default='both',
        help='Which phase to run: 1 (definition only), 2 (code only), both (default)'
    )
    parser.add_argument(
        '--storage',
        '-s',
        choices=['json', 'db', 'both'],
        default='json',
        help='Storage backend: json (default), db (MySQL), both'
    )
    parser.add_argument(
        '--app-id',
        type=int,
        default=None,
        help='App definition ID (for --storage db with --phase 2)'
    )
    parser.add_argument(
        '--db-config',
        default=None,
        help='Path to DB config file (default: ~/.swfaw/db_config.json)'
    )
    parser.add_argument(
        '--with-react',
        action='store_true',
        default=False,
        help='After swfaw Phase 2, run REAW (both phases) to generate a React frontend'
    )
    parser.add_argument(
        '--react-definition-only',
        action='store_true',
        default=False,
        help='After swfaw Phase 2, run only REAW Phase 1 to generate React Application Definition'
    )
    
    args = parser.parse_args()

    # Validate mutually exclusive React flags
    if args.with_react and args.react_definition_only:
        print("Error: --with-react and --react-definition-only are mutually exclusive", file=sys.stderr)
        sys.exit(1)
    
    input_path = Path(args.input)
    app_id = args.app_id
    
    # Phase 1: Generate or load application definition
    if args.phase in ['1', 'both']:
        print("\n" + "="*60)
        print("PHASE 1: GENERATE APPLICATION DEFINITION")
        print("="*60 + "\n")
        
        db_def = load_or_parse_definition(args.input)
        
        # Generate default output path if not provided
        if args.output is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            db_name = db_def.projectMetadata.database.name
            args.output = f'../generated_application/{db_name}_{timestamp}'
        
        # Save definition to output directory using selected storage
        result = save_application_definition(
            db_def, args.output,
            storage=args.storage, db_config=args.db_config,
        )
        print_summary(db_def)

        # Capture app_id if saved to DB (for Phase 2)
        if args.storage in ('db', 'both') and result and result.isdigit():
            app_id = int(result)
        
        if args.phase == '1':
            print(f">> Phase 1 complete. Definition saved.")
            if args.storage in ('json', 'both'):
                print(f">> To generate code, run:")
                print(f"   python phase2_generate_code.py --output {args.output}")
            if app_id:
                print(f">> Or from database:")
                print(f"   python phase2_generate_code.py --output {args.output} --storage db --app-id {app_id}")
            return
    
    # Phase 2: Generate application code
    if args.phase in ['2', 'both']:
        print("\n" + "="*60)
        print("PHASE 2: GENERATE APPLICATION CODE")
        print("="*60 + "\n")
        
        # Ensure output directory is specified for phase 2 only
        if args.phase == '2' and args.output is None:
            print("Error: --output is required for Phase 2")
            sys.exit(1)

        # Load definition based on storage backend
        if args.phase == '2':
            if args.storage == 'db':
                if app_id is None:
                    print("Error: --app-id is required when --storage db with --phase 2")
                    sys.exit(1)
                db_def, _ = load_from_db(app_id, args.db_config)
            else:
                db_def = load_application_definition(args.output)
        else:
            # Both phases: db_def already loaded from Phase 1
            pass
        
        # Generate application
        generate_application(db_def, args.output)

    # ── REAW: React Application Writer ──
    if args.with_react or args.react_definition_only:
        try:
            import os
            import subprocess

            reaw_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'reaw')

            # React definitions go into application_definitions/ (alongside swfaw definitions)
            app_def_path = os.path.abspath(os.path.join(args.output, 'application_definitions'))

            # React app goes alongside webflux_app/
            react_app_output = os.path.abspath(os.path.join(args.output, 'react_app'))

            # REAW Phase 1
            print("\n" + "="*60)
            print("REAW PHASE 1: GENERATE REACT APPLICATION DEFINITION")
            print("="*60 + "\n")

            phase1_result = subprocess.run(
                [sys.executable, 'phase1_generate_react_definition.py',
                 '--input', app_def_path, '--output', app_def_path],
                cwd=reaw_dir,
                capture_output=False,
            )
            if phase1_result.returncode != 0:
                print("REAW Phase 1 failed.", file=sys.stderr)
                sys.exit(1)

            if args.with_react:
                # REAW Phase 2
                print("\n" + "="*60)
                print("REAW PHASE 2: GENERATE REACT SOURCE CODE")
                print("="*60 + "\n")

                phase2_result = subprocess.run(
                    [sys.executable, 'phase2_generate_react_code.py',
                     '--input', app_def_path, '--output', react_app_output],
                    cwd=reaw_dir,
                    capture_output=False,
                )
                if phase2_result.returncode != 0:
                    print("REAW Phase 2 failed.", file=sys.stderr)
                    sys.exit(1)

                print(f"React application: {react_app_output}/")

        except Exception as e:
            print(f"\nREAW Error: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            print("React generation failed. Backend code was not rolled back.", file=sys.stderr)
            sys.exit(1)


if __name__ == '__main__':
    main()
