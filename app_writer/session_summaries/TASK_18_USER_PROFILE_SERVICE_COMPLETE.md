# Task 18: User Profile Service Generator - COMPLETE

## Summary
Created comprehensive prompt for generating UserProfileService that enforces one-to-one relationship between authentication users and application user profiles, with update-only operations after initial creation during registration.

---

## Files Created

### Generator Prompt
**File:** `spring_webflux_application_writer_code_generation_prompts/15_USER_PROFILE_SERVICE_GENERATOR.md`

**Purpose:** Documents how to generate UserProfileService with one-to-one enforcement and update-only operations

---

## Key Concepts

### 1. One-to-One Relationship

**Database Level:**
```sql
-- Unique constraint in ems_auth_user_link
UNIQUE KEY uk_auth_app_user (auth_user_id, app_user_table, deleted_at)
```

**Application Level:**
- Validation before profile creation
- Update-only operations after creation
- No public API for profile creation

### 2. Convention-Based Design

**Table Naming Pattern:**
```
ems_{user_type}
```

**Examples:**
- `ems_user` (user_id)
- `ems_student` (student_id)
- `ems_instructor` (instructor_id)
- `ems_admin` (admin_id)

**ID Field Pattern:**
```
{user_type}_id
```

### 3. Profile Lifecycle

```
Registration → Profile Creation (ONE TIME)
     ↓
Profile Exists
     ↓
Update Only (NO CREATE)
```

**Profile Creation:**
- Only during registration
- Internal method (not exposed via API)
- Creates profile + link in one transaction
- Validates no existing profile

**Profile Updates:**
- Public API endpoint (PUT)
- Requires existing profile
- Throws exception if profile not found
- Authorization: self or admin

---

## Generated Methods

### Profile Retrieval Methods

1. **getProfile(authUserId, userType)**
   - Get profile for auth user
   - Returns empty if not found
   - Non-throwing version

2. **getProfileOrThrow(authUserId, userType)**
   - Get profile for auth user
   - Throws ProfileNotFoundException if not found
   - Use when profile is required

### Profile Update Methods

3. **updateProfile(authUserId, inputDTO, userType)**
   - Update existing profile
   - ONLY updates, does NOT create
   - Throws if profile not found
   - Authorization: self or admin

4. **updateProfileFields(entity, inputDTO)**
   - Helper method to update entity fields
   - Updates all fields from DTO
   - Does not update PK, created_at, deleted_at

### Profile Validation Methods

5. **hasProfile(authUserId, userType)**
   - Check if profile exists
   - Returns boolean
   - Non-blocking check

6. **validateNoExistingProfile(authUserId, userType)**
   - Validate profile does NOT exist
   - Throws ProfileAlreadyExistsException if exists
   - Used before profile creation

### Helper Methods

7. **getAuthUserLink(authUserId, userType)**
   - Get link record
   - Private helper method

8. **toOutputDTO(entity)**
   - Convert entity to DTO
   - Private helper method

---

## Multiple User Type Support

### Configuration

```javascript
const userProfileConfig = {
  userTypes: [
    {
      typeName: 'user',
      tableName: 'ems_user',
      entityClass: 'User',
      idField: 'user_id',
      repository: 'UserRepository',
      inputDTO: 'UserInputDTO',
      outputDTO: 'UserOutputDTO'
    },
    {
      typeName: 'student',
      tableName: 'ems_student',
      entityClass: 'Student',
      idField: 'student_id',
      repository: 'StudentRepository',
      inputDTO: 'StudentInputDTO',
      outputDTO: 'StudentOutputDTO'
    }
  ]
};
```

### Generated Service

```java
@Service
public class UserProfileService {
    
    // User profile methods
    public Mono<UserOutputDTO> getUserProfile(Long authUserId) { ... }
    public Mono<UserOutputDTO> updateUserProfile(Long authUserId, UserInputDTO dto) { ... }
    public Mono<Boolean> hasUserProfile(Long authUserId) { ... }
    
    // Student profile methods
    public Mono<StudentOutputDTO> getStudentProfile(Long authUserId) { ... }
    public Mono<StudentOutputDTO> updateStudentProfile(Long authUserId, StudentInputDTO dto) { ... }
    public Mono<Boolean> hasStudentProfile(Long authUserId) { ... }
}
```

