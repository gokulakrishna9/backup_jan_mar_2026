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
 * Input DTO for CourseInstructor creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CourseInstructorInputDTO {
    
    @NotNull(message = "Courseid is required")
    private Long courseId;
    
    @NotNull(message = "Userid is required")
    private Long userId;
    
    private String role;
    
    private String bio;
    
    @Size(max = 255, message = "Specialization cannot exceed 255 characters")
    private String specialization;
    
}