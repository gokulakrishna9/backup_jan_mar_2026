package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for UserEducation search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserEducationFilterDTO {
    
    // Filter type: EQUALS
    private Long educationId;
    
    // Filter type: EQUALS
    private Long userId;
    
    // Filter type: EQUALS
    private Long institutionId;
    
    // Filter type: LIKE
    private String degreeType;
    
    // Filter type: LIKE
    private String fieldOfStudy;
    
    // Filter type: LIKE
    private String specialization;
    
    // Filter type: EQUALS
    private LocalDate startDate;
    
    // Filter type: EQUALS
    private LocalDate endDate;
    
    // Filter type: LIKE
    private String gradeGpa;
    
    // Filter type: EQUALS
    private Long certificateDocumentId;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}