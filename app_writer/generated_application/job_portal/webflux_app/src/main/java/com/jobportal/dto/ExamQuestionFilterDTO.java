package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Filter DTO for ExamQuestion search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ExamQuestionFilterDTO {
    
    // Filter type: EQUALS
    private String questiontext;
    
    // Filter type: EQUALS
    private String questioncode;
    
    // Filter type: EQUALS
    private String questiontype;
    
    // Filter type: EQUALS
    private Integer points;
    
    // Filter type: EQUALS
    private Integer sortorder;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}