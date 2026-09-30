package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import jakarta.validation.constraints.*;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Input DTO for UserCertification creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserCertificationInputDTO {
    
    @NotNull(message = "Userid is required")
    private Long userId;
    
    @NotNull(message = "Certificationname is required")
    @Size(max = 255, message = "Certificationname cannot exceed 255 characters")
    private String certificationName;
    
    @NotNull(message = "Issuingorganization is required")
    @Size(max = 255, message = "Issuingorganization cannot exceed 255 characters")
    private String issuingOrganization;
    
    private Long institutionId;
    
    @NotNull(message = "Issuedate is required")
    private LocalDate issueDate;
    
    private LocalDate expiryDate;
    
    @Size(max = 255, message = "Credentialid cannot exceed 255 characters")
    private String credentialId;
    
    @Size(max = 500, message = "Credentialurl cannot exceed 500 characters")
    private String credentialUrl;
    
    private Long certificateDocumentId;
    
    private Byte isVerified;
    
}