package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Filter DTO for TrainingProgram search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TrainingProgramFilterDTO {
    
    // Filter type: EQUALS
    private String title;
    
    // Filter type: EQUALS
    private String description;
    
    // Filter type: EQUALS
    private Integer durationdays;
    
    // Filter type: EQUALS
    private BigDecimal price;
    
    // Filter type: EQUALS
    private Boolean isactive;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}