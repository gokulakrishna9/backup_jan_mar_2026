package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import com.fasterxml.jackson.annotation.JsonInclude;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Output DTO for MarketTrendLocation responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class MarketTrendLocationOutputDTO {
    
    private Long locationId;
    
    private Long trendId;
    
    private String country;
    
    private String region;
    
    private String city;
    
    private String jobMarketHealth;
    
    private BigDecimal unemploymentRate;
    
    private String averageSalary;
    
    private BigDecimal costOfLivingIndex;
    
    private String topIndustries;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
    // Related entities can be included here
}