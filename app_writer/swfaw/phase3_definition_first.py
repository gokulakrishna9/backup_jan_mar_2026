"""Phase 3: Definition-First Pipeline — generate SQL DDL + Java code from application definitions.

Reads application definitions from ``application_definitions/<app_name>/`` and
produces both ``schema.sql`` and the full ``webflux_app/`` Java source tree.

Usage (from workspace root)::

    py swfaw/phase3_definition_first.py --app my_app --output generated_application/my_app
    py swfaw/phase3_definition_first.py --app my_app --output generated_application/my_app --full
    py swfaw/phase3_definition_first.py --app my_app --output generated_application/my_app --skip-sql
"""

import argparse
import os
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Path setup — swfaw/ must be on sys.path for generator/model/util imports,
# and the workspace root must be on sys.path for app_def_manager imports.
# ---------------------------------------------------------------------------
_SWFAW_DIR = str(Path(__file__).resolve().parent)
_WORKSPACE_ROOT = str(Path(__file__).resolve().parent.parent)

if _SWFAW_DIR not in sys.path:
    sys.path.insert(0, _SWFAW_DIR)
if _WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, _WORKSPACE_ROOT)

from utils.definition_loader import load_all_definitions, reconstruct_database_definition
from generators.ddl_generator import DDLGenerator
from utils.dependency_mapper import DependencyMapper
from generators.incremental_generator import IncrementalGenerator
from main import generate_application
from app_def_manager.status_tracker import StatusTracker
from version import __version__


def _write_sql(ddl: str, output_dir: Path, sql_file: str) -> Path:
    """Write DDL string to *output_dir*/*sql_file* and return the path."""
    output_dir.mkdir(parents=True, exist_ok=True)
    sql_path = output_dir / sql_file
    sql_path.write_text(ddl, encoding="utf-8")
    return sql_path


def _print_summary(files: list[Path], mode: str) -> None:
    """Print a human-readable summary of regenerated files."""
    print(f"\n{'='*60}")
    print(f"  Generation complete ({mode} mode)")
    print(f"  Files regenerated: {len(files)}")
    print(f"{'='*60}")
    for f in files:
        print(f"  - {f}")
    print()


def main() -> None:
    """CLI entry point for the definition-first pipeline."""
    print(f"\n{'='*60}")
    print(f"swfaw — Phase 3: Definition-First Pipeline")
    print(f"Version: {__version__}")
    print(f"{'='*60}\n")

    parser = argparse.ArgumentParser(
        description="Generate SQL schema + Java code from application definitions",
    )
    parser.add_argument("--app", "-a", required=True, help="Application name")
    parser.add_argument("--output", "-o", required=True, help="Output directory")
    parser.add_argument("--full", action="store_true", help="Force full regeneration")
    parser.add_argument("--skip-sql", action="store_true", help="Skip SQL schema generation")
    parser.add_argument("--skip-java", action="store_true", help="Skip Java code generation")
    parser.add_argument("--sql-file", default="schema.sql", help="Output SQL filename (default: schema.sql)")

    args = parser.parse_args()

    try:
        _run(args)
    except FileNotFoundError as exc:
        print(f"Error: {exc}")
        sys.exit(1)
    except ValueError as exc:
        print(f"Error: {exc}")
        sys.exit(1)
    except Exception as exc:
        print(f"Error: {exc}")
        sys.exit(1)


def _run(args: argparse.Namespace) -> None:
    """Core pipeline logic — separated from main() for testability."""
    definitions_dir = Path("application_definitions") / args.app
    output_dir = Path(args.output)

    # --- Validate definitions directory exists ---
    if not definitions_dir.is_dir():
        raise FileNotFoundError(
            f"Application definitions directory not found: {definitions_dir}"
        )

    # --- Load & validate all definitions ---
    print(f">> Loading definitions from: {definitions_dir}")
    bundle = load_all_definitions(definitions_dir)

    # --- Dirty/clean status ---
    status_tracker = StatusTracker(definitions_dir)
    dirty_files = status_tracker.get_dirty_files()
    status_file_exists = status_tracker.status_path.exists()
    prior_generation_exists = (output_dir / "webflux_app").is_dir()

    # --- Determine generation mode ---
    use_full = (
        args.full
        or (not dirty_files and not status_file_exists)
        or not prior_generation_exists
    )

    if use_full:
        if args.full:
            print(">> Mode: FULL (--full flag)")
        elif not status_file_exists:
            print(">> Mode: FULL (no status file found)")
        elif not prior_generation_exists:
            print(">> Mode: FULL (no prior webflux_app/ found — falling back)")
        regenerated = _full_generation(bundle, output_dir, status_tracker, args)
    else:
        print(">> Mode: INCREMENTAL")
        regenerated = _incremental_generation(
            bundle, dirty_files, output_dir, status_tracker, args,
        )

    _print_summary(regenerated, "full" if use_full else "incremental")


