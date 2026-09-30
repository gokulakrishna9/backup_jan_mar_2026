package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Filter DTO for CourseCodeLab search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CourseCodeLabFilterDTO {
    
    // Filter type: EQUALS
    private String title;
    
    // Filter type: EQUALS
    private String description;
    
    // Filter type: EQUALS
    private String language;
    
    // Filter type: EQUALS
    private String startercode;
    
    // Filter type: EQUALS
    private String solutioncode;
    
    // Filter type: EQUALS
    private String instructions;
    
    // Filter type: EQUALS
    private Integer sortorder;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}