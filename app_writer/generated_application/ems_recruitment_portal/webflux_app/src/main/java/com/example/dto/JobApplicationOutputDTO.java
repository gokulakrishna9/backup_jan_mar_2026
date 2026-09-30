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
 * Output DTO for JobApplication responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class JobApplicationOutputDTO {
    
    private Long applicationId;
    
    private Long jobPostId;
    
    private Long userId;
    
    private String coverLetter;
    
    private Long resumeDocumentId;
    
    private String applicationStatus;
    
    // Format: yyyy-MM-dd'T'HH:mm:ss
    private LocalDateTime appliedAt;
    
    // Format: yyyy-MM-dd'T'HH:mm:ss
    private LocalDateTime statusUpdatedAt;
    
    private Long statusUpdatedByUserId;
    
    private String notes;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
    // Related entities can be included here
}