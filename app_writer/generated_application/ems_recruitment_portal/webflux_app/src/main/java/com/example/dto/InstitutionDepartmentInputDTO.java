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
 * Input DTO for InstitutionDepartment creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class InstitutionDepartmentInputDTO {
    
    @NotNull(message = "Institutionid is required")
    private Long institutionId;
    
    @NotNull(message = "Departmentname is required")
    @Size(max = 255, message = "Departmentname cannot exceed 255 characters")
    private String departmentName;
    
    private String description;
    
    private Long headOfDepartmentUserId;
    
    @Email(message = "Please provide a valid email address")
    @Size(max = 255, message = "Contactemail cannot exceed 255 characters")
    private String contactEmail;
    
    @Size(max = 30, message = "Contactphone cannot exceed 30 characters")
    private String contactPhone;
    
    private Byte isActive;
    
}