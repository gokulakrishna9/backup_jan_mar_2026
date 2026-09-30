package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for CourseModule search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CourseModuleFilterDTO {
    
    // Filter type: EQUALS
    private Long moduleId;
    
    // Filter type: EQUALS
    private Long courseId;
    
    // Filter type: LIKE
    private String moduleName;
    
    // Filter type: EQUALS
    private Integer moduleNumber;
    
    // Filter type: LIKE
    private String description;
    
    // Filter type: EQUALS
    private Integer durationHours;
    
    // Filter type: LIKE
    private String learningObjectives;
    
    // Filter type: EQUALS
    private Integer orderSequence;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}