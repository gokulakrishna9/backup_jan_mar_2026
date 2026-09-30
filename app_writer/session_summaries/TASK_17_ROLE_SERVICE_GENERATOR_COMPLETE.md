# Task 17: Role Service Generator Prompt - COMPLETE

## Summary
Created comprehensive prompt for generating RoleService that handles default role assignment to new users and provides admin methods for role management.

---

## Files Created

### 1. Generator Prompt
**File:** `spring_webflux_application_writer_code_generation_prompts/14_ROLE_SERVICE_GENERATOR.md`

**Purpose:** Documents how to generate RoleService with complete role management functionality

### 2. Sample Implementation
**File:** `code_output/RoleService.java`

**Purpose:** Complete working implementation of RoleService

---

## Key Features

### 1. Default Role Assignment

**Automatic Role Assignment:**
```java
// Assign default USER role to new user
roleService.assignDefaultRolesToNewUser(authUserId);
```

**Custom Role Assignment:**
```java
// Assign custom roles for different user types
roleService.assignDefaultRolesToNewUser(authUserId, List.of("USER", "STUDENT"));
roleService.assignDefaultRolesToNewUser(authUserId, List.of("USER", "INSTRUCTOR", "COURSE_CREATOR"));
```

**Integration with Registration:**
```java
@Transactional
public Mono<AuthUserOutputDTO> register(RegisterDTO dto) {
    return authUserRepository.save(authUser)
        .flatMap(savedUser -> 
            roleService.assignDefaultRolesToNewUser(savedUser.getAuthUserId())
                .thenReturn(savedUser)
        )
        .map(this::toOutputDTO);
}
```

### 2. Admin Role Management

**Create Role:**
```java
@PostMapping("/api/admin/roles")
@PreAuthorize("hasAnyRole('ADMIN', 'SYSTEM_ADMIN')")
public Mono<RoleOutputDTO> createRole(@Valid @RequestBody RoleInputDTO roleInputDTO) {
    return roleService.createRole(roleInputDTO);
}
```

**Update Role:**
```java
@PutMapping("/api/admin/roles/{roleId}")
@PreAuthorize("hasAnyRole('ADMIN', 'SYSTEM_ADMIN')")
public Mono<RoleOutputDTO> updateRole(
        @PathVariable Long roleId,
        @Valid @RequestBody RoleInputDTO roleInputDTO) {
    return roleService.updateRole(roleId, roleInputDTO);
}
```

**Delete Role:**
```java
@DeleteMapping("/api/admin/roles/{roleId}")
@PreAuthorize("hasAnyRole('ADMIN', 'SYSTEM_ADMIN')")
public Mono<Void> deleteRole(@PathVariable Long roleId) {
    return roleService.deleteRole(roleId);
}
```

### 3. User Role Assignment (Admin)

**Assign Role to User:**
```java
@PostMapping("/api/admin/users/{authUserId}/roles/{roleId}")
@PreAuthorize("hasAnyRole('ADMIN', 'SYSTEM_ADMIN')")
public Mono<Void> assignRoleToUser(
        @PathVariable Long authUserId,
        @PathVariable Long roleId) {
    return roleService.assignRoleToUserByAdmin(authUserId, roleId);
}
```

**Remove Role from User:**
```java
@DeleteMapping("/api/admin/users/{authUserId}/roles/{roleId}")
@PreAuthorize("hasAnyRole('ADMIN', 'SYSTEM_ADMIN')")
public Mono<Void> removeRoleFromUser(
        @PathVariable Long authUserId,
        @PathVariable Long roleId) {
    return roleService.removeRoleFromUser(authUserId, roleId);
}
```

**Get User Roles:**
```java
@GetMapping("/api/admin/users/{authUserId}/roles")
@PreAuthorize("hasAnyRole('ADMIN', 'SYSTEM_ADMIN')")
public Flux<RoleOutputDTO> getUserRoles(@PathVariable Long authUserId) {
    return roleService.getUserRoles(authUserId);
}
```

---

## Generated Methods

### Default Role Assignment Methods

1. **assignDefaultRolesToNewUser(authUserId)**
   - Assigns default USER role
   - Called automatically during registration
   - Transactional

2. **assignDefaultRolesToNewUser(authUserId, roleNames)**
   - Assigns custom list of roles
   - For different user types (student, instructor, etc.)
   - Transactional

3. **assignRoleToUser(authUserId, roleId)** (private)
   - Internal method for role assignment
   - Checks for duplicates
   - Creates AuthUserRole record

