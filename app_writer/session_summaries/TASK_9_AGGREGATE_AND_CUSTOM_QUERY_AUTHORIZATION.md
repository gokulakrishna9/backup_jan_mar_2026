# Task 9: Aggregate and Custom Query Authorization - COMPLETE

## Status: ✅ DONE

## User Request

"We can also grant view access to aggregate documents and custom queries with this table."

## Summary

Extended the `ems_entity_authorization` table to control access not just to individual entities, but also to:
1. **Aggregate documents** - Root entity with all children
2. **Custom query results** - Filtered by authorization

This provides a unified authorization model across all data access patterns.

## Authorization Scope

The `ems_entity_authorization` table now controls access to:

### 1. Individual Entities
```
Authorization for Course #123
→ Can access Course #123 record
```

### 2. Aggregate Documents
```
Authorization for Course #123
→ Can access Course #123 + all modules + all content + all enrollments
```

### 3. Custom Query Results
```
Authorization for Course #123, #456
→ Custom query returns only courses #123 and #456
```

## Aggregate Authorization

### Concept

Aggregates are document-like structures with a root entity and children. Authorization is controlled at the **root entity level** - if you have access to the root, you have access to its children.

### Example

```
Course #123 (root)
├── CourseModule #1
│   ├── ModuleContent #1
│   └── ModuleContent #2
├── CourseModule #2
│   └── ModuleContent #3
└── CourseEnrollment #1
```

**Authorization:**
- User has READ access to Course #123 → Can read all modules and content
- User has UPDATE access to Course #123 → Can update course, modules, and content
- User has NO access to Course #123 → Cannot access course or any children

### Implementation

```java
/**
 * Find course with all children (aggregate document).
 * Authorization check on root entity only.
 */
public Mono<CourseAggregateDTO> findAggregateById(Long courseId) {
    return authorizationService.hasAccess("Course", courseId, "READ")
        .flatMap(hasAccess -> {
            if (!hasAccess) {
                return Mono.error(new AccessDeniedException(...));
            }
            
            // Load root + children (no additional auth checks)
            return loadCourseWithChildren(courseId);
        });
}
```

### Nested Endpoints

```java
/**
 * GET /api/courses/123/modules
 * Authorization: Requires READ access to Course #123
 */
@GetMapping("/{courseId}/modules")
public Flux<CourseModuleDTO> getModules(@PathVariable Long courseId) {
    return authorizationService.hasAccess("Course", courseId, "READ")
        .flatMapMany(hasAccess -> {
            if (!hasAccess) return Flux.error(new AccessDeniedException(...));
            return moduleRepository.findByCourseId(courseId);
        });
}

/**
 * POST /api/courses/123/modules
 * Authorization: Requires UPDATE access to Course #123
 */
@PostMapping("/{courseId}/modules")
public Mono<CourseModuleDTO> addModule(
    @PathVariable Long courseId,
    @RequestBody CourseModuleInputDTO dto
) {
    return authorizationService.hasAccess("Course", courseId, "UPDATE")
        .flatMap(hasAccess -> {
            if (!hasAccess) return Mono.error(new AccessDeniedException(...));
            return moduleRepository.save(toEntity(dto, courseId));
        });
}
```

## Custom Query Authorization

### Authorization Strategies

#### 1. FILTER_BY_ACCESS
Get list of accessible entity IDs and filter query results.

**Use for:** List queries returning root entities

```java
public Flux<CourseOutputDTO> findByInstitutionId(Long institutionId) {
    return authorizationService.findAccessibleEntityIds("Course")
        .collectList()
        .flatMapMany(accessibleIds -> {
            if (accessibleIds.isEmpty()) {
                // SYSTEM_ADMIN (empty = "all")
                return repository.findByInstitutionId(institutionId);
            }
            
            // Filter by accessible IDs
            return repository.findByInstitutionIdAndIdIn(institutionId, accessibleIds);
        });
}
```

#### 2. CHECK_ROOT_ENTITY
Check authorization for specific entity ID before executing query.

**Use for:** Single entity queries, aggregate queries

```java
public Mono<CourseAnalyticsDTO> getCourseAnalytics(Long courseId) {
    return authorizationService.hasAccess("Course", courseId, "READ")
        .flatMap(hasAccess -> {
            if (!hasAccess) return Mono.error(new AccessDeniedException(...));
            return repository.findCourseAnalytics(courseId);
        });
}
```

#### 3. JOIN_AUTHORIZATION_TABLE
Join with `ems_entity_authorization` in SQL to filter at database level.

**Use for:** Complex queries, performance-critical queries

```sql
SELECT c.course_id, c.course_name, COUNT(e.enrollment_id) as enrollment_count
FROM ems_course c
LEFT JOIN ems_course_enrollment e ON c.course_id = e.course_id
INNER JOIN ems_entity_authorization ea ON 
    ea.entity_type = 'Course' AND 
    ea.entity_id = c.course_id AND 
    ea.user_id = :userId AND 
    ea.deleted_at IS NULL
WHERE c.deleted_at IS NULL
GROUP BY c.course_id, c.course_name
```

