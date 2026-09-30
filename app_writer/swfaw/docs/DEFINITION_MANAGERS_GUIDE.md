# Definition Managers Guide

## Overview

The Definition Managers layer provides programmatic CRUD operations for manipulating application definitions in swfaw_v2. This layer allows you to programmatically add, view, update, and delete elements within each layer of the application definition.

**Version:** 2.3.0  
**Location:** `emotisense-ai/swfaw_v2/managers/`

## Architecture

The managers layer consists of 5 main components:

1. **DefinitionManager** - Core manager for loading/saving definitions
2. **EntityManager** - CRUD operations on entities (tables)
3. **FieldManager** - CRUD operations on fields (columns)
4. **RelationshipManager** - CRUD operations on relationships
5. **LayerManager** - CRUD operations on layer definition files

## Installation

No additional installation required. The managers are part of swfaw_v2.

```python
from managers import (
    DefinitionManager,
    EntityManager,
    FieldManager,
    RelationshipManager,
    LayerManager
)
```

---

## 1. DefinitionManager

Core manager for loading and saving application definitions.

### Initialization

```python
from managers import DefinitionManager

# Initialize with output directory
def_manager = DefinitionManager("../generated_application/my_app")

# Load existing definition
db_def = def_manager.load()
```

### Methods

#### load()
Load application definition from the output directory.

```python
db_def = def_manager.load()
```

#### save()
Save the current application definition.

```python
file_paths = def_manager.save()
print(f"Saved to: {file_paths['manifest']}")
```

#### get_definition()
Get the current database definition object.

```python
db_def = def_manager.get_definition()
```

#### get_project_metadata()
Get project metadata.

```python
metadata = def_manager.get_project_metadata()
print(f"Project: {metadata.applicationName}")
print(f"Version: {metadata.version}")
```

#### update_project_metadata(**kwargs)
Update project metadata fields.

```python
def_manager.update_project_metadata(
    applicationName="My New App",
    version="2.0.0",
    port=8090
)
def_manager.save()
```

#### get_database_config()
Get database configuration.

```python
db_config = def_manager.get_database_config()
print(f"Database: {db_config.name}")
print(f"Host: {db_config.host}")
```

#### update_database_config(**kwargs)
Update database configuration.

```python
def_manager.update_database_config(
    host="production-db.example.com",
    port=3306,
    name="production_db"
)
def_manager.save()
```

#### list_tables()
List all table names.

```python
tables = def_manager.list_tables()
print(f"Tables: {', '.join(tables)}")
```

#### get_table(table_name)
Get a table by name.

```python
user_table = def_manager.get_table("users")
if user_table:
    print(f"Columns: {len(user_table.columns)}")
```

#### table_exists(table_name)
Check if a table exists.

```python
if def_manager.table_exists("users"):
    print("Users table exists")
```

#### get_statistics()
Get statistics about the application definition.

```python
stats = def_manager.get_statistics()
print(f"Total tables: {stats['total_tables']}")
print(f"Total columns: {stats['total_columns']}")
print(f"Total relationships: {stats['total_relationships']}")
```

---

## 2. EntityManager

CRUD operations on entities (tables).

### Initialization

```python
from managers import DefinitionManager, EntityManager

def_manager = DefinitionManager("../generated_application/my_app")
def_manager.load()

entity_manager = EntityManager(def_manager)
```

### Methods

#### add_entity(table_name, columns=None)
Add a new entity to the definition.

```python
# Add with default columns (just id)
entity_manager.add_entity("products")

# Add with custom columns
columns = [
    {
        "name": "id",
        "type": "BIGINT",
        "primaryKey": True,
        "nullable": False,
        "autoIncrement": True
    },
    {
        "name": "name",
        "type": "VARCHAR(255)",
        "nullable": False
    },
    {
        "name": "price",
        "type": "DECIMAL(10,2)",
        "nullable": False
    }
]
entity_manager.add_entity("products", columns)
def_manager.save()
```

#### remove_entity(table_name)
Remove an entity from the definition.

```python
if entity_manager.remove_entity("old_table"):
    print("Entity removed")
    def_manager.save()
```

