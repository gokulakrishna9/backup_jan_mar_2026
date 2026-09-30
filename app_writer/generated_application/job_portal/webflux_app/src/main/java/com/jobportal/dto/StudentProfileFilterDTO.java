package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Filter DTO for StudentProfile search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class StudentProfileFilterDTO {
    
    // Filter type: EQUALS
    private String resumeurl;
    
    // Filter type: EQUALS
    private String skills;
    
    // Filter type: EQUALS
    private String educationlevel;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}