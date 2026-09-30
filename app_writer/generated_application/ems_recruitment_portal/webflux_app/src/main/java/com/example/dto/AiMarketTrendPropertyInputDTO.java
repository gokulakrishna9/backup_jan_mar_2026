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
 * Input DTO for AiMarketTrendProperty creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AiMarketTrendPropertyInputDTO {
    
    @NotNull(message = "Trendname is required")
    @Size(max = 255, message = "Trendname cannot exceed 255 characters")
    private String trendName;
    
    private String trendDescription;
    
}