#### update_entity(table_name, new_name=None)
Update an entity's properties.

```python
# Rename entity
entity_manager.update_entity("products", new_name="items")
def_manager.save()
```

#### get_entity(table_name)
Get an entity by name.

```python
entity = entity_manager.get_entity("users")
if entity:
    print(f"Table: {entity.name}")
    print(f"Columns: {len(entity.columns)}")
```

#### list_entities()
List all entity names.

```python
entities = entity_manager.list_entities()
for entity in entities:
    print(f"- {entity}")
```

#### entity_exists(table_name)
Check if an entity exists.

```python
if entity_manager.entity_exists("users"):
    print("Users entity exists")
```

#### get_entity_details(table_name)
Get detailed information about an entity.

```python
details = entity_manager.get_entity_details("users")
if details:
    print(f"Name: {details['name']}")
    print(f"Columns: {details['column_count']}")
    print(f"Relationships: {details['relationship_count']}")
    
    for col in details['columns']:
        print(f"  - {col['name']}: {col['type']}")
```

---

## 3. FieldManager

CRUD operations on fields (columns) within entities.

### Initialization

```python
from managers import DefinitionManager, FieldManager

def_manager = DefinitionManager("../generated_application/my_app")
def_manager.load()

field_manager = FieldManager(def_manager)
```

### Methods

#### add_field(table_name, field_name, field_type, **options)
Add a new field to an entity.

```python
# Add simple field
field_manager.add_field("users", "email", "VARCHAR(255)")

# Add field with options
field_manager.add_field(
    "users",
    "age",
    "INT",
    nullable=False,
    default_value="18"
)

# Add unique field
field_manager.add_field(
    "users",
    "username",
    "VARCHAR(100)",
    nullable=False,
    unique=True
)

def_manager.save()
```

#### remove_field(table_name, field_name)
Remove a field from an entity.

```python
if field_manager.remove_field("users", "old_column"):
    print("Field removed")
    def_manager.save()
```

#### update_field(table_name, field_name, **options)
Update a field's properties.

```python
# Rename field
field_manager.update_field("users", "email", new_name="email_address")

# Change type
field_manager.update_field("users", "age", new_type="SMALLINT")

# Update multiple properties
field_manager.update_field(
    "users",
    "email",
    nullable=False,
    unique=True
)

def_manager.save()
```

#### get_field(table_name, field_name)
Get a field by name.

```python
field = field_manager.get_field("users", "email")
if field:
    print(f"Type: {field.type}")
    print(f"Nullable: {field.nullable}")
```

#### list_fields(table_name)
List all field names in an entity.

```python
fields = field_manager.list_fields("users")
for field in fields:
    print(f"- {field}")
```

#### field_exists(table_name, field_name)
Check if a field exists.

```python
if field_manager.field_exists("users", "email"):
    print("Email field exists")
```

#### get_field_details(table_name, field_name)
Get detailed information about a field.

```python
details = field_manager.get_field_details("users", "email")
if details:
    print(f"Name: {details['name']}")
    print(f"Type: {details['type']}")
    print(f"Nullable: {details['nullable']}")
    print(f"Unique: {details['unique']}")
```

#### get_primary_keys(table_name)
Get all primary key fields.

```python
pk_fields = field_manager.get_primary_keys("users")
print(f"Primary keys: {', '.join(pk_fields)}")
```

---

## 4. RelationshipManager

CRUD operations on relationships between entities.

### Initialization

```python
from managers import DefinitionManager, RelationshipManager

def_manager = DefinitionManager("../generated_application/my_app")
def_manager.load()

rel_manager = RelationshipManager(def_manager)
```

### Methods

#### add_relationship(source_table, target_table, relationship_type, foreign_key, referenced_column="id")
Add a new relationship.

```python
# One-to-Many: User has many Orders
rel_manager.add_relationship(
    "orders",
    "users",
    "ManyToOne",
    "user_id",
    "id"
)

# One-to-One: User has one Profile
rel_manager.add_relationship(
    "profiles",
    "users",
    "OneToOne",
    "user_id"
)

def_manager.save()
```

