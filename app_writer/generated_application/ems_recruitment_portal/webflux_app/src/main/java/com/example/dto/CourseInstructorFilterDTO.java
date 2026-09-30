package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for CourseInstructor search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CourseInstructorFilterDTO {
    
    // Filter type: EQUALS
    private Long instructorLinkId;
    
    // Filter type: EQUALS
    private Long courseId;
    
    // Filter type: EQUALS
    private Long userId;
    
    // Filter type: LIKE
    private String role;
    
    // Filter type: LIKE
    private String bio;
    
    // Filter type: LIKE
    private String specialization;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}