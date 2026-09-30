package com.onlineshopping.security;

import com.onlineshopping.exception.ErrorResponse;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.core.io.buffer.DataBuffer;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.server.reactive.ServerHttpResponse;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ServerWebExchange;
import reactor.core.publisher.Mono;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import java.time.LocalDateTime;

/**
 * Handles authorization denied (403 Forbidden) responses.
 * Used when a user is authenticated but lacks permission for the requested resource.
 */
@Slf4j
@Component
@RequiredArgsConstructor
public class AuthorizationDeniedHandler {
    
    private final ObjectMapper objectMapper;
    
    /**
     * Write a 403 Forbidden response with detailed error information.
     */
    public Mono<Void> handle(ServerWebExchange exchange, String operation, String resource) {
        String path = exchange.getRequest().getPath().value();
        log.warn("Access denied for operation '{}' on resource '{}' at path: {}", operation, resource, path);
        
        ServerHttpResponse response = exchange.getResponse();
        response.setStatusCode(HttpStatus.FORBIDDEN);
        response.getHeaders().setContentType(MediaType.APPLICATION_JSON);
        
        String message = String.format("Access denied: insufficient permissions for %s on %s", operation, resource);
        
        ErrorResponse errorResponse = ErrorResponse.builder()
            .timestamp(LocalDateTime.now())
            .status(HttpStatus.FORBIDDEN.value())
            .error(HttpStatus.FORBIDDEN.getReasonPhrase())
            .message(message)
            .path(path)
            .errorCode("ACCESS_DENIED")
            .build();
        
        try {
            byte[] bytes = objectMapper.writeValueAsBytes(errorResponse);
            DataBuffer buffer = response.bufferFactory().wrap(bytes);
            return response.writeWith(Mono.just(buffer));
        } catch (Exception e) {
            log.error("Failed to write forbidden response", e);
            return response.setComplete();
        }
    }
    
    /**
     * Write a generic 403 Forbidden response.
     */
    public Mono<Void> handleGeneric(ServerWebExchange exchange, String message) {
        String path = exchange.getRequest().getPath().value();
        log.warn("Access denied at path {}: {}", path, message);
        
        ServerHttpResponse response = exchange.getResponse();
        response.setStatusCode(HttpStatus.FORBIDDEN);
        response.getHeaders().setContentType(MediaType.APPLICATION_JSON);
        
        ErrorResponse errorResponse = ErrorResponse.builder()
            .timestamp(LocalDateTime.now())
            .status(HttpStatus.FORBIDDEN.value())
            .error(HttpStatus.FORBIDDEN.getReasonPhrase())
            .message(message)
            .path(path)
            .errorCode("ACCESS_DENIED")
            .build();
        
        try {
            byte[] bytes = objectMapper.writeValueAsBytes(errorResponse);
            DataBuffer buffer = response.bufferFactory().wrap(bytes);
            return response.writeWith(Mono.just(buffer));
        } catch (Exception e) {
            log.error("Failed to write forbidden response", e);
            return response.setComplete();
        }
    }
}