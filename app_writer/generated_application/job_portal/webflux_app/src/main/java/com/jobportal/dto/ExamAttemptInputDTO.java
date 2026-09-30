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
 * Input DTO for ExamAttempt creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ExamAttemptInputDTO {
    
    private Integer score;
    
    private Boolean passed;
    
    private LocalDateTime startedat;
    
    private LocalDateTime completedat;
    
    private Integer attemptnumber;
    
}