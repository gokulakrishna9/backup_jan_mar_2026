package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Output DTO for TrainingProgram responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TrainingProgramOutputDTO {
    
    private Long trainingProgramId;
    
    private String title;
    
    private String description;
    
    private Integer durationdays;
    
    private BigDecimal price;
    
    private Boolean isactive;
    
    private LocalDateTime createdAt;
    
    private LocalDateTime updatedAt;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
}