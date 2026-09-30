package com.jobportal.exception;

/**
 * Exception thrown when attempting to create a duplicate entity.
 */
public class DuplicateEntityException extends RuntimeException {
    
    public DuplicateEntityException(String message) {
        super(message);
    }
    
    public DuplicateEntityException(String entityType, String field, Object value) {
        super(String.format("%s with %s '%s' already exists", entityType, field, value));
    }
    
    public DuplicateEntityException(String message, Throwable cause) {
        super(message, cause);
    }
}