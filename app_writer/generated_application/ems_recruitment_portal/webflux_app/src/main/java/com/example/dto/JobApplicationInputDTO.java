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
 * Input DTO for JobApplication creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class JobApplicationInputDTO {
    
    @NotNull(message = "Jobpostid is required")
    private Long jobPostId;
    
    @NotNull(message = "Userid is required")
    private Long userId;
    
    private String coverLetter;
    
    private Long resumeDocumentId;
    
    private String applicationStatus;
    
    private LocalDateTime appliedAt;
    
    private LocalDateTime statusUpdatedAt;
    
    private Long statusUpdatedByUserId;
    
    private String notes;
    
}