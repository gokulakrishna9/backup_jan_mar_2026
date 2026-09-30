"""Example demonstrating generic JSON CRUD operations with LayerManager.

This example shows how to use the LayerManager as a generic JSON manipulation tool
instead of using specific methods for each layer.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from managers import DefinitionManager, LayerManager


def example_basic_crud():
    """Example 1: Basic CRUD operations on JSON files."""
    print("\n" + "="*60)
    print("Example 1: Basic CRUD Operations")
    print("="*60)
    
    def_manager = DefinitionManager("../generated_application/example_app")
    
    try:
        def_manager.load()
    except FileNotFoundError:
        print("Error: Application definition not found.")
        return
    
    layer_manager = LayerManager(def_manager)
    
    # GET: Read entire file
    print("\n1. GET entire security layer:")
    security = layer_manager.get("security")
    print(f"   JWT enabled: {security.get('jwt', {}).get('enabled')}")
    
    # GET: Read nested value
    print("\n2. GET nested value (jwt.expiration):")
    expiration = layer_manager.get("security", "jwt.expiration")
    print(f"   Current expiration: {expiration}ms")
    
    # SET: Update a single value
    print("\n3. SET nested value (jwt.expiration = 3600000):")
    layer_manager.set("security", "jwt.expiration", 3600000)
    print("   ✓ Updated")
    
    # UPDATE: Update multiple fields
    print("\n4. UPDATE multiple fields in jwt config:")
    layer_manager.update("security", "jwt", {
        "issuer": "my-company",
        "audience": "my-users"
    })
    print("   ✓ Updated issuer and audience")
    
    # Verify changes
    jwt_config = layer_manager.get("security", "jwt")
    print(f"\n   Final JWT config:")
    print(f"   - Expiration: {jwt_config.get('expiration')}ms")
    print(f"   - Issuer: {jwt_config.get('issuer')}")
    print(f"   - Audience: {jwt_config.get('audience')}")


def example_array_operations():
    """Example 2: Working with arrays."""
    print("\n" + "="*60)
    print("Example 2: Array Operations")
    print("="*60)
    
    def_manager = DefinitionManager("../generated_application/example_app")
    
    try:
        def_manager.load()
    except FileNotFoundError:
        print("Error: Application definition not found.")
        return
    
    layer_manager = LayerManager(def_manager)
    
    # Check if entities file exists
    if not layer_manager.exists("entities"):
        print("   ℹ Entities file not found, skipping array examples")
        return
    
    # GET: Access array element
    print("\n1. GET first entity:")
    try:
        first_entity = layer_manager.get("entities", "[0]")
        print(f"   Entity name: {first_entity.get('name')}")
    except (IndexError, KeyError):
        print("   ℹ No entities found")
        return
    
    # GET: Access nested field in array element
    print("\n2. GET nested field in array element:")
    try:
        entity_name = layer_manager.get("entities", "[0].name")
        print(f"   Name: {entity_name}")
    except (IndexError, KeyError):
        print("   ℹ Could not access entity name")
    
    # FIND: Search for specific entity
    print("\n3. FIND entity by name:")
    try:
        user_entity = layer_manager.find("entities", ".", {"name": "users"})
        if user_entity:
            print(f"   Found: {user_entity.get('name')}")
            print(f"   Columns: {len(user_entity.get('columns', []))}")
        else:
            print("   ℹ Entity 'users' not found")
    except Exception as e:
        print(f"   ℹ Error: {e}")
    
    # FILTER: Get all entities of a certain type
    print("\n4. FILTER entities (example - would need type field):")
    try:
        # This is just an example - actual structure may vary
        filtered = layer_manager.filter("entities", ".", {"type": "user_table"})
        print(f"   Found {len(filtered)} matching entities")
    except Exception as e:
        print(f"   ℹ Filter not applicable: {e}")


def example_path_navigation():
    """Example 3: Complex path navigation."""
    print("\n" + "="*60)
    print("Example 3: Complex Path Navigation")
    print("="*60)
    
    def_manager = DefinitionManager("../generated_application/example_app")
    
    try:
        def_manager.load()
    except FileNotFoundError:
        print("Error: Application definition not found.")
        return
    
    layer_manager = LayerManager(def_manager)
    
    # List all available files
    print("\n1. List all JSON files:")
    files = layer_manager.list_files()
    for f in files:
        print(f"   - {f}")
    
    # List all layer aliases
    print("\n2. List all layer aliases:")
    layers = layer_manager.list_layers()
    for layer in layers:
        exists = "✓" if layer_manager.exists(layer) else "✗"
        print(f"   {exists} {layer}")
    
    # Check if specific paths exist
    print("\n3. Check if paths exist:")
    paths_to_check = [
        ("security", "jwt"),
        ("security", "jwt.expiration"),
        ("security", "oauth2"),
        ("config", "database"),
        ("nonexistent", None)
    ]
    
    for file_name, path in paths_to_check:
        exists = layer_manager.exists(file_name, path)
        status = "✓" if exists else "✗"
        path_str = f" -> {path}" if path else ""
        print(f"   {status} {file_name}{path_str}")


def example_practical_use_cases():
    """Example 4: Practical use cases."""
    print("\n" + "="*60)
    print("Example 4: Practical Use Cases")
    print("="*60)
    
    def_manager = DefinitionManager("../generated_application/example_app")
    
    try:
        def_manager.load()
    except FileNotFoundError:
        print("Error: Application definition not found.")
        return
    
    layer_manager = LayerManager(def_manager)
    
    # Use case 1: Change JWT expiration to 1 hour
    print("\n1. Change JWT expiration to 1 hour:")
    try:
        layer_manager.set("security", "jwt.expiration", 3600000)
        print("   ✓ JWT expiration set to 1 hour")
    except Exception as e:
        print(f"   ℹ Could not update: {e}")
    
    # Use case 2: Update database configuration
    print("\n2. Update database configuration:")
    try:
        layer_manager.update("config", "database", {
            "host": "production-db.example.com",
            "port": 3306
        })
        print("   ✓ Database config updated")
    except Exception as e:
        print(f"   ℹ Could not update: {e}")
    
    # Use case 3: Disable a specific endpoint
    print("\n3. Disable delete endpoint for User entity:")
    try:
        # Find the User controller config
        user_controller = layer_manager.find("controller", ".", {"entityName": "User"})
        if user_controller:
            # This would require knowing the structure
            print("   ℹ Would need to navigate to endpoints.delete.enabled")
            # layer_manager.set("controller", "...", False)
        else:
            print("   ℹ User controller not found")
    except Exception as e:
        print(f"   ℹ Could not update: {e}")
    
    # Use case 4: Add custom validation message
    print("\n4. Add custom validation message:")
    try:
        # This is an example - actual path depends on structure
        print("   ℹ Would use: layer_manager.set('dto', 'path.to.validation.message', 'Custom message')")
    except Exception as e:
        print(f"   ℹ Could not update: {e}")


def example_comparison():
    """Example 5: Old vs New approach comparison."""
    print("\n" + "="*60)
    print("Example 5: Old vs New Approach Comparison")
    print("="*60)
    
    print("\nOLD APPROACH (specific methods):")
    print("```python")
    print("# Get security config")
    print("security = layer_manager.get_security_config()")
    print("")
    print("# Update JWT config")
    print("layer_manager.update_jwt_config({")
    print("    'expiration': 3600000,")
    print("    'issuer': 'my-company'")
    print("})")
    print("")
    print("# Disable endpoint")
    print("layer_manager.disable_endpoint('User', 'delete')")
    print("```")
    
    print("\nNEW APPROACH (generic CRUD):")
    print("```python")
    print("# Get security config")
    print("security = layer_manager.get('security')")
    print("")
    print("# Update JWT config")
    print("layer_manager.update('security', 'jwt', {")
    print("    'expiration': 3600000,")
    print("    'issuer': 'my-company'")
    print("})")
    print("")
    print("# Disable endpoint")
    print("layer_manager.set('controller', 'path.to.User.endpoints.delete.enabled', False)")
    print("# Or use find + set:")
    print("user_ctrl = layer_manager.find('controller', '.', {'entityName': 'User'})")
    print("# Then update the found object")
    print("```")
    
    print("\nBENEFITS OF NEW APPROACH:")
    print("  ✓ More flexible - works with any JSON structure")
    print("  ✓ No need to add methods for each use case")
    print("  ✓ Consistent API across all files")
    print("  ✓ Easier to maintain and extend")
    print("  ✓ Works with custom JSON files too")


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("Generic JSON CRUD with LayerManager")
    print("="*60)
    print("\nThese examples demonstrate the new generic approach")
    print("to manipulating JSON files in application definitions.")
    
    try:
        example_basic_crud()
        example_array_operations()
        example_path_navigation()
        example_practical_use_cases()
        example_comparison()
        
        print("\n" + "="*60)
        print("All examples completed!")
        print("="*60)
        print("\nThe LayerManager now provides a generic JSON CRUD interface")
        print("that works with any JSON file in the definitions directory.")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
