package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Output DTO for ModuleProgress responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ModuleProgressOutputDTO {
    
    private Long moduleProgressId;
    
    private String status;
    
    private LocalDateTime completedat;
    
    private Integer progresspercent;
    
    private LocalDateTime createdAt;
    
    private LocalDateTime updatedAt;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
}