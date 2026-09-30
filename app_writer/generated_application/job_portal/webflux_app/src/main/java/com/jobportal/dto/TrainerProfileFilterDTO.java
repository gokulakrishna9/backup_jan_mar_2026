package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Filter DTO for TrainerProfile search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TrainerProfileFilterDTO {
    
    // Filter type: EQUALS
    private String specialization;
    
    // Filter type: EQUALS
    private String certifications;
    
    // Filter type: EQUALS
    private BigDecimal hourlyrate;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}