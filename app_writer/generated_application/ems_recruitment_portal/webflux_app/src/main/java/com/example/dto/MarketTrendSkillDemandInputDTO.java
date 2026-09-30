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
 * Input DTO for MarketTrendSkillDemand creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class MarketTrendSkillDemandInputDTO {
    
    @NotNull(message = "Trendid is required")
    private Long trendId;
    
    @NotNull(message = "Skillname is required")
    @Size(max = 255, message = "Skillname cannot exceed 255 characters")
    private String skillName;
    
    private String demandLevel;
    
    private BigDecimal growthRate;
    
    @Size(max = 100, message = "Averagesalaryrange cannot exceed 100 characters")
    private String averageSalaryRange;
    
    private Integer jobOpeningsCount;
    
    @Size(max = 255, message = "Region cannot exceed 255 characters")
    private String region;
    
    @Size(max = 255, message = "Industry cannot exceed 255 characters")
    private String industry;
    
}