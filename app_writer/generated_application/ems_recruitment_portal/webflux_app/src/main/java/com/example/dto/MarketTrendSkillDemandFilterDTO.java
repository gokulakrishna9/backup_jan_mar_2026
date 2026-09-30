package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for MarketTrendSkillDemand search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class MarketTrendSkillDemandFilterDTO {
    
    // Filter type: EQUALS
    private Long demandId;
    
    // Filter type: EQUALS
    private Long trendId;
    
    // Filter type: LIKE
    private String skillName;
    
    // Filter type: LIKE
    private String demandLevel;
    
    // Filter type: LIKE
    private String averageSalaryRange;
    
    // Filter type: EQUALS
    private Integer jobOpeningsCount;
    
    // Filter type: LIKE
    private String region;
    
    // Filter type: LIKE
    private String industry;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}