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
 * Input DTO for UserAchievement creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserAchievementInputDTO {
    
    @NotNull(message = "Userid is required")
    private Long userId;
    
    @NotNull(message = "Title is required")
    @Size(max = 255, message = "Title cannot exceed 255 characters")
    private String title;
    
    private String description;
    
    @Size(max = 100, message = "Achievementtype cannot exceed 100 characters")
    private String achievementType;
    
    @Size(max = 255, message = "Issuer cannot exceed 255 characters")
    private String issuer;
    
    private LocalDate dateAchieved;
    
    @Size(max = 500, message = "Url cannot exceed 500 characters")
    private String url;
    
    private Long documentId;
    
}