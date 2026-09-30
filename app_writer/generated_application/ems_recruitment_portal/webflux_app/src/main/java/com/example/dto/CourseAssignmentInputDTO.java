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
 * Input DTO for CourseAssignment creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CourseAssignmentInputDTO {
    
    @NotNull(message = "Courseid is required")
    private Long courseId;
    
    private Long moduleId;
    
    @NotNull(message = "Title is required")
    @Size(max = 255, message = "Title cannot exceed 255 characters")
    private String title;
    
    private String description;
    
    private String assignmentType;
    
    @NotNull(message = "Maxscore is required")
    private Integer maxScore;
    
    @NotNull(message = "Passingscore is required")
    private Integer passingScore;
    
    private LocalDateTime dueDate;
    
    private Integer durationMinutes;
    
    private Byte isMandatory;
    
}