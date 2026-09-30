package com.jobportal.security;

import com.jobportal.entity.AuthUser;
import com.jobportal.auth.JwtService;
import com.jobportal.repository.AuthUserRepository;
import org.springframework.http.HttpHeaders;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.ReactiveSecurityContextHolder;
import org.springframework.web.server.ServerWebExchange;
import reactor.core.publisher.Mono;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class SecurityContextHolder {
    
    /**
     * Get current authenticated user from security context
     */
    public static Mono<AuthUser> getCurrentUser() {
        return ReactiveSecurityContextHolder.getContext()
            .map(context -> context.getAuthentication())
            .filter(auth -> auth instanceof UsernamePasswordAuthenticationToken)
            .map(auth -> (AuthUser) auth.getPrincipal())
            .switchIfEmpty(Mono.error(new RuntimeException("No authenticated user found")));
    }
    
    /**
     * Get current authenticated user, falling back to JWT in exchange header.
     */
    public static Mono<AuthUser> getCurrentUser(ServerWebExchange exchange, JwtService jwtService,
                                                 AuthUserRepository authUserRepository) {
        return ReactiveSecurityContextHolder.getContext()
            .map(context -> context.getAuthentication())
            .filter(auth -> auth instanceof UsernamePasswordAuthenticationToken)
            .map(auth -> (AuthUser) auth.getPrincipal())
            .switchIfEmpty(Mono.defer(() -> {
                if (exchange == null) {
                    return Mono.error(new RuntimeException("No authenticated user found"));
                }
                String authHeader = exchange.getRequest().getHeaders().getFirst(HttpHeaders.AUTHORIZATION);
                if (authHeader == null || !authHeader.startsWith("Bearer ")) {
                    return Mono.error(new RuntimeException("No authenticated user found"));
                }
                String token = authHeader.substring(7).trim();
                String username = jwtService.extractUsername(token);
                if (username == null) {
                    return Mono.error(new RuntimeException("Invalid JWT token"));
                }
                return authUserRepository.findByUsername(username)
                    .map(user -> {
                        List<Map<String, Object>> roleObjects = jwtService.extractRoles(token);
                        if (roleObjects != null) {
                            user.setRoles(roleObjects.stream()
                                .map(r -> r.get("role") != null ? r.get("role").toString() : "")
                                .collect(Collectors.toList()));
                        } else {
                            user.setRoles(List.of());
                        }
                        return user;
                    })
                    .switchIfEmpty(Mono.error(new RuntimeException("User not found")));
            }));
    }
    
    /**
     * Get current user ID
     */
    public static Mono<Long> getCurrentUserId() {
        return getCurrentUser()
            .map(AuthUser::getAuthUserId);
    }
}