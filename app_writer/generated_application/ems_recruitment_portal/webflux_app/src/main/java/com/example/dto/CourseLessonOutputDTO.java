package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import com.fasterxml.jackson.annotation.JsonInclude;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Output DTO for CourseLesson responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class CourseLessonOutputDTO {
    
    private Long lessonId;
    
    private Long moduleId;
    
    private Long courseId;
    
    private String lessonTitle;
    
    private Integer lessonNumber;
    
    private String contentType;
    
    private String contentUrl;
    
    private Integer durationMinutes;
    
    private Byte isPreviewAvailable;
    
    private Integer orderSequence;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
    // Related entities can be included here
}