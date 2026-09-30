package com.example.service;

import com.example.repository.QueryGroupQueryRepository;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import java.util.List;
import java.util.Map;

/**
 * Role-based authorization service.
 * Checks authorization from JWT claims (roles, tableAccess, queryGroupMemberships).
 * SUPER_ADMIN gets all access, TABLE_ADMIN gets assigned tables, USER gets owned/shared records.
 * Zero database hits for role/table checks — only query group membership verification needs a DB call.
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class RoleAuthorizationService {

    private final QueryGroupQueryRepository queryGroupQueryRepository;

    /**
     * Check if any role in the list is SUPER_ADMIN.
     *
     * @param roles list of role name strings from JWT claims
     * @return true if any role is SUPER_ADMIN
     */
    public boolean isSuperAdmin(List<String> roles) {
        if (roles == null || roles.isEmpty()) {
            return false;
        }
        return roles.stream().anyMatch(role -> "SUPER_ADMIN".equals(role));
    }

    /**
     * Check if the user has the required operation on the given table.
     * Reads from the tableAccess JWT claim — zero database hits.
     *
     * @param tableAccessClaims map of table_name to list of allowed operations from JWT
     * @param tableName the table to check access for
     * @param operation the CRUD operation (CREATE, READ, UPDATE, DELETE)
     * @return true if the user has the operation on the table
     */
    public boolean hasTableAccess(Map<String, List<String>> tableAccessClaims, String tableName, String operation) {
        if (tableAccessClaims == null || tableName == null || operation == null) {
            return false;
        }
        List<String> allowedOperations = tableAccessClaims.get(tableName);
        if (allowedOperations == null || allowedOperations.isEmpty()) {
            return false;
        }
        return allowedOperations.contains(operation);
    }

    /**
     * Check if the user has access to a specific query via query group memberships.
     * Verifies that at least one of the user's query groups contains the requested query.
     * This requires a database call to query_group_query to resolve query names per group.
     *
     * @param queryGroupMemberships list of query_group_ids from JWT claims
     * @param queryName the query name to check access for
     * @param queryGroupQueryRepository repository to look up queries in groups
     * @return Mono<Boolean> true if any of the user's groups contain the query
     */
    public Mono<Boolean> hasQueryAccess(List<Long> queryGroupMemberships, String queryName,
                                         QueryGroupQueryRepository queryGroupQueryRepository) {
        if (queryGroupMemberships == null || queryGroupMemberships.isEmpty() || queryName == null) {
            return Mono.just(false);
        }
        return queryGroupQueryRepository.findByQueryName(queryName)
            .filter(qqEntry -> queryGroupMemberships.contains(qqEntry.getQueryGroupId()))
            .hasElements();
    }
}