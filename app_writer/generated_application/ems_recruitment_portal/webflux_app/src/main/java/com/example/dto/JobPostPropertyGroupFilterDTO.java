package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for JobPostPropertyGroup search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class JobPostPropertyGroupFilterDTO {
    
    // Filter type: EQUALS
    private Long groupId;
    
    // Filter type: LIKE
    private String groupName;
    
    // Filter type: LIKE
    private String groupDescription;
    
    // Filter type: EQUALS
    private Long jobPostId;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}