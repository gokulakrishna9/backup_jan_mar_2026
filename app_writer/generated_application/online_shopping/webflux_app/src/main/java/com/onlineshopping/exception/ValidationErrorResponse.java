package com.onlineshopping.exception;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import com.fasterxml.jackson.annotation.JsonInclude;
import io.swagger.v3.oas.annotations.media.Schema;
import java.time.LocalDateTime;
import java.util.Map;

/**
 * Validation error response structure with field-specific errors.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
@Schema(description = "Validation error response with field-level details")
public class ValidationErrorResponse {
    
    @Schema(description = "Timestamp when the error occurred", example = "2026-03-10T14:30:00")
    private LocalDateTime timestamp;
    
    @Schema(description = "HTTP status code", example = "400")
    private Integer status;
    
    @Schema(description = "HTTP status reason phrase", example = "Bad Request")
    private String error;
    
    @Schema(description = "Error message", example = "Validation failed for the request")
    private String message;
    
    @Schema(description = "Request path", example = "/api/entities")
    private String path;
    
    @Schema(description = "Application-specific error code", example = "VALIDATION_ERROR")
    private String errorCode;
    
    @Schema(description = "Field-specific validation errors")
    private Map<String, String> fieldErrors;
}