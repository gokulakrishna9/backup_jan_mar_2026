"""Permissions endpoint templates — generates PermissionsService, PermissionsController,
and EntityApiRegistry for the GET /api/auth/permissions endpoint.

The endpoint returns the authenticated user's allowed API operations (method + path)
resolved from user roles and table assignments (user_role table):
- SUPER_ADMIN: full access to all entity API paths
- TABLE_ADMIN: full CRUD paths only for assigned tables
- USER: READ paths for owned/shared records
"""


class PermissionsTemplates:
    """Templates for permissions endpoint generation."""

    # EntityApiRegistry — maps table names to controller base paths
    # Generated dynamically from the controller layer definitions
    ENTITY_API_REGISTRY = """package {{ packageName }};

import org.springframework.stereotype.Component;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Registry mapping database table names to their REST API base paths.
 * Auto-generated from controller layer definitions.
 */
@Component
public class EntityApiRegistry {

    private static final Map<String, String> TABLE_TO_PATH;

    static {
        Map<String, String> map = new LinkedHashMap<>();
{% for entry in entries %}
        map.put("{{ entry.tableName }}", "{{ entry.basePath }}");
{% endfor %}
        TABLE_TO_PATH = Collections.unmodifiableMap(map);
    }

    /**
     * Get the API base path for a table name.
     * @return base path or null if table has no API
     */
    public String getBasePath(String tableName) {
        return TABLE_TO_PATH.get(tableName);
    }

    /**
     * Get all table-to-path mappings.
     */
    public Map<String, String> getAllMappings() {
        return TABLE_TO_PATH;
    }
}
"""

    # PermissionsService — resolves user's allowed API operations
    PERMISSIONS_SERVICE = """package {{ packageName }};

import {{ repositoryPackage }}.UserRoleRepository;
import {{ repositoryPackage }}.RecordOwnerRepository;
import {{ repositoryPackage }}.QueryGroupMemberRepository;
import {{ repositoryPackage }}.QueryGroupRecordRepository;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * Resolves the authenticated user's allowed API operations.
 * Returns a flat list of {method, path} objects for the frontend
 * to drive UI visibility via usePermissions / allowedApiList.
 *
 * Resolution is based on user roles and table assignments:
 * - SUPER_ADMIN: full access to all entity API paths
 * - TABLE_ADMIN: full CRUD paths only for assigned tables
 * - USER: READ paths for owned/shared records
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class PermissionsService {

    private final UserRoleRepository userRoleRepository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final EntityApiRegistry entityApiRegistry;

    /**
     * Resolve all allowed API operations for the given user.
     * Reads roles and table assignments from user_role table.
     */
    public Mono<List<AllowedApi>> resolveAllowedApis(Long authUserId) {
        return userRoleRepository.findByAuthUserId(authUserId)
            .collectList()
            .flatMap(roles -> {
                // Check for SUPER_ADMIN role
                boolean isSuperAdmin = roles.stream()
                    .anyMatch(r -> "SUPER_ADMIN".equals(r.getRole()));

                if (isSuperAdmin) {
                    log.debug("SUPER_ADMIN user {} — granting full API access", authUserId);
                    return Mono.just(buildFullAccess());
                }

                // Collect TABLE_ADMIN assigned tables
                Set<String> adminTables = new LinkedHashSet<>();
                boolean hasUserRole = false;
                for (var role : roles) {
                    if ("TABLE_ADMIN".equals(role.getRole()) && role.getTableName() != null) {
                        adminTables.add(role.getTableName());
                    }
                    if ("USER".equals(role.getRole())) {
                        hasUserRole = true;
                    }
                }

                Set<AllowedApi> apis = new LinkedHashSet<>();

                // TABLE_ADMIN: full CRUD for assigned tables
                for (String tableName : adminTables) {
                    String basePath = entityApiRegistry.getBasePath(tableName);
                    if (basePath != null) {
                        apis.add(new AllowedApi("POST", basePath));
                        apis.add(new AllowedApi("GET", basePath + "/*"));
                        apis.add(new AllowedApi("GET", basePath));
                        apis.add(new AllowedApi("PUT", basePath + "/*"));
                        apis.add(new AllowedApi("DELETE", basePath + "/*"));
                    }
                }

                // USER: READ paths for all entities (owned/shared filtering at service layer)
                if (hasUserRole) {
                    for (Map.Entry<String, String> entry : entityApiRegistry.getAllMappings().entrySet()) {
                        String basePath = entry.getValue();
                        apis.add(new AllowedApi("GET", basePath + "/*"));
                        apis.add(new AllowedApi("GET", basePath));
                    }
                }

                return Mono.just(new ArrayList<>(apis));
            })
            .defaultIfEmpty(List.of());
    }

    // ── internals ──────────────────────────────────────────────

    /**
     * Build full access list — every entity gets all CRUD operations.
     */
    private List<AllowedApi> buildFullAccess() {
        List<AllowedApi> apis = new ArrayList<>();
        for (Map.Entry<String, String> entry : entityApiRegistry.getAllMappings().entrySet()) {
            String basePath = entry.getValue();
            apis.add(new AllowedApi("POST", basePath));
            apis.add(new AllowedApi("GET", basePath + "/*"));
            apis.add(new AllowedApi("GET", basePath));
            apis.add(new AllowedApi("PUT", basePath + "/*"));
            apis.add(new AllowedApi("DELETE", basePath + "/*"));
        }
        return apis;
    }

    /**
     * DTO representing one allowed API operation.
     */
    public record AllowedApi(String method, String path) {}
}
"""

    # Permissions Controller — GET /api/auth/permissions
    PERMISSIONS_CONTROLLER = """package {{ packageName }};

import {{ servicePackage }}.PermissionsService;
import {{ securityPackage }}.SecurityContextHolder;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Mono;
import lombok.RequiredArgsConstructor;
import java.util.List;

/**
 * Exposes the authenticated user's allowed API operations.
 * The React frontend calls this after login to populate allowedApiList
 * in AuthContext, which drives usePermissions visibility checks.
 */
@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
@Tag(name = "Permissions", description = "User permission resolution APIs")
public class PermissionsController {

    private final PermissionsService permissionsService;

    @Operation(
        summary = "Get current user's allowed API operations",
        description = "Returns a list of HTTP method + path pairs the authenticated user is permitted to call, "
                    + "resolved from user roles and table assignments."
    )
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Permissions resolved successfully"),
        @ApiResponse(responseCode = "401", description = "Unauthorized — authentication required")
    })
    @GetMapping("/permissions")
    public Mono<List<PermissionsService.AllowedApi>> getPermissions() {
        return SecurityContextHolder.getCurrentUserId()
            .flatMap(permissionsService::resolveAllowedApis);
    }
}
"""
