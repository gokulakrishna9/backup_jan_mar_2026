package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Filter DTO for TrainingExam search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TrainingExamFilterDTO {
    
    // Filter type: EQUALS
    private String title;
    
    // Filter type: EQUALS
    private String description;
    
    // Filter type: EQUALS
    private Integer passingscore;
    
    // Filter type: EQUALS
    private Integer maxscore;
    
    // Filter type: EQUALS
    private Integer timelimitminutes;
    
    // Filter type: EQUALS
    private Integer maxattempts;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}