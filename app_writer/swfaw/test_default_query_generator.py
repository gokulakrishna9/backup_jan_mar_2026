"""Test script for DefaultQueryTransformer.

This script demonstrates the default query generation for different table patterns.
"""

import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from models.database_definition import Table, Column, Relationship
from models.layer_objects import EntityLayerObject, Field

# Import directly to avoid circular import
import importlib.util
spec = importlib.util.spec_from_file_location(
    "default_query_transformer",
    Path(__file__).parent / "transformers" / "default_query_transformer.py"
)
default_query_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(default_query_module)
DefaultQueryTransformer = default_query_module.DefaultQueryTransformer


def create_test_schema():
    """Create a test schema with various relationship patterns."""
    
    # Master table: customers (has children)
    customers = Table(
        name="customers",
        columns=[
            Column(name="id", type="BIGINT", primaryKey=True),
            Column(name="name", type="VARCHAR(255)", nullable=False),
            Column(name="email", type="VARCHAR(255)"),
            Column(name="created_at", type="DATETIME")
        ],
        relationships=[
            Relationship(type="OneToMany", targetTable="orders", foreignKey="customer_id"),
            Relationship(type="OneToMany", targetTable="addresses", foreignKey="customer_id")
        ]
    )
    
    # Leaf table: orders (has master and children)
    orders = Table(
        name="orders",
        columns=[
            Column(name="id", type="BIGINT", primaryKey=True),
            Column(name="customer_id", type="BIGINT"),
            Column(name="order_date", type="DATE"),
            Column(name="total_amount", type="DECIMAL(10,2)"),
            Column(name="status", type="VARCHAR(50)")
        ],
        relationships=[
            Relationship(type="ManyToOne", targetTable="customers", foreignKey="customer_id"),
            Relationship(type="OneToMany", targetTable="order_items", foreignKey="order_id")
        ]
    )
    
    # Leaf table: order_items (only has master)
    order_items = Table(
        name="order_items",
        columns=[
            Column(name="id", type="BIGINT", primaryKey=True),
            Column(name="order_id", type="BIGINT"),
            Column(name="product_id", type="BIGINT"),
            Column(name="quantity", type="INT"),
            Column(name="price", type="DECIMAL(10,2)")
        ],
        relationships=[
            Relationship(type="ManyToOne", targetTable="orders", foreignKey="order_id"),
            Relationship(type="ManyToOne", targetTable="products", foreignKey="product_id")
        ]
    )
    
    # Master table: products
    products = Table(
        name="products",
        columns=[
            Column(name="id", type="BIGINT", primaryKey=True),
            Column(name="title", type="VARCHAR(255)", nullable=False),
            Column(name="description", type="TEXT"),
            Column(name="price", type="DECIMAL(10,2)")
        ],
        relationships=[
            Relationship(type="OneToMany", targetTable="order_items", foreignKey="product_id")
        ]
    )
    
    # Leaf table: addresses
    addresses = Table(
        name="addresses",
        columns=[
            Column(name="id", type="BIGINT", primaryKey=True),
            Column(name="customer_id", type="BIGINT"),
            Column(name="street", type="VARCHAR(255)"),
            Column(name="city", type="VARCHAR(100)"),
            Column(name="country", type="VARCHAR(100)")
        ],
        relationships=[
            Relationship(type="ManyToOne", targetTable="customers", foreignKey="customer_id")
        ]
    )
    
    # Linked table: student_courses (ManyToMany)
    student_courses = Table(
        name="student_courses",
        columns=[
            Column(name="id", type="BIGINT", primaryKey=True),
            Column(name="student_id", type="BIGINT"),
            Column(name="course_id", type="BIGINT"),
            Column(name="enrollment_date", type="DATE")
        ],
        relationships=[
            Relationship(type="ManyToMany", targetTable="students", foreignKey="student_id"),
            Relationship(type="ManyToMany", targetTable="courses", foreignKey="course_id")
        ]
    )
    
    return [customers, orders, order_items, products, addresses, student_courses]


