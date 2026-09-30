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
 * Input DTO for CourseModule creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CourseModuleInputDTO {
    
    @NotNull(message = "Courseid is required")
    private Long courseId;
    
    @NotNull(message = "Modulename is required")
    @Size(max = 255, message = "Modulename cannot exceed 255 characters")
    private String moduleName;
    
    @NotNull(message = "Modulenumber is required")
    private Integer moduleNumber;
    
    private String description;
    
    private Integer durationHours;
    
    private String learningObjectives;
    
    private Byte isMandatory;
    
    @NotNull(message = "Ordersequence is required")
    private Integer orderSequence;
    
}