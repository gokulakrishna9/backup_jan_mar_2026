package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import jakarta.validation.constraints.*;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Input DTO for JobApplicationAnswer creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class JobApplicationAnswerInputDTO {
    
    @NotNull(message = "Applicationid is required")
    private Long applicationId;
    
    @NotNull(message = "Questionid is required")
    private Long questionId;
    
    private String answerText;
    
    private Long answerFileId;
    
}