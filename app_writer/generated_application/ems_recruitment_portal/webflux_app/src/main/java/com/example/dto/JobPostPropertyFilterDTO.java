package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for JobPostProperty search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class JobPostPropertyFilterDTO {
    
    // Filter type: EQUALS
    private Long propertyId;
    
    // Filter type: LIKE
    private String propertyName;
    
    // Filter type: LIKE
    private String propertyValue;
    
    // Filter type: LIKE
    private String propertyType;
    
    // Filter type: LIKE
    private String propertyDescription;
    
    // Filter type: EQUALS
    private Long groupId;
    
    // Filter type: EQUALS
    private Long jobPostId;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}