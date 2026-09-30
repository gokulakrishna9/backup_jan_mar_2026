package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for Course search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CourseFilterDTO {
    
    // Filter type: EQUALS
    private Long courseId;
    
    // Filter type: LIKE
    private String courseName;
    
    // Filter type: LIKE
    private String description;
    
    // Filter type: LIKE
    private String outcomes;
    
    // Filter type: EQUALS
    private Integer courseTypeId;
    
    // Filter type: EQUALS
    private Integer durationWeeks;
    
    // Filter type: EQUALS
    private Long institutionId;
    
    // Filter type: EQUALS
    private Boolean isPublic;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}