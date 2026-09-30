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
 * Output DTO for UserAssignmentSubmission responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class UserAssignmentSubmissionOutputDTO {
    
    private Long submissionId;
    
    private Long assignmentId;
    
    private Long userId;
    
    private String submissionContent;
    
    private Long submissionFileId;
    
    // Format: yyyy-MM-dd'T'HH:mm:ss
    private LocalDateTime submittedAt;
    
    private Integer score;
    
    private String feedback;
    
    private Long gradedByUserId;
    
    // Format: yyyy-MM-dd'T'HH:mm:ss
    private LocalDateTime gradedAt;
    
    private String status;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
    // Related entities can be included here
}