package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for CourseAssignment search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CourseAssignmentFilterDTO {
    
    // Filter type: EQUALS
    private Long assignmentId;
    
    // Filter type: EQUALS
    private Long courseId;
    
    // Filter type: EQUALS
    private Long moduleId;
    
    // Filter type: LIKE
    private String title;
    
    // Filter type: LIKE
    private String description;
    
    // Filter type: LIKE
    private String assignmentType;
    
    // Filter type: EQUALS
    private Integer maxScore;
    
    // Filter type: EQUALS
    private Integer passingScore;
    
    // Filter type: EQUALS
    private LocalDateTime dueDate;
    
    // Filter type: EQUALS
    private Integer durationMinutes;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}