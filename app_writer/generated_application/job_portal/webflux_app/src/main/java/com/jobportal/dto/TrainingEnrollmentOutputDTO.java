package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Output DTO for TrainingEnrollment responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TrainingEnrollmentOutputDTO {
    
    private Long trainingEnrollmentId;
    
    private String status;
    
    private Integer progress;
    
    private LocalDateTime enrolledat;
    
    private LocalDateTime createdAt;
    
    private LocalDateTime updatedAt;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
}