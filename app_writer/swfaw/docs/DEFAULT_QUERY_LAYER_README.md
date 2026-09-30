# Default Query Layer - Intelligent Query Generation

## Overview

The Default Query Layer automatically generates intelligent, relationship-aware queries during Phase 1 of application generation. These queries are saved in `query_layer.json` files and can be customized before Phase 2 code generation.

## What's New in v2.4.0

- **Automatic Query Generation**: No more empty query layers! The system now generates intelligent default queries based on your table relationships.
- **Relationship-Aware**: Queries are tailored to table types (leaf, master, linked).
- **Customizable**: Generated queries can be modified before code generation.
- **Production-Ready**: Includes pagination, authorization, and proper JOIN handling.

## How It Works

### Phase 1: Query Generation

When you run Phase 1 (`phase1_generate_definition.py`), the `DefaultQueryTransformer` analyzes your database schema and generates queries based on relationship patterns:

```bash
cd emotisense-ai/swfaw
python phase1_generate_definition.py --input ../mysql_database_design/schema.sql --output ../generated_application/my_app
```

The transformer:
1. Analyzes all table relationships (OneToMany, ManyToOne, ManyToMany)
2. Classifies tables as Leaf, Master, or Linked
3. Generates appropriate queries for each table type
4. Saves queries to `application_definitions/query_layer.json`

### Phase 2: Code Generation

During Phase 2, the `CustomQueryGenerator` reads the query definitions and generates:
- DTO classes for query results
- Repository methods with R2DBC DatabaseClient
- Service methods with authorization
- Controller endpoints with pagination

## Query Types by Table Pattern

### 1. Leaf Tables (No Children)

**Characteristics:**
- Has ManyToOne relationships (foreign keys to other tables)
- No OneToMany relationships (no other tables reference it)

**Generated Queries:**

#### Basic List
```json
{
  "name": "listOrderItems",
  "description": "List all OrderItems records",
  "returnType": "OrderItemsOutputDTO",
  "select": ["o.id", "o.order_id", "o.product_id", "o.quantity", "o.price"],
  "from": "order_items o",
  "orderBy": ["o.id DESC"],
  "pagination": true
}
```

#### List with Master Labels
Joins all master tables and includes their label columns:
```json
{
  "name": "listOrderItemsWithMasters",
  "description": "List OrderItems with master table labels",
  "returnType": "OrderItemsWithMastersDTO",
  "select": [
    "o.id", "o.order_id", "o.product_id", "o.quantity", "o.price",
    "m1.status as orders_status",
    "m2.title as products_title"
  ],
  "from": "order_items o",
  "joins": [
    {"type": "LEFT", "table": "orders", "alias": "m1", "on": "o.order_id = m1.id"},
    {"type": "LEFT", "table": "products", "alias": "m2", "on": "o.product_id = m2.id"}
  ],
  "pagination": true
}
```

#### Filter by Each Master
One query per master relationship:
```json
{
  "name": "listOrderItemsByOrders",
  "description": "List OrderItems filtered by Orders",
  "returnType": "OrderItemsOutputDTO",
  "where": ["o.order_id = :orderId"],
  "parameters": [
    {"name": "orderId", "type": "Long", "required": true}
  ],
  "pagination": true
}
```

### 2. Master Tables (Have Children)

**Characteristics:**
- Has OneToMany relationships (other tables reference it)
- May also have ManyToOne relationships

**Generated Queries:**

#### Basic List
```json
{
  "name": "listCustomers",
  "description": "List all Customers records",
  "returnType": "CustomersOutputDTO",
  "pagination": true
}
```

#### List with All Child Counts
Aggregates counts from all child tables:
```json
{
  "name": "listCustomersWithChildCounts",
  "description": "List Customers with counts of all child records",
  "returnType": "CustomersWithCountsDTO",
  "select": [
    "c.id",
    "c.name",
    "COUNT(DISTINCT c1.id) as orders_count",
    "COUNT(DISTINCT c2.id) as addresses_count"
  ],
  "from": "customers c",
  "joins": [
    {"type": "LEFT", "table": "orders", "alias": "c1", "on": "c.id = c1.customer_id"},
    {"type": "LEFT", "table": "addresses", "alias": "c2", "on": "c.id = c2.customer_id"}
  ],
  "groupBy": ["c.id", "c.name"],
  "pagination": true
}
```

#### Individual Child Count Queries
One query per child relationship:
```json
{
  "name": "listCustomersWithOrdersCount",
  "description": "List Customers with Orders count",
  "returnType": "CustomersWithOrdersCountDTO",
  "select": [
    "c.id",
    "c.name",
    "COUNT(c.id) as orders_count"
  ],
  "from": "customers c",
  "joins": [
    {"type": "LEFT", "table": "orders", "alias": "c", "on": "c.id = c.customer_id"}
  ],
  "groupBy": ["c.id", "c.name"],
  "pagination": true
}
```

### 3. Linked Tables (ManyToMany)

**Characteristics:**
- Has ManyToMany relationships
- Typically junction/bridge tables

**Generated Queries:**

Two queries are generated, treating each side as master:

