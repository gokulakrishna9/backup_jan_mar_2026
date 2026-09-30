package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for AiCommunityPostEvaluation search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AiCommunityPostEvaluationFilterDTO {
    
    // Filter type: EQUALS
    private Long evaluationId;
    
    // Filter type: EQUALS
    private Long postId;
    
    // Filter type: LIKE
    private String evaluationSummary;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}