/**
 * Sample Spring WebFlux Authorization Layer Code
 * 
 * This is an outline showing the structure of the generated authorization code.
 * Demonstrates dual-layer authorization (table-level + record-level) with group support.
 */

// ============================================================================
// ENTITIES
// ============================================================================

@Data
@Builder
@Table("ems_user_group")
class UserGroup {
    @Id
    private Long groupId;
    private String groupName;
    private String description;
    private Long createdByUserId;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    private LocalDateTime deletedAt;
}

@Data
@Builder
@Table("ems_user_group_membership")
class UserGroupMembership {
    @Id
    private Long membershipId;
    private Long userId;
    private Long groupId;
    private Long addedByUserId;
    private LocalDateTime addedAt;
    private LocalDateTime expiresAt;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    private LocalDateTime deletedAt;
}

@Data
@Builder
@Table("ems_entity_authorization")
class EntityAuthorization {
    @Id
    private Long authorizationId;
    private String entityType;      // 'Course', 'Institution', etc.
    private Long entityId;          // ID of specific record
    private Long userId;            // User access (NULL if group-based)
    private Long groupId;           // Group access (NULL if user-based)
    private String accessLevel;     // 'READ', 'UPDATE', 'DELETE', 'ADMIN'
    private Long grantedByUserId;
    private LocalDateTime grantedAt;
    private LocalDateTime expiresAt;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    private LocalDateTime deletedAt;
}

// ============================================================================
// REPOSITORIES
// ============================================================================

interface UserGroupRepository extends R2dbcRepository<UserGroup, Long> {
    Mono<UserGroup> findByGroupName(String groupName);
    Flux<UserGroup> findByDeletedAtIsNull();
}

interface UserGroupMembershipRepository extends R2dbcRepository<UserGroupMembership, Long> {
    
    @Query("SELECT * FROM ems_user_group_membership " +
           "WHERE user_id = :userId AND deleted_at IS NULL")
    Flux<UserGroupMembership> findActiveByUserId(Long userId);
    
    @Query("SELECT * FROM ems_user_group_membership " +
           "WHERE group_id = :groupId AND deleted_at IS NULL")
    Flux<UserGroupMembership> findActiveByGroupId(Long groupId);
    
    Mono<UserGroupMembership> findByUserIdAndGroupIdAndDeletedAtIsNull(Long userId, Long groupId);
}

interface EntityAuthorizationRepository extends R2dbcRepository<EntityAuthorization, Long> {
    
    /**
     * Find authorizations for user including group memberships.
     */
    @Query("SELECT DISTINCT ea.* FROM ems_entity_authorization ea " +
           "LEFT JOIN ems_user_group_membership ugm ON " +
           "    ea.group_id = ugm.group_id AND ugm.deleted_at IS NULL " +
           "WHERE ea.entity_type = :entityType " +
           "AND ea.entity_id = :entityId " +
           "AND ea.deleted_at IS NULL " +
           "AND (ea.expires_at IS NULL OR ea.expires_at > NOW()) " +
           "AND (ea.user_id = :userId OR ugm.user_id = :userId)")
    Flux<EntityAuthorization> findValidAuthorizationsIncludingGroups(
        Long userId, String entityType, Long entityId);
    
    /**
     * Find all accessible entity IDs for user including groups.
     */
    @Query("SELECT DISTINCT ea.entity_id FROM ems_entity_authorization ea " +
           "LEFT JOIN ems_user_group_membership ugm ON " +
           "    ea.group_id = ugm.group_id AND ugm.deleted_at IS NULL " +
           "WHERE ea.entity_type = :entityType " +
           "AND ea.deleted_at IS NULL " +
           "AND (ea.expires_at IS NULL OR ea.expires_at > NOW()) " +
           "AND (ea.user_id = :userId OR ugm.user_id = :userId)")
    Flux<Long> findAccessibleEntityIdsIncludingGroups(Long userId, String entityType);
}

// ============================================================================
// AUTHORIZATION SERVICE
// ============================================================================

@Slf4j
@Service
@RequiredArgsConstructor
class AuthorizationService {
    
    private final EntityAuthorizationRepository authorizationRepository;
    private final UserGroupMembershipRepository membershipRepository;
    private final UserService userService;
    
