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
 * Input DTO for UserEducation creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserEducationInputDTO {
    
    private String institutionname;
    
    private String degree;
    
    private String fieldofstudy;
    
    private LocalDate startdate;
    
    private LocalDate enddate;
    
    private String grade;
    
    private String description;
    
}