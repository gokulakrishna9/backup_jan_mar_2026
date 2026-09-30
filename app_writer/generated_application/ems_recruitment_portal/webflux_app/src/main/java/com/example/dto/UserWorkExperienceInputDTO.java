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
 * Input DTO for UserWorkExperience creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserWorkExperienceInputDTO {
    
    @NotNull(message = "Userid is required")
    private Long userId;
    
    private Long institutionId;
    
    @NotNull(message = "Jobtitle is required")
    @Size(max = 255, message = "Jobtitle cannot exceed 255 characters")
    private String jobTitle;
    
    @NotNull(message = "Companyname is required")
    @Size(max = 255, message = "Companyname cannot exceed 255 characters")
    private String companyName;
    
    private String employmentType;
    
    @Size(max = 255, message = "Location cannot exceed 255 characters")
    private String location;
    
    @NotNull(message = "Startdate is required")
    private LocalDate startDate;
    
    private LocalDate endDate;
    
    private Byte isCurrent;
    
    private String responsibilities;
    
    private String achievements;
    
    private String skillsUsed;
    
}