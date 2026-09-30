"""Test data generator - generates sample JSON test data for entities."""

import json
from typing import List, Dict, Any
from models.database_definition import DatabaseDefinition, Table


def snake_to_camel(snake_str: str) -> str:
    """Convert snake_case to camelCase"""
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


class TestDataGenerator:
    """Generates sample test data in JSON format for all entities."""

    @staticmethod
    def generate_sample_value(field_type: str, field_name: str) -> Any:
        """Generate a sample value based on field type and name."""
        field_name_lower = field_name.lower()

        # String types
        if field_type in ['String', 'VARCHAR', 'TEXT', 'CHAR']:
            if 'email' in field_name_lower:
                return "user@example.com"
            elif 'name' in field_name_lower:
                return "Sample Name"
            elif 'description' in field_name_lower:
                return "Sample description text"
            elif 'url' in field_name_lower or 'link' in field_name_lower:
                return "https://example.com"
            elif 'phone' in field_name_lower:
                return "+1234567890"
            elif 'address' in field_name_lower:
                return "123 Main St, City, Country"
            elif 'code' in field_name_lower:
                return "CODE123"
            elif 'status' in field_name_lower:
                return "ACTIVE"
            else:
                return f"Sample {field_name}"

        # Numeric types
        elif field_type in ['Integer', 'Long', 'INT', 'BIGINT', 'SMALLINT', 'TINYINT']:
            if 'id' in field_name_lower:
                return 1
            elif 'count' in field_name_lower or 'quantity' in field_name_lower:
                return 10
            elif 'age' in field_name_lower:
                return 25
            elif 'year' in field_name_lower:
                return 2024
            else:
                return 100

        # Decimal types
        elif field_type in ['Double', 'Float', 'BigDecimal', 'DECIMAL', 'FLOAT', 'DOUBLE']:
            if 'price' in field_name_lower or 'amount' in field_name_lower or 'salary' in field_name_lower:
                return 99.99
            elif 'rate' in field_name_lower or 'percentage' in field_name_lower:
                return 4.5
            else:
                return 10.5

        # Boolean types
        elif field_type in ['Boolean', 'BOOLEAN', 'TINYINT(1)']:
            if 'active' in field_name_lower or 'enabled' in field_name_lower:
                return True
            elif 'deleted' in field_name_lower or 'disabled' in field_name_lower:
                return False
            else:
                return True

        # Date/Time types
        elif field_type in ['LocalDate', 'DATE']:
            return "2024-01-01"
        elif field_type in ['LocalDateTime', 'DATETIME', 'TIMESTAMP']:
            return "2024-01-01T10:00:00"
        elif field_type in ['LocalTime', 'TIME']:
            return "10:00:00"

        # JSON types
        elif field_type in ['JSON', 'JSONB']:
            return {}

        # Default
        else:
            return f"sample_{field_name}"

    @staticmethod
    def generate_entity_sample(table: Table) -> Dict[str, Any]:
        """Generate a single sample record for an entity."""
        sample = {}

        for column in table.columns:
            # Skip auto-generated IDs
            if column.name.endswith('_id') and column.primaryKey:
                continue

            # Skip audit fields (will be auto-populated)
            if column.name in ['created_at', 'updated_at', 'created_on', 'updated_on', 'deleted_at']:
                continue

            # Convert column name to camelCase for API compatibility
            field_name = snake_to_camel(column.name)
            
            # Generate sample value
            sample[field_name] = TestDataGenerator.generate_sample_value(
                column.type,
                column.name
            )

        return sample

    @staticmethod
    def generate(db_def: DatabaseDefinition) -> str:
        """Generate complete test data JSON for all entities.
        
        Args:
            db_def: Database definition with all tables
            
        Returns:
            JSON string with test data for all entities
        """
        test_data = {
            "metadata": {
                "project": db_def.projectMetadata.name,
                "description": "Sample test data for API testing",
                "generated": "2024-01-01T00:00:00Z"
            },
            "entities": {}
        }

        # Generate sample data for each table
        for table in db_def.tables:
            entity_name = ''.join(word.capitalize() for word in table.name.split('_'))
            
            # Generate 3 sample records per entity
            samples = []
            for i in range(1, 4):
                sample = TestDataGenerator.generate_entity_sample(table)
                
                # Add variation to string fields
                for key, value in sample.items():
                    if isinstance(value, str) and not any(x in key.lower() for x in ['email', 'url', 'phone', 'code']):
                        sample[key] = f"{value} {i}"
                
                samples.append(sample)
            
            test_data["entities"][entity_name] = samples

        return json.dumps(test_data, indent=2)
