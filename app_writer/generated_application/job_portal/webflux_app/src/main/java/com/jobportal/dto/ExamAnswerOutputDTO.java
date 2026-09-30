package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Output DTO for ExamAnswer responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ExamAnswerOutputDTO {
    
    private Long examAnswerId;
    
    private String answertext;
    
    private String answercode;
    
    private Boolean iscorrect;
    
    private String explanation;
    
    private Integer sortorder;
    
    private LocalDateTime createdAt;
    
    private LocalDateTime updatedAt;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
}