    /**
     * Check if user has access to specific record.
     * Implements dual-layer authorization:
     * 1. SYSTEM_ADMIN bypasses all checks
     * 2. TABLE_ADMIN/TABLE_CREATOR can CREATE (but need record-level for READ/UPDATE/DELETE)
     * 3. Record-level: Check entity_authorization (user + groups)
     */
    public Mono<Boolean> hasAccess(String entityType, Long entityId, String accessLevel) {
        return userService.getCurrentUser()
            .flatMap(user -> {
                // Layer 1: SYSTEM_ADMIN bypasses ALL checks
                if (hasSystemAdminRole(user)) {
                    log.debug("Access granted: SYSTEM_ADMIN role");
                    return Mono.just(true);
                }
                
                // Layer 1: For CREATE operations, check table-level roles
                if ("CREATE".equalsIgnoreCase(accessLevel)) {
                    String tableAdminRole = entityType.toUpperCase() + "_ADMIN";
                    String tableCreatorRole = entityType.toUpperCase() + "_CREATOR";
                    
                    if (hasRole(user, tableAdminRole) || hasRole(user, tableCreatorRole)) {
                        log.debug("Access granted: {} or {} role for CREATE", 
                            tableAdminRole, tableCreatorRole);
                        return Mono.just(true);
                    }
                }
                
                // Layer 2: Check record-level authorization (user + groups)
                return checkRecordLevelAccessWithGroups(
                    user.getUserId(), entityType, entityId, accessLevel);
            });
    }
    
    /**
     * Check record-level access including group memberships.
     */
    private Mono<Boolean> checkRecordLevelAccessWithGroups(
        Long userId, String entityType, Long entityId, String requiredAccessLevel) {
        
        return authorizationRepository
            .findValidAuthorizationsIncludingGroups(userId, entityType, entityId)
            .any(auth -> hasRequiredAccessLevel(auth.getAccessLevel(), requiredAccessLevel))
            .doOnNext(hasAccess -> {
                if (hasAccess) {
                    log.debug("Access granted: user={}, entity={}:{}", 
                        userId, entityType, entityId);
                } else {
                    log.debug("Access denied: user={}, entity={}:{}", 
                        userId, entityType, entityId);
                }
            });
    }
    
    /**
     * Check if user's access level is sufficient.
     * Hierarchy: ADMIN (5) > DELETE (4) > UPDATE (3) > CREATE (2) > READ (1)
     */
    private boolean hasRequiredAccessLevel(String userAccessLevel, String requiredAccessLevel) {
        int userLevel = getAccessLevelRank(userAccessLevel);
        int requiredLevel = getAccessLevelRank(requiredAccessLevel);
        return userLevel >= requiredLevel;
    }
    
    private int getAccessLevelRank(String accessLevel) {
        return switch (accessLevel.toUpperCase()) {
            case "READ" -> 1;
            case "CREATE" -> 2;
            case "UPDATE" -> 3;
            case "DELETE" -> 4;
            case "ADMIN" -> 5;
            default -> 0;
        };
    }
    
    /**
     * Create default authorization when entity is created.
     * Creator gets CREATE, READ, UPDATE, DELETE access (4 records).
     */
    @Transactional
    public Mono<Void> createDefaultAuthorization(
        String entityType, Long entityId, Long creatorUserId) {
        
        List<EntityAuthorization> authorizations = List.of(
            buildAuthorization(entityType, entityId, creatorUserId, "CREATE"),
            buildAuthorization(entityType, entityId, creatorUserId, "READ"),
            buildAuthorization(entityType, entityId, creatorUserId, "UPDATE"),
            buildAuthorization(entityType, entityId, creatorUserId, "DELETE")
        );
        
        return Flux.fromIterable(authorizations)
            .flatMap(authorizationRepository::save)
            .then()
            .doOnSuccess(v -> log.info("Default authorizations created: entity={}:{}, user={}", 
                entityType, entityId, creatorUserId))
            .onErrorResume(throwable -> {
                log.error("Failed to create authorizations: {}", throwable.getMessage());
                return Mono.error(new RuntimeException("Authorization creation failed", throwable));
            });
    }
    
