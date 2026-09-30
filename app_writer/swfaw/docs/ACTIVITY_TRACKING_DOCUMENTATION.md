# Activity Tracking Module Documentation

## Overview

The Activity Tracking module provides comprehensive logging and auditing of user activities within the generated Spring WebFlux application. It tracks CRUD operations, login/logout events, and permission/grant changes, with deleted records stored as JSON for potential recovery.

## Architecture

The module consists of:
- **4 Entity Classes**: Database models for different activity types
- **4 Repository Interfaces**: R2DBC repositories for data access
- **1 Service Class**: Centralized service for logging activities
- **1 Controller Class**: REST API for querying activity logs
- **4 Database Tables**: Separate tables for different activity types

## Database Schema

### Tables

#### 1. crud_activity_log
Tracks all CRUD operations (Create, Read, Update, Delete) on entities.

**Columns:**
- `id` (BIGINT, PK): Unique identifier
- `user_id` (BIGINT): ID of user performing the operation
- `username` (VARCHAR): Username of the user
- `entity_type` (VARCHAR): Type of entity (e.g., "Student", "Course")
- `entity_id` (BIGINT): ID of the affected entity
- `operation` (VARCHAR): Operation type (CREATE, READ, UPDATE, DELETE)
- `timestamp` (DATETIME): When the operation occurred
- `ip_address` (VARCHAR): IP address of the user
- `user_agent` (TEXT): Browser/client user agent
- `changes_json` (TEXT): JSON of changes made (for UPDATE operations)
- `success` (BOOLEAN): Whether the operation succeeded
- `error_message` (TEXT): Error message if operation failed

**Indexes:**
- `idx_user_id`: Fast lookup by user
- `idx_entity`: Fast lookup by entity type and ID
- `idx_operation`: Fast lookup by operation type
- `idx_timestamp`: Fast lookup by time range

#### 2. deleted_record
Stores complete deleted records as JSON for recovery and audit purposes.

**Columns:**
- `id` (BIGINT, PK): Unique identifier
- `entity_type` (VARCHAR): Type of deleted entity
- `entity_id` (BIGINT): Original ID of the deleted entity
- `record_json` (LONGTEXT): Complete JSON representation of deleted record
- `deleted_by_user_id` (BIGINT): ID of user who deleted the record
- `deleted_by_username` (VARCHAR): Username of the deleting user
- `deleted_at` (DATETIME): When the record was deleted
- `ip_address` (VARCHAR): IP address of the user
- `reason` (TEXT): Reason for deletion (optional)
- `can_restore` (BOOLEAN): Whether the record can be restored

**Indexes:**
- `idx_entity`: Fast lookup by entity type and ID
- `idx_deleted_by`: Fast lookup by deleting user
- `idx_deleted_at`: Fast lookup by deletion time
- `idx_can_restore`: Fast lookup of restorable records

#### 3. login_activity_log
Tracks user login and logout events.

**Columns:**
- `id` (BIGINT, PK): Unique identifier
- `user_id` (BIGINT): ID of the user
- `username` (VARCHAR): Username
- `activity_type` (VARCHAR): Type of activity (LOGIN, LOGOUT, LOGIN_FAILED)
- `timestamp` (DATETIME): When the activity occurred
- `ip_address` (VARCHAR): IP address
- `user_agent` (TEXT): Browser/client user agent
- `session_id` (VARCHAR): Session identifier
- `success` (BOOLEAN): Whether the login succeeded
- `failure_reason` (TEXT): Reason for login failure
- `login_method` (VARCHAR): Method used (PASSWORD, OAUTH2, SAML)
- `oauth2_provider` (VARCHAR): OAuth2 provider name (Google, GitHub, etc.)

**Indexes:**
- `idx_user_id`: Fast lookup by user
- `idx_username`: Fast lookup by username
- `idx_activity_type`: Fast lookup by activity type
- `idx_timestamp`: Fast lookup by time range
- `idx_success`: Fast lookup of failed logins

#### 4. grant_activity_log
Tracks permission and grant changes.

