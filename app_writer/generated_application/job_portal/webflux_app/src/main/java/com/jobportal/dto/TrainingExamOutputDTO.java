package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Output DTO for TrainingExam responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TrainingExamOutputDTO {
    
    private Long trainingExamId;
    
    private String title;
    
    private String description;
    
    private Integer passingscore;
    
    private Integer maxscore;
    
    private Integer timelimitminutes;
    
    private Integer maxattempts;
    
    private LocalDateTime createdAt;
    
    private LocalDateTime updatedAt;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
}