**Relationship Types:**
- `OneToOne` - One-to-one relationship
- `OneToMany` - One-to-many relationship
- `ManyToOne` - Many-to-one relationship
- `ManyToMany` - Many-to-many relationship

#### remove_relationship(source_table, target_table, foreign_key=None)
Remove a relationship.

```python
# Remove specific relationship
rel_manager.remove_relationship("orders", "users", "user_id")

# Remove all relationships to target
rel_manager.remove_relationship("orders", "users")

def_manager.save()
```

#### update_relationship(source_table, target_table, foreign_key, **options)
Update a relationship's properties.

```python
# Change relationship type
rel_manager.update_relationship(
    "orders",
    "users",
    "user_id",
    new_type="OneToOne"
)

# Change foreign key
rel_manager.update_relationship(
    "orders",
    "users",
    "user_id",
    new_foreign_key="customer_id"
)

def_manager.save()
```

#### get_relationships(table_name)
Get all relationships for an entity.

```python
relationships = rel_manager.get_relationships("orders")
for rel in relationships:
    print(f"{rel.type}: {rel.targetTable} ({rel.foreignKey})")
```

#### get_relationship(source_table, target_table, foreign_key)
Get a specific relationship.

```python
rel = rel_manager.get_relationship("orders", "users", "user_id")
if rel:
    print(f"Type: {rel.type}")
```

#### list_relationships(table_name)
List all relationships with details.

```python
relationships = rel_manager.list_relationships("orders")
for rel in relationships:
    print(f"- {rel['type']}: {rel['targetTable']} via {rel['foreignKey']}")
```

#### relationship_exists(source_table, target_table, foreign_key)
Check if a relationship exists.

```python
if rel_manager.relationship_exists("orders", "users", "user_id"):
    print("Relationship exists")
```

#### get_incoming_relationships(table_name)
Get all relationships pointing to this entity.

```python
incoming = rel_manager.get_incoming_relationships("users")
for rel in incoming:
    print(f"{rel['sourceTable']} -> users ({rel['type']})")
```

---

## 5. LayerManager

Generic JSON CRUD operations on layer definition files (v2.3).

### Initialization

```python
from managers import DefinitionManager, LayerManager

def_manager = DefinitionManager("../generated_application/my_app")
def_manager.load()

layer_manager = LayerManager(def_manager)
```

### Core CRUD Methods

The LayerManager provides a generic interface for manipulating any JSON file using dot-notation paths.

#### get(file_name, path=None)
Get data from a JSON file, optionally at a specific path.

```python
# Get entire file
security = layer_manager.get("security")

# Get nested value using dot notation
expiration = layer_manager.get("security", "jwt.expiration")
print(f"Expiration: {expiration}ms")

# Get array element
first_entity = layer_manager.get("entities", "[0]")

# Get nested field in array
entity_name = layer_manager.get("entities", "[0].name")
```

**Path Syntax:**
- Dot notation for objects: `"jwt.expiration"`
- Brackets for arrays: `"[0]"` or `"[0].name"`
- Combined: `"entities[0].columns[1].name"`

#### set(file_name, path, value)
Set a value at a specific path.

```python
# Set simple value
layer_manager.set("security", "jwt.expiration", 3600000)

# Set nested value
layer_manager.set("security", "jwt.issuer", "my-company")

# Set array element
layer_manager.set("entities", "[0].name", "NewName")
```

#### update(file_name, path, updates)
Update multiple fields at once.

```python
# Update multiple fields in JWT config
layer_manager.update("security", "jwt", {
    "expiration": 3600000,
    "issuer": "my-company",
    "audience": "my-users"
})

# Update root level
layer_manager.update("config", None, {
    "version": "2.0",
    "updated": "2026-03-11"
})
```

#### delete(file_name, path)
Delete a value at a specific path.

```python
# Delete a field
layer_manager.delete("security", "jwt.issuer")

# Delete array element
layer_manager.delete("entities", "[0]")
```

#### append(file_name, path, value)
Append a value to an array.

```python
# Append to array
layer_manager.append("entities", "tables", {
    "name": "new_table",
    "columns": []
})
```

