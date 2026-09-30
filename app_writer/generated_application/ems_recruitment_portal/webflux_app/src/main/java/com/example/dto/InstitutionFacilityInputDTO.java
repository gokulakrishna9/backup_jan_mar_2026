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
 * Input DTO for InstitutionFacility creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class InstitutionFacilityInputDTO {
    
    @NotNull(message = "Institutionid is required")
    private Long institutionId;
    
    @NotNull(message = "Facilityname is required")
    @Size(max = 255, message = "Facilityname cannot exceed 255 characters")
    private String facilityName;
    
    @Size(max = 100, message = "Facilitytype cannot exceed 100 characters")
    private String facilityType;
    
    private String description;
    
    private Integer capacity;
    
    private Long locationId;
    
    private Byte isAvailable;
    
}