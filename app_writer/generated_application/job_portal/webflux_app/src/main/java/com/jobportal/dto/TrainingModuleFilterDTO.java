package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Filter DTO for TrainingModule search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TrainingModuleFilterDTO {
    
    // Filter type: EQUALS
    private String title;
    
    // Filter type: EQUALS
    private String description;
    
    // Filter type: EQUALS
    private Integer moduleorder;
    
    // Filter type: EQUALS
    private Integer durationminutes;
    
    // Filter type: EQUALS
    private String contenturl;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}