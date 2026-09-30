package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for UserRecommendation search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserRecommendationFilterDTO {
    
    // Filter type: EQUALS
    private Long recommendationId;
    
    // Filter type: EQUALS
    private Long userId;
    
    // Filter type: EQUALS
    private Long recommendedByUserId;
    
    // Filter type: LIKE
    private String recommendationText;
    
    // Filter type: LIKE
    private String relationship;
    
    // Filter type: LIKE
    private String positionAtTime;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}