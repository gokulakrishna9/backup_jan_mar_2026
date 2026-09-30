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
 * Input DTO for AiCommunityPostEvaluation creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AiCommunityPostEvaluationInputDTO {
    
    @NotNull(message = "Postid is required")
    private Long postId;
    
    private String evaluationSummary;
    
    private BigDecimal rating;
    
}