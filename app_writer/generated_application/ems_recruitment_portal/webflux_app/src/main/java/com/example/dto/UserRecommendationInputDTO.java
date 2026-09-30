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
 * Input DTO for UserRecommendation creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserRecommendationInputDTO {
    
    @NotNull(message = "Userid is required")
    private Long userId;
    
    @NotNull(message = "Recommendedbyuserid is required")
    private Long recommendedByUserId;
    
    @NotNull(message = "Recommendationtext is required")
    private String recommendationText;
    
    @Size(max = 100, message = "Relationship cannot exceed 100 characters")
    private String relationship;
    
    @Size(max = 255, message = "Positionattime cannot exceed 255 characters")
    private String positionAtTime;
    
    private Byte isVisible;
    
}