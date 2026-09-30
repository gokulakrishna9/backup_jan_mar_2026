package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for JobApplication search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class JobApplicationFilterDTO {
    
    // Filter type: EQUALS
    private Long applicationId;
    
    // Filter type: EQUALS
    private Long jobPostId;
    
    // Filter type: EQUALS
    private Long userId;
    
    // Filter type: LIKE
    private String coverLetter;
    
    // Filter type: EQUALS
    private Long resumeDocumentId;
    
    // Filter type: LIKE
    private String applicationStatus;
    
    // Filter type: EQUALS
    private LocalDateTime appliedAt;
    
    // Filter type: EQUALS
    private LocalDateTime statusUpdatedAt;
    
    // Filter type: EQUALS
    private Long statusUpdatedByUserId;
    
    // Filter type: LIKE
    private String notes;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}