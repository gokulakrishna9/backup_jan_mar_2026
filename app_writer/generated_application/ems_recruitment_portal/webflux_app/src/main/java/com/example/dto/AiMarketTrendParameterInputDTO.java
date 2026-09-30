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
 * Input DTO for AiMarketTrendParameter creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AiMarketTrendParameterInputDTO {
    
    @NotNull(message = "Parametername is required")
    @Size(max = 150, message = "Parametername cannot exceed 150 characters")
    private String parameterName;
    
    private String parameterValue;
    
    private Long groupId;
    
}