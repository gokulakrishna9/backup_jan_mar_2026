package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for UserWorkExperience search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserWorkExperienceFilterDTO {
    
    // Filter type: EQUALS
    private Long experienceId;
    
    // Filter type: EQUALS
    private Long userId;
    
    // Filter type: EQUALS
    private Long institutionId;
    
    // Filter type: LIKE
    private String jobTitle;
    
    // Filter type: LIKE
    private String companyName;
    
    // Filter type: LIKE
    private String employmentType;
    
    // Filter type: LIKE
    private String location;
    
    // Filter type: EQUALS
    private LocalDate startDate;
    
    // Filter type: EQUALS
    private LocalDate endDate;
    
    // Filter type: LIKE
    private String responsibilities;
    
    // Filter type: LIKE
    private String achievements;
    
    // Filter type: LIKE
    private String skillsUsed;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}