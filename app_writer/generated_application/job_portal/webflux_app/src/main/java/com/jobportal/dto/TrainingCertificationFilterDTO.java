package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Filter DTO for TrainingCertification search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TrainingCertificationFilterDTO {
    
    // Filter type: EQUALS
    private String certificatenumber;
    
    // Filter type: EQUALS
    private String title;
    
    // Filter type: EQUALS
    private LocalDateTime issuedat;
    
    // Filter type: EQUALS
    private LocalDateTime expiresat;
    
    // Filter type: EQUALS
    private String certificateurl;
    
    // Filter type: EQUALS
    private String status;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}