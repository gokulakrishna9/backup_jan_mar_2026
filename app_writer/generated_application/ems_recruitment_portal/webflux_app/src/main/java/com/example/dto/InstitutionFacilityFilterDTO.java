package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for InstitutionFacility search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class InstitutionFacilityFilterDTO {
    
    // Filter type: EQUALS
    private Long facilityId;
    
    // Filter type: EQUALS
    private Long institutionId;
    
    // Filter type: LIKE
    private String facilityName;
    
    // Filter type: LIKE
    private String facilityType;
    
    // Filter type: LIKE
    private String description;
    
    // Filter type: EQUALS
    private Integer capacity;
    
    // Filter type: EQUALS
    private Long locationId;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}