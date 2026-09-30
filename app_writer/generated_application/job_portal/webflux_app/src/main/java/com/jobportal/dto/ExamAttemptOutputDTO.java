package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Output DTO for ExamAttempt responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ExamAttemptOutputDTO {
    
    private Long examAttemptId;
    
    private Integer score;
    
    private Boolean passed;
    
    private LocalDateTime startedat;
    
    private LocalDateTime completedat;
    
    private Integer attemptnumber;
    
    private LocalDateTime createdAt;
    
    private LocalDateTime updatedAt;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
}