---

## Integration with Registration

### Registration Flow

```java
@Service
public class RegistrationService {
    
    @Transactional
    public Mono<RegistrationResponseDTO> registerUser(UserRegistrationDTO dto) {
        // 1. Create auth user
        return authUserRepository.save(authUser)
            .flatMap(savedAuthUser -> {
                // 2. Assign default roles
                return roleService.assignDefaultRolesToNewUser(savedAuthUser.getAuthUserId())
                    .thenReturn(savedAuthUser.getAuthUserId());
            })
            .flatMap(authUserId -> {
                // 3. Create user profile (ONLY during registration)
                return createUserProfileInternal(authUserId, dto.getProfileData());
            });
    }
    
    /**
     * Internal method - NOT exposed via API.
     */
    @Transactional
    private Mono<UserOutputDTO> createUserProfileInternal(
            Long authUserId, 
            UserInputDTO dto) {
        
        // Validate no existing profile
        return userProfileService.validateNoUserProfile(authUserId)
            .then(Mono.defer(() -> {
                // Create user entity
                User user = User.builder()
                    .firstName(dto.getFirstName())
                    .lastName(dto.getLastName())
                    .build();
                
                return userRepository.save(user);
            }))
            .flatMap(savedUser -> {
                // Create link
                AuthUserLink link = AuthUserLink.builder()
                    .authUserId(authUserId)
                    .appUserTable("ems_user")
                    .appUserId(savedUser.getUserId())
                    .build();
                
                return authUserLinkRepository.save(link)
                    .thenReturn(savedUser);
            })
            .map(userProfileService::toUserOutputDTO);
    }
}
```

---

## Controller Layer - Update Only

### User Profile Controller

```java
@RestController
@RequestMapping("/api/profile")
public class UserProfileController {
    
    /**
     * Get current user's profile.
     */
    @GetMapping("/user")
    public Mono<UserOutputDTO> getCurrentUserProfile() {
        return authenticationService.getCurrentAuthUserId()
            .flatMap(userProfileService::getUserProfileOrThrow);
    }
    
    /**
     * Update current user's profile.
     * NO CREATE endpoint - profiles created during registration only.
     */
    @PutMapping("/user")
    public Mono<UserOutputDTO> updateCurrentUserProfile(
            @Valid @RequestBody UserInputDTO inputDTO) {
        
        return authenticationService.getCurrentAuthUserId()
            .flatMap(authUserId -> 
                userProfileService.updateUserProfile(authUserId, inputDTO));
    }
    
    /**
     * Admin: Update user profile by auth user ID.
     */
    @PutMapping("/user/{authUserId}")
    @PreAuthorize("hasAnyRole('ADMIN', 'SYSTEM_ADMIN')")
    public Mono<UserOutputDTO> updateUserProfile(
            @PathVariable Long authUserId,
            @Valid @RequestBody UserInputDTO inputDTO) {
        
        return userProfileService.updateUserProfile(authUserId, inputDTO);
    }
    
    // NOTE: NO POST endpoint for profile creation
    // Profiles are created ONLY during registration
}
```

---

## Authorization

### Self-Update

```java
@PreAuthorize("@authorizationService.isCurrentUser(#authUserId) or hasRole('ADMIN')")
public Mono<UserOutputDTO> updateUserProfile(Long authUserId, UserInputDTO dto) {
    // User can update their own profile OR admin can update any profile
}
```

### Admin-Only Operations

```java
@PreAuthorize("hasAnyRole('ADMIN', 'SYSTEM_ADMIN')")
public Mono<UserOutputDTO> getUserProfile(@PathVariable Long authUserId) {
    // Only admin can view other users' profiles
}
```

---

## Error Handling

### Custom Exceptions

```java
/**
 * Thrown when profile not found.
 */
public class ProfileNotFoundException extends RuntimeException {
    public ProfileNotFoundException(String message) {
        super(message);
    }
}

/**
 * Thrown when attempting to create duplicate profile.
 */
public class ProfileAlreadyExistsException extends RuntimeException {
    public ProfileAlreadyExistsException(String message) {
        super(message);
    }
}
```

