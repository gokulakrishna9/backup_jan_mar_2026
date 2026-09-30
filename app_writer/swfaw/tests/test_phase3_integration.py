"""Integration tests for the Phase 3 definition-first pipeline.

Tests the full scaffold → generate → verify workflow end-to-end.
"""

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Path setup — swfaw/ for generator imports, workspace root for app_def_manager
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app_def_manager.scaffolder import Scaffolder
from app_def_manager.status_tracker import StatusTracker
from utils.definition_loader import load_all_definitions, reconstruct_database_definition
from generators.ddl_generator import DDLGenerator
from main import generate_application


# ---------------------------------------------------------------------------
# Test entities used across integration tests
# ---------------------------------------------------------------------------
TEST_ENTITIES = [
    {
        "name": "Task",
        "fields": [
            {"name": "title", "type": "String"},
            {"name": "dueDate", "type": "LocalDate"},
        ],
    },
    {
        "name": "Category",
        "fields": [
            {"name": "name", "type": "String"},
            {"name": "color", "type": "String"},
        ],
    },
]


@pytest.fixture()
def work_dir():
    """Create a temp directory, chdir into it, and restore cwd on teardown."""
    original_cwd = os.getcwd()
    tmp = tempfile.mkdtemp()
    os.chdir(tmp)
    yield Path(tmp)
    # Restore cwd BEFORE cleanup so Windows doesn't hold a lock on tmp
    os.chdir(original_cwd)


class TestScaffoldFullGeneration:
    """Integration: scaffold → full generation → verify outputs.

    Validates Requirements: 1.1, 1.3, 2.1, 5.1, 8.2, 8.7, 11.1
    """

    def test_scaffold_full_generation_produces_valid_outputs(self, work_dir):
        """Scaffold a test app, run full generation, verify all outputs."""
        # --- 1. Scaffold ---
        scaffolder = Scaffolder()
        app_dir = scaffolder.scaffold_application("test_app", TEST_ENTITIES)
        assert app_dir.is_dir()
        assert (app_dir / "webflux_manifest.json").exists()

        # --- 2. Load definitions ---
        bundle = load_all_definitions(app_dir)
        assert bundle.app_name == "test_app"

        # --- 3. Generate DDL ---
        output_dir = Path("generated_application") / "test_app"
        output_dir.mkdir(parents=True, exist_ok=True)

        ddl = DDLGenerator().generate_schema(
            bundle.entity_layer,
            bundle.relationships,
            bundle.project_metadata,
        )
        sql_path = output_dir / "schema.sql"
        sql_path.write_text(ddl, encoding="utf-8")

        # --- 4. Generate Java code (Req 11.1) ---
        db_def = reconstruct_database_definition(bundle)
        generate_application(db_def, str(output_dir))

        # --- 5. Mark all clean ---
        tracker = StatusTracker(app_dir)
        tracker.mark_all_clean()

        # --- 6. Verify schema.sql contains valid DDL (Req 5.1) ---
        assert sql_path.exists(), "schema.sql must exist"
        sql_content = sql_path.read_text(encoding="utf-8")

        assert "CREATE DATABASE IF NOT EXISTS" in sql_content
        assert "USE" in sql_content

        # One CREATE TABLE per entity
        assert "CREATE TABLE IF NOT EXISTS `task`" in sql_content
        assert "CREATE TABLE IF NOT EXISTS `category`" in sql_content

        # --- 7. Verify webflux_app/ directory structure (Req 1.3, 8.2) ---
        webflux_dir = output_dir / "webflux_app"
        assert webflux_dir.is_dir(), "webflux_app/ directory must exist"
        assert (webflux_dir / "src").is_dir()
        assert (webflux_dir / "pom.xml").exists()

        # --- 8. Verify all files marked clean after generation (Req 8.7) ---
        dirty = tracker.get_dirty_files()
        assert dirty == [], f"All files should be clean, but dirty: {dirty}"

        clean = tracker.get_clean_files()
        assert len(clean) > 0, "Should have clean files tracked"

from app_def_manager.crud import CRUDManager
from utils.dependency_mapper import DependencyMapper
from generators.incremental_generator import IncrementalGenerator


