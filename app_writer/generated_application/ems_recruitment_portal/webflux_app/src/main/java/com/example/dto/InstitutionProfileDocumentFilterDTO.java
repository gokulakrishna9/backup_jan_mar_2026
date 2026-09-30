package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for InstitutionProfileDocument search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class InstitutionProfileDocumentFilterDTO {
    
    // Filter type: EQUALS
    private Long documentId;
    
    // Filter type: EQUALS
    private Long institutionId;
    
    // Filter type: LIKE
    private String title;
    
    // Filter type: LIKE
    private String document;
    
    // Filter type: LIKE
    private String documentType;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}