package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import com.fasterxml.jackson.annotation.JsonInclude;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Output DTO for UserCertification responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class UserCertificationOutputDTO {
    
    private Long certificationId;
    
    private Long userId;
    
    private String certificationName;
    
    private String issuingOrganization;
    
    private Long institutionId;
    
    // Format: yyyy-MM-dd
    private LocalDate issueDate;
    
    // Format: yyyy-MM-dd
    private LocalDate expiryDate;
    
    private String credentialId;
    
    private String credentialUrl;
    
    private Long certificateDocumentId;
    
    private Byte isVerified;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
    // Related entities can be included here
}