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
 * Input DTO for JobInterview creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class JobInterviewInputDTO {
    
    @NotNull(message = "Applicationid is required")
    private Long applicationId;
    
    private String interviewType;
    
    private Integer interviewRound;
    
    @NotNull(message = "Scheduledat is required")
    private LocalDateTime scheduledAt;
    
    private Integer durationMinutes;
    
    @Size(max = 255, message = "Location cannot exceed 255 characters")
    private String location;
    
    @Size(max = 500, message = "Meetinglink cannot exceed 500 characters")
    private String meetingLink;
    
    private Long interviewerUserId;
    
    private String status;
    
    private String feedback;
    
    private BigDecimal rating;
    
}