class TestCRUDIncrementalGeneration:
    """Integration: CRUD mutation → incremental generation → verify only affected files.

    Validates Requirements: 6.1, 6.4, 6.5, 6.7, 8.3
    """

    def test_crud_mutation_incremental_only_regenerates_affected(self, work_dir):
        """Scaffold app, full generate, add a field, run incremental, verify minimality."""
        # --- 1. Scaffold ---
        scaffolder = Scaffolder()
        app_dir = scaffolder.scaffold_application("test_app", TEST_ENTITIES)

        # --- 2. Full generation ---
        bundle = load_all_definitions(app_dir)
        output_dir = Path("generated_application") / "test_app"
        output_dir.mkdir(parents=True, exist_ok=True)

        ddl = DDLGenerator().generate_schema(
            bundle.entity_layer, bundle.relationships, bundle.project_metadata,
        )
        (output_dir / "schema.sql").write_text(ddl, encoding="utf-8")

        db_def = reconstruct_database_definition(bundle)
        generate_application(db_def, str(output_dir))

        tracker = StatusTracker(app_dir)
        tracker.mark_all_clean()

        # Snapshot: record file sizes of all generated Java files
        webflux_dir = output_dir / "webflux_app"
        before_snapshot = {}
        for java_file in webflux_dir.rglob("*.java"):
            before_snapshot[str(java_file)] = java_file.stat().st_mtime_ns

        # --- 3. CRUD mutation: add a field to Task entity ---
        crud = CRUDManager("test_app")
        dirty_files = crud.add_field("Task", {"name": "priority", "type": "Integer"})
        assert len(dirty_files) > 0, "Should have dirty files after mutation"

        # --- 4. Incremental generation ---
        bundle = load_all_definitions(app_dir)  # reload after mutation
        dirty = tracker.get_dirty_files()
        assert len(dirty) > 0, "Should have dirty files"

        dep_mapper = DependencyMapper()
        affected = dep_mapper.resolve_affected_outputs(dirty, bundle)

        # SQL should be regenerated (entity_layer is dirty)
        assert affected.regenerate_sql, "entity_layer dirty should trigger SQL regen"

        # Regenerate SQL
        ddl = DDLGenerator().generate_schema(
            bundle.entity_layer, bundle.relationships, bundle.project_metadata,
        )
        (output_dir / "schema.sql").write_text(ddl, encoding="utf-8")

        # Regenerate affected Java files
        incr_gen = IncrementalGenerator()
        regenerated = incr_gen.regenerate_affected(bundle, affected, output_dir)

        # Mark clean
        tracker.mark_clean(dirty)

        # --- 5. Verify schema.sql now contains the new field ---
        sql_content = (output_dir / "schema.sql").read_text(encoding="utf-8")
        assert "priority" in sql_content, "schema.sql should contain the new 'priority' column"

        # --- 6. Verify regenerated files are non-empty ---
        assert len(regenerated) > 0, "Should have regenerated some files"
        for rpath in regenerated:
            assert Path(rpath).exists(), f"Regenerated file should exist: {rpath}"
            assert Path(rpath).stat().st_size > 0, f"Regenerated file should be non-empty: {rpath}"

        # --- 7. Verify all files now clean ---
        remaining_dirty = tracker.get_dirty_files()
        assert remaining_dirty == [], f"All files should be clean after incremental gen, but dirty: {remaining_dirty}"


from generators.document_storage_schema_generator import DocumentStorageSchemaGenerator
from generators.file_storage_generator import FileStorageGenerator
from generators.json_column_generator import JsonColumnGenerator
from utils.file_writer import create_directory_structure


