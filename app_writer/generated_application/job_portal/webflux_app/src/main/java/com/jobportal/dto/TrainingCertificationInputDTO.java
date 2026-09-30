package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import jakarta.validation.constraints.*;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Input DTO for TrainingCertification creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TrainingCertificationInputDTO {
    
    private String certificatenumber;
    
    private String title;
    
    private LocalDateTime issuedat;
    
    private LocalDateTime expiresat;
    
    private String certificateurl;
    
    private String status;
    
}