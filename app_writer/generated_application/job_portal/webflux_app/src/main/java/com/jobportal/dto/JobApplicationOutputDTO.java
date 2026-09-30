package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
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
public class JobApplicationOutputDTO {
    
    private Long jobApplicationId;
    
    private String status;
    
    private String coverletter;
    
    private LocalDateTime appliedat;
    
    private LocalDateTime createdAt;
    
    private LocalDateTime updatedAt;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
}