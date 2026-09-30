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
 * Input DTO for TrainingModule creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TrainingModuleInputDTO {
    
    private String title;
    
    private String description;
    
    private Integer moduleorder;
    
    private Integer durationminutes;
    
    private String contenturl;
    
}