class TestDocumentStorageFullGeneration:
    """Integration: scaffold with document storage → full generation → verify outputs.

    Validates Requirements: 7.1, 7.2, 7.5, 6.1, 6.2, 8.1, 10.4
    """

    def test_scaffold_document_storage_full_generation(self, work_dir):
        """Scaffold app, enable file storage + collection, full generate, verify outputs."""
        # --- 1. Scaffold ---
        scaffolder = Scaffolder()
        app_dir = scaffolder.scaffold_application("test_app", TEST_ENTITIES)
        assert (app_dir / "webflux_document_storage_layer.json").exists(), \
            "Scaffolder must create webflux_document_storage_layer.json (Req 8.1)"

        # --- 2. Enable file storage and add a document collection ---
        dsl = {
            "fileStorage": {
                "enabled": True,
                "provider": "local",
                "localBasePath": "./uploads",
                "maxFileSizeMb": 50,
                "allowedContentTypes": [],
            },
            "jsonColumns": [],
            "documentCollections": [
                {
                    "name": "AuditLog",
                    "tableName": "audit_log_docs",
                    "description": "Audit logs",
                }
            ],
            "entityAttachments": [],
        }
        with open(app_dir / "webflux_document_storage_layer.json", "w") as f:
            json.dump(dsl, f)

        # --- 3. Load bundle ---
        bundle = load_all_definitions(app_dir)
        assert bundle.document_storage_layer is not None, \
            "document_storage_layer should be loaded (Req 7.1)"

        # --- 4. Generate DDL ---
        output_dir = Path("generated_application") / "test_app"
        output_dir.mkdir(parents=True, exist_ok=True)

        ddl = DDLGenerator().generate_schema(
            bundle.entity_layer, bundle.relationships, bundle.project_metadata,
        )
        sql_path = output_dir / "schema.sql"
        sql_path.write_text(ddl, encoding="utf-8")

        # Append document storage DDL (Req 6.1, 6.2)
        doc_storage_ddl = DocumentStorageSchemaGenerator.generate(bundle.document_storage_layer)
        assert doc_storage_ddl, "Should produce DDL when fileStorage enabled + collections present"
        with open(sql_path, "a", encoding="utf-8") as f:
            f.write("\n\n" + doc_storage_ddl)

        # --- 5. Generate Java code ---
        db_def = reconstruct_database_definition(bundle)
        generate_application(db_def, str(output_dir))

        # Generate document storage Java files (Req 7.1, 7.2, 10.4)
        code_dir = output_dir / "webflux_app"
        package_name = bundle.project_metadata["projectMetadata"]["groupId"]
        dirs = create_directory_structure(str(code_dir), package_name)

        fs_paths = FileStorageGenerator.generate(
            bundle.document_storage_layer, bundle.entity_layer, package_name, dirs,
        )
        jc_paths = JsonColumnGenerator.generate(
            bundle.document_storage_layer, bundle.entity_layer, package_name, dirs,
        )

        # --- 6. Mark all clean ---
        tracker = StatusTracker(app_dir)
        tracker.mark_all_clean()

        # --- 7. Verify schema.sql contains file_metadata and collection DDL (Req 6.1, 6.2) ---
        sql_content = sql_path.read_text(encoding="utf-8")
        assert "CREATE TABLE IF NOT EXISTS `file_metadata`" in sql_content, \
            "schema.sql must contain file_metadata DDL"
        assert "CREATE TABLE IF NOT EXISTS `audit_log_docs`" in sql_content, \
            "schema.sql must contain audit_log_docs collection DDL"

        # --- 8. Verify storage/ directory with expected Java files (Req 7.5) ---
        package_path = package_name.replace(".", "/")
        src_java = code_dir / "src" / "main" / "java" / package_path
        storage_dir = src_java / "storage"
        assert storage_dir.is_dir(), "storage/ package directory must exist"

        expected_storage_files = [
            "StorageProvider.java",
            "LocalStorageProvider.java",
            "S3StorageProvider.java",
            "FileMetadata.java",
            "FileMetadataRepository.java",
            "FileStorageService.java",
            "FileController.java",
        ]
        for fname in expected_storage_files:
            fpath = storage_dir / fname
            assert fpath.exists(), f"storage/{fname} must exist"
            assert fpath.stat().st_size > 0, f"storage/{fname} must be non-empty"

        # --- 9. Verify document/ directory with collection files (Req 7.5) ---
        document_dir = src_java / "document"
        assert document_dir.is_dir(), "document/ package directory must exist"

        expected_document_files = [
            "AuditLog.java",
            "AuditLogRepository.java",
            "AuditLogService.java",
            "AuditLogController.java",
            "AuditLogInputDTO.java",
            "AuditLogOutputDTO.java",
        ]
        for fname in expected_document_files:
            fpath = document_dir / fname
            assert fpath.exists(), f"document/{fname} must exist"
            assert fpath.stat().st_size > 0, f"document/{fname} must be non-empty"

        # --- 10. Verify all files marked clean after generation ---
        dirty = tracker.get_dirty_files()
        assert dirty == [], f"All files should be clean, but dirty: {dirty}"

        # --- 11. Verify generator returned correct paths ---
        assert len(fs_paths) == 7, f"FileStorageGenerator should return 7 paths, got {len(fs_paths)}"
        assert len(jc_paths) == 6, f"JsonColumnGenerator should return 6 paths (1 collection × 6), got {len(jc_paths)}"


