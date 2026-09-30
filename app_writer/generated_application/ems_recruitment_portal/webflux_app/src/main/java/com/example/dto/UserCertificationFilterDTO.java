package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for UserCertification search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserCertificationFilterDTO {
    
    // Filter type: EQUALS
    private Long certificationId;
    
    // Filter type: EQUALS
    private Long userId;
    
    // Filter type: LIKE
    private String certificationName;
    
    // Filter type: LIKE
    private String issuingOrganization;
    
    // Filter type: EQUALS
    private Long institutionId;
    
    // Filter type: EQUALS
    private LocalDate issueDate;
    
    // Filter type: EQUALS
    private LocalDate expiryDate;
    
    // Filter type: LIKE
    private String credentialId;
    
    // Filter type: LIKE
    private String credentialUrl;
    
    // Filter type: EQUALS
    private Long certificateDocumentId;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}