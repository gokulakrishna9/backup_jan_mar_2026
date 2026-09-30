package com.example.security;

import com.example.entity.AuthUser;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.ReactiveSecurityContextHolder;
import reactor.core.publisher.Mono;

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
     * Get current user ID
     */
    public static Mono<Long> getCurrentUserId() {
        return getCurrentUser()
            .map(AuthUser::getAuthUserId);
    }
}