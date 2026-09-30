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
 * Output DTO for UserSkill responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class UserSkillOutputDTO {
    
    private Long skillId;
    
    private Long userId;
    
    private String skillName;
    
    private String skillCategory;
    
    private String proficiencyLevel;
    
    private Integer yearsOfExperience;
    
    private Byte isVerified;
    
    private Long verifiedByInstitutionId;
    
    private Integer endorsementCount;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
    // Related entities can be included here
}