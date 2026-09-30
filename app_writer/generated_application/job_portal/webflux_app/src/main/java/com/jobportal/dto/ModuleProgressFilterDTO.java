package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Filter DTO for ModuleProgress search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ModuleProgressFilterDTO {
    
    // Filter type: EQUALS
    private String status;
    
    // Filter type: EQUALS
    private LocalDateTime completedat;
    
    // Filter type: EQUALS
    private Integer progresspercent;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}