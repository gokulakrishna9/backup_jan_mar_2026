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
 * Input DTO for CourseProperty creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CoursePropertyInputDTO {
    
    @NotNull(message = "Propertyname is required")
    @Size(max = 150, message = "Propertyname cannot exceed 150 characters")
    private String propertyName;
    
    private String propertyValue;
    
    @NotNull(message = "Propertytype is required")
    @Size(max = 50, message = "Propertytype cannot exceed 50 characters")
    private String propertyType;
    
    private String propertyDescription;
    
    private Long groupId;
    
    @NotNull(message = "Courseid is required")
    private Long courseId;
    
}