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
 * Input DTO for UserCourseProgress creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserCourseProgressInputDTO {
    
    @NotNull(message = "Userid is required")
    private Long userId;
    
    @NotNull(message = "Courseid is required")
    private Long courseId;
    
    private Long lessonId;
    
    @Min(value = 0, message = "Completionpercentage must be positive")
    private BigDecimal completionPercentage;
    
    private LocalDateTime lastAccessedAt;
    
    private Integer timeSpentMinutes;
    
    private String status;
    
}