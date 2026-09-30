# Default Query Generation

## Overview

The Default Query Generator automatically creates intelligent queries based on table relationships during Phase 1 (application definition generation). These queries are added to the `query_layer.json` files and can be customized before Phase 2 code generation.

## Query Generation Rules

### 1. Leaf Tables (No Children)

**Definition:** Tables with no OneToMany relationships pointing to them.

**Generated Queries:**

#### a) List with Master Labels
Joins all master tables and includes their label columns.

```json
{
  "name": "listOrdersWithMasters",
  "description": "List Orders with master table labels",
  "returnType": "OrdersWithMastersDTO",
  "select": [
    "o.id",
    "o.order_date",
    "o.customer_id",
    "m1.name as customers_name",
    "m2.title as products_title"
  ],
  "from": "orders o",
  "joins": [
    {
      "type": "LEFT",
      "table": "customers",
      "alias": "m1",
      "on": "o.customer_id = m1.id"
    },
    {
      "type": "LEFT",
      "table": "products",
      "alias": "m2",
      "on": "o.product_id = m2.id"
    }
  ],
  "pagination": true,
  "authorization": {"enabled": true, "documentField": "id"}
}
```

#### b) Filter by Each Master
One query per master relationship for filtering.

```json
{
  "name": "listOrdersByCustomer",
  "description": "List Orders filtered by Customer",
  "returnType": "OrdersOutputDTO",
  "where": ["o.customer_id = :customerId"],
  "parameters": [
    {"name": "customerId", "type": "Long", "required": true}
  ],
  "pagination": true
}
```

### 2. Master Tables (Have Children)

**Definition:** Tables with OneToMany relationships.

**Generated Queries:**

#### a) List with All Child Counts
Aggregates counts from all child tables.

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
    {
      "type": "LEFT",
      "table": "orders",
      "alias": "c1",
      "on": "c.id = c1.customer_id"
    },
    {
      "type": "LEFT",
      "table": "addresses",
      "alias": "c2",
      "on": "c.id = c2.customer_id"
    }
  ],
  "groupBy": ["c.id", "c.name"],
  "pagination": true
}
```

#### b) Individual Child Count Queries
One query per child relationship.

```json
{
  "name": "listCustomersWithOrdersCount",
  "description": "List Customers with Orders count",
  "returnType": "CustomersWithOrdersCountDTO",
  "select": [
    "c.id",
    "c.name",
    "COUNT(c1.id) as orders_count"
  ],
  "from": "customers c",
  "joins": [
    {
      "type": "LEFT",
      "table": "orders",
      "alias": "c1",
      "on": "c.id = c1.customer_id"
    }
  ],
  "groupBy": ["c.id", "c.name"],
  "pagination": true
}
```

### 3. Linked Tables (ManyToMany)

**Definition:** Tables with ManyToMany relationships.

**Generated Queries:**

Two queries are generated, treating each side as master:

#### a) List Linked Table with Target
```json
{
  "name": "listStudentCoursesWithCourse",
  "description": "List StudentCourses with linked Course information",
  "returnType": "StudentCoursesWithCourseDTO",
  "select": [
    "sc.*",
    "c.title as courses_title"
  ],
  "from": "student_courses sc",
  "joins": [
    {
      "type": "LEFT",
      "table": "courses",
      "alias": "c",
      "on": "sc.course_id = c.id"
    }
  ],
  "pagination": true
}
```

#### b) List Target with Linked Table (Reverse)
```json
{
  "name": "listCoursesWithStudentCourses",
  "description": "List Courses with linked StudentCourses information",
  "returnType": "CoursesWithStudentCoursesDTO",
  "select": [
    "c.*",
    "sc.enrollment_date as student_courses_enrollment_date"
  ],
  "from": "courses c",
  "joins": [
    {
      "type": "LEFT",
      "table": "student_courses",
      "alias": "sc",
      "on": "c.id = sc.course_id"
    }
  ],
  "pagination": true
}
```

### 4. Basic List Query

**Always Generated:** Every table gets a basic list query.

```json
{
  "name": "listCustomers",
  "description": "List all Customers records",
  "returnType": "CustomersOutputDTO",
  "select": ["c.id", "c.name", "c.email", "c.created_at"],
  "from": "customers c",
  "orderBy": ["c.id DESC"],
  "pagination": true,
  "authorization": {"enabled": true, "documentField": "id"}
}
```

## Label Column Detection

The generator automatically finds the best label column for each table using this priority:

1. `name`
2. `title`
3. `label`
4. `description`
5. `username`
6. `email`
7. First non-id VARCHAR column
8. `id` (fallback)

## Example Schema

```sql
CREATE TABLE customers (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255)
);

CREATE TABLE orders (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    customer_id BIGINT,
    order_date DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE order_items (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    order_id BIGINT,
    product_name VARCHAR(255),
    quantity INT,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);
```

### Generated Queries

**For `customers` (Master):**
- `listCustomers` - Basic list
- `listCustomersWithChildCounts` - With orders count
- `listCustomersWithOrdersCount` - Individual orders count

**For `orders` (Both Master and Leaf):**
- `listOrders` - Basic list
- `listOrdersWithMasters` - With customer name
- `listOrdersByCustomer` - Filtered by customer
- `listOrdersWithChildCounts` - With order_items count
- `listOrdersWithOrderItemsCount` - Individual order_items count

**For `order_items` (Leaf):**
- `listOrderItems` - Basic list
- `listOrderItemsWithMasters` - With order info
- `listOrderItemsByOrder` - Filtered by order

## Customization

After Phase 1 generation, you can:

1. **Modify queries** in `application_definitions/query_layer.json`
2. **Add custom queries** following the same structure
3. **Remove unwanted queries**
4. **Adjust authorization settings**
5. **Change return types**

## Integration with Code Generation

During Phase 2, the custom query generator reads these definitions and generates:

1. **DTO classes** for each unique returnType
2. **Repository methods** with R2DBC DatabaseClient
3. **Service methods** with authorization checks
4. **Controller endpoints** with pagination support

## Benefits

- **Zero manual query writing** for common patterns
- **Consistent query structure** across the application
- **Authorization-ready** queries
- **Pagination support** out of the box
- **Customizable** before code generation
- **Type-safe** with generated DTOs

## Version

Added in: swfaw v2.4.0
