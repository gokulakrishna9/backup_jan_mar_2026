package com.example.security;

import com.example.entity.AccessAuditLog;
import com.example.entity.AuthUser;
import com.example.repository.AccessAuditLogRepository;
import com.example.repository.QueryGroupQueryRepository;
import com.example.auth.JwtService;
import com.example.service.RoleAuthorizationService;
import com.example.security.EntityTable;
import com.example.security.TableAccess;
import com.example.security.QueryAccess;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.security.core.context.ReactiveSecurityContextHolder;
import org.springframework.stereotype.Component;
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
@Component
@RequiredArgsConstructor
public class AuthorizationWebFilter implements WebFilter {

    private final RoleAuthorizationService roleAuthorizationService;
    private final AccessAuditLogRepository accessAuditLogRepository;
    private final QueryGroupQueryRepository queryGroupQueryRepository;
    private final RequestMappingHandlerMapping handlerMapping;
    private final JwtService jwtService;

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
        return handlerMapping.getHandler(exchange)
            .cast(HandlerMethod.class)
            .flatMap(handlerMethod -> {
                // Read annotations from handler method and controller class
                TableAccess tableAccess = handlerMethod.getMethodAnnotation(TableAccess.class);
                QueryAccess queryAccess = handlerMethod.getMethodAnnotation(QueryAccess.class);
                EntityTable entityTable = handlerMethod.getBeanType().getAnnotation(EntityTable.class);

                // If no authorization annotations present, skip auth (GLOBAL endpoint)
                if (tableAccess == null && queryAccess == null) {
                    return chain.filter(exchange);
                }

                // For annotated endpoints, extract JWT claims from the Authorization header
                return ReactiveSecurityContextHolder.getContext()
                    .flatMap(securityContext -> {
                        Object principal = securityContext.getAuthentication().getPrincipal();
                        
                        // Extract JWT token from Authorization header to read claims
                        String authHeader = exchange.getRequest().getHeaders().getFirst(HttpHeaders.AUTHORIZATION);
                        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
                            return denyAccess(exchange, null, "unknown", null, null, "Missing JWT token");
                        }
                        String token = authHeader.substring(7).trim();
                        
                        // Extract user info from principal (AuthUser) or token
                        final Long userId;
                        final String username;
                        if (principal instanceof AuthUser) {
                            AuthUser authUser = (AuthUser) principal;
                            userId = authUser.getAuthUserId();
                            username = authUser.getUsername();
                        } else {
                            userId = null;
                            username = "unknown";
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
                    .switchIfEmpty(denyAccess(exchange, null, "anonymous", null, null, "No authentication context"));
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
                String body = "{\"error\": \"ACCESS_DENIED\", \"message\": \"" + reason + "\"}";
                byte[] bytes = body.getBytes();
                return exchange.getResponse().writeWith(
                    Mono.just(exchange.getResponse().bufferFactory().wrap(bytes))
                );
            }));
    }
}