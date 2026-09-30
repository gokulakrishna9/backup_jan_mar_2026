package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import jakarta.validation.constraints.*;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Input DTO for MarketTrendJobPostLink creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class MarketTrendJobPostLinkInputDTO {
    
    @NotNull(message = "Trendid is required")
    private Long trendId;
    
    @NotNull(message = "Jobpostid is required")
    private Long jobPostId;
    
    private BigDecimal relevanceScore;
    
    private String growthPotential;
    
    @Size(max = 100, message = "Salarytrend cannot exceed 100 characters")
    private String salaryTrend;
    
    private Byte aiGenerated;
    
}