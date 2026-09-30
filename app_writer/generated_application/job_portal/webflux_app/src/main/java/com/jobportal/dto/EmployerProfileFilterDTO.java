package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Filter DTO for EmployerProfile search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class EmployerProfileFilterDTO {
    
    // Filter type: EQUALS
    private String companyname;
    
    // Filter type: EQUALS
    private String industry;
    
    // Filter type: EQUALS
    private String website;
    
    // Filter type: EQUALS
    private String logourl;
    
    // Filter type: EQUALS
    private String description;
    
    // Filter type: EQUALS
    private String contactemail;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}