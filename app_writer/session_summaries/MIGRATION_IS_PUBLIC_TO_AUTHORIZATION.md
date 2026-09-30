# Migration: is_public Field to Authorization System

## Issue Identified

The old prompts reference an `is_public` field that conflicts with the new comprehensive authorization system.

### Old Approach (is_public field)
```java
@Column("is_public")
private Boolean isPublic;
```

**Problems:**
- Database field for each entity
- Simple boolean (public or private)
- No granular control
- Cannot grant public read to specific records
- Conflicts with record-level authorization

### New Approach (publicReadAccess configuration)
```json
{
  "tables": [
    {
      "name": "ems_course",
      "recordLevelAuthorization": {
        "enabled": true,
        "publicReadAccess": true,
        "requireAuthorizationFor": ["CREATE", "UPDATE", "DELETE"]
      }
    }
  ]
}
```

**Benefits:**
- Configuration-based (no database field needed)
- Table-level setting
- Works with authorization system
- Can be enabled/disabled per table
- Consistent with authorization model

---

## Migration Strategy

### Option 1: Remove is_public Field (RECOMMENDED)

**Remove from:**
1. Entity layer specifications
2. Repository layer specifications
3. Service layer specifications
4. DTO layer specifications
5. SQL parser specifications

**Replace with:**
- `publicReadAccess` configuration in table-level authorization config
- Authorization checks in service layer

### Option 2: Keep is_public as Optional Feature

**If keeping:**
- Make it optional (not automatic for root entities)
- Add configuration flag: `includeIsPublicField: boolean`
- Document that it's separate from authorization system
- Use for simple public/private toggle

---

## Recommended Changes

### 1. Remove Automatic is_public Field

**Current (OLD):**
```javascript
// In entity transformer
if (isRootEntity(table)) {
  properties.hasPublicFlag = true;
  properties.fields.push({
    columnName: 'is_public',
    fieldName: 'isPublic',
    javaType: 'Boolean'
  });
}
```

**New (RECOMMENDED):**
```javascript
// Remove automatic is_public field
// Use publicReadAccess configuration instead
if (table.recordLevelAuthorization?.publicReadAccess) {
  // Skip authorization check for READ operations
  // in service layer
}
```

### 2. Update Service Layer Logic

**Current (OLD):**
```java
public Flux<CourseOutputDTO> findPublicCourses() {
    return repository.findByIsPublicTrueAndDeletedAtIsNull()
        .map(this::toOutputDTO);
}
```

**New (RECOMMENDED):**
```java
public Flux<CourseOutputDTO> findPublicCourses() {
    // If publicReadAccess = true, return all courses
    // If publicReadAccess = false, return only authorized courses
    if (isPublicReadAccessEnabled()) {
        return repository.findAllByDeletedAtIsNull()
            .map(this::toOutputDTO);
    } else {
        return findAccessibleForCurrentUser();
    }
}
```

### 3. Update Repository Queries

**Current (OLD):**
```java
@Query("SELECT * FROM ems_course WHERE is_public = true AND deleted_at IS NULL")
Flux<Course> findPublicCourses();
```

**New (RECOMMENDED):**
```java
// No special query needed
// Use standard findAll with authorization filtering
@Query("SELECT * FROM ems_course WHERE deleted_at IS NULL")
Flux<Course> findAllActive();
```

### 4. Update Configuration

**Add to table configuration:**
```json
{
  "name": "ems_course",
  "recordLevelAuthorization": {
    "enabled": true,
    "publicReadAccess": true,  // ← Replaces is_public field
    "requireAuthorizationFor": ["CREATE", "UPDATE", "DELETE"]
  }
}
```

---

## Implementation Plan

### Phase 1: Update Specifications (IMMEDIATE)

1. ✅ Update `01_ENTITY_LAYER.md` - Remove is_public field
2. ✅ Update `02_DTO_LAYER.md` - Remove is_public field
3. ✅ Update `03_REPOSITORY_LAYER.md` - Remove public queries
4. ✅ Update `04_SERVICE_LAYER.md` - Use publicReadAccess config
5. ✅ Update `12_SQL_PARSER.md` - Don't exclude is_public
6. ✅ Update `GENERATOR_IMPLEMENTATION_PROMPT.md` - Remove is_public references

### Phase 2: Update Authorization Logic

1. ✅ Service layer checks `publicReadAccess` configuration
2. ✅ If `publicReadAccess = true`, skip authorization for READ
3. ✅ If `publicReadAccess = false`, require authorization for READ
4. ✅ Always require authorization for CREATE/UPDATE/DELETE

### Phase 3: Documentation

1. ✅ Document publicReadAccess in authorization spec
2. ✅ Add migration guide
3. ✅ Update examples

---

## Comparison

| Feature | is_public Field | publicReadAccess Config |
|---------|----------------|------------------------|
| Storage | Database field | Configuration only |
| Granularity | Per record | Per table |
| Flexibility | Low | High |
| Authorization | Separate system | Integrated |
| Performance | Extra column | No extra column |
| Complexity | Simple | Moderate |
| Recommended | ❌ No | ✅ Yes |

---

## Decision

**RECOMMENDED: Remove is_public field entirely and use publicReadAccess configuration.**

**Rationale:**
1. Simpler database schema (no extra field)
2. Integrated with authorization system
3. Configuration-based (easier to change)
4. Table-level setting (consistent)
5. No conflicts with record-level authorization

---

## Updated Service Layer Pattern

```java
@Service
@RequiredArgsConstructor
public class CourseService {
    
    private final CourseRepository repository;
    private final AuthorizationService authorizationService;
    private final CourseConfiguration config;  // Contains publicReadAccess setting
    
    /**
     * Find course by ID.
     * Authorization: 
     * - If publicReadAccess = true, allow anyone to read
     * - If publicReadAccess = false, require authorization
     */
    public Mono<CourseOutputDTO> findById(Long courseId) {
        // Check if public read access is enabled
        if (config.isPublicReadAccessEnabled()) {
            // Public access - no authorization check
            return repository.findById(courseId)
                .map(this::toOutputDTO);
        }
        
        // Private access - require authorization
        return authorizationService.hasAccess("Course", courseId, "READ")
            .flatMap(hasAccess -> {
                if (!hasAccess) {
                    return Mono.error(new AccessDeniedException(
                        "You don't have access to this course"));
                }
                return repository.findById(courseId).map(this::toOutputDTO);
            });
    }
    
    /**
     * Find all courses.
     * Authorization:
     * - If publicReadAccess = true, return all courses
     * - If publicReadAccess = false, return only authorized courses
     */
    public Flux<CourseOutputDTO> findAll() {
        if (config.isPublicReadAccessEnabled()) {
            // Public access - return all
            return repository.findAll()
                .map(this::toOutputDTO);
        }
        
        // Private access - return only authorized
        return findAccessibleForCurrentUser();
    }
}
```

---

## Summary

**Action Required:**
1. Remove `is_public` field from entity specifications
2. Remove public queries from repository specifications
3. Update service layer to use `publicReadAccess` configuration
4. Update SQL parser to not exclude `is_public`
5. Document `publicReadAccess` as the recommended approach

**Benefits:**
- Cleaner database schema
- Integrated authorization
- Configuration-based
- More flexible
- No conflicts

**Migration Path:**
- Existing databases with `is_public` field can keep it
- New applications use `publicReadAccess` configuration
- Generator supports both (with config flag)
