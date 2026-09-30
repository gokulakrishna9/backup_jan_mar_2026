package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Filter DTO for JobApplication search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class JobApplicationFilterDTO {
    
    // Filter type: EQUALS
    private String status;
    
    // Filter type: EQUALS
    private String coverletter;
    
    // Filter type: EQUALS
    private LocalDateTime appliedat;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}