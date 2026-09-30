package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for InstitutionDepartment search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class InstitutionDepartmentFilterDTO {
    
    // Filter type: EQUALS
    private Long departmentId;
    
    // Filter type: EQUALS
    private Long institutionId;
    
    // Filter type: LIKE
    private String departmentName;
    
    // Filter type: LIKE
    private String description;
    
    // Filter type: EQUALS
    private Long headOfDepartmentUserId;
    
    // Filter type: LIKE
    private String contactEmail;
    
    // Filter type: LIKE
    private String contactPhone;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}