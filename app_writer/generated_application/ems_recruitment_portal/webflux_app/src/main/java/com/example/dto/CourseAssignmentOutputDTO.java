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
 * Output DTO for CourseAssignment responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class CourseAssignmentOutputDTO {
    
    private Long assignmentId;
    
    private Long courseId;
    
    private Long moduleId;
    
    private String title;
    
    private String description;
    
    private String assignmentType;
    
    private Integer maxScore;
    
    private Integer passingScore;
    
    // Format: yyyy-MM-dd'T'HH:mm:ss
    private LocalDateTime dueDate;
    
    private Integer durationMinutes;
    
    private Byte isMandatory;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
    // Related entities can be included here
}