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
 * Output DTO for InstitutionDepartment responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class InstitutionDepartmentOutputDTO {
    
    private Long departmentId;
    
    private Long institutionId;
    
    private String departmentName;
    
    private String description;
    
    private Long headOfDepartmentUserId;
    
    private String contactEmail;
    
    private String contactPhone;
    
    private Byte isActive;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
    // Related entities can be included here
}