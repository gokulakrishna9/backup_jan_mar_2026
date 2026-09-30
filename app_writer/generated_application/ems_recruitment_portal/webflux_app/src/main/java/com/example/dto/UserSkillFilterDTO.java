package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for UserSkill search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserSkillFilterDTO {
    
    // Filter type: EQUALS
    private Long skillId;
    
    // Filter type: EQUALS
    private Long userId;
    
    // Filter type: LIKE
    private String skillName;
    
    // Filter type: LIKE
    private String skillCategory;
    
    // Filter type: LIKE
    private String proficiencyLevel;
    
    // Filter type: EQUALS
    private Integer yearsOfExperience;
    
    // Filter type: EQUALS
    private Long verifiedByInstitutionId;
    
    // Filter type: EQUALS
    private Integer endorsementCount;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}