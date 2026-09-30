package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for JobApplicationAnswer search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class JobApplicationAnswerFilterDTO {
    
    // Filter type: EQUALS
    private Long answerId;
    
    // Filter type: EQUALS
    private Long applicationId;
    
    // Filter type: EQUALS
    private Long questionId;
    
    // Filter type: LIKE
    private String answerText;
    
    // Filter type: EQUALS
    private Long answerFileId;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}