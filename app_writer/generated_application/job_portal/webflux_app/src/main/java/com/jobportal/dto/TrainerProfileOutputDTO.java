package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Output DTO for TrainerProfile responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TrainerProfileOutputDTO {
    
    private Long trainerProfileId;
    
    private String specialization;
    
    private String certifications;
    
    private BigDecimal hourlyrate;
    
    private LocalDateTime createdAt;
    
    private LocalDateTime updatedAt;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
}