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
 * Input DTO for JobPostBenefit creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class JobPostBenefitInputDTO {
    
    @NotNull(message = "Jobpostid is required")
    private Long jobPostId;
    
    @NotNull(message = "Benefittype is required")
    @Size(max = 100, message = "Benefittype cannot exceed 100 characters")
    private String benefitType;
    
    private String benefitDescription;
    
}