def _full_generation(
    bundle,
    output_dir: Path,
    status_tracker: StatusTracker,
    args: argparse.Namespace,
) -> list[Path]:
    """Perform a full generation: DDL + all Java code."""
    regenerated: list[Path] = []

    # --- SQL DDL ---
    if not args.skip_sql:
        print(">> Generating SQL DDL schema...")
        ddl = DDLGenerator().generate_schema(
            bundle.entity_layer, bundle.relationships, bundle.project_metadata,
        )
        sql_path = _write_sql(ddl, output_dir, args.sql_file)
        regenerated.append(sql_path)
        print(f"   Written: {sql_path}")

        # Append document storage DDL if present
        if bundle.document_storage_layer is not None:
            from generators.document_storage_schema_generator import DocumentStorageSchemaGenerator
            doc_storage_ddl = DocumentStorageSchemaGenerator.generate(bundle.document_storage_layer)
            if doc_storage_ddl:
                with open(sql_path, "a", encoding="utf-8") as f:
                    f.write("\n\n" + doc_storage_ddl)
                print(f"   Appended document storage DDL to: {sql_path}")

    # --- Java code ---
    if not args.skip_java:
        print(">> Reconstructing DatabaseDefinition for Phase 2 generator...")
        db_def = reconstruct_database_definition(bundle)
        print(">> Generating full Java application via generate_application()...")
        app_defs_dir = str(Path("application_definitions") / args.app)
        generate_application(db_def, str(output_dir), definitions_dir=app_defs_dir)
        # generate_application writes into output_dir/webflux_app/ — we note
        # the directory itself as a regenerated artefact.
        regenerated.append(output_dir / "webflux_app")

        # Generate document storage Java files if present
        if bundle.document_storage_layer is not None:
            from generators.file_storage_generator import FileStorageGenerator
            from generators.json_column_generator import JsonColumnGenerator
            from utils.file_writer import create_directory_structure

            code_dir = output_dir / "webflux_app"
            package_name = bundle.project_metadata["projectMetadata"]["groupId"]
            dirs = create_directory_structure(str(code_dir), package_name)

            print(">> Generating document storage Java files...")
            fs_paths = FileStorageGenerator.generate(
                bundle.document_storage_layer, bundle.entity_layer, package_name, dirs,
            )
            for p in fs_paths:
                print(f"   Written: {p}")
            regenerated.extend(fs_paths)

            jc_paths = JsonColumnGenerator.generate(
                bundle.document_storage_layer, bundle.entity_layer, package_name, dirs,
            )
            for p in jc_paths:
                print(f"   Written: {p}")
            regenerated.extend(jc_paths)

        # Generate AI layer Java files if present
        if bundle.ai_layer is not None:
            try:
                from generators.ai_generator import AiGenerator
                print(">> Generating AI layer Java files...")
                ai_gen = AiGenerator()
                ai_paths = ai_gen.generate(bundle, output_dir)
                for p in ai_paths:
                    print(f"   Written: {p}")
                regenerated.extend(ai_paths)
            except ImportError:
                print(">> Skipping AI generation (ai_generator module not yet available)")

    # --- Mark all clean ---
    status_tracker.mark_all_clean()
    print(">> All definition files marked clean.")

    return regenerated


def _incremental_generation(
    bundle,
    dirty_files: list[str],
    output_dir: Path,
    status_tracker: StatusTracker,
    args: argparse.Namespace,
) -> list[Path]:
    """Perform incremental generation based on dirty files."""
    regenerated: list[Path] = []

    dep_mapper = DependencyMapper()
    affected = dep_mapper.resolve_affected_outputs(dirty_files, bundle)

    # --- SQL DDL (if needed) ---
    if not args.skip_sql and affected.regenerate_sql:
        print(">> Regenerating SQL DDL schema (entity/relationship changes detected)...")
        ddl = DDLGenerator().generate_schema(
            bundle.entity_layer, bundle.relationships, bundle.project_metadata,
        )
        sql_path = _write_sql(ddl, output_dir, args.sql_file)
        regenerated.append(sql_path)
        print(f"   Written: {sql_path}")

        # Append document storage DDL if present
        if bundle.document_storage_layer is not None:
            from generators.document_storage_schema_generator import DocumentStorageSchemaGenerator
            doc_storage_ddl = DocumentStorageSchemaGenerator.generate(bundle.document_storage_layer)
            if doc_storage_ddl:
                with open(sql_path, "a", encoding="utf-8") as f:
                    f.write("\n\n" + doc_storage_ddl)
                print(f"   Appended document storage DDL to: {sql_path}")

    # --- Java code (affected entities only) ---
    if not args.skip_java and affected.affected_entities:
        print(f">> Regenerating Java code for {len(affected.affected_entities)} affected entities...")
        incr_gen = IncrementalGenerator()
        paths = incr_gen.regenerate_affected(bundle, affected, output_dir)
        regenerated.extend(paths)
        for p in paths:
            print(f"   Written: {p}")

    # --- AI layer (if webflux_ai_layer.json is dirty) ---
    if not args.skip_java and "webflux_ai_layer.json" in dirty_files:
        if bundle.ai_layer is not None:
            try:
                from generators.ai_generator import AiGenerator
                print(">> Regenerating AI layer Java files...")
                ai_gen = AiGenerator()
                ai_paths = ai_gen.regenerate(bundle, output_dir)
                for p in ai_paths:
                    print(f"   Written: {p}")
                regenerated.extend(ai_paths)
            except ImportError:
                print(">> Skipping AI regeneration (ai_generator module not yet available)")

    # --- Mark only the dirty files clean ---
    status_tracker.mark_clean(dirty_files)
    print(f">> Marked {len(dirty_files)} dirty file(s) clean.")

    return regenerated


if __name__ == "__main__":
    main()
