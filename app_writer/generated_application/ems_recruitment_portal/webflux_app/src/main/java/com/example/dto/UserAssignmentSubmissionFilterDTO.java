package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for UserAssignmentSubmission search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserAssignmentSubmissionFilterDTO {
    
    // Filter type: EQUALS
    private Long submissionId;
    
    // Filter type: EQUALS
    private Long assignmentId;
    
    // Filter type: EQUALS
    private Long userId;
    
    // Filter type: LIKE
    private String submissionContent;
    
    // Filter type: EQUALS
    private Long submissionFileId;
    
    // Filter type: EQUALS
    private LocalDateTime submittedAt;
    
    // Filter type: EQUALS
    private Integer score;
    
    // Filter type: LIKE
    private String feedback;
    
    // Filter type: EQUALS
    private Long gradedByUserId;
    
    // Filter type: EQUALS
    private LocalDateTime gradedAt;
    
    // Filter type: LIKE
    private String status;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}