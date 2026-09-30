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
 * Input DTO for InstitutionPropertyGroup creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class InstitutionPropertyGroupInputDTO {
    
    @NotNull(message = "Groupname is required")
    @Size(max = 150, message = "Groupname cannot exceed 150 characters")
    private String groupName;
    
    private String groupDescription;
    
    @NotNull(message = "Institutionid is required")
    private Long institutionId;
    
    private Byte isActive;
    
}