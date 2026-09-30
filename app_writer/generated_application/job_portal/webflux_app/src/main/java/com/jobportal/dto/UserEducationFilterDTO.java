package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Filter DTO for UserEducation search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserEducationFilterDTO {
    
    // Filter type: EQUALS
    private String institutionname;
    
    // Filter type: EQUALS
    private String degree;
    
    // Filter type: EQUALS
    private String fieldofstudy;
    
    // Filter type: EQUALS
    private LocalDate startdate;
    
    // Filter type: EQUALS
    private LocalDate enddate;
    
    // Filter type: EQUALS
    private String grade;
    
    // Filter type: EQUALS
    private String description;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}