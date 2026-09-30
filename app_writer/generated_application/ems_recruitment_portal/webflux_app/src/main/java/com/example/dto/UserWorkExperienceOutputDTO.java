package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import com.fasterxml.jackson.annotation.JsonInclude;
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
@JsonInclude(JsonInclude.Include.NON_NULL)
public class UserWorkExperienceOutputDTO {
    
    private Long experienceId;
    
    private Long userId;
    
    private Long institutionId;
    
    private String jobTitle;
    
    private String companyName;
    
    private String employmentType;
    
    private String location;
    
    // Format: yyyy-MM-dd
    private LocalDate startDate;
    
    // Format: yyyy-MM-dd
    private LocalDate endDate;
    
    private Byte isCurrent;
    
    private String responsibilities;
    
    private String achievements;
    
    private String skillsUsed;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
    // Related entities can be included here
}