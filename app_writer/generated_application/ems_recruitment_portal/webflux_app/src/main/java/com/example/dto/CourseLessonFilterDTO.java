package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for CourseLesson search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CourseLessonFilterDTO {
    
    // Filter type: EQUALS
    private Long lessonId;
    
    // Filter type: EQUALS
    private Long moduleId;
    
    // Filter type: EQUALS
    private Long courseId;
    
    // Filter type: LIKE
    private String lessonTitle;
    
    // Filter type: EQUALS
    private Integer lessonNumber;
    
    // Filter type: LIKE
    private String contentType;
    
    // Filter type: LIKE
    private String contentUrl;
    
    // Filter type: EQUALS
    private Integer durationMinutes;
    
    // Filter type: EQUALS
    private Integer orderSequence;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}