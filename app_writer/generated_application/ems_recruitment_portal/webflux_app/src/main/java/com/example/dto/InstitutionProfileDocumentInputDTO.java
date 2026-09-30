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
 * Input DTO for InstitutionProfileDocument creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class InstitutionProfileDocumentInputDTO {
    
    @NotNull(message = "Institutionid is required")
    private Long institutionId;
    
    @Size(max = 255, message = "Title cannot exceed 255 characters")
    private String title;
    
    @NotNull(message = "Document is required")
    private String document;
    
    @Size(max = 100, message = "Documenttype cannot exceed 100 characters")
    private String documentType;
    
}