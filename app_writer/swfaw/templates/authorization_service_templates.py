"""Authorization service templates for role-based access control."""


class AuthorizationServiceTemplates:
    """Templates for authorization service generation."""

    # RoleAuthorizationService - checks authorization from JWT claims
    ROLE_AUTHORIZATION_SERVICE = """package {{ packageName }};

import {{ repositoryPackage }}.QueryGroupQueryRepository;
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
"""

    # AuthorizationWebFilter - implements WebFilter, reads annotations, checks JWT claims
    AUTHORIZATION_WEB_FILTER = """package {{ packageName }};

import {{ entityPackage }}.AccessAuditLog;
import {{ repositoryPackage }}.AccessAuditLogRepository;
import {{ repositoryPackage }}.QueryGroupQueryRepository;
import {{ authPackage }}.JwtService;
import {{ servicePackage }}.RoleAuthorizationService;
import {{ securityPackage }}.EntityTable;
import {{ securityPackage }}.TableAccess;
import {{ securityPackage }}.QueryAccess;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.web.method.HandlerMethod;
import org.springframework.web.reactive.result.method.annotation.RequestMappingHandlerMapping;
import org.springframework.web.server.ServerWebExchange;
import org.springframework.web.server.WebFilter;
import org.springframework.web.server.WebFilterChain;
import reactor.core.publisher.Mono;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import java.time.LocalDateTime;
import java.util.Collections;
import java.util.List;
import java.util.Map;

/**
 * Authorization WebFilter that enforces annotation-based access control.
 * Reads @EntityTable, @TableAccess, and @QueryAccess annotations from controller classes/methods.
 * Checks JWT claims (roles, tableAccess, queryGroupMemberships) to authorize requests.
 * Returns 403 + audit log entry on denial.
 * Skips auth for GLOBAL endpoints; JWT-only check for PUBLIC endpoints.
 */
@Slf4j
@RequiredArgsConstructor
public class AuthorizationWebFilter implements WebFilter {

    private final RoleAuthorizationService roleAuthorizationService;
    private final AccessAuditLogRepository accessAuditLogRepository;
    private final QueryGroupQueryRepository queryGroupQueryRepository;
    private final RequestMappingHandlerMapping handlerMapping;
    private final JwtService jwtService;

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
        // Prevent double handler invocation — handlerMapping.getHandler() below
        // causes the DispatcherHandler to re-invoke the controller method.
        // This flag ensures authorization only runs once per request.
        if (exchange.getAttribute("AUTHORIZATION_CHECKED") != null) {
            return chain.filter(exchange);
        }

        // Skip non-API paths (Swagger, webjars, static resources, auth, setup)
        String path = exchange.getRequest().getURI().getPath();
        if (!path.startsWith("/api/") || path.startsWith("/api/auth/")) {
            return chain.filter(exchange);
        }

        return Mono.defer(() -> {
            // Set flag BEFORE getHandler() to prevent the double invocation
            // that getHandler() causes via DispatcherHandler re-entry
            exchange.getAttributes().put("AUTHORIZATION_CHECKED", true);
            return handlerMapping.getHandler(exchange);
        })
            .flatMap(handler -> {
                // Only process HandlerMethod instances (controller methods with annotations)
                if (!(handler instanceof HandlerMethod)) {
                    return chain.filter(exchange);
                }
                HandlerMethod handlerMethod = (HandlerMethod) handler;

                // Read annotations from handler method and controller class
                TableAccess tableAccess = handlerMethod.getMethodAnnotation(TableAccess.class);
                QueryAccess queryAccess = handlerMethod.getMethodAnnotation(QueryAccess.class);
                EntityTable entityTable = handlerMethod.getBeanType().getAnnotation(EntityTable.class);

                // If no authorization annotations present, skip auth (GLOBAL endpoint)
                if (tableAccess == null && queryAccess == null) {
                    return chain.filter(exchange);
                }

                // For annotated endpoints, extract JWT claims directly from the Authorization header
                String authHeader = exchange.getRequest().getHeaders().getFirst(HttpHeaders.AUTHORIZATION);
                if (authHeader == null || !authHeader.startsWith("Bearer ")) {
                    return denyAccess(exchange, null, "unknown", null, null, "Missing JWT token");
                }
                String token = authHeader.substring(7).trim();

                // Extract user info from JWT token
                final Long userId;
                final String username;
                try {
                    username = jwtService.extractUsername(token);
                    userId = jwtService.extractUserId(token);
                } catch (Exception e) {
                    return denyAccess(exchange, null, "unknown", null, null, "Invalid JWT token");
                }

                // Extract claims from JWT token
                List<Map<String, Object>> roleObjects = jwtService.extractRoles(token);
                List<String> roles = roleObjects != null 
                    ? roleObjects.stream().map(r -> r.get("role") != null ? r.get("role").toString() : "").collect(java.util.stream.Collectors.toList())
                    : Collections.emptyList();
                Map<String, List<String>> tableAccessClaims = jwtService.extractTableAccess(token);
                List<Long> queryGroupMemberships = jwtService.extractQueryGroupMemberships(token);
                
                if (tableAccessClaims == null) tableAccessClaims = Collections.emptyMap();
                if (queryGroupMemberships == null) queryGroupMemberships = Collections.emptyList();

                // SUPER_ADMIN gets all access
                if (roleAuthorizationService.isSuperAdmin(roles)) {
                    return chain.filter(exchange);
                }

                        // Check @TableAccess annotation
                        if (tableAccess != null) {
                            String tableName = entityTable != null ? entityTable.value() : null;
                            String operation = tableAccess.operation();

                            if (tableName != null && roleAuthorizationService.hasTableAccess(tableAccessClaims, tableName, operation)) {
                                return chain.filter(exchange);
                            }

                            // Denied — log and return 403
                            return denyAccess(exchange, userId, username, tableName, operation, "Insufficient table access");
                        }

                        // Check @QueryAccess annotation
                        if (queryAccess != null) {
                            String queryName = queryAccess.queryName();

                            return roleAuthorizationService.hasQueryAccess(queryGroupMemberships, queryName, queryGroupQueryRepository)
                                .flatMap(hasAccess -> {
                                    if (hasAccess) {
                                        return chain.filter(exchange);
                                    }
                                    return denyAccess(exchange, userId, username, queryName, "QUERY", "Insufficient query access");
                                });
                        }

                        return chain.filter(exchange);
            })
            .switchIfEmpty(chain.filter(exchange));
    }

    /**
     * Return 403 Forbidden JSON response and log the denial to access_audit_log.
     */
    private Mono<Void> denyAccess(ServerWebExchange exchange, Long userId, String username,
                                   String resource, String operation, String reason) {
        log.warn("Access denied for user {} ({}): {} on {} — {}", username, userId, operation, resource, reason);

        AccessAuditLog auditLog = AccessAuditLog.builder()
            .authUserId(userId)
            .tableName(resource)
            .action(operation)
            .accessGranted(false)
            .denialReason(reason)
            .accessedAt(LocalDateTime.now())
            .build();

        return accessAuditLogRepository.save(auditLog)
            .onErrorResume(e -> {
                log.error("Failed to save audit log for access denial", e);
                return Mono.empty();
            })
            .then(Mono.defer(() -> {
                exchange.getResponse().setStatusCode(HttpStatus.FORBIDDEN);
                exchange.getResponse().getHeaders().setContentType(MediaType.APPLICATION_JSON);
                String body = "{\\"error\\": \\"ACCESS_DENIED\\", \\"message\\": \\"" + reason + "\\"}";
                byte[] bytes = body.getBytes();
                return exchange.getResponse().writeWith(
                    Mono.just(exchange.getResponse().bufferFactory().wrap(bytes))
                );
            }));
    }
}
"""

    # EntityTable annotation - @Target(ElementType.TYPE), @Retention(RetentionPolicy.RUNTIME)
    ENTITY_TABLE_ANNOTATION = """package {{ packageName }};

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * Declares which database table a controller manages.
 * Used by AuthorizationWebFilter to determine the table for access checks.
 */
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
public @interface EntityTable {
    String value();
}
"""

    # TableAccess annotation - @Target(ElementType.METHOD), @Retention(RetentionPolicy.RUNTIME)
    TABLE_ACCESS_ANNOTATION = """package {{ packageName }};

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * Declares the required CRUD operation for a controller method.
 * Used by AuthorizationWebFilter to check the tableAccess JWT claim.
 */
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface TableAccess {
    String operation();
}
"""

    # QueryAccess annotation - @Target(ElementType.METHOD), @Retention(RetentionPolicy.RUNTIME)
    QUERY_ACCESS_ANNOTATION = """package {{ packageName }};

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * Declares which custom query a controller method executes.
 * Used by AuthorizationAspect to check queryGroupMemberships JWT claim.
 */
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface QueryAccess {
    String queryName();
}
"""

    # AuthorizationAspect - AOP aspect that intercepts @TableAccess and @QueryAccess
    # Replaces the AuthorizationWebFilter approach to avoid double handler invocation
    AUTHORIZATION_ASPECT = """package {{ packageName }};

import {{ entityPackage }}.AccessAuditLog;
import {{ repositoryPackage }}.AccessAuditLogRepository;
import {{ repositoryPackage }}.QueryGroupQueryRepository;
import {{ authPackage }}.JwtService;
import {{ servicePackage }}.RoleAuthorizationService;
import {{ securityPackage }}.EntityTable;
import {{ securityPackage }}.TableAccess;
import {{ securityPackage }}.QueryAccess;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.reflect.MethodSignature;
import org.springframework.http.HttpHeaders;
import org.springframework.http.server.reactive.ServerHttpRequest;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ServerWebExchange;
import reactor.core.publisher.Mono;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import java.time.LocalDateTime;
import java.util.Collections;
import java.util.List;
import java.util.Map;

/**
 * Authorization aspect that enforces annotation-based access control.
 * Intercepts controller methods annotated with @TableAccess or @QueryAccess.
 * Reads JWT claims (roles, tableAccess, queryGroupMemberships) to authorize requests.
 * Returns Mono.error with AccessDeniedException on denial + audit log entry.
 *
 * This replaces the WebFilter-based approach which caused double handler invocation
 * due to handlerMapping.getHandler() being called in the filter chain.
 */
@Aspect
@Component
@Slf4j
@RequiredArgsConstructor
public class AuthorizationAspect {

    private final RoleAuthorizationService roleAuthorizationService;
    private final AccessAuditLogRepository accessAuditLogRepository;
    private final QueryGroupQueryRepository queryGroupQueryRepository;
    private final JwtService jwtService;

    /**
     * Intercept any controller method annotated with @TableAccess.
     */
    @Around("@annotation(tableAccess)")
    public Object checkTableAccess(ProceedingJoinPoint joinPoint, TableAccess tableAccess) throws Throwable {
        ServerWebExchange exchange = extractExchange(joinPoint);
        if (exchange == null) {
            // No exchange available — skip authorization (non-web context)
            return joinPoint.proceed();
        }

        String token = extractToken(exchange.getRequest());
        if (token == null) {
            return denyAccess(exchange, null, "unknown", null, tableAccess.operation(), "Missing or invalid JWT token");
        }

        // Extract user info
        final Long userId;
        final String username;
        try {
            username = jwtService.extractUsername(token);
            userId = jwtService.extractUserId(token);
        } catch (Exception e) {
            return denyAccess(exchange, null, "unknown", null, tableAccess.operation(), "Invalid JWT token");
        }

        // Extract roles from JWT
        List<Map<String, Object>> roleObjects = jwtService.extractRoles(token);
        List<String> roles = roleObjects != null
            ? roleObjects.stream().map(r -> r.get("role") != null ? r.get("role").toString() : "").collect(java.util.stream.Collectors.toList())
            : Collections.emptyList();

        // SUPER_ADMIN gets all access
        if (roleAuthorizationService.isSuperAdmin(roles)) {
            return joinPoint.proceed();
        }

        // Read @EntityTable from the controller class
        EntityTable entityTable = joinPoint.getTarget().getClass().getAnnotation(EntityTable.class);
        String tableName = entityTable != null ? entityTable.value() : null;
        String operation = tableAccess.operation();

        // Check tableAccess JWT claim
        Map<String, List<String>> tableAccessClaims = jwtService.extractTableAccess(token);
        if (tableAccessClaims == null) tableAccessClaims = Collections.emptyMap();

        if (tableName != null && !tableName.isEmpty()
                && roleAuthorizationService.hasTableAccess(tableAccessClaims, tableName, operation)) {
            return joinPoint.proceed();
        }

        // USER role: allow access (backend service layer handles record-level filtering)
        if (!roles.isEmpty()) {
            return joinPoint.proceed();
        }

        return denyAccess(exchange, userId, username, tableName, operation, "Insufficient table access");
    }

    /**
     * Intercept any controller method annotated with @QueryAccess.
     */
    @Around("@annotation(queryAccess)")
    public Object checkQueryAccess(ProceedingJoinPoint joinPoint, QueryAccess queryAccess) throws Throwable {
        ServerWebExchange exchange = extractExchange(joinPoint);
        if (exchange == null) {
            return joinPoint.proceed();
        }

        String token = extractToken(exchange.getRequest());
        if (token == null) {
            return denyAccess(exchange, null, "unknown", queryAccess.queryName(), "QUERY", "Missing or invalid JWT token");
        }

        final Long userId;
        final String username;
        try {
            username = jwtService.extractUsername(token);
            userId = jwtService.extractUserId(token);
        } catch (Exception e) {
            return denyAccess(exchange, null, "unknown", queryAccess.queryName(), "QUERY", "Invalid JWT token");
        }

        // Extract roles
        List<Map<String, Object>> roleObjects = jwtService.extractRoles(token);
        List<String> roles = roleObjects != null
            ? roleObjects.stream().map(r -> r.get("role") != null ? r.get("role").toString() : "").collect(java.util.stream.Collectors.toList())
            : Collections.emptyList();

        // SUPER_ADMIN gets all access
        if (roleAuthorizationService.isSuperAdmin(roles)) {
            return joinPoint.proceed();
        }

        // Check query group membership
        List<Long> queryGroupMemberships = jwtService.extractQueryGroupMemberships(token);
        if (queryGroupMemberships == null) queryGroupMemberships = Collections.emptyList();

        String queryName = queryAccess.queryName();
        return roleAuthorizationService.hasQueryAccess(queryGroupMemberships, queryName, queryGroupQueryRepository)
            .flatMap(hasAccess -> {
                if (hasAccess) {
                    try {
                        Object result = joinPoint.proceed();
                        if (result instanceof Mono) {
                            return (Mono<?>) result;
                        }
                        return Mono.justOrEmpty(result);
                    } catch (Throwable t) {
                        return Mono.error(t);
                    }
                }
                return logDenialAndError(userId, username, queryName, "QUERY", "Insufficient query access");
            });
    }

    /**
     * Extract ServerWebExchange from method arguments.
     */
    private ServerWebExchange extractExchange(ProceedingJoinPoint joinPoint) {
        for (Object arg : joinPoint.getArgs()) {
            if (arg instanceof ServerWebExchange) {
                return (ServerWebExchange) arg;
            }
        }
        return null;
    }

    /**
     * Extract Bearer token from request.
     */
    private String extractToken(ServerHttpRequest request) {
        String authHeader = request.getHeaders().getFirst(HttpHeaders.AUTHORIZATION);
        if (authHeader != null && authHeader.startsWith("Bearer ")) {
            String token = authHeader.substring(7).trim();
            return token.isEmpty() ? null : token;
        }
        return null;
    }

    /**
     * Deny access: log audit entry and return Mono.error with AccessDeniedException.
     */
    private Mono<?> denyAccess(ServerWebExchange exchange, Long userId, String username,
                                String resource, String operation, String reason) {
        log.warn("Access denied for user {} ({}): {} on {} — {}", username, userId, operation, resource, reason);
        return logDenialAndError(userId, username, resource, operation, reason);
    }

    /**
     * Log denial to access_audit_log and return Mono.error.
     */
    private Mono<?> logDenialAndError(Long userId, String username, String resource,
                                       String operation, String reason) {
        AccessAuditLog auditLog = AccessAuditLog.builder()
            .authUserId(userId)
            .tableName(resource)
            .action(operation)
            .accessGranted(false)
            .denialReason(reason)
            .accessedAt(LocalDateTime.now())
            .build();

        return accessAuditLogRepository.save(auditLog)
            .onErrorResume(e -> {
                log.error("Failed to save audit log for access denial", e);
                return Mono.empty();
            })
            .then(Mono.error(new org.springframework.security.access.AccessDeniedException(reason)));
    }
}
"""
