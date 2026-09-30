package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Filter DTO for ExamAttempt search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ExamAttemptFilterDTO {
    
    // Filter type: EQUALS
    private Integer score;
    
    // Filter type: EQUALS
    private Boolean passed;
    
    // Filter type: EQUALS
    private LocalDateTime startedat;
    
    // Filter type: EQUALS
    private LocalDateTime completedat;
    
    // Filter type: EQUALS
    private Integer attemptnumber;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}