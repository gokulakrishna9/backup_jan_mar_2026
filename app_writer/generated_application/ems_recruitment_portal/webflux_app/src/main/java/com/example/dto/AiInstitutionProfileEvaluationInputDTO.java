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
 * Input DTO for AiInstitutionProfileEvaluation creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AiInstitutionProfileEvaluationInputDTO {
    
    @NotNull(message = "Institutionid is required")
    private Long institutionId;
    
    private String evaluationSummary;
    
    private BigDecimal rating;
    
}