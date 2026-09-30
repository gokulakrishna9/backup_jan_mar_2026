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
 * Input DTO for MarketTrendIndustry creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class MarketTrendIndustryInputDTO {
    
    @NotNull(message = "Trendid is required")
    private Long trendId;
    
    @NotNull(message = "Industryname is required")
    @Size(max = 255, message = "Industryname cannot exceed 255 characters")
    private String industryName;
    
    private String description;
    
    private BigDecimal growthRate;
    
    @Size(max = 100, message = "Marketsize cannot exceed 100 characters")
    private String marketSize;
    
    private String emergingTechnologies;
    
}