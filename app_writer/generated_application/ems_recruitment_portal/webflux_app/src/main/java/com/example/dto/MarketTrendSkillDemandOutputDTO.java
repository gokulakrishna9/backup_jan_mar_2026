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
 * Output DTO for MarketTrendSkillDemand responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class MarketTrendSkillDemandOutputDTO {
    
    private Long demandId;
    
    private Long trendId;
    
    private String skillName;
    
    private String demandLevel;
    
    private BigDecimal growthRate;
    
    private String averageSalaryRange;
    
    private Integer jobOpeningsCount;
    
    private String region;
    
    private String industry;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
    // Related entities can be included here
}