package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import jakarta.validation.constraints.*;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Input DTO for CourseLesson creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CourseLessonInputDTO {
    
    @NotNull(message = "Moduleid is required")
    private Long moduleId;
    
    @NotNull(message = "Courseid is required")
    private Long courseId;
    
    @NotNull(message = "Lessontitle is required")
    @Size(max = 255, message = "Lessontitle cannot exceed 255 characters")
    private String lessonTitle;
    
    @NotNull(message = "Lessonnumber is required")
    private Integer lessonNumber;
    
    private String contentType;
    
    @Size(max = 500, message = "Contenturl cannot exceed 500 characters")
    private String contentUrl;
    
    private Integer durationMinutes;
    
    private Byte isPreviewAvailable;
    
    @NotNull(message = "Ordersequence is required")
    private Integer orderSequence;
    
}