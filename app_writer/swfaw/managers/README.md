# Definition Managers

Programmatic CRUD operations for manipulating application definitions in swfaw_v2.

## Overview

The managers layer provides a Python API for programmatically adding, viewing, updating, and deleting elements within application definitions. This enables building tools, scripts, and automation on top of swfaw_v2.

## Components

### 1. DefinitionManager
Core manager for loading and saving application definitions.

```python
from managers import DefinitionManager

def_manager = DefinitionManager("../generated_application/my_app")
def_manager.load()
```

### 2. EntityManager
CRUD operations on entities (tables).

```python
from managers import EntityManager

entity_manager = EntityManager(def_manager)
entity_manager.add_entity("products")
```

### 3. FieldManager
CRUD operations on fields (columns).

```python
from managers import FieldManager

field_manager = FieldManager(def_manager)
field_manager.add_field("products", "name", "VARCHAR(255)")
```

### 4. RelationshipManager
CRUD operations on relationships.

```python
from managers import RelationshipManager

rel_manager = RelationshipManager(def_manager)
rel_manager.add_relationship("orders", "users", "ManyToOne", "user_id")
```

### 5. LayerManager
CRUD operations on layer definition files (v2.3).

```python
from managers import LayerManager

layer_manager = LayerManager(def_manager)
layer_manager.disable_endpoint("User", "delete")
```

## Quick Start

```python
from managers import (
    DefinitionManager,
    EntityManager,
    FieldManager,
    RelationshipManager,
    LayerManager
)

# Initialize
def_manager = DefinitionManager("../generated_application/my_app")
def_manager.load()

# Create managers
entity_manager = EntityManager(def_manager)
field_manager = FieldManager(def_manager)
rel_manager = RelationshipManager(def_manager)
layer_manager = LayerManager(def_manager)

# Add entity
entity_manager.add_entity("products")

# Add fields
field_manager.add_field("products", "name", "VARCHAR(255)", nullable=False)
field_manager.add_field("products", "price", "DECIMAL(10,2)", nullable=False)

# Add relationship
rel_manager.add_relationship("products", "categories", "ManyToOne", "category_id")

# Customize validation
layer_manager.update_dto_validation("Product", "name", {
    "required": True,
    "requiredMessage": "Product name is required",
    "maxLength": 255
})

# Save
def_manager.save()
```

## Documentation

See [DEFINITION_MANAGERS_GUIDE.md](../docs/DEFINITION_MANAGERS_GUIDE.md) for comprehensive documentation.

## Examples

See [examples/manager_usage_example.py](../examples/manager_usage_example.py) for practical examples.

## Use Cases

- Building CLI tools for definition management
- Automating entity creation from external sources
- Batch operations on definitions
- Custom validation rule generation
- Integration with other systems
- Programmatic configuration management

## Integration

The managers layer integrates seamlessly with the two-phase architecture:

1. **Phase 1**: Generate initial definition
2. **Use Managers**: Programmatically modify definition
3. **Phase 2**: Generate code from modified definition

## Version

Compatible with swfaw_v2 v2.3.0 and later.
