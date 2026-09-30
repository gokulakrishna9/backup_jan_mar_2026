package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for JobPostBenefit search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class JobPostBenefitFilterDTO {
    
    // Filter type: EQUALS
    private Long benefitId;
    
    // Filter type: EQUALS
    private Long jobPostId;
    
    // Filter type: LIKE
    private String benefitType;
    
    // Filter type: LIKE
    private String benefitDescription;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}