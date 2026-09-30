package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Filter DTO for ExamAnswer search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ExamAnswerFilterDTO {
    
    // Filter type: EQUALS
    private String answertext;
    
    // Filter type: EQUALS
    private String answercode;
    
    // Filter type: EQUALS
    private Boolean iscorrect;
    
    // Filter type: EQUALS
    private String explanation;
    
    // Filter type: EQUALS
    private Integer sortorder;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}