    /**
     * Grant access to user for specific record.
     */
    public Mono<EntityAuthorization> grantAccessToUser(
        String entityType, Long entityId, Long targetUserId, String accessLevel) {
        
        return userService.getCurrentUser()
            .flatMap(currentUser -> hasAccess(entityType, entityId, "ADMIN")
                .flatMap(hasAdminAccess -> {
                    if (!hasAdminAccess) {
                        return Mono.error(new AccessDeniedException(
                            "Only users with ADMIN access can grant permissions"));
                    }
                    
                    EntityAuthorization authorization = buildAuthorization(
                        entityType, entityId, targetUserId, accessLevel);
                    authorization.setGrantedByUserId(currentUser.getUserId());
                    
                    return authorizationRepository.save(authorization);
                }));
    }
    
    /**
     * Grant access to group for specific record.
     * All group members inherit this access.
     */
    public Mono<EntityAuthorization> grantAccessToGroup(
        String entityType, Long entityId, Long groupId, String accessLevel) {
        
        return userService.getCurrentUser()
            .flatMap(currentUser -> hasAccess(entityType, entityId, "ADMIN")
                .flatMap(hasAdminAccess -> {
                    if (!hasAdminAccess) {
                        return Mono.error(new AccessDeniedException(
                            "Only users with ADMIN access can grant permissions"));
                    }
                    
                    EntityAuthorization authorization = EntityAuthorization.builder()
                        .entityType(entityType)
                        .entityId(entityId)
                        .groupId(groupId)  // Group-based
                        .userId(null)      // Not user-based
                        .accessLevel(accessLevel)
                        .grantedByUserId(currentUser.getUserId())
                        .grantedAt(LocalDateTime.now())
                        .build();
                    
                    return authorizationRepository.save(authorization);
                }));
    }
    
    /**
     * Find all entities user has access to (including groups).
     */
    public Flux<Long> findAccessibleEntityIds(String entityType) {
        return userService.getCurrentUser()
            .flatMapMany(user -> {
                // Only SYSTEM_ADMIN has access to all entities
                if (hasSystemAdminRole(user)) {
                    return Flux.empty(); // Special case: means "all"
                }
                
                // Return only authorized entity IDs (user + groups)
                return authorizationRepository.findAccessibleEntityIdsIncludingGroups(
                    user.getUserId(), entityType);
            });
    }
    
    private EntityAuthorization buildAuthorization(
        String entityType, Long entityId, Long userId, String accessLevel) {
        return EntityAuthorization.builder()
            .entityType(entityType)
            .entityId(entityId)
            .userId(userId)
            .groupId(null)
            .accessLevel(accessLevel)
            .grantedByUserId(userId)
            .grantedAt(LocalDateTime.now())
            .build();
    }
    
    private boolean hasRole(User user, String roleName) {
        return user.getRoles() != null &&
               user.getRoles().stream().anyMatch(r -> r.getRoleName().equals(roleName));
    }
    
    private boolean hasSystemAdminRole(User user) {
        return hasRole(user, "SYSTEM_ADMIN");
    }
}

// ============================================================================
// USER GROUP SERVICE
// ============================================================================

@Service
@RequiredArgsConstructor
class UserGroupService {
    
    private final UserGroupRepository groupRepository;
    private final UserGroupMembershipRepository membershipRepository;
    private final UserService userService;
    
    /**
     * Create a new user group.
     */
    public Mono<UserGroup> createGroup(String groupName, String description) {
        return userService.getCurrentUser()
            .flatMap(currentUser -> {
                UserGroup group = UserGroup.builder()
                    .groupName(groupName)
                    .description(description)
                    .createdByUserId(currentUser.getUserId())
                    .createdAt(LocalDateTime.now())
                    .build();
                
                return groupRepository.save(group);
            });
    }
    
    /**
     * Add user to group.
     */
    public Mono<UserGroupMembership> addUserToGroup(Long userId, Long groupId) {
        return userService.getCurrentUser()
            .flatMap(currentUser -> {
                UserGroupMembership membership = UserGroupMembership.builder()
                    .userId(userId)
                    .groupId(groupId)
                    .addedByUserId(currentUser.getUserId())
                    .addedAt(LocalDateTime.now())
                    .build();
                
                return membershipRepository.save(membership);
            });
    }
    
