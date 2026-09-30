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
 * Input DTO for CoursePrerequisite creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CoursePrerequisiteInputDTO {
    
    @NotNull(message = "Courseid is required")
    private Long courseId;
    
    private Long prerequisiteCourseId;
    
    private String prerequisiteType;
    
    private String prerequisiteDescription;
    
    private Byte isMandatory;
    
}