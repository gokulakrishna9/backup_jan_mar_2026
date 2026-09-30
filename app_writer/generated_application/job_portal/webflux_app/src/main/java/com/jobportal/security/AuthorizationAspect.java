package com.jobportal.security;

import com.jobportal.entity.AccessAuditLog;
import com.jobportal.repository.AccessAuditLogRepository;
import com.jobportal.repository.QueryGroupQueryRepository;
import com.jobportal.auth.JwtService;
import com.jobportal.service.RoleAuthorizationService;
import com.jobportal.security.EntityTable;
import com.jobportal.security.TableAccess;
import com.jobportal.security.QueryAccess;
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