    /**
     * Remove user from group (soft delete).
     */
    public Mono<Void> removeUserFromGroup(Long userId, Long groupId) {
        return membershipRepository.findByUserIdAndGroupIdAndDeletedAtIsNull(userId, groupId)
            .flatMap(membership -> {
                membership.setDeletedAt(LocalDateTime.now());
                return membershipRepository.save(membership);
            })
            .then();
    }
    
    /**
     * Get all groups for user.
     */
    public Flux<UserGroup> getUserGroups(Long userId) {
        return membershipRepository.findActiveByUserId(userId)
            .flatMap(membership -> groupRepository.findById(membership.getGroupId()));
    }
    
    /**
     * Get all members of group.
     */
    public Flux<User> getGroupMembers(Long groupId) {
        return membershipRepository.findActiveByGroupId(groupId)
            .flatMap(membership -> userService.findById(membership.getUserId()));
    }
}

// ============================================================================
// SERVICE LAYER (with authorization)
// ============================================================================

@Service
@RequiredArgsConstructor
class CourseService {
    
    private final CourseRepository repository;
    private final AuthorizationService authorizationService;
    private final UserService userService;
    
    /**
     * Create course.
     * Table-level: Requires COURSE_CREATOR, COURSE_ADMIN, or SYSTEM_ADMIN role.
     * Record-level: Creator gets CREATE, READ, UPDATE, DELETE access (4 records).
     * TRANSACTION: Entity creation + authorization creation must be atomic.
     */
    @Transactional
    @PreAuthorize("hasAnyRole('COURSE_CREATOR', 'COURSE_ADMIN', 'SYSTEM_ADMIN')")
    public Mono<CourseOutputDTO> create(CourseInputDTO dto) {
        return userService.getCurrentUser()
            .flatMap(currentUser -> {
                Course course = toEntity(dto);
                
                // Transactional: Save course + create 4 authorization records
                return repository.save(course)
                    .flatMap(savedCourse -> 
                        authorizationService.createDefaultAuthorization(
                            "Course", savedCourse.getCourseId(), currentUser.getUserId()
                        ).thenReturn(savedCourse)
                    )
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find course by ID.
     * Authorization: Requires READ access (user or group).
     */
    public Mono<CourseOutputDTO> findById(Long courseId) {
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
     * Find all accessible courses for current user.
     * Returns only courses user has access to (user + groups).
     */
    public Flux<CourseOutputDTO> findAccessibleForCurrentUser() {
        return userService.getCurrentUser()
            .flatMapMany(user -> {
                // Only SYSTEM_ADMIN can see all courses
                if (hasSystemAdminRole(user)) {
                    return repository.findAll();
                }
                
                // Return only accessible courses (user + groups)
                return authorizationService.findAccessibleEntityIds("Course")
                    .flatMap(repository::findById);
            })
            .map(this::toOutputDTO);
    }
    
    /**
     * Update course.
     * Authorization: Requires UPDATE access (user or group).
     */
    @Transactional
    public Mono<CourseOutputDTO> update(Long courseId, CourseInputDTO dto) {
        return authorizationService.hasAccess("Course", courseId, "UPDATE")
            .flatMap(hasAccess -> {
                if (!hasAccess) {
                    return Mono.error(new AccessDeniedException(
                        "You don't have UPDATE access to this course"));
                }
                
                return repository.findById(courseId)
                    .flatMap(course -> {
                        updateEntityFromDTO(course, dto);
                        return repository.save(course);
                    })
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Delete course (soft delete).
     * Authorization: Requires DELETE access (user or group).
     */
    @Transactional
    public Mono<Void> delete(Long courseId) {
        return authorizationService.hasAccess("Course", courseId, "DELETE")
            .flatMap(hasAccess -> {
                if (!hasAccess) {
                    return Mono.error(new AccessDeniedException(
                        "You don't have DELETE access to this course"));
                }
                
                return repository.findById(courseId)
                    .flatMap(course -> {
                        course.setDeletedAt(LocalDateTime.now());
                        return repository.save(course);
                    })
                    .then();
            });
    }
    
    /**
     * Grant access to user.
     * Requires ADMIN access to the course.
     */
    @Transactional
    public Mono<Void> grantAccessToUser(Long courseId, Long userId, String accessLevel) {
        return authorizationService.grantAccessToUser("Course", courseId, userId, accessLevel)
            .then();
    }
    
    /**
     * Grant access to group.
     * Requires ADMIN access to the course.
     * All group members inherit this access.
     */
    @Transactional
    public Mono<Void> grantAccessToGroup(Long courseId, Long groupId, String accessLevel) {
        return authorizationService.grantAccessToGroup("Course", courseId, groupId, accessLevel)
            .then();
    }
    
    // Helper methods
    private Course toEntity(CourseInputDTO dto) { /* ... */ return null; }
    private CourseOutputDTO toOutputDTO(Course course) { /* ... */ return null; }
    private void updateEntityFromDTO(Course course, CourseInputDTO dto) { /* ... */ }
    private boolean hasSystemAdminRole(User user) { /* ... */ return false; }
}

// ============================================================================
// CONTROLLER LAYER
// ============================================================================

@RestController
@RequestMapping("/api/courses")
@RequiredArgsConstructor
class CourseController {
    
    private final CourseService service;
    
    @PostMapping
    public Mono<CourseOutputDTO> create(@RequestBody CourseInputDTO dto) {
        return service.create(dto);
    }
    
    @GetMapping("/{id}")
    public Mono<CourseOutputDTO> findById(@PathVariable Long id) {
        return service.findById(id);
    }
    
    @GetMapping
    public Flux<CourseOutputDTO> findAccessible() {
        return service.findAccessibleForCurrentUser();
    }
    
    @PutMapping("/{id}")
    public Mono<CourseOutputDTO> update(@PathVariable Long id, @RequestBody CourseInputDTO dto) {
        return service.update(id, dto);
    }
    
    @DeleteMapping("/{id}")
    public Mono<Void> delete(@PathVariable Long id) {
        return service.delete(id);
    }
    
    /**
     * Grant access to user.
     * POST /api/courses/123/grant-access/user
     */
    @PostMapping("/{id}/grant-access/user")
    public Mono<Void> grantAccessToUser(
        @PathVariable Long id,
        @RequestBody GrantAccessDTO dto) {
        return service.grantAccessToUser(id, dto.getUserId(), dto.getAccessLevel());
    }
    
    /**
     * Grant access to group.
     * POST /api/courses/123/grant-access/group
     */
    @PostMapping("/{id}/grant-access/group")
    public Mono<Void> grantAccessToGroup(
        @PathVariable Long id,
        @RequestBody GrantAccessDTO dto) {
        return service.grantAccessToGroup(id, dto.getGroupId(), dto.getAccessLevel());
    }
}

// ============================================================================
// DTOs
// ============================================================================

@Data
class GrantAccessDTO {
    private Long userId;
    private Long groupId;
    private String accessLevel;  // READ, UPDATE, DELETE, ADMIN
}

// ============================================================================
// SUMMARY
// ============================================================================

/**
 * Authorization Flow:
 * 
 * 1. CREATE Operation:
 *    - Check table-level role (COURSE_ADMIN, COURSE_CREATOR, SYSTEM_ADMIN)
 *    - If authorized, create entity + 4 authorization records (transaction)
 * 
 * 2. READ/UPDATE/DELETE Operations:
 *    - SYSTEM_ADMIN: Bypass all checks
 *    - Others: Check record-level authorization (user + groups)
 *    - Query joins entity_authorization with user_group_membership
 *    - User gets highest access level from all sources
 * 
 * 3. Grant Access:
 *    - Requires ADMIN access to entity
 *    - Can grant to individual user OR entire group
 *    - Group members automatically inherit access
 * 
 * 4. Access Hierarchy:
 *    ADMIN (5) > DELETE (4) > UPDATE (3) > CREATE (2) > READ (1)
 *    Higher levels include lower level permissions
 * 
 * 5. Group Benefits:
 *    - Grant to group instead of individual users
 *    - Automatic access propagation
 *    - Users can belong to multiple groups
 *    - Efficient permission management
 */