#### 4. NO_AUTHORIZATION
No authorization check (public data).

**Use for:** Public statistics, anonymous access

### Configuration

In database definition JSON:

```json
{
  "customQueries": [
    {
      "entity": "Course",
      "queries": [
        {
          "name": "findByInstitutionId",
          "returnType": "List",
          "resultClass": "Course",
          "sql": "SELECT * FROM ems_course WHERE institution_id = :institutionId",
          "requiresAuthorization": true,
          "authorizationStrategy": "FILTER_BY_ACCESS",
          "accessLevel": "READ"
        },
        {
          "name": "getCourseFinancialData",
          "returnType": "Single",
          "resultClass": "CourseFinancialDTO",
          "sql": "SELECT * FROM course_financial_view WHERE course_id = :courseId",
          "requiresAuthorization": true,
          "authorizationStrategy": "CHECK_ROOT_ENTITY",
          "accessLevel": "ADMIN"
        },
        {
          "name": "getCourseStatistics",
          "returnType": "List",
          "resultClass": "CourseStatisticsDTO",
          "sql": "SELECT c.*, COUNT(e.enrollment_id) FROM ems_course c ...",
          "requiresAuthorization": true,
          "authorizationStrategy": "JOIN_AUTHORIZATION_TABLE",
          "accessLevel": "READ"
        }
      ]
    }
  ]
}
```

## Examples

### Example 1: Aggregate Access

```
User: Bob (user_id=10)
Authorization: READ access to Course #123
Action: GET /api/courses/123/aggregate

Flow:
1. Check authorization for Course #123
2. Bob has READ access ✓
3. Load Course #123
4. Load all modules (no auth check)
5. Load all enrollments (no auth check)
6. Return aggregate document

Result: ✓ ALLOWED - Bob sees entire aggregate
```

### Example 2: Filtered Custom Query

```
User: Bob (user_id=10)
Authorization: READ access to Course #123, #456
Query: findByInstitutionId(institutionId=1)

Flow:
1. Get accessible course IDs for Bob → [123, 456]
2. Execute query with filter:
   SELECT * FROM ems_course 
   WHERE institution_id = 1 
   AND course_id IN (123, 456)
3. Return filtered results

Result: Only courses #123 and #456 (if they belong to institution #1)
```

### Example 3: Join Authorization Table

```
User: Bob (user_id=10)
Query: getCourseStatistics()

SQL:
SELECT c.course_id, c.course_name, COUNT(e.enrollment_id)
FROM ems_course c
LEFT JOIN ems_course_enrollment e ON c.course_id = e.course_id
INNER JOIN ems_entity_authorization ea ON 
    ea.entity_type = 'Course' AND 
    ea.entity_id = c.course_id AND 
    ea.user_id = 10
GROUP BY c.course_id, c.course_name

Result: Statistics for only courses Bob has access to
```

### Example 4: Sensitive Data Access

```
User: Alice (user_id=5)
Authorization: ADMIN access to Course #123
Query: getCourseFinancialData(courseId=123)

Flow:
1. Check authorization for Course #123
2. Alice has ADMIN access ✓
3. Execute query
4. Return financial data

Result: ✓ ALLOWED
```

## Benefits

### 1. Unified Authorization Model
- Same table controls access to entities, aggregates, and custom queries
- Consistent behavior across all data access patterns
- Single source of truth for permissions

### 2. Simplified Management
- Grant access to root entity → Get access to entire aggregate
- No need to manage permissions for each child entity
- Easier to understand and maintain

### 3. Performance
- Single authorization check for entire aggregate
- Database-level filtering for custom queries
- Efficient indexing on authorization table

### 4. Flexibility
- Choose appropriate authorization strategy per query
- Support for public queries (no authorization)
- Support for sensitive queries (ADMIN only)

### 5. Security
- Always filter by authorization
- Never return unauthorized data
- Explicit authorization requirements in configuration

## Files Updated

1. **RECORD_LEVEL_AUTHORIZATION_SPECIFICATION.md**
   - Added "Authorization for Aggregates" section
   - Added "Authorization for Custom Queries" section
   - Added 4 authorization strategies with examples
   - Added configuration examples
   - Added "Summary: Authorization Scope" section

2. **CUSTOM_QUERIES_SPECIFICATION.md**
   - Added `authorizationStrategy` field
   - Updated field descriptions
   - Added reference to RECORD_LEVEL_AUTHORIZATION_SPECIFICATION.md

## Key Takeaways

1. **Authorization at root level** - Check access to root entity, children inherit
2. **Multiple strategies** - Choose based on query type and performance needs
3. **Always filter** - Never return unauthorized data
4. **Database filtering** - Use JOIN_AUTHORIZATION_TABLE for performance
5. **Document requirements** - Specify authorization in configuration

The authorization system now provides comprehensive access control across all data access patterns: individual entities, aggregates, and custom queries.
