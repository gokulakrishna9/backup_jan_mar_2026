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
 * Input DTO for JobPostRequirement creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class JobPostRequirementInputDTO {
    
    @NotNull(message = "Jobpostid is required")
    private Long jobPostId;
    
    @NotNull(message = "Requirementtype is required")
    private String requirementType;
    
    @NotNull(message = "Requirementdescription is required")
    private String requirementDescription;
    
    private Byte isMandatory;
    
    private Integer minimumYears;
    
    @Size(max = 100, message = "Proficiencylevel cannot exceed 100 characters")
    private String proficiencyLevel;
    
}