#### find(file_name, path, predicate)
Find an item in an array that matches a predicate.

```python
# Find entity by name
user_entity = layer_manager.find("entities", ".", {"name": "users"})
if user_entity:
    print(f"Found: {user_entity['name']}")
```

#### filter(file_name, path, predicate)
Filter items in an array.

```python
# Filter entities by type
user_tables = layer_manager.filter("entities", ".", {"type": "user_table"})
print(f"Found {len(user_tables)} user tables")
```

### Utility Methods

#### exists(file_name, path=None)
Check if a file or path exists.

```python
# Check if file exists
if layer_manager.exists("security"):
    print("Security layer exists")

# Check if path exists
if layer_manager.exists("security", "jwt.expiration"):
    print("JWT expiration is configured")
```

#### list_files()
List all JSON files in the definitions directory.

```python
files = layer_manager.list_files()
for f in files:
    print(f"- {f}")
```

#### list_layers()
List all available layer aliases.

```python
layers = layer_manager.list_layers()
# Returns: ['entity', 'repository', 'service', 'controller', 'dto', 
#           'security', 'config', 'exception', 'audit', 'authorization', 
#           'custom_queries', 'manifest', 'project_metadata', 'entities', 'relationships']
```

### Layer Aliases

The LayerManager supports convenient aliases for common files:

| Alias | File Name |
|-------|-----------|
| `entity` | `entity_layer.json` |
| `repository` | `repository_layer.json` |
| `service` | `service_layer.json` |
| `controller` | `controller_layer.json` |
| `dto` | `dto_layer.json` |
| `security` | `security_layer.json` |
| `config` | `config_layer.json` |
| `exception` | `exception_layer.json` |
| `audit` | `audit_logging_layer.json` |
| `authorization` | `authorization_layer.json` |
| `custom_queries` | `custom_queries_layer.json` |
| `manifest` | `manifest.json` |
| `project_metadata` | `project_metadata.json` |
| `entities` | `entities.json` |
| `relationships` | `relationships.json` |

You can use either the alias or the full file name:

```python
# Using alias
layer_manager.get("security", "jwt.expiration")

# Using full file name
layer_manager.get("security_layer.json", "jwt.expiration")

# Without .json extension
layer_manager.get("security_layer", "jwt.expiration")
```

---

## Complete Usage Examples

### Example 1: Add New Entity with Fields and Relationships

```python
from managers import DefinitionManager, EntityManager, FieldManager, RelationshipManager

# Initialize
def_manager = DefinitionManager("../generated_application/my_app")
def_manager.load()

entity_manager = EntityManager(def_manager)
field_manager = FieldManager(def_manager)
rel_manager = RelationshipManager(def_manager)

# Add new entity
entity_manager.add_entity("products")

# Add fields
field_manager.add_field("products", "name", "VARCHAR(255)", nullable=False)
field_manager.add_field("products", "description", "TEXT")
field_manager.add_field("products", "price", "DECIMAL(10,2)", nullable=False)
field_manager.add_field("products", "category_id", "BIGINT", nullable=False)

# Add relationship
rel_manager.add_relationship("products", "categories", "ManyToOne", "category_id")

# Save
def_manager.save()
print("Product entity created successfully!")
```

### Example 2: Customize Validation Messages

```python
from managers import DefinitionManager, LayerManager

# Initialize
def_manager = DefinitionManager("../generated_application/my_app")
def_manager.load()

layer_manager = LayerManager(def_manager)

# Find the User DTO configuration
user_dto = layer_manager.find("dto", ".", {"entityName": "User"})

if user_dto:
    # Find the email field
    for field in user_dto.get("fields", []):
        if field.get("fieldName") == "email":
            # Update validation
            field["validation"] = {
                "required": True,
                "requiredMessage": "We need your email to send you updates",
                "email": True,
                "emailMessage": "Hmm, that doesn't look like a valid email",
                "maxLength": 255,
                "maxLengthMessage": "Email is too long"
            }
    
    # Save the changes (update the entire DTO layer)
    dto_layer = layer_manager.get("dto")
    # Update the user_dto in the layer and save
    # (Implementation depends on structure)

print("Validation messages updated!")
```