**Columns:**
- `id` (BIGINT, PK): Unique identifier
- `granted_by_user_id` (BIGINT): ID of user making the change
- `granted_by_username` (VARCHAR): Username of granting user
- `target_user_id` (BIGINT): ID of user receiving the grant/revoke
- `target_username` (VARCHAR): Username of target user
- `grant_type` (VARCHAR): Type of grant (GROUP_MEMBERSHIP, ACCESS_CONTROL, DOCUMENT_PERMISSION, ROLE_CHANGE)
- `action` (VARCHAR): Action performed (GRANT, REVOKE, MODIFY)
- `entity_type` (VARCHAR): Type of entity affected
- `entity_id` (BIGINT): ID of affected entity
- `previous_value_json` (TEXT): JSON of previous state
- `new_value_json` (TEXT): JSON of new state
- `timestamp` (DATETIME): When the change occurred
- `ip_address` (VARCHAR): IP address
- `reason` (TEXT): Reason for the change

**Indexes:**
- `idx_granted_by`: Fast lookup by granting user
- `idx_target_user`: Fast lookup by target user
- `idx_grant_type`: Fast lookup by grant type
- `idx_timestamp`: Fast lookup by time range
- `idx_entity`: Fast lookup by entity

## Service Methods

### ActivityTrackingService

#### CRUD Operation Logging

```java
// Log a CREATE operation
Mono<Void> logCreate(Long userId, String username, String entityType, 
                     Long entityId, String ipAddress, String userAgent)

// Log a READ operation
Mono<Void> logRead(Long userId, String username, String entityType, 
                   Long entityId, String ipAddress, String userAgent)

// Log an UPDATE operation
Mono<Void> logUpdate(Long userId, String username, String entityType, 
                     Long entityId, String changesJson, String ipAddress, String userAgent)

// Log a DELETE operation (also stores deleted record as JSON)
Mono<Void> logDelete(Long userId, String username, String entityType, 
                     Long entityId, Object deletedRecord, String ipAddress, String reason)

// Log a failed operation
Mono<Void> logFailedOperation(Long userId, String username, String entityType, 
                              Long entityId, String operation, String errorMessage, String ipAddress)
```

#### Login/Logout Logging

```java
// Log a successful login
Mono<Void> logLogin(Long userId, String username, String ipAddress, String userAgent,
                    String sessionId, String loginMethod, String oauth2Provider)

// Log a logout
Mono<Void> logLogout(Long userId, String username, String ipAddress, String sessionId)

// Log a failed login attempt
Mono<Void> logFailedLogin(String username, String ipAddress, String userAgent,
                          String failureReason, String loginMethod)
```

#### Grant/Permission Logging

```java
// Log a permission grant
Mono<Void> logGrant(Long grantedByUserId, String grantedByUsername, Long targetUserId,
                    String targetUsername, String grantType, String entityType, Long entityId,
                    Object previousValue, Object newValue, String ipAddress, String reason)

// Log a permission revoke
Mono<Void> logRevoke(Long grantedByUserId, String grantedByUsername, Long targetUserId,
                     String targetUsername, String grantType, String entityType, Long entityId,
                     Object previousValue, String ipAddress, String reason)
```

#### Query Methods

```java
// Get CRUD activity for a user
Flux<CrudActivityLog> getUserCrudActivity(Long userId, int limit)

// Get complete history for an entity
Flux<CrudActivityLog> getEntityHistory(String entityType, Long entityId)

// Get login history for a user
Flux<LoginActivityLog> getUserLoginHistory(Long userId, int limit)

// Get grant history for a user
Flux<GrantActivityLog> getUserGrantHistory(Long userId, int limit)

// Get restorable deleted records
Flux<DeletedRecord> getRestorableRecords(String entityType)

// Get a specific deleted record
Mono<DeletedRecord> getDeletedRecord(String entityType, Long entityId)
```

## REST API Endpoints

### ActivityTrackingController

All endpoints are under `/api/activity`:

