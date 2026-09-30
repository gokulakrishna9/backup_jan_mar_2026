package com.example.exception;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import com.fasterxml.jackson.annotation.JsonInclude;
import io.swagger.v3.oas.annotations.media.Schema;
import java.time.LocalDateTime;

/**
 * Standard error response structure.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
@Schema(description = "Standard error response")
public class ErrorResponse {
    
    @Schema(description = "Timestamp when the error occurred", example = "2026-03-10T14:30:00")
    private LocalDateTime timestamp;
    
    @Schema(description = "HTTP status code", example = "400")
    private Integer status;
    
    @Schema(description = "HTTP status reason phrase", example = "Bad Request")
    private String error;
    
    @Schema(description = "Error message", example = "Invalid request parameters")
    private String message;
    
    @Schema(description = "Request path", example = "/api/entities/123")
    private String path;
    
    @Schema(description = "Application-specific error code", example = "ENTITY_NOT_FOUND")
    private String errorCode;
}