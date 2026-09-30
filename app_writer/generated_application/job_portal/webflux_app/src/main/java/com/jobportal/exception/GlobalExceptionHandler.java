package com.jobportal.exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.bind.support.WebExchangeBindException;
import org.springframework.validation.FieldError;
import org.springframework.web.server.ServerWebExchange;
import reactor.core.publisher.Mono;
import lombok.extern.slf4j.Slf4j;

import java.time.LocalDateTime;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * Global exception handler for REST API.
 * Provides consistent error responses across all endpoints.
 */
@Slf4j
@RestControllerAdvice
public class GlobalExceptionHandler {
    
    /**
     * Handle validation errors from @Valid annotation.
     */
    @ExceptionHandler(WebExchangeBindException.class)
    public Mono<ResponseEntity<ValidationErrorResponse>> handleValidationException(
            WebExchangeBindException ex, ServerWebExchange exchange) {
        
        log.warn("Validation failed: {} errors - Path: {}", ex.getErrorCount(), exchange.getRequest().getPath());
        
        Map<String, String> fieldErrors = ex.getBindingResult()
            .getFieldErrors()
            .stream()
            .collect(Collectors.toMap(
                FieldError::getField,
                error -> error.getDefaultMessage() != null ? error.getDefaultMessage() : "Invalid value",
                (existing, replacement) -> existing
            ));
        
        ValidationErrorResponse error = ValidationErrorResponse.builder()
            .timestamp(LocalDateTime.now())
            .status(HttpStatus.BAD_REQUEST.value())
            .error(HttpStatus.BAD_REQUEST.getReasonPhrase())
            .message("Validation failed for the request")
            .path(exchange.getRequest().getPath().value())
            .errorCode("VALIDATION_ERROR")
            .fieldErrors(fieldErrors)
            .build();
        
        return Mono.just(ResponseEntity.status(HttpStatus.BAD_REQUEST).body(error));
    }
    
    /**
     * Handle entity not found errors.
     */
    @ExceptionHandler(EntityNotFoundException.class)
    public Mono<ResponseEntity<ErrorResponse>> handleEntityNotFoundException(
            EntityNotFoundException ex, ServerWebExchange exchange) {
        
        log.warn("Entity not found: {} - Path: {}", ex.getMessage(), exchange.getRequest().getPath());
        
        ErrorResponse error = ErrorResponse.builder()
            .timestamp(LocalDateTime.now())
            .status(HttpStatus.NOT_FOUND.value())
            .error(HttpStatus.NOT_FOUND.getReasonPhrase())
            .message(ex.getMessage())
            .path(exchange.getRequest().getPath().value())
            .errorCode("ENTITY_NOT_FOUND")
            .build();
        
        return Mono.just(ResponseEntity.status(HttpStatus.NOT_FOUND).body(error));
    }
    
    /**
     * Handle access denied errors.
     */
    @ExceptionHandler(AccessDeniedException.class)
    public Mono<ResponseEntity<ErrorResponse>> handleAccessDeniedException(
            AccessDeniedException ex, ServerWebExchange exchange) {
        
        log.warn("Access denied: {} - Path: {}", ex.getMessage(), exchange.getRequest().getPath());
        
        ErrorResponse error = ErrorResponse.builder()
            .timestamp(LocalDateTime.now())
            .status(HttpStatus.FORBIDDEN.value())
            .error(HttpStatus.FORBIDDEN.getReasonPhrase())
            .message(ex.getMessage())
            .path(exchange.getRequest().getPath().value())
            .errorCode("ACCESS_DENIED")
            .build();
        
        return Mono.just(ResponseEntity.status(HttpStatus.FORBIDDEN).body(error));
    }
    
    /**
     * Handle duplicate entity errors.
     */
    @ExceptionHandler(DuplicateEntityException.class)
    public Mono<ResponseEntity<ErrorResponse>> handleDuplicateEntityException(
            DuplicateEntityException ex, ServerWebExchange exchange) {
        
        log.warn("Duplicate entity: {} - Path: {}", ex.getMessage(), exchange.getRequest().getPath());
        
        ErrorResponse error = ErrorResponse.builder()
            .timestamp(LocalDateTime.now())
            .status(HttpStatus.CONFLICT.value())
            .error(HttpStatus.CONFLICT.getReasonPhrase())
            .message(ex.getMessage())
            .path(exchange.getRequest().getPath().value())
            .errorCode("DUPLICATE_ENTITY")
            .build();
        
        return Mono.just(ResponseEntity.status(HttpStatus.CONFLICT).body(error));
    }
    
    /**
     * Handle illegal argument errors.
     */
    @ExceptionHandler(IllegalArgumentException.class)
    public Mono<ResponseEntity<ErrorResponse>> handleIllegalArgumentException(
            IllegalArgumentException ex, ServerWebExchange exchange) {
        
        log.warn("Invalid argument: {} - Path: {}", ex.getMessage(), exchange.getRequest().getPath());
        
        ErrorResponse error = ErrorResponse.builder()
            .timestamp(LocalDateTime.now())
            .status(HttpStatus.BAD_REQUEST.value())
            .error(HttpStatus.BAD_REQUEST.getReasonPhrase())
            .message(ex.getMessage())
            .path(exchange.getRequest().getPath().value())
            .errorCode("INVALID_ARGUMENT")
            .build();
        
        return Mono.just(ResponseEntity.status(HttpStatus.BAD_REQUEST).body(error));
    }
    
    /**
     * Handle all other runtime exceptions.
     */
    @ExceptionHandler(RuntimeException.class)
    public Mono<ResponseEntity<ErrorResponse>> handleRuntimeException(
            RuntimeException ex, ServerWebExchange exchange) {
        
        log.error("Runtime exception: {} - Path: {}", ex.getMessage(), exchange.getRequest().getPath(), ex);
        
        ErrorResponse error = ErrorResponse.builder()
            .timestamp(LocalDateTime.now())
            .status(HttpStatus.INTERNAL_SERVER_ERROR.value())
            .error(HttpStatus.INTERNAL_SERVER_ERROR.getReasonPhrase())
            .message(ex.getMessage())
            .path(exchange.getRequest().getPath().value())
            .errorCode("RUNTIME_ERROR")
            .build();
        
        return Mono.just(ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error));
    }
    
    /**
     * Handle all other exceptions.
     */
    @ExceptionHandler(Exception.class)
    public Mono<ResponseEntity<ErrorResponse>> handleGenericException(
            Exception ex, ServerWebExchange exchange) {
        
        log.error("Unexpected exception: {} - Path: {}", ex.getMessage(), exchange.getRequest().getPath(), ex);
        
        ErrorResponse error = ErrorResponse.builder()
            .timestamp(LocalDateTime.now())
            .status(HttpStatus.INTERNAL_SERVER_ERROR.value())
            .error(HttpStatus.INTERNAL_SERVER_ERROR.getReasonPhrase())
            .message("An unexpected error occurred")
            .path(exchange.getRequest().getPath().value())
            .errorCode("INTERNAL_ERROR")
            .build();
        
        return Mono.just(ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error));
    }
}