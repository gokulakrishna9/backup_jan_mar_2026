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
 * Input DTO for CourseJobPostLink creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CourseJobPostLinkInputDTO {
    
    @NotNull(message = "Courseid is required")
    private Long courseId;
    
    @NotNull(message = "Jobpostid is required")
    private Long jobPostId;
    
    private BigDecimal relevanceScore;
    
    private String matchingSkills;
    
    private Byte aiGenerated;
    
}