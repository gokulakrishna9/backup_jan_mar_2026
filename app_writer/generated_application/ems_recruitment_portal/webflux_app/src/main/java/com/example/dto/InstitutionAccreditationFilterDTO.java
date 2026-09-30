package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for InstitutionAccreditation search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class InstitutionAccreditationFilterDTO {
    
    // Filter type: EQUALS
    private Long accreditationId;
    
    // Filter type: EQUALS
    private Long institutionId;
    
    // Filter type: LIKE
    private String accreditingBody;
    
    // Filter type: LIKE
    private String accreditationType;
    
    // Filter type: LIKE
    private String accreditationLevel;
    
    // Filter type: EQUALS
    private LocalDate issueDate;
    
    // Filter type: EQUALS
    private LocalDate expiryDate;
    
    // Filter type: EQUALS
    private Long certificateDocumentId;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}