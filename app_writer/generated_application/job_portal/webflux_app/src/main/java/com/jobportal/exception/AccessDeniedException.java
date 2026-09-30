package com.jobportal.exception;

/**
 * Exception thrown when access to a resource is denied.
 */
public class AccessDeniedException extends RuntimeException {
    
    public AccessDeniedException(String message) {
        super(message);
    }
    
    public AccessDeniedException(String operation, String resource) {
        super(String.format("Access denied: %s permission required for %s", operation, resource));
    }
    
    public AccessDeniedException(String message, Throwable cause) {
        super(message, cause);
    }
}