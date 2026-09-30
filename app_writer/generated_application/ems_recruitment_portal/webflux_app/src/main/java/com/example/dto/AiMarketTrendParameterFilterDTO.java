package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for AiMarketTrendParameter search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AiMarketTrendParameterFilterDTO {
    
    // Filter type: EQUALS
    private Long parameterId;
    
    // Filter type: LIKE
    private String parameterName;
    
    // Filter type: LIKE
    private String parameterValue;
    
    // Filter type: EQUALS
    private Long groupId;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}