### Example 3: Disable Dangerous Endpoints

```python
from managers import DefinitionManager, LayerManager

# Initialize
def_manager = DefinitionManager("../generated_application/my_app")
def_manager.load()

layer_manager = LayerManager(def_manager)

# Disable delete endpoints for critical entities
critical_entities = ["User", "Order", "Payment"]

for entity in critical_entities:
    # Find the controller config for this entity
    controller = layer_manager.find("controller", ".", {"entityName": entity})
    
    if controller and "endpoints" in controller:
        if "delete" in controller["endpoints"]:
            # Set enabled to False
            controller["endpoints"]["delete"]["enabled"] = False
            print(f"Disabled delete endpoint for {entity}")

# Save changes
# (Would need to save the entire controller layer)

print("Critical endpoints secured!")
```

### Example 4: Configure JWT Settings

```python
from managers import DefinitionManager, LayerManager

# Initialize
def_manager = DefinitionManager("../generated_application/my_app")
def_manager.load()

layer_manager = LayerManager(def_manager)

# Update JWT configuration using generic update
layer_manager.update("security", "jwt", {
    "enabled": True,
    "secret": "production-secret-key-change-me",
    "expiration": 3600000,  # 1 hour
    "issuer": "my-company",
    "audience": "my-app-users"
})

print("JWT configuration updated!")
```

### Example 5: Bulk Entity Creation

```python
from managers import DefinitionManager, EntityManager, FieldManager

# Initialize
def_manager = DefinitionManager("../generated_application/my_app")
def_manager.load()

entity_manager = EntityManager(def_manager)
field_manager = FieldManager(def_manager)

# Define entities to create
entities = [
    {
        "name": "categories",
        "fields": [
            {"name": "name", "type": "VARCHAR(100)", "nullable": False},
            {"name": "description", "type": "TEXT"}
        ]
    },
    {
        "name": "tags",
        "fields": [
            {"name": "name", "type": "VARCHAR(50)", "nullable": False, "unique": True}
        ]
    }
]

# Create entities
for entity_def in entities:
    entity_manager.add_entity(entity_def["name"])
    
    for field_def in entity_def["fields"]:
        field_manager.add_field(
            entity_def["name"],
            field_def["name"],
            field_def["type"],
            nullable=field_def.get("nullable", True),
            unique=field_def.get("unique", False)
        )
    
    print(f"Created entity: {entity_def['name']}")

# Save
def_manager.save()
print("All entities created successfully!")
```

---

## Best Practices

1. **Always Load Before Modifying**
   ```python
   def_manager = DefinitionManager("../generated_application/my_app")
   def_manager.load()  # Always load first!
   ```

2. **Save After Changes**
   ```python
   # Make changes
   entity_manager.add_entity("products")
   
   # Save
   def_manager.save()
   ```

3. **Check Existence Before Operations**
   ```python
   if not entity_manager.entity_exists("products"):
       entity_manager.add_entity("products")
   ```

4. **Use Try-Except for Error Handling**
   ```python
   try:
       entity_manager.add_entity("products")
       def_manager.save()
   except ValueError as e:
       print(f"Error: {e}")
   ```

5. **Validate Before Saving**
   ```python
   # Check statistics before saving
   stats = def_manager.get_statistics()
   print(f"Total tables: {stats['total_tables']}")
   
   # Save
   def_manager.save()
   ```

---

## Integration with Phase 2

After modifying definitions using managers, run Phase 2 to generate code:

```bash
cd emotisense-ai/swfaw_v2
python phase2_generate_code.py --output ../generated_application/my_app
```

The generated code will reflect all your programmatic changes!

---

## Summary

The Definition Managers layer provides:

- ✅ Programmatic CRUD operations on all definition elements
- ✅ Type-safe operations with validation
- ✅ Easy integration with existing swfaw_v2 workflow
- ✅ Support for all v2.3 layer definitions
- ✅ Comprehensive error handling
- ✅ Flexible and extensible architecture

Use these managers to build tools, scripts, and automation on top of swfaw_v2!
