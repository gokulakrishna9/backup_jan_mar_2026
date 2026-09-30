package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for UserCourseProgress search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserCourseProgressFilterDTO {
    
    // Filter type: EQUALS
    private Long progressId;
    
    // Filter type: EQUALS
    private Long userId;
    
    // Filter type: EQUALS
    private Long courseId;
    
    // Filter type: EQUALS
    private Long lessonId;
    
    // Filter type: EQUALS
    private LocalDateTime lastAccessedAt;
    
    // Filter type: EQUALS
    private Integer timeSpentMinutes;
    
    // Filter type: LIKE
    private String status;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}