### Admin Role Management Methods

4. **createRole(roleInputDTO)**
   - Create new role (ADMIN only)
   - Validates uniqueness
   - Uppercase role name

5. **updateRole(roleId, roleInputDTO)**
   - Update role description (ADMIN only)
   - Protects system roles
   - Cannot modify USER, ADMIN, SYSTEM_ADMIN

6. **deleteRole(roleId)**
   - Soft delete role (ADMIN only)
   - Protects system roles
   - Sets deleted_at timestamp

7. **getAllRoles()**
   - Get all roles (ADMIN only)
   - Returns active roles only

8. **getRoleById(roleId)**
   - Get role by ID (ADMIN only)

9. **getRoleByName(roleName)**
   - Get role by name (ADMIN only)

### User Role Assignment Methods

10. **assignRoleToUserByAdmin(authUserId, roleId)**
    - Assign role to user (ADMIN only)
    - SYSTEM_ADMIN role requires SYSTEM_ADMIN permission
    - Validates role exists

11. **assignRolesToUserByAdmin(authUserId, roleIds)**
    - Bulk role assignment (ADMIN only)
    - Assigns multiple roles at once

12. **removeRoleFromUser(authUserId, roleId)**
    - Remove role from user (ADMIN only)
    - Prevents removing last USER role
    - SYSTEM_ADMIN role requires SYSTEM_ADMIN permission

13. **getUserRoles(authUserId)**
    - Get all roles for a user
    - Returns active roles only

### Helper Methods

14. **hasAdminRole(user)** (private)
    - Check if user has ADMIN or SYSTEM_ADMIN role

15. **hasSystemAdminRole(user)** (private)
    - Check if user has SYSTEM_ADMIN role

16. **toOutputDTO(role)** (private)
    - Convert Role entity to RoleOutputDTO

---

## Configuration

### Default Roles

```javascript
const roleServiceConfig = {
  // Default roles assigned to new users
  defaultRoles: ['USER'],
  
  // Protected system roles (cannot be deleted/modified)
  protectedRoles: ['USER', 'ADMIN', 'SYSTEM_ADMIN']
};
```

### User Type Roles

```javascript
const userTypeRoles = {
  'student': ['USER', 'STUDENT'],
  'instructor': ['USER', 'INSTRUCTOR', 'COURSE_CREATOR'],
  'admin': ['USER', 'ADMIN'],
  'system_admin': ['USER', 'ADMIN', 'SYSTEM_ADMIN']
};
```

---

## Security Features

### 1. Permission Checks
- All admin operations require ADMIN or SYSTEM_ADMIN role
- SYSTEM_ADMIN role can only be assigned/removed by SYSTEM_ADMIN
- Protected roles cannot be deleted or modified

### 2. Role Protection
- System roles (USER, ADMIN, SYSTEM_ADMIN) are protected
- Cannot delete protected roles
- Cannot modify protected role names

### 3. Validation
- Prevent duplicate role assignments
- Prevent removing last USER role from user
- Validate role existence before assignment
- Role name must be uppercase with underscores

### 4. Audit Trail
- Comprehensive logging
- Created/updated timestamps
- Soft delete (deleted_at)

---

## DTOs

### RoleInputDTO

```java
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class RoleInputDTO {
    
    @NotBlank(message = "Role name is required")
    @Size(min = 2, max = 50)
    @Pattern(regexp = "^[A-Z_]+$", message = "Role name must be uppercase")
    private String roleName;
    
    @Size(max = 255)
    private String description;
}
```

### RoleOutputDTO

```java
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class RoleOutputDTO {
    private Long roleId;
    private String roleName;
    private String description;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
```

---

## Usage Scenarios

### Scenario 1: User Registration

```java
// 1. Create auth user
AuthUser authUser = new AuthUser(...);

// 2. Save and assign default role
authUserRepository.save(authUser)
    .flatMap(savedUser -> 
        roleService.assignDefaultRolesToNewUser(savedUser.getAuthUserId())
            .thenReturn(savedUser)
    );
```

### Scenario 2: Student Registration

```java
// Assign student-specific roles
roleService.assignDefaultRolesToNewUser(
    authUserId, 
    List.of("USER", "STUDENT")
);
```

### Scenario 3: Admin Creating Custom Role

```java
// Admin creates DEPARTMENT_HEAD role
RoleInputDTO input = new RoleInputDTO(
    "DEPARTMENT_HEAD",
    "Head of academic department"
);

roleService.createRole(input);
```

### Scenario 4: Admin Promoting User

