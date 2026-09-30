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
 * Input DTO for MarketTrendLocation creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class MarketTrendLocationInputDTO {
    
    @NotNull(message = "Trendid is required")
    private Long trendId;
    
    @NotNull(message = "Country is required")
    @Size(max = 100, message = "Country cannot exceed 100 characters")
    private String country;
    
    @Size(max = 255, message = "Region cannot exceed 255 characters")
    private String region;
    
    @Size(max = 100, message = "City cannot exceed 100 characters")
    private String city;
    
    private String jobMarketHealth;
    
    private BigDecimal unemploymentRate;
    
    @Size(max = 100, message = "Averagesalary cannot exceed 100 characters")
    private String averageSalary;
    
    private BigDecimal costOfLivingIndex;
    
    private String topIndustries;
    
}