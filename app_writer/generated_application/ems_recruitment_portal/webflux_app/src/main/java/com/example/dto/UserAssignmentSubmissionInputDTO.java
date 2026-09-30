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
 * Input DTO for UserAssignmentSubmission creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserAssignmentSubmissionInputDTO {
    
    @NotNull(message = "Assignmentid is required")
    private Long assignmentId;
    
    @NotNull(message = "Userid is required")
    private Long userId;
    
    private String submissionContent;
    
    private Long submissionFileId;
    
    private LocalDateTime submittedAt;
    
    private Integer score;
    
    private String feedback;
    
    private Long gradedByUserId;
    
    private LocalDateTime gradedAt;
    
    private String status;
    
}