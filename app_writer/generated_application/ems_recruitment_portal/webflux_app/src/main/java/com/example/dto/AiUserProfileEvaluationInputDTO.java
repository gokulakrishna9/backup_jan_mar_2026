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
 * Input DTO for AiUserProfileEvaluation creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AiUserProfileEvaluationInputDTO {
    
    @NotNull(message = "Userid is required")
    private Long userId;
    
    private Long propertyId;
    
    private String evaluationSummary;
    
    private BigDecimal rating;
    
}