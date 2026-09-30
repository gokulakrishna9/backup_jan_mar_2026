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
 * Input DTO for TrainingExam creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TrainingExamInputDTO {
    
    private String title;
    
    private String description;
    
    private Integer passingscore;
    
    private Integer maxscore;
    
    private Integer timelimitminutes;
    
    private Integer maxattempts;
    
}