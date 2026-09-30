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
 * Output DTO for MarketTrendJobPostLink responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class MarketTrendJobPostLinkOutputDTO {
    
    private Long linkId;
    
    private Long trendId;
    
    private Long jobPostId;
    
    private BigDecimal relevanceScore;
    
    private String growthPotential;
    
    private String salaryTrend;
    
    private Byte aiGenerated;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
    // Related entities can be included here
}