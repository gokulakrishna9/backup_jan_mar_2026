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
 * Input DTO for InstitutionLocation creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class InstitutionLocationInputDTO {
    
    @NotNull(message = "Institutionid is required")
    private Long institutionId;
    
    private String locationType;
    
    @NotNull(message = "Addressline1 is required")
    @Size(max = 255, message = "Addressline1 cannot exceed 255 characters")
    private String addressLine1;
    
    @Size(max = 255, message = "Addressline2 cannot exceed 255 characters")
    private String addressLine2;
    
    @NotNull(message = "City is required")
    @Size(max = 100, message = "City cannot exceed 100 characters")
    private String city;
    
    @Size(max = 100, message = "Stateprovince cannot exceed 100 characters")
    private String stateProvince;
    
    @NotNull(message = "Country is required")
    @Size(max = 100, message = "Country cannot exceed 100 characters")
    private String country;
    
    @Size(max = 20, message = "Postalcode cannot exceed 20 characters")
    private String postalCode;
    
    private BigDecimal latitude;
    
    private BigDecimal longitude;
    
    private Byte isPrimary;
    
}