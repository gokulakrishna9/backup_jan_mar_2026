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
 * Input DTO for InstitutionAccreditation creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class InstitutionAccreditationInputDTO {
    
    @NotNull(message = "Institutionid is required")
    private Long institutionId;
    
    @NotNull(message = "Accreditingbody is required")
    @Size(max = 255, message = "Accreditingbody cannot exceed 255 characters")
    private String accreditingBody;
    
    @Size(max = 255, message = "Accreditationtype cannot exceed 255 characters")
    private String accreditationType;
    
    @Size(max = 100, message = "Accreditationlevel cannot exceed 100 characters")
    private String accreditationLevel;
    
    @NotNull(message = "Issuedate is required")
    private LocalDate issueDate;
    
    private LocalDate expiryDate;
    
    private Long certificateDocumentId;
    
    private Byte isActive;
    
}