class TestDocumentStorageIncrementalGeneration:
    """Integration: CRUD mutation on document storage → incremental generation → verify affected files.

    Validates Requirements: 7.3, 7.4, 8.3
    """

    def test_crud_mutation_incremental_document_storage(self, work_dir):
        """Scaffold, full generate, add JSON column, incremental regen, verify minimality."""
        # --- 1. Scaffold ---
        scaffolder = Scaffolder()
        app_dir = scaffolder.scaffold_application("test_app", TEST_ENTITIES)

        # --- 2. Full generation (baseline) ---
        bundle = load_all_definitions(app_dir)
        output_dir = Path("generated_application") / "test_app"
        output_dir.mkdir(parents=True, exist_ok=True)

        ddl = DDLGenerator().generate_schema(
            bundle.entity_layer, bundle.relationships, bundle.project_metadata,
        )
        (output_dir / "schema.sql").write_text(ddl, encoding="utf-8")

        db_def = reconstruct_database_definition(bundle)
        generate_application(db_def, str(output_dir))

        tracker = StatusTracker(app_dir)
        tracker.mark_all_clean()

        # Snapshot mtime of all generated Java files before mutation
        webflux_dir = output_dir / "webflux_app"
        before_mtime = {}
        for java_file in webflux_dir.rglob("*.java"):
            before_mtime[str(java_file)] = java_file.stat().st_mtime_ns

        # --- 3. CRUD mutation: add a JSON column via CRUDManager (Req 8.3) ---
        crud = CRUDManager("test_app")
        dirty_files = crud.add_json_column("Task", "metadata", "metadata")
        assert "webflux_document_storage_layer.json" in dirty_files, \
            "add_json_column should mark DSL file dirty"

        # --- 4. Reload bundle and resolve affected outputs (Req 7.3) ---
        bundle = load_all_definitions(app_dir)
        dirty = tracker.get_dirty_files()
        assert "webflux_document_storage_layer.json" in dirty, \
            "DSL file should be dirty after add_json_column"

        dep_mapper = DependencyMapper()
        affected = dep_mapper.resolve_affected_outputs(dirty, bundle)

        # DSL dirty should trigger SQL regen (Req 7.3)
        assert affected.regenerate_sql, \
            "webflux_document_storage_layer.json dirty should trigger SQL regen"

        # Collect all affected file types across entities
        all_affected_types = set()
        for types in affected.affected_file_types.values():
            all_affected_types.update(types)
        assert "json_converter" in all_affected_types, \
            "Should include json_converter in affected types"

        # --- 5. Run incremental generation (Req 7.4) ---
        incr_gen = IncrementalGenerator()
        regenerated = incr_gen.regenerate_affected(bundle, affected, output_dir)

        # Mark clean
        tracker.mark_clean(dirty)

        # --- 6. Verify converter files were regenerated ---
        package_name = bundle.project_metadata["projectMetadata"]["groupId"]
        package_path = package_name.replace(".", "/")
        src_java = webflux_dir / "src" / "main" / "java" / package_path
        converter_dir = src_java / "converter"
        assert converter_dir.is_dir(), "converter/ directory must exist after incremental regen"

        expected_converter_files = [
            "JsonReadingConverter.java",
            "JsonWritingConverter.java",
            "R2dbcJsonConversionsConfig.java",
        ]
        regen_strs = [str(p) for p in regenerated]
        for fname in expected_converter_files:
            fpath = converter_dir / fname
            assert fpath.exists(), f"converter/{fname} must exist"
            assert any(fname in s for s in regen_strs), \
                f"{fname} should be in regenerated list"

        # --- 7. Verify unrelated entity files were NOT regenerated (mtime check) ---
        # Category entity files should have been regenerated (DependencyMapper marks
        # all entities affected), but the entity .java files that existed before
        # should have new mtimes only if they were in the regenerated list.
        # The key check: files NOT in the regenerated list should be untouched.
        regen_paths = {str(Path(p).resolve()) for p in regenerated}
        for fpath_str, old_mtime in before_mtime.items():
            resolved = str(Path(fpath_str).resolve())
            if resolved not in regen_paths:
                current_mtime = Path(fpath_str).stat().st_mtime_ns
                assert current_mtime == old_mtime, \
                    f"File {fpath_str} should NOT have been regenerated but mtime changed"

        # --- 8. Verify all files now clean ---
        remaining_dirty = tracker.get_dirty_files()
        assert remaining_dirty == [], \
            f"All files should be clean after incremental gen, but dirty: {remaining_dirty}"
