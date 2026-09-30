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
 * Input DTO for AiJobRecommendation creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AiJobRecommendationInputDTO {
    
    @NotNull(message = "Jobpostid is required")
    private Long jobPostId;
    
    @NotNull(message = "Profileid is required")
    private Long profileId;
    
    private BigDecimal preferenceRating;
    
    private String recommendationSummary;
    
}