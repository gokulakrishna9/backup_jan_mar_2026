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
 * Input DTO for Institution creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class InstitutionInputDTO {
    
    @NotNull(message = "Name is required")
    @Size(max = 255, message = "Name cannot exceed 255 characters")
    private String name;
    
    private String description;
    
    @Size(max = 255, message = "Moto cannot exceed 255 characters")
    private String moto;
    
    private Integer institutionTypeId;
    
    @Size(max = 255, message = "Website cannot exceed 255 characters")
    private String website;
    
    @Email(message = "Please provide a valid email address")
    @Size(max = 255, message = "Contactemail cannot exceed 255 characters")
    private String contactEmail;
    
    @Size(max = 30, message = "Contactphone cannot exceed 30 characters")
    private String contactPhone;
    
    private Byte isActive;
    
    private Byte isEntity;
    
    @NotNull(message = "Ispublic is required")
    private Boolean isPublic;
    
}