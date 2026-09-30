package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for CoursePrerequisite search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CoursePrerequisiteFilterDTO {
    
    // Filter type: EQUALS
    private Long prerequisiteId;
    
    // Filter type: EQUALS
    private Long courseId;
    
    // Filter type: EQUALS
    private Long prerequisiteCourseId;
    
    // Filter type: LIKE
    private String prerequisiteType;
    
    // Filter type: LIKE
    private String prerequisiteDescription;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}