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
 * Input DTO for ModuleProgress creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ModuleProgressInputDTO {
    
    private String status;
    
    private LocalDateTime completedat;
    
    private Integer progresspercent;
    
}