#### CRUD Activity Endpoints

```
GET /api/activity/crud/user/{userId}?limit=100
```
Get CRUD activity for a specific user.

**Parameters:**
- `userId` (path): User ID
- `limit` (query, optional): Maximum number of records (default: 100)

**Response:** Array of `CrudActivityLog` objects

---

```
GET /api/activity/crud/entity/{entityType}/{entityId}
```
Get complete history for a specific entity.

**Parameters:**
- `entityType` (path): Entity type (e.g., "Student")
- `entityId` (path): Entity ID

**Response:** Array of `CrudActivityLog` objects

---

#### Login Activity Endpoints

```
GET /api/activity/login/user/{userId}?limit=50
```
Get login history for a specific user.

**Parameters:**
- `userId` (path): User ID
- `limit` (query, optional): Maximum number of records (default: 50)

**Response:** Array of `LoginActivityLog` objects

---

#### Grant Activity Endpoints

```
GET /api/activity/grant/user/{userId}?limit=50
```
Get grant/permission history for a specific user.

**Parameters:**
- `userId` (path): User ID
- `limit` (query, optional): Maximum number of records (default: 50)

**Response:** Array of `GrantActivityLog` objects

---

#### Deleted Records Endpoints

```
GET /api/activity/deleted?entityType=Student
```
Get all restorable deleted records, optionally filtered by entity type.

**Parameters:**
- `entityType` (query, optional): Filter by entity type

**Response:** Array of `DeletedRecord` objects

---

```
GET /api/activity/deleted/{entityType}/{entityId}
```
Get a specific deleted record.

**Parameters:**
- `entityType` (path): Entity type
- `entityId` (path): Original entity ID

**Response:** `DeletedRecord` object or 404 if not found

---

## Usage Examples

### Example 1: Logging a CREATE Operation

```java
@Service
public class StudentService {
    private final ActivityTrackingService activityTrackingService;
    
    public Mono<Student> createStudent(StudentInputDTO input, ServerWebExchange exchange) {
        return studentRepository.save(student)
            .flatMap(savedStudent -> {
                String ipAddress = activityTrackingService.getIpAddress(exchange);
                String userAgent = activityTrackingService.getUserAgent(exchange);
                
                return activityTrackingService.logCreate(
                    currentUserId,
                    currentUsername,
                    "Student",
                    savedStudent.getId(),
                    ipAddress,
                    userAgent
                ).thenReturn(savedStudent);
            });
    }
}
```

### Example 2: Logging a DELETE with Record Storage

```java
public Mono<Void> deleteStudent(Long id, ServerWebExchange exchange) {
    return studentRepository.findById(id)
        .flatMap(student -> {
            String ipAddress = activityTrackingService.getIpAddress(exchange);
            
            return studentRepository.deleteById(id)
                .then(activityTrackingService.logDelete(
                    currentUserId,
                    currentUsername,
                    "Student",
                    id,
                    student, // The complete student object will be stored as JSON
                    ipAddress,
                    "User requested deletion"
                ));
        });
}
```

### Example 3: Logging a Login

```java
@Service
public class AuthService {
    private final ActivityTrackingService activityTrackingService;
    
    public Mono<LoginResponse> login(LoginRequest request, ServerWebExchange exchange) {
        return authenticateUser(request)
            .flatMap(user -> {
                String ipAddress = activityTrackingService.getIpAddress(exchange);
                String userAgent = activityTrackingService.getUserAgent(exchange);
                String sessionId = generateSessionId();
                
                return activityTrackingService.logLogin(
                    user.getId(),
                    user.getUsername(),
                    ipAddress,
                    userAgent,
                    sessionId,
                    "PASSWORD",
                    null
                ).thenReturn(createLoginResponse(user, sessionId));
            })
            .onErrorResume(error -> {
                String ipAddress = activityTrackingService.getIpAddress(exchange);
                String userAgent = activityTrackingService.getUserAgent(exchange);
                
                return activityTrackingService.logFailedLogin(
                    request.getUsername(),
                    ipAddress,
                    userAgent,
                    error.getMessage(),
                    "PASSWORD"
                ).then(Mono.error(error));
            });
    }
}
```

