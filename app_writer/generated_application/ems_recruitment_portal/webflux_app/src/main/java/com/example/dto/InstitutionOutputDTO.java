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
 * Output DTO for Institution responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class InstitutionOutputDTO {
    
    private Long institutionId;
    
    private String name;
    
    private String description;
    
    private String moto;
    
    private Integer institutionTypeId;
    
    private String website;
    
    private String contactEmail;
    
    private String contactPhone;
    
    private Byte isActive;
    
    private Byte isEntity;
    
    private Boolean isPublic;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
    // Related entities can be included here
}