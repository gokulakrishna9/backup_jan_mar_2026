package com.example.security;

import com.example.auth.JwtService;
import com.example.service.AuthService;
import com.example.exception.ErrorResponse;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.core.io.buffer.DataBuffer;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.server.reactive.ServerHttpRequest;
import org.springframework.http.server.reactive.ServerHttpResponse;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.ReactiveSecurityContextHolder;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ServerWebExchange;
import org.springframework.web.server.WebFilter;
import org.springframework.web.server.WebFilterChain;
import reactor.core.publisher.Mono;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import java.time.LocalDateTime;
import java.util.List;

@Slf4j
@Component
@RequiredArgsConstructor
public class JwtAuthenticationFilter implements WebFilter {
    
    private final JwtService jwtService;
    private final AuthService authService;
    private final ObjectMapper objectMapper;
    
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
        ServerHttpRequest request = exchange.getRequest();
        String path = request.getPath().value();
        
        // Skip authentication for public endpoints
        if (isPublicEndpoint(path)) {
            return chain.filter(exchange);
        }
        
        // Extract JWT token from Authorization header
        String authHeader = request.getHeaders().getFirst(HttpHeaders.AUTHORIZATION);
        
        // Missing Authorization header
        if (authHeader == null || authHeader.trim().isEmpty()) {
            log.warn("Missing Authorization header for path: {}", path);
            return writeUnauthorizedResponse(exchange, "MISSING_TOKEN", 
                "Authorization header is required", path);
        }
        
        // Invalid Authorization header format
        if (!authHeader.startsWith("Bearer ")) {
            log.warn("Invalid Authorization header format for path: {}", path);
            return writeUnauthorizedResponse(exchange, "INVALID_TOKEN_FORMAT", 
                "Authorization header must start with 'Bearer '", path);
        }
        
        String token = authHeader.substring(7).trim();
        
        // Empty token
        if (token.isEmpty()) {
            log.warn("Empty JWT token for path: {}", path);
            return writeUnauthorizedResponse(exchange, "EMPTY_TOKEN", 
                "JWT token is required", path);
        }
        
        // Validate token and set security context
        return authService.validateToken(token)
            .flatMap(user -> {
                // Create authentication with authorities
                List<SimpleGrantedAuthority> authorities = List.of(new SimpleGrantedAuthority("ROLE_USER"));
                
                UsernamePasswordAuthenticationToken authentication =
                    new UsernamePasswordAuthenticationToken(user, null, authorities);
                
                // Set security context and continue filter chain
                return chain.filter(exchange)
                    .contextWrite(ReactiveSecurityContextHolder.withAuthentication(authentication));
            })
            .onErrorResume(e -> {
                // Token validation failed - return 401
                log.warn("JWT token validation failed for path {}: {}", path, e.getMessage());
                return writeUnauthorizedResponse(exchange, "INVALID_TOKEN", 
                    "Invalid or expired JWT token", path);
            });
    }
    
    private Mono<Void> writeUnauthorizedResponse(ServerWebExchange exchange, String errorCode, 
                                                  String message, String path) {
        ServerHttpResponse response = exchange.getResponse();
        response.setStatusCode(HttpStatus.UNAUTHORIZED);
        response.getHeaders().setContentType(MediaType.APPLICATION_JSON);
        
        ErrorResponse errorResponse = ErrorResponse.builder()
            .timestamp(LocalDateTime.now())
            .status(HttpStatus.UNAUTHORIZED.value())
            .error(HttpStatus.UNAUTHORIZED.getReasonPhrase())
            .message(message)
            .path(path)
            .errorCode(errorCode)
            .build();
        
        try {
            byte[] bytes = objectMapper.writeValueAsBytes(errorResponse);
            DataBuffer buffer = response.bufferFactory().wrap(bytes);
            return response.writeWith(Mono.just(buffer));
        } catch (Exception e) {
            log.error("Failed to write error response", e);
            return response.setComplete();
        }
    }
    
    private boolean isPublicEndpoint(String path) {
        return path.startsWith("/api/auth/login") ||
               path.startsWith("/api/auth/register") ||
               path.startsWith("/api/auth/refresh") ||
               path.startsWith("/setup") ||
               path.startsWith("/login") ||
               path.startsWith("/swagger-ui") ||
               path.startsWith("/v3/api-docs") ||
               path.startsWith("/webjars") ||
               path.startsWith("/favicon") ||
               path.equals("/");
    }
}