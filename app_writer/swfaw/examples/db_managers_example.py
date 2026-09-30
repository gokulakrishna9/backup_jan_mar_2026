"""Example usage of the db_managers module.

Demonstrates the DB-backed definition store API — same patterns as the
JSON-based managers/ but operating directly on MySQL tables.

Prerequisites:
    1. MySQL running with swfaw_definition_store database created
       (run swfaw_definition_store.sql first)
    2. pip install mysql-connector-python
    3. Optionally create ~/.swfaw/db_config.json with connection details

Usage:
    cd emotisense-ai/swfaw
    python examples/db_managers_example.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from db_managers import (
    DbConnection, DbStoreManager, DbEntityManager, DbRelationshipManager,
    DbLayerManager, DbSecurityManager, DbConfigManager, DbExceptionManager,
    DbAuditManager, DbAuthorizationManager, DbGroupManager,
    DbQueryManager, DbFilterManager, DbDtoManager,
)


def main():
    # ------------------------------------------------------------------
    # 1. Connect
    # ------------------------------------------------------------------
    # From config file (~/.swfaw/db_config.json):
    #   db = DbConnection.from_config()
    #
    # Or direct:
    db = DbConnection(
        host="localhost",
        database="swfaw_definition_store",
        user="root",
        password="password",
    )

    # ------------------------------------------------------------------
    # 2. Create an app definition (root row)
    # ------------------------------------------------------------------
    store = DbStoreManager(db)
    app_id = store.create_app(
        project_name="Pet Store",
        application_name="PetStoreApp",
        artifact_id="pet-store",
        db_name="pet_store_db",
        description="Demo pet store application",
    )
    print(f"Created app definition: id={app_id}")

    # ------------------------------------------------------------------
    # 3. Entity CRUD (swfaw_entity)
    # ------------------------------------------------------------------
    em = DbEntityManager(db, app_id)

    em.add_entity("pets", columns=[
        {"name": "id", "type": "BIGINT", "primaryKey": True, "nullable": False, "autoIncrement": True},
        {"name": "name", "type": "VARCHAR(255)", "nullable": False},
        {"name": "species", "type": "VARCHAR(100)", "nullable": False},
        {"name": "owner_id", "type": "BIGINT", "nullable": True},
    ], primary_key_column="id")

    em.add_entity("owners", columns=[
        {"name": "id", "type": "BIGINT", "primaryKey": True, "nullable": False, "autoIncrement": True},
        {"name": "name", "type": "VARCHAR(255)", "nullable": False},
        {"name": "email", "type": "VARCHAR(255)", "nullable": False, "unique": True},
    ])

    print(f"Entities: {em.list_entity_names()}")
    print(f"Pet details: {em.get_entity_details('pets')}")

    # ------------------------------------------------------------------
    # 4. Relationship CRUD (swfaw_relationship)
    # ------------------------------------------------------------------
    rm = DbRelationshipManager(db, app_id)
    rel_id = rm.add_relationship("pets", "owners", "ManyToOne", foreign_key_column="owner_id")
    print(f"Added relationship id={rel_id}")
    print(f"Pet relationships: {rm.get_relationships('pets')}")

    # ------------------------------------------------------------------
    # 5. Generic Layer Manager (any table)
    # ------------------------------------------------------------------
    lm = DbLayerManager(db, app_id)

    # Insert an entity_layer row
    lm.insert("entity_layer", {
        "table_name": "pets",
        "class_name": "Pet",
        "package_name": "com.example.entity",
        "has_audit_fields": 1,
        "has_soft_delete": 1,
    })

    # Read it back
    pet_layer = lm.find("entity_layer", {"table_name": "pets"})
    print(f"Entity layer for pets: {pet_layer}")

    # Update a single column
    lm.set("entity_layer", "has_public_flag", 1, {"table_name": "pets"})

    # Check existence
    print(f"Entity layer exists for pets: {lm.exists('entity_layer', {'table_name': 'pets'})}")
    print(f"Available table aliases: {lm.list_tables()}")

    # ------------------------------------------------------------------
    # 6. Security Manager
    # ------------------------------------------------------------------
    sm = DbSecurityManager(db, app_id)
    sm.create_config(jwt_expiration=86400000, jwt_algorithm="HS256")
    sm.update_config(jwt_issuer="pet-store", rate_limit_default_per_min=120)
    sm.set_cors(
        cors_enabled=1,
        allowed_origins_json=["http://localhost:3000", "http://localhost:8080"],
        allowed_methods_json=["GET", "POST", "PUT", "DELETE"],
    )
    sm.add_public_endpoint("/api/v1/auth/**")
    sm.add_public_endpoint("/api/v1/health")
    print(f"Security config: {sm.get_config()}")
    print(f"Public endpoints: {sm.list_public_endpoints()}")

    # ------------------------------------------------------------------
    # 7. App Config Manager
    # ------------------------------------------------------------------
    cm = DbConfigManager(db, app_id)
    cm.create_config(
        server_port=8081,
        java_version="21",
        spring_boot_version="3.3.0",
        swagger_enabled=1,
        swagger_title="Pet Store API",
    )
    cm.set_logging(log_level_root="INFO", log_level_application="DEBUG")
    print(f"App config exists: {cm.config_exists()}")

    # ------------------------------------------------------------------
    # 8. Exception Manager
    # ------------------------------------------------------------------
    exc = DbExceptionManager(db, app_id)
    exc.create_config(log_level="ERROR")
    exc.add_exception("ResourceNotFoundException", 404, "Resource not found")
    exc.add_exception("DuplicateResourceException", 409, "Resource already exists")
    exc.add_message("ResourceNotFoundException", "pets", "Pet not found")
    exc.add_message("ResourceNotFoundException", "owners", "Owner not found")
    print(f"Custom exceptions: {[e['class_name'] for e in exc.list_exceptions()]}")

    # ------------------------------------------------------------------
    # 9. Query Manager
    # ------------------------------------------------------------------
    qm = DbQueryManager(db, app_id)
    query_id = qm.add_query(
        entity_name="pets",
        query_name="findBySpecies",
        return_type="PetDto",
        select_fields=["p.id", "p.name", "p.species", "o.name AS owner_name"],
        from_clause="pets p",
        description="Find pets by species with owner info",
    )
    qm.add_join(query_id, "LEFT JOIN", "owners o", "p.owner_id = o.id")
    qm.add_parameter(query_id, "species", "String", is_required=True)
    full_query = qm.get_full_query("pets", "findBySpecies")
    print(f"Full query: {full_query['query_name']} with {len(full_query['joins'])} joins")

    # ------------------------------------------------------------------
    # 10. Filter Manager
    # ------------------------------------------------------------------
    fm = DbFilterManager(db, app_id)
    filter_id = fm.add_filter("pets")
    fm.add_field(filter_id, "name", "String", operators=["eq", "contains", "startsWith"])
    fm.add_field(filter_id, "species", "String", operators=["eq", "in"])
    full_filter = fm.get_full_filter("pets")
    print(f"Filter for pets: {len(full_filter['fields'])} fields")

    # ------------------------------------------------------------------
    # 11. Refresh statistics
    # ------------------------------------------------------------------
    stats = store.refresh_statistics(app_id)
    print(f"Stats: {stats}")

    # ------------------------------------------------------------------
    # 12. Cleanup (optional — remove the demo app)
    # ------------------------------------------------------------------
    # store.delete_app(app_id)
    # print("Cleaned up demo app")

    print("\nDone! All db_managers working correctly.")


if __name__ == "__main__":
    main()
