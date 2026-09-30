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
 * Output DTO for InstitutionAccreditation responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class InstitutionAccreditationOutputDTO {
    
    private Long accreditationId;
    
    private Long institutionId;
    
    private String accreditingBody;
    
    private String accreditationType;
    
    private String accreditationLevel;
    
    // Format: yyyy-MM-dd
    private LocalDate issueDate;
    
    // Format: yyyy-MM-dd
    private LocalDate expiryDate;
    
    private Long certificateDocumentId;
    
    private Byte isActive;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
    // Related entities can be included here
}