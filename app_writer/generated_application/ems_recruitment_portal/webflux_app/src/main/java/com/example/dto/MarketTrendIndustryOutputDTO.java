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
 * Output DTO for MarketTrendIndustry responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class MarketTrendIndustryOutputDTO {
    
    private Long industryId;
    
    private Long trendId;
    
    private String industryName;
    
    private String description;
    
    private BigDecimal growthRate;
    
    private String marketSize;
    
    private String emergingTechnologies;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
    // Related entities can be included here
}