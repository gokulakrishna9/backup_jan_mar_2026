package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for AiMarketTrendProperty search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AiMarketTrendPropertyFilterDTO {
    
    // Filter type: EQUALS
    private Long trendId;
    
    // Filter type: LIKE
    private String trendName;
    
    // Filter type: LIKE
    private String trendDescription;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}