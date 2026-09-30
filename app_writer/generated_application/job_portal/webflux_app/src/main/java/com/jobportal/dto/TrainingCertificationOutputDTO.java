package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Output DTO for TrainingCertification responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TrainingCertificationOutputDTO {
    
    private Long trainingCertificationId;
    
    private String certificatenumber;
    
    private String title;
    
    private LocalDateTime issuedat;
    
    private LocalDateTime expiresat;
    
    private String certificateurl;
    
    private String status;
    
    private LocalDateTime createdAt;
    
    private LocalDateTime updatedAt;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
}