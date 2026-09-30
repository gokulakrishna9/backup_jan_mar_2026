"""Example script demonstrating the use of Definition Managers.

This script shows how to programmatically manipulate application definitions
using the managers layer.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from managers import (
    DefinitionManager,
    EntityManager,
    FieldManager,
    RelationshipManager,
    LayerManager
)


def example_1_basic_operations():
    """Example 1: Basic CRUD operations on entities and fields."""
    print("\n" + "="*60)
    print("Example 1: Basic CRUD Operations")
    print("="*60)
    
    # Initialize managers
    def_manager = DefinitionManager("../generated_application/example_app")
    
    try:
        def_manager.load()
    except FileNotFoundError:
        print("Error: Application definition not found.")
        print("Please run Phase 1 first to generate a definition.")
        return
    
    entity_manager = EntityManager(def_manager)
    field_manager = FieldManager(def_manager)
    
    # List existing entities
    print("\nExisting entities:")
    for entity in entity_manager.list_entities():
        print(f"  - {entity}")
    
    # Add new entity
    print("\nAdding new entity 'products'...")
    if not entity_manager.entity_exists("products"):
        entity_manager.add_entity("products")
        
        # Add fields
        field_manager.add_field("products", "name", "VARCHAR(255)", nullable=False)
        field_manager.add_field("products", "description", "TEXT")
        field_manager.add_field("products", "price", "DECIMAL(10,2)", nullable=False)
        field_manager.add_field("products", "stock", "INT", default_value="0")
        
        print("  ✓ Entity created with 5 fields (including id)")
    else:
        print("  ℹ Entity already exists")
    
    # Show entity details
    details = entity_manager.get_entity_details("products")
    if details:
        print(f"\nProduct entity details:")
        print(f"  Columns: {details['column_count']}")
        for col in details['columns']:
            print(f"    - {col['name']}: {col['type']}")
    
    # Save changes
    print("\nSaving changes...")
    def_manager.save()
    print("  ✓ Changes saved successfully")


def example_2_relationships():
    """Example 2: Managing relationships between entities."""
    print("\n" + "="*60)
    print("Example 2: Managing Relationships")
    print("="*60)
    
    def_manager = DefinitionManager("../generated_application/example_app")
    
    try:
        def_manager.load()
    except FileNotFoundError:
        print("Error: Application definition not found.")
        return
    
    entity_manager = EntityManager(def_manager)
    field_manager = FieldManager(def_manager)
    rel_manager = RelationshipManager(def_manager)
    
    # Create categories entity if not exists
    if not entity_manager.entity_exists("categories"):
        print("\nCreating 'categories' entity...")
        entity_manager.add_entity("categories")
        field_manager.add_field("categories", "name", "VARCHAR(100)", nullable=False)
        field_manager.add_field("categories", "description", "TEXT")
        print("  ✓ Categories entity created")
    
    # Create products entity if not exists
    if not entity_manager.entity_exists("products"):
        print("\nCreating 'products' entity...")
        entity_manager.add_entity("products")
        field_manager.add_field("products", "name", "VARCHAR(255)", nullable=False)
        field_manager.add_field("products", "price", "DECIMAL(10,2)", nullable=False)
        field_manager.add_field("products", "category_id", "BIGINT", nullable=False)
        print("  ✓ Products entity created")
    else:
        # Add category_id if not exists
        if not field_manager.field_exists("products", "category_id"):
            field_manager.add_field("products", "category_id", "BIGINT", nullable=False)
    
    # Add relationship
    print("\nAdding relationship: products -> categories...")
    if not rel_manager.relationship_exists("products", "categories", "category_id"):
        rel_manager.add_relationship(
            "products",
            "categories",
            "ManyToOne",
            "category_id"
        )
        print("  ✓ Relationship added")
    else:
        print("  ℹ Relationship already exists")
    
    # List relationships
    print("\nProducts relationships:")
    relationships = rel_manager.list_relationships("products")
    for rel in relationships:
        print(f"  - {rel['type']}: {rel['targetTable']} via {rel['foreignKey']}")
    
    # Show incoming relationships for categories
    print("\nIncoming relationships to categories:")
    incoming = rel_manager.get_incoming_relationships("categories")
    for rel in incoming:
        print(f"  - {rel['sourceTable']} -> categories ({rel['type']})")
    
    # Save changes
    print("\nSaving changes...")
    def_manager.save()
    print("  ✓ Changes saved successfully")


def example_3_layer_customization():
    """Example 3: Customizing layer definitions."""
    print("\n" + "="*60)
    print("Example 3: Layer Customization")
    print("="*60)
    
    def_manager = DefinitionManager("../generated_application/example_app")
    
    try:
        def_manager.load()
    except FileNotFoundError:
        print("Error: Application definition not found.")
        return
    
    layer_manager = LayerManager(def_manager)
    
    # Check if User entity exists
    if not def_manager.table_exists("users"):
        print("\nNote: 'users' entity not found. Skipping User-specific customizations.")
    else:
        # Customize DTO validation
        print("\nCustomizing validation for User entity...")
        
        # Check if email field exists
        field_manager = FieldManager(def_manager)
        if field_manager.field_exists("users", "email"):
            layer_manager.update_dto_validation("User", "email", {
                "required": True,
                "requiredMessage": "Email is required for account creation",
                "email": True,
                "emailMessage": "Please provide a valid email address",
                "maxLength": 255,
                "maxLengthMessage": "Email cannot exceed 255 characters"
            })
            print("  ✓ Email validation updated")
        
        # Disable delete endpoint
        print("\nDisabling delete endpoint for User...")
        if layer_manager.disable_endpoint("User", "delete"):
            print("  ✓ Delete endpoint disabled")
        else:
            print("  ℹ Could not disable endpoint (may not exist in layer config)")
    
    # Update JWT configuration
    print("\nUpdating JWT configuration...")
    try:
        layer_manager.update_jwt_config({
            "enabled": True,
            "secret": "example-secret-key-change-in-production",
            "expiration": 3600000,  # 1 hour
            "issuer": "example-company",
            "audience": "example-users"
        })
        print("  ✓ JWT configuration updated")
    except Exception as e:
        print(f"  ℹ Could not update JWT config: {e}")
    
    # List all available layers
    print("\nAvailable layers:")
    for layer in layer_manager.list_layers():
        exists = "✓" if layer_manager.layer_exists(layer) else "✗"
        print(f"  {exists} {layer}")
    
    print("\nNote: Changes to layer definitions are saved automatically")


def example_4_project_configuration():
    """Example 4: Updating project and database configuration."""
    print("\n" + "="*60)
    print("Example 4: Project Configuration")
    print("="*60)
    
    def_manager = DefinitionManager("../generated_application/example_app")
    
    try:
        def_manager.load()
    except FileNotFoundError:
        print("Error: Application definition not found.")
        return
    
    # Show current configuration
    print("\nCurrent project metadata:")
    metadata = def_manager.get_project_metadata()
    print(f"  Name: {metadata.name}")
    print(f"  Application Name: {metadata.applicationName}")
    print(f"  Version: {metadata.version}")
    print(f"  Port: {metadata.port}")
    
    print("\nCurrent database configuration:")
    db_config = def_manager.get_database_config()
    print(f"  Type: {db_config.type}")
    print(f"  Host: {db_config.host}")
    print(f"  Port: {db_config.port}")
    print(f"  Name: {db_config.name}")
    
    # Update project metadata
    print("\nUpdating project metadata...")
    def_manager.update_project_metadata(
        applicationName="Example Application v2",
        version="2.0.0",
        port=8090
    )
    print("  ✓ Project metadata updated")
    
    # Update database configuration
    print("\nUpdating database configuration...")
    def_manager.update_database_config(
        host="localhost",
        port=3306,
        name="example_db_v2"
    )
    print("  ✓ Database configuration updated")
    
    # Show statistics
    print("\nApplication statistics:")
    stats = def_manager.get_statistics()
    print(f"  Total tables: {stats['total_tables']}")
    print(f"  Total columns: {stats['total_columns']}")
    print(f"  Tables with relationships: {stats['tables_with_relationships']}")
    print(f"  Total relationships: {stats['total_relationships']}")
    
    # Save changes
    print("\nSaving changes...")
    def_manager.save()
    print("  ✓ Changes saved successfully")


def example_5_bulk_operations():
    """Example 5: Bulk entity creation."""
    print("\n" + "="*60)
    print("Example 5: Bulk Operations")
    print("="*60)
    
    def_manager = DefinitionManager("../generated_application/example_app")
    
    try:
        def_manager.load()
    except FileNotFoundError:
        print("Error: Application definition not found.")
        return
    
    entity_manager = EntityManager(def_manager)
    field_manager = FieldManager(def_manager)
    rel_manager = RelationshipManager(def_manager)
    
    # Define entities to create
    entities_to_create = [
        {
            "name": "authors",
            "fields": [
                {"name": "first_name", "type": "VARCHAR(100)", "nullable": False},
                {"name": "last_name", "type": "VARCHAR(100)", "nullable": False},
                {"name": "email", "type": "VARCHAR(255)", "nullable": False, "unique": True},
                {"name": "bio", "type": "TEXT"}
            ]
        },
        {
            "name": "books",
            "fields": [
                {"name": "title", "type": "VARCHAR(255)", "nullable": False},
                {"name": "isbn", "type": "VARCHAR(20)", "nullable": False, "unique": True},
                {"name": "published_date", "type": "DATE"},
                {"name": "author_id", "type": "BIGINT", "nullable": False}
            ]
        }
    ]
    
    print("\nCreating entities in bulk...")
    created_count = 0
    
    for entity_def in entities_to_create:
        entity_name = entity_def["name"]
        
        if not entity_manager.entity_exists(entity_name):
            # Create entity
            entity_manager.add_entity(entity_name)
            
            # Add fields
            for field_def in entity_def["fields"]:
                field_manager.add_field(
                    entity_name,
                    field_def["name"],
                    field_def["type"],
                    nullable=field_def.get("nullable", True),
                    unique=field_def.get("unique", False)
                )
            
            created_count += 1
            print(f"  ✓ Created {entity_name} with {len(entity_def['fields'])} fields")
        else:
            print(f"  ℹ {entity_name} already exists")
    
    # Add relationship between books and authors
    if entity_manager.entity_exists("books") and entity_manager.entity_exists("authors"):
        print("\nAdding relationship: books -> authors...")
        if not rel_manager.relationship_exists("books", "authors", "author_id"):
            rel_manager.add_relationship(
                "books",
                "authors",
                "ManyToOne",
                "author_id"
            )
            print("  ✓ Relationship added")
        else:
            print("  ℹ Relationship already exists")
    
    # Save changes
    if created_count > 0:
        print(f"\nSaving changes ({created_count} entities created)...")
        def_manager.save()
        print("  ✓ Changes saved successfully")
    else:
        print("\nNo changes to save")


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("Definition Managers - Usage Examples")
    print("="*60)
    print("\nThese examples demonstrate how to use the managers layer")
    print("to programmatically manipulate application definitions.")
    print("\nNote: Make sure you have run Phase 1 to generate an")
    print("application definition before running these examples.")
    
    # Run examples
    try:
        example_1_basic_operations()
        example_2_relationships()
        example_3_layer_customization()
        example_4_project_configuration()
        example_5_bulk_operations()
        
        print("\n" + "="*60)
        print("All examples completed successfully!")
        print("="*60)
        print("\nNext steps:")
        print("1. Review the changes in application_definitions/")
        print("2. Run Phase 2 to generate code:")
        print("   python phase2_generate_code.py --output ../generated_application/example_app")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
