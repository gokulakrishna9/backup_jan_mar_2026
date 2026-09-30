package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for InstitutionLocation search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class InstitutionLocationFilterDTO {
    
    // Filter type: EQUALS
    private Long locationId;
    
    // Filter type: EQUALS
    private Long institutionId;
    
    // Filter type: LIKE
    private String locationType;
    
    // Filter type: LIKE
    private String addressLine1;
    
    // Filter type: LIKE
    private String addressLine2;
    
    // Filter type: LIKE
    private String city;
    
    // Filter type: LIKE
    private String stateProvince;
    
    // Filter type: LIKE
    private String country;
    
    // Filter type: LIKE
    private String postalCode;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}