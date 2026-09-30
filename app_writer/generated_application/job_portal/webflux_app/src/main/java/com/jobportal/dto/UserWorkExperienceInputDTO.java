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
 * Input DTO for UserWorkExperience creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserWorkExperienceInputDTO {
    
    private String companyname;
    
    private String jobtitle;
    
    private String industry;
    
    private String location;
    
    private LocalDate startdate;
    
    private LocalDate enddate;
    
    private Boolean iscurrent;
    
    private String description;
    
}