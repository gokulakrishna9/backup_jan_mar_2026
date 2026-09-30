package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Filter DTO for Company search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CompanyFilterDTO {
    
    // Filter type: EQUALS
    private String name;
    
    // Filter type: EQUALS
    private String industry;
    
    // Filter type: EQUALS
    private String website;
    
    // Filter type: EQUALS
    private String description;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}