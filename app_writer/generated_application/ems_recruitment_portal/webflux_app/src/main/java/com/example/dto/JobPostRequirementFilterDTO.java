package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for JobPostRequirement search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class JobPostRequirementFilterDTO {
    
    // Filter type: EQUALS
    private Long requirementId;
    
    // Filter type: EQUALS
    private Long jobPostId;
    
    // Filter type: LIKE
    private String requirementType;
    
    // Filter type: LIKE
    private String requirementDescription;
    
    // Filter type: EQUALS
    private Integer minimumYears;
    
    // Filter type: LIKE
    private String proficiencyLevel;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}