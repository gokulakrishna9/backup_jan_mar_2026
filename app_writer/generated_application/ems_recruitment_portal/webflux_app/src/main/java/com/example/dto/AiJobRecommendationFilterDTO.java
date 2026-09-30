package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for AiJobRecommendation search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AiJobRecommendationFilterDTO {
    
    // Filter type: EQUALS
    private Long preferenceId;
    
    // Filter type: EQUALS
    private Long jobPostId;
    
    // Filter type: EQUALS
    private Long profileId;
    
    // Filter type: LIKE
    private String recommendationSummary;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}