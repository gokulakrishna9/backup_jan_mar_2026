package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for JobPost search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class JobPostFilterDTO {
    
    // Filter type: EQUALS
    private Long jobPostId;
    
    // Filter type: LIKE
    private String jobPostSubject;
    
    // Filter type: LIKE
    private String jobPostDescription;
    
    // Filter type: EQUALS
    private Long institutionId;
    
    // Filter type: LIKE
    private String location;
    
    // Filter type: LIKE
    private String salaryRange;
    
    // Filter type: EQUALS
    private LocalDateTime postedOn;
    
    // Filter type: EQUALS
    private LocalDateTime expiresOn;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}