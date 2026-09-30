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
 * Input DTO for ExamAnswer creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ExamAnswerInputDTO {
    
    private String answertext;
    
    private String answercode;
    
    private Boolean iscorrect;
    
    private String explanation;
    
    private Integer sortorder;
    
}