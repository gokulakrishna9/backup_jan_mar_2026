package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for MarketTrendIndustry search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class MarketTrendIndustryFilterDTO {
    
    // Filter type: EQUALS
    private Long industryId;
    
    // Filter type: EQUALS
    private Long trendId;
    
    // Filter type: LIKE
    private String industryName;
    
    // Filter type: LIKE
    private String description;
    
    // Filter type: LIKE
    private String marketSize;
    
    // Filter type: LIKE
    private String emergingTechnologies;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}