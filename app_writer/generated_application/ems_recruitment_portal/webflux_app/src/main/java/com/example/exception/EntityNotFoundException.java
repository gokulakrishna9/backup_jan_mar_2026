package com.example.exception;

/**
 * Exception thrown when an entity is not found.
 */
public class EntityNotFoundException extends RuntimeException {
    
    public EntityNotFoundException(String message) {
        super(message);
    }
    
    public EntityNotFoundException(String entityType, Long id) {
        super(String.format("%s with id %d not found", entityType, id));
    }
    
    public EntityNotFoundException(String message, Throwable cause) {
        super(message, cause);
    }
}