def create_test_entities(tables):
    """Create entity layer objects from tables."""
    entities = []
    
    for table in tables:
        fields = []
        for col in table.columns:
            # Simple type mapping
            java_type = "String"
            if "BIGINT" in col.type or "INT" in col.type:
                java_type = "Long" if "BIGINT" in col.type else "Integer"
            elif "DECIMAL" in col.type:
                java_type = "BigDecimal"
            elif "DATE" in col.type:
                java_type = "LocalDate" if col.type == "DATE" else "LocalDateTime"
            
            fields.append(Field(
                columnName=col.name,
                fieldName=col.name,
                javaType=java_type,
                isPrimaryKey=col.primaryKey,
                isNullable=col.nullable,
                columnDefinition=col.type
            ))
        
        # Convert table name to class name (PascalCase)
        class_name = ''.join(word.title() for word in table.name.split('_'))
        
        entity = EntityLayerObject(
            tableName=table.name,
            className=class_name,
            packageName="com.example.entity",
            fields=fields,
            isRootEntity=True,
            hasPublicFlag=False,
            hasAuditFields=True,
            hasSoftDelete=True
        )
        entities.append(entity)
    
    return entities


def print_query_summary(query_layer):
    """Print a summary of generated queries."""
    print(f"\n{'='*80}")
    print(f"Entity: {query_layer.entityName}")
    print(f"{'='*80}")
    print(f"Total Queries: {len(query_layer.queries)}\n")
    
    for i, query in enumerate(query_layer.queries, 1):
        print(f"{i}. {query.name}")
        print(f"   Description: {query.description}")
        print(f"   Return Type: {query.returnType}")
        print(f"   Pagination: {query.pagination}")
        
        if query.joins:
            print(f"   Joins: {len(query.joins)} table(s)")
            for join in query.joins:
                print(f"      - {join.type} JOIN {join.table} {join.alias or ''}")
        
        if query.where:
            print(f"   Where: {', '.join(query.where)}")
        
        if query.groupBy:
            print(f"   Group By: {', '.join(query.groupBy)}")
        
        if query.parameters:
            print(f"   Parameters: {', '.join(p.name for p in query.parameters)}")
        
        print()


def print_full_query_json(query_layer):
    """Print full JSON representation of queries."""
    print(f"\n{'='*80}")
    print(f"Full JSON for {query_layer.entityName}")
    print(f"{'='*80}\n")
    
    queries_json = []
    for query in query_layer.queries:
        query_dict = {
            "name": query.name,
            "description": query.description,
            "returnType": query.returnType,
            "select": query.select,
            "from": query.from_,
            "joins": [
                {
                    "type": join.type,
                    "table": join.table,
                    "alias": join.alias,
                    "on": join.on
                }
                for join in query.joins
            ],
            "where": query.where,
            "groupBy": query.groupBy,
            "having": query.having,
            "orderBy": query.orderBy,
            "pagination": query.pagination,
            "parameters": [
                {
                    "name": param.name,
                    "type": param.type,
                    "required": param.required,
                    "defaultValue": param.defaultValue
                }
                for param in query.parameters
            ],
            "authorization": query.authorization
        }
        queries_json.append(query_dict)
    
    print(json.dumps(queries_json, indent=2))


def main():
    """Main test function."""
    print("\n" + "="*80)
    print("DEFAULT QUERY GENERATOR TEST")
    print("="*80)
    
    # Create test schema
    print("\n>> Creating test schema...")
    tables = create_test_schema()
    print(f"   Created {len(tables)} tables:")
    for table in tables:
        print(f"   - {table.name} ({len(table.columns)} columns, {len(table.relationships)} relationships)")
    
    # Create entities
    print("\n>> Creating entity layer objects...")
    entities = create_test_entities(tables)
    print(f"   Created {len(entities)} entities")
    
    # Initialize transformer
    print("\n>> Initializing DefaultQueryTransformer...")
    transformer = DefaultQueryTransformer(tables, entities, "com.example")
    
    # Transform to query layers
    print("\n>> Generating default queries...")
    query_layers = transformer.transform()
    print(f"   Generated queries for {len(query_layers)} entities")
    
    # Print summaries
    print("\n" + "="*80)
    print("QUERY SUMMARIES")
    print("="*80)
    
    for query_layer in query_layers:
        print_query_summary(query_layer)
    
    # Print detailed JSON for one entity
    print("\n" + "="*80)
    print("DETAILED EXAMPLE: Orders Entity")
    print("="*80)
    
    orders_layer = next((ql for ql in query_layers if ql.entityName == "Orders"), None)
    if orders_layer:
        print_full_query_json(orders_layer)
    
    # Statistics
    print("\n" + "="*80)
    print("STATISTICS")
    print("="*80)
    
    total_queries = sum(len(ql.queries) for ql in query_layers)
    print(f"\nTotal Queries Generated: {total_queries}")
    print(f"Average Queries per Entity: {total_queries / len(query_layers):.1f}")
    
    print("\n" + "="*80)
    print("TEST COMPLETED SUCCESSFULLY")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
