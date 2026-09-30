package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for AiUserProfileEvaluationParameter search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AiUserProfileEvaluationParameterFilterDTO {
    
    // Filter type: EQUALS
    private Long parameterId;
    
    // Filter type: LIKE
    private String parameterName;
    
    // Filter type: EQUALS
    private Long groupId;
    
    // Filter type: LIKE
    private String parameterValue;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}