package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for JobPostQuestion search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class JobPostQuestionFilterDTO {
    
    // Filter type: EQUALS
    private Long questionId;
    
    // Filter type: EQUALS
    private Long jobPostId;
    
    // Filter type: LIKE
    private String questionText;
    
    // Filter type: LIKE
    private String questionType;
    
    // Filter type: EQUALS
    private Integer orderSequence;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}