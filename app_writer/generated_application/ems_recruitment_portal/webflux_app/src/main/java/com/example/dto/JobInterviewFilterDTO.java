package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for JobInterview search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class JobInterviewFilterDTO {
    
    // Filter type: EQUALS
    private Long interviewId;
    
    // Filter type: EQUALS
    private Long applicationId;
    
    // Filter type: LIKE
    private String interviewType;
    
    // Filter type: EQUALS
    private Integer interviewRound;
    
    // Filter type: EQUALS
    private LocalDateTime scheduledAt;
    
    // Filter type: EQUALS
    private Integer durationMinutes;
    
    // Filter type: LIKE
    private String location;
    
    // Filter type: LIKE
    private String meetingLink;
    
    // Filter type: EQUALS
    private Long interviewerUserId;
    
    // Filter type: LIKE
    private String status;
    
    // Filter type: LIKE
    private String feedback;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}