### Example 4: Logging a Permission Grant

```java
public Mono<Void> addUserToGroup(Long userId, Long groupId, ServerWebExchange exchange) {
    return userGroupMembershipRepository.save(membership)
        .flatMap(saved -> {
            String ipAddress = activityTrackingService.getIpAddress(exchange);
            
            return activityTrackingService.logGrant(
                currentUserId,
                currentUsername,
                userId,
                targetUsername,
                "GROUP_MEMBERSHIP",
                "UserGroup",
                groupId,
                null, // No previous value
                membership, // New membership
                ipAddress,
                "Added to group by admin"
            );
        });
}
```

### Example 5: Querying Activity Logs

```java
// Get recent CRUD activity for a user
Flux<CrudActivityLog> userActivity = activityTrackingService
    .getUserCrudActivity(userId, 50);

// Get complete history of an entity
Flux<CrudActivityLog> entityHistory = activityTrackingService
    .getEntityHistory("Student", studentId);

// Get restorable deleted students
Flux<DeletedRecord> deletedStudents = activityTrackingService
    .getRestorableRecords("Student");

// Restore a deleted record
Mono<DeletedRecord> deletedRecord = activityTrackingService
    .getDeletedRecord("Student", studentId)
    .flatMap(record -> {
        // Parse JSON and recreate the entity
        Student student = objectMapper.readValue(
            record.getRecordJson(), 
            Student.class
        );
        return studentRepository.save(student);
    });
```

## Integration with Existing Services

The activity tracking module is designed to be integrated into existing service methods. Here's how to integrate it:

1. **Inject ActivityTrackingService** into your service classes
2. **Call logging methods** after successful operations
3. **Pass ServerWebExchange** to extract IP address and user agent
4. **Handle errors** by logging failed operations

## Security Considerations

- Activity logs are **append-only** - no update or delete operations
- Access to activity logs should be **restricted to administrators**
- Deleted records contain **sensitive data** - ensure proper access control
- IP addresses and user agents are logged for **security auditing**
- Consider **data retention policies** for activity logs

## Performance Considerations

- All logging operations are **non-blocking** (return `Mono<Void>`)
- Logging happens **asynchronously** and doesn't block main operations
- Database indexes ensure **fast queries** on common access patterns
- Consider **archiving old logs** to maintain performance

## Installation

The activity tracking schema is automatically generated as `activity-tracking-schema.sql`. Run it after the auth schema:

```bash
# 1. Run auth schema
mysql -u root -p database_name < auth-schema.sql

# 2. Run activity tracking schema
mysql -u root -p database_name < activity-tracking-schema.sql

# 3. Build and run application
mvn clean install
mvn spring-boot:run
```

## Generated Files

The activity tracking module generates the following files:

### Entities (4 files)
- `CrudActivityLog.java`
- `DeletedRecord.java`
- `LoginActivityLog.java`
- `GrantActivityLog.java`

### Repositories (4 files)
- `CrudActivityLogRepository.java`
- `DeletedRecordRepository.java`
- `LoginActivityLogRepository.java`
- `GrantActivityLogRepository.java`

### Services (1 file)
- `ActivityTrackingService.java`

### Controllers (1 file)
- `ActivityTrackingController.java`

### SQL Schema (1 file)
- `activity-tracking-schema.sql`

**Total: 11 files**

## Summary

The Activity Tracking module provides:
- ✅ Complete CRUD operation logging
- ✅ Login/logout tracking with failure reasons
- ✅ Permission/grant change tracking
- ✅ Deleted records stored as JSON for recovery
- ✅ Comprehensive REST API for querying logs
- ✅ Non-blocking, reactive implementation
- ✅ Indexed database tables for fast queries
- ✅ IP address and user agent tracking
- ✅ Support for OAuth2 login tracking
- ✅ Separate table structure similar to auth/authz layers
