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
 * Input DTO for JobPosting creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class JobPostingInputDTO {
    
    private String title;
    
    private String description;
    
    private String location;
    
    private BigDecimal salarymin;
    
    private BigDecimal salarymax;
    
    private String jobtype;
    
    private Boolean isactive;
    
}