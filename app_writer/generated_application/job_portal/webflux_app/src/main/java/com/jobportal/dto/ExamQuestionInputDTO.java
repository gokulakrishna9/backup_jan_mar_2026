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
 * Input DTO for ExamQuestion creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ExamQuestionInputDTO {
    
    private String questiontext;
    
    private String questioncode;
    
    private String questiontype;
    
    private Integer points;
    
    private Integer sortorder;
    
}