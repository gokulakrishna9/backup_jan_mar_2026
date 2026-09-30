# Query and Filter Layers Guide - v2.4.0

**Version:** 2.4.0  
**Date:** March 13, 2026  
**Status:** Production Ready

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Query Layer](#query-layer)
4. [Filter Layer](#filter-layer)
5. [Generated Code](#generated-code)
6. [Managers API](#managers-api)
7. [Examples](#examples)
8. [Best Practices](#best-practices)

## Overview

The query and filter layers enable you to define custom database queries with:

- **Complex Joins** - INNER, LEFT, RIGHT, FULL joins
- **Aggregations** - COUNT, SUM, AVG, MIN, MAX
- **Filtering** - Type-aware filter operators
- **Pagination** - Built-in page/size support
- **Authorization** - Document-level access control
- **Audit Logging** - All query executions logged
- **Type Safety** - Parameterized R2DBC queries

All queries are pre-built at code generation time - no dynamic SQL at runtime.

## Quick Start

### Step 1: Generate Application Definition

```bash
cd emotisense-ai/swfaw
python phase1_generate_definition.py --input ../mysql_database_design/schema.sql --output ../generated_application/my_app
```

This creates:
- `application_definitions/query_layer.json` - Empty query definitions
- `application_definitions/filter_layer.json` - Default filter definitions

### Step 2: Define Custom Queries

Edit `application_definitions/query_layer.json`:

```json
{
  "layerType": "query",
  "version": "2.4.0",
  "queries": {
    "User": [
      {
        "name": "findActiveUsersWithRoles",
        "description": "Find active users with their roles",
        "returnType": "UserWithRolesDTO",
        "select": ["u.id", "u.username", "u.email", "r.role_name"],
        "from": "users u",
        "joins": [
          {
            "type": "INNER",
            "table": "user_roles",
            "alias": "ur",
            "on": "u.id = ur.user_id"
          }
        ]
      }
    ]
  }
}
```


### Step 3: Generate Code

```bash
python phase2_generate_code.py --output ../generated_application/my_app
```

This generates:
- `UserCustomQueryRepository.java` - R2DBC DatabaseClient queries
- `UserCustomQueryService.java` - Business logic with authorization
- `UserCustomQueryController.java` - REST endpoints
- `UserWithRolesDTO.java` - Query result DTO
- `UserFilterDTO.java` - Filter DTO

### Step 4: Use Generated Endpoints

```bash
GET /api/user/queries/find-active-users-with-roles?active=true&page=0&size=20
```

## Query Layer

### Query Definition Structure

```json
{
  "name": "queryMethodName",
  "description": "Human-readable description",
  "returnType": "ResultDTOClassName",
  "select": ["u.id", "u.username", "COUNT(o.id) as order_count"],
  "from": "users u",
  "joins": [
    {
      "type": "INNER|LEFT|RIGHT|FULL",
      "table": "orders",
      "alias": "o",
      "on": "u.id = o.user_id"
    }
  ],
  "where": ["u.active = :active", "u.created_date > :fromDate"],
  "groupBy": ["u.id", "u.username"],
  "having": ["COUNT(o.id) > :minOrders"],
  "orderBy": ["u.username ASC", "order_count DESC"],
  "pagination": true,
  "parameters": [
    {
      "name": "active",
      "type": "Boolean",
      "required": true
    },
    {
      "name": "fromDate",
      "type": "LocalDateTime",
      "required": false,
      "defaultValue": "LocalDateTime.now().minusDays(30)"
    }
  ],
  "authorization": {
    "enabled": true,
    "documentField": "id"
  }
}
```

### Query Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | String | Yes | Method name (camelCase) |
| description | String | Yes | Human-readable description |
| returnType | String | Yes | DTO class name for results |
| select | Array | Yes | SELECT fields with aliases |
| from | String | Yes | FROM clause with table alias |
| joins | Array | No | Join definitions |
| where | Array | No | WHERE conditions with parameters |
| groupBy | Array | No | GROUP BY fields |
| having | Array | No | HAVING conditions |
| orderBy | Array | No | ORDER BY clauses |
| pagination | Boolean | No | Enable pagination (default: false) |
| parameters | Array | No | Query parameters |
| authorization | Object | No | Authorization configuration |

### Join Definition

```json
{
  "type": "INNER",
  "table": "orders",
  "alias": "o",
  "on": "u.id = o.user_id"
}
```

**Join Types:** INNER, LEFT, RIGHT, FULL

### Parameter Definition

```json
{
  "name": "active",
  "type": "Boolean",
  "required": true,
  "defaultValue": "true"
}
```

**Supported Types:**
- String
- Integer, Long, Short, Byte
- BigDecimal, Float, Double
- Boolean
- LocalDate, LocalDateTime, LocalTime
- List<T> (for IN clauses)

### Authorization Configuration

```json
{
  "enabled": true,
  "documentField": "id"
}
```

When enabled:
- Service checks document access for each result
- Uses `documentField` to extract document ID
- Filters out unauthorized results
- Logs access attempts

## Filter Layer

### Filter Definition Structure

```json
{
  "layerType": "filter",
  "version": "2.4.0",
  "filters": {
    "User": {
      "fields": [
        {
          "name": "username",
          "type": "String",
          "operators": ["equals", "contains", "startsWith", "endsWith", "in"]
        },
        {
          "name": "createdDate",
          "type": "LocalDateTime",
          "operators": ["equals", "greaterThan", "lessThan", "between"]
        }
      ]
    }
  }
}
```

### Supported Operators

| Operator | Types | SQL | DTO Fields Generated |
|----------|-------|-----|---------------------|
| equals | All | field = :value | fieldName |
| contains | String | field LIKE '%:value%' | fieldNameContains |
| startsWith | String | field LIKE ':value%' | fieldNameStartsWith |
| endsWith | String | field LIKE '%:value' | fieldNameEndsWith |
| greaterThan | Numeric, Date | field > :value | fieldNameGreaterThan |
| lessThan | Numeric, Date | field < :value | fieldNameLessThan |
| between | Numeric, Date | field BETWEEN :from AND :to | fieldNameFrom, fieldNameTo |
| in | All | field IN (:values) | fieldNameIn (List) |

### Default Operators by Type

**String:** equals, contains, startsWith, endsWith, in  
**Numeric:** equals, greaterThan, lessThan, between, in  
**Boolean:** equals  
**Date/Time:** equals, greaterThan, lessThan, between

## Generated Code

### 1. Custom Query Repository

```java
@Repository
public class UserCustomQueryRepository {
    private final DatabaseClient databaseClient;
    
    public Flux<UserWithRolesDTO> findActiveUsersWithRoles(
        Boolean active, 
        LocalDateTime fromDate,
        int page, 
        int size
    ) {
        String sql = "SELECT u.id, u.username, u.email, r.role_name " +
                     "FROM users u " +
                     "INNER JOIN user_roles ur ON u.id = ur.user_id " +
                     "LEFT JOIN roles r ON ur.role_id = r.id " +
                     "WHERE u.active = :active AND u.created_date > :fromDate " +
                     "LIMIT :limit OFFSET :offset";
        
        return databaseClient.sql(sql)
            .bind("active", active)
            .bind("fromDate", fromDate)
            .bind("limit", size)
            .bind("offset", page * size)
            .map((row, metadata) -> {
                return UserWithRolesDTO.builder()
                    .id(row.get("id", Long.class))
                    .username(row.get("username", String.class))
                    .email(row.get("email", String.class))
                    .roleName(row.get("role_name", String.class))
                    .build();
            })
            .all();
    }
    
    public Mono<Long> countFindActiveUsersWithRoles(
        Boolean active, 
        LocalDateTime fromDate
    ) {
        String sql = "SELECT COUNT(*) " +
                     "FROM users u " +
                     "INNER JOIN user_roles ur ON u.id = ur.user_id " +
                     "WHERE u.active = :active AND u.created_date > :fromDate";
        
        return databaseClient.sql(sql)
            .bind("active", active)
            .bind("fromDate", fromDate)
            .map((row, metadata) -> row.get(0, Long.class))
            .one()
            .defaultIfEmpty(0L);
    }
}
```

### 2. Custom Query Service

```java
@Service
public class UserCustomQueryService {
    private final UserCustomQueryRepository repository;
    private final AuthorizationService authorizationService;
    private final AuditLoggingService auditLoggingService;
    
    public Flux<UserWithRolesDTO> findActiveUsersWithRoles(
        Boolean active,
        LocalDateTime fromDate,
        int page,
        int size,
        Long authUserId
    ) {
        // Log query execution
        auditLoggingService.logQueryExecution(
            authUserId,
            "User",
            "findActiveUsersWithRoles",
            true,
            null
        ).subscribe();
        
        return repository.findActiveUsersWithRoles(active, fromDate, page, size)
            .filterWhen(result -> {
                // Check authorization for each result
                return authorizationService.checkDocumentAccess(
                    authUserId,
                    "User",
                    result.getId(),
                    "READ"
                );
            });
    }
}
```

### 3. Custom Query Controller

```java
@RestController
@RequestMapping("/api/user")
@Tag(name = "User Custom Queries")
public class UserCustomQueryController {
    private final UserCustomQueryService service;
    
    @GetMapping("/queries/find-active-users-with-roles")
    @Operation(summary = "Find active users with their roles")
    public Mono<ResponseEntity<Flux<UserWithRolesDTO>>> findActiveUsersWithRoles(
        @RequestParam Boolean active,
        @RequestParam(required = false) LocalDateTime fromDate,
        @RequestParam(defaultValue = "0") int page,
        @RequestParam(defaultValue = "20") int size,
        Authentication authentication
    ) {
        Long authUserId = Long.parseLong(authentication.getName());
        
        Flux<UserWithRolesDTO> results = service.findActiveUsersWithRoles(
            active, fromDate, page, size, authUserId
        );
        
        Mono<Long> total = service.countFindActiveUsersWithRoles(active, fromDate);
        
        return total.map(count -> {
            return ResponseEntity.ok()
                .header("X-Total-Count", String.valueOf(count))
                .header("X-Page", String.valueOf(page))
                .header("X-Page-Size", String.valueOf(size))
                .body(results);
        });
    }
}
```

### 4. Query Result DTO

```java
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserWithRolesDTO {
    private Long id;
    private String username;
    private String email;
    private String roleName;
}
```

### 5. Filter DTO

```java
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserFilterDTO {
    // username filters
    private String username;
    private String usernameContains;
    private String usernameStartsWith;
    private String usernameEndsWith;
    private List<String> usernameIn;
    
    // email filters
    private String email;
    private String emailContains;
    
    // active filter
    private Boolean active;
    
    // createdDate filters
    private LocalDateTime createdDate;
    private LocalDateTime createdDateGreaterThan;
    private LocalDateTime createdDateLessThan;
    private LocalDateTime createdDateFrom;
    private LocalDateTime createdDateTo;
}
```


## Managers API

### QueryManager

Programmatic CRUD operations for query definitions.

```python
from managers import DefinitionManager, LayerManager, QueryManager

# Initialize
def_manager = DefinitionManager("../generated_application/my_app")
def_manager.load()
layer_manager = LayerManager(def_manager)
query_manager = QueryManager(layer_manager)

# Add a query
query_def = {
    "name": "findActiveUsers",
    "description": "Find all active users",
    "returnType": "UserDTO",
    "select": ["u.id", "u.username"],
    "from": "users u",
    "where": ["u.active = :active"],
    "pagination": True,
    "parameters": [
        {"name": "active", "type": "Boolean", "required": True}
    ]
}
query_manager.add_query("User", query_def)

# Get a query
query = query_manager.get_query("User", "findActiveUsers")

# Update a query
query_manager.update_query("User", "findActiveUsers", {
    "description": "Find all active users (updated)"
})

# Remove a query
query_manager.remove_query("User", "findActiveUsers")

# List all queries for an entity
queries = query_manager.list_queries("User")

# Save changes
def_manager.save()
```

### FilterManager

Programmatic CRUD operations for filter definitions.

```python
from managers import DefinitionManager, LayerManager, FilterManager

# Initialize
def_manager = DefinitionManager("../generated_application/my_app")
def_manager.load()
layer_manager = LayerManager(def_manager)
filter_manager = FilterManager(layer_manager)

# Add a filter field
filter_field = {
    "name": "status",
    "type": "String",
    "operators": ["equals", "in"]
}
filter_manager.add_filter_field("User", filter_field)

# Get a filter field
field = filter_manager.get_filter_field("User", "status")

# Update a filter field
filter_manager.update_filter_field("User", "status", {
    "operators": ["equals", "in", "contains"]
})

# Remove a filter field
filter_manager.remove_filter_field("User", "status")

# List all filter fields for an entity
fields = filter_manager.list_filter_fields("User")

# Save changes
def_manager.save()
```


## Examples

### Example 1: Simple Query with Pagination

```json
{
  "name": "findUsersByStatus",
  "description": "Find users by status",
  "returnType": "UserDTO",
  "select": ["id", "username", "email", "status"],
  "from": "users",
  "where": ["status = :status"],
  "orderBy": ["username ASC"],
  "pagination": true,
  "parameters": [
    {"name": "status", "type": "String", "required": true}
  ]
}
```

**Generated Endpoint:**
```
GET /api/user/queries/find-users-by-status?status=active&page=0&size=20
```

### Example 2: Query with Multiple Joins

```json
{
  "name": "findOrdersWithCustomerAndProducts",
  "description": "Find orders with customer and product details",
  "returnType": "OrderDetailsDTO",
  "select": [
    "o.id",
    "o.order_date",
    "c.name as customer_name",
    "p.name as product_name",
    "oi.quantity"
  ],
  "from": "orders o",
  "joins": [
    {"type": "INNER", "table": "customers", "alias": "c", "on": "o.customer_id = c.id"},
    {"type": "INNER", "table": "order_items", "alias": "oi", "on": "o.id = oi.order_id"},
    {"type": "INNER", "table": "products", "alias": "p", "on": "oi.product_id = p.id"}
  ],
  "where": ["o.order_date > :fromDate"],
  "orderBy": ["o.order_date DESC"],
  "pagination": true,
  "parameters": [
    {"name": "fromDate", "type": "LocalDate", "required": true}
  ]
}
```

### Example 3: Aggregation Query

```json
{
  "name": "getUserOrderStatistics",
  "description": "Get order statistics per user",
  "returnType": "UserOrderStatsDTO",
  "select": [
    "u.id",
    "u.username",
    "COUNT(o.id) as total_orders",
    "SUM(o.total_amount) as total_spent",
    "AVG(o.total_amount) as avg_order_value"
  ],
  "from": "users u",
  "joins": [
    {"type": "LEFT", "table": "orders", "alias": "o", "on": "u.id = o.user_id"}
  ],
  "groupBy": ["u.id", "u.username"],
  "having": ["COUNT(o.id) > :minOrders"],
  "orderBy": ["total_spent DESC"],
  "pagination": true,
  "parameters": [
    {"name": "minOrders", "type": "Integer", "required": false, "defaultValue": "0"}
  ]
}
```

### Example 4: Query with Authorization

```json
{
  "name": "findUserDocuments",
  "description": "Find documents accessible to user",
  "returnType": "DocumentDTO",
  "select": ["d.id", "d.title", "d.created_date", "u.username as owner"],
  "from": "documents d",
  "joins": [
    {"type": "INNER", "table": "users", "alias": "u", "on": "d.owner_id = u.id"}
  ],
  "where": ["d.status = :status"],
  "orderBy": ["d.created_date DESC"],
  "pagination": true,
  "parameters": [
    {"name": "status", "type": "String", "required": true}
  ],
  "authorization": {
    "enabled": true,
    "documentField": "id"
  }
}
```

**Note:** Authorization checks each result against the authenticated user's permissions.


## Best Practices

### Query Design

1. **Use Aliases** - Always use table aliases for clarity
   ```json
   "from": "users u"
   "joins": [{"table": "orders", "alias": "o", "on": "u.id = o.user_id"}]
   ```

2. **Parameterize Everything** - Never hardcode values in SQL
   ```json
   "where": ["u.status = :status"]  // Good
   "where": ["u.status = 'active'"]  // Bad
   ```

3. **Use Pagination** - For queries that return multiple results
   ```json
   "pagination": true
   ```

4. **Meaningful Names** - Use descriptive query names
   ```json
   "name": "findActiveUsersWithRoles"  // Good
   "name": "query1"  // Bad
   ```

5. **Document Queries** - Provide clear descriptions
   ```json
   "description": "Find all active users with their assigned roles and permissions"
   ```

### Performance

1. **Index Columns** - Ensure WHERE/JOIN columns are indexed
2. **Limit Joins** - Avoid excessive joins (max 5-6)
3. **Use Aggregations Wisely** - GROUP BY can be expensive
4. **Test with Data** - Test queries with realistic data volumes

### Authorization

1. **Enable When Needed** - Only enable authorization for sensitive data
   ```json
   "authorization": {"enabled": true, "documentField": "id"}
   ```

2. **Choose Correct Field** - Use the field that identifies the document
   ```json
   "documentField": "id"  // For user records
   "documentField": "orderId"  // For order-related queries
   ```

3. **Performance Impact** - Authorization checks each result individually

### Filter Design

1. **Appropriate Operators** - Choose operators that make sense
   ```json
   // String fields
   "operators": ["equals", "contains", "startsWith"]
   
   // Numeric fields
   "operators": ["equals", "greaterThan", "lessThan", "between"]
   
   // Boolean fields
   "operators": ["equals"]
   ```

2. **Avoid Over-Filtering** - Don't add filters for every field
3. **Consider UI** - Think about how filters will be used in the frontend

### Maintenance

1. **Version Control** - Commit query_layer.json and filter_layer.json
2. **Document Changes** - Add comments in commit messages
3. **Test After Changes** - Regenerate and test after modifying queries
4. **Review Generated Code** - Check generated repositories/services

## Troubleshooting

### Common Issues

**Issue:** Query not generating code  
**Solution:** Check JSON syntax in query_layer.json

**Issue:** SQL syntax error at runtime  
**Solution:** Test SQL manually in database, check parameter bindings

**Issue:** Authorization always denies access  
**Solution:** Verify documentField matches the ID field in results

**Issue:** Pagination not working  
**Solution:** Ensure `"pagination": true` is set

**Issue:** Count query returns wrong value  
**Solution:** Check WHERE conditions match between query and count

### Debugging

1. **Check Generated Code** - Look at generated repository methods
2. **Enable SQL Logging** - Set `spring.r2dbc.show-sql=true`
3. **Test Queries Manually** - Run SQL in database client
4. **Check Parameters** - Verify parameter types and names match

## Migration from v2.3

Query and filter layers are new in v2.4. To migrate:

1. **Regenerate Definitions**
   ```bash
   python phase1_generate_definition.py --input schema.sql --output my_app
   ```

2. **Review New Files**
   - `query_layer.json` - Add custom queries
   - `filter_layer.json` - Review default filters

3. **Regenerate Code**
   ```bash
   python phase2_generate_code.py --output my_app
   ```

4. **Test Endpoints**
   - Custom query endpoints: `/api/{entity}/queries/{queryName}`

## Additional Resources

- **Session Summary:** `session_summaries/2026-03-13_query_filter_layers_implementation.md`
- **Managers Guide:** `docs/DEFINITION_MANAGERS_GUIDE.md`
- **Layer Documentation:** `docs/LAYERS_DOCUMENTATION.md`

## Support

For issues or questions:
- Check generated code in `src/main/java/.../query/`
- Review query definitions in `application_definitions/query_layer.json`
- Test SQL manually in database client
- Check application logs for errors

---

**Version:** 2.4.0  
**Last Updated:** March 13, 2026  
**Status:** Production Ready
