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
 * Output DTO for InstitutionLocation responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class InstitutionLocationOutputDTO {
    
    private Long locationId;
    
    private Long institutionId;
    
    private String locationType;
    
    private String addressLine1;
    
    private String addressLine2;
    
    private String city;
    
    private String stateProvince;
    
    private String country;
    
    private String postalCode;
    
    private BigDecimal latitude;
    
    private BigDecimal longitude;
    
    private Byte isPrimary;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
    // Related entities can be included here
}