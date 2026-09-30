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
 * Output DTO for JobInterview responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class JobInterviewOutputDTO {
    
    private Long interviewId;
    
    private Long applicationId;
    
    private String interviewType;
    
    private Integer interviewRound;
    
    // Format: yyyy-MM-dd'T'HH:mm:ss
    private LocalDateTime scheduledAt;
    
    private Integer durationMinutes;
    
    private String location;
    
    private String meetingLink;
    
    private Long interviewerUserId;
    
    private String status;
    
    private String feedback;
    
    private BigDecimal rating;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
    // Related entities can be included here
}