#### Query 1: List with Target Information
```json
{
  "name": "listStudentCoursesWithCourse",
  "description": "List StudentCourses with linked Course information",
  "returnType": "StudentCoursesWithCourseDTO",
  "select": ["sc.*", "c.title as courses_title"],
  "from": "student_courses sc",
  "joins": [
    {"type": "LEFT", "table": "courses", "alias": "c", "on": "sc.course_id = c.id"}
  ],
  "pagination": true
}
```

#### Query 2: Reverse Perspective
```json
{
  "name": "listCoursesWithStudentCourses",
  "description": "List Courses with linked StudentCourses information",
  "returnType": "CoursesWithStudentCoursesDTO",
  "select": ["c.*", "sc.enrollment_date as student_courses_enrollment_date"],
  "from": "courses c",
  "joins": [
    {"type": "LEFT", "table": "student_courses", "alias": "sc", "on": "c.id = sc.course_id"}
  ],
  "pagination": true
}
```

## Label Column Detection

The system automatically finds the best "label" column for each table using this priority:

1. `name`
2. `title`
3. `label`
4. `description`
5. `username`
6. `email`
7. First non-id VARCHAR column
8. `id` (fallback)

This ensures meaningful data is included in JOIN queries.

## Example: E-Commerce Schema

### Schema
```sql
CREATE TABLE customers (
    id BIGINT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255)
);

CREATE TABLE orders (
    id BIGINT PRIMARY KEY,
    customer_id BIGINT,
    order_date DATE,
    status VARCHAR(50),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE order_items (
    id BIGINT PRIMARY KEY,
    order_id BIGINT,
    product_id BIGINT,
    quantity INT,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE products (
    id BIGINT PRIMARY KEY,
    title VARCHAR(255),
    price DECIMAL(10,2)
);
```

### Generated Queries

**Customers (Master):**
- `listCustomers` - Basic list
- `listCustomersWithChildCounts` - With orders count
- `listCustomersWithOrdersCount` - Individual orders count

**Orders (Master + Leaf):**
- `listOrders` - Basic list
- `listOrdersWithMasters` - With customer name
- `listOrdersByCustomer` - Filtered by customer
- `listOrdersWithChildCounts` - With order_items count
- `listOrdersWithOrderItemsCount` - Individual order_items count

**OrderItems (Leaf):**
- `listOrderItems` - Basic list
- `listOrderItemsWithMasters` - With order status and product title
- `listOrderItemsByOrders` - Filtered by order
- `listOrderItemsByProducts` - Filtered by product

**Products (Master):**
- `listProducts` - Basic list
- `listProductsWithChildCounts` - With order_items count
- `listProductsWithOrderItemsCount` - Individual order_items count

## Customization

After Phase 1, you can customize queries in `application_definitions/query_layer.json`:

### Add Custom WHERE Conditions
```json
{
  "name": "listActiveOrders",
  "where": ["o.status = 'active'", "o.order_date >= :startDate"],
  "parameters": [
    {"name": "startDate", "type": "LocalDate", "required": true}
  ]
}
```

### Modify SELECT Fields
```json
{
  "select": [
    "o.id",
    "o.order_date",
    "o.total_amount",
    "SUM(oi.quantity) as total_items"
  ]
}
```

### Add Additional JOINs
```json
{
  "joins": [
    {"type": "INNER", "table": "payments", "alias": "p", "on": "o.id = p.order_id"}
  ]
}
```

### Disable Authorization
```json
{
  "authorization": {"enabled": false}
}
```

## Testing

Run the test script to see query generation in action:

```bash
cd emotisense-ai/swfaw
python test_default_query_generator.py
```

This creates a sample schema and shows all generated queries with detailed output.

## Benefits

1. **Zero Manual Work**: Queries are generated automatically from your schema
2. **Relationship-Aware**: Intelligent queries based on table relationships
3. **Production-Ready**: Includes pagination, authorization, and proper SQL
4. **Customizable**: Modify before code generation
5. **Consistent**: All queries follow the same structure
6. **Type-Safe**: Generated DTOs for query results
7. **Time-Saving**: Eliminates hours of boilerplate query writing

## Migration from v2.3

If you have existing applications generated with v2.3:

1. **Regenerate Phase 1**: Run Phase 1 again to get default queries
2. **Review Queries**: Check `query_layer.json` files
3. **Customize**: Modify queries as needed
4. **Regenerate Phase 2**: Run Phase 2 to generate code

Your existing custom queries will be preserved if you manually merge them.

## Version History

- **v2.4.0**: Initial release of default query generation
- **v2.3.0**: Empty query layers (manual query definition required)

## See Also

- [DEFAULT_QUERY_GENERATION.md](./DEFAULT_QUERY_GENERATION.md) - Detailed technical documentation
- [QUERY_FILTER_LAYERS_GUIDE.md](./QUERY_FILTER_LAYERS_GUIDE.md) - Query and filter layer guide
- [LAYER_DEFINITIONS_GUIDE.md](./LAYER_DEFINITIONS_GUIDE.md) - Complete layer definitions guide
