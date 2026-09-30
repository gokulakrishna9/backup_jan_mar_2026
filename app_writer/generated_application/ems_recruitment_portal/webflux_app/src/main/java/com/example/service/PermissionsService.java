package com.example.service;

import com.example.repository.UserRoleRepository;
import com.example.repository.RecordOwnerRepository;
import com.example.repository.QueryGroupMemberRepository;
import com.example.repository.QueryGroupRecordRepository;
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