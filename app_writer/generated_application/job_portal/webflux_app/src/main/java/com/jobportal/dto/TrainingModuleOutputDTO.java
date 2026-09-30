package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Output DTO for TrainingModule responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TrainingModuleOutputDTO {
    
    private Long trainingModuleId;
    
    private String title;
    
    private String description;
    
    private Integer moduleorder;
    
    private Integer durationminutes;
    
    private String contenturl;
    
    private LocalDateTime createdAt;
    
    private LocalDateTime updatedAt;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
}