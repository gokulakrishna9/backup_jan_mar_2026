package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Output DTO for UserWorkExperience responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserWorkExperienceOutputDTO {
    
    private Long userWorkExperienceId;
    
    private String companyname;
    
    private String jobtitle;
    
    private String industry;
    
    private String location;
    
    private LocalDate startdate;
    
    private LocalDate enddate;
    
    private Boolean iscurrent;
    
    private String description;
    
    private LocalDateTime createdAt;
    
    private LocalDateTime updatedAt;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
}