```java
// Admin assigns COURSE_CREATOR role to instructor
roleService.assignRoleToUserByAdmin(instructorAuthUserId, courseCreatorRoleId);
```

### Scenario 5: Admin Demoting User

```java
// Admin removes COURSE_CREATOR role
roleService.removeRoleFromUser(instructorAuthUserId, courseCreatorRoleId);
```

---

## Integration Points

### 1. UserService
```java
@Service
public class UserService {
    private final RoleService roleService;
    
    @Transactional
    public Mono<AuthUser> createUser(AuthUser authUser) {
        return authUserRepository.save(authUser)
            .flatMap(savedUser -> 
                roleService.assignDefaultRolesToNewUser(savedUser.getAuthUserId())
                    .thenReturn(savedUser)
            );
    }
}
```

### 2. AuthService
```java
@Service
public class AuthService {
    private final RoleService roleService;
    
    @Transactional
    public Mono<AuthUserOutputDTO> register(RegisterDTO dto) {
        return createAuthUser(dto)
            .flatMap(authUser -> 
                roleService.assignDefaultRolesToNewUser(authUser.getAuthUserId())
                    .thenReturn(authUser)
            );
    }
}
```

### 3. RoleController
```java
@RestController
@RequestMapping("/api/admin/roles")
public class RoleController {
    private final RoleService roleService;
    
    @PostMapping
    public Mono<RoleOutputDTO> createRole(@Valid @RequestBody RoleInputDTO dto) {
        return roleService.createRole(dto);
    }
}
```

---

## Error Handling

### Custom Exceptions

1. **RoleNotFoundException**
   - Thrown when role not found by ID or name
   - HTTP 404

2. **RoleAlreadyExistsException**
   - Thrown when creating duplicate role
   - HTTP 409

3. **AccessDeniedException**
   - Thrown when user lacks permission
   - HTTP 403

### Error Messages

```java
// Role not found
"Default role not found: USER"
"Role not found: CUSTOM_ROLE"

// Access denied
"Only ADMIN or SYSTEM_ADMIN can create roles"
"Only SYSTEM_ADMIN can assign SYSTEM_ADMIN role"
"Cannot modify protected system role: USER"
"Cannot delete protected system role: ADMIN"
"Cannot remove last USER role from user"

// Duplicate
"Role already exists: CUSTOM_ROLE"
```

---

## Testing

### Unit Tests

```java
@Test
void assignDefaultRolesToNewUser_Success() {
    // Given
    Long authUserId = 1L;
    when(roleRepository.findByRoleNameAndDeletedAtIsNull("USER"))
        .thenReturn(Mono.just(userRole));
    
    // When/Then
    StepVerifier.create(roleService.assignDefaultRolesToNewUser(authUserId))
        .verifyComplete();
}

@Test
void createRole_AsAdmin_Success() {
    // Given
    RoleInputDTO input = new RoleInputDTO("CUSTOM_ROLE", "Description");
    when(userService.getCurrentUser()).thenReturn(Mono.just(adminUser));
    
    // When/Then
    StepVerifier.create(roleService.createRole(input))
        .expectNextCount(1)
        .verifyComplete();
}

@Test
void createRole_AsNonAdmin_AccessDenied() {
    // Given
    when(userService.getCurrentUser()).thenReturn(Mono.just(regularUser));
    
    // When/Then
    StepVerifier.create(roleService.createRole(input))
        .expectError(AccessDeniedException.class)
        .verify();
}
```

---

## Benefits

### 1. Automation
- Automatic role assignment during registration
- No manual intervention needed
- Consistent role assignment

### 2. Flexibility
- Configurable default roles
- Custom roles per user type
- Easy to extend

### 3. Security
- Admin-only role management
- Protected system roles
- Permission validation

### 4. Maintainability
- Centralized role logic
- Clear separation of concerns
- Comprehensive logging

### 5. Scalability
- Reactive (non-blocking)
- Transactional
- Efficient queries

---

## Status: COMPLETE ✅

Successfully created:
1. ✅ Generator prompt document (14_ROLE_SERVICE_GENERATOR.md)
2. ✅ Sample implementation (RoleService.java)
3. ✅ Default role assignment methods
4. ✅ Admin role management methods
5. ✅ User role assignment methods
6. ✅ Security and validation
7. ✅ Integration examples
8. ✅ Testing guidance
9. ✅ Complete documentation

The Role Service Generator prompt provides complete guidance for generating role management functionality with automatic default role assignment and admin role management capabilities!
