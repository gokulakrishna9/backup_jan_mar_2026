package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Filter DTO for UserWorkExperience search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserWorkExperienceFilterDTO {
    
    // Filter type: EQUALS
    private String companyname;
    
    // Filter type: EQUALS
    private String jobtitle;
    
    // Filter type: EQUALS
    private String industry;
    
    // Filter type: EQUALS
    private String location;
    
    // Filter type: EQUALS
    private LocalDate startdate;
    
    // Filter type: EQUALS
    private LocalDate enddate;
    
    // Filter type: EQUALS
    private Boolean iscurrent;
    
    // Filter type: EQUALS
    private String description;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}