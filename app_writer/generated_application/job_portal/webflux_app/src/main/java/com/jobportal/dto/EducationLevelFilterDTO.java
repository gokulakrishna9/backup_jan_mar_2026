package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Filter DTO for EducationLevel search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class EducationLevelFilterDTO {
    
    // Filter type: EQUALS
    private String name;
    
    // Filter type: EQUALS
    private String description;
    
    // Filter type: EQUALS
    private Integer sortorder;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}