### Error Messages

```java
// Profile not found
"User profile not found for auth user: 123"
"Student profile not found for auth user: 456"

// Profile already exists
"User profile already exists for auth user: 123"
"Student profile already exists for auth user: 456"
```

---

## Usage Scenarios

### Scenario 1: User Registration

```java
// Registration creates profile (ONE TIME)
POST /api/auth/register
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "password123",
  "firstName": "John",
  "lastName": "Doe"
}

// Creates:
// 1. ems_auth_user record (auth_user_id = 123)
// 2. ems_user record (user_id = 456)
// 3. ems_auth_user_link record (links 123 to 456)
// 4. ems_auth_user_role records (default roles)
```

### Scenario 2: Get Profile

```java
// User gets their own profile
GET /api/profile/user

// Returns:
{
  "userId": 456,
  "firstName": "John",
  "lastName": "Doe",
  "email": "john@example.com"
}
```

### Scenario 3: Update Profile

```java
// User updates their own profile
PUT /api/profile/user
{
  "firstName": "Jane",
  "lastName": "Smith",
  "phoneNumber": "555-1234"
}

// Updates ems_user record (user_id = 456)
// NO new record created
```

### Scenario 4: Admin Updates User Profile

```java
// Admin updates another user's profile
PUT /api/profile/user/123
{
  "firstName": "Updated",
  "lastName": "Name"
}

// Admin can update any user's profile
```

### Scenario 5: Multiple User Types

```java
// One auth user can have multiple profiles (different types)
authUserId = 123
├─ User profile (user_id = 456)
├─ Student profile (student_id = 789)
└─ Instructor profile (instructor_id = 101)

// Each profile is independent
// Each has its own link record
// Each can be updated separately
```

---

## Benefits

### 1. Data Integrity
- One-to-one relationship enforced
- No duplicate profiles
- Database constraints prevent violations
- Consistent data model

### 2. Security
- Authorization on all operations
- Users can only update own profile
- Admin can update any profile
- No public profile creation

### 3. Simplicity
- Convention-based naming
- Clear lifecycle: create once, update many
- Easy to understand
- Minimal configuration

### 4. Flexibility
- Support multiple user types
- Each type has dedicated methods
- Easy to add new types
- Type-safe operations

### 5. Performance
- Efficient queries with indexes
- Reactive (non-blocking)
- Minimal database roundtrips
- Optimized link table lookups

---

## Key Design Decisions

### 1. Update-Only After Creation
- Profiles created ONLY during registration
- All subsequent operations are updates
- No public API for profile creation
- Prevents duplicate profiles

### 2. Convention-Based Naming
- Table: `ems_{user_type}`
- ID: `{user_type}_id`
- Reduces configuration
- Predictable structure

### 3. Link Table Pattern
- Separate link table (`ems_auth_user_link`)
- Flexible: supports multiple user types
- Unique constraint enforces one-to-one
- Soft delete support

### 4. Authorization Integration
- Self-update allowed
- Admin can update any profile
- Uses existing authorization service
- Consistent with system security model

### 5. Multiple User Type Support
- One auth user can have multiple profiles
- Each profile is a different user type
- Example: Student + Instructor
- Independent lifecycle for each type

---

## Status: COMPLETE ✅

Successfully created:
1. ✅ Generator prompt document (15_USER_PROFILE_SERVICE_GENERATOR.md)
2. ✅ One-to-one enforcement strategy
3. ✅ Update-only operations after creation
4. ✅ Convention-based table naming
5. ✅ Profile retrieval methods
6. ✅ Profile update methods
7. ✅ Profile validation methods
8. ✅ Multiple user type support
9. ✅ Authorization integration
10. ✅ Registration flow integration
11. ✅ Controller layer (update-only)
12. ✅ Error handling
13. ✅ Testing guidance
14. ✅ Complete documentation

The User Profile Service Generator prompt provides complete guidance for generating profile management functionality with strict one-to-one enforcement and update-only operations after initial creation!

