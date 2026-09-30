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
 * Input DTO for MarketTrendInstitutionLink creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class MarketTrendInstitutionLinkInputDTO {
    
    @NotNull(message = "Trendid is required")
    private Long trendId;
    
    @NotNull(message = "Institutionid is required")
    private Long institutionId;
    
    private BigDecimal relevanceScore;
    
    private String specializationAreas;
    
    private String partnershipOpportunities;
    
    private Byte aiGenerated;
    
}