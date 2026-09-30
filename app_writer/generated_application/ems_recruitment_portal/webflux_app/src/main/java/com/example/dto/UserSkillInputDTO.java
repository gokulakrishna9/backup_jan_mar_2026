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
 * Input DTO for UserSkill creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserSkillInputDTO {
    
    @NotNull(message = "Userid is required")
    private Long userId;
    
    @NotNull(message = "Skillname is required")
    @Size(max = 255, message = "Skillname cannot exceed 255 characters")
    private String skillName;
    
    @Size(max = 100, message = "Skillcategory cannot exceed 100 characters")
    private String skillCategory;
    
    private String proficiencyLevel;
    
    private Integer yearsOfExperience;
    
    private Byte isVerified;
    
    private Long verifiedByInstitutionId;
    
    private Integer endorsementCount;
    
}