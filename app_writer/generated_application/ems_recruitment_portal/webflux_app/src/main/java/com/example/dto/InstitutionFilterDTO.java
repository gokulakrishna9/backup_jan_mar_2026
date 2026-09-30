package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for Institution search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class InstitutionFilterDTO {
    
    // Filter type: EQUALS
    private Long institutionId;
    
    // Filter type: LIKE
    private String name;
    
    // Filter type: LIKE
    private String description;
    
    // Filter type: LIKE
    private String moto;
    
    // Filter type: EQUALS
    private Integer institutionTypeId;
    
    // Filter type: LIKE
    private String website;
    
    // Filter type: LIKE
    private String contactEmail;
    
    // Filter type: LIKE
    private String contactPhone;
    
    // Filter type: EQUALS
    private Boolean isPublic;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}