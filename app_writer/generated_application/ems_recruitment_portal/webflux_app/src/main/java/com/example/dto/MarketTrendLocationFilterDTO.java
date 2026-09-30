package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for MarketTrendLocation search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class MarketTrendLocationFilterDTO {
    
    // Filter type: EQUALS
    private Long locationId;
    
    // Filter type: EQUALS
    private Long trendId;
    
    // Filter type: LIKE
    private String country;
    
    // Filter type: LIKE
    private String region;
    
    // Filter type: LIKE
    private String city;
    
    // Filter type: LIKE
    private String jobMarketHealth;
    
    // Filter type: LIKE
    private String averageSalary;
    
    // Filter type: LIKE
    private String topIndustries;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}