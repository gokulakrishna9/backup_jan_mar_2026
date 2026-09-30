package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import jakarta.validation.constraints.*;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Input DTO for CourseCodeLab creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CourseCodeLabInputDTO {
    
    private String title;
    
    private String description;
    
    private String language;
    
    private String startercode;
    
    private String solutioncode;
    
    private String instructions;
    
    private Integer sortorder;
    
}