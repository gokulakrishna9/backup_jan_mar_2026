package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for UserAchievement search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserAchievementFilterDTO {
    
    // Filter type: EQUALS
    private Long achievementId;
    
    // Filter type: EQUALS
    private Long userId;
    
    // Filter type: LIKE
    private String title;
    
    // Filter type: LIKE
    private String description;
    
    // Filter type: LIKE
    private String achievementType;
    
    // Filter type: LIKE
    private String issuer;
    
    // Filter type: EQUALS
    private LocalDate dateAchieved;
    
    // Filter type: LIKE
    private String url;
    
    // Filter type: EQUALS
    private Long documentId;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}