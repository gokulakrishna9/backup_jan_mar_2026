package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for AiUserProfileEvaluationParameterGroup search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AiUserProfileEvaluationParameterGroupFilterDTO {
    
    // Filter type: EQUALS
    private Long groupId;
    
    // Filter type: LIKE
    private String groupName;
    
    // Filter type: LIKE
    private String description;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}