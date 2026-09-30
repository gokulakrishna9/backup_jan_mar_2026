package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Output DTO for ExamQuestion responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ExamQuestionOutputDTO {
    
    private Long examQuestionId;
    
    private String questiontext;
    
    private String questioncode;
    
    private String questiontype;
    
    private Integer points;
    
    private Integer sortorder;
    
    private LocalDateTime createdAt;
    
    private LocalDateTime updatedAt;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
}